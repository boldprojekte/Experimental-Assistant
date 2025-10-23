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
2. **Create Task List** → Markdown file with checkboxes in `/Aufgaben/`
3. **Parallel Research** → Spawn multiple `web-research-specialist` subagents
4. **Collect Results** → Document in `/Dokumente/01_in Arbeit/`
5. **Self-Review** → Quality check and possibly further searches
6. **Finalization** → Formatting and archiving
7. **User-Review** → Approval and indexing

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

## Phase 2: Create Task List

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
- [ ] Self-Review: Quality check of results
- [ ] Finalization: Formatting and summary
```

### Storage Location

`Aufgaben/{Filename}` (relative to working directory)

---

## Phase 3: Parallel Research

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

## Phase 4: Collect Results

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

## Phase 5: Self-Review

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
→ Continue to Phase 6 (Finalization)

**Option B: Further research needed**
→ Back to Phase 3:
1. Add new sub-tasks to task list
2. Spawn new subagents for missing aspects
3. Integrate results into existing document
4. Perform self-review again

### Review Checkbox

When self-review is completed:
- Check off checkbox in task list: `- [x] Self-Review: Quality check of results`

---

## Phase 6: Finalization

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

## Phase 7: User-Review

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

1. **Thinking first**: Always use `mcp__sequential-thinking__sequentialthinking` for planning and review
2. **Parallel subagents**: Spawn all `web-research-specialist` in **one** message
3. **Supervisor role**: You coordinate, subagents research
4. **Continuous updates**: Update task list and document **immediately** after each sub-task
5. **Self-review is mandatory**: Quality over speed
6. **Strict folder management**: `01_in Arbeit` → `02_Review` → `Dokumente/`
7. **Always user-review**: Never finalize without approval

---

## Path Reference

**All paths relative to working directory**

```
├── Aufgaben/
│   ├── {Tasklist}.md              ← Phase 2: Created
│   └── Archiv/
│       └── {Tasklist}.md          ← Phase 6: Moved

├── Dokumente/
│   ├── 01_in Arbeit/
│   │   └── {Research-Doc}.md       ← Phase 4: Created
│   ├── 02_Review/
│   │   └── {Research-Doc}.md       ← Phase 6: Moved
│   ├── {Research-Doc}.md           ← Phase 7: Finally moved
│   └── INDEX.md                    ← Phase 7: Updated
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
- Go through workflow again (from Phase 5)
