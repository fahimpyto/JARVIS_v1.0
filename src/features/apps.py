import os
import shutil
import subprocess
from pathlib import Path
import psutil
import win32gui
import win32con


def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True)
    except Exception:
        pass


def find_exe(candidates):
    for p in candidates:
        try:
            if Path(p).exists():
                return p
        except Exception:
            pass

    for exe in candidates:
        name = os.path.basename(exe)
        found = shutil.which(name)
        if found:
            return found

    return None


def open_explorer_shell(verb):
    run_cmd(f'explorer.exe {verb}')


def open_path(p):
    try:
        os.startfile(p)
        return True
    except Exception:
        return False


def close_app_by_names(process_names):
    found = False

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            pname = proc.info.get("name") or ""
            for name in process_names:
                if pname.lower().startswith(name.lower()):
                    proc.kill()
                    found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return found


# -------------------------
# Apps
# -------------------------
def open_whatsapp(speak=None):
    app_id = r"shell:AppsFolder\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
    if speak:
        speak("Opening WhatsApp.")
    run_cmd(f'explorer.exe {app_id}')


def close_whatsapp(speak=None):
    if close_app_by_names(["whatsapp", "WhatsApp"]):
        if speak:
            speak("WhatsApp closed.")
    else:
        if speak:
            speak("WhatsApp not running.")


def open_chrome(speak=None):
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "chrome.exe",
    ]

    exe = find_exe(candidates)

    if exe:
        if speak:
            speak("Opening Google Chrome.")
        try:
            subprocess.Popen([exe])
        except Exception:
            run_cmd(f'"{exe}"')
    else:
        if speak:
            speak("Chrome not found.")


def close_chrome(speak=None):
    if close_app_by_names(["chrome", "chrome.exe"]):
        if speak:
            speak("Chrome closed.")
    else:
        if speak:
            speak("Chrome not running.")


def open_brave(speak=None):
    candidates = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        "brave.exe",
    ]

    exe = find_exe(candidates)

    if exe:
        if speak:
            speak("Opening Brave.")
        try:
            subprocess.Popen([exe])
        except Exception:
            run_cmd(f'"{exe}"')
    else:
        if speak:
            speak("Brave not found.")


def close_brave(speak=None):
    if close_app_by_names(["brave", "brave.exe"]):
        if speak:
            speak("Brave closed.")
    else:
        if speak:
            speak("Brave not running.")


def open_this_pc(speak=None):
    if speak:
        speak("Opening This PC.")
    open_explorer_shell("shell:MyComputerFolder")


def close_this_pc():
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd) and "This PC" in win32gui.GetWindowText(hwnd):
            windows.append(hwnd)

    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)

    for hwnd in windows:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)


# -------------------------
# Known folders
# -------------------------
def open_known_folder(name, speak=None):
    mapping = {
        "downloads": "shell:Downloads",
        "documents": "shell:Documents",
        "pictures": "shell:Pictures",
        "photos": "shell:Pictures",
        "videos": "shell:Videos",
        "music": "shell:Music",
        "desktop": "shell:Desktop",
    }

    key = name.strip().lower()

    if key in mapping:
        if speak:
            speak(f"Opening {key}.")
        open_explorer_shell(mapping[key])
        return True

    return False
