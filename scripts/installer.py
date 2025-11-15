import os
import sys
import subprocess
import json
import zipfile

def install_windows_deps():
    """Installs dependencies for Windows."""
    print("Running Windows installation...")

    # Install GTK
    gtk_vendor_path = os.path.abspath("vendor/gtk-windows")
    if not os.path.exists(gtk_vendor_path):
        print("Installing GTK runtime...")
        gtk_installer = os.path.abspath("data/packages/gtk-runtime-3.8.1-i686.exe")
        if os.path.exists(gtk_installer):
            subprocess.run([gtk_installer, "/S", f"/D={gtk_vendor_path}"], check=True)
            print("GTK runtime installed successfully.")
        else:
            print("ERROR: GTK installer not found.")
    else:
        print("GTK runtime already installed.")

    # Extract NConvert
    nconvert_zip = os.path.abspath("data/packages/NConvert-win64.zip")
    nconvert_install_dir = os.path.abspath("data/installed")
    if os.path.exists(nconvert_zip):
        print("Extracting NConvert...")
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

def create_default_json():
    """Creates the default tree.json file."""
    print("Creating default tree.json...")
    json_path = os.path.abspath("data/tree.json")
    default_data = [
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
    ]
    with open(json_path, "w") as f:
        json.dump(default_data, f, indent=4)
    print("tree.json created successfully.")

def main():
    if sys.platform == "win32":
        install_windows_deps()
    elif sys.platform.startswith("linux"):
        install_linux_deps()
    else:
        print(f"Unsupported platform: {sys.platform}")
        sys.exit(1)

    create_default_json()
    print("Installation complete.")

if __name__ == "__main__":
    main()
