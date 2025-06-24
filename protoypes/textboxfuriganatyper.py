import re

import re

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





print(extract_kana_chunks("日本語", "にほんご"))
print(extract_kana_chunks("食べます", "たべます"))
print(extract_kana_chunks("真っ直ぐ", "まっすぐ"))
print(extract_kana_chunks("お店", "おみせ"))
print(extract_kana_chunks("東京タワー", "とうきょうたわー"))

print(f"chunks: {extract_kana_chunks('間', 'あいだ')} | expected: ['あいだ']")
print(f"chunks: {extract_kana_chunks('時間割', 'じかんわり')} | expected: ['じかんわり']")
print(f"chunks: {extract_kana_chunks('食べます', 'たべます')} | expected: ['た']")
print(f"chunks: {extract_kana_chunks('日本語', 'にほんご')} | expected: ['にほんご']")
print(f"chunks: {extract_kana_chunks('真っ直ぐ', 'まっすぐ')} | expected: ['ま','す']")
print(f"chunks: {extract_kana_chunks('東京タワー', 'とうきょうたわー')} | expected: ['とうきょう']")
print(f"chunks: {extract_kana_chunks('ありがとう', 'ありがとう')} | expected: []")
print(f"chunks: {extract_kana_chunks('行行行', 'いきいきいき')} | expected: ['いき', 'いき', 'いき']")
print(f"chunks: {extract_kana_chunks('今日', 'きょう')} | expected: ['きょう']")
# print(f"chunks: {extract_kana_chunks('', '')} | expected: []")
