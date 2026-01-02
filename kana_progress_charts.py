import json
import plotly.graph_objects as go

# Load JSON
with open("kana_mastery_progress.json", "r", encoding="utf-8") as f:
    kana_data = json.load(f)

# Compute correctness
history_data = {}
correctness_percent = {}

for kana, info in kana_data.items():
    history = info["stats"]["history"]
    history_data[kana] = history
    if history:
        correctness_percent[kana] = sum(history) / len(history) * 100
    else:
        correctness_percent[kana] = 0

# Sort kana: 100% correct first, 0% last
sorted_words = sorted(correctness_percent.keys(), key=lambda w: correctness_percent[w], reverse=True)

# Max attempts for x-axis
max_attempts = max(len(h) for h in history_data.values())
num_words = len(sorted_words)

# Scrollable viewport
visible_rows = 400
row_height = 10

fig = go.Figure()

# Add colored rectangles; assign y-values top-to-bottom
for idx, word in enumerate(sorted_words):
    # Calculate y-value so first item is top
    y_val = num_words - idx - 1
    history = history_data[word]
    for x_idx, h in enumerate(history):
        color = 'green' if h == 1 else 'red'
        fig.add_shape(
            type="rect",
            x0=x_idx, x1=x_idx + 1,
            y0=y_val - 0.5, y1=y_val + 0.5,
            line=dict(width=1, color='black'),
            fillcolor=color,
        )
        # Scatter for hover info
        fig.add_trace(go.Scatter(
            x=[x_idx + 0.5],
            y=[y_val],
            mode='markers',
            marker=dict(size=0.1, color=color),
            hovertemplate=f'Kana: {word}<br>Attempt: {x_idx + 1}<br>{"Correct" if h==1 else "Wrong"}<extra></extra>',
            showlegend=False
        ))

# Layout: invert y-axis no longer needed, range matches rows
fig.update_yaxes(
    tickvals=list(range(num_words)),
    ticktext=list(reversed(sorted_words)),  # match y-values
    autorange=False,
    range=[-0.5, num_words - 0.5],
    fixedrange=True
)
fig.update_xaxes(
    title_text="Attempt Number",
    range=[0, max_attempts],
    dtick=1,
    fixedrange=True
)

# Fixed viewport height for scrolling
fig.update_layout(
    title="Kana History: Correct (green = correct, red = wrong)",
    height=row_height*visible_rows,
    margin=dict(l=150, r=50, t=50, b=50),
    hovermode="closest"
)

fig.show()
