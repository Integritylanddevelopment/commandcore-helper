from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Splitter
from textual.containers import Container, Vertical

from .tree_view import TreeViewWidget
from .folder_contents import FolderContentsWidget
from .preview_pane import PreviewPaneWidget

class ExplorerApp(App):
    CSS_PATH = None
    TITLE = "CommandCore Explorer"
    SUB_TITLE = "Navigate | Preview | Trigger"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Splitter(
            TreeViewWidget(id="tree"),
            Vertical(
                FolderContentsWidget(id="contents"),
                PreviewPaneWidget(id="preview")
            ),
            id="main_split"
        )
        yield Footer()

    def on_mount(self):
        self.query_one("#tree").focus()

    async def on_tree_view_widget_folder_selected(self, message: TreeViewWidget.FolderSelected):
        self.query_one("#contents").folder_path = message.folder_path
        self.query_one("#preview").update("[Select a file to preview]")
