#!/bin/bash
# Quick test script for PKGBUILD

echo "=========================================="
echo "Testing PKGBUILD"
echo "=========================================="
echo ""

# Check if in correct directory
if [ ! -f "PKGBUILD" ]; then
    echo "Error: PKGBUILD not found in current directory"
    exit 1
fi

echo "Step 1: Cleaning previous builds..."
rm -rf src/ pkg/ *.pkg.tar.zst

echo ""
echo "Step 2: Building package..."
makepkg -f

if [ $? -eq 0 ]; then
    echo ""
    echo "Step 3: Installing package..."
    sudo pacman -U *.pkg.tar.zst
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "=========================================="
        echo "✓ Package installed successfully!"
        echo "=========================================="
        echo ""
        echo "Test the application:"
        echo "  human-detection-camera"
        echo ""
        echo "Or from application menu"
        echo ""
        echo "To uninstall:"
        echo "  sudo pacman -R human-detection-camera"
        echo ""
    else
        echo ""
        echo "✗ Installation failed"
    fi
else
    echo ""
    echo "✗ Build failed"
    exit 1
fi
