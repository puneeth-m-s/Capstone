import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# File path for the data
csv_file = "system_monitor.csv"

# Initialize the figure and subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

def update(frame):
    """Fetch and update the latest CPU & GPU usage and temperature data dynamically"""
    df = pd.read_csv(csv_file, encoding='utf-8-sig')
    
    # Convert Timestamp to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    
    # Keep only the last 50 data points to prevent clutter
    df = df.tail(50)
    
    # Clear previous plots
    ax1.clear()
    ax2.clear()
    
    # Plot CPU Data (Left Side)
    ax1.plot(df["Timestamp"], df["CPU Usage (%)"], label="CPU Usage (%)", color="blue", linewidth=2)
    if "CPU Temperature (°C)" in df.columns:
        ax1.plot(df["Timestamp"], df["CPU Temperature (°C)"], label="CPU Temperature (°C)", color="red", linewidth=2)
    
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Usage / Temperature")
    ax1.set_title("CPU Performance Over Time")
    ax1.legend()
    ax1.grid()
    
    # Plot GPU Data (Right Side) if available
    if "GPU Usage (%)" in df.columns and "N/A" not in df["GPU Usage (%)"].values:
        ax2.plot(df["Timestamp"], df["GPU Usage (%)"], label="GPU Usage (%)", color="green", linewidth=2)
        if "GPU Temperature (°C)" in df.columns:
            ax2.plot(df["Timestamp"], df["GPU Temperature (°C)"], label="GPU Temperature (°C)", color="orange", linewidth=2)
        ax2.set_title("GPU Performance Over Time")
    else:
        ax2.set_title("GPU Not Available")
    
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Usage / Temperature")
    ax2.legend()
    ax2.grid()
    
    plt.xticks(rotation=45)

# Animate the graph to update every second (1000ms interval)
ani = animation.FuncAnimation(fig, update, interval=1000, blit=False)

plt.show()
