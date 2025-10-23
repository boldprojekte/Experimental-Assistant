---
name: calendar
description: Workflow guide for calendar operations. Use for retrieving appointments, creating appointments, deleting appointments, showing calendar, checking events, planning meetings, checking schedule conflicts, showing this week, today, tomorrow, next week. Critical for correct calendar selection (company calendar vs. employee calendar) and conflict avoidance.
---

# Calendar Workflow

## Two Calendars

- **Company Calendar**: Tools **without** `_personal` (kontakt@bold-projekte.com)
- **Employee Calendar**: Tools **with** `_personal` (franke@bold-projekte.com)

## Retrieving Appointments

**DEFAULT**: Always query **both** calendars unless user explicitly specifies one.

```
1. searchEvent (Company Calendar)
2. searchEvent_personal (Employee Calendar)
3. Display results separately
```

## Creating Appointments

**MANDATORY before creation:**

1. **Conflict Check**: Retrieve both calendars for the time period, report any overlaps
2. **Calendar Selection**: If not explicitly specified → ask user which calendar
3. Use correct tool version (`_personal` or without)

**Timezone Handling:**

- **Format**: `YYYY-MM-DDTHH:MM:SS` (WITHOUT timezone offset like +01:00 or +02:00)
- Google Calendar will then automatically use the calendar's timezone (Europe/Berlin)
- **Example**: `2025-10-23T18:00:00` for 6:00 PM
- **NOT**: `2025-10-23T18:00:00+01:00` (causes errors with DST/standard time)

## Core Principles

1. Check both calendars (unless explicitly stated otherwise)
2. Conflict check is mandatory before creation
3. If unclear, ask which calendar to use
