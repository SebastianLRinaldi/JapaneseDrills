import json
from pathlib import Path

master_path = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"



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

def load_master(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# Build kana -> (script, type) mapping
def build_kana_map(kana_struct):
    mapping = {}
    for script, all_kana in kana_struct.items():
        for type_name, vowels in all_kana["ALL KANA"].items():
            for vowel_dict in vowels.values():
                for k in vowel_dict:
                    mapping[k] = (script, type_name)
    return mapping

# Compute performance
def kana_performance(master_data, kana_map):
    kana_stats = master_data["kana"]
    group_perf = {}
    individual_perf = []

    for k, v in kana_stats.items():
        total = v.get("correct", 0) + v.get("wrong", 0)
        accuracy = v["correct"] / total if total else 0
        avg_time = v.get("avg_time")
        if avg_time is None:
            avg_time = float('inf')
        score = accuracy / (avg_time + 0.0001)

        individual_perf.append({
            "kana": k,
            "accuracy": accuracy,
            "avg_time": avg_time,
            "score": score
        })

        if k in kana_map:
            script, type_name = kana_map[k]
            group_key = f"{script} - {type_name}"
            if group_key not in group_perf:
                group_perf[group_key] = {"total_score": 0, "count": 0}
            group_perf[group_key]["total_score"] += score
            group_perf[group_key]["count"] += 1

    # Calculate average score per group
    for g in group_perf:
        group_perf[g]["avg_score"] = group_perf[g]["total_score"] / group_perf[g]["count"]

    best_individual = sorted(individual_perf, key=lambda x: x["score"], reverse=True)
    worst_individual = sorted(individual_perf, key=lambda x: x["score"])
    best_groups = sorted(group_perf.items(), key=lambda x: x[1]["avg_score"], reverse=True)
    worst_groups = sorted(group_perf.items(), key=lambda x: x[1]["avg_score"])

    return best_individual, worst_individual, best_groups, worst_groups

# Pretty print
def print_pretty(individual, groups, title="Performance"):
    print(f"\n=== {title} ===\n")
    print("Individual Kana:")
    print(f"{'Kana':<4} {'Accuracy':<8} {'Avg Time':<8} {'Score':<8}")
    for entry in individual[:10]:
        print(f"{entry['kana']:<4} {entry['accuracy']*100:6.1f}% {entry['avg_time']:6.2f}s {entry['score']:6.2f}")

    print("\nGroups:")
    print(f"{'Group':<25} {'Avg Score':<10}")
    for group, stats in groups[:5]:
        print(f"{group:<25} {stats['avg_score']:6.2f}")

# --- Example Usage ---
master_data = load_master(master_path)
# Insert your KANA structure here or import it
kana_map = build_kana_map(KANA)

best_kana, worst_kana, best_groups, worst_groups = kana_performance(master_data, kana_map)

print_pretty(best_kana, best_groups, "Best Kana & Groups")
print_pretty(worst_kana, worst_groups, "Worst Kana & Groups")
