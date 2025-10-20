import re

def convert_brackets(text):
    return re.sub(r'([\u4e00-\u9fff]+)\[(.+?)\]', r'<ruby>\1<rt>\2</rt></ruby>', text)

def convert_braces(text):
    return re.sub(r'([\u4e00-\u9fff]+)\{(.+?)\}', r'<ruby>\1<rt>\2</rt></ruby>', text)

def convert_caret(text):
    return re.sub(r'([\u4e00-\u9fff]+)\^(.+?)', r'<ruby>\1<rt>\2</rt></ruby>', text)

def convert_aozora(text):
    return re.sub(r'｜([\u4e00-\u9fff]+)《(.+?)》', r'<ruby>\1<rt>\2</rt></ruby>', text)

def is_kana(text):
    return re.fullmatch(r'[ぁ-んァ-ンー]+', text)

def contains_kanji(text):
    return re.search(r'[\u4e00-\u9fff]', text)

def convert_curly_to_ruby(text):
    return re.sub(r'([\u4e00-\u9fff]+)\{(.+?)\}', r'<ruby>\1<rt>\2</rt></ruby>', text)

def wrap_in_html(ruby_body):
    return f"""
    <html><head><meta charset="UTF-8"><style>
    body {{ font-size: 24px; line-height: 2; }}
    ruby rt {{ font-size: 0.5em; }}
    </style></head><body>{ruby_body}</body></html>
    """

def _katakana_to_hiragana(s):
    out = ''
    for ch in s:
        code = ord(ch)
        # Katakana block → subtract 0x60
        if 0x30A1 <= code <= 0x30F3:
            out += chr(code - 0x60)
        else:
            out += ch
    return out

def extract_kana_chunks(preedit, last_kana):
    kanji = re.compile(r'[\u4e00-\u9fff]')
    # 1) Segment preedit into runs of Kanji vs non-Kanji
    segs = []
    cur = preedit[0]
    is_k = bool(kanji.match(cur))
    for ch in preedit[1:]:
        if bool(kanji.match(ch)) == is_k:
            cur += ch
        else:
            segs.append((is_k, cur))
            cur = ch
            is_k = not is_k
    segs.append((is_k, cur))

    # 2) Build (isKanji, text, translit) list
    proc = []
    for is_k, txt in segs:
        if not is_k:
            proc.append((False, txt, _katakana_to_hiragana(txt)))
        else:
            proc.append((True, txt, None))

    # 3) Walk through, slicing last_kana at each non-Kanji translit
    chunks = []
    pos = 0
    for idx, (is_k, txt, translit) in enumerate(proc):
        if is_k:
            # Kanji run: take everything up to the next translit boundary
            if idx+1 < len(proc) and proc[idx+1][2]:
                b = proc[idx+1][2]
                j = last_kana.find(b, pos)
                chunk = last_kana[pos:j]
                pos = j
            else:
                chunk = last_kana[pos:]
                pos = len(last_kana)
            if chunk:
                chunks.append(chunk)
        else:
            # Non-Kanji: skip its translit length
            pos += len(translit)

    return chunks
