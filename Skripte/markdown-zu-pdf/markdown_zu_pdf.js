#!/usr/bin/env node

/**
 * Markdown zu PDF Konverter mit modernem GitHub-Styling
 * ======================================================
 *
 * Verwendung:
 *   node markdown_zu_pdf.js input.md [output.pdf]
 *   node markdown_zu_pdf.js --dir Dokumente/
 *   node markdown_zu_pdf.js --dir Dokumente/ --rekursiv
 */

import { mdToPdf } from 'md-to-pdf';
import { readdir, stat } from 'fs/promises';
import { join, dirname, basename, extname, resolve } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));

// PDF-Konfiguration mit GitHub-Styling
const PDF_CONFIG = {
  stylesheet: [
    'https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown.min.css'
  ],
  css: `
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .markdown-body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
      font-size: 11pt;
      line-height: 1.6;
      max-width: 100%;
      padding: 40px;
      box-sizing: border-box;
    }

    h1, h2, h3, h4, h5, h6 {
      font-weight: 600;
      page-break-after: avoid;
      margin-top: 24px;
      margin-bottom: 16px;
    }

    h1 {
      font-size: 2em;
      border-bottom: 1px solid #d0d7de;
      padding-bottom: 0.3em;
    }

    h2 {
      font-size: 1.5em;
      border-bottom: 1px solid #d0d7de;
      padding-bottom: 0.3em;
    }

    pre {
      background-color: #f6f8fa;
      border-radius: 6px;
      padding: 16px;
      overflow: auto;
      page-break-inside: avoid;
    }

    code {
      background-color: rgba(175,184,193,0.2);
      border-radius: 3px;
      padding: 0.2em 0.4em;
      font-family: ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace;
      font-size: 85%;
    }

    pre code {
      background-color: transparent;
      padding: 0;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    table {
      border-collapse: collapse;
      width: 100%;
      page-break-inside: avoid;
      margin: 16px 0;
    }

    table th, table td {
      border: 1px solid #d0d7de;
      padding: 6px 13px;
    }

    table th {
      background-color: #f6f8fa;
      font-weight: 600;
    }

    img {
      max-width: 100%;
      page-break-inside: avoid;
    }

    blockquote {
      border-left: 4px solid #d0d7de;
      padding-left: 16px;
      color: #57606a;
      margin: 0 0 16px 0;
    }

    ul, ol {
      padding-left: 2em;
    }

    .page-break {
      page-break-after: always;
    }

    /* Inhaltsverzeichnis Styling */
    .toc {
      background-color: #f6f8fa;
      border-radius: 6px;
      padding: 16px 24px;
      margin-bottom: 32px;
      page-break-after: avoid;
    }

    .toc h2 {
      margin-top: 0;
      border-bottom: none;
    }
  `,
  body_class: 'markdown-body',
  highlight_style: 'github',
  marked_options: {
    gfm: true,
    breaks: true
  },
  pdf_options: {
    format: 'A4',
    margin: {
      top: '25mm',
      right: '20mm',
      bottom: '25mm',
      left: '20mm'
    },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: `
      <style>
        section {
          width: 100%;
          margin: 0 auto;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          font-size: 9pt;
          color: #57606a;
          text-align: center;
          padding: 0 20mm;
        }
      </style>
      <section>
        <span class="title"></span>
      </section>
    `,
    footerTemplate: `
      <style>
        section {
          width: 100%;
          margin: 0 auto;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          font-size: 9pt;
          color: #57606a;
          text-align: center;
          padding: 0 20mm;
        }
      </style>
      <section>
        Seite <span class="pageNumber"></span> von <span class="totalPages"></span>
      </section>
    `
  }
};

/**
 * Konvertiert eine einzelne Markdown-Datei zu PDF
 */
async function convertFile(inputPath, outputPath = null) {
  try {
    const resolvedInput = resolve(inputPath);
    const resolvedOutput = outputPath ? resolve(outputPath) : resolvedInput.replace(/\.md$/, '.pdf');

    console.log(`📄 Konvertiere: ${basename(resolvedInput)}`);

    const pdf = await mdToPdf({ path: resolvedInput }, {
      ...PDF_CONFIG,
      dest: resolvedOutput
    });

    if (pdf && pdf.filename) {
      console.log(`✓ Erstellt: ${pdf.filename}`);
      return pdf.filename;
    } else {
      throw new Error('PDF-Generierung fehlgeschlagen');
    }
  } catch (error) {
    console.error(`✗ Fehler bei ${basename(inputPath)}:`);
    console.error(error);
    throw error;
  }
}

/**
 * Findet alle Markdown-Dateien in einem Verzeichnis
 */
async function findMarkdownFiles(dir, recursive = false) {
  const files = [];
  const entries = await readdir(dir, { withFileTypes: true });

  for (const entry of entries) {
    const fullPath = join(dir, entry.name);

    if (entry.isDirectory() && recursive) {
      files.push(...await findMarkdownFiles(fullPath, recursive));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      // Filtere SKILL.md, README.md und temporäre Dateien aus
      if (!['SKILL.md', 'README.md'].includes(entry.name) && !entry.name.startsWith('.temp_')) {
        files.push(fullPath);
      }
    }
  }

  return files;
}

/**
 * Konvertiert alle Markdown-Dateien in einem Verzeichnis
 */
async function convertDirectory(dir, recursive = false, outputDir = null) {
  console.log(`📁 Suche Markdown-Dateien in: ${dir}${recursive ? ' (rekursiv)' : ''}`);

  const files = await findMarkdownFiles(dir, recursive);

  if (files.length === 0) {
    console.log('Keine Markdown-Dateien gefunden.');
    return [];
  }

  console.log(`Gefunden: ${files.length} Datei(en)\n`);

  const results = [];

  for (const file of files) {
    try {
      let outputPath;
      if (outputDir) {
        outputPath = join(outputDir, basename(file).replace(/\.md$/, '.pdf'));
      } else {
        outputPath = file.replace(/\.md$/, '.pdf');
      }

      const result = await convertFile(file, outputPath);
      results.push(result);
    } catch (error) {
      // Fehler bereits in convertFile geloggt
    }
  }

  return results;
}

/**
 * Zeigt Hilfetext an
 */
function showHelp() {
  console.log(`
Markdown zu PDF Konverter mit GitHub-Styling
=============================================

Verwendung:
  node markdown_zu_pdf.js <eingabe.md> [ausgabe.pdf]
  node markdown_zu_pdf.js --dir <verzeichnis> [--rekursiv] [-o <ausgabe-verzeichnis>]
  node markdown_zu_pdf.js --help

Optionen:
  --dir <verzeichnis>        Konvertiert alle .md Dateien im Verzeichnis
  --rekursiv, -r            Unterverzeichnisse einschließen
  -o <ausgabe-verzeichnis>  Zielverzeichnis für PDFs
  --help, -h                Zeigt diese Hilfe

Beispiele:
  node markdown_zu_pdf.js dokument.md
  node markdown_zu_pdf.js dokument.md ausgabe.pdf
  node markdown_zu_pdf.js --dir Dokumente/
  node markdown_zu_pdf.js --dir Dokumente/ --rekursiv
  node markdown_zu_pdf.js --dir Dokumente/ -o PDFs/
`);
}

/**
 * Main-Funktion
 */
async function main() {
  const args = process.argv.slice(2);

  // Hilfe anzeigen
  if (args.length === 0 || args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }

  try {
    // Verzeichnis-Modus
    if (args.includes('--dir')) {
      const dirIndex = args.indexOf('--dir');
      const dir = args[dirIndex + 1];

      if (!dir) {
        console.error('✗ Fehler: --dir benötigt ein Verzeichnis');
        process.exit(1);
      }

      const recursive = args.includes('--rekursiv') || args.includes('-r');

      let outputDir = null;
      if (args.includes('-o')) {
        const outIndex = args.indexOf('-o');
        outputDir = args[outIndex + 1];
      }

      const results = await convertDirectory(dir, recursive, outputDir);
      console.log(`\n✓ ${results.length} PDF(s) erfolgreich erstellt!`);

    } else {
      // Einzeldatei-Modus
      const input = args[0];
      const output = args[1] || null;

      await convertFile(input, output);
      console.log('\n✓ PDF erfolgreich erstellt!');
    }

  } catch (error) {
    console.error(`\n✗ Fehler: ${error.message}`);
    process.exit(1);
  }
}

// Skript ausführen
main();
