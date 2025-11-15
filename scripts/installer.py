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

def install_windows_deps():
    """Installs dependencies for Windows."""
    print("Running Windows installation...")

    # Install GTK
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

    # Extract NConvert
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
    if sys.platform == "win32":
        install_windows_deps()
    elif sys.platform.startswith("linux"):
        install_linux_deps()
    else:
        print(f"Unsupported platform: {sys.platform}")
        sys.exit(1)

    create_default_config()
    print("Installation complete.")

if __name__ == "__main__":
    main()
