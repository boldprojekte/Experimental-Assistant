#!/usr/bin/env python3
"""
Analyze RAG chunks for BauO-NRW.pdf to understand why the 0.4 H formula wasn't retrieved.
"""

import os
import json
from qdrant_client import QdrantClient
from dotenv import load_dotenv

# Load environment
load_dotenv()

def analyze_chunks():
    # Connect to Qdrant
    client = QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY")
    )

    collection_name = os.getenv("QDRANT_COLLECTION", "documents")

    print("=" * 80)
    print("Analyzing BauO-NRW.pdf chunks")
    print("=" * 80)

    # Scroll through all points (no filter, we'll filter in Python)
    offset = None
    all_points = []
    bauo_points = []

    print("\nFetching all points from Qdrant...")

    while True:
        results = client.scroll(
            collection_name=collection_name,
            limit=100,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )

        points, offset = results
        all_points.extend(points)

        # Filter for BauO-NRW.pdf in Python
        for point in points:
            file_name = point.payload.get('file_name', '')
            if 'BauO-NRW' in file_name:
                bauo_points.append(point)

        if offset is None:
            break

    print(f"\nTotal chunks in collection: {len(all_points)}")
    print(f"Chunks from BauO-NRW.pdf: {len(bauo_points)}")

    # Use BauO-NRW points for further analysis
    all_points = bauo_points
    print("=" * 80)

    # First, let's inspect what fields exist
    print("\n🔍 Inspecting payload structure of first chunk:")
    if all_points:
        first_point = all_points[0]
        print(f"Available keys: {list(first_point.payload.keys())}")
        print(f"Sample payload: {first_point.payload}")
        print("=" * 80)

    # Search for chunks containing the formula
    formula_chunks = []
    section_6_chunks = []

    for point in all_points:
        # Extract text from _node_content JSON
        text = ''
        node_content = point.payload.get('_node_content', '')
        if node_content:
            try:
                node_data = json.loads(node_content)
                text = node_data.get('text', '')
            except json.JSONDecodeError:
                text = ''

        # Look for the 0.4 H formula
        if '0,4' in text or '0.4' in text:
            formula_chunks.append((point, text))

        # Look for § 6 mentions
        if '§ 6' in text or '§6' in text or 'Abstandsflächen' in text:
            section_6_chunks.append((point, text))

    print(f"\n📊 Analysis Results:")
    print(f"   Chunks with '0,4' or '0.4': {len(formula_chunks)}")
    print(f"   Chunks mentioning § 6 or Abstandsflächen: {len(section_6_chunks)}")
    print("=" * 80)

    # Show formula chunks
    if formula_chunks:
        print("\n🎯 CHUNKS CONTAINING THE FORMULA (0,4 H):")
        print("=" * 80)
        for i, (point, text) in enumerate(formula_chunks, 1):
            chunk_id = point.id

            print(f"\n[Chunk {i}] ID: {chunk_id}")
            print("-" * 80)

            # Highlight the formula line
            for line in text.split('\n'):
                if '0,4' in line or '0.4' in line:
                    print(f">>> {line}")
                else:
                    print(f"    {line}")
            print("-" * 80)
    else:
        print("\n❌ NO CHUNKS FOUND CONTAINING '0,4 H' FORMULA!")
        print("   This means the formula was likely split across chunk boundaries.")

    # Show some § 6 chunks for context
    print("\n\n📋 SAMPLE § 6 / ABSTANDSFLÄCHEN CHUNKS:")
    print("=" * 80)
    for i, (point, text) in enumerate(section_6_chunks[:5], 1):
        chunk_id = point.id

        print(f"\n[Sample {i}] ID: {chunk_id}")
        print("-" * 80)
        print(text[:500] + "..." if len(text) > 500 else text)
        print("-" * 80)

    # Statistics about chunk sizes
    print("\n\n📈 CHUNK SIZE STATISTICS:")
    print("=" * 80)
    chunk_sizes = []
    for point in all_points:
        node_content = point.payload.get('_node_content', '')
        if node_content:
            try:
                node_data = json.loads(node_content)
                text = node_data.get('text', '')
                chunk_sizes.append(len(text))
            except json.JSONDecodeError:
                pass

    if chunk_sizes:
        print(f"   Min chunk size: {min(chunk_sizes)} characters")
        print(f"   Max chunk size: {max(chunk_sizes)} characters")
        print(f"   Avg chunk size: {sum(chunk_sizes) // len(chunk_sizes)} characters")

    return formula_chunks, section_6_chunks

if __name__ == "__main__":
    analyze_chunks()
