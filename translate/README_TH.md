# สกิลแปลนิยายภาษาไทย — คู่่มือฉบับสมบรูณ์

**เวอรชัน:** 1.0  
**สร้งเมื่อ:** 2026-05-27  
**จุดประสงค:** ฝก AI agent ใหแปลเว็บโนเวลภาษาอังกฤษเปนภาษาไทยไดอยางมืออาชีพ

---

## 📚 สารบญ

ไดเรกทอรีนีมีทุกสิ่งที่ตองการสำหรับฝก AITranslator:

```
skill_ai/translate/
├── README.md                      # ภาพรวม (ไฟลนี้)
├── README_TH.md                   # คู่มือภาษาไทย (this file)
├── MODELS_AND_API.md              # คู่มือ AI models & Ollama Pay
├── TRANSLATION_WORKFLOW.md        # คู่มือขั้นตอนการแปล
├── PROMPT_TEMPLATES.md            # Prompt ทั้งหมด
├── QA_CHECKLISTS.md               # ขั้นตอน QC
├── REGEX_PATTERNS.md              # Patterns สำหรบ validation
│
├── examples/
│   ├── input_sample.html          # กอนแปล (อังกฤษ)
│   ├── translated_sample.html     # หลังแปล (ไทย)
│   └── polished_sample.html       # หลังขัดเกลา (ไทยเกาเฟย)
│
├── prompts/
│   ├── system_translate.txt       # System prompt สำหรบแปล
│   └── system_polish.txt          # System prompt สำหรบสไตล์เกาเฟย
│
├── scripts/
│   ├── translate_epub.py          # สคริปตแปล (template)
│   ├── polish_gaofei.py           # สคริปตขัดเกลา (template)
│   └── thai_only_fixer.py         # สคริปตเก็บกวาดภาษาอังกฤ
│
└── validation/
    ├── chinese_filter.py          # ลบตวอักษรจีน
    └── structure_validator.py     # ตรวจสอบโครงสราง HTML
```

---

## 🤖 โมเดล AI ที่แนะนำ

### สำหรับแปล (อังกฤษ → ไทย)

| โมเดล | ผูใหบริการ | การใชงาน | หมายเหตุ |
|-------|----------|----------|---------|
| **Gemma 4** | Ollama Pay | แปลหลัก | เร็ว คุณภาพดี |
| DeepSeek V3.1 | Ollama Pay | แปลคุณภาพสูง | ชากวา แตแม่นยำกวา |
| Claude 3.5 Sonnet | Anthropic API | พรีเมียม | คุณภาพดีที่สุด ราคาสูง |

### สำหรับขัดเกลา (สไตล์เกาเฟย)

| โมเดล | ผูใหบริการ | การใชงาน | หมายเหตุ |
|-------|----------|----------|---------|
| **DeepSeek V3.1** | Ollama Pay | ขัดเกลาเกาเฟย | สไตล์วรรณคดีดีเลิศ |
| Gemma 4 | Ollama Pay | ขัดเกลาเบาๆ | เร็ว เหมาะกับงานชุด |

---

## 🔌 ผูใหบริการ API

### Ollama Pay API (แนะนำ)

**Endpoint:** `https://ollama-pay.thaigqsoft.com/api/v1`

**โมเดลที่มี:**
- `gemma4:31b-cloud` — Gemma 4 31B (เร็ว เหมาะแปล)
- `deepseek-v3.1:671b-cloud` — DeepSeek V3.1 671B (ดีที่สุดสำหรับขัดเกลา)

**วิธีตั่งคา:**
```bash
# ขอ API key จาก: https://ollama-pay.thaigqsoft.com
export API_KEY="your-key-here"
```

**ตัวอยางการใช:**
```python
from openai import OpenAI

client = OpenAI(
    api_key="your-key-here",
    base_url="https://ollama-pay.thaigqsoft.com/api/v1"
)

response = client.chat.completions.create(
    model="gemma4:31b-cloud",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt}
    ],
    temperature=0.3,
    max_tokens=8192
)
```

**ขอไดเปรียบ:**
- ✅ จายตามการใช (ไมตองสมัคสมาชิกรายเดือน)
- ✅ มีหลายโมเดลใหเลือก
- ✅ API เขากันไดกบ OpenAI
- ✅ ซัพพอร์ตจากไทย

---

## 🎯 วัตถุประสงคการเรียนรู้

หลังศึกษาสกิลนี้ AI ควรสามารถ:

### 1. การแปล
- [ ] แปล อังกฤษ → ไทย โดยรักษ โครงสราง HTML
- [ ] เก็บ คำวิสามานยนาม (ชื่อตวละคร, สถานท, เทคนิค) เปนอังกฤษ
- [ ] แปล ทุกอยางที่เหลือครบถวน
- [ ] หลีกเลี่่ยงตวอักษรจีนรั่วไหล
- [ ] ใช Gemma 4 หรือ DeepSeek V3.1 ผาน Ollama Pay API

### 2. การขัดเกลา
- [ ] ใช สไตล์เกาเฟย (คม, มีไหวพริบ, นาดึงดูด)
- [ ] ปรับปรุง การไหลลื่น และ อานงาย
- [ ] รักษา ความหมาย และ พล็อตเดิม
- [ ] รักษา โครงสราง HTML

### 3. การควบคุมคุณภาพ
- [ ] ตรวจจับ ตวอักษรจีน ดวย regex
- [ ] ระบุ คำอังกฤษที่เหลือ
- [ ] ตรวจสอบ การรักษ โครงสราง HTML
- [ ] รัน QC checklists อยางเปนระบบ

### 4. การใชเครื่องมือ
- [ ] ใช สคริปตแปล
- [ ] ใช validation filters
- [ ] ติดตาม ความกาวหนา ดวย checkpoint files
- [ ] จัดการ ประมวลผลแบบชุด

---

## 📖 ลำดับการศึกษา

### เฟส 1: พื้นฐาน
1. อ่าน `README.md` — เข้าใจภาพรวม
2. อ่าน `MODELS_AND_API.md` — เรียนรูเกี่ยวกับ AI models & Ollama Pay
3. อ่าน `TRANSLATION_WORKFLOW.md` — เรียนรูขบวนการทั้งหมด
4. ศึกษา `examples/` — ดูตวอยางกอน/หลัง

### เฟส 2: Prompts
5. อ่าน `PROMPT_TEMPLATES.md` — เรียนรู prompt engineering
6. ศึกษา `prompts/system_translate.txt` — Prompt แปล
7. ศึกษา `prompts/system_polish.txt` — Prompt ขัดเกลา

### เฟส 3: เครื่องมือ
8. ศึกษ `scripts/translate_epub.py` — ตรรกะการแปล
9. ศึกษ `scripts/polish_gaofei.py` — ตรรกะการขัดเกลา
10. ศึกษ `scripts/thai_only_fixer.py` — การทำความสะอาดดวย dictionary

### เฟส 4: Validation
11. อ่าน `REGEX_PATTERNS.md` — เรียนรู patterns validation
12. ศึกษา `validation/chinese_filter.py` — การลบจีน
13. ศึกษา `validation/structure_validator.py` — การตรวจสอบโครงสราง

### เฟส 5: Quality Control
14. อ่าน `QA_CHECKLISTS.md` — ขั้นตอน QC
15. ศึกษ `qa_checklists/qc1_post_translation.md`
16. ศึกษ `qa_checklists/qc2_post_polish.md`

---

## 🚀 เร่มตนใชงาน

### สำหรับโปรเจกตใหม

1. **ตังคาไดเรกทอร:**
```bash
mkdir -p project/{extracted,translated,polished,polished_clean}
```

2. **แยก EPUB:**
```bash
unzip -o novel.epub -d extracted/
```

3. **รันแปล:**
```bash
cd scripts/
python translate_epub.py --start 1 --end 100
```

4. **รัน QC1:**
```bash
cd ../qa_checklists/
# ทำตาม checklist ใน qc1_post_translation.md
```

5. **รันขัดเกลา:**
```bash
python polish_gaofei.py --start 1 --end 100
```

6. **รัน QC2:**
```bash
# ทำตาม checklist ใน qc2_post_polish.md
```

7. **รันเก็บกวาดอังกฤษ:**
```bash
python thai_only_fixer.py
```

8. **สราง EPUB ใหม่:**
```bash
cd polished_clean/
zip -X0 ../final.epub mimetype
zip -X9 ../final.epub -r META-INF OEBPS
```

---

## 🎯 แนวคิดสำคัญ

### 1. การรักษ โครงสราง HTML

**กฎทอง:** เปลี่ยนแปลง เฉพาะ ข้อความ ภายใน `<p>` tags เทานั้น

```html
<!-- กอน -->
<p>He <em>slowly</em> walked forward.</p>

<!-- หลัง (ไทย) -->
<p>เขา<em>ค่อ ยๆ</em> กาวเดินไปขางหนา</p>
```

**หามเปลี่ยน:**
- โครงสราง HTML tags
- Attributes (class, id, ฯลฯ)
- Nested tags (`<em>`, `<strong>`, `<a>`)

---

### 2. การจัดการ คำวิสามานยนาม

**เก็บไวเปน อังกฤษ:**
- ชื่อตวละคร: Feng, Ruoqing, Quinn
- ชื่อสถานท: Atlas Studios, Qi Realm
- ชื่ อเทคนิค: Spirit Bristle Nine Yang Divine Art
- ขอความระบบ: [System: ...]

**แปล ทุกอยางอื่น:**
- คำกริยา, คำคุณศัพท, คำวิเศษณ
- คำเชื่อม (the, and, to, however)
- ขอความบรรยาย

---

### 3. ตัวกรอง ตวอักษรจีน

**สำคัญมาก:** DeepSeek V3.1 มักมีตวอักษรจีนรั่วไหล แมจะสั่งใน prompt แลวก็ตาม

**Regex Pattern:**
```python
CHINESE_RE = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+')
```

**ตองใชเสมอ** หลังไดรับ response จาก API

---

### 4. สไตล์ เกาเฟย

| ลักษณะ | คำอธิบาย |
|--------|----------|
| น้ำเสียง | คม, มีไหวพริบ, นาดึงดูด |
| การไหลลื่น | บทสนทนาธรรมชาติ มีมุกภายใน |
| บทพรรณนา | กระชับ ไมเวิ่นเว้อ |
| บทสนทนา | บุคลิกตวละครชัดเจน |
| จังหวะ | ผสมประโยคสั้ น-ยาว ใหลื่นไหล |

---

## 📊 เกณฑ คุณภาพ

| Gate | การตรวจสอบ | เกณฑผาน |
|------|-----------|---------|
| QC1 | ตวอักษรจีน | < 5 ไฟล |
| QC1 | อังกฤษเหลือ | เฉพาะคำวิสามานยนาม |
| QC2 | ตวอักษรจีน | ศูนย tolerance |
| QC2 | อังกฤษเหลือ | เฉพาะคำวิสามานยนาม |
| QC3 | Dictionary sweep | < 5 คำ/หนา |
| QC4 | โครงสราง EPUB | ถูกตอง, เปดใน Books ได |

---

## ⚠️ ปญหาที่พบบอย

### 1. จีนรั่วไหล

**ปญหา:** DeepSeek output มีจีน แมจะสั่งแลว

**วิธีแก:** รัน `chinese_filter.py` เสมอหลัง polish

---

### 2. ลำดับ Dictionary

**ปญหา:** คำสั้ นถูกแทนที่กอนคำยาว

**วิธีแก:** เรียง dictionary ตามความยาว (ยาวสุดกอน)

```python
sorted_dict = sorted(REPLACEMENTS.items(), key=lambda x: -len(x[0]))
```

---

### 3. ลำดับ การสราง EPUB

**ปญหา:** EPUB ไมเปดในโปรแกรมอาน

**วิธีแก:** `mimetype` ตองเปนไฟลแรก และ ไมบีบอัด

```bash
zip -X0 final.epub mimetype      # แรก, ไมบีบอัด
zip -X9 final.epub -r META-INF OEBPS  # หลัง, บีบอัด
```

---

### 4. ความปลอดภัย API Key

**ปญหา:** Token หลุดในสคริปต

**วิธีแก:** 
- ใช environment variables
- หาม commit key จริงๆ ลง version control
- ใช placeholder ในสคริปตที่แบงปน

```python
# ดี
API_KEY = os.environ.get('API_KEY', 'YOUR_KEY_HERE')

# ไมดี
API_KEY = 'sk-xxxxxxxxxxxxxxxx'  # หามเด็ดยิ่ง!
```

---

## 📝 แบบฝกหัด

### แบบฝก 1: ระบุ คำวิสามานยนาม

จากขอความนี้:
> "Feng walked through the Qi Realm, sensing the power of Spirit Bristle Nine Yang Divine Art."

**คำถาม:** คำไหนควรคงไวเปนอังกฤษ?

**คำตอบ:** Feng, Qi Realm, Spirit Bristle Nine Yang Divine Art

---

### แบบฝก 2: ตรวจจับ จีน

จากขอความนี้:
> "เขาเดินไป他รูสึกถึงพลัง"

**คำถาม:** มีอะไรผิด?

**คำตอบ:** มีตวอักษรจีน 他 ตองลบออก

---

### แบบฝก 3: ตรวจสอบ โครงสราง

กำหนดให:
- ต้นฉบับ: 10 `<p>` tags
- หลังแปล: 9 `<p>` tags

**คำถาม:** ถูกตองหรือไม?

**คำตอบ:** ไม — จำนวน paragraph ไมตรง แสดงวาเสียหาย

---

## 🧪 ทดสอบความรู

### Quiz

1. Unicode range อะไรใชตรวจจับตวอักษรจีน?
2. ทำไมตองเรียง dictionary ตามความยาว?
3. ไฟลแรกใน EPUB archive คืออะไร?
4. บอก 3 ลักษณะของสไตล์เกาเฟย
5. ควรแกไข tags อะไรตอนแปล?

### คำตอบ

1. `[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]+`
2. เพื่อเลี่ยงการแทนที่บางสวน (คำยาวกอน)
3. `mimetype` (ไมบีบอัด)
4. น้ำเสียงคม, การไหลลื่นธรรมชาติ, บทพรรณนากระชับ
5. เฉพาะขอความภายใน `<p>` tags

---

## 📞 การสนับสนุน และ ทรัพยากร

### เอกสาร
- `TRANSLATION_WORKFLOW.md` — คู่มือขบวนการเต็ม
- `PROMPT_TEMPLATES.md` — Prompt engineering
- `QA_CHECKLISTS.md` — ขั้ นตอน QC

### สคริปต
- `translate_epub.py` — การแปล
- `polish_gaofei.py` — การขัดเกลา
- `thai_only_fixer.py` — การทำความสะอาด

### Validation
- `chinese_filter.py` — ลบจีน
- `structure_validator.py` — ตรวจสอบ HTML

### ตวอยาง
- `input_sample.html` — กอน
- `translated_sample.html` — หลังแปล
- `polished_sample.html` — หลังขัดเกลา

---

## 📈 ประวัติเวอรชัน

| เวอรชัน | วันที่ | การเปลี่ยนแปลง |
|---------|------|---------------|
| 1.0 | 2026-05-27 | สรางสกิลครั้งแรก |

---

## ✅ Checklist การเสร็จสั้ น

หลังศึกษาสกิลนี้ ตรวจสอบวาคุณสามารถ:

- [ ] อธิบาย ขบวนการแปล ทั้งหมด
- [ ] แยกแยะ คำวิสามานยนาม vs เนื้อหาที่แปลได
- [ ] ตรวจจับ ตวอักษรจีน ดวย regex
- [ ] ใช หลักการ สไตล์เกาเฟย
- [ ] รัน QC checklists
- [ ] ใช validation scripts
- [ ] สรางไฟล EPUB ที่ถูกตอง
- [ ] หลีกเลี่่ยง ปญหาที่พบบอย

**พรอมแปลแลว!** 🎉
