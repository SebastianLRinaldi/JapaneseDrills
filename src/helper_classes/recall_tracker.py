import json
from datetime import datetime, date
import pprint
import time
import re
from pathlib import Path
from collections import Counter

from requests import session
from src.helper_classes import word_type
from src.helper_functions import sum_durations

# class RecallTracker:
#     def __init__(self):
#         master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\master_test.json"
#         sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\session_test"
#         # master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\master.json"
#         # sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
        
#         self.master_path = Path(master_path)
#         self.sessions_dir = Path(sessions_dir)
#         self.sessions_dir.mkdir(exist_ok=True)

#         self.master = {}
#         self.master_stats = {}
#         self.master_words = {}
#         self.init_mastery_file()

#     def get_stored_words(self):
#         return list(self.master_words.keys())

#     def init_mastery_file(self):
#         # load and init master data
#         if self.master_path.exists():
#             with open(self.master_path, "r", encoding="utf-8") as f:
#                 self.master = json.load(f)
#         else:
#             self.master = {"stats": {"total_sessions": 0 , "total_recall_time": "00m:00s"}, "words": {}}
            
#         self.master_stats:dict = self.master.get("stats", {})
#         self.master_words:dict = self.master.get("words", {})

#     def process_session(self, session_text:str, session_duration:str):
#         self.master_stats["total_sessions"] = self.master_stats.get("total_sessions", 0) + 1
#         self.master_stats["total_recall_time"] = self.update_session_time(session_duration)
#         curr_session_name, untracked_words, tracked_words = self.process_session_words(session_text)
#         self.update_performance_stats(curr_session_name, untracked_words, tracked_words)
#         self.add_session(session_duration, untracked_words, tracked_words)
#         self.update_master()
#         return untracked_words, tracked_words
        
#     def process_session_words(self, session_text:str):
#         now = datetime.now() 
#         curr_session_name = f"{now.strftime(f'session({self.master_stats.get("total_sessions", 0)}) %Y-%m-%d')}"

#         # get words from QTextEdit, one per line
#         session_words = [w.strip() for w in session_text.split("\n") if w.strip()]

#         # split words into new vs old
#         untracked_words = [w for w in session_words if w not in self.master_words]
#         tracked_words = [w for w in session_words if w in self.master_words]
        
#         word_counts = Counter(session_words)
#         for w, count in word_counts.items():
#             if w not in self.master_words:
#                 self.master_words[w] = {"count": 0, "first_recalled": curr_session_name, "last_recalled": None}
#             self.master_words[w]["count"] += count
#             self.master_words[w]["last_recalled"] = curr_session_name

#         return curr_session_name, untracked_words, tracked_words

#     def add_session(self, session_duration, untracked_words, tracked_words):
#         today = str(date.today())
#         now = datetime.now() 
#         ############## UPDATE SESSION FOLDER ###################
#         # save session summary
#         session_data = {
#             "session_num": self.master_stats.get("total_sessions", 0),
#             "date": today,
#             "time":now.strftime('%I:%M%p'),
#             "session_duration":sum_durations([session_duration]),
#             "total_count": len(untracked_words) + len(tracked_words),
#             "new_count": len(untracked_words),
#             "old_count": len(tracked_words),
#             "new_words": untracked_words,
#             "old_words": tracked_words,
#         }
        
#         filename = f"{now.strftime(f'session({self.master_stats.get("total_sessions", 0)})_%Y-%m-%d.json')}"
#         session_path = self.sessions_dir / filename
        
#         self.save_json(session_data, session_path)

#     def update_master(self):
#         today = str(date.today())
#         # update word order to be sorted by recall count lowest to highest
        
#         sorted_master_words = dict(sorted(self.master_words.items(), key=lambda x: x[1]["count"]))
#         self.master_words.clear()
#         self.master_words.update(sorted_master_words)
#         # update overall stats in master
#         all_words_resorted = list(self.master_words.items())

#         least_recalled = {w: v["count"] for w, v in all_words_resorted[:20]}
#         most_recalled  = {w: v["count"] for w, v in all_words_resorted[:-20:-1]}
#         # self. update_performance_stats()
#         self.master_stats.update({
#             "total_words": len(all_words_resorted),
#             "total_recall_count": sum(word["count"] for word in self.master_words.values()),
#             "last_session_date": today,
#             "least_recalled": least_recalled,  # first 20 (lowest counts)
#             "most_recalled": most_recalled, # last 20 (highest counts)
#         })

#         self.save_json(self.master, self.master_path)


#     def update_performance_stats(self, curr_session_name:str, untracked_words:list[str], tracked_words:list[str]):
#         """
#         best session unique words total
#         best session total words total

#         best_unq_total: {session_name: "name", unq_total:000}
#         best_total: {session_name: "name", total:000}

#         if curr_session is better > than saved session:
#             replace saved_session with curr_session (name:total)
        
#         """
#         curr_stats = {
#             "best_total_word_count": len(untracked_words) + len(tracked_words),
#             "best_new_word_count": len(untracked_words),
#             "best_old_word_count": len(tracked_words),
#         }

#         for key, curr_count in curr_stats.items():
#             stat = self.master_stats.setdefault(key, {"count": 0, "session": ""})
#             if curr_count > stat.get("count", 0):
#                 stat["count"] = curr_count
#                 stat["session"] = curr_session_name

#         self.save_json(self.master, self.master_path)

    
#     def update_session_time(self, session_duration):
#         stats:dict = self.master.get("stats", {})
        
#         total_recall_time = stats.get("total_recall_time", "") 

#         return sum_durations([total_recall_time, session_duration])


#     def save_json(self, obj_data, obj_path):
#         with open(obj_path, "w", encoding="utf-8") as f:
#             json.dump(obj_data, f, ensure_ascii=False, indent=2)

















class RecallTracker:
    def __init__(self):
        master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\master_test.json"
        sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\session_test"
        # master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\master.json"
        # sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
        
        self.master_path = Path(master_path)
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)

        self.master = {}
        self.master_stats = {}
        self.master_words = {}
        self.init_mastery_file()

        self.current_session_data = {}
        self.current_session_path = ""
        self.current_session_name = ""

    def clear(self):
        self.current_session_data = {}
        self.current_session_path = ""
        self.current_session_name = ""
        self.init_mastery_file()
        
    
    def get_stored_words(self):
        return list(self.master_words.keys())

    def init_mastery_file(self):
        # load and init master data
        if self.master_path.exists():
            with open(self.master_path, "r", encoding="utf-8") as f:
                self.master = json.load(f)
        else:
            self.master = {"stats": {"total_sessions": 0 , "total_recall_time": "00m:00s"}, "words": {}}
            
        self.master_stats:dict = self.master.get("stats", {})
        self.master_words:dict = self.master.get("words", {})


    def add_event_to_session(self, timestamp:int, word:str):
        if word in self.master_words:
            word_type = "old"
        else:
            word_type = "new"
        event = { "timestamp": timestamp, "word": word, "type": word_type }
        print(event)
        if self.current_session_data:
            self.current_session_data["events"].append(event)
            # pprint.pprint(self.current_session_data)
        # self.save_json(self.current_session_data, self.current_session_path)

    def remove_event_from_session(self, word:str):
        if self.current_session_data:
            self.current_session_data["events"] = [
                event for event in self.current_session_data["events"]
                if event["word"] != word
            ]

    def sort_session_words(self):
        new_words = [event["word"] for event in self.current_session_data["events"] if event["type"] == "new"]
        old_words = [event["word"] for event in self.current_session_data["events"] if event["type"] == "old"]
        return old_words, new_words

    def get_session_word_type_count(self):
        new_count = sum(1 for event in self.current_session_data["events"] if event["type"] == "new")
        old_count = sum(1 for event in self.current_session_data["events"] if event["type"] == "old")
        return old_count, new_count

    def make_blank_session(self):
        if not self.current_session_path:
            today = str(date.today())
            current_session_num = self.master_stats.get("total_sessions", 0) + 1
            
            ############## UPDATE SESSION FOLDER ###################
            # save session summary
            self.current_session_data = {
                "session_num": current_session_num,
                "date": today,
                "time": "",
                "session_duration": 0,
                "total_count":0,
                "new_count": 0,
                "old_count": 0,
                "new_words":[],
                "old_words":[],
                "events": [
                ]
            }
            
            filename = f"{f'session({current_session_num})_{today}.json'}"
            self.current_session_path = self.sessions_dir / filename
            self.current_session_name = Path(self.current_session_path).stem.replace("_", " ")
            
            self.save_json(self.current_session_data, self.current_session_path)

    def process_session(self, session_duration:str):
        self.master_stats["total_sessions"] = self.master_stats.get("total_sessions", 0) + 1
        self.master_stats["total_recall_time"] = self.update_session_time(session_duration)
        self.process_session_words()
        self.update_performance_stats()
        self.update_session(session_duration)
        self.update_master()
        
    def process_session_words(self):

        session_words = [event["word"] for event in self.current_session_data["events"]]
        
        word_counts = Counter(session_words)
        for word, count in word_counts.items():
            if word not in self.master_words:
                self.master_words[word] = {"count": 0, "first_recalled": self.current_session_name, "last_recalled": None}
            self.master_words[word]["count"] += count
            self.master_words[word]["last_recalled"] = self.current_session_name

    def update_session(self, session_duration):
        today = str(date.today())
        now = datetime.now() 

        old_count, new_count = self.get_session_word_type_count()
        old_words, new_words = self.sort_session_words()

        print(f"OLD: {old_count}={old_words}\nNEW: {new_count}={new_words}, ")
        
        self.current_session_data.update({
            "session_num": self.master_stats.get("total_sessions", 0),
            "date": today,
            "time":now.strftime('%I:%M%p'),
            "session_duration":sum_durations([session_duration]),
            "total_count": old_count + new_count,
            "new_count": new_count,
            "old_count": old_count,
            "new_words": new_words,
            "old_words": old_words,
        })
        self.save_json(self.current_session_data, self.current_session_path )

    def update_master(self):
        today = str(date.today())
        # update word order to be sorted by recall count lowest to highest
        
        sorted_master_words = dict(sorted(self.master_words.items(), key=lambda x: x[1]["count"]))
        self.master_words.clear()
        self.master_words.update(sorted_master_words)
        # update overall stats in master
        all_words_resorted = list(self.master_words.items())

        least_recalled = {w: v["count"] for w, v in all_words_resorted[:20]}
        most_recalled  = {w: v["count"] for w, v in all_words_resorted[:-20:-1]}
        # self. update_performance_stats()
        self.master_stats.update({
            "total_words": len(all_words_resorted),
            "total_recall_count": sum(word["count"] for word in self.master_words.values()),
            "last_session_date": today,
            "least_recalled": least_recalled,  # first 20 (lowest counts)
            "most_recalled": most_recalled, # last 20 (highest counts)
        })

        self.save_json(self.master, self.master_path)


    def update_performance_stats(self):
        """
        best session unique words total
        best session total words total

        best_unq_total: {session_name: "name", unq_total:000}
        best_total: {session_name: "name", total:000}

        if curr_session is better > than saved session:
            replace saved_session with curr_session (name:total)
        
        """
        old_count, new_count = self.get_session_word_type_count()
        
        curr_stats = {
            "best_total_word_count": new_count + old_count,
            "best_new_word_count": new_count,
            "best_old_word_count": old_count,
        }

        for key, curr_count in curr_stats.items():
            stat = self.master_stats.setdefault(key, {"count": 0, "session": ""})
            if curr_count > stat.get("count", 0):
                stat["count"] = curr_count
                stat["session"] = self.current_session_name

        self.save_json(self.master, self.master_path)

    
    def update_session_time(self, session_duration):
        stats:dict = self.master.get("stats", {})
        
        total_recall_time = stats.get("total_recall_time", "") 

        return sum_durations([total_recall_time, session_duration])


    def save_json(self, obj_data, obj_path):
        with open(obj_path, "w", encoding="utf-8") as f:
            json.dump(obj_data, f, ensure_ascii=False, indent=2)
