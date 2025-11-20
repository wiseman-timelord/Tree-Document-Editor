import os
import sys
import subprocess
import json
import zipfile
import time
import shutil
import platform

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from 'scripts')
project_root = os.path.dirname(script_dir)

def get_project_path(*args):
    """Constructs an absolute path from the project root."""
    return os.path.join(project_root, *args)

def find_python_windows():
    """Find Python executable on Windows, checking multiple locations."""
    # Check local installation first
    local_python = get_project_path("data", "installed", "Python311", "python.exe")
    if os.path.exists(local_python):
        return local_python
    
    # Check common Python installation paths
    common_paths = [
        r"C:\Python311\python.exe",
        r"C:\Users\{}\AppData\Local\Programs\Python\Python311\python.exe".format(os.getenv('USERNAME')),
        r"C:\Program Files\Python311\python.exe",
        r"C:\Program Files (x86)\Python311\python.exe",
    ]
    
    for path in common_paths:
        if os.path.exists(path):
            return path
    
    # Check if python is in PATH
    try:
        result = subprocess.run(['where', 'python'], capture_output=True, text=True)
        if result.returncode == 0:
            python_path = result.stdout.strip().split('\n')[0]
            # Verify it's Python 3.x
            version_result = subprocess.run([python_path, '--version'], capture_output=True, text=True)
            if 'Python 3' in version_result.stdout or 'Python 3' in version_result.stderr:
                return python_path
    except:
        pass
    
    return None

def ensure_python_windows():
    """Ensure Python is available on Windows, installing if necessary."""
    print("Checking for Python installation...")
    
    python_exe = find_python_windows()
    
    if python_exe:
        print(f"✓ Found Python at: {python_exe}")
        # Verify version
        try:
            result = subprocess.run([python_exe, '--version'], capture_output=True, text=True)
            version = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
            print(f"✓ Python version: {version}")
            return python_exe
        except:
            pass
    
    print("Python 3.11 not found. Installing from offline package...")
    
    # Install Python
    success, python_exe = install_python_for_windows()
    if success:
        print("✓ Python installation completed successfully")
        return python_exe
    else:
        print("✗ Python installation failed")
        return None

# ------------------------------------------------------------------
#  Python Installation (Windows only)
# ------------------------------------------------------------------
def install_python_for_windows():
    """Install Python 3.11 for Windows if not already installed."""
    python_dir = get_project_path("data", "installed", "Python311")
    python_exe = os.path.join(python_dir, "python.exe")
    
    print("\nChecking Python installation...")
    
    # Check if already installed
    if os.path.exists(python_exe):
        print(f"✓ Python already installed at: {python_dir}")
        return True, python_exe
    
    print("Python not found. Installing Python 3.11 offline...")
    
    python_installer = get_project_path("data", "packages", "python-3.11.0-amd64.exe")
    
    if not os.path.exists(python_installer):
        print(f"ERROR: Python installer not found at:")
        print(f"  {python_installer}")
        print("\nPlease place python-3.11.0-amd64.exe in the data/packages directory.")
        return False, None
    
    # Ensure target directory exists
    os.makedirs(python_dir, exist_ok=True)
    
    print("Installing Python 3.11...")
    print("This may take a few minutes, please wait...")
    
    try:
        # Run Python installer with start /wait equivalent using subprocess
        result = subprocess.run(
            [python_installer, "/quiet", "InstallAllUsers=0", 
             f"TargetDir={python_dir}", "PrependPath=0", 
             "Include_test=0", "Include_pip=1"],
            timeout=600  # 10 minute timeout
        )
        
        # Wait and verify installation with retry logic
        print("\nVerifying Python installation...")
        for attempt in range(1, 11):
            if os.path.exists(python_exe):
                print(f"✓ Python installed successfully at: {python_dir}")
                return True, python_exe
            print(f"  Waiting for installation to complete... (attempt {attempt}/10)")
            time.sleep(3)
        
        # If we get here, installation failed
        print("\nERROR: Python installation failed. Python.exe not found after installation.")
        print(f"Expected location: {python_exe}")
        print("\nPlease check:")
        print("  1. The Python installer is the correct version (3.11.0 for AMD64)")
        print("  2. You have sufficient permissions to install software")
        print("  3. There is enough disk space available")
        
        # Show what's in the directory
        if os.path.exists(python_dir):
            print(f"\nContents of {python_dir}:")
            for item in os.listdir(python_dir):
                print(f"  - {item}")
        
        return False, None
        
    except subprocess.TimeoutExpired:
        print("ERROR: Python installation timed out after 10 minutes.")
        return False, None
    except Exception as e:
        print(f"ERROR: Python installation failed: {e}")
        return False, None

# ------------------------------------------------------------------
#  PyGObject Installation (Windows only)
# ------------------------------------------------------------------
def install_pygobject_for_windows(python_exe):
    """Install PyGObject wheel into the Python installation."""
    wheel_path = get_project_path("data", "packages", "PyGObject-3.11-win64.whl")
    
    print("\nInstalling PyGObject...")
    
    if not os.path.isfile(wheel_path):
        print(f"ERROR: PyGObject wheel not found at:")
        print(f"  {wheel_path}")
        print("\nPlease ensure the wheel file is in the correct location.")
        print("You may need to download it from:")
        print("  https://github.com/pygobject/pygobject/releases")
        return False
    
    print(f"Using wheel: {os.path.basename(wheel_path)}")
    
    try:
        # First ensure pip is available
        subprocess.run([python_exe, "-m", "ensurepip", "--default-pip"],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                      timeout=60)
    except:
        pass  # pip might already be installed
    
    try:
        subprocess.check_call([python_exe, "-m", "pip", "install",
                               "--no-index", "--no-deps", wheel_path],
                              timeout=120)
        print("✓ PyGObject installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install PyGObject: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("ERROR: PyGObject installation timed out.")
        return False

# ------------------------------------------------------------------
#  GTK Installation (Windows only)
# ------------------------------------------------------------------
def install_gtk_for_windows():
    """Install GTK runtime for Windows."""
    gtk_vendor_path = get_project_path("vendor", "gtk-windows")
    
    print("\nInstalling GTK runtime...")
    
    # Check if already installed
    if os.path.exists(gtk_vendor_path) and os.path.exists(os.path.join(gtk_vendor_path, "bin")):
        dll_path = os.path.join(gtk_vendor_path, "bin", "libgtk-3-0.dll")
        if os.path.exists(dll_path):
            print("✓ GTK runtime already installed.")
            return True
    
    gtk_installer = get_project_path("data", "packages", "gtk-runtime-3.8.1-i686.exe")
    
    if not os.path.exists(gtk_installer):
        print(f"ERROR: GTK installer not found at:")
        print(f"  {gtk_installer}")
        print("\nPlease place the GTK installer in the specified directory.")
        return False
    
    # Ensure vendor directory exists
    os.makedirs(os.path.dirname(gtk_vendor_path), exist_ok=True)
    
    print(f"Installing to: {gtk_vendor_path}")
    print("This may take a few minutes...")
    
    try:
        # Run GTK installer and wait for completion
        result = subprocess.run(
            [gtk_installer, "/S", f"/D={gtk_vendor_path}"],
            timeout=300
        )
        
        # Wait for files to be written
        time.sleep(5)
        
        # Verify installation
        dll_path = os.path.join(gtk_vendor_path, "bin", "libgtk-3-0.dll")
        if os.path.exists(dll_path):
            print("✓ GTK runtime installed successfully.")
            return True
        else:
            print("WARNING: GTK installation completed but key files not found.")
            print(f"Expected file not found: {dll_path}")
            
            # Show what was installed
            if os.path.exists(gtk_vendor_path):
                print(f"\nContents of {gtk_vendor_path}:")
                for item in os.listdir(gtk_vendor_path):
                    print(f"  - {item}")
            
            return False
            
    except subprocess.TimeoutExpired:
        print("ERROR: GTK installation timed out after 5 minutes.")
        return False
    except Exception as e:
        print(f"ERROR: GTK installation failed: {e}")
        return False

# ------------------------------------------------------------------
#  NConvert Extraction (Windows only)
# ------------------------------------------------------------------
def extract_nconvert():
    """Extract NConvert for Windows."""
    print("\nExtracting NConvert...")
    
    nconvert_zip = get_project_path("data", "packages", "NConvert-win64.zip")
    nconvert_install_dir = get_project_path("data", "installed")
    
    # Check if already extracted
    nconvert_exe = os.path.join(nconvert_install_dir, "nconvert.exe")
    if os.path.exists(nconvert_exe):
        print("✓ NConvert already extracted.")
        return True
    
    if not os.path.exists(nconvert_zip):
        print(f"WARNING: NConvert package not found at:")
        print(f"  {nconvert_zip}")
        print("Skipping NConvert extraction (optional component).")
        return True  # Not critical
    
    try:
        os.makedirs(nconvert_install_dir, exist_ok=True)
        with zipfile.ZipFile(nconvert_zip, 'r') as zip_ref:
            zip_ref.extractall(nconvert_install_dir)
        print("✓ NConvert extracted successfully.")
        return True
    except Exception as e:
        print(f"WARNING: Failed to extract NConvert: {e}")
        return True  # Not critical

# ------------------------------------------------------------------
#  Windows Installation
# ------------------------------------------------------------------
def install_windows_deps():
    """Installs dependencies for Windows."""
    print("Running Windows installation...")
    print("-" * 79)
    
    print(f"\nProject root: {project_root}")
    print(f"Current Python: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    all_success = True
    
    # 1. First ensure Python is available
    python_exe = ensure_python_windows()
    if not python_exe:
        print("\nERROR: Could not obtain Python executable. Cannot continue.")
        return False
    
    print(f"\nUsing Python: {python_exe}")
    
    # 2. Install GTK runtime
    if not install_gtk_for_windows():
        all_success = False
    
    # 3. Extract NConvert (optional)
    extract_nconvert()
    
    # 4. Install PyGObject using the newly installed Python
    if not install_pygobject_for_windows(python_exe):
        all_success = False
    
    return all_success

# ------------------------------------------------------------------
#  Linux Installation
# ------------------------------------------------------------------
def install_linux_deps():
    """Verifies dependencies for Linux (Ubuntu 25 assumed to have everything)."""
    print("Running Linux installation...")
    print("-" * 79)
    
    print(f"\nProject root: {project_root}")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # For Ubuntu 25, we assume GTK3 and Python 3 are already installed
    print("\nAssuming Ubuntu 25.04 with pre-installed dependencies:")
    print("  - Python 3.x")
    print("  - GTK3")
    print("  - PyGObject (python3-gi)")
    
    # Quick verification checks (non-blocking)
    print("\nVerifying installations...")
    
    all_ok = True
    
    # Check Python 3
    try:
        result = subprocess.run([sys.executable, "--version"], 
                                capture_output=True, text=True, check=True)
        print(f"✓ Python: {result.stdout.strip()}")
    except:
        print("✗ Python check failed")
        all_ok = False
    
    # Check for GTK3
    try:
        subprocess.run(["pkg-config", "--exists", "gtk+-3.0"], 
                       check=True, capture_output=True)
        # Get version
        result = subprocess.run(["pkg-config", "--modversion", "gtk+-3.0"], 
                               capture_output=True, text=True, check=True)
        print(f"✓ GTK3: {result.stdout.strip()}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ GTK3 not found")
        print("\n  Install with: sudo apt-get install -y libgtk-3-0 libgtk-3-dev")
        all_ok = False
    
    # Check for PyGObject
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
        print(f"✓ PyGObject: Available (GTK {Gtk.MAJOR_VERSION}.{Gtk.MINOR_VERSION})")
    except (ImportError, ValueError) as e:
        print("✗ PyGObject not found or incorrectly configured")
        print("\n  Install with: sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0")
        all_ok = False
    
    # Check for ImageMagick (optional)
    try:
        result = subprocess.run(["convert", "-version"], 
                               capture_output=True, text=True, check=True)
        version_line = result.stdout.split('\n')[0]
        print(f"✓ ImageMagick: {version_line} (optional)")
    except:
        print("○ ImageMagick not found (optional)")
        print("  Install with: sudo apt-get install -y imagemagick")
    
    if not all_ok:
        print("\n" + "=" * 79)
        print("IMPORTANT: Some required components are missing.")
        print("Please install them using the commands shown above.")
        print("=" * 79)
    
    return all_ok

# ------------------------------------------------------------------
#  Configuration File Creation
# ------------------------------------------------------------------
def create_default_config():
    """Creates the default configuration.json file."""
    print("\nCreating default configuration...")
    config_path = get_project_path("data", "configuration.json")
    
    # Don't overwrite existing config
    if os.path.exists(config_path):
        print("✓ Configuration file already exists.")
        return True
    
    default_data = {
        "tree": [
            {
                "text": "Root",
                "children": [
                    {
                        "text": "Child 1",
                        "children": [
                            {"text": "Grandchild 1", "children": []}
                        ],
                    },
                    {"text": "Child 2", "children": []},
                ],
            }
        ],
        "settings": {
            "theme": "default"
        }
    }
    
    try:
        # Ensure the 'data' directory exists
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding='utf-8') as f:
            json.dump(default_data, f, indent=4)
        print(f"✓ configuration.json created at:")
        print(f"  {config_path}")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create configuration.json: {e}")
        return False

# ------------------------------------------------------------------
#  Main Installation Entry Point
# ------------------------------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: installer.py <windows|linux>")
        sys.exit(1)

    platform_arg = sys.argv[1].lower()
    
    print("=" * 79)
    print("  Tree-Document-Editor Installer")
    print("=" * 79)
    print(f"Platform: {platform_arg}")
    print()

    success = True
    
    if platform_arg == "windows":
        success = install_windows_deps()
    elif platform_arg == "linux":
        success = install_linux_deps()
    else:
        print(f"ERROR: Unsupported platform: {platform_arg}")
        print("Please specify 'windows' or 'linux'")
        sys.exit(1)

    # Always try to create config
    if not create_default_config():
        success = False

    print()
    print("=" * 79)
    if success:
        print("✓ Installation completed successfully!")
        print("\nYou can now return to the menu and select 'Launch Tree-Document-Editor'.")
    else:
        print("✗ Installation completed with errors.")
        print("Please review the messages above and resolve any issues.")
    print("=" * 79)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()