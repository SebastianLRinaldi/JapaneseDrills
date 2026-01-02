# import json
# from pathlib import Path
# import plotly.graph_objects as go

# master_path = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"

# # Load master data
# with open(master_path, "r", encoding="utf-8") as f:
#     master_data = json.load(f)

# # Compute score per kana
# kana_scores = []
# for k, v in master_data["kana"].items():
#     total = v.get("correct", 0) + v.get("wrong", 0)
#     accuracy = v["correct"] / total if total else 0
#     avg_time = v.get("avg_time") or float('inf')
#     score = accuracy / (avg_time + 0.0001)
#     kana_scores.append((k, score, accuracy, avg_time))

# # Sort kana by score descending
# kana_scores.sort(key=lambda x: x[1], reverse=True)

# # Split for plotting
# kana_labels = [k for k, s, a, t in kana_scores]
# scores = [s for k, s, a, t in kana_scores]
# accuracy = [a for k, s, a, t in kana_scores]
# avg_time = [t for k, s, a, t in kana_scores]

# # Highlight top 5 green, bottom 5 red, rest blue
# colors = ['green' if i < 5 else 'red' if i >= len(kana_scores)-5 else 'skyblue' for i in range(len(kana_scores))]

# # Create interactive bar chart
# fig = go.Figure(data=[
#     go.Bar(
#         x=kana_labels,
#         y=scores,
#         text=[f"Accuracy: {a*100:.1f}%, Avg Time: {t:.2f}s" for a, t in zip(accuracy, avg_time)],
#         hoverinfo='x+y+text',
#         marker_color=colors
#     )
# ])

# fig.update_layout(
#     title="Kana Performance Scores",
#     xaxis_title="Kana",
#     yaxis_title="Score (Accuracy / Avg Time)",
#     xaxis_tickangle=-90,
#     template="plotly_white",
#     height=500
# )

# fig.show()
import json
from pathlib import Path
import plotly.graph_objects as go
from plotly.subplots import make_subplots

master_path = r"F:\_Small\344 School Python\JapaneseDrills\kana_recall_data\kana_mastery_progress.json"

# Load master data
with open(master_path, "r", encoding="utf-8") as f:
    master_data = json.load(f)

GROUPS = {
    "Hiragana Main": ["あ","い","う","え","お","か","き","く","け","こ","さ","し","す","せ","そ","た","ち","つ","て","と",
                      "な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ","ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ","ろ","わ","を","ん"],
    "Hiragana Dakuten": ["が","ぎ","ぐ","げ","ご","ざ","じ","ず","ぜ","ぞ","だ","ぢ","づ","で","ど","ば","び","ぶ","べ","ぼ","ぱ","ぴ","ぷ","ぺ","ぽ"],
    "Hiragana Combination": ["きゃ","きゅ","きょ","しゃ","しゅ","しょ","ちゃ","ちゅ","ちょ","にゃ","にゅ","にょ",
                             "ひゃ","ひゅ","ひょ","みゃ","みゅ","みょ","りゃ","りゅ","りょ","ぎゃ","ぎゅ","ぎょ",
                             "じゃ","じゅ","じょ","びゃ","びゅ","びょ","ぴゃ","ぴゅ","ぴょ"],
    "Katakana Main": ["ア","イ","ウ","エ","オ","カ","キ","ク","ケ","コ","サ","シ","ス","セ","ソ","タ","チ","ツ","テ","ト",
                      "ナ","ニ","ヌ","ネ","ノ","ハ","ヒ","フ","ヘ","ホ","マ","ミ","ム","メ","モ","ヤ","ユ","ヨ","ラ","リ","ル","レ","ロ","ワ","ヲ","ン"],
    "Katakana Dakuten": ["ガ","ギ","グ","ゲ","ゴ","ザ","ジ","ズ","ゼ","ゾ","ダ","ヂ","ヅ","デ","ド","バ","ビ","ブ","ベ","ボ","パ","ピ","プ","ペ","ポ"],
    "Katakana Combination": ["キャ","キュ","キョ","シャ","シュ","ショ","チャ","チュ","チョ","ニャ","ニュ","ニョ",
                             "ヒャ","ヒュ","ヒョ","ミャ","ミュ","ミョ","リャ","リュ","リョ","ギャ","ギュ","ギョ",
                             "ジャ","ジュ","ジョ","ビャ","ビュ","ビョ","ピャ","ピュ","ピョ"]
}

def get_score(kana):
    stats = master_data["kana"].get(kana, {})
    total = stats.get("correct",0)+stats.get("wrong",0)
    accuracy = stats.get("correct",0)/total if total else 0
    avg_time = stats.get("avg_time") or float('inf')
    return accuracy / (avg_time + 0.0001)

# Create subplot figure: 6 rows, 1 column
fig = make_subplots(rows=6, cols=1, shared_xaxes=False, vertical_spacing=0.05,
                    subplot_titles=list(GROUPS.keys()))

for i, (group_name, kana_list) in enumerate(GROUPS.items(), start=1):
    scores = [get_score(k) for k in kana_list]
    colors = ['green' if s > 0.9 else 'red' if s == 0 else 'skyblue' for s in scores]

    fig.add_trace(
        go.Bar(
            x=kana_list,
            y=scores,
            marker_color=colors,
            text=[f"{s:.2f}" for s in scores],
            textposition='auto',
            hovertext=[f"Score: {s:.2f}" for s in scores]
        ),
        row=i, col=1
    )

fig.update_layout(
    height=1800,  # tall enough to fit all 6 charts
    title_text="Kana Performance by Type/Script",
    showlegend=False,
    template="plotly_white"
)

# Rotate x-axis labels for readability
for i in range(1, 7):
    fig.update_xaxes(tickangle=-45, row=i, col=1)

fig.show()
