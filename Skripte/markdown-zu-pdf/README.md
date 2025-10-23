# Markdown to PDF Converter

Converts Markdown files to PDFs with GitHub styling.

## Prerequisites

- Node.js v14+
- Installed dependencies (run `npm install` in this directory first time)

## Installation

From project root:
```bash
cd Skripte/markdown-zu-pdf/
npm install
```

## Usage

**Can be run from any directory** - uses absolute/relative paths.

### Single File
```bash
# From script directory
cd Skripte/markdown-zu-pdf/
node markdown_zu_pdf.js ../../Dokumente/file.md

# From project root
node Skripte/markdown-zu-pdf/markdown_zu_pdf.js Dokumente/file.md

# From anywhere with absolute path
node /path/to/script/markdown_zu_pdf.js /path/to/file.md

# Specify output location
node markdown_zu_pdf.js input.md /path/to/output.pdf
```

### Batch Convert
```bash
# All .md in a directory (PDFs created in same locations)
node markdown_zu_pdf.js --dir /path/to/directory/

# Include subdirectories
node markdown_zu_pdf.js --dir /path/to/directory/ --rekursiv

# Output all PDFs to different directory
node markdown_zu_pdf.js --dir /path/to/directory/ -o /output/path/
```

### AI Agent Examples
```bash
# User: "Convert this markdown to PDF"
# Agent can run from script dir with any path:
node markdown_zu_pdf.js /full/path/to/user/file.md

# User: "Convert all docs in Dokumente/"
# From project root:
node Skripte/markdown-zu-pdf/markdown_zu_pdf.js --dir Dokumente/

# Works with relative paths too
cd Skripte/markdown-zu-pdf/
node markdown_zu_pdf.js --dir ../../Aufgaben/ --rekursiv
```

## Customization

Edit `PDF_CONFIG` object in `markdown_zu_pdf.js` to change:
- Font size (default: 11pt)
- Margins (default: 20-25mm)
- CSS styling

## Technical

- Engine: md-to-pdf (Puppeteer + Chromium)
- Format: A4, GitHub-Flavored Markdown
- Output: PDF with syntax highlighting + page numbers
