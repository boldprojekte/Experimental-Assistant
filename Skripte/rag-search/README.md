# RAG Search

Intelligent document search using Retrieval-Augmented Generation with hybrid search (dense + sparse embeddings).

## Features

- **Hybrid Search**: Combines semantic (OpenAI embeddings) + keyword (BM42) search with Relative Score Fusion
- **Cohere Reranking**: Optional ML-based reranking for significantly improved relevance (rerank-english-v3.0)
- **Smart Indexing**: Auto-detects changed, new, and deleted files - only re-indexes what's needed
- **Intelligent Cleanup**: Automatically removes old chunks from Qdrant when files are changed or deleted
- **Score Threshold Filtering**: Only returns results above configurable relevance score (default 0.2)
- **Token-Based Chunking**: Intelligent chunking with configurable size (400-800 tokens) and markdown-awareness
- **JSON Output**: Structured JSON output for reliable parsing by AI agents (`--json` flag)
- **Multi-Format Support**: Markdown, PDF, DOCX, PPTX, TXT, and more
- **LlamaParse Integration**: Optional advanced PDF parsing for complex documents
- **Metadata Filtering**: Filter results by subdirectory or filename
- **Configurable via ENV**: Chunk size, overlap, retrieval parameters, reranking, and score threshold
- **Location Independent**: Run from any directory
- **Cross-Platform**: Works on Windows + macOS

## Prerequisites

- Python 3.12+
- Qdrant Cloud account (or self-hosted instance)
- OpenAI API key
- Cohere API key (optional, for reranking)
- LlamaParse API key (optional, for advanced PDF parsing)

## Installation

```bash
cd Skripte/rag-search/
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your API keys and adjust settings:

```bash
# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_COLLECTION=documents

# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-openai-api-key

# Cohere Configuration (optional - for reranking)
COHERE_API_KEY=your-cohere-api-key
USE_COHERE_RERANK=false  # Set to true to enable ML-based reranking

# LlamaParse Configuration (optional - for advanced PDF parsing)
LLAMA_CLOUD_API_KEY=llx-your-llamaparse-api-key
USE_LLAMA_PARSE=false  # Set to true for advanced PDF parsing

# RAG Configuration (tunable)
RAG_MIN_CHUNK_SIZE=400        # Minimum chunk size in tokens
RAG_MAX_CHUNK_SIZE=800        # Maximum chunk size in tokens (system uses average: 600)
RAG_CHUNK_OVERLAP=80          # Token overlap between chunks (13% at 600 tokens)
RAG_SIMILARITY_TOP_K=5        # Final number of results to return
RAG_SPARSE_TOP_K=12           # BM25 candidates before hybrid fusion
RAG_SCORE_THRESHOLD=0.2       # Minimum relevance score (0.0-1.0)
RAG_RERANK_TOP_N=5            # Final results after Cohere reranking
RAG_RERANK_CANDIDATES=20      # Candidates sent to Cohere (higher = better quality)

# Chunking Strategy
USE_SEMANTIC_CHUNKING=false   # true = semantic (slow), false = token-based with markdown respect (fast)
SEMANTIC_THRESHOLD=95         # Breakpoint percentile for semantic chunking (90-99)
```

## Usage

**Can be run from any directory**

### Indexing Documents

```bash
# Index default directory (Dokumente/03_RAG)
python rag_index.py

# Index custom directory
python rag_index.py /path/to/documents

# Force complete re-index (clears Qdrant collection)
python rag_index.py --force
```

**What happens during indexing:**
1. Scans directory recursively for documents
2. **Detects deleted files** → Removes chunks from Qdrant
3. **Detects changed files** → Deletes old chunks, indexes new version
4. **Detects new files** → Indexes them
5. Loads documents with SimpleDirectoryReader (auto-detects file types)
6. Chunks text intelligently (sentence-aware, configurable size)
7. Generates embeddings (OpenAI text-embedding-3-small)
8. Stores in Qdrant with hybrid search enabled (BM42 + Dense vectors)
9. Creates payload indexes for metadata filtering

**Smart Change Detection:**
- Uses metadata file (`rag_metadata.json` in script directory)
- Quick check via `mtime` + `size`
- Hash verification (MD5) on changes
- Only changed/new/deleted files are processed

### Querying

```bash
# Basic query (auto re-indexes if files changed)
python rag_query.py "What is machine learning?"

# Filter by subdirectory
python rag_query.py "Explain the architecture" --subdir research

# Custom number of results
python rag_query.py "Best practices" --top-k 10

# Adjust sparse search results (more keyword focus)
python rag_query.py "query" --sparse-top-k 20

# Custom documents path
python rag_query.py "query" --docs-path /path/to/docs

# Skip re-index check (faster, use when you know files haven't changed)
python rag_query.py "query" --no-reindex-check

# Hide source information
python rag_query.py "query" --no-sources

# JSON output (for AI agents and automation)
python rag_query.py "query" --json
```

### JSON Output Format

When using `--json` flag, the output is structured JSON with complete chunk text:

```json
{
  "status": "success",
  "count": 3,
  "score_threshold": 0.2,
  "chunks": [
    {
      "text": "Complete chunk text without truncation...",
      "score": 0.9935,
      "metadata": {
        "filename": "document.pdf",
        "subdirectory": "topic",
        "file_path": "/absolute/path/to/document.pdf"
      }
    }
  ]
}
```

**Benefits of JSON mode:**
- ✅ **Complete text**: No truncation, full chunk content
- ✅ **Reliable parsing**: Structured data, no regex needed
- ✅ **Silent mode**: No log messages, pure JSON output
- ✅ **AI-friendly**: Designed for programmatic consumption

**Query process:**
1. **Auto re-index check**: Detects changes/deletions and updates Qdrant
2. Generates query embedding (OpenAI)
3. **Hybrid search** (Relative Score Fusion):
   - Sparse search (BM42): Retrieves `sparse_top_k` results (keyword matching)
   - Dense search (Semantic): Retrieves `sparse_top_k` results (semantic similarity)
   - Fusion: Merges both result sets using Relative Score Fusion
4. **Optional Cohere Reranking**: ML-based reranking of candidates
5. **Score Threshold Filter**: Only returns chunks above minimum score
6. Returns relevant chunks with scores and metadata (no LLM generation)

## AI Agent Examples

```bash
# Index research papers
python /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/rag-search/rag_index.py \
  /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Dokumente/03_RAG

# Query about specific topic
python /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/rag-search/rag_query.py \
  "What are the key findings about reinforcement learning?" \
  --top-k 5

# Search within specific folder
python /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/rag-search/rag_query.py \
  "Hybrid search implementation details" \
  --subdir research/papers
```

## How It Works

### Architecture

```
Documents → SimpleDirectoryReader → SentenceSplitter (chunks) → OpenAI Embeddings
                                                                        ↓
                                              Qdrant (Dense + Sparse Vectors)
                                                                        ↓
Query → OpenAI Embeddings → Hybrid Search (Fusion) → Cohere Reranking → Threshold Filter
                                                                        ↓
                                              Retrieved Chunks (with scores & metadata)
```

**Note:** This tool returns **chunks only** (no LLM generation). The AI agent processes chunks directly for optimal token efficiency.

### Smart File Management

**Change Detection:**
- Metadata stored in `Skripte/rag-search/rag_metadata.json`
- Tracks: `mtime`, `size`, `hash`, `indexed_at`
- Quick check: Compare `mtime` + `size` (fast)
- Verification: MD5 hash on suspected changes (accurate)

**Qdrant Cleanup:**
- **Deleted files**: Automatically removes all chunks from Qdrant
- **Changed files**: Deletes old chunks before indexing new version
- **Force re-index**: Clears entire collection

### Hybrid Search with Relative Score Fusion

Uses **Relative Score Fusion** to combine dense and sparse search results.

**How it works:**
- Normalizes scores from both searches (0-1 range)
- Combines using weighted sum: `fused_score = alpha * (sparse_norm + dense_norm)`
- Default `alpha = 0.5` balances both methods equally

**Optional Cohere Reranking:**
- ML-based reranking using `rerank-english-v3.0` model
- Retrieves 2x candidates, reranks with advanced model
- Significantly improves relevance vs. fusion alone
- Enable with `USE_COHERE_RERANK=true`

**Weighting Control:**
- `RAG_SPARSE_TOP_K`: Higher = more keyword influence
- `RAG_RERANK_CANDIDATES`: Candidates sent to Cohere reranker
- `RAG_RERANK_TOP_N`: Final number of chunks returned

**Example:**
```env
RAG_SPARSE_TOP_K=20    # More keyword focus
RAG_SIMILARITY_TOP_K=5 # Still only 5 final results
```

### Metadata

Each chunk includes:
- `filename`: Original file name (e.g., "test.md")
- `subdirectory`: Relative path from root (e.g., "research/papers")
- `file_path`: Absolute path to source file

## Customization

### Chunk Size & Overlap

Edit `.env`:

```bash
RAG_MIN_CHUNK_SIZE=400   # Minimum chunk size in tokens
RAG_MAX_CHUNK_SIZE=800   # Maximum chunk size in tokens (average: 600)
RAG_CHUNK_OVERLAP=80     # Token overlap (13% at 600 tokens)
USE_SEMANTIC_CHUNKING=false  # false = token-based (fast), true = semantic (slow)
```

**Guidelines:**
- **Token-based chunking (recommended)**: Fast, markdown-aware, configurable 400-800 tokens
- **Semantic chunking**: Slower but adaptive breakpoints at natural boundaries
- Small chunks (300-500 tokens): Better for fact-based queries
- Medium chunks (600-800 tokens): Better for complex reasoning (recommended)
- Overlap: 10-15% of chunk size recommended

### Retrieval Parameters

Edit `.env`:

```bash
RAG_SIMILARITY_TOP_K=5   # Final results returned
RAG_SPARSE_TOP_K=12      # BM25 candidates before fusion
RAG_SCORE_THRESHOLD=0.2  # Minimum relevance score (0.0-1.0)
```

**Guidelines:**
- More semantic focus: Lower `sparse_top_k` (e.g., 8)
- More keyword focus: Higher `sparse_top_k` (e.g., 20)
- More context to LLM: Higher `similarity_top_k` (e.g., 10)
- Filter irrelevant results: Higher `score_threshold` (e.g., 0.3-0.4)
- Allow more results: Lower `score_threshold` (e.g., 0.15-0.2)

### Reranking Parameters (Cohere)

Edit `.env`:

```bash
USE_COHERE_RERANK=true         # Enable/disable reranking
RAG_RERANK_CANDIDATES=20       # Candidates sent to reranker
RAG_RERANK_TOP_N=5             # Final results after reranking
```

**Guidelines:**
- Better quality: Higher `rerank_candidates` (e.g., 20) - more options for reranker
- Faster queries: Lower `rerank_candidates` (e.g., 10) - less API calls
- More context to LLM: Higher `rerank_top_n` (e.g., 8-10)
- **Recommended**: `candidates=4x` of `top_n` (e.g., 20 candidates → 5 results)

### Embedding Model

Edit `rag_index.py` line 125:

```python
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-large",  # More accurate, more expensive
    api_key=os.getenv('OPENAI_API_KEY')
)
```

**Note**: No LLM is used during query - the system returns only chunks for maximum token efficiency.

## Troubleshooting

**Q: "Index required but not found for subdirectory"**
A: Run `python rag_index.py --force` to recreate payload indexes

**Q: Old data still appears after file deletion**
A: The system now auto-deletes on query. Or manually run `python rag_index.py`

**Q: Slow indexing**
A: Disable LlamaParse for simple PDFs: `USE_LLAMA_PARSE=false`

**Q: Poor search results**
A: Try adjusting `RAG_SPARSE_TOP_K` (higher = more keyword matching)

**Q: Memory issues**
A: Reduce `RAG_CHUNK_SIZE` or index fewer documents at once

**Q: Changes not detected**
A: Delete `rag_metadata.json` and run `python rag_index.py --force`

## Technical Details

### Stack

- **Vector DB**: Qdrant (cloud-hosted)
- **Embeddings**: OpenAI text-embedding-3-small (1536 dimensions)
- **Reranking**: Cohere rerank-english-v3.0 (optional, recommended)
- **Sparse Embeddings**: BM42 via FastEmbed
- **Fusion Method**: Relative Score Fusion
- **Chunking**: SentenceSplitter (token-based, 400-800 tokens) or SemanticSplitter
- **PDF Parsing**: PyPDF (default) or LlamaParse (advanced)
- **Framework**: LlamaIndex
- **Output**: JSON (structured) or Human-readable text

### Performance

- **Indexing**: ~2 docs/sec (depends on doc size & API latency)
- **Query**: ~1-2 sec (embedding + hybrid search + reranking)
- **Storage**: ~1.5 KB per chunk (embeddings + metadata)
- **Change Detection**: <100ms (metadata check)

### Costs (Approximate)

- **Embedding**: $0.00002 per 1k tokens (~$0.10 per 1M words)
- **LlamaParse**: $0.003 per page (optional)
- **Cohere Rerank**: ~$1-2 per 1M searches (optional, highly recommended)
- **Qdrant Cloud**: Free tier available, paid plans from $25/month

### Why This Setup?

✅ **Hybrid Search**: Relative Score Fusion combines semantic + keyword, 15-35% better than semantic-only
✅ **Cohere Reranking**: ML-based reranking significantly improves relevance (state-of-the-art 2024)
✅ **LlamaIndex**: 35% retrieval boost in 2025, ideal for focused RAG applications
✅ **Token-Based Chunking**: 400-800 tokens optimal for RAG, faster than semantic, markdown-aware
✅ **JSON Output**: Reliable structured output for AI agents, no truncation or parsing errors
✅ **OpenAI Embeddings**: Best price/performance ratio ($0.02/M tokens, 75.8% accuracy)
✅ **Qdrant**: Performance-conscious, cost-effective, production-ready
✅ **BM42**: Modern sparse embeddings, optimized for RAG

## File Structure

```
rag-search/
├── rag_index.py           # Indexing script
├── rag_query.py           # Query script
├── requirements.txt       # Dependencies
├── .env                   # Configuration (not in git)
├── .env.example          # Configuration template
├── .gitignore            # Excludes .env and metadata
├── rag_metadata.json     # Change detection metadata (not in git)
└── README.md             # This file
```

## Cross-Platform Notes

- Uses `Path()` for all file operations (Windows + macOS compatible)
- Loads `.env` from script directory (not cwd)
- Works with absolute and relative paths
- Line endings handled automatically by libraries
- Metadata stored in script directory (portable across environments)
