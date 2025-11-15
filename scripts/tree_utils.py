import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

def serialize_tree(treestore):
    data = []
    for row in treestore:
        node = {"text": row[0], "children": []}
        if row.iterchildren():
            node["children"] = serialize_children(row.iterchildren())
        data.append(node)
    return data

def serialize_children(children):
    data = []
    for child in children:
        node = {"text": child[0], "children": []}
        if child.iterchildren():
            node["children"] = serialize_children(child.iterchildren())
        data.append(node)
    return data

def deserialize_tree(data, treestore, parent):
    for node in data:
        new_iter = treestore.append(parent, [node["text"]])
        if "children" in node:
            deserialize_tree(node["children"], treestore, new_iter)
