# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

Personal AI assistant for Jan-Peter Franke integrating:
- **ClickUp** (project management)
- **Google Calendar** (calendar management)
- **Gmail** (email management)
- **Playwright** (browser automation)
- **Archicad** (CAD automation for architecture)

All integrations use MCP servers with dedicated workflow skills.

## Project Structure

```
├── .claude/
│   ├── skills/           # Workflow skills (SKILL.md)
│   │   ├── clickup/
│   │   ├── calendar/
│   │   ├── gmail/
│   │   ├── browser/
│   │   ├── archicad/
│   │   ├── deep-research/
│   │   ├── scripts/
│   │   └── rag/
│   ├── agents/           # Subagent definitions
│   └── settings.local.json
├── Dokumente/            # Document management
│   ├── 01_in Arbeit/    # Active work
│   ├── 02_Review/       # Awaiting review
│   ├── 03_RAG/          # Long-term knowledge base
│   ├── INDEX.md         # Document index
│   └── 00_Archiv/       # Archived
├── Aufgaben/             # Active task lists
│   └── Archiv/          # Completed tasks
└── Skripte/              # Utility scripts
```

## Conventions

### Document Workflow

Documents follow this lifecycle:
1. **01_in Arbeit** → Active work by AI/user
2. **02_Review** → Ready for user review
3. **Dokumente/** → Reviewed and approved
4. **00_Archiv** → No longer needed

Task lists in `Aufgaben/` track active progress. Completed lists move to `Aufgaben/Archiv/`.

### Language Handling

**CRITICAL**: Match document language to user's request language.
- Folder names (Dokumente, Aufgaben, Skripte) remain in German
- Skills and prompts remain in English
- **Document content matches request language**

### Task Naming

Task lists follow: `YYYY-MM-DD_{Type}_{Topic}.md`
- Research: `2025-10-23_Research_Machine_Learning.md`
- General: `2025-10-23_Task_Update_Documentation.md`

## Skills Routing

**CRITICAL**: Always invoke the appropriate skill BEFORE calling MCP tools directly. Skills contain workflow logic, search strategies, and operational patterns that are essential for correct execution.

### Quick Reference

| Skill | When to Invoke | MCP Tool Pattern |
|-------|----------------|------------------|
| `clickup` | Task/project management operations | `mcp__clickup__*` |
| `calendar` | Calendar and scheduling operations | `mcp__Calendar__*` |
| `gmail` | Email management operations | `mcp__Gmail__*` |
| `browser` | Web automation and interaction | `mcp__playwright__*` |
| `archicad` | CAD automation and design operations | `mcp__archicad__*` |
| `deep-research` | Complex multi-source research | Web-research subagents |
| `scripts` | Code utilities and conversions | `Skripte/` directory |
| `rag` | Knowledge indexing and retrieval | `Skripte/rag-search/*.py` |

### Skill-Specific Guidance

**ClickUp** (`clickup`)
- Invoke for: Creating/editing/searching tasks, managing contacts, creating documents, organizing lists/folders, time tracking
- **Never** call `mcp__clickup__*` tools directly
- Skill contains: Workspace structure, search strategies, workflow guidance

**Calendar** (`calendar`)
- Invoke for: Viewing/creating/deleting events, checking conflicts, scheduling meetings
- **Never** call `mcp__Calendar__*` tools directly
- Skill contains: Calendar selection logic (business vs. personal), conflict-checking workflows

**Gmail** (`gmail`)
- Invoke for: Searching/reading/replying to emails, managing labels/drafts, organizing inbox
- **Never** call `mcp__Gmail__*` tools directly
- Skill contains: Search strategies, email composition patterns, organization workflows

**Browser** (`browser`)
- Invoke for: Website navigation, screenshots, form interaction, web scraping, visual interaction
- **Never** call `mcp__playwright__*` tools directly
- Skill contains: Interaction workflows, permission requirements, automation patterns

**Archicad** (`archicad`)
- Invoke for: CAD automation, creating/modifying elements, querying project data, managing layers/views, Archicad control
- **Never** call `mcp__archicad__*` tools directly
- Skill contains: Multi-instance management, semantic tool discovery, workflow patterns
- **Critical**: Always discover instances first, use natural language for tool discovery

**Deep Research** (`deep-research`)
- Invoke for: Comprehensive research requiring multiple sources, complex analysis, topic synthesis
- **Never** spawn `web-research-specialist` subagents directly
- Skill contains: Task decomposition, parallel research coordination, documentation workflows

**Scripts** (`scripts`)
- Invoke for: File conversions, data processing, automation, learning new tools through code
- **Never** work with `Skripte/` without loading skill first
- Skill contains: Script organization, discovery workflows, INDEX management
- **Critical**: Always check `Skripte/INDEX.md` before installing new tools

**RAG** (`rag`)
- Invoke for: Indexing documents into long-term memory, querying knowledge base, retrieving information from stored documents
- **Never** call `rag_index.py` or `rag_query.py` directly
- Skill contains: Knowledge base management, query reformulation strategies, answer synthesis from chunks
- **Critical**: Always load skill before knowledge management operations

### Decision Criteria

When choosing between similar tools, use these guidelines:

**Research: `deep-research` vs `WebSearch`**

Use `deep-research` skill when:
- Complex topics requiring 3+ independent sub-topics
- Comparisons with multiple aspects to analyze
- Comprehensive analysis from various angles
- Topics requiring synthesis of multiple sources
- Parallel research coordination needed

Use `WebSearch` tool when:
- Simple definitions or single facts
- Straightforward questions answerable in 1-2 searches
- Quick lookups or current information
- Time-sensitive queries requiring fast answers

**Web Access: `browser` vs `WebFetch`**

Use `browser` skill when:
- Forms require visual interaction (CAPTCHAs, dynamic fields)
- Multi-step processes with page transitions
- JavaScript-heavy sites (SPAs)
- Login sessions required
- User wants to watch the interaction process
- Complex web scraping with dynamic content

Use `WebFetch` tool when:
- Simple information retrieval from static pages
- Static content extraction
- No interaction needed
- Faster, lighter approach is sufficient
- Reading documentation or articles

**Tool Installation: Scripts First**

Before installing any new tools or writing conversion/processing code:
1. **ALWAYS** check `Skripte/INDEX.md` first
2. Look for existing scripts that solve the problem
3. Only install new tools if no script exists

Examples:
- ❌ "make PDF" → Install Pandoc directly
- ✅ "make PDF" → Load `scripts` skill → Check INDEX.md → Use `markdown-zu-pdf`
- ❌ "transcribe audio" → Install Whisper
- ✅ "transcribe audio" → Load `scripts` skill → Check INDEX.md → Use existing script

**Knowledge Retrieval: `rag` vs `WebSearch` vs File Reading**

Use `rag` skill when:
- User asks about previously saved knowledge
- Querying long-term memory (`Dokumente/03_RAG/`)
- Need to retrieve information from indexed documents
- Searching across multiple documents with semantic understanding

Use `WebSearch` tool when:
- Need current/live information from the internet
- User explicitly asks to search the web
- Information is not in knowledge base
- Time-sensitive or recent events

Use File Reading (Read/Grep tools) when:
- Specific file location is known
- Need exact file content
- Working with active documents (`01_in Arbeit/`, `02_Review/`)
- Code navigation or debugging
