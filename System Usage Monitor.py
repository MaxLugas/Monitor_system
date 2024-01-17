import tkinter as tk
import psutil
import platform


def update_system_info():
    # CPU and Memory
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()

    # OS details
    os_info = platform.system() + " " + platform.version()

    # Disk details
    disk_info = psutil.disk_usage('/')

    # Display information
    cpu_label.config(text=f"CPU: {cpu_percent}%")
    memory_label.config(text=f"Memory: {memory_info.percent}%")
    os_label.config(text=f"OS: {os_info}")
    disk_label.config(text=f"Disk: {disk_info.percent}%")

    root.after(500, update_system_info)


root = tk.Tk()
root.title("Monitor")

# Запрещаем изменение размеров окна
root.resizable(False, False)

cpu_label = tk.Label(root, text="CPU Usage: N/A", font=("Helvetica", 14))
cpu_label.pack()

memory_label = tk.Label(root, text="Memory Usage: N/A", font=("Helvetica", 14))
memory_label.pack()

os_label = tk.Label(root, text="OS: N/A", font=("Helvetica", 14))
os_label.pack()

disk_label = tk.Label(root, text="Disk Usage: N/A", font=("Helvetica", 14))
disk_label.pack()

update_system_info()

root.mainloop()
