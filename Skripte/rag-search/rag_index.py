#!/usr/bin/env python3
"""
RAG Index Script
Indexes documents from a directory into Qdrant vector database using LlamaIndex.

Features:
- Smart file change detection (only re-indexes changed files)
- Hybrid search (dense + sparse embeddings)
- Recursive directory scanning with subdirectory metadata
- Supports: Markdown, PDF, DOCX, PPTX, TXT, and more
- Optional LlamaParse for advanced PDF parsing

Usage:
    python rag_index.py [path_to_documents]

Example:
    python rag_index.py /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Dokumente/03_RAG
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Load environment variables from script directory
from dotenv import load_dotenv
from urllib.parse import urlparse

# Get script directory and load .env
__file__ = Path(__file__).resolve()
SCRIPT_DIR = __file__.parent
load_dotenv(SCRIPT_DIR / '.env')

# LlamaIndex imports
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from qdrant_client import QdrantClient


class DocumentIndexer:
    """Handles document indexing with file change detection"""

    METADATA_FILE = "rag_metadata.json"

    def __init__(self, docs_path: str, silent: bool = False):
        """Initialize indexer with document path"""
        self.docs_path = Path(docs_path).resolve()
        # Store metadata in script directory instead of docs directory
        self.metadata_path = SCRIPT_DIR / self.METADATA_FILE
        self.file_metadata = self._load_metadata()
        self.silent = silent

        # Setup LlamaIndex components
        self._setup_clients()

    def _load_metadata(self) -> Dict:
        """Load file metadata from JSON"""
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_metadata(self):
        """Save file metadata to JSON"""
        with open(self.metadata_path, 'w') as f:
            json.dump(self.file_metadata, f, indent=2)

    def _get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _file_changed(self, file_path: Path) -> bool:
        """Check if file has changed since last index"""
        rel_path = str(file_path.relative_to(self.docs_path))

        # New file
        if rel_path not in self.file_metadata:
            return True

        old_meta = self.file_metadata[rel_path]
        stat = file_path.stat()

        # Quick check: mtime or size changed
        if (old_meta.get('mtime') != stat.st_mtime or
            old_meta.get('size') != stat.st_size):
            # Verify with hash
            current_hash = self._get_file_hash(file_path)
            return current_hash != old_meta.get('hash')

        return False

    def _update_file_metadata(self, file_path: Path):
        """Update metadata for a file"""
        rel_path = str(file_path.relative_to(self.docs_path))
        stat = file_path.stat()

        self.file_metadata[rel_path] = {
            'mtime': stat.st_mtime,
            'size': stat.st_size,
            'hash': self._get_file_hash(file_path),
            'indexed_at': datetime.now().isoformat()
        }

    def _setup_clients(self):
        """Setup Qdrant and OpenAI clients"""
        # Qdrant client
        qdrant_url = os.getenv('QDRANT_URL')
        qdrant_api_key = os.getenv('QDRANT_API_KEY')
        self.collection_name = os.getenv('QDRANT_COLLECTION', 'documents')

        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )

        # Setup embeddings
        Settings.embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=os.getenv('OPENAI_API_KEY')
        )

        # Setup text splitter (markdown-aware + semantic chunking)
        min_chunk_size = int(os.getenv('RAG_MIN_CHUNK_SIZE', '400'))
        max_chunk_size = int(os.getenv('RAG_MAX_CHUNK_SIZE', '800'))
        chunk_overlap = int(os.getenv('RAG_CHUNK_OVERLAP', '80'))

        use_semantic_chunking = os.getenv('USE_SEMANTIC_CHUNKING', 'false').lower() == 'true'

        if use_semantic_chunking:
            from llama_index.core.node_parser import SemanticSplitterNodeParser

            if not self.silent:
                print("✓ Using Semantic Chunking (adaptive breakpoints)")

            # Semantic Splitter für optimale Chunk-Grenzen
            Settings.node_parser = SemanticSplitterNodeParser(
                buffer_size=1,
                breakpoint_percentile_threshold=int(os.getenv('SEMANTIC_THRESHOLD', '95')),
                embed_model=Settings.embed_model
            )
        else:
            from llama_index.core.node_parser import SentenceSplitter

            if not self.silent:
                print(f"✓ Using SentenceSplitter (token-based: {min_chunk_size}-{max_chunk_size} tokens)")

            # SentenceSplitter mit Token-Limit und Markdown-Awareness
            # Respektiert Absätze durch paragraph_separator
            avg_chunk_size = (min_chunk_size + max_chunk_size) // 2
            Settings.node_parser = SentenceSplitter(
                chunk_size=avg_chunk_size,      # Mittelwert (z.B. 600 tokens)
                chunk_overlap=chunk_overlap,
                separator="\n\n",                # Respektiert Markdown-Absätze
                paragraph_separator="\n\n\n"    # Respektiert größere Breaks (z.B. zwischen Sections)
            )

        # Create vector store with hybrid search
        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            enable_hybrid=True,
            batch_size=20,
            fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions"
        )

    def _get_file_extractor(self):
        """Get file extractor configuration"""
        use_llama_parse = os.getenv('USE_LLAMA_PARSE', 'false').lower() == 'true'

        if use_llama_parse:
            try:
                from llama_parse import LlamaParse

                parser = LlamaParse(
                    api_key=os.getenv('LLAMA_CLOUD_API_KEY'),
                    result_type="markdown",
                    verbose=True
                )

                print("✓ LlamaParse enabled for PDF processing")
                return {".pdf": parser}
            except Exception as e:
                print(f"⚠ LlamaParse setup failed: {e}")
                print("  Falling back to default PDF parser")
                return None

        return None

    def _delete_chunks_from_qdrant(self, filename: str):
        """Delete all chunks of a specific file from Qdrant"""
        from qdrant_client.models import Filter, FieldCondition, MatchValue

        # Delete points where metadata.filename matches
        self.qdrant_client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="filename",
                        match=MatchValue(value=filename)
                    )
                ]
            )
        )

    def get_changed_files(self) -> List[Path]:
        """Get list of files that have changed"""
        changed_files = []
        deleted_files_list = []

        # Track current files
        current_files = set()

        # Scan all supported files
        for file_path in self.docs_path.rglob('*'):
            if file_path.is_file() and file_path.name != self.METADATA_FILE:
                # Skip hidden files
                if file_path.name.startswith('.'):
                    continue

                rel_path = str(file_path.relative_to(self.docs_path))
                current_files.add(rel_path)

                if self._file_changed(file_path):
                    changed_files.append(file_path)

        # Check for deleted files
        deleted_files = set(self.file_metadata.keys()) - current_files
        if deleted_files:
            print(f"\n🗑️  Found {len(deleted_files)} deleted files:")
            for f in deleted_files:
                print(f"  - {f}")
                # Extract just the filename for Qdrant deletion
                filename = Path(f).name
                deleted_files_list.append(filename)
                # Remove from metadata
                del self.file_metadata[f]

            # Delete chunks from Qdrant
            print(f"🧹 Removing chunks from Qdrant...")
            for filename in deleted_files_list:
                try:
                    self._delete_chunks_from_qdrant(filename)
                    print(f"  ✓ Deleted chunks for: {filename}")
                except Exception as e:
                    print(f"  ⚠️  Failed to delete {filename}: {e}")

            # Save metadata after deletion
            self._save_metadata()

        return changed_files

    def index_documents(self, force_reindex: bool = False):
        """Index documents with change detection"""

        if force_reindex:
            print("🔄 Force re-index enabled")
            self.file_metadata = {}
            # Clear entire collection on force reindex
            print("🧹 Clearing entire collection...")
            try:
                self.qdrant_client.delete_collection(collection_name=self.collection_name)
                print("  ✓ Collection cleared")
            except Exception as e:
                print(f"  ⚠️  Collection might not exist: {e}")

            # Reinitialize vector store to recreate collection
            print("🔧 Reinitializing vector store...")
            self.vector_store = QdrantVectorStore(
                client=self.qdrant_client,
                collection_name=self.collection_name,
                enable_hybrid=True,
                batch_size=20,
                fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions"
            )

        # Check for changes
        changed_files = self.get_changed_files()

        # If only deletions happened (no changed files and no force reindex)
        if not changed_files and not force_reindex:
            print("✓ All files up to date. No indexing needed.")
            return

        # If no files to index (e.g., folder is empty)
        if not changed_files and force_reindex:
            # Check if folder has any files
            all_files = list(self.docs_path.rglob('*'))
            file_count = len([f for f in all_files if f.is_file() and not f.name.startswith('.')])
            if file_count == 0:
                print("📭 No documents found in directory. Collection cleared.")
                return

        if changed_files:
            print(f"\n📄 Found {len(changed_files)} files to index:")
            for f in changed_files:
                rel_path = f.relative_to(self.docs_path)
                print(f"  - {rel_path}")

            # Delete old chunks of changed files from Qdrant
            print(f"\n🧹 Removing old chunks of changed files from Qdrant...")
            for file_path in changed_files:
                filename = file_path.name
                try:
                    self._delete_chunks_from_qdrant(filename)
                    print(f"  ✓ Deleted old chunks for: {filename}")
                except Exception as e:
                    print(f"  ⚠️  Failed to delete {filename}: {e}")

        print(f"\n🔍 Loading documents...")

        # Load documents with metadata
        file_extractor = self._get_file_extractor()

        # Load only changed files (or all if force reindex)
        if force_reindex:
            documents = SimpleDirectoryReader(
                input_dir=str(self.docs_path),
                recursive=True,
                required_exts=None,
                file_extractor=file_extractor,
                exclude_hidden=True
            ).load_data()
        else:
            # Load only changed files
            documents = SimpleDirectoryReader(
                input_files=[str(f) for f in changed_files],
                file_extractor=file_extractor
            ).load_data()

        # Add subdirectory metadata
        for doc in documents:
            file_path = Path(doc.metadata.get('file_path', ''))
            if file_path.exists():
                rel_path = file_path.relative_to(self.docs_path)
                doc.metadata['subdirectory'] = str(rel_path.parent) if rel_path.parent != Path('.') else 'root'
                doc.metadata['filename'] = file_path.name

        print(f"✓ Loaded {len(documents)} document chunks")

        # Create index with hybrid search
        print(f"\n🚀 Creating index with hybrid search...")

        storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
            show_progress=True
        )

        print(f"✓ Index created successfully")

        # Create payload indexes for metadata filtering
        print(f"\n🔧 Creating payload indexes for filtering...")
        from qdrant_client.models import PayloadSchemaType

        self.qdrant_client.create_payload_index(
            collection_name=self.collection_name,
            field_name="subdirectory",
            field_schema=PayloadSchemaType.KEYWORD
        )

        self.qdrant_client.create_payload_index(
            collection_name=self.collection_name,
            field_name="filename",
            field_schema=PayloadSchemaType.KEYWORD
        )

        print(f"✓ Payload indexes created (subdirectory, filename)")

        # Update metadata for all changed files
        for file_path in changed_files:
            self._update_file_metadata(file_path)

        self._save_metadata()
        print(f"✓ Metadata saved")

        print(f"\n✅ Indexing complete!")
        print(f"   Collection: {self.collection_name}")
        print(f"   Documents: {len(documents)} chunks")
        print(f"   Hybrid Search: Enabled (Dense + Sparse)")


def main():
    """Main entry point"""

    # Check for force reindex flag first
    force_reindex = '--force' in sys.argv

    # Get documents path from args or use default
    # Filter out --force flag from args
    args = [arg for arg in sys.argv[1:] if arg != '--force']

    if len(args) > 0:
        docs_path = Path(args[0]).resolve()
    else:
        # Default path
        docs_path = Path(__file__).resolve().parent.parent.parent / "Dokumente" / "03_RAG"

    # Validate path
    if not docs_path.exists():
        print(f"❌ Error: Path does not exist: {docs_path}")
        print(f"\nUsage: python rag_index.py [path_to_documents] [--force]")
        sys.exit(1)

    if not docs_path.is_dir():
        print(f"❌ Error: Path is not a directory: {docs_path}")
        sys.exit(1)

    print(f"📁 Document path: {docs_path}")
    print(f"🔧 Loading configuration from: {SCRIPT_DIR / '.env'}")

    # Create indexer and run
    indexer = DocumentIndexer(docs_path)
    indexer.index_documents(force_reindex=force_reindex)


if __name__ == '__main__':
    main()
