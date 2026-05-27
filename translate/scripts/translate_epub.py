#!/usr/bin/env python3
"""
translate_epub.py — Thai translation of <p> tags via DeepSeek V3.1 API

USAGE:
    python translate_epub.py [--start N] [--end N]

FEATURES:
- Translates only <p> tag content, preserving HTML structure
- Resumable: progress saved to translation_progress.json
- Chinese character filter in post-processing
- Batch processing with progress tracking

NOTE: This is a TEMPLATE script. Fill in your own API credentials.
"""

import os
import json
import re
import sys
import time
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — FILL IN YOUR OWN VALUES
# ─────────────────────────────────────────────────────────────────────────────

# Working directories
WORK = "/path/to/your/project"
HTML_DIR = os.path.join(WORK, "extracted", "OEBPS")
OUT_DIR = os.path.join(WORK, "translated")
PROGRESS_FILE = os.path.join(WORK, "translation_progress.json")

# API Configuration (PLACEHOLDER — replace with your own)
API_BASE = "https://your-api-endpoint.com/v1"
API_KEY = "YOUR_API_KEY_HERE"  # ⚠️ NEVER commit real keys to version control
MODEL = "your-model-name"  # e.g., gemma4:31b-cloud, deepseek-v3.1:671b-cloud

# Regex for Chinese characters
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

# ─────────────────────────────────────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a professional Thai literary translator specializing in English-to-Thai novel translation.

Your task:
1. Translate ALL text content inside <p> tags from English to Thai completely
2. Preserve ALL HTML tags, attributes, and structure exactly as-is
3. Keep ONLY proper nouns (character names, place names, skill names) in English
4. Maintain the original paragraph breaks and formatting
5. Use natural, fluent Thai literary style
6. Do NOT add, remove, or modify any HTML tags
7. Output ONLY the translated HTML — no explanations
8. IMPORTANT: Do NOT output any Chinese characters — Thai language only"""

USER_PROMPT_TEMPLATE = """Translate the following HTML content completely to Thai. Only translate the text inside <p> tags. Keep all HTML tags unchanged.

```html
{html_content}
```"""


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def load_progress():
    """Load progress file, return dict mapping filename -> True for completed."""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress):
    """Save progress dict to disk."""
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def get_page_files(html_dir):
    """Return sorted list of page-XXXX.html filenames."""
    files = [f for f in os.listdir(html_dir)
             if f.startswith("page-") and f.endswith(".html")]
    files.sort(key=lambda x: int(x.split("-")[1].split(".")[0]))
    return files


def strip_chinese_from_html(html):
    """Strip Chinese characters from <p> tag content only, preserving HTML structure."""
    soup = BeautifulSoup(html, "html.parser")
    for p in soup.find_all("p"):
        if p.string and isinstance(p.string, NavigableString) and not isinstance(p.string, Comment):
            p.string = CHINESE_RE.sub('', p.string)
        else:
            for child in p.children:
                if isinstance(child, NavigableString) and not isinstance(child, Comment) and child.strip():
                    cleaned = CHINESE_RE.sub('', str(child))
                    child.replace_with(cleaned)
    return str(soup)


def translate_page(client, html_content, page_name, retries=3):
    """
    Translate <p> tag content in the HTML.
    Returns translated HTML string.
    """
    for attempt in range(retries):
        try:
            # NOTE: This is a template — implement your own API call
            # Example for OpenAI-compatible API:
            # response = client.chat.completions.create(
            #     model=MODEL,
            #     messages=[
            #         {"role": "system", "content": SYSTEM_PROMPT},
            #         {"role": "user", "content": USER_PROMPT_TEMPLATE.format(html_content=html_content)}
            #     ],
            #     temperature=0.3,
            #     max_tokens=8192,
            #     timeout=120,
            # )
            # translated = response.choices[0].message.content.strip()
            
            raise NotImplementedError("Implement your API call here")
            
            # Strip code fences if present
            if translated.startswith("```"):
                translated = re.sub(r'^```[a-zA-Z]*\n?', '', translated)
                translated = re.sub(r'\n?```$', '', translated)
                translated = translated.strip()

            # Strip Chinese characters
            translated = strip_chinese_from_html(translated)

            return translated

        except Exception as e:
            wait = (attempt + 1) * 10
            print(f"  [WARN] Attempt {attempt + 1}/{retries} failed for {page_name}: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(f"Failed to translate {page_name} after {retries} attempts.")


def validate_translation(original_html, translated_html, page_name):
    """Basic validation: check that HTML structure is preserved."""
    orig_soup = BeautifulSoup(original_html, "html.parser")
    trans_soup = BeautifulSoup(translated_html, "html.parser")

    orig_ps = orig_soup.find_all("p")
    trans_ps = trans_soup.find_all("p")

    if len(orig_ps) != len(trans_ps):
        print(f"  [WARN] {page_name}: <p> count mismatch: original={len(orig_ps)} vs translated={len(trans_ps)}")
        return True

    # Check for Chinese characters
    chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
    for p in trans_ps:
        text = p.get_text()
        if chinese_pattern.search(text):
            print(f"  [WARN] {page_name}: Chinese characters detected in output")
            break

    return True


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Parse CLI args
    start_page = None
    end_page = None
    for i, arg in enumerate(sys.argv[1:]):
        if arg == "--start" and i + 2 < len(sys.argv):
            start_page = int(sys.argv[i + 2])
        elif arg == "--end" and i + 2 < len(sys.argv):
            end_page = int(sys.argv[i + 2])

    # Ensure output directory
    os.makedirs(OUT_DIR, exist_ok=True)

    # Load progress
    progress = load_progress()
    if progress:
        done_count = sum(1 for v in progress.values() if v)
        print(f"Resuming: {done_count} pages already translated")

    # Get page files
    files = get_page_files(HTML_DIR)
    print(f"Total HTML files found: {len(files)}")

    # Filter by range if specified
    if start_page is not None or end_page is not None:
        filtered = []
        for f in files:
            num = int(f.split("-")[1].split(".")[0])
            if start_page is not None and num < start_page:
                continue
            if end_page is not None and num > end_page:
                continue
            filtered.append(f)
        files = filtered
        print(f"Filtered to pages {start_page or 0}-{end_page or 9999}: {len(files)} files")

    # Initialize API client (IMPLEMENT THIS)
    # from openai import OpenAI
    # client = OpenAI(api_key=API_KEY, base_url=API_BASE)
    client = None  # Placeholder

    # Process each page
    total = len(files)
    for idx, fname in enumerate(files, 1):
        page_num = fname.split("-")[1].split(".")[0]

        # Skip if already translated
        if progress.get(fname):
            out_path = os.path.join(OUT_DIR, fname)
            if os.path.exists(out_path):
                continue

        print(f"[{idx:4d}/{total}][{page_num}] Translating {fname} ...", flush=True)

        # Read original HTML
        src_path = os.path.join(HTML_DIR, fname)
        with open(src_path, "r", encoding="utf-8") as f:
            original_html = f.read()

        # Translate
        try:
            translated_html = translate_page(client, original_html, fname)
        except Exception as e:
            print(f"\n[ERROR] Failed to translate {fname}: {e}")
            print("Saving progress and exiting.")
            save_progress(progress)
            sys.exit(1)

        # Validate
        validate_translation(original_html, translated_html, fname)

        # Save translated file
        out_path = os.path.join(OUT_DIR, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(translated_html)

        # Update progress
        progress[fname] = True
        save_progress(progress)

        print(f"[{idx:4d}/{total}][{page_num}] Done ({os.path.getsize(out_path)} bytes)", flush=True)

    print(f"\nTranslation complete! {len(files)} pages processed.")
    print(f"Output: {OUT_DIR}/")


if __name__ == "__main__":
    main()
