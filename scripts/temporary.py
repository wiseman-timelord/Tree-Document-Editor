"""
Temporary configuration constants for the Tree-Document-Editor.
"""
import os

# Get the project root directory
_current_dir = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = _current_dir

# Configuration file path
CONFIG_FILE = os.path.join(PROJECT_ROOT, "configuration.json")

# Additional paths if needed
DATA_DIR = PROJECT_ROOT
INSTALLED_DIR = os.path.join(PROJECT_ROOT, "installed")
PACKAGES_DIR = os.path.join(PROJECT_ROOT, "packages")