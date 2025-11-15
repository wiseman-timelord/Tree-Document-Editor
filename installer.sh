#!/bin/bash

# Check for GTK3 using pkg-config
if ! pkg-config --exists gtk+-3.0; then
  echo "GTK3 is not installed."
  echo "Please install it using your system's package manager."
  echo "For Debian/Ubuntu, run: sudo apt-get install -y libgtk-3-dev"
  echo "For Fedora, run: sudo yum install -y gtk3-devel"
  echo "For Arch, run: sudo pacman -S gtk3"
  exit 1
fi

echo "Dependencies are satisfied."
exit 0
