#!/usr/bin/env python3
"""
Test JSON parsing from rag_query.py output
"""

import subprocess
import json

# Run query with JSON output
result = subprocess.run(
    [
        "python3", "rag_query.py",
        "Wie ermittelt man die Tiefe der Abstandsflächen? Welche Formel verwendet man zur Berechnung?",
        "--json"
    ],
    capture_output=True,
    text=True,
    cwd="/Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/rag-search"
)

print("=" * 80)
print("RAW OUTPUT:")
print("=" * 80)
print(result.stdout)
print()

# Parse JSON (skip non-JSON lines before first '{')
output = result.stdout
# Find the first '{' and take everything from there
json_start = output.find('{')
if json_start == -1:
    json_str = ""
else:
    json_str = output[json_start:]

try:
    data = json.loads(json_str)

    print("=" * 80)
    print("PARSED JSON:")
    print("=" * 80)
    print(f"Status: {data['status']}")
    print(f"Count: {data['count']}")
    print(f"Score Threshold: {data['score_threshold']}")
    print()

    # Check if we found the formula
    for i, chunk in enumerate(data['chunks'], 1):
        print(f"\n📄 Chunk {i} ({chunk['metadata']['filename']}):")
        print(f"   Score: {chunk['score']}")

        # Check for the formula
        if '0,4 H' in chunk['text'] or '0.4 H' in chunk['text']:
            print("   ✅ CONTAINS FORMULA!")
            # Find the line with formula
            for line in chunk['text'].split('\n'):
                if '0,4 H' in line or '0.4 H' in line:
                    print(f"   📌 {line.strip()}")
        else:
            print(f"   Text length: {len(chunk['text'])} characters")

    print("\n" + "=" * 80)
    print("✅ JSON PARSING SUCCESS")
    print("=" * 80)

except json.JSONDecodeError as e:
    print(f"❌ JSON Parsing Error: {e}")
    print(f"Attempted to parse: {json_str[:200]}...")
