# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal AI assistant project for Jan-Peter Franke that integrates with:
- **ClickUp** (project management) via MCP server with dedicated skill
- **Google Calendar** (calendar management) via MCP server with dedicated skill
- **Gmail** (email management) via MCP server with dedicated skill
- **Playwright** (browser automation) via MCP server with dedicated skill

## Project Structure

```
├── .claude/
│   ├── skills/
│   │   ├── clickup/           # ClickUp workflow skill (SKILL.md)
│   │   ├── calendar/          # Calendar workflow skill (SKILL.md)
│   │   ├── gmail/             # Gmail workflow skill (SKILL.md)
│   │   ├── browser/           # Browser automation skill (SKILL.md)
│   │   ├── deep-research/     # Deep Research workflow skill (SKILL.md)
│   │   └── scripts/           # Scripts creation/execution skill (SKILL.md)
│   ├── agents/                # Subagent definitions (e.g., web-research-specialist.md)
│   └── settings.local.json    # MCP tool permissions
├── Dokumente/                 # Document management
│   ├── 01_in Arbeit/         # Documents being worked on by AI/user
│   ├── 02_Review/            # Documents awaiting user review
│   ├── INDEX.md              # Document index
│   └── 00_Archiv/            # Archived documents
├── Aufgaben/                  # Active task lists
│   └── Archiv/               # Completed task lists
└── Skripte/                   # Code scripts for tasks
```

### Document Workflow

Documents follow a specific lifecycle:
1. **01_in Arbeit**: Active work by AI agent and user
2. **02_Review**: Ready for user review after AI completion
3. **Parent folder** (`Dokumente/`): After review is complete and approved
4. **00_Archiv**: No longer needed

Task lists in `Aufgaben/` are actively maintained to track progress and coordination. Completed lists move to `Aufgaben/Archiv/`.

Documents can be indexed in `Dokumente/INDEX.md` for easy retrieval.

### Language Handling

**CRITICAL**: Documents and responses must match the language of the user's request:
- German folder names are part of the workflow structure (Dokumente, Aufgaben, Skripte)
- All prompts and skills are in English for consistency
- **Documents created must be in the SAME language as the user's request**
- Agent responses should match the request language

**Example**: User asks in German → Document in German. User asks in English → Document in English.

### Task Naming Convention

Task lists in `Aufgaben/` follow a consistent naming pattern:
- Research tasks: `YYYY-MM-DD_Research_{Topic}.md`
- General tasks: `YYYY-MM-DD_Task_{Description}.md`

**Example**: `2025-10-23_Research_Machine_Learning.md` or `2025-10-23_Task_Update_Documentation.md`

## ClickUp Integration

**IMPORTANT**: Always use the ClickUp skill when working with ClickUp operations.

### When to Invoke the ClickUp Skill

Use the skill for ANY ClickUp-related operations:
- Creating, editing, or searching tasks
- Showing all tasks in a project/list
- Managing contacts (Kontakte)
- Creating documents
- Organizing lists or folders
- Starting/stopping time tracking

**Invoke the skill**: Use `Skill` tool with command `clickup` before calling any `mcp__clickup__*` tools.

**NEVER call ClickUp MCP tools directly** without first loading the skill. The skill contains critical workflow guidance, workspace structure, and search strategy logic.

## Calendar Integration

**IMPORTANT**: Always use the Calendar skill when working with calendar operations.

### When to Invoke the Calendar Skill

Use the skill for ANY calendar-related operations:
- Viewing/retrieving calendar events (today, this week, next week, etc.)
- Creating new appointments or meetings
- Deleting calendar events
- Checking for scheduling conflicts
- Any operation involving both business and personal calendars

**Invoke the skill**: Use `Skill` tool with command `calendar` before calling any `mcp__Calendar__*` tools.

**NEVER call Calendar MCP tools directly** without first loading the skill. The skill contains critical calendar selection logic (business vs. personal) and conflict-checking requirements.

## Gmail Integration

**IMPORTANT**: Always use the Gmail skill when working with email operations.

### When to Invoke the Gmail Skill

Use the skill for ANY Gmail-related operations:
- Searching for emails or threads
- Reading messages or conversations
- Replying to emails
- Managing labels (adding, removing, creating)
- Creating or managing drafts
- Organizing inbox (mark as read/unread, delete)
- Any operation involving email management

**Invoke the skill**: Use `Skill` tool with command `gmail` before calling any `mcp__Gmail__*` tools.

**NEVER call Gmail MCP tools directly** without first loading the skill. The skill contains critical search strategy guidance, workflow patterns, and email organization logic.

## Deep Research Integration

**IMPORTANT**: Always use the Deep Research skill for comprehensive internet research tasks.

### When to Invoke the Deep Research Skill

Use the skill for ANY deep research operations:
- Comprehensive internet research requiring multiple sources
- Complex research questions that need to be broken down into sub-questions
- Research tasks requiring parallel web searches
- Detailed analysis and investigation of topics
- Research that needs structured documentation and tracking

**Invoke the skill**: Use `Skill` tool with command `deep-research` before starting any multi-source research.

**NEVER spawn web-research-specialist subagents directly** without first loading the skill. The skill contains critical workflow orchestration.

### Examples: When to use deep-research vs. WebSearch

**Use deep-research skill for:**
- Complex topics requiring 3+ independent sub-topics
- Comparisons with multiple aspects to analyze
- Comprehensive analysis from various angles
- Topics requiring synthesis of multiple sources

**Use WebSearch tool for:**
- Simple definitions or single facts
- Straightforward questions answerable in 1-2 searches
- Quick lookups or current information

**Rule of thumb**: If the answer requires breaking down into 3+ sub-topics → use deep-research. Otherwise → use WebSearch.

See the deep-research skill for detailed complexity assessment guidance and examples.

## Browser Integration

**IMPORTANT**: Always use the Browser skill when working with browser automation tasks.

### When to Invoke the Browser Skill

Use the skill for ANY browser automation operations:
- Navigating websites and extracting information
- Taking screenshots of web pages
- Interacting with web applications
- Automated browsing tasks
- Web scraping or data extraction
- Any task requiring visual interaction with websites, the user can see as well

**Invoke the skill**: Use `Skill` tool with command `browser` before calling any `mcp__playwright__*` tools.

**NEVER call Playwright MCP tools directly** without first loading the skill. The skill contains critical workflow patterns (Navigate → Snapshot → Interact → Verify) and permission requirements.

### When to Use Browser vs. Other Tools

**Use Browser when:**
- Forms require visual interaction (CAPTCHAs, dynamic fields)
- Multi-step processes with page transitions
- JavaScript-heavy sites (SPAs)
- Login sessions required
- User wants to watch the interaction process

**Use WebFetch/WebSearch when:**
- Simple information retrieval
- Static content extraction
- No interaction needed
- Faster, lighter approach is sufficient

## Scripts Integration

**IMPORTANT**: Always use the Scripts skill when working with scripts in `Skripte/`.

### When to Invoke the Scripts Skill

Use the skill for ANY script-related operations:
- Creating new scripts
- Running existing scripts
- Organizing script directories
- When the user asks for something that can only be done with a script (utility tool)

**Invoke the skill**: Use `Skill` tool with command `scripts` before working with `Skripte/`.

**NEVER create or run scripts** without first loading the skill. The skill contains critical organization and workflow patterns.