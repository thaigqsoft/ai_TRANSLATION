# Complete Translation Workflow

**Purpose:** Step-by-step guide for translating English web novels to Thai.

---

## 📋 Prerequisites

### Required Tools

```bash
# Python packages
pip install openai beautifulsoup4 lxml tqdm

# System tools
# - unzip (for EPUB extraction)
# - zip (for EPUB rebuild)
# - grep (for QC checks)
```

### API Access

- **Model:** DeepSeek V3.1 (671B parameters)
- **Endpoint:** OpenAI-compatible API
- **Capabilities:** Thai translation, literary polishing

---

## 🔄 Full Workflow

### Step 1: Download Source Material

**Source:** EPUB file from provider (9kafe.com, thebullyproject.com, etc.)

```bash
# Place EPUB in working directory
cp /path/to/novel.epub /workspace/project/
```

---

### Step 2: Extract EPUB

```bash
cd /workspace/project/
mkdir extracted/
unzip -o novel.epub -d extracted/

# Verify structure
ls extracted/OEBPS/page-*.html
# Expected: page-0001.html, page-0002.html, ...
```

**Expected Output:**
```
extracted/
├── META-INF/
│   └── container.xml
├── OEBPS/
│   ├── page-0001.html
│   ├── page-0002.html
│   ├── ...
│   ├── book.opf
│   └── style.css
└── mimetype
```

---

### Step 3: Translate (English → Thai)

**Script:** `translate_epub.py`

```bash
cd /workspace/project/
python translate_epub.py
```

**With range:**
```bash
python translate_epub.py --start 10 --end 50
```

**What it does:**
1. Reads `OEBPS/page-*.html` files
2. Sends `<p>` tag content to translation API
3. Saves translated files to `translated/` directory
4. Tracks progress in `translation_progress.json`

**Progress file format:**
```json
{
  "page-0001.html": true,
  "page-0002.html": true,
  "page-0003.html": false
}
```

**Expected output:**
```
[1/804][001] Translating page-0001.html ...
[1/804][001] Done (4523 bytes)
[2/804][002] Translating page-0002.html ...
```

---

### Step 4: QC1 — Post-Translation Check

**Goal:** Catch Chinese character leaks and remaining English

```bash
cd /workspace/project/translated/

# Check 1: Chinese characters (CRITICAL)
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' OEBPS/ | head -30

# Check 2: Remaining English (3+ characters)
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' OEBPS/ | head -30

# Check 3: File count match
ls OEBPS/page-*.html | wc -l
# Should match source file count
```

**Pass criteria:**
- Chinese: < 5 files affected
- English: Only proper nouns (character names, places)
- File count: Matches source

**If Chinese found:**
```bash
# Run Chinese filter on affected files
python /path/to/validation/chinese_filter.py --dir OEBPS/
```

---

### Step 5: Polish (Gao Fei Style)

**Script:** `polish_gaofei.py`

```bash
cd /workspace/project/
python polish_gaofei.py
```

**Parallel mode (faster):**
```bash
# Launch 4 workers
python polish_gaofei.py --worker 0 --total-workers 4 &
python polish_gaofei.py --worker 1 --total-workers 4 &
python polish_gaofei.py --worker 2 --total-workers 4 &
python polish_gaofei.py --worker 3 --total-workers 4 &
wait
```

**What it does:**
1. Reads `translated/page-*.html` files
2. Sends Thai text for Gao Fei style polishing
3. Applies Chinese character filter automatically
4. Saves to `polished/` directory
5. Tracks progress in `gaofei_progress.json`

**Performance:**
- Batch size: 10 pages per request
- Speed: ~4-5 minutes per batch
- Full 800 pages: ~5-6 hours (single worker)
- Full 800 pages: ~1.5 hours (4 workers)

---

### Step 6: QC2 — Post-Polish Check

**Goal:** CRITICAL — DeepSeek V3.1 leaks Chinese during polish

```bash
cd /workspace/project/polished/

# Check 1: Chinese characters (ZERO tolerance)
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' OEBPS/

# Check 2: Remaining English
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' OEBPS/ | head -30
```

**If Chinese found:**
```bash
# Must clean immediately
python /path/to/validation/chinese_filter.py --dir OEBPS/ --recursive
```

---

### Step 7: English Sweep

**Script:** `thai_only_fixer.py`

**Purpose:** Regex-based dictionary cleanup for remaining English

```bash
cd /workspace/project/
python thai_only_fixer.py
```

**How it works:**
1. Loads ~1200-term dictionary
2. Scans `<p>`, `<h2>`, `<title>` tags only
3. Replaces English words with Thai equivalents
4. Preserves proper nouns

**Dictionary categories:**
| Category | Count | Examples |
|----------|-------|----------|
| Multi-word phrases | ~30 | "Spirit Bristle", "Absolute Finger" |
| Cultivation realms | ~100 | "Qi Condensation", "Divine Realm" |
| Common words | ~500 | "the", "and", "become", "suddenly" |
| Connectors | ~30 | "although", "however", "therefore" |
| Pronouns | ~30 | "I", "you", "he", "she", "they" |

**Output:**
```
English Sweep Complete!
Files processed: 804
Replacements made: 12453
Output: polished_clean/
```

---

### Step 8: QC3 — Final Language Check

```bash
cd /workspace/project/polished_clean/OEBPS/

# Check for remaining English (proper nouns only should remain)
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' page-*.html | grep -vP '(Feng|Ruoqing|Yuan|Atlas|Studios)' | head -30

# Random sampling (check 10 pages manually)
for i in 001 100 200 300 400 500 600 700 800; do
    echo "=== Page $i ==="
    grep -oP '<p>.*?</p>' page-$i.html | head -3
done
```

**Pass criteria:**
- Only proper nouns remain in English
- < 5 English words per page (non-proper-noun)

---

### Step 9: Inject CSS (iPhone 16 Pro Optimization)

**Target device:** iPhone 16 Pro (2450px height)

**CSS to inject:**
```css
body {
    font-family: "Sukhumvit Set", "Thonburi", sans-serif;
    line-height: 2;
    text-align: justify;
    margin: 1em;
}
p {
    text-indent: 2em;
    margin: 0.5em 0;
}
h1, h2, h3 {
    text-align: center;
    margin: 1em 0;
}
```

**Implementation:**
```python
# Using BeautifulSoup
from bs4 import BeautifulSoup

def inject_css(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Create style tag
    style = soup.new_tag('style')
    style.string = CSS_CONTENT
    
    # Find or create head
    if soup.head:
        soup.head.append(style)
    else:
        head = soup.new_tag('head')
        head.append(style)
        if soup.html:
            soup.html.insert(0, head)
    
    return str(soup)
```

---

### Step 10: Rebuild EPUB

**CRITICAL:** Order matters! `mimetype` must be first and uncompressed.

```bash
cd /workspace/project/polished_clean/

# Create new EPUB
# Step 1: mimetype (NO compression, -0 flag)
zip -X0 ../final_novel.epub mimetype

# Step 2: META-INF
zip -X9 ../final_novel.epub META-INF/container.xml

# Step 3: All other files (compressed)
zip -X9 ../final_novel.epub book.opf toc.ncx OEBPS/style.css OEBPS/cover-image.jpg OEBPS/*.html
```

**Verification:**
```bash
# Check file order
unzip -l ../final_novel.epub | head -20

# Verify mimetype is first and uncompressed
python3 -c "
import zipfile
with zipfile.ZipFile('../final_novel.epub') as z:
    print('First file:', z.namelist()[0])
    print('mimetype compression:', z.getinfo('mimetype').compress_type)
    # 0 = stored (no compression), 8 = deflated
"
```

---

### Step 11: QC4 — Final EPUB Validation

```bash
# Check 1: Structure validation
unzip -l final_novel.epub | head -20
# Must have: mimetype, META-INF/container.xml, book.opf, OEBPS/*

# Check 2: mimetype verification
python3 -c "
import zipfile
with zipfile.ZipFile('final_novel.epub') as z:
    assert z.namelist()[0] == 'mimetype', 'mimetype must be first'
    assert z.getinfo('mimetype').compress_type == 0, 'mimetype must be uncompressed'
print('✓ EPUB structure valid')
"

# Check 3: Open in Apple Books (manual visual check)
open -a "Books" "final_novel.epub"

# Check 4: File size
ls -lh final_novel.epub
# Typical: 2-5 MB for 800 pages
```

---

### Step 12: Deliver

**Telegram notification:**
```bash
TOKEN="YOUR_BOT_TOKEN"
CHAT_ID="YOUR_CHAT_ID"
FILE="/workspace/project/final_novel.epub"

curl -s -X POST "https://api.telegram.org/bot${TOKEN}/sendDocument" \
  -F chat_id="${CHAT_ID}" \
  -F document=@"${FILE}" \
  -F caption="✅ Translation Complete!

📖 Novel Title
📄 Pages: 804
📦 Size: $(ls -lh ${FILE} | awk '{print $5}')
⏱️  Time: ~8 hours
"
```

---

## 📊 Timeline Estimates

| Phase | 800 pages (single) | 800 pages (4 workers) |
|-------|-------------------|----------------------|
| Extract | 1 min | 1 min |
| Translate | 3-4 hours | 3-4 hours |
| QC1 | 5 min | 5 min |
| Polish | 5-6 hours | 1.5 hours |
| QC2 | 5 min | 5 min |
| English Sweep | 3 min | 3 min |
| QC3 | 10 min | 10 min |
| CSS + Rebuild | 5 min | 5 min |
| QC4 | 5 min | 5 min |
| **Total** | **~9-11 hours** | **~5-7 hours** |

---

## 🐛 Troubleshooting

### Issue: Chinese characters in output

**Solution:**
```bash
python validation/chinese_filter.py --dir polished/ --force
```

### Issue: API timeout

**Solution:**
- Reduce batch size from 10 to 5
- Increase timeout from 120s to 300s
- Add retry logic with exponential backoff

### Issue: EPUB won't open in Books

**Solution:**
```bash
# Check mimetype is first
unzip -l novel.epub | head -5

# Rebuild with correct order
zip -X0 novel.epub mimetype
zip -X9 novel.epub -r META-INF OEBPS
```

### Issue: Translation stuck/resume

**Solution:**
```bash
# Progress file exists — script will auto-resume
python translate_epub.py

# Force restart from page N
python translate_epub.py --start 100
```

---

## ✅ Completion Checklist

- [ ] Source EPUB extracted
- [ ] All pages translated to Thai
- [ ] QC1 passed (Chinese < 5 files)
- [ ] All pages polished (Gao Fei style)
- [ ] QC2 passed (ZERO Chinese)
- [ ] English sweep complete
- [ ] QC3 passed (proper nouns only)
- [ ] CSS injected for iPhone
- [ ] EPUB rebuilt correctly
- [ ] QC4 passed (structure valid)
- [ ] Delivered to recipient
