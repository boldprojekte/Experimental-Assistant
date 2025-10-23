# Audio/Video Transcription Script

Converts audio/video files to MP3 and transcribes them using Assembly.ai.

## Features

- ✅ Converts any audio/video format to MP3 (mp4, m4a, mov, wav, avi, etc.)
- ✅ Configurable audio bitrate (default: 128 kbps)
- ✅ Automatic transcription with Assembly.ai
- ✅ **Automatic language detection** (99+ languages including German, English, Spanish, etc.)
- ✅ Batch processing (processes entire folder)
- ✅ Progress tracking with visual feedback
- ✅ Cross-platform (Windows + macOS)

## Prerequisites

- Node.js 16+ (ES modules support)
- Assembly.ai API key ([Get one here](https://www.assemblyai.com/app/account))

## Installation

```bash
cd Skripte/audio-transcription/
npm install
```

## Configuration

Create a `.env` file in the script directory with your Assembly.ai API key:

```bash
cd Skripte/audio-transcription/
cp .env.example .env
```

Then edit `.env` and add your Assembly.ai API key:

```
ASSEMBLYAI_API_KEY=your_actual_api_key_here
```

**Note:** The `.env` file must be in the script directory (`Skripte/audio-transcription/`). This keeps API keys organized with their respective scripts.

## Usage

**Can be run from any directory**

### Basic Usage

```bash
node transcribe_audio.js <folder> [bitrate]
```

### Examples

**Default bitrate (128 kbps):**
```bash
# Relative path
node transcribe_audio.js ./media-files

# Absolute path
node transcribe_audio.js /Users/j.franke/Desktop/audio-recordings
```

**Custom bitrate (192 kbps):**
```bash
node transcribe_audio.js ./media-files 192
```

**From any directory:**
```bash
# Run from project root
node Skripte/audio-transcription/transcribe_audio.js /path/to/audio-files

# Run from different location
cd /tmp
node /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/audio-transcription/transcribe_audio.js /path/to/files
```

## AI Agent Examples

```bash
# Process user's current folder
cd /Users/j.franke/Desktop/Windsurf/Experimental-Assistant
node Skripte/audio-transcription/transcribe_audio.js . 128

# Process specific recordings folder
node Skripte/audio-transcription/transcribe_audio.js /Users/j.franke/Documents/Recordings 192

# High-quality transcription (256 kbps)
node Skripte/audio-transcription/transcribe_audio.js ./interviews 256
```

## Output

The script creates a `transcriptions/` subfolder in your input folder containing:

- **MP3 files**: Converted audio files (e.g., `recording.mp3`)
- **Text files**: Transcripts (e.g., `recording.txt`)

**Example:**
```
media-files/
├── interview.m4a              (original)
└── transcriptions/
    ├── interview.mp3          (converted)
    └── interview.txt          (transcript)
```

## Supported Formats

**Audio:** mp3, m4a, wav, flac, aac, ogg, wma
**Video:** mp4, mov, avi, mkv, flv, wmv, webm

## Language Detection

The script uses **automatic language detection** powered by Assembly.ai's Universal model:

- ✅ Supports **99+ languages** automatically
- ✅ No manual language selection needed
- ✅ Works for German, English, Spanish, French, Italian, and many more
- ✅ Provides confidence scores for detected language

**How it works:**
The script automatically detects the spoken language in your audio/video files. You don't need to specify the language - just run the script and it will transcribe in the correct language.

**Example:**
- German audio → German transcript
- English audio → English transcript
- Mixed languages → Detects primary language

## Customization

### Change Default Bitrate

Edit line 180 in `transcribe_audio.js`:

```javascript
const bitrate = args[1] ? parseInt(args[1]) : 128;  // Change 128 to your preferred default
```

### Supported Bitrates

- Minimum: 32 kbps (low quality, small file)
- Default: 128 kbps (good quality, reasonable size)
- High: 192 kbps (high quality)
- Maximum: 320 kbps (maximum quality, large file)

## Troubleshooting

### "ASSEMBLYAI_API_KEY not set"
Make sure you created a `.env` file in the script directory (`Skripte/audio-transcription/`) with your API key.

### "No audio/video files found"
Check that your folder contains supported file formats.

### FFmpeg Errors
The script automatically installs FFmpeg binaries. If you encounter issues, try reinstalling:
```bash
rm -rf node_modules
npm install
```

## Technical

- **Engine**: Node.js (ES modules)
- **FFmpeg**: fluent-ffmpeg + @ffmpeg-installer/ffmpeg (automatic binaries)
- **Transcription**: Assembly.ai official SDK with Universal model
- **Language Detection**: Automatic (99+ languages supported)
- **Cross-platform**: Windows + macOS (automatic FFmpeg binary selection)
- **Environment**: `.env` file in script directory
