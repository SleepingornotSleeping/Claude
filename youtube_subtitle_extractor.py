#!/usr/bin/env python3
"""
YouTube Subtitle Extractor
Extracts subtitles from YouTube videos using yt-dlp.
Supports auto-generated and manual subtitles in multiple languages.
"""

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed. Run: pip install yt-dlp", file=sys.stderr)
    sys.exit(1)


def list_subtitles(url: str) -> dict:
    """List all available subtitles for a YouTube video."""
    ydl_opts = {
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        subtitles = info.get("subtitles", {})
        auto_captions = info.get("automatic_captions", {})
        title = info.get("title", "Unknown")
        return {
            "title": title,
            "manual": subtitles,
            "auto": auto_captions,
        }


def clean_vtt_to_text(vtt_content: str) -> str:
    """Convert VTT subtitle content to plain text, removing duplicates."""
    lines = vtt_content.splitlines()
    seen = []
    result = []

    for line in lines:
        # Skip VTT header, metadata, timestamps, cue IDs, and empty lines
        if (
            line.startswith("WEBVTT")
            or line.startswith("Kind:")
            or line.startswith("Language:")
            or re.match(r"^\d{2}:\d{2}:\d{2}", line)
            or re.match(r"^\d{2}:\d{2}\.", line)
            or re.match(r"^[\d]+$", line)
            or "-->" in line
            or not line.strip()
        ):
            continue
        # Remove HTML/VTT tags like <00:00:00.000>, <c>, </c>, etc.
        clean = re.sub(r"<[^>]+>", "", line).strip()
        if clean and clean not in seen:
            seen.append(clean)
            result.append(clean)

    return "\n".join(result)


def clean_srt_to_text(srt_content: str) -> str:
    """Convert SRT subtitle content to plain text."""
    # Remove SRT index numbers
    text = re.sub(r"^\d+\s*$", "", srt_content, flags=re.MULTILINE)
    # Remove timestamps
    text = re.sub(
        r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", "", text
    )
    # Remove HTML tags
    text = re.sub(r"<[^>]+>", "", text)
    # Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def download_subtitle(
    url: str,
    lang: str = "en",
    auto: bool = True,
    fmt: str = "txt",
    output_dir: str = ".",
) -> str:
    """
    Download subtitle for a YouTube video.

    Args:
        url: YouTube video URL
        lang: Language code (e.g. 'en', 'zh-Hans', 'ja')
        auto: Whether to fall back to auto-generated subtitles
        fmt: Output format - 'txt' (plain text), 'srt', 'vtt', 'json'
        output_dir: Directory to save the output file

    Returns:
        Path to the saved subtitle file
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": auto,
            "subtitleslangs": [lang],
            "subtitlesformat": "vtt",  # always fetch vtt for reliable parsing
            "outtmpl": os.path.join(tmpdir, "%(title)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get("title", "subtitle")
            # Sanitize title for use as filename
            safe_title = re.sub(r'[\\/*?:"<>|]', "_", title)

        # Find downloaded vtt file
        vtt_files = list(Path(tmpdir).glob(f"*.{lang}.vtt"))
        if not vtt_files:
            # Try auto-caption variant like en-orig
            vtt_files = list(Path(tmpdir).glob("*.vtt"))

        if not vtt_files:
            raise FileNotFoundError(
                f"No subtitle file found for language '{lang}'. "
                "Use --list to check available languages."
            )

        vtt_content = vtt_files[0].read_text(encoding="utf-8")

        # Convert to requested format
        if fmt == "txt":
            content = clean_vtt_to_text(vtt_content)
            ext = "txt"
        elif fmt == "vtt":
            content = vtt_content
            ext = "vtt"
        elif fmt == "srt":
            # yt-dlp can write srt directly, but we convert from vtt here
            content = vtt_content  # simplified: keep as vtt internally
            ext = "srt"
        elif fmt == "json":
            lines = clean_vtt_to_text(vtt_content).splitlines()
            content = json.dumps(
                {"title": title, "language": lang, "lines": lines},
                ensure_ascii=False,
                indent=2,
            )
            ext = "json"
        else:
            content = vtt_content
            ext = "vtt"

        out_path = output_dir / f"{safe_title}.{lang}.{ext}"
        out_path.write_text(content, encoding="utf-8")
        return str(out_path)


def print_subtitle_list(info: dict) -> None:
    """Pretty-print available subtitle languages."""
    print(f"\nTitle: {info['title']}")
    print("\n=== Manual Subtitles ===")
    if info["manual"]:
        for lang, formats in info["manual"].items():
            fmts = ", ".join(f["ext"] for f in formats if "ext" in f)
            print(f"  {lang}: {fmts}")
    else:
        print("  (none)")

    print("\n=== Auto-Generated Subtitles ===")
    if info["auto"]:
        for lang in list(info["auto"].keys())[:20]:
            print(f"  {lang}")
        if len(info["auto"]) > 20:
            print(f"  ... and {len(info['auto']) - 20} more")
    else:
        print("  (none)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Extract subtitles from YouTube videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available subtitle languages
  python youtube_subtitle_extractor.py --list https://www.youtube.com/watch?v=VIDEO_ID

  # Download English subtitles as plain text (default)
  python youtube_subtitle_extractor.py https://www.youtube.com/watch?v=VIDEO_ID

  # Download Chinese subtitles
  python youtube_subtitle_extractor.py -l zh-Hans https://www.youtube.com/watch?v=VIDEO_ID

  # Download as SRT format
  python youtube_subtitle_extractor.py -f srt https://www.youtube.com/watch?v=VIDEO_ID

  # Save to specific directory
  python youtube_subtitle_extractor.py -o ./subtitles https://www.youtube.com/watch?v=VIDEO_ID

  # Only use manual subtitles (no auto-generated fallback)
  python youtube_subtitle_extractor.py --no-auto https://www.youtube.com/watch?v=VIDEO_ID
        """,
    )
    parser.add_argument("url", nargs="?", help="YouTube video URL")
    parser.add_argument(
        "--list", "-L",
        action="store_true",
        help="List available subtitle languages and exit",
    )
    parser.add_argument(
        "--lang", "-l",
        default="en",
        metavar="LANG",
        help="Subtitle language code (default: en). E.g. zh-Hans, ja, ko, fr",
    )
    parser.add_argument(
        "--format", "-f",
        dest="fmt",
        default="txt",
        choices=["txt", "vtt", "srt", "json"],
        help="Output format (default: txt)",
    )
    parser.add_argument(
        "--output", "-o",
        default=".",
        metavar="DIR",
        help="Output directory (default: current directory)",
    )
    parser.add_argument(
        "--no-auto",
        action="store_true",
        help="Disable auto-generated subtitle fallback",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print subtitle content to stdout instead of saving to file",
    )

    args = parser.parse_args()

    if not args.url:
        parser.print_help()
        sys.exit(1)

    try:
        if args.list:
            print(f"Fetching subtitle list for: {args.url}")
            info = list_subtitles(args.url)
            print_subtitle_list(info)
        else:
            print(f"Extracting '{args.lang}' subtitles from: {args.url}")
            out_path = download_subtitle(
                url=args.url,
                lang=args.lang,
                auto=not args.no_auto,
                fmt=args.fmt,
                output_dir=args.output,
            )
            if args.print:
                print(Path(out_path).read_text(encoding="utf-8"))
                # Clean up the file since we printed to stdout
                Path(out_path).unlink()
            else:
                print(f"Saved: {out_path}")

    except yt_dlp.utils.DownloadError as e:
        print(f"Download error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nAborted.", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    main()
