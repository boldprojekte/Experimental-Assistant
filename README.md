# Experimental Assistant

Personal AI assistant for Jan-Peter Franke, powered by Claude Code with integrated productivity tools and workflow automation.

## 🎯 Project Goal

An intelligent, skill-based assistant that:
- **Automates project management** via ClickUp
- **Coordinates communication** through Gmail and Google Calendar
- **Conducts research** on the internet and documents findings
- **Performs browser automation** for recurring web tasks
- **Provides reusable scripts** for common operations
- **Manages documents** with a review workflow

## 🏗️ Architecture

The project is built on three main components:

### 1. **Skills** (`.claude/skills/`)
Specialized workflow guides for Claude Code:
- **browser** - Browser automation with Playwright
- **calendar** - Google Calendar management (Business & Personal)
- **clickup** - ClickUp integration for project management
- **deep-research** - Multi-source internet research
- **gmail** - Email management and organization
- **scripts** - Script creation and management

### 2. **MCP Servers** (Model Context Protocol)
Integrations via MCP servers:
- **ClickUp MCP** - Direct API access to ClickUp
- **Calendar MCP** - Google Calendar API
- **Gmail MCP** - Gmail API
- **Playwright MCP** - Browser control
- **Ref MCP** - Documentation scanner

### 3. **Scripts** (`Skripte/`)
Reusable utility scripts:
- **audio-transcription** - Audio/Video → MP3 → Assembly.ai transcription
- **markdown-zu-pdf** - Markdown → PDF with GitHub styling

## 📁 Project Structure

```
.
├── .claude/                      # Claude Code configuration
│   ├── agents/                   # Subagent definitions
│   │   └── web-research-specialist.md
│   ├── skills/                   # Workflow skills
│   │   ├── browser/
│   │   ├── calendar/
│   │   ├── clickup/
│   │   ├── deep-research/
│   │   ├── gmail/
│   │   └── scripts/
│   └── settings.local.json       # MCP tool permissions
│
├── Dokumente/                    # Document management
│   ├── 01_in Arbeit/            # Active documents (AI + User)
│   ├── 02_Review/               # Ready for review after AI work
│   ├── 00_Archiv/               # Archived documents
│   └── INDEX.md                 # Document index
│
├── Aufgaben/                     # Task management
│   ├── [active-tasks].md        # Running task lists
│   └── Archiv/                  # Completed tasks
│
├── Skripte/                      # Reusable scripts
│   ├── INDEX.md                 # Script overview
│   ├── audio-transcription/     # Audio → Text
│   └── markdown-zu-pdf/         # Markdown → PDF
│
├── CLAUDE.md                     # Project instructions for Claude
└── README.md                     # This file
```

## 🚀 Setup

### Prerequisites

- **Claude Code CLI** (claude.ai/code)
- **Node.js 16+** for scripts
- **Git** for version control

### Installation

1. **Clone repository:**
   ```bash
   git clone https://github.com/boldprojekte/Experimental-Assistant.git
   cd Experimental-Assistant
   ```

2. **Configure MCP servers:**
   - MCP servers are configured in `.claude/settings.local.json`
   - API keys must be set for:
     - ClickUp (`CLICKUP_API_KEY`)
     - Google Calendar (OAuth)
     - Gmail (OAuth)
     - Assembly.ai (`ASSEMBLYAI_API_KEY` - for audio-transcription only)

3. **Install scripts:**
   ```bash
   # For each script in Skripte/
   cd Skripte/audio-transcription/
   npm install
   ```

4. **Start Claude Code:**
   ```bash
   claude-code
   ```

## 💡 Usage

### Invoking Skills

Skills are automatically loaded by Claude Code when relevant tasks are detected:

```
User: "Create a new task in ClickUp"
→ Claude automatically loads the clickup skill

User: "Research the best AI tools 2025"
→ Claude automatically loads the deep-research skill

User: "Transcribe the audio file in this folder"
→ Claude automatically loads the scripts skill
```

### Running Scripts

**Audio Transcription:**
```bash
node Skripte/audio-transcription/transcribe_audio.js /path/to/audio/files 128
```

**Markdown to PDF:**
```bash
node Skripte/markdown-zu-pdf/markdown_zu_pdf.js document.md output.pdf
```

See individual `README.md` files in each script directory for details.

### Document Workflow

1. **New documents** → `Dokumente/01_in Arbeit/`
2. **After AI processing** → `Dokumente/02_Review/`
3. **After user review** → `Dokumente/`
4. **No longer needed** → `Dokumente/00_Archiv/`

### Task Management

- Active task lists in `Aufgaben/`
- Naming convention: `YYYY-MM-DD_[Type]_[Description].md`
  - Research: `2025-10-23_Research_AI_Tools.md`
  - Tasks: `2025-10-23_Task_Update_Documentation.md`
- Completed tasks → `Aufgaben/Archiv/`

## 🔧 Features

### ClickUp Integration
- Create, update, and search tasks
- Workspace-wide search with filters
- Start/stop time tracking
- Manage documents and lists

### Calendar Integration
- Retrieve events (today, this week, next week)
- Create and delete appointments
- Conflict detection
- Business & Personal calendar support

### Gmail Integration
- Email search with advanced filters
- Read and reply to messages
- Manage labels
- Create drafts

### Browser Automation
- Website navigation
- Screenshot capture
- Form filling
- Data extraction

### Deep Research
- Multi-source internet research
- Parallel subagent coordination
- Structured documentation
- Automatic task tracking

## 🛠️ Development

### Adding New Skills

1. Create skill file: `.claude/skills/skill-name/SKILL.md`
2. Document workflow
3. Reference in `CLAUDE.md`

### Creating New Scripts

See `Skripte/scripts/SKILL.md` for the complete 6-step workflow:
1. Research
2. Plan & User Approval
3. Implement
4. Test & Debug
5. Document
6. Update INDEX

### Conventions

**Language:**
- Folders: German (`Dokumente/`, `Aufgaben/`, `Skripte/`)
- Skills & Code: English
- Documents: Language of user request

**Environment Variables:**
- `.env` files live in their respective script folder
- Loaded from script directory, not from cwd
- `.env.example` templates for new users

## 📊 Project Status

- ✅ Skill system implemented (6 skills)
- ✅ MCP servers integrated (ClickUp, Gmail, Calendar, Playwright)
- ✅ Script system with 2 utility scripts
- ✅ Document & task management workflow
- ✅ `.gitignore` for Node.js projects
- 🔄 More scripts planned

## 🤝 Contributing

This is a personal assistant project, but improvement suggestions are welcome:
1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

Private project for Jan-Peter Franke.