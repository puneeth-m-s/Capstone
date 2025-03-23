import psutil
import time
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

def get_cpu_info():
    """Fetch CPU usage and memory usage."""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    cpu_memory_usage = memory_info.percent  # Total system memory usage
    return cpu_usage, cpu_memory_usage

def get_gpu_info():
    """Fetch GPU usage and memory usage if GPU is available."""
    if not gpu_available:
        return "No GPU detected", "N/A"

    nvml_handle = nvmlDeviceGetHandleByIndex(0)
    gpu_usage = nvmlDeviceGetUtilizationRates(nvml_handle).gpu
    gpu_mem = nvmlDeviceGetMemoryInfo(nvml_handle)

    return gpu_usage, gpu_mem.used / gpu_mem.total * 100

while True:
    cpu_usage, cpu_memory_usage = get_cpu_info()

    if cpu_usage > 80:
        print(f"⚠️ ALERT: High CPU Usage! ({cpu_usage}%) ⚠️")
    
    if cpu_memory_usage > 80:
        print(f"⚠️ ALERT: High CPU Memory Usage! ({cpu_memory_usage}%) ⚠️")

    if gpu_available:
        gpu_usage, gpu_mem_usage = get_gpu_info()
        print(f"CPU Usage: {cpu_usage}%")
        print(f"CPU Memory Usage: {cpu_memory_usage}%")
        print(f"GPU Usage: {gpu_usage}%, GPU Memory Usage: {gpu_mem_usage:.2f}%")
    else:
        print(f"CPU Usage: {cpu_usage}%")
        print(f"CPU Memory Usage: {cpu_memory_usage}%")
        print(f"GPU Not Found: {gpu_error_msg}")

    print("-" * 40)
    time.sleep(2)
