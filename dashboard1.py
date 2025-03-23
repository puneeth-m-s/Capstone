import psutil
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import time
import threading
import pynvml

# Initialize NVIDIA Management Library
try:
    pynvml.nvmlInit()
    gpu_available = True
    gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)
except:
    gpu_available = False

data = {'time': [], 'cpu': [], 'gpu': []}

# Function to fetch CPU and GPU usage
def fetch_metrics():
    while True:
        data['time'].append(time.strftime('%H:%M:%S'))
        data['cpu'].append(psutil.cpu_percent())
        
        if gpu_available:
            gpu_util = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle).gpu
        else:
            gpu_util = 0
        
        data['gpu'].append(gpu_util)
        
        if len(data['time']) > 50:
            data['time'].pop(0)
            data['cpu'].pop(0)
            data['gpu'].pop(0)
        
        time.sleep(1)

# Start background thread for monitoring
threading.Thread(target=fetch_metrics, daemon=True).start()

# Initialize Dash app
app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Real-Time CPU & GPU Monitoring Dashboard"),
    dcc.Graph(id='cpu-graph'),
    dcc.Graph(id='gpu-graph'),
    dcc.Interval(id='interval', interval=1000, n_intervals=0)
])

@app.callback(
    [Output('cpu-graph', 'figure'), Output('gpu-graph', 'figure')],
    [Input('interval', 'n_intervals')]
)
def update_graph(n):
    cpu_fig = go.Figure(data=[go.Scatter(x=data['time'], y=data['cpu'], mode='lines', name='CPU Usage')])
    cpu_fig.update_layout(title='CPU Usage (%)', xaxis_title='Time', yaxis_title='Usage %')
    
    gpu_fig = go.Figure(data=[go.Scatter(x=data['time'], y=data['gpu'], mode='lines', name='GPU Usage')])
    gpu_fig.update_layout(title='GPU Usage (%)', xaxis_title='Time', yaxis_title='Usage %')
    
    return cpu_fig, gpu_fig

if __name__ == '__main__':
    app.run(debug=True)
