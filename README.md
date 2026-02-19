# YouTube Subtitle Extractor

A Python command-line tool to automatically extract subtitles from YouTube videos.

## Features

- Extract **manual** subtitles and **auto-generated** captions
- Support for **multiple languages** (English, Chinese, Japanese, Korean, French, etc.)
- Output in **multiple formats**: plain text (`.txt`), VTT, SRT, JSON
- **Deduplication** of repeated subtitle lines (common in auto-generated captions)
- Strip HTML/VTT tags and timestamps from output

## Installation

```bash
pip install -r requirements.txt
```

Or install directly:

```bash
pip install yt-dlp
```

## Usage

```
python youtube_subtitle_extractor.py [options] <YouTube URL>
```

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--list` | `-L` | List all available subtitle languages |
| `--lang LANG` | `-l` | Language code (default: `en`) |
| `--format FORMAT` | `-f` | Output format: `txt`, `vtt`, `srt`, `json` (default: `txt`) |
| `--output DIR` | `-o` | Output directory (default: current directory) |
| `--no-auto` | | Disable auto-generated subtitle fallback |
| `--print` | | Print subtitle content to stdout |

### Examples

```bash
# List all available subtitle languages
python youtube_subtitle_extractor.py --list https://www.youtube.com/watch?v=VIDEO_ID

# Download English subtitles as plain text (default)
python youtube_subtitle_extractor.py https://www.youtube.com/watch?v=VIDEO_ID

# Download Chinese Simplified subtitles
python youtube_subtitle_extractor.py -l zh-Hans https://www.youtube.com/watch?v=VIDEO_ID

# Download as JSON format
python youtube_subtitle_extractor.py -f json https://www.youtube.com/watch?v=VIDEO_ID

# Save subtitles to a specific directory
python youtube_subtitle_extractor.py -o ./subtitles https://www.youtube.com/watch?v=VIDEO_ID

# Print subtitles directly to the terminal
python youtube_subtitle_extractor.py --print https://www.youtube.com/watch?v=VIDEO_ID

# Only use manual subtitles (no auto-generated fallback)
python youtube_subtitle_extractor.py --no-auto https://www.youtube.com/watch?v=VIDEO_ID
```

## Output Formats

| Format | Description |
|--------|-------------|
| `txt` | Plain text, one sentence per line, duplicates removed |
| `vtt` | WebVTT format with timestamps |
| `srt` | SubRip format with timestamps |
| `json` | JSON with title, language, and array of text lines |

## Common Language Codes

| Language | Code |
|----------|------|
| English | `en` |
| Chinese (Simplified) | `zh-Hans` |
| Chinese (Traditional) | `zh-Hant` |
| Japanese | `ja` |
| Korean | `ko` |
| French | `fr` |
| Spanish | `es` |
| German | `de` |
| Arabic | `ar` |

Use `--list` to see all available languages for a specific video.
