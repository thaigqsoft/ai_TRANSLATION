# QC1 Checklist — Post-Translation

**Phase:** After `translate_epub.py` completes  
**Location:** `translated/OEBPS/`

---

## ✅ Check 1.1: Chinese Character Detection

```bash
cd translated/OEBPS/

# Find all Chinese characters
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' . | head -30

# Count affected files
grep -l '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' page-*.html | wc -l
```

**Pass Criteria:**
- [ ] < 5 files with Chinese characters
- [ ] Chinese only in proper nouns (if any)

**Result:** ___ files affected  
**Status:** ☐ Pass ☐ Fail

**If Failed:**
```bash
python /path/to/validation/chinese_filter.py --dir . --force
```

---

## ✅ Check 1.2: Remaining English Detection

```bash
# Find English words 3+ characters
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' . | head -30

# Exclude known proper nouns
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' . | \
  grep -vP '(Feng|Ruoqing|Yuan|Atlas|Studios|Qi|Qin|Yang)' | head -20
```

**Pass Criteria:**
- [ ] Only proper nouns remain
- [ ] < 10 non-proper-noun English words per 100 pages

**Result:** ___ English words found (excluding proper nouns)  
**Status:** ☐ Pass ☐ Fail

---

## ✅ Check 1.3: File Count Verification

```bash
# Source file count
ls ../extracted/OEBPS/page-*.html | wc -l

# Translated file count
ls page-*.html | wc -l
```

**Pass Criteria:**
- [ ] Counts match exactly

**Result:** Source = ___, Translated = ___  
**Status:** ☐ Pass ☐ Fail

---

## ✅ Check 1.4: Random Sampling

```bash
# Check 5 random pages
for page in 001 100 300 500 700; do
    echo "=== Page $page ==="
    grep -oP '<p>.*?</p>' page-$page.html | head -2
done
```

**What to Look For:**
- [ ] Fully translated Thai text
- [ ] No English sentences
- [ ] No Chinese characters
- [ ] HTML tags intact

**Status:** ☐ Pass ☐ Fail

---

## 📋 Summary

| Check | Status | Notes |
|-------|--------|-------|
| 1.1 Chinese Detection | ☐ | |
| 1.2 English Detection | ☐ | |
| 1.3 File Count | ☐ | |
| 1.4 Random Sampling | ☐ | |

**Overall QC1 Status:** ☐ Pass ☐ Fail  
**Date:** ___________  
**Checked by:** ___________

---

## 🔧 Actions Taken (if failed)

```
Date/Time: ___________
Action: _______________
Result: _______________
```
