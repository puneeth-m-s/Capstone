import psutil
import time
import csv
import os

try:
    from pynvml import (
        nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates,
        nvmlDeviceGetMemoryInfo, nvmlDeviceGetCount
    )
    nvmlInit()
    gpu_count = nvmlDeviceGetCount()
    gpu_available = gpu_count > 0
except Exception as e:
    gpu_available = False
    gpu_error_msg = str(e)

# Create CSV file for data collection
filename = "performance_data.csv"
if not os.path.exists(filename):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "CPU_Usage", "CPU_Memory_Usage", "GPU_Usage", "GPU_Memory_Usage"])

def get_cpu_info():
    """Fetch CPU usage and memory usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    cpu_memory_usage = memory_info.percent  # System memory usage
    return cpu_usage, cpu_memory_usage

def get_gpu_info():
    """Fetch GPU usage and memory usage if GPU is available."""
    if not gpu_available:
        return "N/A", "N/A"

    nvml_handle = nvmlDeviceGetHandleByIndex(0)
    gpu_usage = nvmlDeviceGetUtilizationRates(nvml_handle).gpu
    gpu_mem = nvmlDeviceGetMemoryInfo(nvml_handle)

    return gpu_usage, gpu_mem.used / gpu_mem.total * 100

# Data collection loop
for _ in range(100):  # Collect data for 100 cycles (~200 seconds)
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cpu_usage, cpu_memory_usage = get_cpu_info()

    if gpu_available:
        gpu_usage, gpu_mem_usage = get_gpu_info()
    else:
        gpu_usage, gpu_mem_usage = "N/A", "N/A"

    # Save data to CSV
    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, cpu_usage, cpu_memory_usage, gpu_usage, gpu_mem_usage])

    print(f"{timestamp} | CPU: {cpu_usage}% | CPU Memory: {cpu_memory_usage}% | GPU: {gpu_usage}% | GPU Memory: {gpu_mem_usage}%")
    print("-" * 50)

    time.sleep(2)  # Collect data every 2 seconds
