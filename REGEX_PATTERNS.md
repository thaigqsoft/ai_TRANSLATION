# Regex Patterns for Validation & Cleanup

**Purpose:** Ready-to-use regex patterns for Chinese detection, English cleanup, and HTML validation.

---

## 🔴 Chinese Character Detection

### Basic Pattern

```python
# Matches all CJK Unified Ideographs
CHINESE_RE = re.compile(r'[\u4e00-\u9fff]+')
```

### Comprehensive Pattern (Recommended)

```python
# Matches:
# - CJK Unified Ideographs (\u4e00-\u9fff)
# - CJK Extension A (\u3400-\u4dbf)
# - CJK Compatibility Ideographs (\uf900-\ufaff)
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
```

### Usage Examples

```python
import re

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

# Check if text contains Chinese
text = "เขาเดินไป他"
if CHINESE_RE.search(text):
    print("Chinese detected!")

# Remove all Chinese
clean_text = CHINESE_RE.sub('', text)
print(clean_text)  # "เขาเดินไป"

# Find all Chinese matches
matches = CHINESE_RE.findall(text)
print(matches)  # ['他']
```

---

## 🟡 English Detection (Thai Context)

### Basic Pattern

```python
# Matches English words in Thai text
ENGLISH_RE = re.compile(r'[A-Za-z]+')
```

### Context-Aware Pattern (Recommended)

```python
# Matches English words 3+ characters NOT surrounded by Thai
# Negative lookbehind: not preceded by Thai
# Negative lookahead: not followed by Thai
ENGLISH_RE = re.compile(r'(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])')
```

### Proper Noun Exclusion

```python
# Common proper nouns to exclude from cleanup
PROPER_NOUNS = [
    'Feng', 'Ruoqing', 'Yuan', 'Atlas', 'Studios',
    'Qin', 'Yang', 'Ren', 'Dong', 'Zhou', 'Xiao',
    'Yun', 'Tian', 'Hua', 'Ming', 'Li', 'Wang',
    'Zhang', 'Bai', 'Long', 'Jiang', 'Han', 'Xu',
    'Wei', 'Lin', 'Huang', 'Wu', 'Liu', 'Chen',
    'Zhao', 'Sun', 'Zhu', 'Ma', 'Hu', 'Guo',
    'He', 'Gao', 'Luo', 'Liang', 'Song', 'Tang',
    'Absolute', 'Finger', 'Spirit', 'Bristle'
]

# Pattern that excludes proper nouns
PROPER_NOUN_PATTERN = '|'.join(PROPER_NOUNS)
ENGLISH_CLEANUP_RE = re.compile(
    rf'(?<![ก-ฮ])(?!{PROPER_NOUN_PATTERN})[A-Za-z]{{3,}}(?![ก-ฮ])'
)
```

### Usage Examples

```python
import re

# Pattern for finding problematic English
ENGLISH_RE = re.compile(r'(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])')

text = "Feng มองเห็น the book บนโต๊ะ"

# Find all English
matches = ENGLISH_RE.findall(text)
print(matches)  # ['the', 'book'] (Feng excluded by Thai context)

# In <p> tag context
html = '<p>Feng เดินเข้าไปใน the room</p>'
p_content = re.search(r'<p>(.*?)</p>', html).group(1)
english_in_p = ENGLISH_RE.findall(p_content)
print(english_in_p)  # ['the']
```

---

## 🟢 HTML Structure Patterns

### Extract <p> Tag Content

```python
# Non-greedy match for <p> content
P_TAG_RE = re.compile(r'<p>(.*?)</p>', re.DOTALL)

# Usage
html = '<p>Text 1</p><p>Text 2</p>'
paragraphs = P_TAG_RE.findall(html)
print(paragraphs)  # ['Text 1', 'Text 2']
```

### Extract All Tag Names

```python
# Match any HTML tag
TAG_RE = re.compile(r'<(/?)(\w+)([^>]*)>')

# Usage
html = '<p class="test">Content</p>'
matches = TAG_RE.findall(html)
print(matches)  # [('/', 'p', ' class="test"')]
```

### Validate HTML Structure Preservation

```python
def validate_structure(original, translated):
    """Check if HTML structure is preserved after translation."""
    from bs4 import BeautifulSoup
    
    orig_soup = BeautifulSoup(original, 'html.parser')
    trans_soup = BeautifulSoup(translated, 'html.parser')
    
    # Check <p> count
    orig_ps = orig_soup.find_all('p')
    trans_ps = trans_soup.find_all('p')
    
    if len(orig_ps) != len(trans_ps):
        return False, f"Paragraph count mismatch: {len(orig_ps)} vs {len(trans_ps)}"
    
    # Check tag structure (simplified)
    orig_tags = [tag.name for tag in orig_soup.find_all()]
    trans_tags = [tag.name for tag in trans_soup.find_all()]
    
    if orig_tags != trans_tags:
        return False, "Tag structure differs"
    
    return True, "Structure preserved"
```

---

## 🔧 Cleanup Patterns

### Strip Chinese from HTML (Preserving Structure)

```python
import re
from bs4 import BeautifulSoup, NavigableString, Comment

CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')

def strip_chinese_from_html(html):
    """Remove Chinese characters from <p> tag content only."""
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

# Usage
html = '<p>เขาเดินไป他</p>'
clean = strip_chinese_from_html(html)
print(clean)  # '<p>เขาเดินไป</p>'
```

### Replace English Words (Dictionary-Based)

```python
import re

# Dictionary (longer phrases FIRST!)
REPLACEMENTS = {
    "Spirit Bristle": "สปิริตบริสเซิล",
    "Absolute Finger": "แอบโซลูทฟิงเกอร์",
    "Qi Condensation": "ชีกักขั่น",
    "Divine Realm": "ไดไวน์เรียลม์",
    "suddenly": "ทันใดนั้่น",
    "immediately": "ทันที",
    "become": "กลายเป็่น",
    "remain": "ยังคง",
    "the": "",  # Often can be removed
    "and": "และ",
    # ... more entries
}

def replace_english_words(text):
    """Replace English words with Thai equivalents."""
    result = text
    
    # Sort by length (longest first) to avoid partial replacements
    sorted_dict = sorted(REPLACEMENTS.items(), key=lambda x: -len(x[0]))
    
    for eng, thai in sorted_dict:
        # Pattern: word boundary, not surrounded by Thai
        pattern = rf'(?<![ก-ฮa-zA-Z]){re.escape(eng)}(?![ก-ฮa-zA-Z])'
        result = re.sub(pattern, thai, result, flags=re.IGNORECASE)
    
    return result

# Usage
text = "He suddenly become powerful"
clean = replace_english_words(text)
print(clean)  # "เขา ทันใดนั้่น กลายเป็่น มีพลัง"
```

---

## 📊 Validation Patterns

### Check Translation Completeness

```python
def check_translation_complete(original_html, translated_html):
    """Verify translation didn't skip content."""
    from bs4 import BeautifulSoup
    
    orig_soup = BeautifulSoup(original_html, 'html.parser')
    trans_soup = BeautifulSoup(translated_html, 'html.parser')
    
    # Extract <p> text content
    orig_texts = [p.get_text().strip() for p in orig_soup.find_all('p')]
    trans_texts = [p.get_text().strip() for p in trans_soup.find_all('p')]
    
    issues = []
    
    # Check count
    if len(orig_texts) != len(trans_texts):
        issues.append(f"Paragraph count: {len(orig_texts)} → {len(trans_texts)}")
    
    # Check for empty translations
    for i, (orig, trans) in enumerate(zip(orig_texts, trans_texts)):
        if orig.strip() and not trans.strip():
            issues.append(f"Page {i+1}: Empty translation")
    
    return len(issues) == 0, issues
```

### Check for Untranslated English

```python
def count_english_words(html_content):
    """Count English words in <p> tags."""
    import re
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html_content, 'html.parser')
    english_count = 0
    
    ENGLISH_RE = re.compile(r'(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])')
    
    for p in soup.find_all('p'):
        text = p.get_text()
        matches = ENGLISH_RE.findall(text)
        english_count += len(matches)
    
    return english_count

# Usage
html = '<p>Feng เดินเข้าไปใน the room</p>'
count = count_english_words(html)
print(count)  # 1 (only "the" counted, Feng excluded)
```

---

## 🎯 Bash/Grep Patterns

### Command Line Chinese Detection

```bash
# Find Chinese in all HTML files
grep -rn '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' OEBPS/

# Count occurrences
grep -oP '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' OEBPS/*.html | wc -l

# List files with Chinese
grep -l '[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]' OEBPS/*.html
```

### Command Line English Detection

```bash
# Find English 3+ chars in Thai context
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' OEBPS/

# Exclude proper nouns
grep -rnP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' OEBPS/ | \
  grep -vP '(Feng|Ruoqing|Yuan|Atlas|Studios)'

# Count per file
for f in OEBPS/page-*.html; do
    count=$(grep -oP '(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])' "$f" | wc -l)
    echo "$f: $count English words"
done
```

### File Count Verification

```bash
# Count HTML files
ls OEBPS/page-*.html | wc -l

# Verify range completeness
ls OEBPS/page-*.html | \
  sed 's/page-0*//' | sed 's/.html//' | \
  sort -n | \
  awk 'NR==1{min=$1} {if($1!=prev+1){print "Gap: "prev"-"$1} prev=$1} END{print "Range: "min"-"prev}'
```

---

## 📋 Pattern Quick Reference

| Purpose | Pattern | Flags |
|---------|---------|-------|
| Chinese chars | `[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+` | None |
| English in Thai | `(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])` | None |
| <p> content | `<p>(.*?)</p>` | `re.DOTALL` |
| Any HTML tag | `<(/?)(\w+)([^>]*)>` | None |
| Word boundary | `\bword\b` | None |
| Thai chars | `[ก-ฮ]` | None |

---

## ⚠️ Common Pitfalls

### 1. Forgetting Unicode Ranges

**Wrong:**
```python
CHINESE_RE = re.compile(r'[\u4e00-\u9fff]+')  # Missing extensions
```

**Correct:**
```python
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
```

---

### 2. Dictionary Order Matters

**Wrong:**
```python
REPLACEMENTS = {
    "the": "เดอะ",
    "Spirit Bristle": "สปิริตบริสเซิล",  # Never matches!
}
```

**Correct:**
```python
REPLACEMENTS = {
    "Spirit Bristle": "สปิริตบริสเซิล",  # Longer first
    "the": "เดอะ",
}
```

---

### 3. Not Handling Mixed Content

**Wrong:**
```python
# This fails for <p>He <em>slowly</em> walked</p>
p.string = CHINESE_RE.sub('', p.string)
```

**Correct:**
```python
# Handle nested tags
for child in p.children:
    if isinstance(child, NavigableString):
        child.replace_with(CHINESE_RE.sub('', str(child)))
```

---

### 4. Greedy vs Non-Greedy

**Wrong (greedy):**
```python
re.findall(r'<p>.*</p>', html)  # Matches from first <p> to last </p>
```

**Correct (non-greedy):**
```python
re.findall(r'<p>.*?</p>', html)  # Matches each <p> individually
```

---

## 🧪 Testing Patterns

```python
def test_patterns():
    """Test regex patterns work correctly."""
    
    # Chinese detection
    CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
    assert CHINESE_RE.search('เขาเดิน他')
    assert not CHINESE_RE.search('เขาเดินไป')
    
    # English in Thai
    ENGLISH_RE = re.compile(r'(?<![ก-ฮ])[A-Za-z]{3,}(?![ก-ฮ])')
    assert 'the' in ENGLISH_RE.findall('เขาเห็น the book')
    assert 'Feng' not in ENGLISH_RE.findall('Feng เดิน')  # Followed by Thai
    
    # <p> extraction
    P_RE = re.compile(r'<p>(.*?)</p>', re.DOTALL)
    assert len(P_RE.findall('<p>a</p><p>b</p>')) == 2
    
    print("All pattern tests passed!")

test_patterns()
```
