#!/usr/bin/env python3
"""
polish_gaofei.py — Polish Thai-translated text in Gao Fei style

USAGE:
    # Single process:
    python polish_gaofei.py [--start N] [--end N]

    # Parallel (e.g. 4 workers):
    python polish_gaofei.py --worker 0 --total-workers 4
    python polish_gaofei.py --worker 1 --total-workers 4
    ...

FEATURES:
- Polishes only <p> tag content, preserving HTML structure
- Resumable: progress saved to gaofei_progress.json
- Chinese character filter in post-processing
- Batch processing with progress tracking

NOTE: This is a TEMPLATE script. Fill in your own API credentials.
"""

import os
import json
import re
import sys
import time
import math
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION — FILL IN YOUR OWN VALUES
# ─────────────────────────────────────────────────────────────────────────────

WORK = "/path/to/your/project"
IN_DIR = os.path.join(WORK, "translated")
OUT_DIR = os.path.join(WORK, "polished")
BATCH_SIZE = 1  # Single page per API call for reliability

# API Configuration (PLACEHOLDER)
API_BASE = "https://your-api-endpoint.com/v1"
API_KEY = "YOUR_API_KEY_HERE"
MODEL = "deepseek-v3.1:671b-cloud"

# Regex for Chinese characters
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

# ─────────────────────────────────────────────────────────────────────────────
# PROMPTS
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a Thai literary novel polisher specializing in the "Gao Fei" style.

Gao Fei style characteristics:
- Sharp, witty, and engaging narrative voice
- Natural conversational flow with occasional snarky internal monologue
- Descriptive yet punchy prose — not overly flowery
- Strong character voice in dialogue (distinct personalities)
- Smooth pacing with good rhythm (mix of short and long sentences)
- Maintains the essence and plot of the original, only elevating the prose
- Uses vivid but not excessive imagery
- Keeps the genre feel — fantasy/vampire/system novel tone

Your task:
1. Polish ONLY the text inside <p> tags from the Thai translation
2. Preserve ALL HTML tags, attributes, and structure exactly as-is
3. Keep all proper nouns, character names, system messages unchanged
4. DO NOT change the meaning or plot — only improve the reading experience
5. Use natural Thai that flows well when read aloud
6. Do NOT add any Chinese characters to the output
7. Output ONLY the polished HTML — no explanations, no notes"""

BATCH_PROMPT_TEMPLATE = """Below are {count} HTML file(s) that contain Thai translations of a fantasy/vampire/web novel. Polish each file's <p> tag content in Gao Fei style.

IMPORTANT: Preserve ALL HTML tags and structure. Only modify the Thai text inside <p> tags.

Return your response in the following format — for each file, output a section like:

=== FILE: filename.html ===
[polished HTML content]
=== END: filename.html ===

--- Files to polish ---

{batched_content}

Remember:
- Only polish text inside <p> tags
- Keep all HTML structure intact
- No Chinese characters
- No explanations, just the formatted output"""


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def load_progress(progress_file):
    """Load progress file, return dict mapping filename -> True if completed."""
    if os.path.exists(progress_file):
        with open(progress_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress, progress_file):
    """Save progress dict to disk."""
    with open(progress_file, "w", encoding="utf-8") as f:
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


def parse_batch_response(response_text, filenames):
    """
    Parse the model's response into a dict of {filename: polished_html}.
    Expected format: === FILE: name.html === ... === END: name.html ===
    """
    results = {}
    current_file = None
    current_content = []
    in_content = False

    for line in response_text.split('\n'):
        file_match = re.match(r'=== FILE:\s*(.+?) ===', line)
        end_match = re.match(r'=== END:\s*(.+?) ===', line)

        if file_match:
            if current_file and current_content:
                results[current_file] = '\n'.join(current_content).strip()
            current_file = file_match.group(1).strip()
            current_content = []
            in_content = True
        elif end_match:
            if current_file and current_content:
                results[current_file] = '\n'.join(current_content).strip()
            current_file = None
            current_content = []
            in_content = False
        elif in_content:
            current_content.append(line)

    if current_file and current_content:
        results[current_file] = '\n'.join(current_content).strip()

    return results


def polish_batch(client, batch_files, batch_htmls):
    """
    Polish a batch of HTML files together.
    Returns dict of {filename: polished_html}.
    """
    # Prepare batched content
    batched_parts = []
    for fname, html in zip(batch_files, batch_htmls):
        batched_parts.append(f"=== FILE: {fname} ===\n{html}\n=== END: {fname} ===")

    batched_content = "\n\n".join(batched_parts)
    prompt = BATCH_PROMPT_TEMPLATE.format(
        count=len(batch_files),
        batched_content=batched_content
    )

    for attempt in range(3):
        try:
            # NOTE: Implement your own API call here
            # response = client.chat.completions.create(
            #     model=MODEL,
            #     messages=[
            #         {"role": "system", "content": SYSTEM_PROMPT},
            #         {"role": "user", "content": prompt}
            #     ],
            #     temperature=0.4,
            #     max_tokens=32768,
            #     timeout=600,
            # )
            # result = response.choices[0].message.content.strip()
            # parsed = parse_batch_response(result, batch_files)
            
            raise NotImplementedError("Implement your API call here")
            
            return parsed

        except Exception as e:
            wait = (attempt + 1) * 15
            print(f"  [WARN] Batch attempt {attempt + 1}/3 failed: {e}. Retrying in {wait}s...")
            time.sleep(wait)

    raise RuntimeError(f"Failed to polish batch after 3 attempts: {batch_files}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Parse CLI args
    start_page = None
    end_page = None
    worker_id = None
    total_workers = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--start" and i + 1 < len(sys.argv):
            start_page = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--end" and i + 1 < len(sys.argv):
            end_page = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--worker" and i + 1 < len(sys.argv):
            worker_id = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--total-workers" and i + 1 < len(sys.argv):
            total_workers = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1

    # Determine progress file
    if worker_id is not None:
        suffix = f"_{worker_id}"
        progress_file = os.path.join(WORK, f"gaofei_progress{suffix}.json")
        print(f"[Worker {worker_id}] Parallel mode enabled ({total_workers or '?'} workers total)")
    else:
        suffix = ""
        progress_file = os.path.join(WORK, "gaofei_progress.json")

    # Ensure output directory
    os.makedirs(OUT_DIR, exist_ok=True)

    # Load progress
    progress = load_progress(progress_file)
    if progress:
        done_count = sum(1 for v in progress.values() if v)
        print(f"Resuming: {done_count} pages already polished")

    # Get translated page files
    files = get_page_files(IN_DIR)
    print(f"Total translated HTML files found: {len(files)}")

    if not files:
        print(f"No files found in {IN_DIR}. Run translation first.")
        sys.exit(1)

    # Filter by range
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

    # If in parallel mode, split the range
    if worker_id is not None and total_workers is not None and total_workers > 1:
        chunk_size = math.ceil(len(files) / total_workers)
        start_idx = worker_id * chunk_size
        end_idx = min(start_idx + chunk_size, len(files))
        files = files[start_idx:end_idx]
        print(f"[Worker {worker_id}] Assigned pages {start_idx}-{end_idx-1} ({len(files)} files)")

    # Initialize client (IMPLEMENT THIS)
    # from openai import OpenAI
    # client = OpenAI(api_key=API_KEY, base_url=API_BASE)
    client = None  # Placeholder

    # Process in batches
    total = len(files)
    for i in range(0, len(files), BATCH_SIZE):
        batch = files[i:i + BATCH_SIZE]

        # Check which files are already done
        pending = []
        for fname in batch:
            out_path = os.path.join(OUT_DIR, fname)
            if progress.get(fname) and os.path.exists(out_path):
                continue
            pending.append(fname)

        if not pending:
            continue

        # Read pending HTML files
        htmls = []
        for fname in pending:
            src_path = os.path.join(IN_DIR, fname)
            with open(src_path, "r", encoding="utf-8") as f:
                htmls.append(f.read())

        # Polish the batch
        try:
            results = polish_batch(client, pending, htmls)
        except Exception as e:
            print(f"\n[ERROR] Failed batch {pending}: {e}")
            print("Saving progress and exiting.")
            save_progress(progress, progress_file)
            sys.exit(1)

        # Save results
        for fname in pending:
            if fname in results:
                polished_html = results[fname]

                # Post-process: strip Chinese characters
                polished_html = strip_chinese_from_html(polished_html)

                # Save
                out_path = os.path.join(OUT_DIR, fname)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(polished_html)

                progress[fname] = True
            else:
                print(f"  [WARN] {fname}: No result in batch response")
                progress[fname] = False

        save_progress(progress, progress_file)

        print(f"[{len(pending)} pages] Done", flush=True)

    # Final summary
    done = sum(1 for v in progress.values() if v)
    failed = sum(1 for v in progress.values() if not v)
    print(f"\nPolish complete! Done: {done}, Failed: {failed}")
    print(f"Output: {OUT_DIR}/")


if __name__ == "__main__":
    main()
