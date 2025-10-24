#!/usr/bin/env python3
"""
Show the full content of the target chunk.
"""

import os
import json
from qdrant_client import QdrantClient
from dotenv import load_dotenv

load_dotenv()

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

collection_name = os.getenv("QDRANT_COLLECTION", "documents")

# Retrieve the specific chunk
points = client.retrieve(
    collection_name=collection_name,
    ids=["9769063e-4e21-4dd3-ae97-8ffd39002d6e"],
    with_payload=True,
    with_vectors=False
)

if points:
    point = points[0]
    node_content = point.payload.get('_node_content', '')
    node_data = json.loads(node_content)
    text = node_data.get('text', '')

    print("=" * 80)
    print("FULL TEXT OF TARGET CHUNK")
    print("ID: 9769063e-4e21-4dd3-ae97-8ffd39002d6e")
    print("=" * 80)
    print(text)
    print("=" * 80)
    print(f"\nChunk length: {len(text)} characters")
    print(f"Contains '0,4 H': {'0,4 H' in text}")
    print(f"Position of '0,4 H': {text.find('0,4 H')}")
