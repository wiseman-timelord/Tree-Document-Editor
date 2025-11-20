#!/bin/bash

# Change to the script directory
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Python configuration
PYTHON_CMD="python3"

main_menu() {
    clear
    echo "==============================================================================="
    echo "   Tree-Document-Editor: Menu"
    echo "==============================================================================="
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo "   1) Launch Tree-Document-Editor"
    echo ""
    echo "   2) Install Requirements"
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo ""
    echo "-------------------------------------------------------------------------------"
    read -p "Selection; Menu Options = 1-2, Quit Program = Q: " choice
    
    case "$choice" in
        1|[Ll]aunch)
            launch_app
            ;;
        2|[Ii]nstall)
            install_deps
            ;;
        [Qq]|[Qq]uit)
            quit_app
            exit 0
            ;;
        *)
            echo "Invalid selection. Please try again."
            read -p "Press Enter to continue..."
            ;;
    esac
    
    main_menu
}

launch_app() {
    clear
    echo "==============================================================================="
    echo "   Launching Tree-Document-Editor"
    echo "==============================================================================="
    echo ""
    echo "Starting application..."
    $PYTHON_CMD "$SCRIPT_DIR/scripts/editor.py"
    echo ""
    read -p "Press Enter to continue..."
}

install_deps() {
    clear
    echo "==============================================================================="
    echo "   Installing Requirements"
    echo "==============================================================================="
    echo ""
    $PYTHON_CMD "$SCRIPT_DIR/scripts/installer.py" linux
    echo ""
    read -p "Press Enter to continue..."
}

quit_app() {
    clear
    echo "==============================================================================="
    echo "   Exiting Program"
    echo "==============================================================================="
    echo ""
    echo "Exiting program..."
    echo "Thank you for using Tree-Document-Editor."
    echo ""
    sleep 2
}

# Start the menu
main_menu