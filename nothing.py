import streamlit as st
import pandas as pd
import psutil
import time
import os
from statsmodels.tsa.arima.model import ARIMA  # ARIMA for time-series prediction

st.set_page_config(layout="wide")  # Full-width layout
st.title("📊 Real-Time CPU & GPU Monitor with ML Predictions")

# CSV File to Store Data
CSV_FILE = "system_usage.csv"

# Check if the CSV file exists, if not, create it
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Time", "CPU Usage", "GPU Usage"]).to_csv(CSV_FILE, index=False)

#
# Load existing data
df = pd.read_csv(CSV_FILE)

#
# Initialize session state for real-time graph
if "data" not in st.session_state:
    st.session_state.data = df.tail(50)  

#
# **Graph and Number placeholders**
col1, col2 = st.columns(2)
cpu_placeholder = col1.metric("🖥️ CPU Usage", "0%")
gpu_placeholder = col2.metric("🎮 GPU Usage", "0%")
chart_placeholder = st.empty()
prediction_placeholder = st.empty()  # Placeholder for ML prediction

def predict_future_cpu(data):
    """ Train ARIMA model and predict next CPU usage """
    if len(data) < 10:  

        return None
    model = ARIMA(data, order=(2,1,2))  # ARIMA model (adjust order based on performance)
    model_fit = model.fit()
    prediction = model_fit.forecast(steps=5)  # Predict next 5 seconds
    return prediction

while True:
    # **Get system usage data**
    cpu_usage = psutil.cpu_percent()
    gpu_usage = 0  # Default if no GPU available
    timestamp = time.strftime("%H:%M:%S")

    # **Append new data and update CSV**
    new_data = pd.DataFrame({"Time": [timestamp], "CPU Usage": [cpu_usage], "GPU Usage": [gpu_usage]})
    st.session_state.data = pd.concat([st.session_state.data, new_data]).tail(50)

    # Save to CSV (append mode)
    with open(CSV_FILE, "a") as f:
        new_data.to_csv(f, header=f.tell()==0, index=False)  # Only add header if file is empty

    # **Update metrics**
    cpu_placeholder.metric("🖥️ CPU Usage", f"{cpu_usage}%")
    gpu_placeholder.metric("🎮 GPU Usage", f"{gpu_usage}%")

    # **Train and Predict CPU Usage**
    cpu_predictions = predict_future_cpu(st.session_state.data["CPU Usage"])
    
    # **Update the graph**
    with chart_placeholder:
        st.line_chart(st.session_state.data.set_index("Time"))

    # **Show Predictions**
    if cpu_predictions is not None:
        prediction_placeholder.write(f"📈 **Predicted CPU Usage (Next 5s):** {list(cpu_predictions)}")

    time.sleep(1)  # Update every second