#!/bin/bash
# Script: Tree-Document-Editor.sh

cd "$(dirname "$0")"
export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages

# Function to display the main menu
main_menu() {
    clear
    echo "==============================================================================="
    echo "   Tree-Document-Editor: Bash Menu"
    echo "==============================================================================="
    echo
    echo
    echo
    echo
    echo
    echo
    echo
    echo "   1) Launch Tree-Document-Editor"
    echo
    echo "   2) Install Requirements"
    echo
    echo
    echo
    echo
    echo
    echo
    echo
    echo "-------------------------------------------------------------------------------"
    read -p "Selection; Menu Options = 1-2, Quit Program = Q: " choice
}

# Function to launch the application
launch() {
    clear
    echo "==============================================================================="
    echo "   Launching Tree-Document-Editor"
    echo "==============================================================================="
    echo
    echo "Starting application..."
    python3 scripts/editor.py
    echo
    read -p "Press Enter to continue..."
}

# Function to install requirements
install() {
    clear
    echo "==============================================================================="
    echo "   Installing Requirements"
    echo "==============================================================================="
    echo
    echo "Running Python installer script..."
    python3 scripts/installer.py linux
    echo
    echo "Installation complete."
    read -p "Press Enter to continue..."
}

# Function to quit the program
quit() {
    clear
    echo "==============================================================================="
    echo "   Exiting Program"
    echo "==============================================================================="
    echo
    echo "Exiting program..."
    echo "Thank you for using Tree-Document-Editor."
    echo
    sleep 2
    exit 0
}

# Main loop
while true; do
    main_menu
    case "$choice" in
        1) launch ;;
        2) install ;;
        q|Q) quit ;;
        *) echo "Invalid selection. Please try again."; read -p "Press Enter to continue..." ;;
    esac
done
