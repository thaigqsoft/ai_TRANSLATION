# QC2 Checklist — Post-Polish (CRITICAL)

**Phase:** After `polish_gaofei.py` completes  
**Location:** `polished/OEBPS/`

> ⚠️ **WARNING:** DeepSeek V3.1 leaks Chinese characters during polish — ZERO tolerance!

---

## ✅ Check 2.1: Chinese Character Detection (CRITICAL)

```bash
cd polished/OEBPS/

# Find ALL Chinese characters
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' .

# Count total occurrences
grep -oP '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' . -r | wc -l

# List affected files
grep -l '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' page-*.html
```

**Pass Criteria:**
- [ ] ZERO Chinese characters allowed
- [ ] If found: MUST clean before proceeding

**Result:** ___ Chinese characters found  
**Status:** ☐ Pass ☐ Fail **(Fail = BLOCKER)**

**If Failed (MANDATORY):**
```bash
# Emergency cleanup
python /path/to/validation/chinese_filter.py --dir . --recursive --force

# Re-check
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' .
# Should return nothing
```

---

## ✅ Check 2.2: Remaining English Detection

```bash
# Find English words 3+ characters
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' . | head -30

# Check for 2-character English (often missed)
grep -rnP '(?<![ก-ฮ])[A-Za-z]{2}(?![ก-ฮ])' . | head -20
```

**Pass Criteria:**
- [ ] Only proper nouns remain
- [ ] < 5 non-proper-noun English words per 100 pages

**Result:** ___ English words found (excluding proper nouns)  
**Status:** ☐ Pass ☐ Fail

---

## ✅ Check 2.3: Polish Quality Spot Check

```bash
# Read 10 random pages for flow
for page in 050 150 250 350 450 550 650 750; do
    echo "=== Page $page (first paragraph) ==="
    grep -oP '<p>.*?</p>' page-$page.html | head -1
done
```

**What to Look For:**
- [ ] Natural Thai flow
- [ ] Consistent tone
- [ ] No awkward literal translations
- [ ] Gao Fei style characteristics (witty, sharp, engaging)

**Status:** ☐ Pass ☐ Fail

**Notes on Quality:**
```
_______________________________________________________
_______________________________________________________
_______________________________________________________
```

---

## ✅ Check 2.4: File Integrity

```bash
# Check all files are valid HTML
python3 -c "
from bs4 import BeautifulSoup
import glob

errors = []
for f in glob.glob('page-*.html'):
    try:
        with open(f) as fh:
            BeautifulSoup(fh.read(), 'html.parser')
    except Exception as e:
        errors.append(f'{f}: {e}')

if errors:
    for e in errors[:10]:
        print(e)
else:
    print('All files valid HTML')
"
```

**Pass Criteria:**
- [ ] All files parse as valid HTML

**Status:** ☐ Pass ☐ Fail

---

## 📋 Summary

| Check | Status | Notes |
|-------|--------|-------|
| 2.1 Chinese Detection | ☐ | **BLOCKER if failed** |
| 2.2 English Detection | ☐ | |
| 2.3 Polish Quality | ☐ | |
| 2.4 File Integrity | ☐ | |

**Overall QC2 Status:** ☐ Pass ☐ Fail  
**Date:** ___________  
**Checked by:** ___________

---

## 🔧 Actions Taken (if failed)

### Chinese Character Cleanup

```
Date/Time: ___________
Command: python validation/chinese_filter.py --dir . --recursive --force
Files affected: ___
Re-check result: ☐ Pass ☐ Fail
```

### Other Actions

```
Date/Time: ___________
Action: _______________
Result: _______________
```

---

## ⚠️ Escalation

If Chinese characters persist after cleanup:

1. Check individual problematic files manually
2. Consider re-translating affected pages
3. Review API prompt for Chinese prevention
4. Document pattern of leakage for future prevention
