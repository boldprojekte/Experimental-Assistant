#!/usr/bin/env node

/**
 * Audio/Video Transcription Script
 * Converts audio/video files to MP3 and transcribes them with Assembly.ai
 *
 * Usage:
 *   node transcribe_audio.js <folder> [bitrate]
 *
 * Example:
 *   node transcribe_audio.js ./media-files 128
 *   node transcribe_audio.js /absolute/path/to/files 192
 */

import { resolve, join, extname, basename, dirname } from 'path';
import { fileURLToPath } from 'url';
import { readdir, mkdir } from 'fs/promises';
import { existsSync } from 'fs';
import ffmpeg from 'fluent-ffmpeg';
import ffmpegInstaller from '@ffmpeg-installer/ffmpeg';
import { AssemblyAI } from 'assemblyai';
import { config } from 'dotenv';

// Get script directory for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment variables from script directory
config({ path: join(__dirname, '.env') });

// Configure ffmpeg path
ffmpeg.setFfmpegPath(ffmpegInstaller.path);

// Supported audio/video formats
const SUPPORTED_FORMATS = [
  '.mp4', '.m4a', '.mov', '.avi', '.mkv', '.flv', '.wmv',
  '.wav', '.mp3', '.flac', '.aac', '.ogg', '.wma', '.webm'
];

/**
 * Convert audio/video file to MP3
 * @param {string} inputPath - Absolute path to input file
 * @param {string} outputPath - Absolute path to output MP3 file
 * @param {number} bitrate - Audio bitrate in kbps
 * @returns {Promise<void>}
 */
function convertToMp3(inputPath, outputPath, bitrate) {
  return new Promise((resolve, reject) => {
    ffmpeg(inputPath)
      .toFormat('mp3')
      .audioBitrate(bitrate)
      .on('start', () => {
        console.log(`  Converting: ${basename(inputPath)}`);
      })
      .on('progress', (progress) => {
        if (progress.percent) {
          process.stdout.write(`\r  Progress: ${Math.round(progress.percent)}%`);
        }
      })
      .on('end', () => {
        console.log('\n  ✓ Conversion complete');
        resolve();
      })
      .on('error', (err) => {
        console.error('\n  ✗ Conversion failed:', err.message);
        reject(err);
      })
      .save(outputPath);
  });
}

/**
 * Transcribe MP3 file with Assembly.ai
 * @param {AssemblyAI} client - Assembly.ai client
 * @param {string} mp3Path - Absolute path to MP3 file
 * @returns {Promise<string>} Transcript text
 */
async function transcribeAudio(client, mp3Path) {
  console.log(`  Uploading to Assembly.ai: ${basename(mp3Path)}`);

  const transcript = await client.transcripts.transcribe({
    audio: mp3Path,
    language_detection: true,  // Automatic language detection (99 languages)
  });

  if (transcript.status === 'error') {
    throw new Error(transcript.error);
  }

  console.log('  ✓ Transcription complete');
  return transcript.text;
}

/**
 * Save transcript to text file
 * @param {string} transcriptPath - Path to save transcript
 * @param {string} text - Transcript text
 */
async function saveTranscript(transcriptPath, text) {
  const { writeFile } = await import('fs/promises');
  await writeFile(transcriptPath, text, 'utf8');
  console.log(`  ✓ Saved transcript: ${basename(transcriptPath)}`);
}

/**
 * Process a single audio/video file
 * @param {AssemblyAI} client - Assembly.ai client
 * @param {string} filePath - Path to file
 * @param {string} outputDir - Output directory for MP3 and transcript
 * @param {number} bitrate - Audio bitrate in kbps
 */
async function processFile(client, filePath, outputDir, bitrate) {
  const fileName = basename(filePath, extname(filePath));
  const mp3Path = join(outputDir, `${fileName}.mp3`);
  const transcriptPath = join(outputDir, `${fileName}.txt`);

  console.log(`\n📄 Processing: ${basename(filePath)}`);

  try {
    // Convert to MP3
    await convertToMp3(filePath, mp3Path, bitrate);

    // Transcribe
    const transcript = await transcribeAudio(client, mp3Path);

    // Save transcript
    await saveTranscript(transcriptPath, transcript);

    console.log('  ✓ Complete\n');
  } catch (error) {
    console.error(`  ✗ Failed: ${error.message}\n`);
  }
}

/**
 * Main function
 */
async function main() {
  // Parse arguments
  const args = process.argv.slice(2);

  if (args.length === 0) {
    console.error('Usage: node transcribe_audio.js <folder> [bitrate]');
    console.error('Example: node transcribe_audio.js ./media-files 128');
    process.exit(1);
  }

  const inputFolder = resolve(args[0]);
  const bitrate = args[1] ? parseInt(args[1]) : 128;

  // Validate bitrate
  if (isNaN(bitrate) || bitrate < 32 || bitrate > 320) {
    console.error('Error: Bitrate must be between 32 and 320 kbps');
    process.exit(1);
  }

  // Check if folder exists
  if (!existsSync(inputFolder)) {
    console.error(`Error: Folder not found: ${inputFolder}`);
    process.exit(1);
  }

  // Get Assembly.ai API key
  const apiKey = process.env.ASSEMBLYAI_API_KEY;
  if (!apiKey) {
    console.error('Error: ASSEMBLYAI_API_KEY environment variable not set');
    console.error('Create a .env file with: ASSEMBLYAI_API_KEY=your_key_here');
    process.exit(1);
  }

  // Initialize Assembly.ai client
  const client = new AssemblyAI({ apiKey });

  console.log('🎙️  Audio/Video Transcription Script');
  console.log('=====================================');
  console.log(`Input folder: ${inputFolder}`);
  console.log(`Audio bitrate: ${bitrate} kbps`);
  console.log('');

  // Create output folder
  const outputDir = join(inputFolder, 'transcriptions');
  if (!existsSync(outputDir)) {
    await mkdir(outputDir, { recursive: true });
    console.log(`Created output folder: ${outputDir}\n`);
  }

  // Read all files from folder
  const files = await readdir(inputFolder);
  const audioFiles = files
    .filter(file => SUPPORTED_FORMATS.includes(extname(file).toLowerCase()))
    .map(file => join(inputFolder, file));

  if (audioFiles.length === 0) {
    console.log('No audio/video files found in folder.');
    process.exit(0);
  }

  console.log(`Found ${audioFiles.length} file(s) to process\n`);

  // Process each file
  for (const filePath of audioFiles) {
    await processFile(client, filePath, outputDir, bitrate);
  }

  console.log('✅ All files processed!');
}

// Execute
main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
