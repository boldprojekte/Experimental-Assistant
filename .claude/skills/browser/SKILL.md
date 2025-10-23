---
name: browser
description: Workflow guide for browser automation and web interaction. Use for navigating websites, filling forms, clicking buttons, extracting information, interacting with web pages, taking screenshots, automated browsing tasks, web scraping, or any task requiring interaction with websites through Chrome browser.
---

# Browser Automation Workflow

**User can see what you see** - Browser window is visible.

## CRITICAL: Ask User Permission First

**ALWAYS ask BEFORE:**
- Login credentials, passwords, 2FA codes
- Purchases, payments, financial info
- "Buy", "Purchase", "Pay", "Confirm Order" buttons
- Terms & conditions, legal agreements
- Personal data (addresses, SSN, phone)
- Deleting/modifying user data
- Sending messages/emails

**Do NOT proceed without explicit approval!**

---

## Core Workflow: Navigate → Snapshot → Interact → Verify

```
1. browser_navigate (URL)
2. browser_snapshot (get element refs from accessibility tree)
3. browser_click/type/fill_form (use ref from snapshot)
4. browser_snapshot (verify success)
```

**NEVER interact without recent snapshot!** Refs become stale after page changes.

**Re-snapshot after:** Navigation, form submit, dynamic content, tab switch

---

## 80/20 Tools (cover 80% of tasks)

**Essential 8:**
- `browser_navigate` - Go to URL
- `browser_snapshot` - Get accessibility tree (element refs)
- `browser_click` - Click elements
- `browser_type` - Type in single field
- `browser_fill_form` - Fill multiple fields (preferred)
- `browser_select_option` - Dropdowns
- `browser_wait_for` - Wait for content/time
- `browser_handle_dialog` - Auto-detected alerts/confirms

**Use snapshot over screenshot:** Snapshot provides element refs (automation). Screenshot only for visual documentation.

---

## Common Workflows

### Login (ASK USER FIRST!)
```
1. navigate → snapshot
2. ASK: "Need to enter credentials. Confirm?"
3. fill_form → click submit
4. wait_for (success) → snapshot (verify)
```

### Form Submission (ASK if sensitive!)
```
1. navigate → snapshot
2. fill_form (all fields)
3. ASK if personal/financial data
4. click submit → wait_for → snapshot
```

### Multi-step
```
1. navigate → snapshot
2. interact → wait_for
3. snapshot (NEW REFS!) → repeat
```

**Critical:** Fresh snapshot after EVERY page change!

---

## Element Selection

**Use semantic selectors from accessibility tree:**
- ✅ Role-based: "button with name 'Login'"
- ✅ Labels: "textbox labeled 'Email'"
- ❌ Fragile: XPath, CSS selectors

**Provide clear descriptions:**
- ✅ "Submit button in registration form"
- ❌ "button"

---

## Token Management

Snapshots can consume 15,000+ tokens. Minimize:
- Only snapshot when needed (before interactions, after critical changes)
- Use `browser_wait_for` instead of repeated snapshots
- Extract data efficiently from accessibility tree

---

## Advanced (use sparingly)

- `browser_tabs` - Multi-tab operations
- `browser_file_upload` - After clicking upload (absolute paths!)
- `browser_evaluate` - JavaScript (only if native tools fail)
- `browser_console_messages` / `browser_network_requests` - Debugging

---

## Session Management

**Close only when:** All tasks done, user requests, cleanup needed
**Leave open if:** User might inspect, multi-part workflow

---

## Core Principles

1. **ASK FIRST** - Logins, purchases, sensitive data
2. **Snapshot → Interact → Verify** - Never skip
3. **Fresh refs** - Re-snapshot after page changes
4. **Semantic selectors** - Use accessibility tree roles/labels
5. **Token-aware** - Minimize unnecessary snapshots
6. **User visibility** - User watches browser
7. **Close when done** - Only when truly finished
