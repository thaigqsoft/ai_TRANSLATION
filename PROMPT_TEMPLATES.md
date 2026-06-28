# Prompt Templates for Translation & Polishing

**Purpose:** Ready-to-use prompts for AI translation and Thai literary polishing.

---

## 📝 System Prompts

### Translation System Prompt

**File:** `prompts/system_translate.txt`

```
You are a professional Thai literary translator specializing in English-to-Thai novel translation.

Your task:
1. Translate ALL text content inside <p> tags from English to Thai completely
2. Preserve ALL HTML tags, attributes, and structure exactly as-is
3. Keep ONLY proper nouns (character names, place names, skill names) in their original English form — translate EVERYTHING else
4. Maintain the original paragraph breaks and formatting
5. Use natural, fluent Thai literary style appropriate for a fantasy/vampire/web novel
6. Do NOT add, remove, or modify any HTML tags
7. Output ONLY the translated HTML — no explanations, no notes
8. IMPORTANT: Do NOT output any Chinese characters whatsoever — Thai language only
9. IMPORTANT: Translate EVERY word inside <p> tags — do not leave any English words untranslated (except character names and proper nouns)
```

---

### Polishing System Prompt (Gao Fei Style)

**File:** `prompts/system_polish.txt`

```
You are a Thai literary novel polisher specializing in the "Gao Fei" style.

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
3. Keep all proper nouns, character names, system messages, item names, skill names unchanged
4. DO NOT change the meaning or plot — only improve the reading experience
5. Use natural Thai that flows well when read aloud
6. Do NOT add any Chinese characters to the output
7. Output ONLY the polished HTML — no explanations, no notes
```

---

## 📤 User Prompts

### Translation User Prompt Template

**File:** `prompts/user_translate.txt`

```
Translate the following HTML content completely to Thai. Only translate the text inside <p> tags. Keep all HTML tags unchanged. Do not leave any English text untranslated (character names like Quinn are OK to keep).

```html
{html_content}
```
```

**Usage:**
- Replace `{html_content}` with actual HTML
- Send as user message after system prompt

---

### Polishing User Prompt Template (Batch Mode)

**File:** `prompts/user_polish_batch.txt`

```
Below are {count} HTML file(s) that contain Thai translations of a fantasy/vampire/web novel. Polish each file's <p> tag content in Gao Fei style.

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
- No explanations, just the formatted output
```

**Batched content format:**
```
=== FILE: page-0001.html ===
[HTML content here]
=== END: page-0001.html ===

=== FILE: page-0002.html ===
[HTML content here]
=== END: page-0002.html ===
```

---

## 🔧 Prompt Engineering Notes

### Recommended Models

| Task | Model | Provider | Notes |
|------|-------|----------|-------|
| Translation | `gemma4:31b-cloud` | Ollama Pay | Fast, good Thai quality |
| Translation | `deepseek-v3.1:671b-cloud` | Ollama Pay | Higher accuracy, slower |
| Polishing | `deepseek-v3.1:671b-cloud` | Ollama Pay | Best for Gao Fei style |

**API Endpoint:** `https://ollama-pay.thaigqsoft.com/api/v1`

### Temperature Settings

| Task | Temperature | Reason |
|------|-------------|--------|
| Translation | 0.3 | Consistency, accuracy |
| Polishing | 0.4 | Creative flow while maintaining meaning |
| Batch polish | 0.4 | Balance creativity with coherence |

### Max Tokens

| Task | Max Tokens | Reason |
|------|------------|--------|
| Single page translate | 8192 | Full page with buffer |
| Single page polish | 32768 | Room for expanded prose |
| Batch (10 pages) | 32768 | Shared across batch |

### Timeout Settings

| Task | Timeout | Reason |
|------|---------|--------|
| Translation | 120s | Per page |
| Batch polish | 600s | 10 pages together |

---

## 🎯 Proper Noun Handling

### What to Keep in English

**Character Names:**
- Feng, Ruoqing, Quinn, Feng (Feng), Ruoqing (Ruoqing)
- Clan names: Qin, Yang, Ren, Dong, Zhou, Xiao, Yun, Tian

**Place Names:**
- Atlas Studios, Qi Realm, Divine Realm
- Sect names, city names, dimension names

**Technique/Skill Names:**
- Spirit Bristle Nine Yang Divine Art
- Absolute Finger
- Instant Flash
- Heavenly Soul

**System Messages:**
- [System: ...]
- [Quest Complete]
- [Level Up]

### What to Translate

**Everything else:**
- Verbs: become, remain, walk, speak, think
- Adjectives: great, small, ancient, powerful
- Adverbs: suddenly, slowly, quietly, immediately
- Connecting words: the, a, an, and, but, however
- Prepositions: upon, within, toward, without
- Pronouns: I, you, he, she, it, we, they

---

## 🚫 Anti-Patterns (What NOT to Do)

### Bad Translation Examples

**❌ Leaving English:**
```html
<!-- WRONG -->
<p>He suddenly felt a great power within him</p>
<!-- Should be fully Thai except proper nouns -->
```

**❌ Adding Chinese:**
```html
<!-- WRONG -->
<p>เขารู้สึกถึงพลังอันยิ่งใหญ่ภายในตัว他</p>
<!-- Chinese character 他 leaked through -->
```

**❌ Breaking HTML:**
```html
<!-- WRONG -->
<p>เขาค่อยๆ เดิน<em>ไปข้างหน้า</p></em>
<!-- Tags malformed -->
```

### Good Translation Examples

**✅ Fully translated, proper nouns kept:**
```html
<!-- CORRECT -->
<p>เขารู้สึกถึงพลังอันยิ่งใหญ่ภายในตัว</p>
```

**✅ HTML preserved:**
```html
<!-- CORRECT -->
<p>เขา<em>ค่อยๆ</em> ก้าวเดินไปข้างหน้า</p>
```

**✅ Proper nouns in English:**
```html
<!-- CORRECT -->
<p>Feng มองไปที่ Ruoqing ด้วยสายตาเอาจริง</p>
```

---

## 📋 Prompt Checklist

Before sending to API:

- [ ] System prompt set correctly
- [ ] HTML content properly escaped in prompt
- [ ] Temperature appropriate for task
- [ ] Max tokens sufficient
- [ ] Timeout set for request size
- [ ] Retry logic in place (3 attempts)
- [ ] Chinese filter ready for post-processing

---

## 🔄 Response Parsing

### Expected Response Format

**Single page:**
```html
<p>เนื้อหาภาษาไทย</p>
<p>ย่อหน้าถัดไป</p>
```

**Batch mode:**
```
=== FILE: page-0001.html ===
<p>เนื้อหาภาษาไทย</p>
=== END: page-0001.html ===

=== FILE: page-0002.html ===
<p>เนื้อหาภาษาไทย</p>
=== END: page-0002.html ===
```

### Parsing Code

```python
def parse_batch_response(response_text, filenames):
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

    return results
```

---

## 💡 Tips for Better Results

1. **Be explicit about Chinese** — Mention "NO Chinese characters" multiple times
2. **Show format examples** — Include expected output format in prompt
3. **Use few-shot if needed** — Add 1-2 examples for complex tasks
4. **Batch similar content** — Group pages by tone/scene for consistency
5. **Post-process always** — Never trust output without validation
