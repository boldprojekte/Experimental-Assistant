# Video Downloader

Universal video downloader supporting YouTube, Vimeo, Loom, and 1000+ platforms with quality control.

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

```bash
cd Skripte/video-download/
pip install -r requirements.txt
```

## Usage

**Can be run from any directory**

### Basic Usage

```bash
# Download video in best quality (default)
python3 video_download.py <video_url>

# Download with specific quality
python3 video_download.py <video_url> --quality=720p

# Download to specific directory
python3 video_download.py <video_url> /path/to/output

# Download with quality and output directory
python3 video_download.py <video_url> /path/to/output --quality=1080p
```

### Quality Options

- `best` - Best available quality (default)
- `2160p` - 4K quality (3840x2160)
- `1440p` - 2K quality (2560x1440)
- `1080p` - Full HD (1920x1080)
- `720p` - HD (1280x720)
- `480p` - SD (854x480)
- `360p` - Low quality (640x360)

### Recommended Storage Location

**Convention**: Videos should be saved to the dedicated videos directory:

```
/Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Dokumente/04_Videos
```

This keeps all downloaded videos organized in one central location. The script will create this directory if it doesn't exist.

### AI Agent Examples

```bash
# Download Loom video to recommended Videos folder
python3 /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/video-download/video_download.py \
  "https://www.loom.com/share/xxxxx" \
  /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Dokumente/04_Videos

# Download YouTube video in 1080p to Videos folder
python3 /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/video-download/video_download.py \
  "https://www.youtube.com/watch?v=xxxxx" \
  /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Dokumente/04_Videos \
  --quality=1080p

# Download Vimeo video in 720p to Videos folder
python3 /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/video-download/video_download.py \
  "https://vimeo.com/123456789" \
  /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Dokumente/04_Videos \
  --quality=720p

# Download embedded video with referer
python3 /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Skripte/video-download/video_download.py \
  "https://vimeo.com/123456789" \
  /Users/j.franke/Desktop/Windsurf/Experimental-Assistant/Dokumente/04_Videos \
  --referer="https://example.com/page"
```

## Supported Platforms

YouTube, Vimeo, Loom, TikTok, Twitter, Instagram, Facebook, Dailymotion, and 1000+ more.

**Full list**: Run `yt-dlp --list-extractors`

## Customization

- **Output filename**: Automatically uses video title
- **Format**: Always MP4 (with audio merged)
- **Quality fallback**: If requested quality unavailable, downloads best available
- **Referer support**: Use `--referer` for embedded videos requiring referrer headers

## Technical

- **Engine**: yt-dlp (Python)
- **Format**: MP4 with best available codec
- **Audio**: Merged automatically using FFmpeg
- **Cross-platform**: Windows + macOS + Linux
