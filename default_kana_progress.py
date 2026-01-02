import json

KANA = {
    "HIRAGANA": {
        "ALL KANA": {
            "MAIN KANA": {
                "A": {"あ":"a","か":"ka","さ":"sa","た":"ta","な":"na","は":"ha","ま":"ma","や":"ya","ら":"ra","わ":"wa"},
                "I": {"い":"i","き":"ki","し":"shi","ち":"chi","に":"ni","ひ":"hi","み":"mi","り":"ri"},
                "U": {"う":"u","く":"ku","す":"su","つ":"tsu","ぬ":"nu","ふ":"fu","む":"mu","ゆ":"yu","る":"ru"},
                "E": {"え":"e","け":"ke","せ":"se","て":"te","ね":"ne","へ":"he","め":"me","れ":"re"},
                "O": {"お":"o","こ":"ko","そ":"so","と":"to","の":"no","ほ":"ho","も":"mo","よ":"yo","ろ":"ro","を":"wo"},
                "N": {"ん":"n"}
            },
            "DAKUTEN KANA": {
                "A": {"が":"ga","ざ":"za","だ":"da","ば":"ba","ぱ":"pa"},
                "I": {"ぎ":"gi","じ":"ji","ぢ":"ji","び":"bi","ぴ":"pi"},
                "U": {"ぐ":"gu","ず":"zu","づ":"zu","ぶ":"bu","ぷ":"pu"},
                "E": {"げ":"ge","ぜ":"ze","で":"de","べ":"be","ぺ":"pe"},
                "O": {"ご":"go","ぞ":"zo","ど":"do","ぼ":"bo","ぽ":"po"}
            },
            "COMBINATION KANA": {
                "A": {"きゃ":"kya","しゃ":"sha","ちゃ":"cha","にゃ":"nya","ひゃ":"hya","みゃ":"mya","りゃ":"rya","ぎゃ":"gya","じゃ":"ja","びゃ":"bya","ぴゃ":"pya"},
                "U": {"きゅ":"kyu","しゅ":"shu","ちゅ":"chu","にゅ":"nyu","ひゅ":"hyu","みゅ":"myu","りゅ":"ryu","ぎゅ":"gyu","じゅ":"ju","びゅ":"byu","ぴゅ":"pyu"},
                "O": {"きょ":"kyo","しょ":"sho","ちょ":"cho","にょ":"nyo","ひょ":"hyo","みょ":"myo","りょ":"ryo","ぎょ":"gyo","じょ":"jo","びょ":"byo","ぴょ":"pyo"}
            }
        }
    },
    "KATAKANA": {
        "ALL KANA": {
            "MAIN KANA": {
                "A": {"ア":"a","カ":"ka","サ":"sa","タ":"ta","ナ":"na","ハ":"ha","マ":"ma","ヤ":"ya","ラ":"ra","ワ":"wa"},
                "I": {"イ":"i","キ":"ki","シ":"shi","チ":"chi","ニ":"ni","ヒ":"hi","ミ":"mi","リ":"ri"},
                "U": {"ウ":"u","ク":"ku","ス":"su","ツ":"tsu","ヌ":"nu","フ":"fu","ム":"mu","ユ":"yu","ル":"ru"},
                "E": {"エ":"e","ケ":"ke","セ":"se","テ":"te","ネ":"ne","ヘ":"he","メ":"me","レ":"re"},
                "O": {"オ":"o","コ":"ko","ソ":"so","ト":"to","ノ":"no","ホ":"ho","モ":"mo","ヨ":"yo","ロ":"ro","ヲ":"wo"},
                "N": {"ン":"n"}
            },
            "DAKUTEN KANA": {
                "A": {"ガ":"ga","ザ":"za","ダ":"da","バ":"ba","パ":"pa"},
                "I": {"ギ":"gi","ジ":"ji","ヂ":"ji","ビ":"bi","ピ":"pi"},
                "U": {"グ":"gu","ズ":"zu","ヅ":"zu","ブ":"bu","プ":"pu"},
                "E": {"ゲ":"ge","ゼ":"ze","デ":"de","ベ":"be","ペ":"pe"},
                "O": {"ゴ":"go","ゾ":"zo","ド":"do","ボ":"bo","ポ":"po"}
            },
            "COMBINATION KANA": {
                "A": {"キャ":"kya","シャ":"sha","チャ":"cha","ニャ":"nya","ヒャ":"hya","ミャ":"mya","リャ":"rya","ギャ":"gya","ジャ":"ja","ビャ":"bya","ピャ":"pya"},
                "U": {"キュ":"kyu","シュ":"shu","チュ":"chu","ニュ":"nyu","ヒュ":"hyu","ミュ":"myu","リュ":"ryu","ギュ":"gyu","ジュ":"ju","ビュ":"byu","ピュ":"pyu"},
                "O": {"キョ":"kyo","ショ":"sho","チョ":"cho","ニョ":"nyo","ヒョ":"hyo","ミョ":"myo","リョ":"ryo","ギョ":"gyo","ジョ":"jo","ビョ":"byo","ピョ":"pyo"}
            }
        }
    }
}

progress = {}

for script_name, script_data in KANA.items():
    for category_name, category_data in script_data["ALL KANA"].items():
        for vowel, kana_map in category_data.items():
            for kana_char, romaji in kana_map.items():
                progress[kana_char] = {
                    "stats": {"correct": 0, "wrong": 0, "history": []},
                    "meta": {"script": script_name, "category": category_name, "vowel": vowel}
                }

# Save to JSON file if needed
with open("kana_mastery_progress.json", "w", encoding="utf-8") as f:
    json.dump(progress, f, ensure_ascii=False, indent=2)

print("Progress JSON generated for all kana!")
