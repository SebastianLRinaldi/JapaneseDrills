"""
Test dashboards
"""
# import matplotlib.pyplot as plt
# plt.rcParams['font.family'] = 'MS Gothic'
# sessions = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
# words_recalled = [100, 120, 130, 140, 125, 135, 146, 110, 120, 115, 130]  # example data

# plt.plot(sessions, words_recalled, marker='o')
# plt.title("Words Recalled Per Session")
# plt.xlabel("Session")
# plt.ylabel("Words Recalled")
# plt.grid(True)
# plt.show()





# most_recalled = {"聞く": 12, "木曜日": 12, "本": 11, "先週": 11}
# least_recalled = {"全然": 1, "お願い": 1, "押す": 1}

# plt.figure(figsize=(10,4))

# plt.subplot(1,2,1)
# plt.bar(most_recalled.keys(), most_recalled.values(), color='green')
# plt.title("Most Recalled Words")
# plt.xticks(rotation=45)

# plt.subplot(1,2,2)
# plt.bar(least_recalled.keys(), least_recalled.values(), color='red')
# plt.title("Least Recalled Words")
# plt.xticks(rotation=45)

# plt.tight_layout()
# plt.show()




# import numpy as np

# recall_counts = [1,1,1,1,2,2,3,3,4,5,5,6,7,7,7]  # simplified example

# plt.hist(recall_counts, bins=np.arange(1, max(recall_counts)+2)-0.5, color='skyblue', edgecolor='black')
# plt.title("Distribution of Word Recall Counts")
# plt.xlabel("Number of Times Word Recalled")
# plt.ylabel("Number of Words")
# plt.show()


# cumulative_words = [20, 45, 70, 90, 120, 145, 180, 200, 220, 240, 254]  # example

# plt.plot(sessions, cumulative_words, marker='o', linestyle='-')
# plt.title("Cumulative Words Learned Over Sessions")
# plt.xlabel("Session")
# plt.ylabel("Total Words Learned")
# plt.grid(True)
# plt.show()



# import seaborn as sns
# import pandas as pd

# data = pd.DataFrame({
#     "word": ["聞く","木曜日","全然","お願い"],
#     "session1": [1,0,1,1],
#     "session2": [1,0,0,0],
#     "session3": [1,1,0,0],
#     "session4": [1,1,0,0]
# })

# sns.heatmap(data.set_index("word"), annot=True, cmap="YlGnBu")
# plt.title("Word Recall Across Sessions")
# plt.xlabel("Session")
# plt.show()



# import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
# import numpy as np

# # ----------------------------
# # Example Data (replace with your actual master.json data)
# # ----------------------------
# sessions = list(range(1, 12))  # 11 sessions
# words_recalled = [100, 120, 130, 140, 125, 135, 146, 110, 120, 115, 130]
# duration_minutes = [25, 30, 35, 28, 32, 40, 45, 20, 25, 30, 35]
# cumulative_words = np.cumsum([20, 25, 25, 20, 30, 25, 35, 20, 20, 20, 14])
# most_recalled = {"聞く": 12, "木曜日": 12, "本": 11, "先週": 11}
# least_recalled = {"全然": 1, "お願い": 1, "押す": 1}

# # Heatmap example (words x sessions)
# words = ["聞く","木曜日","全然","お願い"]
# heatmap_data = pd.DataFrame({
#     "word": words,
#     "session1": [1,0,1,1],
#     "session2": [1,0,0,0],
#     "session3": [1,1,0,0],
#     "session4": [1,1,0,0],
#     "session5": [1,1,0,0],
#     "session6": [1,1,1,0],
#     "session7": [1,1,1,0],
#     "session8": [1,1,0,0],
#     "session9": [1,1,0,0],
#     "session10": [1,1,0,0],
#     "session11": [1,1,0,0]
# })
# heatmap_data.set_index("word", inplace=True)

# best_metrics = {"Total Words": 146, "New Words": 99, "Old Words": 138}

# # ----------------------------
# # Create the dashboard figure
# # ----------------------------
# fig = plt.figure(constrained_layout=True, figsize=(18, 12))
# gs = fig.add_gridspec(3, 3)

# # Session Words Recalled
# ax1 = fig.add_subplot(gs[0, 0])
# ax1.plot(sessions, words_recalled, marker='o')
# ax1.set_title("Words Recalled Per Session")
# ax1.set_xlabel("Session")
# ax1.set_ylabel("Words Recalled")
# ax1.grid(True)

# # Study Duration
# ax2 = fig.add_subplot(gs[0, 1])
# ax2.bar(sessions, duration_minutes, color='orange')
# ax2.set_title("Study Time Per Session")
# ax2.set_xlabel("Session")
# ax2.set_ylabel("Minutes")

# # Cumulative Words Learned
# ax3 = fig.add_subplot(gs[0, 2])
# ax3.plot(sessions, cumulative_words, marker='o', linestyle='-')
# ax3.set_title("Cumulative Words Learned")
# ax3.set_xlabel("Session")
# ax3.set_ylabel("Total Words")
# ax3.grid(True)

# # Most & Least Recalled Words
# ax4 = fig.add_subplot(gs[1, 0])
# ax4.bar(most_recalled.keys(), most_recalled.values(), color='green', label='Most Recalled')
# ax4.bar(least_recalled.keys(), least_recalled.values(), color='red', label='Least Recalled')
# ax4.set_title("Word Recall Highlights")
# ax4.legend()
# ax4.set_xticklabels(list(most_recalled.keys()) + list(least_recalled.keys()), rotation=45)

# # Recall Heatmap
# ax5 = fig.add_subplot(gs[1, 1])
# sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax5)
# ax5.set_title("Word Recall Across Sessions")
# ax5.set_xlabel("Session")
# ax5.set_ylabel("Word")

# # Best Session Metrics
# ax6 = fig.add_subplot(gs[1, 2])
# ax6.barh(list(best_metrics.keys()), list(best_metrics.values()), color=['blue','green','purple'])
# ax6.set_title("Best Session Metrics")

# # Distribution of Word Recall Counts
# ax7 = fig.add_subplot(gs[2, :])
# recall_counts = [1,1,1,1,2,2,3,3,4,5,5,6,7,7,7]
# ax7.hist(recall_counts, bins=np.arange(1, max(recall_counts)+2)-0.5, color='skyblue', edgecolor='black')
# ax7.set_title("Distribution of Word Recall Counts")
# ax7.set_xlabel("Times Word Recalled")
# ax7.set_ylabel("Number of Words")

# plt.show()



"""
IDEAL BOARD LOOK
"""
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# ------------------------------------------------------------------
# 🔹 Paths
# ------------------------------------------------------------------
base_path = r"F:\_Small\344 School Python\JapaneseDrills\free_recall_data"
master_path = os.path.join(base_path, "master.json")
sessions_dir = os.path.join(base_path, "sessions")

# ------------------------------------------------------------------
# 🔹 Load master.json
# ------------------------------------------------------------------
with open(master_path, "r", encoding="utf-8") as f:
    master = json.load(f)

stats = master["stats"]
words_data = master["words"]
# print(words_data.keys())
# exit()
# ------------------------------------------------------------------
# 🔹 Extract summary stats
# ------------------------------------------------------------------
total_sessions = stats.get("total_sessions", 0)
total_recall_time = stats.get("total_recall_time", "")
total_words = stats.get("total_words", 0)
total_recall_count = stats.get("total_recall_count", 0)
most_recalled = stats.get("most_recalled", {})
least_recalled = stats.get("least_recalled", {})

best_metrics = {
    "Best Total Word Count": stats["best_total_word_count"]["count"],
    "Best New Word Count": stats["best_new_word_count"]["count"],
    "Best Old Word Count": stats["best_old_word_count"]["count"]
}

# ------------------------------------------------------------------
# 🔹 Create word-level DataFrame
# ------------------------------------------------------------------
df_words = pd.DataFrame([
    {"Word": w, **info} for w, info in words_data.items()
])
df_words["count"] = df_words["count"].astype(int)
df_words = df_words.sort_values("count", ascending=False)

# ------------------------------------------------------------------
# 🔹 Load all session files
# ------------------------------------------------------------------
session_files = sorted(
    [f for f in os.listdir(sessions_dir) if f.endswith(".json")],
    key=lambda x: int(x.split("(")[1].split(")")[0])
)

session_nums = []
session_total_words = []
session_new_words = []
session_old_words = []
session_durations = []

for file in session_files:
    path = os.path.join(sessions_dir, file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    session_num = data.get("session_num", len(session_nums) + 1)
    session_nums.append(session_num)

    if "events" in data:  # new structure
        total = len(data["events"])
        new = sum(1 for e in data["events"] if e["type"] == "new")
        old = total - new
        session_total_words.append(total)
        session_new_words.append(new)
        session_old_words.append(old)
    else:  # old structure
        new = len(data.get("new_words", []))
        old = len(data.get("old_words", []))
        total = new + old
        session_total_words.append(total)
        session_new_words.append(new)
        session_old_words.append(old)

    # Duration fallback (if available)
    duration = data.get("duration_sec", 0)
    session_durations.append(duration / 60.0)

df_sessions = pd.DataFrame({
    "Session": session_nums,
    "TotalWords": session_total_words,
    "NewWords": session_new_words,
    "OldWords": session_old_words,
    "Duration(min)": session_durations,
})

# ------------------------------------------------------------------
# 🔹 Build the visualization dashboard
# ------------------------------------------------------------------
fig = plt.figure(constrained_layout=True, figsize=(18, 12))
gs = fig.add_gridspec(3, 3)

# 1️⃣ Words per session
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df_sessions["Session"], df_sessions["TotalWords"], marker='o', color='blue', label='Total')
ax1.plot(df_sessions["Session"], df_sessions["NewWords"], marker='o', color='red', label='New')
ax1.plot(df_sessions["Session"], df_sessions["OldWords"], marker='o', color='gray', label='Old')
ax1.set_title("Words per Session")
ax1.set_xlabel("Session")
ax1.set_ylabel("Count")
ax1.legend()
ax1.grid(True)

# 2️⃣ Session Duration
ax2 = fig.add_subplot(gs[0, 1])
ax2.bar(df_sessions["Session"], df_sessions["Duration(min)"], color='orange')
ax2.set_title("Session Duration (minutes)")
ax2.set_xlabel("Session")
ax2.set_ylabel("Duration")

# 3️⃣ Cumulative Progress
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot(df_sessions["Session"], np.cumsum(df_sessions["NewWords"]), marker='o', label='Cumulative New')
ax3.plot(df_sessions["Session"], np.cumsum(df_sessions["OldWords"]), marker='o', label='Cumulative Old')
ax3.plot(df_sessions["Session"], np.cumsum(df_sessions["TotalWords"]), marker='o', label='Total')
ax3.legend()
ax3.set_title("Cumulative Learning Progress")
ax3.set_xlabel("Session")
ax3.set_ylabel("Cumulative Word Count")
ax3.grid(True)

# 4️⃣ Most & Least Recalled Words
ax4 = fig.add_subplot(gs[1, 0])
ax4.bar(list(most_recalled.keys())[:10], list(most_recalled.values())[:10], color='green', label='Most')
ax4.bar(list(least_recalled.keys())[:10], list(least_recalled.values())[:10], color='red', label='Least')
ax4.set_title("Top and Bottom Recalled Words")
ax4.legend()
ax4.set_xticklabels(list(most_recalled.keys())[:10], rotation=45)

# 5️⃣ Distribution of recall counts
ax5 = fig.add_subplot(gs[1, 1])
ax5.hist(df_words["count"], bins=20, color='skyblue', edgecolor='black')
ax5.set_title("Word Recall Frequency Distribution")
ax5.set_xlabel("Recall Count")
ax5.set_ylabel("Word Count")

# 6️⃣ Best Session Metrics
ax6 = fig.add_subplot(gs[1, 2])
ax6.barh(list(best_metrics.keys()), list(best_metrics.values()), color=['purple', 'red', 'gray'])
ax6.set_title("Best Session Highlights")

# 7️⃣ Heatmap of Top 20 Words vs Sessions
top_words = df_words.head(20)["Word"].tolist()
matrix = pd.DataFrame(0, index=top_words, columns=df_sessions["Session"])

for file in session_files:
    with open(os.path.join(sessions_dir, file), "r", encoding="utf-8") as f:
        data = json.load(f)
    sess_num = data.get("session_num")
    if "events" in data:
        for e in data["events"]:
            if e["word"] in matrix.index:
                matrix.loc[e["word"], sess_num] += 1
    elif "new_words" in data:
        for w in data["new_words"] + data["old_words"]:
            if w in matrix.index:
                matrix.loc[w, sess_num] += 1

ax7 = fig.add_subplot(gs[2, :])
sns.heatmap(matrix, cmap="YlGnBu", ax=ax7, cbar_kws={'label': 'Recalls'})
ax7.set_title("Top Words Recalled Across Sessions")
ax7.set_xlabel("Session")
ax7.set_ylabel("Word")

plt.suptitle(f"JapaneseDrills Progress Overview — {total_sessions} Sessions | {total_words} Words | {total_recall_count} Recalls | {total_recall_time}",
            fontsize=14, y=1.02)
plt.show()
