import os
import time
import csv
import argparse
import psutil
from datetime import datetime

def clear_screen():
    """Clears the terminal screen cleanly on Windows."""
    os.system('cls')

def get_cpu_bar(percentage, width=20):
    """Generates a visual progress bar for CPU usage."""
    filled_length = int(width * percentage / 100)
    bar = '█' * filled_length + '-' * (width - filled_length)
    return f"[{bar}] {percentage:.1f}%"

def log_to_csv(cpu, ram, disk):
    """Logs system metrics with a timestamp to a CSV file for history tracking."""
    file_exists = os.path.isfile("system_log.csv")
    
    with open("system_log.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        # Write headers if the file is being created for the first time
        if not file_exists:
            writer.writerow(["Timestamp", "CPU (%)", "RAM (%)", "Disk (%)"])
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, cpu, ram, disk])

def main():
    # --- Professional Setup: Command Line Arguments ---
    parser = argparse.ArgumentParser(description="SysPulse: A professional command-line system monitor.")
    parser.add_argument(
        "-i", "--interval", 
        type=float, 
        default=2.0, 
        help="Refresh interval in seconds (default: 2.0)"
    )
    parser.add_argument(
        "--no-log", 
        action="store_true", 
        help="Disable background logging to CSV"
    )
    args = parser.parse_args()

    try:
        while True:
            clear_screen()
            
            # Fetch core metrics
            global_cpu = psutil.cpu_percent()
            vm = psutil.virtual_memory()
            disk = psutil.disk_usage('C:\\')
            
            # --- Log Data to CSV ---
            log_status = "ENABLED (system_log.csv)"
            if not args.no_log:
                log_to_csv(global_cpu, vm.percent, disk.percent)
            else:
                log_status = "DISABLED"

            # --- UI Rendering ---
            print("=" * 60)
            print("            SYSPULSE - ENTERPRISE SYSTEM MONITOR")
            print(f"   Refresh: {args.interval}s | Logging: {log_status} | Ctrl+C to Exit")
            print("=" * 60)
            
            # CPU Section
            print("\n[ CPU USAGE ]")
            print(f"Total CPU: {get_cpu_bar(global_cpu)}")
            cores = psutil.cpu_percent(percpu=True)
            for i, core_val in enumerate(cores):
                print(f"  Core {i}:  {get_cpu_bar(core_val, width=15)}")
                
            # Memory & Storage Section
            print("\n[ MEMORY & STORAGE ]")
            ram_used_gb = vm.used / (1024**3)
            ram_total_gb = vm.total / (1024**3)
            print(f"RAM Usage: {get_cpu_bar(vm.percent)} ({ram_used_gb:.2f} GB / {ram_total_gb:.2f} GB)")
            
            disk_used_gb = disk.used / (1024**3)
            disk_total_gb = disk.total / (1024**3)
            print(f"Disk (C:): {get_cpu_bar(disk.percent)} ({disk_used_gb:.1f} GB / {disk_total_gb:.1f} GB)")

            # Process Section
            print("\n[ TOP 5 PROCESSES BY MEMORY ]")
            print(f"  {'PID':<10} | {'Process Name':<25} | {'Memory (MB)':<12}")
            print("  " + "-" * 53)
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    processes.append((proc.info['pid'], proc.info['name'], mem_mb))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            
            processes.sort(key=lambda x: x[2], reverse=True)
            for pid, name, mem in processes[:5]:
                short_name = name[:23] + ".." if len(name) > 25 else name
                print(f"  {pid:<10} | {short_name:<25} | {mem:>10.1f} MB")
                
            print("=" * 60)
            
            time.sleep(args.interval)

    except KeyboardInterrupt:
        clear_screen()
        print("\nSysPulse stopped. Have a great day!")

if __name__ == "__main__":
    main()