# This file contains the logic for previewing features.

# Import necessary modules
import os
import sys
import tkinter as tk
from tkinter import ttk
import mimetypes

# Define preview logic
class PreviewLogic:
    def __init__(self, gui_root):
        self.gui_root = gui_root
        self.preview_frame = ttk.Frame(gui_root)
        self.preview_frame.pack(fill=tk.BOTH, expand=True)

    def display_assets(self, asset_directory):
        """Display a list of assets in the GUI."""
        if not os.path.exists(asset_directory):
            print(f"Directory {asset_directory} does not exist.")
            return

        asset_list = os.listdir(asset_directory)
        asset_listbox = tk.Listbox(self.preview_frame)
        asset_listbox.pack(fill=tk.BOTH, expand=True)

        for asset in asset_list:
            asset_listbox.insert(tk.END, asset)

        asset_listbox.bind("<Double-Button-1>", lambda event: self.preview_asset(asset_directory, asset_listbox.get(tk.ACTIVE)))

    def preview_asset(self, asset_directory, asset_name):
        """Preview the selected asset based on its type."""
        asset_path = os.path.join(asset_directory, asset_name)
        mime_type, _ = mimetypes.guess_type(asset_path)

        preview_window = tk.Toplevel(self.gui_root)
        preview_window.title(f"Preview: {asset_name}")

        if mime_type and mime_type.startswith("image"):
            self.preview_image(preview_window, asset_path)
        elif mime_type and mime_type.startswith("text"):
            self.preview_text(preview_window, asset_path)
        else:
            self.preview_generic(preview_window, asset_name)

    def preview_image(self, preview_window, asset_path):
        """Display an image preview."""
        from PIL import Image, ImageTk

        img = Image.open(asset_path)
        img = img.resize((400, 400), Image.ANTIALIAS)
        img_tk = ImageTk.PhotoImage(img)

        label = tk.Label(preview_window, image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.pack(fill=tk.BOTH, expand=True)

    def preview_text(self, preview_window, asset_path):
        """Display a text file preview."""
        with open(asset_path, "r") as file:
            content = file.read()

        text_widget = tk.Text(preview_window)
        text_widget.insert(tk.END, content)
        text_widget.pack(fill=tk.BOTH, expand=True)

    def preview_generic(self, preview_window, asset_name):
        """Fallback preview for unsupported file types."""
        label = tk.Label(preview_window, text=f"Cannot preview {asset_name}. Unsupported file type.")
        label.pack(fill=tk.BOTH, expand=True)

# Example usage
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Asset Preview GUI")
    preview_logic = PreviewLogic(root)
    preview_logic.display_assets("./data/organized/test_project")
    root.mainloop()
