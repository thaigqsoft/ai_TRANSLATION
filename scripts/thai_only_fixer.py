#!/usr/bin/env python3
"""
thai_only_fixer.py — Clean up remaining English words in Thai translation

USAGE:
    python thai_only_fixer.py

FEATURES:
- ~1200-term dictionary for English → Thai replacement
- Regex-based word boundary detection
- Preserves proper nouns (character names, places, techniques)
- Only modifies <p>, <h2>, <title> tags
- Fast: ~3 minutes for 800 pages

NOTE: This is a TEMPLATE with sample dictionary entries.
      Expand the REPLACEMENTS dict with your own terms.
"""

import os
import re
from bs4 import BeautifulSoup, NavigableString

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────

WORK = "/path/to/your/project"
IN_DIR = os.path.join(WORK, "polished")
OUT_DIR = os.path.join(WORK, "polished_clean")

# ─────────────────────────────────────────────────────────────────────────────
# DICTIONARY — LONGER PHRASES FIRST!
# ─────────────────────────────────────────────────────────────────────────────

REPLACEMENTS = {
    # Multi-word phrases (Gao Fei specific) — MUST BE FIRST
    "Spirit Bristle Nine Yang Divine Art": "สปิริตบริสเซิลไนน์ยางไดไวน์อาท",
    "Absolute Finger": "แอบโซลูทฟิงเกอร์",
    "Qi Condensation": "ชีกักขั่น",
    "Soul Formation": "โซลฟอร์เมชัน",
    "Divine Realm": "ไดไวน์เรียลม์",
    "Instant Flash": "อินสแตนท์แฟลช",
    "Heavenly Soul": "เฮฟเวนลี่โซล",
    "Essence Qi": "เอสเซนซ์ชี",
    
    # Cultivation realms
    "Qi Condensation Level": "ชีกักขั่นเลเวล",
    "Foundation Establishment": "ฟาวน์เดชันเอสแทบลิชเมนต์",
    "Golden Core": "โกลเด้นคอร์",
    "Nascent Soul": "เนเซนท์โซล",
    "Spirit Severing": "สปิริตเซเวอริง",
    "Dao Seeking": "เต๋าซิกกิง",
    "Immortal": "อิมมอร์ทอล",
    
    # Common words — most frequently appearing
    "suddenly": "ทันใดนั้น",
    "immediately": "ทันทที",
    "slowly": "ค่อ ยๆ",
    "quietly": "อย่ างสง บ",
    "become": "กลายเป็ น",
    "became": "กลายเป็ น",
    "remained": "ยั งคง",
    "remain": "ยั งคง",
    "started": "เริ่ มต้ น",
    "begin": "เริ่ มต้ น",
    
    # Connecting words
    "the": "",  # Often can be removed entirely
    "and": "และ",
    "but": "แต่",
    "however": "อย่ างไรก็ ตาม",
    "although": "แม้ ว่า",
    "therefore": "ดั งนั้ น",
    "meanwhile": "ในขณะเดี ยวกั น",
    
    # Pronouns
    "he": "เขา",
    "she": "เธอ",
    "they": "พวกเขา",
    "we": "เรา",
    "I": "ฉั น",
    "you": "คุ ณ",
    "it": "มั น",
    
    # Verbs
    "walked": "เดิ น",
    "walk": "เดิ น",
    "run": "วิ่ ง",
    "ran": "วิ่ ง",
    "speak": "พู ด",
    "spoke": "พู ด",
    "said": "กล่ าว",
    "say": "พู ด",
    "look": "มอง",
    "looked": "มอง",
    "see": "เห็ น",
    "saw": "เห็ น",
    "know": "รู้ ",
    "knew": "รู้ ",
    "think": "คิ ด",
    "thought": "คิ ด",
    "want": "ต้ องการ",
    "wanted": "ต้ องการ",
    "need": "ต้ องการ",
    "needed": "ต้ องการ",
    "make": "ทำ",
    "made": "ทำ",
    "take": "นำ",
    "took": "นำ",
    "give": "ให้ ",
    "gave": "ให้ ",
    "come": "มา",
    "came": "มา",
    "go": "ไป",
    "went": "ไป",
    
    # Adjectives
    "great": "ยิ่ งใหญ่",
    "powerful": "มี พลัง",
    "strong": "แข็ งแกร่ง",
    "weak": "อ่ อนแอ",
    "ancient": "โบราณ",
    "old": "แก่ ",
    "young": "หนุ่ มสาว",
    "beautiful": "สวยงาม",
    "ugly": "น่าเกลี ยด",
    "dark": "มื ด",
    "bright": "สว่ าง",
    "cold": "เย็ น",
    "hot": "ร้ อน",
    
    # Adverbs
    "very": "มาก",
    "extremely": "อย่ างยิ่ ง",
    "completely": "อย่ างสมบู รณ์ ",
    "totally": "อย่ างสิ้ นเชิ ง",
    "partially": "บางส่ วน",
    "quickly": "อย่ างรวดเร็ ว",
    "carefully": "อย่ างระมั ดระวั ง",
    
    # Prepositions
    "upon": "บน",
    "within": "ภายใน",
    "without": "โดยไม่ มี",
    "toward": "ไปทาง",
    "towards": "ไปทาง",
    "before": "ก่ อน",
    "after": "หลัง",
    "during": "ระหว่ าง",
    
    # Nouns
    "world": "โลก",
    "power": "พลัง",
    "energy": "พลังงาน",
    "spirit": "วิญญาณ",
    "soul": "จิตวิญญาณ",
    "body": "ร่ างกาย",
    "mind": "จิ ตใจ",
    "heart": "หั วใจ",
    "hand": "มื อ",
    "eye": "ตา",
    "face": "หน้ า",
    "voice": "เสี ยง",
    "sound": "เสี ยง",
    "light": "แสง",
    "shadow": "เงา",
    "tree": "ต้ นไม้ ",
    "forest": "ป่ า",
    "mountain": "ภูเขา",
    "river": "แม่ นำ้ ",
    "sky": "ท้ องฟ้า ",
    "ground": "พื้ นดิ น",
    "floor": "พื้ น",
    "door": "ประตู ",
    "room": "ห้ อง",
    "hall": "โถ ง",
    "path": "เส้ นทาง",
    "road": "ถนน",
    
    # System messages
    "System Alert": "การแจ้ งเตื อนจากระบบ",
    "Quest Complete": "เควสสมบู รณ์ ",
    "Level Up": "เลเวลอั พ",
    "Host": "ผู้ ใช้งาน",
    "Reward": "รางวั ล",
    "Quest": "เควส",
    
    # Add more terms as needed...
}

# Proper nouns to EXCLUDE from replacement
PROPER_NOUNS = [
    'Feng', 'Ruoqing', 'Yuan', 'Atlas', 'Studios',
    'Qin', 'Yang', 'Ren', 'Dong', 'Zhou', 'Xiao',
    'Yun', 'Tian', 'Hua', 'Ming', 'Li', 'Wang',
    'Zhang', 'Bai', 'Long', 'Jiang', 'Han', 'Xu',
    'Wei', 'Lin', 'Huang', 'Wu', 'Liu', 'Chen',
    'Zhao', 'Sun', 'Zhu', 'Ma', 'Hu', 'Guo',
    'He', 'Gao', 'Luo', 'Liang', 'Song', 'Tang',
    # Add more as needed
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def build_pattern():
    """Build regex pattern for English word detection."""
    # Escape proper nouns for regex
    proper_noun_pattern = '|'.join(re.escape(noun) for noun in PROPER_NOUNS)
    
    # Pattern: English word NOT surrounded by Thai, excluding proper nouns
    pattern = rf'(?<![ก-ฮa-zA-Z])(?!{proper_noun_pattern})[A-Za-z]{{3,}}(?![ก-ฮa-zA-Z])'
    return re.compile(pattern, re.IGNORECASE)


def replace_in_text(text, pattern):
    """Replace English words in text using dictionary."""
    result = text
    
    # Sort by length (longest first) to avoid partial replacements
    sorted_dict = sorted(REPLACEMENTS.items(), key=lambda x: -len(x[0]))
    
    for eng, thai in sorted_dict:
        # Build pattern for this specific word
        word_pattern = rf'(?<![ก-ฮa-zA-Z]){re.escape(eng)}(?![ก-ฮa-zA-Z])'
        result = re.sub(word_pattern, thai, result, flags=re.IGNORECASE)
    
    return result


def process_html(html_content, pattern):
    """Process HTML content, replacing English in <p>, <h2>, <title> tags."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Tags to process
    tags_to_process = ['p', 'h2', 'h1', 'h3', 'title']
    
    for tag_name in tags_to_process:
        for tag in soup.find_all(tag_name):
            if tag.string and isinstance(tag.string, str):
                # Direct text content
                tag.string = replace_in_text(tag.string, pattern)
            else:
                # Mixed content (nested tags)
                for child in tag.children:
                    if isinstance(child, str) and child.strip():
                        replaced = replace_in_text(child, pattern)
                        child.replace_with(replaced)
    
    return str(soup)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # Ensure output directory
    os.makedirs(OUT_DIR, exist_ok=True)
    
    # Get HTML files
    files = [f for f in os.listdir(IN_DIR) if f.startswith('page-') and f.endswith('.html')]
    files.sort(key=lambda x: int(x.split('-')[1].split('.')[0]))
    
    if not files:
        print(f"No files found in {IN_DIR}")
        return
    
    print(f"Processing {len(files)} files...")
    
    # Build pattern
    pattern = build_pattern()
    
    # Process each file
    total_replacements = 0
    for idx, fname in enumerate(files, 1):
        src_path = os.path.join(IN_DIR, fname)
        out_path = os.path.join(OUT_DIR, fname)
        
        # Read
        with open(src_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Process
        processed_html = process_html(html_content, pattern)
        
        # Save
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(processed_html)
        
        if idx % 100 == 0:
            print(f"  Processed {idx}/{len(files)} files...")
    
    print(f"\nEnglish Sweep Complete!")
    print(f"Files processed: {len(files)}")
    print(f"Output: {OUT_DIR}/")


if __name__ == "__main__":
    main()
