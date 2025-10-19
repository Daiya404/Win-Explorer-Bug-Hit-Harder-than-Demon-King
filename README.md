# Admin CMD Hotkey for Windows Explorer Bug

This is a simple Python script for Windows that registers a global hotkey (`Ctrl+Shift+F12`) to open an administrative Command Prompt. It was created as a practical workaround for a specific Windows bug where mouse clicks on the taskbar and in Explorer windows become unresponsive.

## The Problem

On certain Windows systems, a bug can occur where the `explorer.exe` process stops responding to mouse clicks. While the mouse cursor still moves, you cannot click on the taskbar, Start Menu, or interact with open folder windows.

A known manual fix for this issue is to open the Task Manager (`Ctrl+Shift+Esc`), run a new task, and open `cmd.exe` with administrative privileges. This action somehow resets the state of Explorer and restores mouse functionality.

This script automates that fix, binding it to a single, convenient hotkey.

## How It Works

The script uses Python's built-in `ctypes` library to interact directly with the Windows API.

1.  **Register Hotkey**: It calls the `RegisterHotKey` function from `user32.dll` to register the `Ctrl+Shift+F12` key combination system-wide. This means the hotkey will work no matter what application you are currently using.
2.  **Message Loop**: The script enters a message loop, listening for Windows messages. When the registered hotkey is pressed, Windows sends a `WM_HOTKEY` message, which the script intercepts.
3.  **Execute Command**: Upon detecting the hotkey press, it uses `shell32.dll`'s `ShellExecuteW` function to launch `cmd.exe` with the `runas` verb, which triggers a User Account Control (UAC) prompt to grant it administrator privileges.

A log file named `AdventurerGuild.log` is created in your user's home directory (`C:\Users\YourUsername`) to record when the script starts and when the hotkey is triggered.

## How to Use

### Prerequisites

- Windows OS
- Python 3 installed (make sure to add Python to your system's PATH during installation).

### 1. Running the Script Manually

You can run the script directly from a terminal. It will run in the foreground, and the hotkey will remain active as long as the terminal window is open.

1.  Download the `FKYOUMICROSOFT.py` script and save it to a permanent location on your computer.
2.  Open a Command Prompt or PowerShell.
3.  Navigate to the directory where you saved the file.
    ```cmd
    cd C:\Path\To\Your\Script
    ```
4.  Run the script using Python.
    ```cmd
    python FKYOUMICROSOFT.py
    ```
    You should see a message confirming that the hotkey was successfully registered. You can now minimize this window.

### 2. Running the Script in the Background

To avoid keeping a terminal window open, you can run the script with `pythonw.exe`, which executes it without a console window.

1.  Open a Command Prompt or PowerShell.
2.  Run the following command:
    `cmd
    pythonw.exe C:\Path\To\Your\Script\FKYOUMICROSOFT.py
    `
    The script will now be running silently in the background. To stop it, you will need to use the Task Manager to find and end the `pythonw.exe` process.

### 3. Running Automatically on Startup (Recommended)

For the most convenient use, you can set the script to run automatically every time you log in to Windows.

1.  Right-click on your desktop and select **New > Shortcut**.
2.  In the "Type the location of the item" box, enter the following command, making sure to replace the path with the actual path to your script:
    ```
    pythonw.exe C:\Path\To\Your\Script\FKYOUMICROSOFT.py
    ```
3.  Click **Next**, give the shortcut a name (e.g., "Hotkey Fix"), and click **Finish**.
4.  Press `Win + R` to open the Run dialog.
5.  Type `shell:startup` and press Enter. This will open your user's Startup folder.
6.  Move the shortcut you just created into this Startup folder.

Now, the script will start automatically and silently in the background every time you log in, and the `Ctrl+Shift+F12` hotkey will always be ready.

## Potential Issues

- **Hotkey Conflict:** If another application has already registered `Ctrl+Shift+F12` as a global hotkey, this script will fail to register it. The log file will contain an error message in this case.
- **Antivirus Software:** Some antivirus programs may flag this script as suspicious because it registers a global hotkey and attempts to run a program with administrator rights. This is expected behavior for this type of utility. You may need to add an exception for the script in your antivirus software.

## Disclaimer

This script interacts with core Windows system functions. Please review the code to ensure you understand what it does before running it. Use it at your own risk.
