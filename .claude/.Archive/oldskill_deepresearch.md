---
name: Deep Research
description: Workflow guide for comprehensive internet research with multiple sources. Use for deep research, detailed research, comprehensive analysis, web search with multiple sources, complex research queries, thorough investigation. The skill coordinates parallel web-research subagents as a supervisor and manages the complete workflow from task division to final documentation.
---

# Deep Research Workflow

Workflow for comprehensive internet research with Supervisor-Pattern and parallel web-research subagents.

## Path Configuration

**Working Directory**: `/Users/j.franke/Desktop/Windsurf/Experimental-Assistant/`

**Key Paths** (all relative to working directory):
- Task lists: `Aufgaben/`
- Task archive: `Aufgaben/Archiv/`
- Active documents: `Dokumente/01_in Arbeit/`
- Review documents: `Dokumente/02_Review/`
- Final documents: `Dokumente/`
- Document index: `Dokumente/INDEX.md`

## Workflow Overview

1. **Analysis & Planning** → Thinking process for task division
2. **Research Question Transformation** → Transform user request into detailed research brief
3. **Create Task List** → Markdown file with checkboxes in `/Aufgaben/`
4. **Parallel Research** → Spawn multiple `web-research-specialist` subagents
5. **Collect Results** → Document in `/Dokumente/01_in Arbeit/`
6. **Compression** → Normalize and deduplicate findings while preserving all information
7. **Self-Review** → Quality check and possibly further searches
8. **Finalization** → Formatting and archiving
9. **User-Review** → Approval and indexing

---

## Phase 1: Analysis & Planning

**IMPORTANT**: Use the thinking process with `mcp__sequential-thinking__sequentialthinking` tool for planning and review!

### Thinking Process

Analyze the user request systematically:

**0. Optional: Clarification Check**

Ask the user ONLY when:
- **Ambiguous acronyms/abbreviations**: e.g. "ML" could mean "Machine Learning" or "Markup Language"
- **Unknown technical terms without context**: Specialized terms that can have different meanings
- **Missing critical information**: e.g. "Compare ML frameworks" - which aspect? Performance? Ease of use? Cost?
- **Unclear scope definition**: e.g. "recent developments" - last month? Last year? Last 5 years?
- **Contradictory requirements**: User asks for A and B, but A excludes B

**Do NOT ask when:**
- The question is clear enough to start
- You've already asked once (maximum 1x clarification!)
- It's only about additional "nice-to-have" details

**Structured Clarification Format:**

When clarification is needed, use this format:

```
I need clarification on the following before starting research:

**[Aspect 1]**: [Specific question]
- Option A: [...]
- Option B: [...]
- Option C: [...]

**[Aspect 2]**: [Specific question]

Once clarified, I'll proceed with research focusing on [brief summary of planned approach].
```

**Example:**
```
I need clarification on the following before starting research:

**Comparison Criteria**: What aspects should I prioritize when comparing ML frameworks?
- Technical focus (performance, scalability, architecture)
- Developer experience (ease of use, documentation, learning curve)
- Ecosystem (community, libraries, deployment options)
- All of the above

**Time Scope**: What timeframe should I focus on?
- Latest developments (2024-2025)
- Mature stable versions (last 3-5 years)

Once clarified, I'll spawn 3-5 workers to research frameworks across your specified dimensions.
```

**1. Identify main question**
- What is the central question?
- What language is the user's request in? (Research MUST be in the same language!)

**2. Assess complexity & determine number of sub-agents**

**Adaptive Parallelization - Choose 1-5 Sub-Agents:**

**1 Sub-Agent** - Simple, focused questions:
- Definitions of individual terms
- Single facts or lists
- Straightforward how-to questions
- Example: "What is quantum computing?"
- Example: "List top 10 JavaScript frameworks 2025"

**2-3 Sub-Agents** - Comparisons or multiple aspects:
- Comparisons between 2-3 things
- Questions with 2-3 clearly delineated sub-aspects
- Example: "Compare React vs Vue vs Angular"
- Example: "Explain pros and cons of cloud computing"

**4-5 Sub-Agents** - Complex, multi-layered analyses:
- Comprehensive topics with many facets
- In-depth analyses with multiple independent areas
- State-of-the-art overviews
- Example: "How does machine learning work?" → 5 areas
- Example: "Deep Research Best Practices 2025" → 5 aspects

**3. Define sub-areas**
- Which specific aspects need to be researched?
- One sub-area = One sub-agent

**4. Formulate search queries**
- Which specific search queries cover each sub-area?

**5. Expected results**
- What should each search deliver?

---

**Example thinking for "How does machine learning work?" (Complex → 5 Sub-Agents)**:
- Sub-area 1: Fundamentals and definitions
- Sub-area 2: Most important algorithms (Supervised, Unsupervised, Reinforcement)
- Sub-area 3: Practical applications and use cases
- Sub-area 4: Tools and frameworks
- Sub-area 5: Current trends and developments

**Example thinking for "Compare Python vs JavaScript" (Comparison → 2 Sub-Agents)**:
- Sub-area 1: Python - Strengths, use cases, ecosystem
- Sub-area 2: JavaScript - Strengths, use cases, ecosystem

**Example thinking for "What is React?" (Simple → 1 Sub-Agent)**:
- Sub-area 1: React definition, concepts, application

---

## Phase 2: Research Question Transformation

**Purpose**: Transform the user's request into a detailed, unambiguous research brief that workers can execute effectively.

**IMPORTANT**: Use the thinking process with `mcp__sequential-thinking__sequentialthinking` tool for this transformation!

### Transformation Guidelines

Apply these principles to create a detailed research question:

**1. Maximize Specificity and Detail**
- Include all known user preferences explicitly
- List key attributes or dimensions to consider
- Ensure all details from the user are included

**2. Fill Unstated But Necessary Dimensions as Open-Ended**
- If certain attributes are essential but not specified, explicitly state they are open-ended
- Don't invent constraints - state the lack of specification
- Guide workers to treat unstated aspects as flexible

**3. Avoid Unwarranted Assumptions**
- If the user hasn't provided a detail, don't create one
- State when something is unspecified
- Accept all possible options for unstated criteria

**4. Use First Person Perspective**
- Phrase the research brief from the user's perspective
- Example: "I need to understand..." rather than "The user wants..."

**5. Specify Source Preferences**
- If specific sources should be prioritized, state them explicitly
- For product/travel research: Prefer official sites, manufacturer pages, reputable e-commerce
- For academic/scientific: Prefer original papers, official journal publications
- For people: Prefer LinkedIn profiles, personal websites
- For language-specific queries: Prioritize sources in that language

**6. Handle Time Sensitivity**
- If the topic is time-sensitive, specify the relevant timeframe
- For "latest" or "current": Explicitly state 2024-2025 or current year
- For historical: Specify the time period of interest

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

**Example 2: Comparison Query**

Original: "Compare ML frameworks"

Transformed (after clarification):
```
I need a comprehensive comparison of machine learning frameworks (TensorFlow, PyTorch, JAX) focusing on:
- Technical aspects: performance, scalability, architecture
- Developer experience: ease of use, documentation, learning curve
- Ecosystem: community support, available libraries, deployment options
- Production readiness: stability, industry adoption, maintenance

Prioritize official documentation, recent benchmarks from 2024-2025, and authoritative technical sources.
Target audience: Technical decision-maker selecting framework for production ML project.
Language: English
```

**Example 3: Complex Research**

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

After transformation, present the research brief:

```markdown
## Transformed Research Brief

**Original Request**: {User's original question}

**Detailed Research Question**:
{Transformed detailed research question with all specifications}

**Key Dimensions**:
- {Dimension 1}
- {Dimension 2}
- {Dimension 3}

**Source Priorities**: {Any specific source guidance}

**Language**: {Target language for research}

**Time Scope**: {Relevant timeframe if applicable}
```

This transformed brief will be used to guide worker agents and ensure consistent, comprehensive research.

---

## Phase 3: Create Task List

Create a Markdown file with checkboxes in `/Aufgaben/`.

### Filename Format

`YYYY-MM-DD_Research_{Topic}.md`

**Example**: `2025-10-23_Research_Machine_Learning.md`

### Task List Format

```markdown
# Research: {Topic}

**Created**: {Date} {Time}
**Status**: In Progress

## Main Question
{The original user request}

## Sub-Tasks

- [ ] {Sub-area 1}: {Brief description}
- [ ] {Sub-area 2}: {Brief description}
- [ ] {Sub-area 3}: {Brief description}
- [ ] Compression: Normalize and deduplicate findings
- [ ] Self-Review: Quality check of results
- [ ] Finalization: Formatting and summary
```

### Storage Location

`Aufgaben/{Filename}` (relative to working directory)

---

## Phase 4: Parallel Research

**SUPERVISOR ROLE**: You coordinate multiple `web-research-specialist` subagents.

### Spawn Subagents

Use the `Task` tool with `subagent_type: "web-research-specialist"` for **EACH** sub-area.

**IMPORTANT**: Spawn all subagents **in parallel** in a single message!

**Number of Sub-Agents**: Based on complexity assessment from Phase 1 (1-5 Sub-Agents)

**Example for complex question (5 Sub-Agents)**:

```markdown
I'm now spawning 5 web-research-specialist subagents in parallel:

- Subagent 1: Machine learning fundamentals
- Subagent 2: Supervised vs Unsupervised Learning
- Subagent 3: Neural Networks and Deep Learning
- Subagent 4: ML Frameworks (TensorFlow, PyTorch)
- Subagent 5: Current trends 2024/2025
```

**Example for simple question (1 Sub-Agent)**:

```markdown
I'm spawning 1 web-research-specialist subagent:

- Subagent 1: React definition, concepts and application
```

**Use ONE message block with all Task tool calls!**

---

### Prompt Structure for Subagents

Each subagent receives a clear task (the agent knows how to research on its own):

```
Research: {Specific question for this sub-area}

Focus:
- {Aspect 1}
- {Aspect 2}
- {Aspect 3}

IMPORTANT: Respond in the same language as the original user request.
```

**Note**: The agent has its own research prompt with methodology, tool preference, and output format. Only give it the task, not the HOW.

---

## Phase 5: Collect Results

Create a **Research Document** in `/Dokumente/01_in Arbeit/`.

### Filename Format

`Research_{Topic}_{Date}.md`

**Example**: `Research_Machine_Learning_2025-10-23.md`

### Document Structure

```markdown
# Research: {Topic}

**Created**: {Date}
**Researched by**: Claude Deep Research Agent
**Status**: In Progress

---

## Overview

{Brief introduction to the question}

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
- {URL 1}
- {URL 2}

---

... (additional sub-areas)

---

## Summary

{Will be added in Phase 6}
```

### Workflow per Subagent

1. Subagent returns result
2. **Immediately**: Insert result into research document (append or edit)
3. **Immediately**: Check off checkbox in task list (`- [x]`)
4. Continue to next subagent

**IMPORTANT**: Update task list **after each** completed sub-task!

### Supervisor-Worker Pattern Best Practice

**Supervisor has full visibility, Workers only filtered context:**

✅ **Supervisor** (You):
- Sees all worker results
- Has complete task list and overall overview
- Integrates everything into ONE central document
- Coordinates the entire workflow

✅ **Workers** (Subagents):
- Receive only their specific sub-task
- Return ONLY text results (no documents!)
- NO visibility of other workers
- NO document creation (Supervisor integrates)

### Storage Location

`Dokumente/01_in Arbeit/{Filename}` (relative to working directory)

---

## Phase 6: Compression

**Purpose**: Normalize and deduplicate worker findings while preserving ALL substantive information. This prepares the research for self-review and final synthesis.

**IMPORTANT**: This is NOT summarization - you must preserve all relevant information verbatim. Only remove redundancy and normalize formatting.

### Compression Process

**Step 1: Read Complete Research Document**

Use the `Read` tool to load the entire research document from `Dokumente/01_in Arbeit/{Filename}`.

**Step 2: Analysis with Thinking Tool**

Use `mcp__sequential-thinking__sequentialthinking` to identify:

1. **Duplicate Information**:
   - Same facts stated by multiple workers
   - Overlapping findings across sections
   - Repeated source citations

2. **Contradictions or Discrepancies**:
   - Workers providing conflicting information
   - Different interpretations of the same topic
   - Inconsistent data points

3. **Formatting Inconsistencies**:
   - Different heading styles
   - Varied citation formats
   - Inconsistent bullet point or numbering usage

4. **Citation Overlaps**:
   - Same URL cited multiple times with different numbers
   - Missing source details
   - Broken or incomplete citations

**Step 3: Compress and Normalize**

Update the research document with these changes:

**A. Merge Duplicates**

When multiple workers report the same information:
```markdown
# Before (redundant):
## Section 1
React is a JavaScript library [1].

## Section 2
React is a JavaScript library for building UIs [2].

# After (compressed):
## Overview
React is a JavaScript library for building user interfaces [1][2].
```

**B. Handle Contradictions**

When workers provide conflicting information, preserve both views:
```markdown
# Conflicting Information:
Some sources indicate React 19 was released in December 2024 [1], while others suggest
early 2025 [2][3]. The official React blog confirms the stable release date as
December 5, 2024 [1].
```

**C. Normalize Citations**

Renumber citations sequentially (1, 2, 3, 4...) with NO gaps:
```markdown
# Before:
Finding from worker 1 [1][2].
Finding from worker 2 [5][7].
Finding from worker 3 [2][9].

# After:
Finding from worker 1 [1][2].
Finding from worker 2 [3][4].
Finding from worker 3 [2][5].

### Sources
[1] Source A: https://...
[2] Source B: https://...
[3] Source C: https://...
[4] Source D: https://...
[5] Source E: https://...
```

**D. Standardize Formatting**

- Ensure consistent heading hierarchy (##, ###)
- Use uniform bullet point style
- Apply consistent code block formatting
- Normalize spacing and line breaks

**Step 4: Verify Preservation**

Critical checkpoint - verify that:
- ✅ All substantive facts from original are retained
- ✅ All sources from workers are preserved
- ✅ No information was lost during compression
- ✅ Contradictions are flagged, not resolved arbitrarily
- ✅ Citations are complete and correctly numbered

**Step 5: Update Document**

Use the `Edit` tool to update the research document with the compressed version.

### What to Compress

**DO compress:**
- ✅ Redundant statements of the same fact
- ✅ Duplicate source citations
- ✅ Formatting inconsistencies
- ✅ Repetitive introductions/conclusions
- ✅ Overlapping explanations of the same concept

**DO NOT compress:**
- ❌ Different perspectives on the same topic
- ❌ Specific examples or use cases
- ❌ Technical details or data points
- ❌ Nuanced differences in explanations
- ❌ Source-specific insights

### Example Compression

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

### Compression Checklist

When compression is complete, verify:
- [ ] All worker findings integrated (none discarded)
- [ ] Duplicate information merged
- [ ] Contradictions flagged explicitly
- [ ] Citations renumbered sequentially (no gaps)
- [ ] All sources preserved with correct URLs
- [ ] Formatting consistent throughout
- [ ] Document structure logical and clear
- [ ] No information lost (verify against original)

This compressed document is now ready for self-review.

---

## Phase 7: Self-Review

**MANDATORY** before finalization!

### Review Process

1. **Read research document** (complete document with `Read` tool)
2. **Thinking process** with `mcp__sequential-thinking__sequentialthinking`:
   - Was the main question sufficiently answered?
   - Are there open questions or gaps?
   - Is the information current (date check)?
   - Are important aspects missing?

3. **Pragmatic Quality Checks**:
   - [ ] Critical facts confirmed by multiple sources (if multiple mentioned)
   - [ ] Contradictions resolved or explicitly mentioned
   - [ ] Main sources are authoritative (not just blogs/social media)
   - [ ] Timeliness fits the topic (for time-sensitive topics)

### Decision

**Option A: Sufficiently answered**
→ Continue to Phase 8 (Finalization)

**Option B: Further research needed**
→ Back to Phase 4:
1. Add new sub-tasks to task list
2. Spawn new subagents for missing aspects
3. Integrate results into existing document
4. Perform self-review again

### Review Checkbox

When self-review is completed:
- Check off checkbox in task list: `- [x] Self-Review: Quality check of results`

---

## Phase 8: Finalization

### Write Summary

Add to the `## Summary` section in the research document:

```markdown
## Summary

### Key Findings
1. {Main finding 1}
2. {Main finding 2}
3. {Main finding 3}

### Answer to the Main Question
{Direct, precise answer to the original user request}

### Further Information
- {Link/Topic 1}
- {Link/Topic 2}
```

### Check Formatting

- Headings correctly hierarchical
- All sources linked
- Markdown formatting consistent
- Readability ensured

### Archiving

**Step 1: Move task list**

From: `/Aufgaben/{Filename}`
To: `/Aufgaben/Archiv/{Filename}`

**Step 2: Move document**

From: `/Dokumente/01_in Arbeit/{Filename}`
To: `/Dokumente/02_Review/{Filename}`

**Use `Bash` with `mv` command**:

```bash
mv "Aufgaben/{Filename}" "Aufgaben/Archiv/{Filename}"

mv "Dokumente/01_in Arbeit/{Filename}" "Dokumente/02_Review/{Filename}"
```

### Finalization Checkbox

Check off checkbox: `- [x] Finalization: Formatting and summary`

---

## Phase 9: User-Review

### Present Result

Show the user:

1. **Link to research document**: `Dokumente/02_Review/{Filename}`
2. **Brief summary** of key findings (2-3 sentences)
3. **Review request**:

```markdown
---

## Research Completed

The research document is ready and awaiting your review:

📄 **Document**: [Dokumente/02_Review/{Filename}](Dokumente/02_Review/{Filename})

### Key Findings
- {Finding 1}
- {Finding 2}
- {Finding 3}

---

**Are you satisfied with the result?**

- ✅ **Yes, approve** → Document will be moved to `Dokumente/` and indexed
- 🔄 **Revision** → Tell me what should be adjusted
```

### After Confirmation

**If user confirms**:

**Step 1: Move document**

From: `/Dokumente/02_Review/{Filename}`
To: `/Dokumente/{Filename}`

```bash
mv "Dokumente/02_Review/{Filename}" "Dokumente/{Filename}"
```

**Step 2: Update INDEX.md**

File: `Dokumente/INDEX.md` (relative to working directory)

1. Read INDEX.md
2. Add new entry:

```markdown
- **{Date}** - [{Topic}]({Filename}) - Research: {Brief description}
```

3. Sorting: Newest entries at top

**Step 3: Confirmation**

```markdown
✅ **Research completed and archived!**

- Document: [Dokumente/{Filename}](Dokumente/{Filename})
- Index updated: [Dokumente/INDEX.md](Dokumente/INDEX.md)
```

---

## Core Principles

1. **Structured clarification**: Use structured format when asking for clarification
2. **Transform questions**: Convert user requests into detailed research briefs (Phase 2)
3. **Thinking first**: Always use `mcp__sequential-thinking__sequentialthinking` for planning, transformation, and compression
4. **Parallel subagents**: Spawn all `web-research-specialist` in **one** message
5. **Supervisor role**: You coordinate, subagents research
6. **Continuous updates**: Update task list and document **immediately** after each sub-task
7. **Compression is mandatory**: Clean and normalize findings before self-review (Phase 6)
8. **Self-review is mandatory**: Quality over speed (Phase 7)
9. **Strict folder management**: `01_in Arbeit` → `02_Review` → `Dokumente/`
10. **Always user-review**: Never finalize without approval (Phase 9)

---

## Path Reference

**All paths relative to working directory**

```
├── Aufgaben/
│   ├── {Tasklist}.md              ← Phase 3: Created
│   └── Archiv/
│       └── {Tasklist}.md          ← Phase 8: Moved

├── Dokumente/
│   ├── 01_in Arbeit/
│   │   └── {Research-Doc}.md       ← Phase 5: Created → Phase 6: Compressed
│   ├── 02_Review/
│   │   └── {Research-Doc}.md       ← Phase 8: Moved
│   ├── {Research-Doc}.md           ← Phase 9: Finally moved
│   └── INDEX.md                    ← Phase 9: Updated
```

---

## Error Handling

### Subagent delivers no results

- Note in research document: `{Sub-area}: No sufficient results found`
- Check in self-review whether critical
- If necessary, use different search terms and spawn new subagent

### User requests revision

- Clarify user requirements
- Add new sub-tasks to task list
- Spawn additional subagents or manually revise sections
- Go through workflow again (from Phase 7)
