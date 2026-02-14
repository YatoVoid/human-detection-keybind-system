#!/usr/bin/env python3
"""
Cross-Platform Human Detection Camera Application
Detects humans via camera and triggers custom keybinds
Works on Windows and Linux with automatic dependency installation
"""

import sys
import os
import subprocess
import platform

# Auto-install required packages
def install_requirements():
    """Install required packages if missing"""
    required_packages = {
        'opencv-python': 'cv2',
        'numpy': 'numpy',
        'PyQt5': 'PyQt5',
        'pynput': 'pynput'
    }
    
    # Map package names to system package names for common distros
    arch_packages = {
        'opencv-python': 'python-opencv',
        'numpy': 'python-numpy',
        'PyQt5': 'python-pyqt5',
        # pynput not in official repos, will use pip/AUR
    }
    
    missing_packages = []
    missing_imports = []
    
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package)
            missing_imports.append(import_name)
    
    if missing_packages:
        print(f"\n{'='*60}")
        print(f"Missing packages detected: {', '.join(missing_packages)}")
        print(f"{'='*60}\n")
        
        # Try different installation methods
        install_success = False
        
        # Method 1: Try pip install with --user flag first
        print("Method 1: Trying pip install --user...")
        try:
            for package in missing_packages:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', package])
                print(f"  ✓ Installed {package}")
            install_success = True
            print("\n✓ All dependencies installed successfully!\n")
        except subprocess.CalledProcessError:
            print("  ✗ --user installation failed")
        
        # Method 2: Try with virtual environment
        if not install_success:
            print("\nMethod 2: Creating virtual environment...")
            venv_path = os.path.join(os.path.dirname(__file__) or '.', 'venv')
            try:
                if not os.path.exists(venv_path):
                    subprocess.check_call([sys.executable, '-m', 'venv', venv_path])
                    print(f"  ✓ Created virtual environment at: {venv_path}")
                
                # Determine pip path in venv
                if platform.system() == "Windows":
                    pip_path = os.path.join(venv_path, 'Scripts', 'pip')
                else:
                    pip_path = os.path.join(venv_path, 'bin', 'pip')
                
                for package in missing_packages:
                    subprocess.check_call([pip_path, 'install', package])
                    print(f"  ✓ Installed {package}")
                
                print(f"\n{'='*60}")
                print("Virtual environment created successfully!")
                print(f"To run this app, use:")
                if platform.system() == "Windows":
                    print(f"  {os.path.join(venv_path, 'Scripts', 'python')} {__file__}")
                else:
                    print(f"  {os.path.join(venv_path, 'bin', 'python')} {__file__}")
                print(f"{'='*60}\n")
                sys.exit(0)
                
            except Exception as e:
                print(f"  ✗ Virtual environment creation failed: {e}")
        
        # Method 3: System package manager (Linux only)
        if not install_success and platform.system() == "Linux":
            print("\nMethod 3: Checking system package manager...")
            
            # Detect package manager
            pkg_manager = None
            install_cmd = None
            
            if os.path.exists('/usr/bin/pacman'):
                pkg_manager = 'pacman'
                print("  Detected: Arch Linux (pacman)")
                
                # Separate packages that are in official repos vs AUR/pip
                arch_pkgs = []
                pip_pkgs = []
                
                for pkg in missing_packages:
                    if pkg in arch_packages:
                        arch_pkgs.append(arch_packages[pkg])
                    else:
                        pip_pkgs.append(pkg)
                
                if arch_pkgs:
                    install_cmd = f"sudo pacman -S {' '.join(arch_pkgs)}"
                    if pip_pkgs:
                        install_cmd += f"\n  pip install --user {' '.join(pip_pkgs)}  # or use AUR"
                else:
                    install_cmd = f"pip install --user {' '.join(pip_pkgs)}"
            elif os.path.exists('/usr/bin/apt'):
                pkg_manager = 'apt'
                print("  Detected: Debian/Ubuntu (apt)")
                # Convert to debian package names
                debian_pkgs = [f"python3-{pkg.replace('opencv-python', 'opencv')}" 
                              for pkg in missing_packages]
                install_cmd = f"sudo apt install {' '.join(debian_pkgs)}"
            elif os.path.exists('/usr/bin/dnf'):
                pkg_manager = 'dnf'
                print("  Detected: Fedora (dnf)")
                fedora_pkgs = [f"python3-{pkg}" for pkg in missing_packages]
                install_cmd = f"sudo dnf install {' '.join(fedora_pkgs)}"
            
            if install_cmd:
                print(f"\n{'='*60}")
                print("MANUAL INSTALLATION REQUIRED")
                print(f"{'='*60}")
                print("\nPlease run the following command to install dependencies:\n")
                print(f"  {install_cmd}\n")
                print("Then run this script again.\n")
                print("Alternative: Create a virtual environment:")
                print(f"  python -m venv venv")
                print(f"  source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
                print(f"  pip install {' '.join(missing_packages)}")
                print(f"  python {os.path.basename(__file__)}")
                print(f"{'='*60}\n")
                sys.exit(1)
        
        # If we're here and still have missing packages, installation failed
        if not install_success:
            print(f"\n{'='*60}")
            print("INSTALLATION FAILED")
            print(f"{'='*60}")
            print("\nPlease install the required packages manually:\n")
            print(f"  pip install --user {' '.join(missing_packages)}")
            print("\nOr create a virtual environment:")
            print(f"  python -m venv venv")
            if platform.system() == "Windows":
                print(f"  venv\\Scripts\\activate")
            else:
                print(f"  source venv/bin/activate")
            print(f"  pip install {' '.join(missing_packages)}")
            print(f"{'='*60}\n")
            sys.exit(1)

# Install requirements before importing
install_requirements()

import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QTextEdit, QGroupBox, QSpinBox, QCheckBox,
                             QScrollArea, QMessageBox, QLineEdit)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QFont
from pynput.keyboard import Controller, Key
import time
import json

class KeybindWidget(QWidget):
    """Widget for configuring a single keybind"""
    removed = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name (e.g., Close All Windows)")
        self.name_input.setMinimumWidth(200)
        
        self.keys_input = QLineEdit()
        self.keys_input.setPlaceholderText("Keys (e.g., alt+f4 or win+d)")
        self.keys_input.setMinimumWidth(250)
        
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.clicked.connect(lambda: self.removed.emit(self))
        self.remove_btn.setMaximumWidth(80)
        
        layout.addWidget(QLabel("Name:"))
        layout.addWidget(self.name_input)
        layout.addWidget(QLabel("Keys:"))
        layout.addWidget(self.keys_input)
        layout.addWidget(self.remove_btn)
        
        self.setLayout(layout)
    
    def get_keybind(self):
        """Get the keybind configuration"""
        return {
            'name': self.name_input.text().strip(),
            'keys': self.keys_input.text().strip().lower()
        }
    
    def set_keybind(self, name, keys):
        """Set the keybind configuration"""
        self.name_input.setText(name)
        self.keys_input.setText(keys)

class HumanDetectionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Human Detection Camera System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize variables
        self.camera = None
        self.camera_index = 0
        self.available_cameras = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.keyboard = Controller()
        
        # Detection settings
        self.detection_enabled = False
        self.last_trigger_time = 0
        self.cooldown_seconds = 2
        self.confidence_threshold = 0.5
        
        # Keybinds
        self.keybind_widgets = []
        
        # Load cascade classifier for human detection
        self.load_detector()
        
        # Setup UI
        self.setup_ui()
        
        # Detect cameras
        self.detect_cameras()
        
        # Load saved settings
        self.load_settings()
    
    def load_detector(self):
        """Load the human detection model"""
        # Using Haar Cascade for full body detection
        cascade_path = cv2.data.haarcascades + 'haarcascade_fullbody.pkl'
        
        # Try multiple cascade options
        cascades = [
            'haarcascade_fullbody.xml',
            'haarcascade_upperbody.xml',
        ]
        
        self.cascades = []
        for cascade_name in cascades:
            try:
                cascade_path = cv2.data.haarcascades + cascade_name
                cascade = cv2.CascadeClassifier(cascade_path)
                if not cascade.empty():
                    self.cascades.append(cascade)
            except:
                pass
        
        if not self.cascades:
            print("Warning: Could not load human detection cascades")
    
    def setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title = QLabel("Human Detection Camera System")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Camera selection
        camera_group = QGroupBox("Camera Selection")
        camera_layout = QHBoxLayout()
        
        self.camera_combo = QComboBox()
        self.camera_combo.currentIndexChanged.connect(self.change_camera)
        camera_layout.addWidget(QLabel("Select Camera:"))
        camera_layout.addWidget(self.camera_combo)
        
        self.refresh_btn = QPushButton("Refresh Cameras")
        self.refresh_btn.clicked.connect(self.detect_cameras)
        camera_layout.addWidget(self.refresh_btn)
        
        camera_group.setLayout(camera_layout)
        main_layout.addWidget(camera_group)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Left side - Camera view
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.camera_label = QLabel()
        self.camera_label.setMinimumSize(640, 480)
        self.camera_label.setScaledContents(True)
        self.camera_label.setStyleSheet("border: 2px solid #333; background-color: #000;")
        left_layout.addWidget(self.camera_label)
        
        self.status_label = QLabel("Status: No camera selected")
        self.status_label.setFont(QFont("Arial", 10))
        left_layout.addWidget(self.status_label)
        
        content_layout.addWidget(left_widget, 2)
        
        # Right side - Controls
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Detection controls
        detection_group = QGroupBox("Detection Controls")
        detection_layout = QVBoxLayout()
        
        self.start_btn = QPushButton("Start Detection")
        self.start_btn.clicked.connect(self.toggle_detection)
        self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        detection_layout.addWidget(self.start_btn)
        
        # Confidence threshold
        conf_layout = QHBoxLayout()
        conf_layout.addWidget(QLabel("Confidence:"))
        self.confidence_spin = QSpinBox()
        self.confidence_spin.setRange(10, 100)
        self.confidence_spin.setValue(50)
        self.confidence_spin.setSuffix("%")
        self.confidence_spin.valueChanged.connect(self.update_confidence)
        conf_layout.addWidget(self.confidence_spin)
        detection_layout.addLayout(conf_layout)
        
        # Cooldown
        cooldown_layout = QHBoxLayout()
        cooldown_layout.addWidget(QLabel("Cooldown:"))
        self.cooldown_spin = QSpinBox()
        self.cooldown_spin.setRange(0, 60)
        self.cooldown_spin.setValue(2)
        self.cooldown_spin.setSuffix(" seconds")
        self.cooldown_spin.valueChanged.connect(self.update_cooldown)
        cooldown_layout.addWidget(self.cooldown_spin)
        detection_layout.addLayout(cooldown_layout)
        
        detection_group.setLayout(detection_layout)
        right_layout.addWidget(detection_group)
        
        # Keybinds
        keybind_group = QGroupBox("Keybinds (triggered on human detection)")
        keybind_layout = QVBoxLayout()
        
        # Scroll area for keybinds
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setMinimumHeight(200)
        
        self.keybind_container = QWidget()
        self.keybind_container_layout = QVBoxLayout(self.keybind_container)
        self.keybind_container_layout.setAlignment(Qt.AlignTop)
        scroll.setWidget(self.keybind_container)
        
        keybind_layout.addWidget(scroll)
        
        add_keybind_btn = QPushButton("+ Add Keybind")
        add_keybind_btn.clicked.connect(self.add_keybind)
        keybind_layout.addWidget(add_keybind_btn)
        
        # Help text
        help_text = QLabel(
            "Key format examples:\n"
            "• Single key: a, space, esc\n"
            "• Combo: ctrl+c, alt+f4, win+d\n"
            "• Multiple: ctrl+shift+esc\n\n"
            "Special keys: ctrl, alt, shift, win, cmd, esc, enter, tab, space"
        )
        help_text.setStyleSheet("color: #666; font-size: 9px;")
        help_text.setWordWrap(True)
        keybind_layout.addWidget(help_text)
        
        keybind_group.setLayout(keybind_layout)
        right_layout.addWidget(keybind_group)
        
        # Save settings button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.clicked.connect(self.save_settings)
        right_layout.addWidget(self.save_btn)
        
        right_layout.addStretch()
        
        content_layout.addWidget(right_widget, 1)
        main_layout.addLayout(content_layout)
        
        # Add default keybind
        self.add_keybind()
    
    def add_keybind(self):
        """Add a new keybind widget"""
        widget = KeybindWidget()
        widget.removed.connect(self.remove_keybind)
        self.keybind_widgets.append(widget)
        self.keybind_container_layout.addWidget(widget)
        
        # Set default for first keybind
        if len(self.keybind_widgets) == 1:
            if platform.system() == "Windows":
                widget.set_keybind("Minimize All Windows", "win+d")
            else:
                widget.set_keybind("Show Desktop", "ctrl+alt+d")
    
    def remove_keybind(self, widget):
        """Remove a keybind widget"""
        if len(self.keybind_widgets) > 0:
            self.keybind_widgets.remove(widget)
            widget.deleteLater()
    
    def detect_cameras(self):
        """Detect available cameras"""
        self.camera_combo.clear()
        self.available_cameras = []
        
        # Try first 10 camera indices
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                self.available_cameras.append(i)
                self.camera_combo.addItem(f"Camera {i}")
                cap.release()
        
        if not self.available_cameras:
            self.status_label.setText("Status: No cameras detected")
            QMessageBox.warning(self, "No Cameras", "No cameras were detected on your system.")
        else:
            self.status_label.setText(f"Status: Found {len(self.available_cameras)} camera(s)")
    
    def change_camera(self, index):
        """Change the active camera"""
        if index >= 0 and index < len(self.available_cameras):
            self.stop_camera()
            self.camera_index = self.available_cameras[index]
            self.start_camera()
    
    def start_camera(self):
        """Start the camera"""
        if self.camera is None or not self.camera.isOpened():
            self.camera = cv2.VideoCapture(self.camera_index)
            if self.camera.isOpened():
                self.timer.start(30)  # 30ms refresh rate
                self.status_label.setText(f"Status: Camera {self.camera_index} active")
            else:
                self.status_label.setText(f"Status: Failed to open camera {self.camera_index}")
    
    def stop_camera(self):
        """Stop the camera"""
        self.timer.stop()
        if self.camera is not None:
            self.camera.release()
            self.camera = None
    
    def toggle_detection(self):
        """Toggle human detection on/off"""
        self.detection_enabled = not self.detection_enabled
        
        if self.detection_enabled:
            self.start_btn.setText("Stop Detection")
            self.start_btn.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-weight: bold; padding: 10px; }")
            if not self.timer.isActive():
                self.start_camera()
        else:
            self.start_btn.setText("Start Detection")
            self.start_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
    
    def update_confidence(self, value):
        """Update confidence threshold"""
        self.confidence_threshold = value / 100.0
    
    def update_cooldown(self, value):
        """Update cooldown period"""
        self.cooldown_seconds = value
    
    def detect_humans(self, frame):
        """Detect humans in the frame"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        humans = []
        
        # Try each cascade
        for cascade in self.cascades:
            detected = cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            if len(detected) > 0:
                humans.extend(detected)
        
        return humans
    
    def parse_keybind(self, keys_string):
        """Parse keybind string into key objects"""
        if not keys_string:
            return []
        
        # Map of string to Key objects
        special_keys = {
            'ctrl': Key.ctrl,
            'alt': Key.alt,
            'shift': Key.shift,
            'win': Key.cmd if platform.system() == "Darwin" else Key.cmd,
            'cmd': Key.cmd,
            'esc': Key.esc,
            'enter': Key.enter,
            'tab': Key.tab,
            'space': Key.space,
            'backspace': Key.backspace,
            'delete': Key.delete,
            'up': Key.up,
            'down': Key.down,
            'left': Key.left,
            'right': Key.right,
            'f1': Key.f1, 'f2': Key.f2, 'f3': Key.f3, 'f4': Key.f4,
            'f5': Key.f5, 'f6': Key.f6, 'f7': Key.f7, 'f8': Key.f8,
            'f9': Key.f9, 'f10': Key.f10, 'f11': Key.f11, 'f12': Key.f12,
        }
        
        keys = []
        parts = keys_string.split('+')
        
        for part in parts:
            part = part.strip()
            if part in special_keys:
                keys.append(special_keys[part])
            elif len(part) == 1:
                keys.append(part)
            else:
                print(f"Warning: Unknown key '{part}'")
        
        return keys
    
    def trigger_keybind(self, keys):
        """Trigger a keybind"""
        if not keys:
            return
        
        try:
            # Press all keys
            for key in keys:
                self.keyboard.press(key)
            
            # Small delay
            time.sleep(0.05)
            
            # Release all keys in reverse order
            for key in reversed(keys):
                self.keyboard.release(key)
                
        except Exception as e:
            print(f"Error triggering keybind: {e}")
    
    def trigger_all_keybinds(self):
        """Trigger all configured keybinds"""
        current_time = time.time()
        
        # Check cooldown
        if current_time - self.last_trigger_time < self.cooldown_seconds:
            return
        
        self.last_trigger_time = current_time
        
        # Trigger each keybind
        for widget in self.keybind_widgets:
            keybind = widget.get_keybind()
            if keybind['keys']:
                keys = self.parse_keybind(keybind['keys'])
                if keys:
                    print(f"Triggering: {keybind['name']} - {keybind['keys']}")
                    self.trigger_keybind(keys)
                    time.sleep(0.1)  # Small delay between keybinds
    
    def update_frame(self):
        """Update camera frame"""
        if self.camera is None or not self.camera.isOpened():
            return
        
        ret, frame = self.camera.read()
        if not ret:
            return
        
        # Detect humans if enabled
        human_count = 0
        if self.detection_enabled and self.cascades:
            humans = self.detect_humans(frame)
            human_count = len(humans)
            
            # Draw rectangles around detected humans
            for (x, y, w, h) in humans:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, 'Human', (x, y-10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Trigger keybinds if humans detected
            if human_count > 0:
                self.trigger_all_keybinds()
        
        # Add status overlay
        status_text = f"Detection: {'ON' if self.detection_enabled else 'OFF'} | Humans: {human_count}"
        cv2.putText(frame, status_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0) if self.detection_enabled else (128, 128, 128), 2)
        
        # Convert to Qt format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        
        # Display
        self.camera_label.setPixmap(QPixmap.fromImage(qt_image))
    
    def save_settings(self):
        """Save settings to file"""
        settings = {
            'confidence': self.confidence_spin.value(),
            'cooldown': self.cooldown_spin.value(),
            'keybinds': [widget.get_keybind() for widget in self.keybind_widgets]
        }
        
        try:
            with open('detection_settings.json', 'w') as f:
                json.dump(settings, f, indent=2)
            QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {e}")
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists('detection_settings.json'):
                with open('detection_settings.json', 'r') as f:
                    settings = json.load(f)
                
                self.confidence_spin.setValue(settings.get('confidence', 50))
                self.cooldown_spin.setValue(settings.get('cooldown', 2))
                
                # Clear existing keybinds
                for widget in self.keybind_widgets[:]:
                    self.remove_keybind(widget)
                
                # Load saved keybinds
                keybinds = settings.get('keybinds', [])
                if keybinds:
                    for kb in keybinds:
                        self.add_keybind()
                        if self.keybind_widgets:
                            self.keybind_widgets[-1].set_keybind(kb.get('name', ''), kb.get('keys', ''))
        except Exception as e:
            print(f"Failed to load settings: {e}")
    
    def closeEvent(self, event):
        """Clean up on close"""
        self.stop_camera()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = HumanDetectionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
