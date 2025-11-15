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

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
JSON_FILE="$SCRIPT_DIR/data/tree.json"

echo "Creating/Replacing default tree.json..."
cat > "$JSON_FILE" << EOL
[
    {
        "text": "Root",
        "children": [
            {
                "text": "Child 1",
                "children": [
                    {
                        "text": "Grandchild 1",
                        "children": []
                    }
                ]
            },
            {
                "text": "Child 2",
                "children": []
            }
        ]
    }
]
EOL
echo "tree.json created successfully."

exit 0
