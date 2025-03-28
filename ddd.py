import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import chardet

# CSV File
csv_file = "system_monitor.csv"

# Detect CSV Encoding
def detect_encoding(file):
    with open(file, "rb") as f:
        result = chardet.detect(f.read(10000))  # Check first 10,000 bytes
    return result["encoding"]

# Read CSV with proper encoding
def read_csv_file(file):
    encoding = detect_encoding(file)
    try:
        df = pd.read_csv(file, encoding=encoding, errors="replace")
        df.columns = df.columns.str.replace("°", "")  # Remove degree symbols
        df = df.applymap(lambda x: str(x).replace("°", "") if isinstance(x, str) else x)
        return df
    except Exception as e:
        print("Error reading CSV:", e)
        return pd.DataFrame()  # Return empty DataFrame if error occurs

# Initialize Figure
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
cpu_ax, gpu_ax = axes  # Assign subplots

# Update Function for Animation
def update(frame):
    df = read_csv_file(csv_file)
    
    if df.empty:
        print("CSV file is empty or not readable. Skipping update.")
        return

    try:
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])  # Convert timestamp
        df = df.tail(50)  # Keep last 50 records for smooth updates

        cpu_ax.clear()
        cpu_ax.plot(df["Timestamp"], df["CPU Usage (%)"], color="blue", label="CPU Usage (%)")
        cpu_ax.set_title("CPU Usage Over Time")
        cpu_ax.set_xlabel("Time")
        cpu_ax.set_ylabel("CPU Usage (%)")
        cpu_ax.legend()
        cpu_ax.tick_params(axis="x", rotation=45)

        gpu_ax.clear()
        gpu_ax.plot(df["Timestamp"], df["GPU Usage (%)"], color="red", label="GPU Usage (%)")
        gpu_ax.set_title("GPU Usage Over Time")
        gpu_ax.set_xlabel("Time")
        gpu_ax.set_ylabel("GPU Usage (%)")
        gpu_ax.legend()
        gpu_ax.tick_params(axis="x", rotation=45)

    except Exception as e:
        print("Error updating graph:", e)

# Animate Graph Every 2 Seconds
ani = animation.FuncAnimation(fig, update, interval=2000)

plt.tight_layout()
plt.show()
