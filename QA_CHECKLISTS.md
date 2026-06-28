# Quality Assurance Checklists

**Purpose:** Systematic QC procedures for each translation phase.

---

## 🔍 QC1: Post-Translation Check

**When:** Immediately after `translate_epub.py` completes

**Location:** `translated/OEBPS/`

### Check 1.1: Chinese Character Detection

```bash
cd translated/OEBPS/

# Find all Chinese characters
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' . | head -30

# Count affected files
grep -l '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' page-*.html | wc -l
```

**Pass criteria:**
- < 5 files with Chinese characters
- Chinese only in proper nouns (if any)

**If failed:**
```bash
# Run Chinese filter
python /path/to/validation/chinese_filter.py --dir . --force
```

---

### Check 1.2: Remaining English Detection

```bash
# Find English words 3+ characters
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' . | head -30

# Exclude known proper nouns
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' . | \
  grep -vP '(Feng|Ruoqing|Yuan|Atlas|Studios|Qi|Qin|Yang)' | head -20
```

**Pass criteria:**
- Only proper nouns remain
- < 10 non-proper-noun English words per 100 pages

**Common false positives (acceptable):**
- Character names
- Place names
- Technique names
- System messages

---

### Check 1.3: File Count Verification

```bash
# Source file count
ls ../extracted/OEBPS/page-*.html | wc -l

# Translated file count
ls page-*.html | wc -l

# Compare
echo "Source: $(ls ../extracted/OEBPS/page-*.html | wc -l)"
echo "Translated: $(ls page-*.html | wc -l)"
```

**Pass criteria:**
- Counts must match exactly

---

### Check 1.4: Random Sampling

```bash
# Check 5 random pages
for page in 001 100 300 500 700; do
    echo "=== Page $page ==="
    grep -oP '<p>.*?</p>' page-$page.html | head -2
done
```

**What to look for:**
- Fully translated Thai text
- No English sentences
- No Chinese characters
- HTML tags intact

---

## 🔍 QC2: Post-Polish Check

**When:** Immediately after `polish_gaofei.py` completes

**Location:** `polished/OEBPS/`

### Check 2.1: Chinese Character Detection (CRITICAL)

**DeepSeek V3.1 leaks Chinese during polish — ZERO tolerance**

```bash
cd polished/OEBPS/

# Find ALL Chinese characters
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' .

# Count total occurrences
grep -oP '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' . -r | wc -l

# List affected files
grep -l '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' page-*.html
```

**Pass criteria:**
- ZERO Chinese characters allowed
- If found: MUST clean before proceeding

**If failed:**
```bash
# Emergency cleanup
python /path/to/validation/chinese_filter.py --dir . --recursive --force

# Re-check
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' .
# Should return nothing
```

---

### Check 2.2: Remaining English Detection

```bash
# Find English words 3+ characters
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' . | head -30

# Check for 2-character English (often missed)
grep -rnP '(?<![ก-ฮ])[A-Za-z]{2}(?![ก-ฮ])' . | head -20
```

**Pass criteria:**
- Only proper nouns remain
- < 5 non-proper-noun English words per 100 pages

---

### Check 2.3: Polish Quality Spot Check

```bash
# Read 10 random pages for flow
for page in 050 150 250 350 450 550 650 750; do
    echo "=== Page $page (first paragraph) ==="
    grep -oP '<p>.*?</p>' page-$page.html | head -1
done
```

**What to look for:**
- Natural Thai flow
- Consistent tone
- No awkward literal translations
- Gao Fei style characteristics (witty, sharp, engaging)

---

## 🔍 QC3: Post-English-Sweep Check

**When:** After `thai_only_fixer.py` completes

**Location:** `polished_clean/OEBPS/`

### Check 3.1: Comprehensive English Scan

```bash
cd polished_clean/OEBPS/

# All English 3+ chars (excluding proper nouns)
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' . | \
  grep -vP '(Feng|Ruoqing|Yuan|Atlas|Studios|Qin|Yang|Ren|Dong|Absolute|Finger|Spirit|Bristle)' | head -30

# English 2 chars
grep -rnP '(?<![ก-ฮ])[A-Za-z]{2}(?![ก-ฮ])' . | head -20

# Single English letters (should be none except in tags)
grep -rnP '(?<![ก-ฮa-zA-Z])[A-Za-z](?![ก-ฮa-zA-Z])' . | head -10
```

**Pass criteria:**
- Only proper nouns remain
- < 5 English words per page (non-proper-noun)

---

### Check 3.2: Dictionary Coverage Verification

```bash
# Check if common English words remain
for word in "the" "and" "become" "suddenly" "however" "although"; do
    count=$(grep -ri "$word" . | grep -vP '(Feng|Ruoqing)' | wc -l)
    echo "$word: $count occurrences"
done
```

**Expected:**
- All common words should be 0 or very low
- If high: dictionary needs expansion

---

### Check 3.3: Page-by-Page Analysis

```bash
python3 -c "
import re, glob

files = sorted(glob.glob('page-*.html'))
total_english = 0

for f in files[:100]:  # Sample first 100 pages
    with open(f) as fh:
        text = fh.read()
    
    # Extract <p> content only
    paras = re.findall(r'<p>(.*?)</p>', text, re.DOTALL)
    
    for p in paras:
        # Find English words 3+ chars
        eng = re.findall(r'(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])', p)
        if eng:
            total_english += len(eng)

print(f'First 100 pages: {total_english} English words in <p> tags')
print(f'Average: {total_english / 100:.1f} per page')
"
```

**Pass criteria:**
- < 5 English words per page average
- Only proper nouns in the count

---

## 🔍 QC4: Final EPUB Validation

**When:** After EPUB rebuild

**Location:** `final_novel.epub`

### Check 4.1: Structure Validation

```bash
# List contents
unzip -l final_novel.epub | head -20

# Expected structure:
# Archive:  final_novel.epub
#   Length      Date    Time    Name
# ---------  ---------- -----   ----
#         0  2026-05-27 10:00   mimetype
#       500  2026-05-27 10:00   META-INF/container.xml
#     10000  2026-05-27 10:00   book.opf
#      2000  2026-05-27 10:00   toc.ncx
#     50000  2026-05-27 10:00   OEBPS/style.css
#   ...
```

**Must have:**
- `mimetype` (first file)
- `META-INF/container.xml`
- `book.opf`
- `toc.ncx`
- `OEBPS/style.css`
- `OEBPS/page-*.html`

---

### Check 4.2: Mimetype Verification

```bash
python3 -c "
import zipfile

with zipfile.ZipFile('final_novel.epub') as z:
    names = z.namelist()
    
    # Check 1: mimetype is first
    assert names[0] == 'mimetype', f'First file should be mimetype, got {names[0]}'
    
    # Check 2: mimetype is uncompressed
    info = z.getinfo('mimetype')
    assert info.compress_type == 0, f'mimetype should be uncompressed (0), got {info.compress_type}'
    
    print('✓ EPUB structure valid')
    print(f'  Total files: {len(names)}')
    print(f'  First file: {names[0]}')
    print(f'  mimetype compression: {info.compress_type} (0=stored)')
"
```

---

### Check 4.3: Visual Validation (Apple Books)

```bash
# Open in Apple Books
open -a "Books" "final_novel.epub"
```

**Manual checks:**
- [ ] Opens without error
- [ ] Thai text displays correctly
- [ ] Font is readable (Sukhumvit Set or fallback)
- [ ] Line spacing comfortable
- [ ] Text indentation present
- [ ] No garbled characters
- [ ] Navigation works (TOC)
- [ ] Page breaks appropriate

---

### Check 4.4: File Size Check

```bash
ls -lh final_novel.epub

# Typical sizes:
# 800 pages: 2-5 MB
# 2500 pages: 8-15 MB
```

**If too large (>20 MB for 800 pages):**
- Check for duplicate images
- Verify CSS isn't bloated
- Consider image optimization

---

## 📋 QC Summary Checklist

### Before Moving to Next Phase

| Phase | Checks | Status |
|-------|--------|--------|
| QC1 (Post-Translate) | Chinese < 5 files | ☐ |
| | English = proper nouns only | ☐ |
| | File count matches | ☐ |
| QC2 (Post-Polish) | Chinese = ZERO | ☐ |
| | English = proper nouns only | ☐ |
| | Flow quality spot check | ☐ |
| QC3 (Post-Sweep) | < 5 English/page | ☐ |
| | Dictionary coverage OK | ☐ |
| QC4 (Final EPUB) | Structure valid | ☐ |
| | mimetype first + uncompressed | ☐ |
| | Visual check passed | ☐ |

---

## 🐛 Troubleshooting Guide

### Problem: Chinese keeps appearing after polish

**Root cause:** DeepSeek V3.1 leaks Chinese despite instructions

**Solution:**
```bash
# Apply aggressive filter
python validation/chinese_filter.py --dir polished/ --recursive --force

# Verify
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' polished/
# Should be empty
```

---

### Problem: Too much English remaining

**Root cause:** Dictionary incomplete or order wrong

**Solution:**
```bash
# Check which words are most common
grep -roP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' polished/ | \
  sort | uniq -c | sort -rn | head -30

# Add missing words to dictionary
# Edit thai_only_fixer.py → REPLACEMENTS dict
# Remember: longer phrases first!
```

---

### Problem: EPUB won't open

**Root cause:** mimetype not first or compressed

**Solution:**
```bash
# Check current state
python3 -c "
import zipfile
with zipfile.ZipFile('final_novel.epub') as z:
    print('Files:', z.namelist()[:5])
    print('mimetype compression:', z.getinfo('mimetype').compress_type)
"

# Rebuild correctly
cd polished_clean/
zip -X0 ../final_novel.epub mimetype
zip -X9 ../final_novel.epub META-INF/container.xml book.opf toc.ncx OEBPS/style.css OEBPS/*.html
```

---

### Problem: Translation stuck at page N

**Root cause:** API timeout or network issue

**Solution:**
```bash
# Script should auto-resume from progress file
python translate_epub.py

# If needed, force restart from page N
python translate_epub.py --start N

# Check progress file
cat translation_progress.json | python -m json.tool | grep -A1 'false'
```
