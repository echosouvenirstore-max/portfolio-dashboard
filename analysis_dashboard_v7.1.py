import os
import webbrowser
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from fpdf import FPDF

# =====================================================
# 1. Load data
# =====================================================
csv_path = "paris_2015_2024_weather.csv"
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"CSV file not found: {csv_path}")

df = pd.read_csv(csv_path)

# Clean numeric cols
numeric_cols = df.select_dtypes(include="number").columns
df[numeric_cols] = df[numeric_cols].apply(lambda col: col.ffill().bfill())

# =====================================================
# 2. Dash App
# =====================================================
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Paris Weather Dashboard", style={"textAlign": "center"}),

    dcc.Dropdown(
        id="metric",
        options=[
            {"label": c, "value": c}
            for c in numeric_cols
        ],
        value=numeric_cols[0],
        clearable=False
    ),

    dcc.Graph(id="main_plot"),

    html.Button("Download PDF Report", id="btn_pdf"),

    html.Div(id="pdf_status", style={"marginTop": "15px", "fontWeight": "bold"})
])


# =====================================================
# 3. Callbacks
# =====================================================
@app.callback(
    Output("main_plot", "figure"),
    Input("metric", "value")
)
def update_graph(selected_metric):
    fig = px.line(df, x=df.columns[0], y=selected_metric, title=f"{selected_metric} over time")
    return fig


@app.callback(
    Output("pdf_status", "children"),
    Input("btn_pdf", "n_clicks"),
    prevent_initial_call=True
)
def generate_pdf(n):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)

    pdf.cell(0, 10, "Paris Weather Dashboard Report", ln=True)

    # Add summary stats
    for col in numeric_cols:
        pdf.set_font("Arial", size=12)
        text = f"{col}: mean={df[col].mean():.2f}, min={df[col].min():.2f}, max={df[col].max():.2f}"
        pdf.cell(0, 8, text, ln=True)

    pdf.output("weather_report.pdf")

    return "PDF generated: weather_report.pdf"


# =====================================================
# 4. Auto-open browser + Launch Server
# =====================================================
if __name__ == "__main__":
    url = "http://127.0.0.1:8050"
    print(f"Dashboard running on: {url}")

    # ***** AUTO OPEN BROWSER *****
    webbrowser.open(url)

    # Modern Dash run
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
