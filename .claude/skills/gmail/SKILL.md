---
name: Gmail
description: Workflow guide for Gmail operations. Use for searching emails, reading messages, sending replies, managing labels, creating drafts, organizing inbox, marking as read/unread. Critical for correct search strategy and professional email composition.
---

# Gmail Workflow

Workflow guide for Gmail operations with focus on search strategy, email composition, and workflow orchestration.

## Search Strategy

**IMPORTANT**: Choose the correct search approach based on the request.

### Gmail Query Syntax

Use these query patterns for precise searches:
- Find by sender: `from:example@gmail.com`
- Find by subject: `subject:invoice`
- Find unread: `is:unread`
- Find with attachment: `has:attachment`
- Find by date: `after:2025/01/01 before:2025/12/31`
- Combine: `from:john@example.com has:attachment is:unread`

### When to Use Threads vs Messages

- **`getManyThreads`** → Full conversation context needed
- **`search`** → Individual emails sufficient

### Date Format

Use RFC3339 format for date filters:
- Format: `YYYY-MM-DDTHH:MM:SSZ`
- Example: `2025-10-23T00:00:00Z` (UTC)
- Quick reference: Today = current date at 00:00:00

## Email Composition Standards

**CRITICAL**: All emails must be professionally formatted with HTML and signed as "Jan-Peter Franke."

### Base HTML Style

All text must use:
```
font-family: Arial, sans-serif;
font-size: 16px;
color: #333333;
line-height: 1.6;
```

### HTML Structure Elements

- **Paragraphs**: `<p style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; line-height: 1.6; margin-bottom: 16px;">`
- **Bold**: `<strong>Important Text</strong>`
- **Lists**: `<ul style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; margin-bottom: 16px; padding-left: 20px;">`
- **Numbered**: `<ol style="font-family: Arial, sans-serif; font-size: 16px; color: #333333; margin-bottom: 16px; padding-left: 20px;">`

### Email Structure Guidelines

**Subject Line:**
- Concise, informative (German by default unless query language differs)
- Reflect core purpose and relevant project

**Opening:**
- Start directly with topic after greeting
- NO introductory pleasantries unless explicitly requested

**Tone Adaptation:**
- Professional-formal ("Sie"-form): Default
- Professional-friendly ("Sie"-form): If specified
- Collegial ("Du"-form): If specified
- Adapt based on user input for each email

**Content Structure:**
- Use `<strong>` for key terms, names, dates
- Use `<ul>` for benefits, requirements, unordered items
- Use `<ol>` for sequential steps, processes
- Break long paragraphs into digestible sections

**Closing:**
- "Sie"-form: "Mit freundlichen Grüßen"
- "Du"-form: "Viele Grüße" or "Beste Grüße"
- Always end with: `<p style="...">Closing<br>Jan-Peter Franke</p>`

## Contact Lookup

**IMPORTANT**: All contacts are stored in ClickUp Backoffice Space.

**Special exception**: For contact lookup, you may use ClickUp MCP directly without loading the skill.

**Auto-lookup when creating emails/drafts:**
When a name is mentioned for email recipient:
1. Use `mcp__clickup__clickup_search` with name (searches Backoffice Space)
2. **No results** → Use placeholder `[E-Mail-Adresse einfügen]`
3. **One contact found** → Extract and use email directly
4. **Multiple contacts** → Ask user which one to use

**Manual lookup workflow:**
- User: "Send email to supplier XYZ"
- Action: `clickup_search` for "XYZ" → Find contact in Backoffice → Extract email → Create draft

## Common Workflows

### Workflow 1: Find and Reply

1. Search with `search` (use date range, sender, query syntax)
2. Get message with `get` (simplified view unless attachments needed)
3. Read context thoroughly
4. Draft reply with proper HTML formatting
5. Use `reply` (for message) or `replyThread` (for conversation)
6. Mark as read with `markAsRead`

### Workflow 2: Create Professional Email

1. Determine tone (Sie/Du-form) from context
2. Structure content logically (greeting → topic → details → closing)
3. Apply HTML formatting with inline styles
4. Use `createDraft` with formatted HTML
5. Provide draft ID and instructions for user

### Workflow 3: Organize with Labels

1. Search unread: `search` with query `is:unread`
2. Get labels with `getLabels` (check existing)
3. Add labels with `addLabels` (use names, not IDs)
4. Archive if needed (remove INBOX label)

### Workflow 4: Inbox Triage

1. Search with date filters and status (`is:unread`)
2. Process each message: read → label → reply or archive
3. Mark as read after processing
4. Delete sparingly (prefer archiving)

## Core Principles

1. **Search before action** - Always find correct IDs first
2. **Context first** - Read messages before replying
3. **Professional formatting** - Always use HTML standards for emails
4. **Tone awareness** - Adapt Sie/Du-form appropriately
5. **Efficient queries** - Use Gmail query syntax for precision
6. **Simplified by default** - Use simplified view unless full content needed
7. **Thread awareness** - Choose threads vs messages based on context
8. **User confirmation** - Confirm before sending, deleting, or major changes
9. **Screenshot deletion** - Ask the user if he is happy with the result and if you can delete screenshots after finishing. Screenshots are here: ".playwright-mcp"
