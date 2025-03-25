import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# File path for the data
csv_file = "performance_data.csv"

# Initialize the figure and subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

def update(frame):
    """Fetch and update the latest CPU & GPU usage data dynamically"""
    df = pd.read_csv(csv_file)

    # Convert Timestamp to datetime
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # Keep only the last 50 data points to prevent clutter
    df = df.tail(50)

    # Clear previous plots
    ax1.clear()
    ax2.clear()

    # Plot CPU Data (Left Side)
    ax1.plot(df["Timestamp"], df["CPU_Usage"], label="CPU Usage (%)", color="blue", linewidth=2)
    ax1.plot(df["Timestamp"], df["CPU_Memory_Usage"], label="CPU Memory Usage (%)", color="red", linewidth=2)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Usage (%)")
    ax1.set_title("CPU Performance Over Time")
    ax1.legend()
    ax1.grid()

    # Plot GPU Data (Right Side) if available
    if "GPU_Usage" in df.columns and "N/A" not in df["GPU_Usage"].values:
        ax2.plot(df["Timestamp"], df["GPU_Usage"], label="GPU Usage (%)", color="green", linewidth=2)
        ax2.plot(df["Timestamp"], df["GPU_Memory_Usage"], label="GPU Memory Usage (%)", color="orange", linewidth=2)
        ax2.set_title("GPU Performance Over Time")
    else:
        ax2.set_title("GPU Not Available")
    
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Usage (%)")
    ax2.legend()
    ax2.grid()

    plt.xticks(rotation=45)

# Animate the graph to update every second (1000ms interval)
ani = animation.FuncAnimation(fig, update, interval=1000, blit=False)

plt.show()
