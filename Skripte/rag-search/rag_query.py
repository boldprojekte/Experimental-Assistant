#!/usr/bin/env python3
"""
RAG Query Script
Query documents from Qdrant vector database using LlamaIndex hybrid search.

Features:
- Automatic re-indexing if files changed
- Hybrid search (dense + sparse embeddings)
- Filter by subdirectory
- Formatted results with source metadata

Usage:
    python rag_query.py "your question" [--subdir path] [--top-k N] [--docs-path PATH]

Examples:
    # Basic query
    python rag_query.py "What is machine learning?"

    # Query with subdirectory filter
    python rag_query.py "Explain the architecture" --subdir "research/papers"

    # Custom top-k results
    python rag_query.py "Best practices" --top-k 10

    # Custom documents path
    python rag_query.py "query" --docs-path /path/to/docs
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, List

# Load environment variables from script directory
from dotenv import load_dotenv

# Get script directory and load .env
__file__ = Path(__file__).resolve()
SCRIPT_DIR = __file__.parent
load_dotenv(SCRIPT_DIR / '.env')

# LlamaIndex imports
from llama_index.core import VectorStoreIndex, Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.postprocessor.cohere_rerank import CohereRerank
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue


class RAGQuery:
    """Handles RAG queries with auto-reindexing"""

    def __init__(self, docs_path: Optional[str] = None):
        """Initialize query engine"""
        # Set docs path
        if docs_path:
            self.docs_path = Path(docs_path).resolve()
        else:
            self.docs_path = SCRIPT_DIR.parent.parent / "Dokumente" / "03_RAG"

        # Setup clients
        self._setup_clients()

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

        # Create vector store with hybrid search
        self.vector_store = QdrantVectorStore(
            client=self.qdrant_client,
            collection_name=self.collection_name,
            enable_hybrid=True,
            fastembed_sparse_model="Qdrant/bm42-all-minilm-l6-v2-attentions"
        )

    def check_and_reindex(self):
        """Check if files changed and reindex if needed"""
        print("🔍 Checking for file changes...")

        # Import indexer
        from rag_index import DocumentIndexer

        indexer = DocumentIndexer(str(self.docs_path))
        changed_files = indexer.get_changed_files()

        if changed_files:
            print(f"⚠️  {len(changed_files)} files have changed. Re-indexing...")
            indexer.index_documents()
            print("✓ Re-indexing complete\n")
        else:
            print("✓ All files up to date\n")

    def query(
        self,
        question: str,
        subdirectory: Optional[str] = None,
        similarity_top_k: Optional[int] = None,
        sparse_top_k: Optional[int] = None
    ) -> List:
        """
        Query the RAG system (retrieval only, no LLM generation)

        Args:
            question: The query string
            subdirectory: Optional filter for subdirectory
            similarity_top_k: Number of final results to return (defaults from ENV)
            sparse_top_k: Number of results from each sparse/dense search (defaults from ENV)

        Returns:
            List of retrieved nodes with scores and metadata
        """

        # Load defaults from ENV if not provided
        if similarity_top_k is None:
            similarity_top_k = int(os.getenv('RAG_SIMILARITY_TOP_K', '5'))
        if sparse_top_k is None:
            sparse_top_k = int(os.getenv('RAG_SPARSE_TOP_K', '12'))

        # Create index from existing vector store
        index = VectorStoreIndex.from_vector_store(self.vector_store)

        # Build filters if subdirectory specified
        vector_store_kwargs = {}
        if subdirectory:
            # Qdrant filter for metadata
            qdrant_filters = Filter(
                must=[
                    FieldCondition(
                        key="subdirectory",
                        match=MatchValue(value=subdirectory)
                    )
                ]
            )
            vector_store_kwargs = {"qdrant_filters": qdrant_filters}

        # Check if Cohere Reranker is enabled
        use_rerank = os.getenv('USE_COHERE_RERANK', 'false').lower() == 'true'
        cohere_rerank = None
        rerank_candidates = similarity_top_k

        if use_rerank:
            cohere_api_key = os.getenv('COHERE_API_KEY')
            if cohere_api_key:
                # Get reranking parameters from ENV
                rerank_top_n = int(os.getenv('RAG_RERANK_TOP_N', str(similarity_top_k)))
                rerank_candidates = int(os.getenv('RAG_RERANK_CANDIDATES', str(similarity_top_k * 2)))

                cohere_rerank = CohereRerank(
                    api_key=cohere_api_key,
                    top_n=rerank_top_n,  # Final number after reranking
                    model="rerank-english-v3.0"  # Latest model (2024)
                )
                # Fetch more candidates for reranking
                similarity_top_k = rerank_candidates

        # Create retriever (no LLM, just chunks)
        retriever = index.as_retriever(
            similarity_top_k=similarity_top_k,
            sparse_top_k=sparse_top_k,
            vector_store_kwargs=vector_store_kwargs
        )

        # Execute query
        print(f"💬 Query: {question}")
        if subdirectory:
            print(f"📁 Filter: subdirectory = '{subdirectory}'")
        if use_rerank:
            print(f"🎯 Reranking: Enabled (Cohere rerank-english-v3.0)")
            print(f"   Candidates: {rerank_candidates} → Final: {rerank_top_n}")
        print(f"🔎 Searching (hybrid: dense + sparse)...\n")

        # Retrieve nodes (no LLM generation)
        nodes = retriever.retrieve(question)

        # Apply Cohere reranking manually if enabled
        if cohere_rerank:
            nodes = cohere_rerank.postprocess_nodes(nodes, query_str=question)

        return nodes

    def format_response(self, nodes, show_sources: bool = True):
        """Format and print retrieved nodes (no LLM answer)"""
        # Get score threshold from ENV
        score_threshold = float(os.getenv('RAG_SCORE_THRESHOLD', '0.3'))

        if show_sources and nodes:
            # Filter nodes by score threshold
            filtered_nodes = [
                node for node in nodes
                if hasattr(node, 'score') and node.score >= score_threshold
            ]

            if not filtered_nodes:
                print("=" * 80)
                print("⚠️  NO RELEVANT SOURCES FOUND")
                print("=" * 80)
                print(f"No sources with score >= {score_threshold} found.")
                print("This may indicate the query is not relevant to the indexed documents.\n")
                return

            print("=" * 80)
            print(f"📚 RETRIEVED {len(filtered_nodes)} CHUNKS")
            print("=" * 80)

            for idx, node in enumerate(filtered_nodes, 1):
                score = node.score if hasattr(node, 'score') else 'N/A'
                filename = node.metadata.get('filename', 'Unknown')
                subdirectory = node.metadata.get('subdirectory', 'root')

                print(f"\n[{idx}] {filename} ({subdirectory})")
                print(f"    Score: {score}")
                print(f"    Text: {node.text[:200]}...")
                print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Query documents using RAG with hybrid search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python rag_query.py "What is machine learning?"
  python rag_query.py "Explain the architecture" --subdir research/papers
  python rag_query.py "Best practices" --top-k 10
        """
    )

    parser.add_argument(
        'question',
        type=str,
        help='The question to ask'
    )

    parser.add_argument(
        '--subdir',
        type=str,
        default=None,
        help='Filter results by subdirectory (e.g., "research/papers")'
    )

    parser.add_argument(
        '--top-k',
        type=int,
        default=5,
        help='Number of results to return (default: 5)'
    )

    parser.add_argument(
        '--sparse-top-k',
        type=int,
        default=12,
        help='Number of results from each sparse/dense search (default: 12)'
    )

    parser.add_argument(
        '--docs-path',
        type=str,
        default=None,
        help='Path to documents directory (default: Dokumente/03_RAG)'
    )

    parser.add_argument(
        '--no-reindex-check',
        action='store_true',
        help='Skip checking for file changes before querying'
    )

    parser.add_argument(
        '--no-sources',
        action='store_true',
        help='Hide source information in output'
    )

    args = parser.parse_args()

    # Create query engine
    print(f"🔧 Loading configuration from: {SCRIPT_DIR / '.env'}\n")

    rag = RAGQuery(docs_path=args.docs_path)

    # Check for changes and reindex if needed
    if not args.no_reindex_check:
        rag.check_and_reindex()

    # Execute query
    try:
        nodes = rag.query(
            question=args.question,
            subdirectory=args.subdir,
            similarity_top_k=args.top_k,
            sparse_top_k=args.sparse_top_k
        )

        # Format and display nodes
        rag.format_response(nodes, show_sources=not args.no_sources)

    except Exception as e:
        print(f"❌ Error during query: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
