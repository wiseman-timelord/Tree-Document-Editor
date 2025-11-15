import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import json
import os
import sys

# Add the 'data' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')))

from temporary import CONFIG_FILE
from scripts.tree_utils import serialize_tree, deserialize_tree

class TreeEditorWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Jules-Tree-Document-Editor")
        self.set_default_size(600, 400)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        # Create a TreeStore
        self.treestore = Gtk.TreeStore(str)
        self.treeview = Gtk.TreeView(model=self.treestore)

        # Create a TreeViewColumn
        renderer_text = Gtk.CellRendererText()
        renderer_text.set_property("editable", True)
        renderer_text.connect("edited", self.on_text_edited)

        column = Gtk.TreeViewColumn("Tree", renderer_text, text=0)
        self.treeview.append_column(column)

        # Load initial data
        self.load_initial_data()

        # Create buttons
        self.add_button = Gtk.Button(label="Add")
        self.add_button.connect("clicked", self.on_add_clicked)

        self.remove_button = Gtk.Button(label="Remove")
        self.remove_button.connect("clicked", self.on_remove_clicked)

        self.edit_button = Gtk.Button(label="Edit")
        self.edit_button.connect("clicked", self.on_edit_clicked)

        self.save_button = Gtk.Button(label="Save")
        self.save_button.connect("clicked", self.on_save_clicked)

        self.load_button = Gtk.Button(label="Load")
        self.load_button.connect("clicked", self.on_load_clicked)

        # Layout
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 5, 1)
        self.scrollable_treelist.add(self.treeview)

        self.grid.attach(self.add_button, 0, 1, 1, 1)
        self.grid.attach(self.remove_button, 1, 1, 1, 1)
        self.grid.attach(self.edit_button, 2, 1, 1, 1)
        self.grid.attach(self.save_button, 3, 1, 1, 1)
        self.grid.attach(self.load_button, 4, 1, 1, 1)


        self.connect("destroy", Gtk.main_quit)

    def load_initial_data(self):
        """Loads the initial tree data and ensures all nodes are collapsed."""
        self.on_load_clicked(None)  # Load the data
        self.treeview.collapse_all()  # Collapse all nodes

    def on_save_clicked(self, button):
        tree_data = serialize_tree(self.treestore)
        # Preserve existing settings
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config_data = json.load(f)
        else:
            config_data = {"settings": {}} # Default if file doesn't exist

        config_data["tree"] = tree_data

        with open(CONFIG_FILE, "w") as f:
            json.dump(config_data, f, indent=4)

    def on_load_clicked(self, button):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                config_data = json.load(f)
            self.treestore.clear()
            deserialize_tree(config_data.get("tree", []), self.treestore, None)

    def on_text_edited(self, widget, path, text):
        self.treestore[path][0] = text

    def on_add_clicked(self, button):
        selection = self.treeview.get_selection()
        model, parent_iter = selection.get_selected()
        self.treestore.append(parent_iter, ["New Node"])

    def on_remove_clicked(self, button):
        selection = self.treeview.get_selection()
        model, tree_iter = selection.get_selected()
        if tree_iter:
            model.remove(tree_iter)

    def on_edit_clicked(self, button):
        selection = self.treeview.get_selection()
        model, tree_iter = selection.get_selected()
        if tree_iter:
            path = model.get_path(tree_iter)
            column = self.treeview.get_column(0)
            self.treeview.set_cursor(path, column, True)

    def run(self):
        self.show_all()
        # Collapse all nodes after showing the window
        self.treeview.collapse_all()
        Gtk.main()

if __name__ == "__main__":
    # Ensure the script can find the 'data' module
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    editor = TreeEditorWindow()
    editor.run()
