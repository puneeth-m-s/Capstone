import pandas as pd
import matplotlib.pyplot as plt

# Load the collected data
df = pd.read_csv("performance_data.csv")

# Convert Timestamp to datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Plot CPU Usage
plt.figure(figsize=(12, 6))
plt.plot(df["Timestamp"], df["CPU_Usage"], label="CPU Usage (%)", color="blue")
plt.plot(df["Timestamp"], df["CPU_Memory_Usage"], label="CPU Memory Usage (%)", color="red")
plt.xlabel("Time")
plt.ylabel("Usage (%)")
plt.title("CPU Performance Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.grid()
plt.show()

# Plot GPU Usage (if available)
if "N/A" not in df["GPU_Usage"].values:
    plt.figure(figsize=(12, 6))
    plt.plot(df["Timestamp"], df["GPU_Usage"], label="GPU Usage (%)", color="green")
    plt.plot(df["Timestamp"], df["GPU_Memory_Usage"], label="GPU Memory Usage (%)", color="orange")
    plt.xlabel("Time")
    plt.ylabel("Usage (%)")
    plt.title("GPU Performance Over Time")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()
