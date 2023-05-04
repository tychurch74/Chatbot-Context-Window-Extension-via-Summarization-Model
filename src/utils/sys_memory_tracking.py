import psutil
import time

def display_memory_usage():
    memory = psutil.virtual_memory()
    total_memory = memory.total / (1024 ** 2)  # Convert to MB
    used_memory = memory.used / (1024 ** 2)  # Convert to MB
    free_memory = memory.available / (1024 ** 2)  # Convert to MB
    memory_percent = memory.percent

    print(f"Total memory: {total_memory:.2f} MB")
    print(f"Used memory: {used_memory:.2f} MB")
    print(f"Free memory: {free_memory:.2f} MB")
    print(f"Memory usage percentage: {memory_percent}%")

while True:
    display_memory_usage()
    time.sleep(5)  # Refresh interval in seconds

