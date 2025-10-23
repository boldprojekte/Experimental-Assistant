# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal AI assistant project for Jan-Peter Franke that integrates with:
- **ClickUp** (project management) via MCP server with dedicated skill
- **Google Calendar** (calendar management) via MCP server with dedicated skill
- **Gmail** (email management) via MCP server

## Project Structure

```
├── .claude/
│   ├── skills/
│   │   ├── clickup/           # ClickUp workflow skill (SKILL.md)
│   │   └── calendar/          # Calendar workflow skill (SKILL.md)
│   └── settings.local.json    # MCP tool permissions
├── Dokumente/                 # Document management
│   ├── 00_Archiv/            # Archived documents
│   ├── 00_in Arbeit/         # Documents being worked on by AI/user
│   └── 00_Review/            # Documents awaiting user review
├── Aufgaben/                  # Active task lists
│   └── Archiv/               # Completed task lists
└── Skripte/                   # Code scripts for tasks
```

### Document Workflow

Documents follow a specific lifecycle:
1. **00_in Arbeit**: Active work by AI agent and user
2. **00_Review**: Ready for user review after AI completion
3. **Parent folder**: After review is complete
4. **00_Archiv**: No longer needed

Task lists in `Aufgaben/` are actively maintained to track progress and coordination. Completed lists move to `Aufgaben/Archiv/`.

## ClickUp Integration

**CRITICAL**: Always use the ClickUp skill when working with ClickUp operations.

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

**CRITICAL**: Always use the Calendar skill when working with calendar operations.

### When to Invoke the Calendar Skill

Use the skill for ANY calendar-related operations:
- Viewing/retrieving calendar events (today, this week, next week, etc.)
- Creating new appointments or meetings
- Deleting calendar events
- Checking for scheduling conflicts
- Any operation involving both business and personal calendars

**Invoke the skill**: Use `Skill` tool with command `calendar` before calling any `mcp__Calendar__*` tools.

**NEVER call Calendar MCP tools directly** without first loading the skill. The skill contains critical calendar selection logic (business vs. personal) and conflict-checking requirements.