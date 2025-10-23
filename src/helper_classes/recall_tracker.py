import json
from datetime import datetime, date
import time
import re
from pathlib import Path
from collections import Counter

# class RecallTracker:
#     def __init__(self):
#         # master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\master.json"
#         # sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
#         master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\master_test.json"
#         sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\session_test"
        
#         self.master_path = Path(master_path)
#         self.sessions_dir = Path(sessions_dir)
#         self.sessions_dir.mkdir(exist_ok=True)

#         # load or init master data
#         if self.master_path.exists():
#             with open(self.master_path, "r", encoding="utf-8") as f:
#                 self.master = json.load(f)
#         else:
#             self.master = {"stats": {"total_sessions": 0 , "total_recall_time": "00m:00s"}, "words": {}}

#         self.master_words = [w for w in self.master["words"]]

#     def process_session(self, text:str, session_duration:str):
#         # get words from QTextEdit, one per line
#         words = [w.strip() for w in text.split("\n") if w.strip()]
#         today = str(date.today())
#         now = datetime.now() 
        
#         # split words into new vs old
#         new_words = [w for w in words if w not in self.master["words"]]
#         old_words = [w for w in words if w in self.master["words"]]

#         ############## UPDATE MASTER ###################
#         # update per word in master
#         stats:dict = self.master.get("stats", {})
#         stats["total_sessions"] = stats.get("total_sessions", 0) + 1
#         stats["total_recall_time"] = self.update_session_time(session_duration)
#         last_recalled = f"{now.strftime(f'session({stats.get("total_sessions", 0)}) %Y-%m-%d')}"
        
#         word_counts = Counter(words)
#         for w, count in word_counts.items():
#             if w not in self.master["words"]:
#                 self.master["words"][w] = {"count": 0, "first_recalled": last_recalled, "last_recalled": None}
#             self.master["words"][w]["count"] += count
#             self.master["words"][w]["last_recalled"] = last_recalled

#         # update word order to be sorted by recall count lowest to highest
        
#         self.master["words"] = dict(sorted(self.master["words"].items(), key=lambda x: x[1]["count"]))
            
#         # update overall stats in master
#         all_words_resorted = list(self.master["words"].items())

#         least_recalled = {w: v["count"] for w, v in all_words_resorted[:20]}
#         most_recalled  = {w: v["count"] for w, v in all_words_resorted[:-20:-1]}
        
#         stats.update({
#             "total_words": len(all_words_resorted),
#             "total_recall_count": sum(word["count"] for word in self.master["words"].values()),
#             "last_session_date": today,
#             "least_recalled": least_recalled,  # first 20 (lowest counts)
#             "most_recalled": most_recalled, # last 20 (highest counts)
#         })

#         # save master
#         with open(self.master_path, "w", encoding="utf-8") as f:
#             json.dump(self.master, f, ensure_ascii=False, indent=2)

#         ############## UPDATE SESSION FOLDER ###################
#         # save session summary
#         session_data = {
#             "session_num": stats.get("total_sessions", 0),
#             "date": today,
#             "time":now.strftime('%I:%M%p'),
#             "session_duration":self.sum_durations([session_duration]),
#             "total_count": len(words),
#             "new_count": len(new_words),
#             "old_count": len(old_words),
#             "new_words": new_words,
#             "old_words": old_words,
#         }
        
#         filename = f"{now.strftime(f'session({stats.get("total_sessions", 0)})_%Y-%m-%d.json')}"
#         session_path = self.sessions_dir / filename
#         with open(session_path, "w", encoding="utf-8") as f:
#             json.dump(session_data, f, ensure_ascii=False, indent=2)

#         return session_data, self.master


#     def update_session_time(self, session_duration):
#         stats:dict = self.master.get("stats", {})
        
#         total_recall_time = stats.get("total_recall_time", "") 

#         return self.sum_durations([total_recall_time, session_duration])


#     def sum_durations(self, durations:list[str]):
#         total_seconds = 0

#         for duration in durations:
#             total_seconds += self.parse_duration(duration)

#         return self.format_duration(total_seconds)

#     def format_duration(self, total_seconds):
#         days, rem = divmod(total_seconds, 86400)
#         hrs, rem = divmod(rem, 3600)
#         mins, secs = divmod(rem, 60)

#         parts = []
#         if days > 0:
#             parts.append(f"{days}d")
#         if hrs > 0 or days > 0:  # show hours if any days or hours exist
#             parts.append(f"{hrs}h")
#         if mins > 0 or hrs > 0 or days > 0:  # show minutes if any larger units exist
#             parts.append(f"{mins}m")
#         parts.append(f"{secs}s")  # always show seconds

#         return ":".join(parts)

#     def parse_duration(self, duration):
#         # Matches optional D,H,M,S parts
#         pattern = r'(?:(\d+)d:)?(?:(\d+)h:)?(?:(\d+)m:)?(\d+)s'
#         match = re.fullmatch(pattern, duration)
#         if not match:
#             raise ValueError(f"Invalid duration format: {duration}")
        
#         days, hrs, mins, secs = match.groups(default='0')
#         total_seconds = int(days)*86400 + int(hrs)*3600 + int(mins)*60 + int(secs)
#         return total_seconds



class RecallTracker:
    def __init__(self):
        # master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\master_test.json"
        # sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data_test\session_test"
        master_path=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\master.json"
        sessions_dir=r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data\sessions"
        
        self.master_path = Path(master_path)
        self.sessions_dir = Path(sessions_dir)
        self.sessions_dir.mkdir(exist_ok=True)

        self.master = {}
        self.master_stats = {}
        self.master_words = {}
        self.init_mastery_file()

    def init_mastery_file(self):
        # load and init master data
        if self.master_path.exists():
            with open(self.master_path, "r", encoding="utf-8") as f:
                self.master = json.load(f)
        else:
            self.master = {"stats": {"total_sessions": 0 , "total_recall_time": "00m:00s"}, "words": {}}
            
        self.master_stats:dict = self.master.get("stats", {})
        self.master_words:dict = self.master.get("words", {})

    def process_session(self, session_text:str, session_duration:str):
        self.master_stats["total_sessions"] = self.master_stats.get("total_sessions", 0) + 1
        self.master_stats["total_recall_time"] = self.update_session_time(session_duration)
        untracked_words, tracked_words = self.process_session_words(session_text)
        self.add_session(session_duration, untracked_words, tracked_words)
        self.update_master()
        
    def process_session_words(self, session_text:str):
        now = datetime.now() 
        last_recalled = f"{now.strftime(f'session({self.master_stats.get("total_sessions", 0)}) %Y-%m-%d')}"

        # get words from QTextEdit, one per line
        session_words = [w.strip() for w in session_text.split("\n") if w.strip()]

        # split words into new vs old
        new_words = [w for w in session_words if w not in self.master_words]
        old_words = [w for w in session_words if w in self.master_words]
        
        word_counts = Counter(session_words)
        for w, count in word_counts.items():
            if w not in self.master_words:
                self.master_words[w] = {"count": 0, "first_recalled": last_recalled, "last_recalled": None}
            self.master_words[w]["count"] += count
            self.master_words[w]["last_recalled"] = last_recalled

        return new_words, old_words

    def add_session(self, session_duration, untracked_words, tracked_words):
        today = str(date.today())
        now = datetime.now() 
        ############## UPDATE SESSION FOLDER ###################
        # save session summary
        session_data = {
            "session_num": self.master_stats.get("total_sessions", 0),
            "date": today,
            "time":now.strftime('%I:%M%p'),
            "session_duration":self.sum_durations([session_duration]),
            "total_count": len(untracked_words) + len(tracked_words),
            "new_count": len(untracked_words),
            "old_count": len(tracked_words),
            "new_words": untracked_words,
            "old_words": tracked_words,
        }
        
        filename = f"{now.strftime(f'session({self.master_stats.get("total_sessions", 0)})_%Y-%m-%d.json')}"
        session_path = self.sessions_dir / filename
        
        self.save_json(session_data, session_path)

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
        
        self.master_stats.update({
            "total_words": len(all_words_resorted),
            "total_recall_count": sum(word["count"] for word in self.master_words.values()),
            "last_session_date": today,
            "least_recalled": least_recalled,  # first 20 (lowest counts)
            "most_recalled": most_recalled, # last 20 (highest counts)
        })

        
        self.save_json(self.master, self.master_path)

    def update_session_time(self, session_duration):
        stats:dict = self.master.get("stats", {})
        
        total_recall_time = stats.get("total_recall_time", "") 

        return self.sum_durations([total_recall_time, session_duration])

    def sum_durations(self, durations:list[str]):
        total_seconds = 0

        for duration in durations:
            total_seconds += self.parse_duration(duration)

        return self.format_duration(total_seconds)

    def format_duration(self, total_seconds):
        days, rem = divmod(total_seconds, 86400)
        hrs, rem = divmod(rem, 3600)
        mins, secs = divmod(rem, 60)

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hrs > 0 or days > 0:  # show hours if any days or hours exist
            parts.append(f"{hrs}h")
        if mins > 0 or hrs > 0 or days > 0:  # show minutes if any larger units exist
            parts.append(f"{mins}m")
        parts.append(f"{secs}s")  # always show seconds

        return ":".join(parts)

    def parse_duration(self, duration):
        # Matches optional D,H,M,S parts
        pattern = r'(?:(\d+)d:)?(?:(\d+)h:)?(?:(\d+)m:)?(\d+)s'
        match = re.fullmatch(pattern, duration)
        if not match:
            raise ValueError(f"Invalid duration format: {duration}")
        
        days, hrs, mins, secs = match.groups(default='0')
        total_seconds = int(days)*86400 + int(hrs)*3600 + int(mins)*60 + int(secs)
        return total_seconds

    def save_json(self, obj_data, obj_path):
        with open(obj_path, "w", encoding="utf-8") as f:
            json.dump(obj_data, f, ensure_ascii=False, indent=2)
