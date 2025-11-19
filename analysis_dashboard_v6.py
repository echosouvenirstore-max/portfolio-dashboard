import os
import webbrowser
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px


# =====================================================
# 1. Load CSV
# =====================================================
csv_path = "paris_2015_2024_weather.csv"

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"[ERROR] CSV not found: {csv_path}")

df = pd.read_csv(csv_path)

# Clean numeric columns
numeric_cols = df.select_dtypes(include="number").columns
df[numeric_cols] = df[numeric_cols].apply(lambda c: c.ffill().bfill())


# =====================================================
# 2. Dash App
# =====================================================
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Paris Weather Dashboard (v6.2)", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="metric_selector",
        options=[
            {"label": col, "value": col}
            for col in numeric_cols
        ],
        value=numeric_cols[0],
        clearable=False
    ),

    dcc.Graph(id="main_graph")
])


# =====================================================
# 3. Callbacks
# =====================================================
@app.callback(
    Output("main_graph", "figure"),
    Input("metric_selector", "value")
)
def update_plot(metric):
    fig = px.line(
        df,
        x=df.columns[0],
        y=metric,
        title=f"{metric} — Time Series"
    )
    return fig


# =====================================================
# 4. Auto-open browser + Launch Server
# =====================================================
if __name__ == "__main__":
    url = "http://127.0.0.1:8050"
    print(f"Dashboard running on {url}")

    # Auto-open browser
    webbrowser.open(url)

    # Correct method for Dash 3.x+
    app.run(debug=True, port=8050, use_reloader=True)
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['precipitation'],
    mode='lines',
    line=dict(
        width=2.2,
        color="rgba(31, 119, 180, 0.8)"   # manga mazava, opaque kokoa
    ),
    name="Daily Precipitation"
))

fig.update_layout(
    title="Daily Precipitation (2015–2024)",
    xaxis_title="Date",
    yaxis_title="Precipitation (mm)",
    template="simple_white",
    hovermode="x unified",
    height=600
)
