from ast import Dict
import json
from datetime import datetime, date
import pprint
import time
import re
from pathlib import Path
from collections import Counter

from requests import session
from src.globals.global_signals import global_signal_manager
from src.helper_classes import word_type
from src.helper_functions import sum_durations_w_format
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

"""

{
  "stats": {
    "total_sessions": 0,
    "total_recall_time": "",
    "total_recall_count": 0,
    "last_session_date": "",
    "least_recalled": {},
    "most_recalled": {},
    "best_correct_kana_count": {
      "count": 0,
      "session": ""
    }

  },
  "kana": {
    "あ": {
      "stats": {
        "correct": 1,
        "wrong": 0,
        "history": [
          1
        ]
      },
      "meta": {
        "script": "HIRAGANA",
        "category": "MAIN KANA",
        "vowel": "A"
      }
    },
    "か": {
      "stats": {
        "correct": 1,
        "wrong": 0,
        "history": [
          1
        ]
      },
      "meta": {
        "script": "HIRAGANA",
        "category": "MAIN KANA",
        "vowel": "A"
      }
    },

"""

class KanaRecallTracker:
    def __init__(self):
        master_path=r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"
        sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_sessions"
        
        self.master_path = Path(master_path)
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)

        self.master = {}
        self.master_stats = {}
        self.master_kana = {}

        self.current_session_data = {}
        self.current_session_path = ""
        self.current_session_name = ""

                
        self.init_master()

        
        
    def load_json(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_json(self, filename, obj):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            
    def init_kana_dict(self):
        kana_dict = {}
        for script in KANA.values():
            for all_kana in script.values():
                for category in all_kana.values():
                    for vowel_group in category.values():
                        for kana in vowel_group.keys():
                            kana_dict[kana] = {
                                "correct": 0,
                                "wrong": 0,
                                "avg_time": None,
                                "best_time":None
                            }
        return kana_dict

    def init_master(self):
        path = Path(self.master_path)

        if path.exists():
            self.master = self.load_json(self.master_path)

        else:
            self.master = {
                "stats": {
                    "total_sessions": 0,
                    "total_recall_time": 0,
                    "total_recall_count": 0,
                },
                "kana":self.init_kana_dict()
            }
            
            self.save_json(self.master_path, self.master)

        self.master_stats = self.master["stats"]
        self.master_kana = self.master["kana"]

    def finalize_master_from_session(self, session_duration):
        total_correct = 0

        # Iterate through all events in the session
        for event in self.current_session_data["events"]:
            kana = event["kana"]
            correct = event["correct"]
            elapsed_time = event["elapsed_time"] if correct else None

            k = self.master_kana[kana]

            if correct:
                # Increment correct count
                k["correct"] += 1
                total_correct += 1
                # Update avg_time incrementally
                if k["avg_time"] is None:
                    k["avg_time"] = elapsed_time
                else:
                    k["avg_time"] = (k["avg_time"] * (k["correct"] - 1) + elapsed_time) / k["correct"]
                # Update best_time
                if k["best_time"] is None or elapsed_time < k["best_time"]:
                    k["best_time"] = elapsed_time
            else:
                # Increment wrong count
                k["wrong"] += 1

        # Update master session stats
        stats = self.master_stats
        stats["total_sessions"] += 1
        stats["total_recall_time"] = sum_durations_w_format([stats["total_recall_time"], session_duration])
        stats["total_recall_count"] += total_correct

        # Save master
        self.save_json(self.master_path, self.master)

    def init_new_session(self, script_sel, category_sel, vowels):
        today = str(date.today())
        now = datetime.now() 
        current_session_num = self.master_stats.get("total_sessions", 0) + 1
        
        ############## UPDATE SESSION FOLDER ###################
        # save session summary
        self.current_session_data = {
            "session_num": current_session_num,
            "date": today,
            "time":now.strftime('%I:%M%p'),
            "summary": {
                "script":script_sel,
                "category":category_sel,
                "vowels":vowels,
                "session_duration": 0,
                "total_count":0,
                "correct_count": 0,
                "wrong_count": 0
            },
            "events": [
            ]
        }
        
        filename = f"{f'kana_session({current_session_num})_{today}.json'}"
        self.current_session_path = self.sessions_dir / filename
        self.current_session_name = Path(self.current_session_path).stem.replace("_", " ")
        
        self.save_json(self.current_session_path, self.current_session_data)

    def add_event_to_session(self, timestamp:int, elapsed_time:float, kana_pair, answer:str):
        summary = self.current_session_data["summary"]
        kana, eng = kana_pair
        if eng == answer:
            correct = True
            summary["correct_count"] += 1 
        else:
            correct = False
            summary["wrong_count"] += 1 
        summary["total_count"] += 1 
        event = {"timestamp": timestamp, "elapsed_time":elapsed_time, "kana": kana, "ans": answer, "correct":correct}
        if self.current_session_data:
            self.current_session_data["events"].append(event)
            
        self.save_json(self.current_session_path, self.current_session_data)

    def finalize_session(self, session_duration):
        summary = self.current_session_data["summary"]
        summary["session_duration"] = sum_durations_w_format([summary["session_duration"], session_duration])
        self.save_json(self.current_session_path, self.current_session_data)