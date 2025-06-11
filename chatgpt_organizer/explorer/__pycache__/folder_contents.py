from textual.widgets import Static
import os

class FolderContentsWidget(Static):
    def __init__(self, id=None):
        super().__init__("", id=id)
        self.folder_path = ""

    def render(self):
        if not self.folder_path:
            return "[No folder selected]"
        try:
            files = os.listdir(self.folder_path)
            return "\n".join(files)
        except Exception as e:
            return f"[Error reading folder] {e}"
