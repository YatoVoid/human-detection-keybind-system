
<img width="1483" height="937" alt="Pasted image" src="https://github.com/user-attachments/assets/8fd95270-5dee-4178-bff8-2e60fbb1046d" />
<img width="1483" height="937" alt="Pasted image (2)" src="https://github.com/user-attachments/assets/2cc5d83f-da68-4397-bd78-562ca7aeaa98" />


# Human Detection Camera System

A cross-platform application that detects humans via camera and triggers custom keyboard shortcuts. Works seamlessly on Windows and Linux with automatic dependency installation.

## Features

- 🎥 **Automatic Camera Detection** - Detects all available cameras on your system
- 👤 **Human Detection** - Uses computer vision to detect humans in real-time
- ⌨️ **Custom Keybinds** - Configure multiple keyboard shortcuts to trigger when humans are detected
- 🎯 **Key Recording** - Click "Record" to automatically capture your keypresses instead of typing them
- 🔧 **Auto-Install Dependencies** - Automatically installs all required packages
- 💾 **Settings Persistence** - Saves your configuration for next time
- 🖥️ **Cross-Platform** - Works on both Windows and Linux
- 🎨 **Easy-to-Use GUI** - Simple, intuitive interface

## Setup Scripts Explained

### `setup.sh` - Universal Linux/macOS Setup
- Auto-detects your Linux distribution (Arch, Ubuntu, Debian, Fedora, openSUSE, etc.)
- Uses the appropriate package manager (pacman, apt, dnf, zypper)
- Installs system packages and Python dependencies
- Falls back to pip if system packages unavailable

### `setup_arch.sh` - Arch Linux Optimized
- Specifically designed for Arch Linux
- Handles AUR packages (python-pynput)
- Installs xdotool for better keybind support

### `setup_windows.bat` - Windows Batch Script
- Double-click to run
- Checks if Python is installed
- Installs all dependencies via pip
- User-friendly with pause prompts

### `setup_windows.ps1` - Windows PowerShell
- Alternative to batch script
- Better error handling and colored output
- Shows detailed installation progress

### `run_app.bat` - Windows Quick Launcher
- Double-click to start the app
- No need to open command prompt
- Shows errors if app crashes

## How to Use

## Quick Start

### 🐧 Linux (All Distributions)
**One-command setup (Arch, Ubuntu, Debian, Fedora, openSUSE):**
```bash
chmod +x setup.sh
./setup.sh
python3 human_detection_app.py
```

The script auto-detects your distribution and installs packages accordingly.

**Arch Linux specific:**
```bash
chmod +x setup_arch.sh
./setup_arch.sh
python human_detection_app.py
```

### 🪟 Windows
**Method 1: Batch Script (Recommended)**
1. Double-click `setup_windows.bat`
2. Wait for installation to complete
3. Double-click `run_app.bat` to start the app

**Method 2: PowerShell Script**
1. Right-click `setup_windows.ps1` → "Run with PowerShell"
2. Follow the prompts
3. Run: `python human_detection_app.py`

**Method 3: Manual**
```cmd
pip install opencv-python numpy PyQt5 pynput
python human_detection_app.py
```

### 🍎 macOS
```bash
chmod +x setup.sh
./setup.sh
python3 human_detection_app.py
```

### Manual Installation (Any OS)
If you prefer to install dependencies first:

**Arch Linux:**
```bash
sudo pacman -S python-opencv python-numpy python-pyqt5 xdotool
# Then install pynput via AUR or pip:
yay -S python-pynput  # OR: pip install --user pynput
```

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install python3-opencv python3-numpy python3-pyqt5 python3-pynput xdotool
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-opencv python3-numpy python3-pyqt5 python3-pynput xdotool
```

**openSUSE:**
```bash
sudo zypper install python3-opencv python3-numpy python3-qt5 xdotool
pip install --user pynput
```

**Windows:**
```cmd
pip install opencv-python numpy PyQt5 pynput
```

**macOS:**
```bash
pip install opencv-python numpy PyQt5 pynput
```

## How to Use

1. **Launch the Application**
   - Run the script using the command above
   - The app will auto-install any missing dependencies

2. **Select Camera**
   - Choose your camera from the dropdown menu
   - Click "Refresh Cameras" if you don't see your camera

3. **Configure Keybinds**
   - Click "+ Add Keybind" to add keyboard shortcuts
   - Enter a name (e.g., "Close All Windows")
   - **Click "Record" button** and press your desired key combination
   - Or manually type the keys (e.g., "super+d" or "alt+f4")
   - The keys will be detected automatically when recording
   - Add multiple keybinds as needed

4. **Adjust Settings**
   - **Confidence**: Detection sensitivity (50% is good default)
   - **Cooldown**: Minimum seconds between triggers (prevents spam)

5. **Start Detection**
   - Click "Start Detection" button
   - When a human is detected, all configured keybinds will trigger

6. **Save Settings**
   - Click "Save Settings" to persist your configuration
   - Settings auto-load on next startup

## Keybind Examples

### Windows
- `win+d` - Show desktop / Minimize all windows
- `alt+f4` - Close active window
- `win+l` - Lock computer
- `ctrl+shift+esc` - Open Task Manager
- `alt+tab` - Switch windows

### Linux
- `ctrl+alt+d` - Show desktop
- `alt+f4` - Close window
- `ctrl+alt+l` - Lock screen
- `super+d` - Minimize all windows
- `ctrl+alt+delete` - System monitor

### Supported Keys
- **Modifiers**: `ctrl`, `alt`, `shift`, `win`, `cmd`
- **Special**: `esc`, `enter`, `tab`, `space`, `backspace`, `delete`
- **Arrow Keys**: `up`, `down`, `left`, `right`
- **Function**: `f1` through `f12`
- **Any letter/number**: `a`, `1`, etc.

## Requirements

The script will auto-install these if missing:
- Python 3.6+
- opencv-python
- numpy
- PyQt5
- pynput

## Troubleshooting

### "Externally-Managed Environment" Error (Arch/Modern Linux)
This is a PEP 668 restriction on newer Linux distributions. Use one of these solutions:

**Solution 1: System packages (Recommended)**
```bash
./setup_arch.sh  # For Arch Linux
# Or manually: sudo pacman -S python-opencv python-numpy python-pyqt5 python-pynput
```

**Solution 2: User installation**
The script will automatically try this method.

**Solution 3: Virtual environment**
```bash
python -m venv venv
source venv/bin/activate
pip install opencv-python numpy PyQt5 pynput
python human_detection_app.py
```

### Camera Not Detected
- Ensure your camera is connected and not in use by another application
- Try clicking "Refresh Cameras"
- Check camera permissions in your OS settings

### Detection Not Working
- Ensure good lighting conditions
- Position yourself clearly in frame
- Adjust the confidence slider
- Detection works best with full body or upper body visibility

### Keybinds Not Triggering
- Verify keybind format (use lowercase, + between keys)
- Some key combinations may be reserved by your OS
- Test with simple keybinds first (e.g., single letter)
- Check that cooldown period hasn't blocked the trigger
- **Linux users:** Install `xdotool` for better keybind reliability
  ```bash
  sudo pacman -S xdotool  # Arch
  sudo apt install xdotool  # Debian/Ubuntu
  ```

### Permission Issues (Linux)
If camera access is denied:
```bash
sudo usermod -a -G video $USER
# Then log out and log back in
```

### Import Errors
If auto-install fails, manually install:
```bash
pip install --upgrade pip
pip install opencv-python numpy PyQt5 pynput
```

## Use Cases

- **Privacy Protection**: Minimize windows when someone approaches
- **Security**: Lock screen when motion detected
- **Automation**: Close specific apps when someone enters room
- **Parental Controls**: Switch to appropriate content when detected
- **Office Productivity**: Auto-hide sensitive information

## Technical Details

- **Detection Method**: OpenCV Haar Cascade Classifiers
- **Detection Types**: Full body and upper body
- **Frame Rate**: ~30 FPS
- **Latency**: <100ms from detection to keybind trigger
- **Resource Usage**: Low (1-5% CPU on modern systems)

## File Structure

```
human_detection_app.py       # Main application
detection_settings.json      # Saved settings (auto-created)

# Setup scripts
setup.sh                     # Universal Linux/macOS setup
setup_arch.sh                # Arch Linux specific setup
setup_windows.bat            # Windows batch setup
setup_windows.ps1            # Windows PowerShell setup
run_app.bat                  # Windows quick launcher

README.md                    # This file
```

## License

Free to use and modify for personal and commercial purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Verify your Python version is 3.6+
3. Ensure camera permissions are granted
4. Test with default settings first

## Version

1.0.0 - Initial Release
