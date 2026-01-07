import json
from collections import defaultdict
from pathlib import Path

MASTER_PATH = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"
TOP_N = 5

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
                "A": {
                    "きゃ":"kya","しゃ":"sha","ちゃ":"cha","にゃ":"nya","ひゃ":"hya",
                    "みゃ":"mya","りゃ":"rya","ぎゃ":"gya","じゃ":"ja","びゃ":"bya","ぴゃ":"pya"
                },
                "U": {
                    "きゅ":"kyu","しゅ":"shu","ちゅ":"chu","にゅ":"nyu","ひゅ":"hyu",
                    "みゅ":"myu","りゅ":"ryu","ぎゅ":"gyu","じゅ":"ju","びゅ":"byu","ぴゅ":"pyu"
                },
                "O": {
                    "きょ":"kyo","しょ":"sho","ちょ":"cho","にょ":"nyo","ひょ":"hyo",
                    "みょ":"myo","りょ":"ryo","ぎょ":"gyo","じょ":"jo","びょ":"byo","ぴょ":"pyo"
                }
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
                "A": {
                    "キャ":"kya","シャ":"sha","チャ":"cha","ニャ":"nya","ヒャ":"hya",
                    "ミャ":"mya","リャ":"rya","ギャ":"gya","ジャ":"ja","ビャ":"bya","ピャ":"pya"
                },
                "U": {
                    "キュ":"kyu","シュ":"shu","チュ":"chu","ニュ":"nyu","ヒュ":"hyu",
                    "ミュ":"myu","リュ":"ryu","ギュ":"gyu","ジュ":"ju","ビュ":"byu","ピュ":"pyu"
                },
                "O": {
                    "キョ":"kyo","ショ":"sho","チョ":"cho","ニョ":"nyo","ヒョ":"hyo",
                    "ミョ":"myo","リョ":"ryo","ギョ":"gyo","ジョ":"jo","ビョ":"byo","ピョ":"pyo"
                }
            }
        }
    }
}



# ------------------------
# Load
# ------------------------

def load_master(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------------
# Build kana -> metadata map
# ------------------------

def build_kana_map(kana_struct):
    """
    kana -> {
        script: HIRAGANA / KATAKANA
        type: MAIN / DAKUTEN / COMBINATION
        vowel: A I U E O N
    }
    """
    mapping = {}

    for script, script_data in kana_struct.items():
        for type_name, vowel_groups in script_data["ALL KANA"].items():
            for vowel, kana_dict in vowel_groups.items():
                for kana in kana_dict:
                    mapping[kana] = {
                        "script": script,
                        "type": type_name,
                        "vowel": vowel
                    }
    return mapping

# ------------------------
# Score computation
# ------------------------

def compute_score(stats):
    correct = stats.get("correct", 0)
    wrong = stats.get("wrong", 0)
    total = correct + wrong

    accuracy = correct / total if total else 0

    avg_time = stats.get("avg_time")
    if avg_time is None:
        avg_time = float("inf")

    return {
        "accuracy": accuracy,
        "avg_time": avg_time,
        "score": accuracy / (avg_time + 1e-4)
    }

# ------------------------
# Grouped performance
# ------------------------

def grouped_kana_performance(master_data, kana_map):
    """
    result[script][type][vowel] = {
        "best": [...],
        "worst": [...]
    }
    """
    buckets = defaultdict(list)

    for kana, stats in master_data["kana"].items():
        if kana not in kana_map:
            continue

        meta = kana_map[kana]
        perf = compute_score(stats)

        buckets[
            meta["script"],
            meta["type"],
            meta["vowel"]
        ].append({
            "kana": kana,
            **perf
        })

    result = defaultdict(lambda: defaultdict(dict))

    for (script, type_name, vowel), entries in buckets.items():
        entries_sorted = sorted(entries, key=lambda x: x["score"], reverse=True)

        result[script][type_name][vowel] = {
            "best": entries_sorted[:TOP_N],
            "worst": entries_sorted[-TOP_N:]
        }

    return result

# ------------------------
# Print
# ------------------------

def print_grouped(result):
    for script in result:
        print(f"\n=== {script} ===")

        for type_name in result[script]:
            print(f"\n  -- {type_name} --")

            for vowel in result[script][type_name]:
                group = result[script][type_name][vowel]

                print(f"\n    Vowel {vowel}")
                print("      Best:")
                for e in group["best"]:
                    print(f"        {e['kana']}  acc={e['accuracy']:.2f}  t={e['avg_time']:.2f}  s={e['score']:.2f}")

                print("      Worst:")
                for e in group["worst"]:
                    print(f"        {e['kana']}  acc={e['accuracy']:.2f}  t={e['avg_time']:.2f}  s={e['score']:.2f}")

# ------------------------
# Run
# ------------------------

master_data = load_master(MASTER_PATH)
kana_map = build_kana_map(KANA)

grouped = grouped_kana_performance(master_data, kana_map)
print_grouped(grouped)
