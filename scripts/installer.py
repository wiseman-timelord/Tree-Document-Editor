import os
import sys
import subprocess
import json
import zipfile

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (one level up from 'scripts')
project_root = os.path.dirname(script_dir)

def get_project_path(*args):
    """Constructs an absolute path from the project root."""
    return os.path.join(project_root, *args)

# ------------------------------------------------------------------
#  NEW: offline PyGObject wheel install (Windows only)
# ------------------------------------------------------------------
def install_pygobject_for_windows():
    """Install PyGObject wheel into the offline Python that is running this script."""
    python_exe = sys.executable          # the interpreter we just installed
    wheel_path = get_project_path("data", "packages", "PyGObject-3.11-win64.whl")
    if not os.path.isfile(wheel_path):
        print("ERROR: PyGObject wheel not found at", wheel_path)
        sys.exit(1)
    print("Installing PyGObject wheel …")
    subprocess.check_call([python_exe, "-m", "pip", "install",
                           "--no-index", "--no-deps", wheel_path])

def install_windows_deps():
    """Installs dependencies for Windows."""
    print("Running Windows installation...")

    # 1. GTK runtime
    gtk_vendor_path = get_project_path("vendor", "gtk-windows")
    if not os.path.exists(gtk_vendor_path):
        print("Installing GTK runtime...")
        gtk_installer = get_project_path("data", "packages", "gtk-runtime-3.8.1-i686.exe")
        if os.path.exists(gtk_installer):
            subprocess.run([gtk_installer, "/S", f"/D={gtk_vendor_path}"], check=True)
            print("GTK runtime installed successfully.")
        else:
            print("ERROR: GTK installer not found.")
    else:
        print("GTK runtime already installed.")

    # 2. NConvert extract
    nconvert_zip = get_project_path("data", "packages", "NConvert-win64.zip")
    nconvert_install_dir = get_project_path("data", "installed")
    if os.path.exists(nconvert_zip):
        print("Extracting NConvert...")
        os.makedirs(nconvert_install_dir, exist_ok=True)
        with zipfile.ZipFile(nconvert_zip, 'r') as zip_ref:
            zip_ref.extractall(nconvert_install_dir)
        print("NConvert extracted successfully.")
    else:
        print("NConvert package not found. Skipping extraction.")

    # 3. PyGObject (offline wheel)
    install_pygobject_for_windows()

def install_linux_deps():
    """Installs dependencies for Linux."""
    print("Running Linux installation...")
    try:
        subprocess.run(["pkg-config", "--exists", "gtk+-3.0"], check=True)
        print("GTK3 is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GTK3 is not installed.")
        print("Please install it using your system's package manager.")
        print("For Debian/Ubuntu, run: sudo apt-get install -y libgtk-3-dev")
        print("For Fedora, run: sudo yum install -y gtk3-devel")
        print("For Arch, run: sudo pacman -S gtk3")

    try:
        subprocess.run(["which", "magick"], check=True, capture_output=True)
        print("ImageMagick is already installed.")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ImageMagick is not installed.")
        print("Please install it using your system's package manager.")
        print("For Debian/Ubuntu, run: sudo apt-get install -y imagemagick")
        print("For Fedora, run: sudo yum install -y ImageMagick")
        print("For Arch, run: sudo pacman -S imagemagick")

def create_default_config():
    """Creates the default configuration.json file."""
    print("Creating default configuration.json...")
    config_path = get_project_path("data", "configuration.json")
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
    # Ensure the 'data' directory exists
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(default_data, f, indent=4)
    print("configuration.json created successfully.")

def main():
    if len(sys.argv) < 2:
        print("Usage: installer.py <windows|linux>")
        sys.exit(1)

    platform = sys.argv[1]

    if platform == "windows":
        install_windows_deps()
    elif platform == "linux":
        install_linux_deps()
    else:
        print(f"Unsupported platform: {platform}")
        sys.exit(1)

    create_default_config()
    print("Installation complete.")

if __name__ == "__main__":
    main()