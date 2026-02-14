# Universal Setup Script for Human Detection Camera - Windows (PowerShell)
# Automatically installs all required Python packages

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Human Detection Camera - Windows Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python is installed: $pythonVersion" -ForegroundColor Green
    Write-Host ""
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python from: https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Installing required packages..." -ForegroundColor Yellow
Write-Host ""

# List of packages to install
$packages = @("opencv-python", "numpy", "PyQt5", "pynput")

$failedPackages = @()

foreach ($package in $packages) {
    Write-Host "Installing $package..." -ForegroundColor Cyan
    
    try {
        $output = python -m pip install $package 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Installed $package" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Failed to install $package" -ForegroundColor Red
            $failedPackages += $package
        }
    } catch {
        Write-Host "  ✗ Error installing $package" -ForegroundColor Red
        $failedPackages += $package
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan

if ($failedPackages.Count -eq 0) {
    Write-Host "✓ Installation Complete!" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now run the application:" -ForegroundColor Yellow
    Write-Host "  python human_detection_app.py"
    Write-Host ""
    Write-Host "Or double-click on: run_app.bat"
} else {
    Write-Host "⚠ Installation completed with errors" -ForegroundColor Yellow
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Failed packages:" -ForegroundColor Red
    foreach ($pkg in $failedPackages) {
        Write-Host "  - $pkg" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please try installing manually:" -ForegroundColor Yellow
    Write-Host "  pip install $($failedPackages -join ' ')"
}

Write-Host ""
Read-Host "Press Enter to exit"