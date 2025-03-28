import csv
import datetime
import os
from dash import Dash, dcc, html
import psutil
import dash_daq as daq
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# GPU Monitoring Setup
gpu_available = False
try:
    from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetTemperature, nvmlShutdown, NVML_TEMPERATURE_GPU
    nvmlInit()
    gpu_available = True
    gpu_handle = nvmlDeviceGetHandleByIndex(0)  # First GPU
except ImportError:
    gpu_available = False

# CSV File Setup
csv_filename = "system_monitor.csv"

# Function to create CSV file only once
if not os.path.exists(csv_filename) or os.stat(csv_filename).st_size == 0:
    with open(csv_filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPU Usage (%)", "CPU Temperature (°C)", "GPU Usage (%)", "GPU Temperature (°C)"])

# Initialize Dash App
app = Dash(__name__)

# Data History for Graphs
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
            html.P(id="cpu-temp", style={"fontSize": "18px", "fontWeight": "bold"}),
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
            html.P(id="gpu-temp", style={"fontSize": "18px", "fontWeight": "bold"}),
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


# Function to get CPU Temperature
def get_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            return temps['coretemp'][0].current
        elif "cpu-thermal" in temps:  # Raspberry Pi
            return temps['cpu-thermal'][0].current
        else:
            return None
    except:
        return None


# Function to get GPU Usage and Temperature
def get_gpu_usage_and_temp():
    if gpu_available:
        try:
            gpu_usage = nvmlDeviceGetUtilizationRates(gpu_handle).gpu
            gpu_temp = nvmlDeviceGetTemperature(gpu_handle, NVML_TEMPERATURE_GPU)
            return gpu_usage, gpu_temp
        except:
            return 0, None
    return 0, None


# Callback: Update Dashboard Data
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
    cpu_temp = get_cpu_temperature()

    # Get GPU Data
    gpu_usage, gpu_temp = get_gpu_usage_and_temp()

    # Format temperature values
    cpu_temp_text = f"CPU Temperature: {cpu_temp}°C" if cpu_temp is not None else "CPU Temperature: Not Available"
    gpu_temp_text = f"GPU Temperature: {gpu_temp}°C" if gpu_temp is not None else "GPU Temperature: Not Available"

    # Store data history for graphing
    cpu_usage_history.append(cpu_usage)
    gpu_usage_history.append(gpu_usage)

    # Keep last 50 values for smooth updates
    cpu_usage_history[:] = cpu_usage_history[-50:]
    gpu_usage_history[:] = gpu_usage_history[-50:]

    # **Append data to CSV File**
    with open(csv_filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.datetime.now(), cpu_usage, cpu_temp if cpu_temp else "N/A", gpu_usage, gpu_temp if gpu_temp else "N/A"])

    # CPU Graph
    cpu_graph = go.Figure(data=[go.Scatter(y=cpu_usage_history, mode="lines", name="CPU Usage")])
    cpu_graph.update_layout(title="CPU Usage Over Time", xaxis_title="Time", yaxis_title="Usage (%)")

    # GPU Graph
    gpu_graph = go.Figure(data=[go.Scatter(y=gpu_usage_history, mode="lines", name="GPU Usage")])
    gpu_graph.update_layout(title="GPU Usage Over Time", xaxis_title="Time", yaxis_title="Usage (%)")

    return cpu_usage, cpu_temp_text, cpu_graph, gpu_usage, gpu_temp_text, gpu_graph


# Run the Dash app
if __name__ == "__main__":
    app.run(debug=True)
