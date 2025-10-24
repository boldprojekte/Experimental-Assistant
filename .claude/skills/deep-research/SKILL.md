---
name: Deep Research
description: Workflow guide for comprehensive internet research with multiple sources. Use for deep research, detailed research, comprehensive analysis, web search with multiple sources, complex research queries, thorough investigation. The skill coordinates parallel web-research subagents as a supervisor and manages the complete workflow from task division to final documentation.
---

# Deep Research Workflow

Workflow for comprehensive internet research with Supervisor-Pattern and parallel web-research subagents.

## Path Configuration

**Working Directory**: `/Users/j.franke/Desktop/Windsurf/Experimental-Assistant/`

**Key Paths** (all relative to working directory):
- Task lists: `Aufgaben/` → Archive: `Aufgaben/Archiv/`
- Active docs: `Dokumente/01_in Arbeit/` → Review: `Dokumente/02_Review/` → Final: `Dokumente/`
- Document index: `Dokumente/INDEX.md`

## Workflow Overview

1. **Analysis & Planning** → Thinking process for task division
2. **Research Question Transformation** → Transform user request into detailed research brief
3. **Create Task List** → Markdown file with checkboxes in `Aufgaben/`
4. **Parallel Research** → Spawn multiple `web-research-specialist` subagents
5. **Collect Results** → Document in `Dokumente/01_in Arbeit/`
6. **Compression** → Normalize and deduplicate findings
7. **Self-Review** → Quality check and possibly further searches
8. **Finalization** → Formatting and archiving
9. **User-Review** → Approval and indexing

---

## Phase 1: Analysis & Planning

**Use `mcp__sequential-thinking__sequentialthinking` for planning!**

### Clarification (Optional)

Ask when necessary (max 1x):
- Ambiguous acronyms/abbreviations
- Missing critical information (scope, criteria, timeframe)
- Contradictory requirements

**Structured format when asking:**
```
I need clarification before starting research:

**[Aspect]**: [Question]
- Option A: [...]
- Option B: [...]

Once clarified, I'll [brief approach].
```

### Planning Steps

1. **Identify main question** - What's the central question? What language?
2. **Assess complexity** - Determine number of sub-agents (1-5):
   - **1 Sub-Agent**: Simple definitions, single facts, straightforward how-to
   - **2-3 Sub-Agents**: Comparisons, multiple distinct aspects
   - **4-5 Sub-Agents**: Complex multi-layered analyses, comprehensive overviews
3. **Define sub-areas** - Which specific aspects? (One sub-area = One sub-agent)
4. **Expected results** - What should each search deliver?

---

## Phase 2: Research Question Transformation

**Transform user request into detailed, unambiguous research brief using `mcp__sequential-thinking__sequentialthinking`**

### Transformation Principles

1. **Maximize Specificity**: Include all user preferences, list key dimensions
2. **Handle Unstated Requirements**: State explicitly as "open-ended" if essential but unspecified
3. **Avoid Assumptions**: Don't invent details - state when unspecified
4. **First Person**: "I need..." not "The user wants..."
5. **Source Preferences**:
   - Product/travel → Official sites, manufacturer pages
   - Academic/scientific → Original papers, journals
   - People → LinkedIn, personal websites
   - Language-specific → Sources in that language
6. **Time Sensitivity**: Specify timeframe (e.g., "2024-2025" for current topics)

### Transformation Examples

**Example 1: Simple Query**

Original: "What is React?"

Transformed:
```
I need a comprehensive overview of React, the JavaScript library. Please cover:
- Core concepts and purpose
- Key features and capabilities
- Basic usage and getting started
- When and why to use it

Prioritize official React documentation and recent resources (2024-2025).
Language: English
```

**Example 2: Complex Research**

Original: "Explain how machine learning works"

Transformed:
```
I need a deep understanding of how machine learning works, covering:
- Fundamental concepts and definitions
- Main types of learning (supervised, unsupervised, reinforcement)
- Key algorithms and how they work
- Neural networks and deep learning basics
- Practical applications and real-world use cases
- Current tools, frameworks, and ecosystem
- Recent trends and developments (2024-2025)

Balance technical depth with accessibility. Include both theoretical explanations and practical examples.
Prioritize authoritative sources: academic papers for concepts, official documentation for tools, reputable tech publications for trends.
Language: English
```

### Output Format

```markdown
## Transformed Research Brief

**Original**: {User's question}

**Detailed Research Question**: {Transformed with all specifications}

**Key Dimensions**: {Dimension 1}, {Dimension 2}, {Dimension 3}
**Source Priorities**: {Guidance if applicable}
**Language**: {Target language}
**Time Scope**: {Timeframe if applicable}
```

---

## Phase 3: Create Task List

**File**: `Aufgaben/YYYY-MM-DD_Research_{Topic}.md`

```markdown
# Research: {Topic}

**Created**: {Date} {Time}
**Status**: In Progress

## Main Question
{Original user request}

## Sub-Tasks
- [ ] {Sub-area 1}: {Brief description}
- [ ] {Sub-area 2}: {Brief description}
- [ ] Compression: Normalize and deduplicate findings
- [ ] Self-Review: Quality check of results
- [ ] Finalization: Formatting and summary
```

---

## Phase 4: Parallel Research

**Spawn all `web-research-specialist` subagents in ONE message using `Task` tool!**

Number based on Phase 1 assessment (1-5 agents). Give each agent clear, focused task:

```
Research: {Specific question for this sub-area}

Focus:
- {Aspect 1}
- {Aspect 2}

IMPORTANT: Respond in {same language as user request}.
```

**Note**: Agent has own research methodology - only give task, not HOW.

---

## Phase 5: Collect Results

**Create**: `Dokumente/01_in Arbeit/Research_{Topic}_{Date}.md`

```markdown
# Research: {Topic}

**Created**: {Date}
**Researched by**: Claude Deep Research Agent
**Status**: In Progress

---

## {Sub-area 1}
{Results from Subagent 1}

### Sources
- {URL 1}
- {URL 2}

---

## {Sub-area 2}
{Results from Subagent 2}

### Sources
...

---

## Summary
{Added in Phase 8}
```

### Workflow
1. Subagent returns → Insert into document → Check off task → Continue
2. Update task list after EACH completed sub-task

### Supervisor-Worker Pattern
- **Supervisor (You)**: See all results, integrate into ONE document, coordinate workflow
- **Workers (Subagents)**: Receive only their task, return ONLY text, no file creation

---

## Phase 6: Compression

**Normalize and deduplicate while preserving ALL information. NOT summarization!**

### Process

**Step 1**: Read complete document from `Dokumente/01_in Arbeit/{Filename}`

**Step 2**: Use `mcp__sequential-thinking__sequentialthinking` to identify:
- Duplicate information across workers
- Contradictions or discrepancies
- Formatting inconsistencies
- Citation overlaps

**Step 3**: Compress and normalize:

**A. Merge Duplicates**: When multiple workers state same fact → Combine with multiple citations
Example: "React is a JavaScript library [1]" + "React is a JS library for UIs [2]" → "React is a JavaScript library for building user interfaces [1][2]"

**B. Handle Contradictions**: Preserve both views explicitly
Example: "Sources indicate release in Dec 2024 [1] vs early 2025 [2][3]. Official blog confirms Dec 5, 2024 [1]."

**C. Normalize Citations**: Renumber sequentially (1, 2, 3...) with NO gaps

**D. Standardize Formatting**: Consistent headings (##, ###), bullet points, code blocks

**Step 4**: Verify preservation - ALL facts, sources, and information retained

**Step 5**: Update document with `Edit` tool

### Compression Example

**Before Compression** (redundant):
```markdown
## Machine Learning Basics (Worker 1)
Machine learning is a subset of AI that enables systems to learn from data [1].
It uses algorithms to find patterns [2]. There are three main types: supervised,
unsupervised, and reinforcement learning [3].

### Sources
[1] IBM What is ML: https://ibm.com/ml
[2] MIT ML Guide: https://mit.edu/ml
[3] Stanford ML: https://stanford.edu/ml

## ML Fundamentals (Worker 2)
Machine learning allows computers to learn without explicit programming [4].
The three primary categories are supervised learning, unsupervised learning,
and reinforcement learning [5]. ML is a branch of artificial intelligence [6].

### Sources
[4] Google ML Crash Course: https://google.com/ml
[5] Stanford ML Course: https://stanford.edu/ml
[6] IBM AI Overview: https://ibm.com/ml
```

**After Compression** (normalized):
```markdown
## Machine Learning Fundamentals

Machine learning is a subset of artificial intelligence that enables systems to
learn from data without explicit programming [1][4]. It uses algorithms to identify
patterns and make predictions [2].

The field is organized into three main types [3][5]:
1. **Supervised Learning**: Learning from labeled data
2. **Unsupervised Learning**: Finding patterns in unlabeled data
3. **Reinforcement Learning**: Learning through trial and reward

### Sources
[1] IBM What is ML: https://ibm.com/ml
[2] MIT ML Guide: https://mit.edu/ml
[3] Stanford ML: https://stanford.edu/ml
[4] Google ML Crash Course: https://google.com/ml
[5] Stanford ML Course: https://stanford.edu/ml
```

### Compression Guidelines

**DO**: Merge redundant facts, deduplicate citations, fix formatting, remove repetition
**DON'T**: Remove different perspectives, examples, technical details, nuanced explanations

**Checklist**:
- [ ] All worker findings integrated
- [ ] Duplicates merged
- [ ] Contradictions flagged
- [ ] Citations sequential (no gaps)
- [ ] All sources preserved
- [ ] Formatting consistent
- [ ] No information lost

---

## Phase 7: Self-Review

**MANDATORY before finalization!**

1. **Read** complete document
2. **Think** with `mcp__sequential-thinking__sequentialthinking`:
   - Main question sufficiently answered?
   - Open questions or gaps?
   - Information current?
   - Important aspects missing?
3. **Quality checks**:
   - [ ] Critical facts from authoritative sources
   - [ ] Contradictions resolved or mentioned
   - [ ] Timeliness appropriate

### Decision
- **Sufficiently answered** → Phase 8 (Finalization)
- **Further research needed** → Back to Phase 4 (spawn additional workers)

Check off: `- [x] Self-Review: Quality check of results`

---

## Phase 8: Finalization

### Add Summary

```markdown
## Summary

### Key Findings
1. {Finding 1}
2. {Finding 2}

### Answer to Main Question
{Direct answer}

### Further Information
- {Link/Topic 1}
```

### Check Formatting
- Headings hierarchical
- Sources linked
- Markdown consistent
- Readable

### Archive

```bash
mv "Aufgaben/{Filename}" "Aufgaben/Archiv/{Filename}"
mv "Dokumente/01_in Arbeit/{Filename}" "Dokumente/02_Review/{Filename}"
```

Check off: `- [x] Finalization: Formatting and summary`

---

## Phase 9: User-Review

### Present Result

Show user:
1. Link to `Dokumente/02_Review/{Filename}`
2. Brief summary (2-3 sentences)
3. Request: "✅ Approve → Move to `Dokumente/` and index" or "🔄 Revision → Tell me what to adjust"

### After Approval

```bash
mv "Dokumente/02_Review/{Filename}" "Dokumente/{Filename}"
```

Update `Dokumente/INDEX.md`:
```markdown
- **{Date}** - [{Topic}]({Filename}) - Research: {Brief description}
```

Confirm: "✅ Research completed and archived!"

---

## Core Principles

1. **Structured clarification** - Use format when asking questions
2. **Transform questions** - Phase 2 creates detailed brief
3. **Think first** - Use thinking tool for planning, transformation, compression
4. **Parallel spawn** - All subagents in ONE message
5. **Supervisor coordinates** - Workers only research
6. **Immediate updates** - Check tasks after each completion
7. **Compression mandatory** - Phase 6 before review
8. **Self-review mandatory** - Phase 7 quality gate
9. **Strict folders** - `01_in Arbeit` → `02_Review` → `Dokumente/`
10. **User approval** - Phase 9 never skip

---

## Error Handling

**No results**: Note in document, check in review if critical, retry with different terms
**Revision requested**: Clarify needs, add tasks, spawn workers, repeat from Phase 7
