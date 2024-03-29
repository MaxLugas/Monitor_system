import tkinter as tk
import psutil
import platform
import GPUtil
import threading


def get_gpu_temperature():
    try:
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu_temperature_info = ", ".join([f"{gpu.temperature}°C" for gpu in gpus])
            return f"GPU Temperature: {gpu_temperature_info}"
        else:
            return "GPU Temperature: N/A"
    except Exception as e:
        return f"GPU Temperature: N/A (Error: {e})"


def get_battery_status():
    try:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            power_plugged = battery.power_plugged
            status = "Plugged In" if power_plugged else "Not Plugged In"
            return f"Battery: {percent}% ({status})"
        else:
            return "Battery: N/A"
    except Exception as e:
        return f"Battery: N/A (Error: {e})"


def get_network_usage():
    try:
        network_info = psutil.net_io_counters()
        return (f"Network Usage: In: {convert_bytes(network_info.bytes_recv)} | Out: "
                f"{convert_bytes(network_info.bytes_sent)}")
    except Exception as e:
        return f"Network Usage: N/A (Error: {e})"


def convert_bytes(bytes):
    kb = bytes / 1024
    mb = kb / 1024
    gb = mb / 1024
    if gb >= 1:
        return f"{gb:.2f} GB"
    elif mb >= 1:
        return f"{mb:.2f} MB"
    elif kb >= 1:
        return f"{kb:.2f} KB"
    else:
        return f"{bytes} B"


def update_system_info():
    while True:
        # CPU and Memory
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()

        # GPU Temperature
        gpu_temperature_info = get_gpu_temperature()

        # Battery Status
        battery_status_info = get_battery_status()

        # Network Usage
        network_usage_info = get_network_usage()

        # OS details
        os_info = platform.system() + " " + platform.version().split()[0]  # Оставляем только версию

        # Disk details
        disk_info = psutil.disk_usage('/')

        # Display information
        root.after_idle(
            lambda: update_labels(cpu_percent, memory_info.percent, gpu_temperature_info,
                                  battery_status_info, network_usage_info, os_info, disk_info.percent)
        )
        root.update()
        root.update_idletasks()


def update_labels(cpu_percent, memory_percent, gpu_temp, battery_status, network_usage, os_info, disk_percent):
    cpu_label.config(text=f"CPU: {cpu_percent}%")
    memory_label.config(text=f"Memory: {memory_percent}%")
    gpu_label.config(text=gpu_temp)
    battery_label.config(text=battery_status)
    network_label.config(text=network_usage)
    os_label.config(text=f"OS: {os_info}")
    disk_label.config(text=f"Disk: {disk_percent}%")


root = tk.Tk()
root.title("Monitor")

root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", root.destroy)

os_label = tk.Label(root, text="OS: N/A", font=("Helvetica", 14))
os_label.pack()

cpu_label = tk.Label(root, text="CPU Usage: N/A", font=("Helvetica", 14))
cpu_label.pack()

memory_label = tk.Label(root, text="Memory Usage: N/A", font=("Helvetica", 14))
memory_label.pack()

gpu_label = tk.Label(root, text="GPU Temperature: N/A", font=("Helvetica", 14))
gpu_label.pack()

battery_label = tk.Label(root, text="Battery: N/A", font=("Helvetica", 14))
battery_label.pack()

network_label = tk.Label(root, text="Network Usage: N/A", font=("Helvetica", 14))
network_label.pack()

disk_label = tk.Label(root, text="Disk Usage: N/A", font=("Helvetica", 14))
disk_label.pack()

update_thread = threading.Thread(target=update_system_info, daemon=True)
update_thread.start()

root.mainloop()
