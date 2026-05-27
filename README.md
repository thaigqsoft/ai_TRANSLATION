# Thai Novel Translation Skill — Complete Guide

**Version:** 1.0  
**Created:** 2026-05-27  
**Purpose:** Train AI agents to translate English web novels to Thai with professional quality

---

## 📚 What's Included

This skill directory contains everything needed to train an AI translator:

```
skill_ai/translate/
├── README.md                      # Overview (this file)
├── TRANSLATION_WORKFLOW.md        # Step-by-step workflow guide
├── PROMPT_TEMPLATES.md            # All prompts for translation & polish
├── QA_CHECKLISTS.md               # Quality control procedures
├── REGEX_PATTERNS.md              # Validation & cleanup patterns
│
├── examples/
│   ├── input_sample.html          # Before translation (English)
│   ├── translated_sample.html     # After translation (Thai)
│   └── polished_sample.html       # After Gao Fei polish (Refined Thai)
│
├── prompts/
│   ├── system_translate.txt       # System prompt for translation
│   └── system_polish.txt          # System prompt for Gao Fei style
│
├── scripts/
│   ├── translate_epub.py          # Translation script (template)
│   ├── polish_gaofei.py           # Polishing script (template)
│   └── thai_only_fixer.py         # English cleanup script
│
└── validation/
    ├── chinese_filter.py          # Chinese character removal
    └── structure_validator.py     # HTML structure checker
```

---

## 🎯 Learning Objectives

After studying this skill, an AI should be able to:

### 1. Translation
- [ ] Translate English → Thai while preserving HTML structure
- [ ] Keep proper nouns in English (character names, places, techniques)
- [ ] Translate all other content completely
- [ ] Avoid Chinese character leakage

### 2. Polishing
- [ ] Apply Gao Fei literary style characteristics
- [ ] Improve flow and readability
- [ ] Maintain original meaning and plot
- [ ] Preserve HTML structure

### 3. Quality Control
- [ ] Detect Chinese characters using regex
- [ ] Identify remaining English words
- [ ] Validate HTML structure preservation
- [ ] Run systematic QC checklists

### 4. Tool Usage
- [ ] Use translation scripts
- [ ] Apply validation filters
- [ ] Track progress with checkpoint files
- [ ] Handle batch processing

---

## 📖 Study Order

### Phase 1: Fundamentals
1. Read `README.md` — Understand overview
2. Read `TRANSLATION_WORKFLOW.md` — Learn the full process
3. Study `examples/` — See before/after comparisons

### Phase 2: Prompts
4. Read `PROMPT_TEMPLATES.md` — Learn prompt engineering
5. Study `prompts/system_translate.txt` — Translation prompt
6. Study `prompts/system_polish.txt` — Polishing prompt

### Phase 3: Tools
7. Review `scripts/translate_epub.py` — Translation logic
8. Review `scripts/polish_gaofei.py` — Polishing logic
9. Review `scripts/thai_only_fixer.py` — Dictionary cleanup

### Phase 4: Validation
10. Read `REGEX_PATTERNS.md` — Learn validation patterns
11. Study `validation/chinese_filter.py` — Chinese removal
12. Study `validation/structure_validator.py` — Structure check

### Phase 5: Quality Control
13. Read `QA_CHECKLISTS.md` — QC procedures
14. Review `qa_checklists/qc1_post_translation.md`
15. Review `qa_checklists/qc2_post_polish.md`

---

## 🔑 Key Concepts

### 1. HTML Structure Preservation

**Golden Rule:** Only modify text INSIDE `<p>` tags.

```html
<!-- BEFORE -->
<p>He <em>slowly</em> walked forward.</p>

<!-- AFTER (Thai) -->
<p>เขา<em>ค่อยๆ</em> ก้าวเดินไปข้างหน้า</p>
```

**Never change:**
- HTML tag structure
- Attributes (class, id, etc.)
- Nested tags (`<em>`, `<strong>`, `<a>`)

---

### 2. Proper Noun Handling

**Keep in English:**
- Character names: Feng, Ruoqing, Quinn
- Place names: Atlas Studios, Qi Realm
- Technique names: Spirit Bristle Nine Yang Divine Art
- System messages: [System: ...]

**Translate everything else:**
- Verbs, adjectives, adverbs
- Connecting words (the, and, to, however)
- Descriptive text

---

### 3. Chinese Character Filter

**Critical:** DeepSeek V3.1 leaks Chinese characters even when instructed not to.

**Regex Pattern:**
```python
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
```

**Always apply after receiving API response.**

---

### 4. Gao Fei Style

| Trait | Description |
|-------|-------------|
| Voice | Sharp, witty, engaging |
| Flow | Natural conversational rhythm |
| Prose | Descriptive but punchy |
| Dialogue | Distinct character personalities |
| Pacing | Mix of short and long sentences |

---

## 🚀 Quick Start

### For New Projects

1. **Setup directories:**
```bash
mkdir -p project/{extracted,translated,polished,polished_clean}
```

2. **Extract EPUB:**
```bash
unzip -o novel.epub -d extracted/
```

3. **Run translation:**
```bash
cd scripts/
python translate_epub.py --start 1 --end 100
```

4. **Run QC1:**
```bash
cd ../qa_checklists/
# Follow qc1_post_translation.md checklist
```

5. **Run polish:**
```bash
python polish_gaofei.py --start 1 --end 100
```

6. **Run QC2:**
```bash
# Follow qc2_post_polish.md checklist
```

7. **Run English sweep:**
```bash
python thai_only_fixer.py
```

8. **Rebuild EPUB:**
```bash
cd polished_clean/
zip -X0 ../final.epub mimetype
zip -X9 ../final.epub -r META-INF OEBPS
```

---

## 📊 Quality Gates

| Gate | Check | Pass Criteria |
|------|-------|---------------|
| QC1 | Chinese chars | < 5 files |
| QC1 | English remaining | Only proper nouns |
| QC2 | Chinese chars | ZERO tolerance |
| QC2 | English remaining | Only proper nouns |
| QC3 | Dictionary sweep | < 5 English/page |
| QC4 | EPUB structure | Valid, opens in Books |

---

## ⚠️ Common Pitfalls

### 1. Chinese Leaks

**Problem:** DeepSeek outputs Chinese despite instructions

**Solution:** Always run `chinese_filter.py` after polish

---

### 2. Dictionary Order

**Problem:** Short words replaced before long phrases

**Solution:** Sort dictionary by length (longest first)

```python
sorted_dict = sorted(REPLACEMENTS.items(), key=lambda x: -len(x[0]))
```

---

### 3. EPUB Rebuild Order

**Problem:** EPUB won't open in readers

**Solution:** `mimetype` must be first file, uncompressed

```bash
zip -X0 final.epub mimetype      # First, no compression
zip -X9 final.epub -r META-INF OEBPS  # Then, compressed
```

---

### 4. API Key Security

**Problem:** Tokens exposed in scripts

**Solution:** 
- Use environment variables
- Never commit real keys to version control
- Use placeholder values in shared scripts

```python
# Good
API_KEY = os.environ.get('API_KEY', 'YOUR_KEY_HERE')

# Bad (example format only - NEVER use real keys!)
API_KEY = 'sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'  # NEVER commit real keys!
```

---

## 📝 Training Exercises

### Exercise 1: Identify Proper Nouns

Given this text:
> "Feng walked through the Qi Realm, sensing the power of Spirit Bristle Nine Yang Divine Art."

**Question:** Which words should remain in English?

**Answer:** Feng, Qi Realm, Spirit Bristle Nine Yang Divine Art

---

### Exercise 2: Detect Chinese

Given this text:
> "เขาเดินไป他รู้สึกถึงพลัง"

**Question:** What's wrong?

**Answer:** Chinese character 他 detected — must remove

---

### Exercise 3: Validate Structure

Given:
- Original: 10 `<p>` tags
- Translated: 9 `<p>` tags

**Question:** Is this valid?

**Answer:** No — paragraph count mismatch indicates lost content

---

## 🧪 Testing Your Knowledge

### Quiz

1. What Unicode range detects Chinese characters?
2. Why must dictionary entries be sorted by length?
3. What's the first file in an EPUB archive?
4. Name three Gao Fei style characteristics
5. What tags should you modify during translation?

### Answers

1. `[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+`
2. To avoid partial replacements (long phrases first)
3. `mimetype` (uncompressed)
4. Sharp voice, natural flow, punchy prose, distinct dialogue, good pacing
5. Only text inside `<p>` tags

---

## 📞 Support & Resources

### Documentation
- `TRANSLATION_WORKFLOW.md` — Full process guide
- `PROMPT_TEMPLATES.md` — Prompt engineering
- `QA_CHECKLISTS.md` — Quality procedures

### Scripts
- `translate_epub.py` — Translation
- `polish_gaofei.py` — Polishing
- `thai_only_fixer.py` — English cleanup

### Validation
- `chinese_filter.py` — Remove Chinese
- `structure_validator.py` — Check HTML

### Examples
- `input_sample.html` — Before
- `translated_sample.html` — After translation
- `polished_sample.html` — After polish

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-27 | Initial skill creation |

---

## ✅ Completion Checklist

After studying this skill, verify you can:

- [ ] Explain the full translation workflow
- [ ] Identify proper nouns vs translatable content
- [ ] Detect Chinese characters using regex
- [ ] Apply Gao Fei style principles
- [ ] Run QC checklists
- [ ] Use validation scripts
- [ ] Build valid EPUB files
- [ ] Avoid common pitfalls

**Ready to translate!** 🎉
