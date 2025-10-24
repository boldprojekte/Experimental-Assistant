#!/usr/bin/env python3
"""
Universal Video Downloader
Downloads videos from YouTube, Vimeo, Loom, and 1000+ sites to MP4 format using yt-dlp

Usage:
    python video_download.py <video_url> [output_dir] [--quality=<quality>] [--referer=<url>]
"""

import sys
import subprocess
from pathlib import Path
import argparse

# Quality presets
QUALITY_PRESETS = {
    'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    '2160p': 'bestvideo[height<=2160][ext=mp4]+bestaudio[ext=m4a]/best[height<=2160][ext=mp4]/best',
    '1440p': 'bestvideo[height<=1440][ext=mp4]+bestaudio[ext=m4a]/best[height<=1440][ext=mp4]/best',
    '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best',
    '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best',
    '480p': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best',
    '360p': 'bestvideo[height<=360][ext=mp4]+bestaudio[ext=m4a]/best[height<=360][ext=mp4]/best',
}

def download_video(url, output_dir=None, quality='best', referer=None):
    """Download video using yt-dlp"""

    # Resolve output directory (default: current working directory)
    if output_dir:
        output_path = Path(output_dir).resolve()
    else:
        output_path = Path.cwd()

    # Ensure output directory exists
    output_path.mkdir(parents=True, exist_ok=True)

    # Get format string for quality
    format_string = QUALITY_PRESETS.get(quality, QUALITY_PRESETS['best'])

    # Build yt-dlp command
    cmd = [
        'yt-dlp',
        '--format', format_string,
        '--merge-output-format', 'mp4',
        '--output', str(output_path / '%(title)s.%(ext)s'),
        url
    ]

    # Add referer if provided (for embedded videos)
    if referer:
        cmd.extend(['--referer', referer])

    print(f"Downloading video to: {output_path}")
    print(f"Quality: {quality}")
    if referer:
        print(f"Using referer: {referer}")

    try:
        # Run yt-dlp
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print("\n✓ Download completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error downloading video:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("✗ Error: yt-dlp not found. Please install it first:")
        print("  pip install yt-dlp")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Download videos from YouTube, Vimeo, Loom, and 1000+ sites to MP4 format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quality Options:
  best    - Best available quality (default)
  2160p   - 4K quality (3840x2160)
  1440p   - 2K quality (2560x1440)
  1080p   - Full HD (1920x1080)
  720p    - HD (1280x720)
  480p    - SD (854x480)
  360p    - Low quality (640x360)

Supported Sites:
  YouTube, Vimeo, Loom, TikTok, Twitter, Instagram, Facebook, and 1000+ more
  Full list: yt-dlp --list-extractors

Examples:
  # Download Loom video in best quality
  python video_download.py https://www.loom.com/share/xxxxx

  # Download YouTube video in 1080p
  python video_download.py https://www.youtube.com/watch?v=xxxxx --quality=1080p

  # Download to specific directory with 720p quality
  python video_download.py https://vimeo.com/123456789 /path/to/output --quality=720p

  # Download embedded video with referer
  python video_download.py https://vimeo.com/123456789 --referer=https://example.com/page
        """
    )

    parser.add_argument('url', help='Video URL from supported platform')
    parser.add_argument('output_dir', nargs='?', help='Output directory (default: current directory)')
    parser.add_argument('--quality', '-q',
                        choices=list(QUALITY_PRESETS.keys()),
                        default='best',
                        help='Video quality (default: best)')
    parser.add_argument('--referer', help='Referer URL for embedded videos')

    args = parser.parse_args()

    # Download video
    success = download_video(args.url, args.output_dir, args.quality, args.referer)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
