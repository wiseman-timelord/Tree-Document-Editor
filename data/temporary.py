import os

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Get the project root directory (same level as 'data')
project_root = os.path.dirname(script_dir)

def get_project_path(*args):
    """Constructs an absolute path from the project root."""
    return os.path.join(project_root, *args)

CONFIG_FILE = get_project_path("data", "configuration.json")
