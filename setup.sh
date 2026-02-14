#!/usr/bin/env bash
# Universal Setup Script for Human Detection Camera
# Works on: Arch, Ubuntu/Debian, Fedora, and other Linux distributions

echo "=========================================="
echo "Human Detection Camera - Universal Setup"
echo "=========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    echo "Detected: Linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
    echo "Detected: macOS"
else
    echo "This script is for Linux/macOS only."
    echo "For Windows, please run: setup_windows.bat"
    exit 1
fi

# Detect Linux distribution
if [ "$OS" = "linux" ]; then
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
        echo "Distribution: $NAME"
    else
        DISTRO="unknown"
        echo "Could not detect distribution"
    fi
fi

echo ""
echo "Installing system packages..."
echo ""

# Install based on package manager
if [ "$OS" = "linux" ]; then
    case "$DISTRO" in
        arch|manjaro|endeavouros)
            echo "Using pacman..."
            sudo pacman -S --needed python-opencv python-numpy python-pyqt5 xdotool
            SYSTEM_INSTALL=$?
            ;;
        
        ubuntu|debian|linuxmint|pop)
            echo "Using apt..."
            sudo apt update
            sudo apt install -y python3-opencv python3-numpy python3-pyqt5 xdotool
            SYSTEM_INSTALL=$?
            ;;
        
        fedora|rhel|centos)
            echo "Using dnf..."
            sudo dnf install -y python3-opencv python3-numpy python3-pyqt5 xdotool
            SYSTEM_INSTALL=$?
            ;;
        
        opensuse*)
            echo "Using zypper..."
            sudo zypper install -y python3-opencv python3-numpy python3-qt5 xdotool
            SYSTEM_INSTALL=$?
            ;;
        
        *)
            echo "⚠ Unknown distribution: $DISTRO"
            echo "Skipping system package installation."
            echo "You may need to install these packages manually:"
            echo "  - OpenCV for Python"
            echo "  - NumPy"
            echo "  - PyQt5"
            echo "  - xdotool"
            SYSTEM_INSTALL=1
            ;;
    esac
    
    if [ $SYSTEM_INSTALL -ne 0 ]; then
        echo ""
        echo "⚠ System package installation had issues."
        echo "Continuing with pip installation..."
    else
        echo "✓ System packages installed successfully!"
    fi
fi

echo ""
echo "Installing Python packages via pip..."
echo ""

# List of pip packages
PIP_PACKAGES="pynput"

# Try different pip installation methods
install_with_pip() {
    local method=$1
    local cmd=$2
    
    echo "Method $method: $cmd"
    
    for package in $PIP_PACKAGES; do
        if eval "$cmd $package" 2>/dev/null; then
            echo "  ✓ Installed $package"
        else
            return 1
        fi
    done
    return 0
}

# Method 1: pip with --user
if install_with_pip 1 "python3 -m pip install --user"; then
    PIP_SUCCESS=true
# Method 2: pip with --break-system-packages (for newer systems)
elif install_with_pip 2 "python3 -m pip install --break-system-packages"; then
    PIP_SUCCESS=true
# Method 3: Try python instead of python3
elif install_with_pip 3 "python -m pip install --user"; then
    PIP_SUCCESS=true
else
    PIP_SUCCESS=false
fi

echo ""

if [ "$PIP_SUCCESS" = true ]; then
    echo "=========================================="
    echo "✓ Installation Complete!"
    echo "=========================================="
    echo ""
    echo "You can now run the application:"
    echo "  python3 human_detection_app.py"
    echo ""
    echo "Or:"
    echo "  python human_detection_app.py"
    echo ""
else
    echo "=========================================="
    echo "⚠ Automatic pip installation failed"
    echo "=========================================="
    echo ""
    echo "Please install pynput manually using one of these methods:"
    echo ""
    echo "Method 1: pip with --user"
    echo "  pip install --user pynput"
    echo ""
    echo "Method 2: Virtual environment (recommended)"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install pynput opencv-python numpy PyQt5"
    echo "  python human_detection_app.py"
    echo ""
    echo "Method 3: AUR (Arch-based only)"
    echo "  yay -S python-pynput"
    echo ""
    exit 1
fi