---
name: scripts
description: Workflow guide for creating, organizing, and running scripts. Use for script development, script execution, script organization, and maintaining the scripts directory structure. Critical for keeping scripts organized and discoverable.
---

# Scripts Workflow

Workflow guide for creating, organizing, and running utility scripts in the `Skripte/` directory.

## Core Principle

**For running scripts**: ALWAYS read INDEX.md → README.md → Execute (in that order, never skip)

## Directory Structure

**IMPORTANT**: All scripts must follow this organization:

```
Skripte/
├── INDEX.md                    # Scripts overview (update when adding new scripts)
└── script-name/                # Each script in its own folder
    ├── README.md               # Usage documentation
    ├── script-file.js/.py      # Main script
    ├── package.json            # Dependencies (if Node.js)
    ├── requirements.txt        # Dependencies (if Python)
    ├── .env.example            # Environment variable template (if needed)
    └── .env                    # Actual environment variables (git-ignored)
```

## Creating a New Script

**MANDATORY workflow** - follow ALL steps in order:

### 1. Research Phase

**ALWAYS research first before coding**:

```
1. Use WebSearch and Ref MCP (documentation scanner) to find:
   - Modern approaches for the task
   - Latest library versions and best practices
   - Cross-platform compatibility issues
   - Common pitfalls to avoid
   

2. Read official documentation:
   - Use mcp__Ref__ref_search_documentation for library docs
   - Check platform compatibility (Windows + macOS minimum)
   - Identify simplest approach that works
```

**Example**:
```
Task: "Create script to convert images to WebP"

Research:
- Search: "node.js convert images to webp 2025"
- Search: "sharp vs imagemagick webp conversion"
- Check: sharp documentation for latest API
- Verify: Cross-platform support (Windows/Mac)
```

### 2. Plan & User Approval

**BEFORE writing any code**:

1. **Present approach to user**:
   - Library/tool choice and why
   - Key features planned
   - Cross-platform compatibility plan
   - Estimated complexity

2. **Ask user for approval**:
   - Use AskUserQuestion if multiple valid approaches
   - Explain trade-offs clearly
   - Get confirmation before proceeding

**Example**:
```
"I found two approaches for image conversion:

1. **sharp** (Node.js) - Fast, cross-platform, 10MB install
2. **Pillow** (Python) - Mature, widely used, requires Python

I recommend sharp because:
- Native binaries for Windows/Mac
- Faster performance
- Simpler installation

Proceed with sharp?"
```

### 3. Implementation Phase

**Create directory**:
```bash
cd Skripte/
mkdir script-name/
cd script-name/
```

**Write script with these requirements**:

**CRITICAL - Location Independence**:
- **Use `resolve()` for all paths** - No cwd assumptions
- **Accept absolute/relative paths** - Let caller choose
- **No hardcoded paths** - Make everything configurable

**CRITICAL - Cross-Platform**:
- **Test on both Windows and macOS** if possible
- Use `path.join()` / `Path()` (not manual `/` or `\`)
- Avoid platform-specific commands
- Handle line endings correctly

**CRITICAL - Simplicity**:
- **Don't overengineer** - Solve the specific problem
- Minimal dependencies (fewer = better)
- No unnecessary abstractions
- Clear, readable code over clever code

**CRITICAL - Environment Variables & API Keys**:
- **Always load .env from script directory** - Never from cwd
- Each script keeps its own .env in its folder
- Use ES modules pattern to get script directory:
  ```javascript
  import { fileURLToPath } from 'url';
  import { dirname, join } from 'path';
  const __dirname = dirname(fileURLToPath(import.meta.url));
  config({ path: join(__dirname, '.env') });
  ```
- Include `.env.example` template in script folder
- Document required environment variables in README

**Example (Node.js)**:
```javascript
#!/usr/bin/env node
import { resolve } from 'path';

// ✅ GOOD - works anywhere, cross-platform
const inputPath = resolve(process.argv[2]);
const outputPath = process.argv[3] ? resolve(process.argv[3]) : inputPath.replace('.md', '.pdf');

// ❌ BAD - assumes cwd, platform-specific
const inputPath = './input.md';
const outputPath = '../output.pdf';
```

**Example (Python)**:
```python
#!/usr/bin/env python3
from pathlib import Path

# ✅ GOOD - works anywhere, cross-platform
input_path = Path(sys.argv[1]).resolve()
output_path = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else input_path.with_suffix('.pdf')

# ❌ BAD - assumes cwd, platform-specific
input_path = Path('./input.md')
output_path = Path('../output.pdf')
```

### 4. Testing & Debugging Phase

**BEFORE writing README or updating INDEX**:

1. **Test basic functionality**:
   ```bash
   # Test with single file
   node script_name.js /path/to/test/file.ext

   # Test with different output location
   node script_name.js /path/to/input.ext /different/output.ext

   # Test from different working directories
   cd /tmp && node /path/to/script_name.js /path/to/file.ext
   ```

2. **Debug issues**:
   - Fix errors immediately
   - Test edge cases (missing files, wrong paths, etc.)
   - Verify output is correct

3. **Cross-platform check** (if possible):
   - Verify path handling works correctly
   - Check file system operations

**Only proceed to documentation when script works correctly!**

### 5. Documentation Phase

**After script is tested and working**:

**Create README.md** (concise, 50-70 lines):

```markdown
# Script Name

Brief description (1 line).

## Prerequisites

- Runtime version
- Dependencies (if any)

## Installation

```bash
cd Skripte/script-name/
npm install  # or pip install -r requirements.txt
```

## Usage

**Can be run from any directory**

### Single File
```bash
# Basic usage
node script_name.js /path/to/file.ext

# With output
node script_name.js input.ext output.ext
```

### AI Agent Examples
```bash
# Common use cases with real project paths
```

## Customization

How to modify behavior (if applicable)

## Technical

- Engine/Framework
- Key dependencies
- Cross-platform: Windows + macOS
```

### 6. Update INDEX

**Add to `Skripte/INDEX.md`** (compact format):

```markdown
### script-name
One-line description. Use for [when to use].
**See**: `script-name/README.md`
```

## Running Scripts

### Workflow (MANDATORY ORDER)

**ALWAYS follow this exact sequence**:

1. **Read `Skripte/INDEX.md` FIRST**
   - Scan for script matching the task
   - Get script folder name
   - Never skip this step - INDEX is the source of truth

2. **Read `Skripte/{script-name}/README.md` SECOND**
   - Get usage instructions
   - Check prerequisites
   - Find relevant examples

3. **Execute THIRD**
   - Follow README instructions exactly
   - Use appropriate paths for the task

**NEVER**:
- ❌ Skip INDEX and go directly to a script
- ❌ Guess script names without checking INDEX
- ❌ Execute without reading README first

### Execution Pattern

```bash
# Navigate to script directory
cd Skripte/script-name/

# Install dependencies (first time only)
npm install  # Node.js
# OR
pip install -r requirements.txt  # Python

# Run script
node script_name.js [args]
# OR
python script_name.py [args]
```

## Best Practices

### Quality (CRITICAL)

**Always follow the 6-step creation workflow**:
1. Research → 2. Plan & User Approval → 3. Implement → 4. Test & Debug → 5. Document → 6. Update INDEX

**Never skip research, user approval, or testing!**

### Flexibility (CRITICAL)

**Scripts MUST work from any directory for AI agents**:
- ✅ Use `resolve()` / `.resolve()` for all paths
- ✅ Accept both absolute and relative paths
- ✅ No hardcoded paths or cwd assumptions
- ✅ Smart defaults (e.g., output path = input path with different extension)

### Cross-Platform (CRITICAL)

**Scripts MUST work on Windows + macOS minimum**:
- ✅ Use `path.join()` / `Path()` (not manual `/` or `\`)
- ✅ Test path handling on both platforms if possible
- ✅ Avoid platform-specific shell commands
- ✅ Handle line endings correctly (use libraries, not manual `\n` or `\r\n`)
- ✅ Check library compatibility before choosing

### Simplicity (CRITICAL)

**Keep it simple - don't overengineer**:
- ✅ Solve the specific problem (no extra features)
- ✅ Minimal dependencies (fewer is better)
- ✅ No unnecessary abstractions or patterns
- ✅ Readable code over clever code
- ✅ If it works simply, ship it

**Examples**:
- ❌ BAD: "Let's add a plugin system for future extensibility"
- ✅ GOOD: "Convert markdown to PDF. Done."

### Organization

- **One script = One folder**: Never put scripts directly in `Skripte/`
- **Self-contained**: All dependencies in script folder
- **README required**: Every script must have README.md
- **INDEX updated**: Always update INDEX.md when adding scripts

### Environment Variables (CRITICAL)

**All scripts MUST load .env from their own directory**:
- ✅ `.env` file lives in the script folder (e.g., `Skripte/audio-transcription/.env`)
- ✅ Load from script directory, NOT from current working directory
- ✅ Include `.env.example` template with placeholder values
- ✅ Document all required environment variables in README
- ❌ NEVER load from cwd - breaks when script runs from different directories

**Node.js Pattern (ES Modules)**:
```javascript
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { config } from 'dotenv';

const __dirname = dirname(fileURLToPath(import.meta.url));
config({ path: join(__dirname, '.env') });
```

**Why this matters**:
- Multiple scripts may need different API keys
- Keeps credentials organized with their scripts
- Works regardless of where script is executed from
- Easier to manage and share (via .env.example)

### Documentation

- Keep README concise (50-70 lines)
- **Specify flexibility**: "Can be run from any directory"
- **Specify cross-platform**: "Windows + macOS"
- Focus on usage examples with real project paths
- Include AI agent examples
- Show common use cases

### Naming

- **Folders**: lowercase with hyphens (`markdown-zu-pdf`)
- **Scripts**: lowercase with underscores (`markdown_zu_pdf.js`)
- **Descriptive**: Name should indicate purpose

### Dependencies

- **Research first**: Find modern, well-maintained libraries
- **Check cross-platform**: Verify Windows/Mac support
- **Local install**: Install in script folder (not globally)
- **Documented**: List in package.json/requirements.txt
- **Minimal**: Only include what's actually needed

## Common Patterns

### Node.js Script Template

```javascript
#!/usr/bin/env node

/**
 * Script Name
 * Brief description
 * 
 * Usage:
 *   node script.js [args]
 */

// Imports
import { } from 'module';

// Configuration
const CONFIG = {
  // config here
};

// Main function
async function main() {
  // implementation
}

// Execute
main();
```

### Python Script Template

```python
#!/usr/bin/env python3
"""
Script Name
Brief description

Usage:
    python script.py [args]
"""

import argparse

def main():
    """Main function"""
    # implementation
    pass

if __name__ == '__main__':
    main()
```

## Workflow Summary

**Creating (6 MANDATORY STEPS)**:
1. **Research**: WebSearch for modern approaches + library docs
2. **Plan & Approval**: Present approach to user, get confirmation
3. **Implement**: Write script (location-independent, cross-platform, simple)
4. **Test & Debug**: Verify it works before docs
5. **Document**: Create README after testing
6. **Update INDEX**: Add compact entry

**Running (STRICT ORDER)**:
1. **FIRST**: Read `Skripte/INDEX.md` → find script
2. **SECOND**: Read `Skripte/{script}/README.md` → get usage
3. **THIRD**: Execute → follow README instructions

**Never skip steps!**

**Key Principles**:
- ✅ Research before coding
- ✅ Get user approval on approach
- ✅ Test before documenting
- ✅ Cross-platform (Windows + macOS)
- ✅ Simple (no overengineering)
- ✅ Flexible (works from any directory)
