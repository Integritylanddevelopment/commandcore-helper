from textual.widgets import Static

class PreviewPaneWidget(Static):
    def update_preview(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.update(f.read())
        except Exception as e:
            self.update(f"[Error opening file] {e}")
