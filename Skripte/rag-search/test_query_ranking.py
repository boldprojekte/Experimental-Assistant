#!/usr/bin/env python3
"""
Test query to understand ranking behavior for the 0.4 H formula.
"""

import os
import json
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from qdrant_client import QdrantClient
from llama_index.core import Settings

# Load environment
load_dotenv()

# Initialize clients
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Setup embedding model
Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Create vector store
vector_store = QdrantVectorStore(
    client=client,
    collection_name=os.getenv("QDRANT_COLLECTION", "documents")
)

# Create index
index = VectorStoreIndex.from_vector_store(vector_store)

# Test queries
test_queries = [
    "Wie ermittelt man die Tiefe der Abstandsflächen? Welche Formel verwendet man zur Berechnung?",
    "Abstandsflächen Tiefe Berechnung Formel 0,4 H Wandhöhe",
    "§ 6 Absatz 5 BauO NRW Abstandsflächen beträgt",
]

print("=" * 80)
print("RANKING TEST - Why wasn't the 0.4 H formula retrieved?")
print("=" * 80)
print(f"\nTarget Chunk ID: 9769063e-4e21-4dd3-ae97-8ffd39002d6e")
print("=" * 80)

for query_text in test_queries:
    print(f"\n\n🔍 Query: {query_text}")
    print("=" * 80)

    # Create retriever with high top_k to see all results
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=20,  # Get more results to see ranking
    )

    # Retrieve nodes
    retrieved_nodes = retriever.retrieve(query_text)

    print(f"\nRetrieved {len(retrieved_nodes)} nodes")
    print("-" * 80)

    # Check if target chunk is in results
    target_found = False
    target_rank = None

    for i, node in enumerate(retrieved_nodes, 1):
        node_id = node.node_id
        score = node.score
        text = node.text[:200] + "..." if len(node.text) > 200 else node.text

        # Check if this is the target chunk
        is_target = node_id == "9769063e-4e21-4dd3-ae97-8ffd39002d6e"
        if is_target:
            target_found = True
            target_rank = i

        # Mark target with special formatting
        marker = "🎯 TARGET " if is_target else ""

        print(f"\n[{marker}Rank {i}] Score: {score:.4f}")
        print(f"Node ID: {node_id}")
        print(f"Text: {text}")
        print("-" * 80)

    if target_found:
        print(f"\n✅ Target chunk FOUND at rank {target_rank} (score: {retrieved_nodes[target_rank-1].score:.4f})")
    else:
        print(f"\n❌ Target chunk NOT FOUND in top 20 results")

print("\n\n" + "=" * 80)
print("Analysis Summary")
print("=" * 80)
print("""
The target chunk contains:
'(5) Die Tiefe der Abstandsflächen beträgt 0,4 H, mindestens 3 m.'

This is exactly what the user was searching for, but it wasn't retrieved
in the original queries. The test above shows:
1. Where the chunk ranks for different query formulations
2. What score it receives
3. Why it might have been filtered out
""")
