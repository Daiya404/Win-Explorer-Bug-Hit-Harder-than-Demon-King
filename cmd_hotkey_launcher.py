

import sys
import ctypes
import ctypes.wintypes
import time
from pathlib import Path
from datetime import datetime
from threading import Thread

# Standard values of Windows OS
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
WM_HOTKEY = 0x0312
VK_F12 = 0x7B

# Unique ID for our hotkey
HOTKEY_ID = 1

# logging function
def log(message):
    log_file = Path.home() / 'CMDFixer.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass

# spam prot
last_trigger_time = 0
cooldown = 2.0  

def trigger_hotkey():
    global last_trigger_time
    current_time = time.time()
    
    if current_time - last_trigger_time < cooldown:
        log("Cooldown active, ignoring trigger.")
        return
        
    last_trigger_time = current_time
    log("HOTKEY TRIGGERED")
    Thread(target=open_cmd, daemon=True).start()

def open_cmd():
    try:
        command_string = '/k "echo CMD Hotkey Fixer - Working... & timeout /t 1 /nobreak >nul & exit"'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", command_string, None, 1)
    except Exception as e:
        log(f"✗ Exception during CMD execution: {e}")

def main():
    log("=" * 70)
    log("CMD HOTKEY FIXER STARTING (Windows API Version)")
    log("Hotkey: Ctrl+Shift+F12")
    log("=" * 70)

    # to ensure the hotkey is always unregistered on exit
    try:
        log("Registering hotkey with Windows...")
        
        # core function
        if not ctypes.windll.user32.RegisterHotKey(None, HOTKEY_ID, MOD_CONTROL | MOD_SHIFT, VK_F12):
            log("✗ Failed to register hotkey. Another program may be using it.")
            ctypes.windll.user32.MessageBoxW(0, "Failed to register hotkey.\nAnother program may be using Ctrl+Shift+F12.", "Error", 0x10)
            return 1
            
        log("✓ Hotkey registered successfully. Waiting for messages.")
        
        # "message loop"
        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == WM_HOTKEY:
                if msg.wParam == HOTKEY_ID:
                    trigger_hotkey()

    except Exception as e:
        log(f"CRITICAL ERROR: {e}")
        return 1
        
    finally:
        log("Unregistering hotkey...")
        ctypes.windll.user32.UnregisterHotKey(None, HOTKEY_ID)
        log("✓ Cleanup complete. Exiting.")
            
    return 0

if __name__ == '__main__':
    sys.exit(main())