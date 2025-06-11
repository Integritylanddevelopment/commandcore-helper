from textual.widgets import TreeControl, TreeNode
import os

class TreeViewWidget(TreeControl):
    class FolderSelected:
        def __init__(self, folder_path):
            self.folder_path = folder_path

    def __init__(self, id=None):
        super().__init__("File Explorer", "C:/", id=id)
        self.load_directory("C:/", self.root)

    def load_directory(self, path, node):
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    child = node.add(entry, full_path)
                    child.allow_expand = True
        except PermissionError:
            pass

    async def on_node_expanded(self, node: TreeNode):
        self.load_directory(node.data, node)

    async def on_tree_node_selected(self, node: TreeNode):
        self.post_message(self.FolderSelected(node.data))
