---
name: ClickUp
description: Workflow guide for ClickUp operations. Use for creating tasks, editing tasks, searching tasks, showing all tasks in project, managing contacts (located in Backoffice Space), creating documents, organizing lists, creating folders, starting time tracking, or stopping time tracking. Critical for correct search strategy selection and workspace structure understanding.
---

# ClickUp Workflow

Workflow guide for ClickUp operations with focus on correct search strategy and workspace structure.

## Workspace Structure

**IMPORTANT** for determining where to create or find elements.

### Spaces Overview

- **Personal List** (ID: `901208069739`) - Private tasks. **HIDDEN** space, not visible in hierarchy queries. Use for all personal/private tasks.
- **Privat** - Only private notes and documents (NOT for tasks!)
- **Operations** - Architecture projects (Format: Project number + Location + Street)
- **Gut Gewohnt** - Real estate project development (with Robert Crummenerl)
- **Backoffice** - Accounting, purchases, **Contacts**, vacation calendar
- **Process Library** - ClickUp templates (Project folders with pre-configured tasks)
- **Growth** - Growth tasks/documents (Website, Marketing, Acquisition)
- **baumeet.ing** - Construction protocol SaaS platform

## Search Strategy

**IMPORTANT**: Choose the correct search approach based on the request.

### Context-Based Search (all tasks in project/list/space)

Use when user asks for "all tasks in X" or "show project Y tasks":

1. Use `clickup_get_workspace_hierarchy` to identify list/folder ID
2. Use `clickup_get_workspace_tasks` with `list_ids` or `folder_ids`
3. **NEVER use `clickup_search`** - only searches titles, misses most tasks

### Keyword Search (find specific task)

Use when searching for a specific task by name/keyword:

1. Use `clickup_search` with search terms
2. Identify correct task from results

**Examples:**
- "Find task 'Call Kaya'" → `clickup_search` with keywords
- "Where is the invoice for supplier X?" → `clickup_search`

### Search Before Modify

Always search for existing element before update/edit:
- Use `clickup_search` for tasks by name
- Verify existence before update tool call

## Task Operations

### Default Settings

Apply unless explicitly specified otherwise:
- **Priority**: normal
- **Assignee**: "me" (the user)
- **Due Date**: only if mentioned
- **Tags**: only if mentioned
- **Custom Fields**: only if mentioned

### Create Task

1. Identify target list from workspace structure
2. Use `clickup_create_task` with `list_id` and `name`
3. Apply defaults, optional fields only if specified
4. Provide link: `https://app.clickup.com/t/{task_id}`

### Bulk Operations

For multiple tasks in the same list:
- Use `clickup_create_bulk_tasks` (more efficient than multiple single calls)

## Additional Operations

### Contacts
- Location: Backoffice Space
- Search first with `clickup_search`

### Documents
- Location based on context:
  - Private → Privat Space
  - Project → Operations Space (specific project)
  - Templates → Process Library
  - Growth → Growth Space
  - baumeet.ing → baumeet.ing Space
- Provide document link after creation

### Time Tracking
- Start: `clickup_start_time_tracking`
- Stop: `clickup_stop_time_tracking`
- Manual: `clickup_add_time_entry`

## Core Principles

1. **Choose correct search strategy** - Context-based vs. Keyword search
2. **Speed over perfection** - Use defaults, don't ask too much
3. **Structure awareness** - Know workspace structure before action
4. **Always link** - Provide direct ClickUp links to created/modified elements
5. **Personal List for private** - ID `901208069739` for personal tasks
