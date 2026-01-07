import json
from collections import defaultdict
from pathlib import Path

# ------------------------
# CONFIG
# ------------------------

MASTER_PATH = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"
TOP_N_GLOBAL = 15
TOP_N_PER_GROUP = 15

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
# LOAD
# ------------------------

def load_master(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ------------------------
# KANA MAP
# ------------------------

def build_kana_map(kana_struct):
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
# SCORING
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
# COLLECT ALL KANA
# ------------------------

def collect_all_kana(master_data, kana_map):
    all_entries = []

    for kana, stats in master_data["kana"].items():
        if kana not in kana_map:
            continue

        perf = compute_score(stats)
        meta = kana_map[kana]

        all_entries.append({
            "kana": kana,
            "script": meta["script"],
            "type": meta["type"],
            "vowel": meta["vowel"],
            **perf
        })

    return all_entries

# ------------------------
# GLOBAL BEST / WORST
# ------------------------

def global_best_worst(all_entries):
    sorted_all = sorted(all_entries, key=lambda x: x["score"], reverse=True)
    return (
        sorted_all[:TOP_N_GLOBAL],
        sorted_all[-TOP_N_GLOBAL:]
    )

# ------------------------
# REGROUP
# ------------------------

def regroup_by_group(entries):
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for e in entries:
        grouped[e["script"]][e["type"]][e["vowel"]].append(e)

    for script in grouped:
        for type_name in grouped[script]:
            for vowel in grouped[script][type_name]:
                grouped[script][type_name][vowel] = sorted(
                    grouped[script][type_name][vowel],
                    key=lambda x: x["score"],
                    reverse=True
                )[:TOP_N_PER_GROUP]

    return grouped

# ------------------------
# PRINT
# ------------------------

def print_grouped(title, grouped):
    print(f"\n=== {title} ===")

    for script in grouped:
        print(f"\n{script}")
        for type_name in grouped[script]:
            print(f"  {type_name}")
            for vowel, entries in grouped[script][type_name].items():
                print(f"    Vowel {vowel}")
                for e in entries:
                    print(
                        f"      {e['kana']}  "
                        f"acc={e['accuracy']:.2f}  "
                        f"t={e['avg_time']:.2f}  "
                        f"s={e['score']:.4f}"
                    )

# ------------------------
# RUN
# ------------------------

master_data = load_master(MASTER_PATH)
kana_map = build_kana_map(KANA)

all_entries = collect_all_kana(master_data, kana_map)

best15, worst15 = global_best_worst(all_entries)

best_grouped = regroup_by_group(best15)
worst_grouped = regroup_by_group(worst15)

print_grouped("GLOBAL BEST 15 → GROUPED", best_grouped)
print_grouped("GLOBAL WORST 15 → GROUPED", worst_grouped)




# import json
# import sys
# from collections import defaultdict
# from pathlib import Path

# from PyQt6.QtWidgets import (
#     QApplication,
#     QMainWindow,
#     QTreeWidget,
#     QTreeWidgetItem,
#     QTabWidget,
# )
# from PyQt6.QtCore import Qt

# # ======================
# # CONFIG
# # ======================

# MASTER_PATH = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"
# TOP_N_GLOBAL = 15
# TOP_N_PER_GROUP = 15

# # ======================
# # KANA DATA (UNCHANGED)
# # ======================

# KANA = {
#     "HIRAGANA": {
#         "ALL KANA": {
#             "MAIN KANA": {
#                 "A": {"あ": "a", "か": "ka", "さ": "sa", "た": "ta", "な": "na", "は": "ha", "ま": "ma", "や": "ya", "ら": "ra", "わ": "wa"},
#                 "I": {"い": "i", "き": "ki", "し": "shi", "ち": "chi", "に": "ni", "ひ": "hi", "み": "mi", "り": "ri"},
#                 "U": {"う": "u", "く": "ku", "す": "su", "つ": "tsu", "ぬ": "nu", "ふ": "fu", "む": "mu", "ゆ": "yu", "る": "ru"},
#                 "E": {"え": "e", "け": "ke", "せ": "se", "て": "te", "ね": "ne", "へ": "he", "め": "me", "れ": "re"},
#                 "O": {"お": "o", "こ": "ko", "そ": "so", "と": "to", "の": "no", "ほ": "ho", "も": "mo", "よ": "yo", "ろ": "ro", "を": "wo"},
#                 "N": {"ん": "n"},
#             },
#             "DAKUTEN KANA": {
#                 "A": {"が": "ga", "ざ": "za", "だ": "da", "ば": "ba", "ぱ": "pa"},
#                 "I": {"ぎ": "gi", "じ": "ji", "ぢ": "ji", "び": "bi", "ぴ": "pi"},
#                 "U": {"ぐ": "gu", "ず": "zu", "づ": "zu", "ぶ": "bu", "ぷ": "pu"},
#                 "E": {"げ": "ge", "ぜ": "ze", "で": "de", "べ": "be", "ぺ": "pe"},
#                 "O": {"ご": "go", "ぞ": "zo", "ど": "do", "ぼ": "bo", "ぽ": "po"},
#             },
#             "COMBINATION KANA": {
#                 "A": {"きゃ": "kya", "しゃ": "sha", "ちゃ": "cha", "にゃ": "nya", "ひゃ": "hya", "みゃ": "mya", "りゃ": "rya", "ぎゃ": "gya", "じゃ": "ja", "びゃ": "bya", "ぴゃ": "pya"},
#                 "U": {"きゅ": "kyu", "しゅ": "shu", "ちゅ": "chu", "にゅ": "nyu", "ひゅ": "hyu", "みゅ": "myu", "りゅ": "ryu", "ぎゅ": "gyu", "じゅ": "ju", "びゅ": "byu", "ぴゅ": "pyu"},
#                 "O": {"きょ": "kyo", "しょ": "sho", "ちょ": "cho", "にょ": "nyo", "ひょ": "hyo", "みょ": "myo", "りょ": "ryo", "ぎょ": "gyo", "じょ": "jo", "びょ": "byo", "ぴょ": "pyo"},
#             },
#         }
#     },
#     "KATAKANA": {
#         "ALL KANA": {
#             "MAIN KANA": {
#                 "A": {"ア": "a", "カ": "ka", "サ": "sa", "タ": "ta", "ナ": "na", "ハ": "ha", "マ": "ma", "ヤ": "ya", "ラ": "ra", "ワ": "wa"},
#                 "I": {"イ": "i", "キ": "ki", "シ": "shi", "チ": "chi", "ニ": "ni", "ヒ": "hi", "ミ": "mi", "リ": "ri"},
#                 "U": {"ウ": "u", "ク": "ku", "ス": "su", "ツ": "tsu", "ヌ": "nu", "フ": "fu", "ム": "mu", "ユ": "yu", "ル": "ru"},
#                 "E": {"エ": "e", "ケ": "ke", "セ": "se", "テ": "te", "ネ": "ne", "ヘ": "he", "メ": "me", "レ": "re"},
#                 "O": {"オ": "o", "コ": "ko", "ソ": "so", "ト": "to", "ノ": "no", "ホ": "ho", "モ": "mo", "ヨ": "yo", "ロ": "ro", "ヲ": "wo"},
#                 "N": {"ン": "n"},
#             },
#             "DAKUTEN KANA": {
#                 "A": {"ガ": "ga", "ザ": "za", "ダ": "da", "バ": "ba", "パ": "pa"},
#                 "I": {"ギ": "gi", "ジ": "ji", "ヂ": "ji", "ビ": "bi", "ピ": "pi"},
#                 "U": {"グ": "gu", "ズ": "zu", "ヅ": "zu", "ブ": "bu", "プ": "pu"},
#                 "E": {"ゲ": "ge", "ゼ": "ze", "デ": "de", "ベ": "be", "ペ": "pe"},
#                 "O": {"ゴ": "go", "ゾ": "zo", "ド": "do", "ボ": "bo", "ポ": "po"},
#             },
#             "COMBINATION KANA": {
#                 "A": {"キャ": "kya", "シャ": "sha", "チャ": "cha", "ニャ": "nya", "ヒャ": "hya", "ミャ": "mya", "リャ": "rya", "ギャ": "gya", "ジャ": "ja", "ビャ": "bya", "ピャ": "pya"},
#                 "U": {"キュ": "kyu", "シュ": "shu", "チュ": "chu", "ニュ": "nyu", "ヒュ": "hyu", "ミュ": "myu", "リュ": "ryu", "ギュ": "gyu", "ジュ": "ju", "ビュ": "byu", "ピュ": "pyu"},
#                 "O": {"キョ": "kyo", "ショ": "sho", "チョ": "cho", "ニョ": "nyo", "ヒョ": "hyo", "ミョ": "myo", "リョ": "ryo", "ギョ": "gyo", "ジョ": "jo", "ビョ": "byo", "ピョ": "pyo"},
#             },
#         }
#     },
# }

# # ======================
# # DATA PIPELINE
# # ======================

# def load_master(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

# def build_kana_map(kana_struct):
#     mapping = {}
#     for script, script_data in kana_struct.items():
#         for type_name, vowel_groups in script_data["ALL KANA"].items():
#             for vowel, kana_dict in vowel_groups.items():
#                 for kana in kana_dict:
#                     mapping[kana] = {
#                         "script": script,
#                         "type": type_name,
#                         "vowel": vowel,
#                     }
#     return mapping

# def compute_score(stats):
#     correct = stats.get("correct", 0)
#     wrong = stats.get("wrong", 0)
#     total = correct + wrong

#     accuracy = correct / total if total else 0

#     avg_time = stats.get("avg_time")
#     if avg_time is None:
#         avg_time = float("inf")

#     return {
#         "accuracy": accuracy,
#         "avg_time": avg_time,
#         "score": accuracy / (avg_time + 1e-4),
#     }

# def collect_all_kana(master_data, kana_map):
#     out = []
#     for kana, stats in master_data["kana"].items():
#         if kana not in kana_map:
#             continue

#         perf = compute_score(stats)
#         meta = kana_map[kana]

#         out.append({
#             "kana": kana,
#             **meta,
#             **perf,
#         })
#     return out

# def global_best_worst(entries):
#     entries = sorted(entries, key=lambda x: x["score"], reverse=True)
#     return entries[:TOP_N_GLOBAL], entries[-TOP_N_GLOBAL:]

# def regroup_by_group(entries):
#     grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

#     for e in entries:
#         grouped[e["script"]][e["type"]][e["vowel"]].append(e)

#     return grouped

# # ======================
# # PYQT UI
# # ======================

# def populate_tree(tree, grouped_data):
#     tree.setHeaderLabels(["Item", "Accuracy", "Avg Time", "Score"])
#     tree.clear()

#     for script, types in grouped_data.items():
#         script_item = QTreeWidgetItem([script])
#         tree.addTopLevelItem(script_item)

#         for type_name, vowels in types.items():
#             type_item = QTreeWidgetItem([type_name])
#             script_item.addChild(type_item)

#             for vowel, entries in vowels.items():
#                 vowel_item = QTreeWidgetItem([f"Vowel {vowel}"])
#                 type_item.addChild(vowel_item)

#                 for e in entries:
#                     QTreeWidgetItem(
#                         vowel_item,
#                         [
#                             e["kana"],
#                             f"{e['accuracy']:.2f}",
#                             f"{e['avg_time']:.2f}",
#                             f"{e['score']:.4f}",
#                         ],
#                     )

#     tree.expandAll()

# class KanaPerformanceWindow(QMainWindow):
#     def __init__(self, best_grouped, worst_grouped):
#         super().__init__()

#         self.setWindowTitle("Kana Performance")
#         self.resize(900, 700)

#         tabs = QTabWidget()

#         best_tree = QTreeWidget()
#         worst_tree = QTreeWidget()

#         populate_tree(best_tree, best_grouped)
#         populate_tree(worst_tree, worst_grouped)

#         tabs.addTab(best_tree, "Best 15")
#         tabs.addTab(worst_tree, "Worst 15")

#         self.setCentralWidget(tabs)

# # ======================
# # MAIN
# # ======================

# if __name__ == "__main__":
#     master_data = load_master(MASTER_PATH)
#     kana_map = build_kana_map(KANA)

#     all_entries = collect_all_kana(master_data, kana_map)
#     best15, worst15 = global_best_worst(all_entries)

#     best_grouped = regroup_by_group(best15)
#     worst_grouped = regroup_by_group(worst15)

#     app = QApplication(sys.argv)
#     window = KanaPerformanceWindow(best_grouped, worst_grouped)
#     window.show()
#     sys.exit(app.exec())




import json
import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

MASTER_PATH = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"
TOP_N_GLOBAL = 15

"""
        if self.mode=="best":
            bg="#1abc9c"; fg="#fff"; border="2px solid #0e6655"
        elif self.mode=="worst":
            bg="#c0392b"; fg="#fff"; border="2px solid #641e16"
        else:
            bg="#1a1a1a"; fg="#666"; border="1px solid #111"
"""

# -------------------------
# Load and compute scores

# -------------------------
def load_master(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def compute_score(stats):
    correct = stats.get("correct",0)
    wrong = stats.get("wrong",0)
    total = correct+wrong
    accuracy = correct/total if total else 0
    avg_time = stats.get("avg_time") or float("inf")
    score = accuracy / (avg_time + 1e-4)
    return accuracy, avg_time, score

# -------------------------
# KANA CHART DATA
# Each row: main consonant, then combos
# Dakuten row follows under main
# -------------------------
# Vowels order
VOWELS = ["a","i","u","e","o"]

HIRAGANA_ROWS = [
    # Main
    ["あ","い","う","え","お"],
    ["か","き","く","け","こ","きゃ","きゅ","きょ"],
    ["さ","し","す","せ","そ","しゃ","しゅ","しょ"],
    ["た","ち","つ","て","と","ちゃ","ちゅ","ちょ"],
    ["な","に","ぬ","ね","の","にゃ","にゅ","にょ"],
    ["は","ひ","ふ","へ","ほ","ひゃ","ひゅ","ひょ","ふぁ","ふぃ"], # optional f combos
    ["ま","み","む","め","も","みゃ","みゅ","みょ"],
    ["や","","ゆ","","よ"],
    ["ら","り","る","れ","ろ","りゃ","りゅ","りょ"],
    ["わ","","","","を"],
    ["ん",""],

    # Dakuten
    ["が","ぎ","ぐ","げ","ご","ぎゃ","ぎゅ","ぎょ"],
    ["ざ","じ","ず","ぜ","ぞ","じゃ","じゅ","じょ"],
    ["だ","ぢ","づ","で","ど","ぢゃ","ぢゅ","ぢょ"],
    ["ば","び","ぶ","べ","ぼ","びゃ","びゅ","びょ"],
    ["ぱ","ぴ","ぷ","ぺ","ぽ","ぴゃ","ぴゅ","ぴょ"]
]

KATAKANA_ROWS = [
    ["ア","イ","ウ","エ","オ"],
    ["カ","キ","ク","ケ","コ","キャ","キュ","キョ"],
    ["サ","シ","ス","セ","ソ","シャ","シュ","ショ"],
    ["タ","チ","ツ","テ","ト","チャ","チュ","チョ"],
    ["ナ","ニ","ヌ","ネ","ノ","ニャ","ニュ","ニョ"],
    ["ハ","ヒ","フ","ヘ","ホ","ヒャ","ヒュ","ヒョ"],
    ["マ","ミ","ム","メ","モ","ミャ","ミュ","ミョ"],
    ["ヤ","","ユ","","ヨ"],
    ["ラ","リ","ル","レ","ロ","リャ","リュ","リョ"],
    ["ワ","","","","ヲ"],
    ["ン",""],

    # Dakuten
    ["ガ","ギ","グ","ゲ","ゴ","ギャ","ギュ","ギョ"],
    ["ザ","ジ","ズ","ゼ","ゾ","ジャ","ジュ","ジョ"],
    ["ダ","ヂ","ヅ","デ","ド","ヂャ","ヂュ","ヂョ"],
    ["バ","ビ","ブ","ベ","ボ","ビャ","ビュ","ビョ"],
    ["パ","ピ","プ","ペ","ポ","ピャ","ピュ","ピョ"]
]

FULL_CHARTS = [("Hiragana", HIRAGANA_ROWS), ("Katakana", KATAKANA_ROWS)]





# -------------------------
# KANA CELL
# -------------------------

# class KanaCell(QLabel):
#     def __init__(self, kana, data=None, mode="neutral"):
#         super().__init__(kana if kana else "")
#         self.kana = kana
#         self.data = data
#         self.mode = mode
#         self.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.setFixedSize(48, 48)  # larger fixed size
#         self.apply_style()
#         if data:
#             acc,t,score = data
#             self.setToolTip(f"{kana}\nAccuracy: {acc:.1%}\nAvg time: {t:.2f}s\nScore: {score:.4f}")

#     def apply_style(self):
#         if not self.kana:
#             self.setStyleSheet("background: transparent; border: none;")
#             return
#         if self.mode=="best":
#             bg="#1abc9c"; fg="#fff"; border="2px solid #0e6655"
#         elif self.mode=="worst":
#             bg="#c0392b"; fg="#fff"; border="2px solid #641e16"
#         else: 
#             bg="#1a1a1a"; fg="#666"; border="1px solid #111"
#         self.setStyleSheet(f"""
#             QLabel {{
#                 background-color: {bg};
#                 color: {fg};
#                 font-size: 14px;
#                 font-weight: bold;
#                 border: {border};
#             }}
#         """)




class KanaCell(QLabel):
    NEUTRAL_COLOR = QColor("#666666")  # text for score 0
    LOW_COLOR = QColor("#c0392b")      # text for low positive score
    HIGH_COLOR = QColor("#1abc9c")     # text for high score
    TEXT_LIGHT = QColor("#f5f5f5")          # soft white
    TEXT_DARK  = QColor("#1a1a1a")           # dark for contrast on light bg

    def __init__(self, kana, data=None, mode="neutral"):
        super().__init__(kana if kana else "")
        self.kana = kana
        self.data = data
        self.mode = mode  # "neutral", "best", "worst"
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFixedSize(48, 48)
        self.apply_style()
        if data:
            acc, t, score = data
            self.setToolTip(f"{kana}\nAccuracy: {acc:.1%}\nAvg time: {t:.2f}s\nScore: {score:.4f}")

    def apply_style(self):
        if not self.kana:
            self.setStyleSheet("background: transparent; border: none;")
            return

        # Background and border from mode
        if self.mode == "best":
            bg = "#1abc9c"
            border = "2px solid #0e6655"
            fg = self.TEXT_DARK
        elif self.mode == "worst":
            bg = "#c0392b"
            border = "2px solid #641e16"
            fg = self.TEXT_DARK
        else:
            bg = "#1a1a1a"
            border = "1px solid #111"

            # Text color based on score gradient
            if self.data:
                _, _, score = self.data
                if score <= 0:
                    fg = self.NEUTRAL_COLOR
                else:
                    t = min(score, 1.0)  # normalize for gradient
                    fg = self.interpolate_color(self.LOW_COLOR, self.HIGH_COLOR, t)
            else:
                fg = self.NEUTRAL_COLOR

        self.setStyleSheet(f"""
            QLabel {{
                background-color: {bg};
                color: {fg.name()};
                font-size: 14px;
                font-weight: bold;
                border: {border};
            }}
        """)

    @staticmethod
    def interpolate_color(c1: QColor, c2: QColor, t: float) -> QColor:
        r = int(c1.red() + (c2.red() - c1.red()) * t)
        g = int(c1.green() + (c2.green() - c1.green()) * t)
        b = int(c1.blue() + (c2.blue() - c1.blue()) * t)
        return QColor(r, g, b)







# class KanaCell(QLabel):
#     NEUTRAL_BG = QColor("#2e2e2e")   # neutral dark gray
#     LOW_BG     = QColor("#f08c7a")   # soft coral / muted orange
#     HIGH_BG    = QColor("#7fd1b9")   # pastel teal / soft green-blue
#     TEXT_LIGHT = "#f5f5f5"           # soft white
#     TEXT_DARK  = "#1a1a1a"           # dark for contrast on light bg

#     def __init__(self, kana, data=None, temp=None):
#         super().__init__(kana if kana else "")
#         self.kana = kana
#         self.data = data
#         self.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         self.setFixedSize(48, 48)
#         self.apply_style()
#         if data:
#             acc, t, score = data
#             self.setToolTip(f"{kana}\nAccuracy: {acc:.1%}\nAvg time: {t:.2f}s\nScore: {score:.4f}")

#     def apply_style(self):
#         if not self.kana:
#             self.setStyleSheet("background: transparent; border: none;")
#             return

#         # Determine background color based on score
#         if self.data:
#             _, _, score = self.data
#             if score <= 0:
#                 bg_color = self.NEUTRAL_BG
#             else:
#                 t = min(score, 1.0)  # normalize score for gradient
#                 bg_color = self.interpolate_color(self.LOW_BG, self.HIGH_BG, t)
#         else:
#             bg_color = self.NEUTRAL_BG

#         # Choose text color for readability based on bg brightness
#         if self.is_bright(bg_color):
#             fg_color = self.TEXT_DARK
#         else:
#             fg_color = self.TEXT_LIGHT

#         self.setStyleSheet(f"""
#             QLabel {{
#                 background-color: {bg_color.name()};
#                 color: {fg_color};
#                 font-size: 14px;
#                 font-weight: bold;
#                 border: 1px solid #111;
#             }}
#         """)

#     @staticmethod
#     def interpolate_color(c1: QColor, c2: QColor, t: float) -> QColor:
#         r = int(c1.red() + (c2.red() - c1.red()) * t)
#         g = int(c1.green() + (c2.green() - c1.green()) * t)
#         b = int(c1.blue() + (c2.blue() - c1.blue()) * t)
#         return QColor(r, g, b)

#     @staticmethod
#     def is_bright(color: QColor) -> bool:
#         # Compute perceived brightness (YIQ)
#         brightness = (color.red() * 299 + color.green() * 587 + color.blue() * 114) / 1000
#         return brightness > 128




# -------------------------
# KANA CHART WIDGET
# -------------------------
class KanaChart(QWidget):
    def __init__(self, kana_stats, highlight_set, chart_rows, mode):
        super().__init__()

        # Use a fixed-size inner widget for the grid
        grid_container = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)  # compact spacing
        grid_layout.setContentsMargins(0, 0, 0, 0)

        max_cols = max(len(row) for row in chart_rows)
        for r, row in enumerate(chart_rows):
            for c, kana in enumerate(row):
                if not kana:
                    continue
                data = kana_stats.get(kana)
                cell_mode = mode if kana in highlight_set else "neutral"
                cell = KanaCell(kana, data, cell_mode)
                grid_layout.addWidget(cell, r, c)

        grid_container.setLayout(grid_layout)

        # Fix the size of the container to prevent expansion
        total_width = max_cols * 48 + (max_cols - 1) * 2  # cell size + spacing
        total_height = len(chart_rows) * 48 + (len(chart_rows) - 1) * 2
        grid_container.setFixedSize(total_width, total_height)

        # Add the container to this widget (so you can place it in tabs)
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(grid_container)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

# -------------------------
# MAIN WINDOW
# -------------------------
class KanaChartWindow(QMainWindow):
    def __init__(self,kana_stats,best_set,worst_set):
        super().__init__()
        self.setWindowTitle("Kana Performance Chart")
        self.resize(800,700)
        tabs = QTabWidget()
        for name, chart_rows in FULL_CHARTS:
            tabs.addTab(KanaChart(kana_stats,best_set,chart_rows,"best"), f"{name} Best 15")
            tabs.addTab(KanaChart(kana_stats,worst_set,chart_rows,"worst"), f"{name} Worst 15")
        self.setCentralWidget(tabs)

# -------------------------
# RUN
# -------------------------
if __name__=="__main__":
    master = load_master(MASTER_PATH)
    kana_stats={}
    scored=[]
    for kana, stats in master["kana"].items():
        acc,t,score = compute_score(stats)
        kana_stats[kana]=(acc,t,score)
        scored.append((kana,score))
    print(f"SCORED: {scored}")
    scored.sort(key=lambda x:x[1],reverse=True)
    best_set={k for k,_ in scored[:TOP_N_GLOBAL]}
    worst_set={k for k,_ in scored[-TOP_N_GLOBAL:]}
    app=QApplication(sys.argv)
    window=KanaChartWindow(kana_stats,best_set,worst_set)
    window.show()
    sys.exit(app.exec())


