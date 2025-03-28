from dash import Dash, dcc, html
import psutil
import dash_daq as daq
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# Check if GPU monitoring is available
try:
    from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetTemperature, nvmlShutdown, NVML_TEMPERATURE_GPU
    nvmlInit()
    gpu_available = True
    gpu_handle = nvmlDeviceGetHandleByIndex(0)  # First GPU
except ImportError:
    gpu_available = False

# Initialize Dash app
app = Dash(__name__)

# Store historical data
cpu_usage_history = []
gpu_usage_history = []

# App Layout
app.layout = html.Div([
    html.H1("System Monitor Dashboard", style={'textAlign': 'center'}),

    # CPU & GPU Monitoring Section
    html.Div([
        # CPU Usage
        html.Div([
            html.H3("CPU Usage"),
            daq.Gauge(
                id="cpu-gauge",
                label="CPU Usage (%)",
                min=0,
                max=100,
                showCurrentValue=True
            ),
            html.P("CPU Temperature: ", id="cpu-temp", style={"fontSize": "18px", "fontWeight": "bold"}),
        ], style={"width": "45%", "padding": "10px"}),

        # GPU Usage
        html.Div([
            html.H3("GPU Usage"),
            daq.Gauge(
                id="gpu-gauge",
                label="GPU Usage (%)",
                min=0,
                max=100,
                showCurrentValue=True
            ),
            html.P("GPU Temperature: ", id="gpu-temp", style={"fontSize": "18px", "fontWeight": "bold"}),
        ], style={"width": "45%", "padding": "10px"}),

    ], style={"display": "flex", "justify-content": "space-around"}),

    # Live Graphs
    html.Div([
        dcc.Graph(id="cpu-graph"),
        dcc.Graph(id="gpu-graph")
    ]),

    # Interval Component (Triggers update every 2 seconds)
    dcc.Interval(id="interval-update", interval=2000, n_intervals=0)
], style={"padding": "20px"})

# Callback to update real-time data
@app.callback(
    [Output("cpu-gauge", "value"),
     Output("cpu-temp", "children"),
     Output("cpu-graph", "figure"),
     Output("gpu-gauge", "value"),
     Output("gpu-temp", "children"),
     Output("gpu-graph", "figure")],
    Input("interval-update", "n_intervals")
)
def update_dashboard(n_intervals):
    # Get CPU Data
    cpu_usage = psutil.cpu_percent()
    try:
        cpu_temp = psutil.sensors_temperatures().get("coretemp", [{}])[0].get("current", "N/A")
    except:
        cpu_temp = "N/A"

    # Get GPU Data
    if gpu_available:
        gpu_usage = nvmlDeviceGetUtilizationRates(gpu_handle).gpu
        gpu_temp = nvmlDeviceGetTemperature(gpu_handle, NVML_TEMPERATURE_GPU)
    else:
        gpu_usage, gpu_temp = 0, "N/A"

    # Store data history for graphing
    cpu_usage_history.append(cpu_usage)
    gpu_usage_history.append(gpu_usage)

    # Keep only last 50 values for smooth updates
    cpu_usage_history[:] = cpu_usage_history[-50:]
    gpu_usage_history[:] = gpu_usage_history[-50:]

    # CPU Usage Graph
    cpu_graph = go.Figure(data=[go.Scatter(y=cpu_usage_history, mode="lines", name="CPU Usage")])
    cpu_graph.update_layout(title="CPU Usage Over Time", xaxis_title="Time", yaxis_title="Usage (%)")

    # GPU Usage Graph
    gpu_graph = go.Figure(data=[go.Scatter(y=gpu_usage_history, mode="lines", name="GPU Usage")])
    gpu_graph.update_layout(title="GPU Usage Over Time", xaxis_title="Time", yaxis_title="Usage (%)")

    return cpu_usage, f"CPU Temperature: {cpu_temp}°C", cpu_graph, gpu_usage, f"GPU Temperature: {gpu_temp}°C", gpu_graph

# Run the Dash app
if __name__ == "__main__":
    app.run(debug=True)
