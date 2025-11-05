from fugashi import Tagger
from furigana.furigana import split_okurigana

def katakana_to_hiragana(katakana):
    return ''.join(chr(ord(c)-0x60) if 'ァ' <= c <= 'ン' else c for c in katakana)

# word = "真っ直ぐ"
# hiragana = "まっすぐ"

# word = "図書館"
# hiragana = "としょかん"

# word = "お願い"
# hiragana = "おねかい"

# word = "お菓子"
# hiragana = "おかし"

# word = "昨日お菓子を食べました"

word = input("")

tagger = Tagger()
"""
# Analyze the word
# for token in tagger(word):
#     print(f"TOKEN: {token.surface}, {token.feature.kana}")
# """

# kana_readings = [token.feature.kana for token in tagger(word)]
# katakana = "".join(kana_readings)
# print(f"katakana={katakana}")
    
# hiragana = katakana_to_hiragana(katakana)
# print(f"hiragana={hiragana}")  # おかし

# split_word_obj = split_okurigana(word, hiragana)
# print(f"{list(split_word_obj)}")

kana_readings = [token.feature.kana for token in tagger(word)]
surface_readings = [token.surface for token in tagger(word)]
print(f"kanas={kana_readings}")
print(f"surface={surface_readings}")

katakana = "".join(kana_readings)
print(f"katakana={katakana}")

zipped_readings = zip(surface_readings, kana_readings)
furigana_sentence = []

print("\n ++++")
for reading in zipped_readings:
    surface, kana = reading
    print(f"surface={surface} | kana={kana}")
    hiragana = katakana_to_hiragana(kana)
    print(f"hiragana={hiragana}")

    split_word_obj = split_okurigana(surface, hiragana)
    print(f"{list(split_word_obj)}")
        


# print(furigana_sentence)