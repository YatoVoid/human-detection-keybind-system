#!/bin/bash
# Setup script for Arch Linux users

echo "=========================================="
echo "Human Detection Camera - Arch Linux Setup"
echo "=========================================="
echo ""

echo "Installing required packages via pacman..."
sudo pacman -S --needed python-opencv python-numpy python-pyqt5

if [ $? -ne 0 ]; then
    echo ""
    echo "✗ Pacman installation failed. Please check the errors above."
    exit 1
fi

echo ""
echo "Installing python-pynput via pip (not in official repos)..."

# Try pip install with --user first
if python -m pip install --user pynput 2>/dev/null; then
    echo "✓ Installed pynput via pip --user"
elif python -m pip install --break-system-packages pynput 2>/dev/null; then
    echo "✓ Installed pynput via pip --break-system-packages"
else
    echo ""
    echo "⚠ Could not install pynput automatically."
    echo ""
    echo "Option 1: Install from AUR (recommended)"
    echo "  yay -S python-pynput"
    echo "  # or: paru -S python-pynput"
    echo ""
    echo "Option 2: Install via pip"
    echo "  pip install --user pynput"
    echo ""
    echo "Option 3: Use virtual environment"
    echo "  python -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install pynput"
    echo ""
    exit 1
fi

echo ""
echo "✓ All dependencies installed successfully!"
echo ""
echo "You can now run the application:"
echo "  python human_detection_app.py"
echo ""
