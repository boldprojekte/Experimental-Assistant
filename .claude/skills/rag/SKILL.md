---
name: rag
description: Workflow guide for RAG knowledge management. Use for indexing documents into long-term memory, querying knowledge base, and retrieving relevant information. Critical for query reformulation and answer grounding from retrieved chunks.
---

# RAG Knowledge Management Workflow

Hybrid search (BM25 + Dense Vector) for long-term knowledge in `Dokumente/03_RAG/`.

## Use Cases

✅ Query knowledge base | Index documents to long-term memory
❌ Current/live info (use WebSearch) | Specific known files (use Read)

---

## Workflow

### Step 1: Query Understanding (Think First)

**Analyze the user's question deeply**:
1. What is the user REALLY asking? (core question + implicit requirements)
2. What context is implied but unstated?
3. Complexity: Simple (fact/definition) | Medium (concept/process) | Complex (multi-aspect analysis)

**Query Reformulation Principles**:

❌ **DON'T compress to keywords**:
- "RAG optimization" ← loses context and nuance
- "best practices list" ← strips away semantic meaning
- "X definition" ← misses the "why"

✅ **DO preserve semantic richness**:
- "RAG performance optimization techniques including query reformulation, retrieval efficiency, and parameter tuning strategies"
- "Production-ready best practices with practical implementation guidance, common pitfalls, and decision criteria"
- "Comprehensive explanation of X including core concepts, practical applications, and contextual relevance"

**Key principle**: Read between the lines for unstated context and requirements.

---

### Step 2: Query Reformulation Strategy

**Based on assessed complexity**:

**Simple Queries (Facts/Definitions)**:
- 1 focused query with exact terms from user question
- Add technical synonyms only if absolutely necessary
- Example: "What is OAuth?" → "OAuth authentication protocol definition and core concepts"

**Medium Queries (Concepts/Processes)**:
- 1-2 queries with semantic expansion
- Include related terms and broader context
- Example: "How does authentication work?" → "authentication methods and workflows including OAuth, JWT, session-based approaches and security considerations"

**Complex Queries (Multi-Aspect)**:
- 2-3 decomposed sub-queries (MAXIMUM 3!)
- Each sub-query focuses on one distinct aspect
- Example: "Optimize RAG system" →
  1. "RAG query reformulation and expansion techniques for better retrieval"
  2. "RAG retrieval stopping criteria and efficiency optimization"
  3. "RAG hyperparameter tuning strategies and best practices"

**Multi-Query Pattern** (for comprehensive answers):
- Rephrase the same question from different perspectives
- Captures semantic variations
- Use when thoroughness is critical

---

### Step 3: Execute Retrieval

**CRITICAL**: Always use `--json` flag for structured, parsable output.

```bash
cd /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/rag-search

# Standard query with JSON output (REQUIRED)
python3 rag_query.py "semantically rich reformulated query" --json

# With subdirectory filter
python3 rag_query.py "query" --subdir {topic} --json

# ONLY if clear problem after evaluation
python3 rag_query.py "query" --top-k 10 --json
```

**JSON Output Format**:
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
        "file_path": "/path/to/document.pdf"
      }
    }
  ]
}
```

**Parsing Instructions**:
1. Locate first `{` in output (skip any log messages before JSON)
2. Parse JSON from that point: `json_start = output.find('{'); json.loads(output[json_start:])`
3. Access chunks via `data['chunks']`, each has `text`, `score`, and `metadata`
4. **Important**: `text` field contains FULL chunk text (no truncation)

**Parameter Discipline (Best Practice 2024-2025)**:

✅ **ALWAYS USE**:
- `--json`: Required for reliable parsing and complete text

✅ **USE DEFAULTS** (preferred):
- `--top-k 5`: Proven optimal for most queries
- `--sparse-top-k 12`: Balanced keyword/semantic mix
- System automatically handles hybrid search (BM25 + Dense Vector)

⚠️ **ONLY ADJUST IF**:
- Clear insufficient coverage AFTER evaluation
- User explicitly requests different settings
- Specific known problem (e.g., too many irrelevant chunks)

❌ **DON'T**:
- Speculatively tune parameters "just in case"
- Change settings without evidence of problems
- Over-optimize prematurely
- Forget `--json` flag

**Available Parameters** (use sparingly):
- `--json`: **REQUIRED** - Structured JSON output
- `--subdir {name}`: Filter by subdirectory
- `--top-k {n}`: Number of chunks (default: 5, range: 3-10)
- `--sparse-top-k {n}`: Keyword focus (default: 12)
- `--no-reindex-check`: Skip re-indexing (faster, only if files unchanged)

---

### Step 4: Document Grading (After EACH Retrieval)

**Evaluate retrieved chunks with binary assessment**:

✅ **Relevance**: Do chunks directly address the question? (yes/no)
✅ **Coverage**: Are key aspects covered? Sufficient depth?
✅ **Quality**: No contradictions? Information accurate?

**Stopping Decision Tree**:
```
After each retrieval:
├─ >= 3 chunks highly relevant? → STOP, proceed to answer
├─ Full coverage of user's question? → STOP, proceed to answer
├─ Iteration count >= 3? → FORCE STOP (hard limit)
├─ Last 2 retrievals very similar? → STOP (diminishing returns)
└─ All checks failed → Consider ONE more retrieval with reformulated query
```

**Hard Limits (Non-Negotiable)**:
- Maximum 3 retrieval iterations per user question
- Maximum 2 query reformulations (initial + 2 rewrites)
- After limits: Work with available chunks or tell user transparently

---

### Step 5: Handle Insufficient Results

**If chunks are irrelevant or insufficient**:

**Attempt 1 failed?**
- Reformulate query with different terms/perspective
- Try subdirectory filter if topic known
- ONE more retrieval allowed

**Attempt 2 failed?**
- Assess: Is information likely in knowledge base?
- Consider: Increase `--top-k` to 8-10 for broader context
- ONE final retrieval allowed (iteration 3)

**Attempt 3 failed OR hard limit reached?**
- **STOP** - Do not retrieve further
- Respond transparently:

```
I searched the knowledge base 3 times but couldn't find information about [topic].

Queries tried:
1. "[query 1]" - [brief result summary]
2. "[query 2]" - [brief result summary]
3. "[query 3]" - [brief result summary]

Retrieved chunks discuss [actual content], but don't address [user's specific question].

Options:
- Try different search terms? [suggest specific alternatives]
- Search in specific subdirectory? [if applicable]
- Search the web instead for current information?
```

---

### Step 6: Answer Generation (Anti-Hallucination)

**Strict Grounding Rules**:
- ✅ ONLY use information from retrieved chunks
- ✅ Quote precisely from chunks (use quotes for direct excerpts)
- ✅ Cite EVERY statement: `(Source: filename.md, subdirectory: topic)`
- ✅ Mark uncertainty with `[?]` if chunks are unclear
- ✅ State gaps openly: "Information about [X] not found in knowledge base"
- ❌ NEVER invent information not in chunks
- ❌ NEVER add external knowledge
- ❌ NEVER speculate beyond chunk content
- ❌ NEVER assume what chunks "probably mean"

**Answer Structure**:
```
[Direct answer in 1-2 sentences - highest confidence info]

**[Aspect 1]**
[Detailed explanation from chunks]
"[Relevant quote]" (Source: document.md, subdirectory: topic)

**[Aspect 2]** [if applicable]
[Additional information]
"[Another quote]" (Source: other-doc.md)

**Note**: [If gaps] Information about [missing aspect] not found in knowledge base.
```

**If contradictions in chunks**:
```
The knowledge base contains different perspectives:

**Perspective 1**: "[Quote]" (Source: doc1.md)
**Perspective 2**: "[Quote]" (Source: doc2.md)

[Ask user for clarification or preference]
```

**Citations are mandatory**: Every statement must cite source with `(Source: file, subdirectory: topic)` format.

---

## Core Principles (2024-2025 Best Practices)

1. **Semantic Understanding > Keyword Matching**
   - Preserve semantic richness and context
   - Read between the lines for implicit requirements
   - Don't compress queries to bare keywords

2. **Adaptive Retrieval with Hard Limits**
   - Complexity-based strategy (Simple/Medium/Complex)
   - Maximum 3 iterations, no exceptions
   - Document grading after EACH retrieval

3. **Parameter Discipline**
   - Use proven defaults (top_k=5, sparse_top_k=12)
   - Don't tune speculatively without evidence
   - Adjust only for clear, evaluated problems
   - **ALWAYS use --json flag** for reliable output

4. **Strict Grounding**
   - Answer ONLY from retrieved chunks (complete text, no truncation)
   - Cite every statement with source
   - Transparent about gaps and limitations
   - **Read entire chunk text** - important info may be at end

5. **Honest Transparency**
   - Say "not found" when information isn't in chunks
   - Don't invent, speculate, or assume
   - Offer alternatives (web search, different terms)

---

## Common Anti-Patterns (AVOID)

❌ **Query Compression**: Reducing to keywords instead of semantic queries
❌ **Over-Retrieval**: Searching 5+ times hoping for better results
❌ **Parameter Tweaking**: Changing top_k without clear reason
❌ **Hallucination**: Adding information not present in chunks
❌ **Speculation**: Guessing what chunks "probably mean"
❌ **Citation Skipping**: Making statements without source attribution
❌ **Premature Optimization**: Adjusting settings before evaluating results
❌ **Missing JSON Flag**: Not using --json (causes parsing errors, truncation)

✅ **Best Practices**: JSON output, semantic queries, hard limits, default parameters, strict grounding, complete chunk reading, transparent failures

---

## Document Management

**Moving documents to long-term memory**:
1. Identify source document
2. Determine target: `Dokumente/03_RAG/{topic}/` or `Dokumente/03_RAG/`
3. Move document
4. Confirm to user

**Auto-indexing**: New files automatically detected and indexed on next query.

**Subdirectories**: Use `--subdir {topic}` to filter searches. Enables topic-specific retrieval.

---

## Output Rules

- **Language**: Match user's question language (German → German, English → English)
- **Style**: Precise, factual, no unnecessary elaboration
- **Citations**: Required for every statement
- **Tone**: Helpful but honest - admit when information unavailable
