import time
import psutil
import win32gui
import win32process
import win32con
import tkinter as tk
from tkinter import messagebox
import threading
import sys
import keyboard  # pip install keyboard
import json
import os

# Load apps and passwords from JSON file
def load_apps_from_json(file_path="app_config.json"):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load app config: {e}")
        return {}

# Apps to protect
apps = load_apps_from_json()

CHECK_INTERVAL = 2
locked_pids = set()
unlocked_titles = {}
last_prompt_times = {}
COOLDOWN_SECONDS = 10

def kill_process_by_pid(pid):
    try:
        proc = psutil.Process(pid)
        proc.kill()
        print(f"💀 Killed process {pid}")
    except Exception as e:
        print(f"⚠️ Failed to kill process {pid}: {e}")

def minimize_window(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    except Exception as e:
        print(f"⚠️ Failed to minimize window: {e}")

def restore_window(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)
    except Exception as e:
        print(f"⚠️ Failed to restore window: {e}")

def block_keys():
    keys_to_block = [
        "esc", "tab", "f4", "left windows", "right windows", "win"
    ]
    for key in keys_to_block:
        try:
            keyboard.block_key(key)
        except Exception as e:
            print(f"⚠️ Could not block key {key}: {e}")
    print("🛡️ Blocked keys: Esc, Tab, F4, Windows")

def unblock_keys():
    keys_to_unblock = [
        "esc", "tab", "f4", "left windows", "right windows", "win"
    ]
    for key in keys_to_unblock:
        try:
            keyboard.unblock_key(key)
        except Exception as e:
            print(f"⚠️ Could not unblock key {key}: {e}")
    print("🛡️ Unblocked keys.")

# Minimize all windows except the password popup
def minimize_all_other_windows(except_hwnd):
    def callback(hwnd, _):
        if hwnd != except_hwnd and win32gui.IsWindowVisible(hwnd):
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            except Exception as e:
                print(f"⚠️ Failed to minimize window {hwnd}: {e}")
        return True
    win32gui.EnumWindows(callback, None)

def show_password_prompt(pid, title, hwnd, correct_password):
    def check_password():
        entered = entry.get()
        if entered == correct_password:
            print("✅ Access granted.")
            unlocked_titles[title.lower()] = time.time()
            last_prompt_times[title.lower()] = time.time()
            unblock_keys()
            root.destroy()
            restore_window(hwnd)
        else:
            messagebox.showerror("Access Denied", "Wrong password. Closing app.")
            unblock_keys()
            root.destroy()
            kill_process_by_pid(pid)

    def cancel_and_kill():
        unblock_keys()
        root.destroy()
        kill_process_by_pid(pid)

    block_keys()

    root = tk.Tk()
    root.title("🔒 App Locked")
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    tk.Label(root, text=f"🔒 Access to {title} is restricted", font=("Arial", 28), fg="white", bg="black").pack(pady=50)
    tk.Label(root, text="Enter password:", font=("Arial", 20), fg="white", bg="black").pack()

    entry = tk.Entry(root, show="*", font=("Arial", 20), width=30)
    entry.pack(pady=20)
    entry.focus()

    tk.Button(root, text="Unlock", font=("Arial", 18), command=check_password).pack(pady=10)
    tk.Button(root, text="Close App", font=("Arial", 16), command=cancel_and_kill, bg="red", fg="white").pack()

    minimize_all_other_windows(root.winfo_id())

    root.mainloop()

def enum_windows():
    def callback(hwnd, _):
        if not win32gui.IsWindowVisible(hwnd):
            return True

        title = win32gui.GetWindowText(hwnd).strip()
        title_lower = title.lower()

        matched_app = None
        matched_password = None
        for app_name, app_password in apps.items():
            if app_name.lower() in title_lower:
                matched_app = app_name
                matched_password = app_password
                break

        if matched_app:
            _, pid = win32process.GetWindowThreadProcessId(hwnd)

            now = time.time()
            if pid in locked_pids:
                return True

            if title_lower in last_prompt_times and now - last_prompt_times[title_lower] < COOLDOWN_SECONDS:
                return True

            print(f"🔐 Found protected app window: {title} (PID: {pid})")

            locked_pids.add(pid)
            minimize_window(hwnd)

            threading.Thread(target=show_password_prompt, args=(pid, title, hwnd, matched_password)).start()

        return True

    win32gui.EnumWindows(callback, None)

def app_locker_loop():
    print(f"🛡️ App Locker running. Watching for {', '.join(apps.keys())}...")
    while True:
        enum_windows()
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        app_locker_loop()
    except KeyboardInterrupt:
        print("🛑 Locker stopped.")
        sys.exit(0)
