#!/usr/bin/env python3
"""
chinese_filter.py — Remove Chinese characters from HTML files

USAGE:
    python chinese_filter.py --dir /path/to/html/files [--recursive] [--force]

FEATURES:
- Removes Chinese characters from <p> tag content only
- Preserves HTML structure
- Supports recursive directory scanning
- Dry-run mode for testing

UNICODE RANGES:
- CJK Unified Ideographs: \u4e00-\u9fff
- CJK Extension A: \u3400-\u4dbf
- CJK Compatibility: \uf900-\ufaff
"""

import os
import re
import sys
import argparse
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')


# ─────────────────────────────────────────────────────────────────────────────
# FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def strip_chinese_from_html(html):
    """Strip Chinese characters from <p> tag content only, preserving HTML structure."""
    soup = BeautifulSoup(html, 'html.parser')
    
    for p in soup.find_all('p'):
        if p.string and isinstance(p.string, NavigableString) and not isinstance(p.string, Comment):
            # Direct text content
            p.string = CHINESE_RE.sub('', p.string)
        else:
            # Mixed content (tags inside <p>)
            for child in p.children:
                if isinstance(child, NavigableString) and not isinstance(child, Comment) and child.strip():
                    cleaned = CHINESE_RE.sub('', str(child))
                    child.replace_with(cleaned)
    
    return str(soup)


def count_chinese_chars(text):
    """Count Chinese characters in text."""
    matches = CHINESE_RE.findall(text)
    return sum(len(m) for m in matches)


def process_file(filepath, force=False):
    """
    Process a single HTML file.
    Returns: (success, chinese_count_before, chinese_count_after)
    """
    # Read
    with open(filepath, 'r', encoding='utf-8') as f:
        original_html = f.read()
    
    # Count Chinese before
    soup_before = BeautifulSoup(original_html, 'html.parser')
    chinese_before = sum(count_chinese_chars(p.get_text()) for p in soup_before.find_all('p'))
    
    if chinese_before == 0 and not force:
        return True, 0, 0  # No Chinese found, skip
    
    # Process
    processed_html = strip_chinese_from_html(original_html)
    
    # Count Chinese after
    soup_after = BeautifulSoup(processed_html, 'html.parser')
    chinese_after = sum(count_chinese_chars(p.get_text()) for p in soup_after.find_all('p'))
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(processed_html)
    
    return True, chinese_before, chinese_after


def scan_directory(dir_path, recursive=False):
    """Scan directory for HTML files."""
    html_files = []
    
    if recursive:
        for root, dirs, files in os.walk(dir_path):
            for f in files:
                if f.endswith('.html'):
                    html_files.append(os.path.join(root, f))
    else:
        for f in os.listdir(dir_path):
            if f.endswith('.html'):
                html_files.append(os.path.join(dir_path, f))
    
    return sorted(html_files)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Remove Chinese characters from HTML files')
    parser.add_argument('--dir', required=True, help='Directory containing HTML files')
    parser.add_argument('--recursive', action='store_true', help='Scan subdirectories')
    parser.add_argument('--force', action='store_true', help='Process all files even if no Chinese detected')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed without modifying')
    
    args = parser.parse_args()
    
    # Scan for files
    html_files = scan_directory(args.dir, args.recursive)
    
    if not html_files:
        print(f"No HTML files found in {args.dir}")
        return
    
    print(f"Found {len(html_files)} HTML files")
    
    # Process
    total_before = 0
    total_after = 0
    files_with_chinese = 0
    
    for filepath in html_files:
        if args.dry_run:
            # Just count
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            soup = BeautifulSoup(html, 'html.parser')
            count = sum(count_chinese_chars(p.get_text()) for p in soup.find_all('p'))
            if count > 0:
                print(f"  {filepath}: {count} Chinese chars")
                total_before += count
                files_with_chinese += 1
        else:
            # Process
            success, before, after = process_file(filepath, args.force)
            if before > 0:
                files_with_chinese += 1
                total_before += before
                total_after += after
                print(f"  {os.path.basename(filepath)}: {before} → {after} Chinese chars")
    
    # Summary
    print(f"\n{'=' * 50}")
    if args.dry_run:
        print(f"DRY RUN - No files modified")
    print(f"Files with Chinese: {files_with_chinese}")
    print(f"Total Chinese chars before: {total_before}")
    if not args.dry_run:
        print(f"Total Chinese chars after: {total_after}")
        print(f"Removed: {total_before - total_after}")


if __name__ == "__main__":
    main()
