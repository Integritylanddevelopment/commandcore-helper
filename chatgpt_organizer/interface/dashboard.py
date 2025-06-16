import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from configparser import ConfigParser

config = ConfigParser()
config.read("config/settings.ini")
DATA_PATH = config.get("paths", "data_path", fallback="data/organized")
TOGGLE_VIEWS = ["Description", "Summary", "Inventory"]

class CommandCoreGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CommandCore OS")
        self.geometry("1400x800")
        self.configure(bg="#1e1e1e")
        self.current_folder = None
        self.current_chat = None
        self.current_view = "Summary"

        layout = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg="#1e1e1e")
        layout.pack(fill=tk.BOTH, expand=True)

        left_frame = tk.PanedWindow(layout, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg="#1e1e1e")
        self.folder_list = tk.Listbox(left_frame, width=30, bg="#2d2d2d", fg="#ffffff")
        left_frame.add(self.folder_list)
        self.folder_list.bind("<<ListboxSelect>>", self.load_chats)

        self.chat_list = tk.Listbox(left_frame, width=30, bg="#2d2d2d", fg="#ffffff")
        left_frame.add(self.chat_list)
        self.chat_list.bind("<<ListboxSelect>>", self.load_chat_content)

        layout.add(left_frame)

        center_frame = tk.Frame(layout, bg="#1e1e1e")
        self.chat_view = scrolledtext.ScrolledText(center_frame, bg="#1e1e1e", fg="#dcdcdc")
        self.chat_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        layout.add(center_frame)

        right_frame = tk.Frame(layout, bg="#1e1e1e")

        toggle_frame = tk.Frame(right_frame, bg="#1e1e1e")
        for view in TOGGLE_VIEWS:
            btn = tk.Button(toggle_frame, text=view, command=lambda v=view: self.set_view(v),
                            bg="#333", fg="#fff", width=10)
            btn.pack(side=tk.LEFT, padx=2)
        toggle_frame.pack(fill=tk.X, pady=(0, 5))

        self.summary_view = scrolledtext.ScrolledText(right_frame, bg="#1e1e1e", fg="#dcdcdc", height=20)
        self.summary_view.pack(fill=tk.BOTH, expand=True)

        self.asset_list = tk.Listbox(right_frame, bg="#2d2d2d", fg="#ffffff")
        self.asset_list.pack(fill=tk.X, padx=5, pady=(10, 10))

        layout.add(right_frame)

        self.load_projects()

    def set_view(self, view_type): self.current_view = view_type; self.update_summary_panel()
    def load_projects(self):
        self.folder_list.delete(0, tk.END)
        for folder in os.listdir(DATA_PATH):
            path = os.path.join(DATA_PATH, folder)
            if os.path.isdir(path):
                self.folder_list.insert(tk.END, folder)
    def load_chats(self, event): s = self.folder_list.curselection(); self.current_folder = os.path.join(DATA_PATH, self.folder_list.get(s[0])) if s else None; self.chat_list.delete(0, tk.END); [self.chat_list.insert(tk.END, f) for f in os.listdir(self.current_folder) if os.path.isdir(os.path.join(self.current_folder, f))]
    def load_chat_content(self, event): s = self.chat_list.curselection(); self.current_chat = os.path.join(self.current_folder, self.chat_list.get(s[0])) if s else None; p = os.path.join(self.current_chat, "chat.md"); self.chat_view.delete("1.0", tk.END); self.chat_view.insert(tk.END, open(p, encoding="utf-8").read() if os.path.exists(p) else "[No chat.md found]"); self.update_summary_panel(); self.load_assets()
    def update_summary_panel(self): self.summary_view.delete("1.0", tk.END); p = os.path.join(self.current_chat, {"Summary": "README.md", "Description": "description.md", "Inventory": "inventory.md"}.get(self.current_view, "README.md")); self.summary_view.insert(tk.END, open(p, encoding="utf-8").read() if os.path.exists(p) else f"[No {os.path.basename(p)} found]")
    def load_assets(self): self.asset_list.delete(0, tk.END); a = os.path.join(self.current_chat, "assets"); [self.asset_list.insert(tk.END, f) for f in os.listdir(a)] if os.path.exists(a) else None

if __name__ == "__main__":
    app = CommandCoreGUI()
    app.mainloop()
