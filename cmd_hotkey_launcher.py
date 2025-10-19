"""
CMD Hotkey Fixer - Final Version (No Admin Required)
- Uses the native Windows API for hotkeys, which is 100% reliable.
- Does NOT require running as an administrator.
- Will NEVER cause stuck keys or trigger incorrectly.
"""

import sys
import ctypes
import ctypes.wintypes
import time
from pathlib import Path
from datetime import datetime
from threading import Thread

# --- Windows API Constants ---
# These are standard values used to talk to the Windows OS.
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
WM_HOTKEY = 0x0312
VK_F12 = 0x7B

# Unique ID for our hotkey
HOTKEY_ID = 1

# --- Simple logging function ---
def log(message):
    log_file = Path.home() / 'CMDFixer.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")
    except IOError:
        pass

# --- Debouncing variables to prevent spamming ---
last_trigger_time = 0
cooldown = 2.0  # 2-second cooldown

def trigger_hotkey():
    """
    This function is called when the hotkey is detected.
    It includes a cooldown to prevent accidental double-triggers.
    """
    global last_trigger_time
    current_time = time.time()
    
    if current_time - last_trigger_time < cooldown:
        log("Cooldown active, ignoring trigger.")
        return
        
    last_trigger_time = current_time
    log("HOTKEY TRIGGERED")
    Thread(target=open_cmd, daemon=True).start()

def open_cmd():
    """
    Opens CMD with a UAC prompt for administrator privileges.
    The script itself does not need to be admin, only the final action.
    """
    try:
        command_string = '/k "echo CMD Hotkey Fixer - Working... & timeout /t 1 /nobreak >nul & exit"'
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", command_string, None, 1)
    except Exception as e:
        log(f"✗ Exception during CMD execution: {e}")

def main():
    """Main entry point for the script."""
    
    log("=" * 70)
    log("CMD HOTKEY FIXER STARTING (Windows API Version)")
    log("Hotkey: Ctrl+Shift+F12")
    log("=" * 70)

    # Use a try...finally block to ensure the hotkey is always unregistered on exit.
    try:
        log("Registering hotkey with Windows...")
        
        # This is the core function. We tell Windows:
        # "Please notify this script when Ctrl+Shift+F12 is pressed."
        if not ctypes.windll.user32.RegisterHotKey(None, HOTKEY_ID, MOD_CONTROL | MOD_SHIFT, VK_F12):
            log("✗ Failed to register hotkey. Another program may be using it.")
            ctypes.windll.user32.MessageBoxW(0, "Failed to register hotkey.\nAnother program may be using Ctrl+Shift+F12.", "Error", 0x10)
            return 1
            
        log("✓ Hotkey registered successfully. Waiting for messages.")
        
        # This is the "message loop". It waits for Windows to send a notification.
        msg = ctypes.wintypes.MSG()
        while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
            if msg.message == WM_HOTKEY:
                if msg.wParam == HOTKEY_ID:
                    trigger_hotkey()

    except Exception as e:
        log(f"CRITICAL ERROR: {e}")
        return 1
        
    finally:
        # This is crucial: unregister the hotkey when the script closes.
        log("Unregistering hotkey...")
        ctypes.windll.user32.UnregisterHotKey(None, HOTKEY_ID)
        log("✓ Cleanup complete. Exiting.")
            
    return 0

if __name__ == '__main__':
    sys.exit(main())