"""
CMD Hotkey Fixer - Windows Explorer Bug Workaround
Opens CMD as administrator via keyboard shortcut to fix frozen taskbar/explorer issues.
"""

import ctypes
import sys
import logging
import time
from pathlib import Path
from threading import Lock, Timer, Thread
import keyboard
import psutil


TEST_MODE = '--test' in sys.argv


class CMDHotkeyFixer:
    """Keyboard hotkey listener that opens CMD with administrator privileges"""
    
    # Hotkey configuration - choose one by uncommenting
    HOTKEY_OPTIONS = {
        'default': 'ctrl+alt+shift+c',     # Recommended: Easy to remember, unlikely conflict
        'option1': 'ctrl+shift+f12',       # F-key combination
        'option2': 'ctrl+shift+`',         # Backtick key
        'option3': 'win+shift+f11',        # Windows key combo
        'option4': 'ctrl+alt+home',        # Home key combo
    }
    
    def __init__(self):
        self.hotkey = self.HOTKEY_OPTIONS['default']
        self.cooldown_lock = Lock()
        self.is_on_cooldown = False
        self.cooldown_seconds = 1.0
        self.log_path = Path.home() / 'CMDHotkeyFixer.log'
        self.auto_close_delay = 1.5  # Seconds before auto-closing CMD
        self.cmd_start_time = None
        
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging to user's home directory"""
        handlers = [logging.FileHandler(str(self.log_path), encoding='utf-8')]
        
        # Add console output in test mode
        if TEST_MODE:
            handlers.append(logging.StreamHandler(sys.stdout))
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=handlers,
            force=True
        )
        
        self.logger = logging.getLogger(__name__)
        
        # Log initialization
        self.logger.info('=' * 60)
        self.logger.info('CMD Hotkey Fixer - Starting')
        self.logger.info(f'Log file: {self.log_path}')
        self.logger.info(f'Hotkey: {self.hotkey.upper()}')
        self.logger.info(f'Test mode: {TEST_MODE}')
        self.logger.info('=' * 60)
        
        if TEST_MODE:
            print(f'\n{"=" * 60}')
            print(f'TEST MODE ACTIVE')
            print(f'Log file: {self.log_path}')
            print(f'Hotkey: {self.hotkey.upper()}')
            print(f'{"=" * 60}\n')
    
    def reset_cooldown(self):
        """Reset cooldown flag after specified delay"""
        with self.cooldown_lock:
            self.is_on_cooldown = False
    
    def find_and_close_cmd(self):
        """Find and close CMD windows that were recently opened"""
        try:
            self.logger.info('Searching for CMD windows to close...')
            
            closed_count = 0
            
            # Find all CMD processes
            for proc in psutil.process_iter(['pid', 'name', 'create_time']):
                try:
                    if proc.info['name'].lower() == 'cmd.exe':
                        # Check if this CMD was created around the time we opened it
                        proc_age = time.time() - proc.info['create_time']
                        
                        # Only close CMD windows created in the last few seconds
                        if proc_age < 5:
                            self.logger.info(f'Closing CMD process (PID: {proc.info["pid"]})')
                            
                            # Try graceful close first
                            proc.terminate()
                            
                            # Wait a bit, then force kill if still running
                            try:
                                proc.wait(timeout=1)
                            except psutil.TimeoutExpired:
                                proc.kill()
                            
                            closed_count += 1
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            if closed_count > 0:
                self.logger.info(f'✓ Closed {closed_count} CMD window(s)')
                if TEST_MODE:
                    print(f'✓ CMD auto-closed ({closed_count} window(s))')
            else:
                self.logger.info('No recent CMD windows found to close')
                
        except Exception as e:
            self.logger.error(f'Error closing CMD: {type(e).__name__}: {e}')
    
    def close_cmd_windows(self):
        """Close all CMD windows after a delay"""
        time.sleep(self.auto_close_delay)
        self.find_and_close_cmd()
    
    def open_cmd_admin(self):
        """Open CMD with administrator privileges (with debounce protection)"""
        # Prevent multiple rapid triggers
        with self.cooldown_lock:
            if self.is_on_cooldown:
                self.logger.debug('Hotkey ignored - cooldown active')
                return
            self.is_on_cooldown = True
        
        # Schedule cooldown reset
        Timer(self.cooldown_seconds, self.reset_cooldown).start()
        
        try:
            self.logger.info(f'Hotkey triggered: {self.hotkey.upper()}')
            self.logger.info('Opening CMD as administrator...')
            
            # Open CMD with administrator privileges using Windows Shell API
            result = ctypes.windll.shell32.ShellExecuteW(
                None,           # Parent window handle
                'runas',        # Operation: run as administrator
                'cmd.exe',      # Program to execute
                None,           # Parameters
                None,           # Working directory
                1               # Show command: SW_SHOWNORMAL
            )
            
            # ShellExecuteW returns > 32 on success
            if result > 32:
                self.cmd_start_time = time.time()
                self.logger.info('✓ CMD opened successfully')
                if TEST_MODE:
                    print('✓ CMD opened successfully')
                
                # Start auto-close timer in background thread
                close_thread = Thread(target=self.close_cmd_windows, daemon=True)
                close_thread.start()
                
            else:
                self.logger.warning(f'ShellExecute returned error code: {result}')
                if TEST_MODE:
                    print(f'⚠ Warning: ShellExecute returned code {result}')
                
        except Exception as e:
            self.logger.error(f'✗ Failed to open CMD: {type(e).__name__}: {e}')
            if TEST_MODE:
                print(f'✗ Error: {e}')
    
    def run(self):
        """Start the hotkey listener"""
        try:
            self.logger.info(f'Listener active - waiting for {self.hotkey.upper()}')
            
            if TEST_MODE:
                print('Listener is now active!')
                print(f'Press {self.hotkey.upper()} to test')
                print('Press Ctrl+C to exit\n')
            
            # Register the hotkey
            keyboard.add_hotkey(self.hotkey, self.open_cmd_admin, suppress=False)
            
            # Keep program running
            keyboard.wait()
            
        except Exception as e:
            self.logger.critical(f'Critical error in listener: {type(e).__name__}: {e}')
            if TEST_MODE:
                print(f'\n✗ CRITICAL ERROR: {e}')
            sys.exit(1)
    
    def stop(self):
        """Cleanup and stop the listener"""
        self.logger.info('Stopping CMD Hotkey Fixer')
        keyboard.unhook_all()
        if TEST_MODE:
            print('\nStopped.')


def main():
    """Entry point for the application"""
    fixer = None
    try:
        fixer = CMDHotkeyFixer()
        fixer.run()
    except KeyboardInterrupt:
        if fixer:
            fixer.stop()
        sys.exit(0)
    except Exception as e:
        if fixer:
            fixer.logger.critical(f'Unhandled exception: {type(e).__name__}: {e}')
        else:
            print(f'Critical error during initialization: {e}')
        sys.exit(1)


if __name__ == '__main__':
    main()