Write-Host "🔧 Restoring interface/gui.py to working version..."

$guiCode = @"
import os
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import importlib
from search.query import query_index

DATA_PATH = "data/organized"
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
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(center_frame, textvariable=self.search_var, width=60)
        search_entry.pack(pady=(10, 0), padx=10)
        search_btn = tk.Button(center_frame, text="Search", command=self.run_search)
        search_btn.pack(pady=(0, 10))
        self.chat_view = scrolledtext.ScrolledText(center_frame, bg="#1e1e1e", fg="#dcdcdc")
        self.chat_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        plugin_label = tk.Label(center_frame, text="Run Plugin", fg="#fff", bg="#1e1e1e")
        plugin_label.pack(pady=(10, 0))
        self.plugin_var = tk.StringVar()
        self.plugin_dropdown = ttk.Combobox(center_frame, textvariable=self.plugin_var, width=40)
        self.plugin_dropdown["values"] = sorted([
            "github_push", "firebase_sync", "zip_uploader", "blog", "social",
            "notify", "tagger", "import_zip", "index_generator", "chat_formatter",
            "duplicate_finder", "project_linker", "chat_cleaner", "chat_stats",
            "chat_merger", "webhook_listener", "plugin_runner"
        ])
        self.plugin_dropdown.pack(pady=5)
        plugin_button = tk.Button(center_frame, text="Execute Plugin", command=self.run_plugin)
        plugin_button.pack(pady=(0, 10))
        layout.add(center_frame)
        right_outer = tk.PanedWindow(layout, orient=tk.VERTICAL, sashrelief=tk.RAISED, bg="#1e1e1e")
        right_top = tk.Frame(right_outer, bg="#1e1e1e")
        toggle_frame = tk.Frame(right_top, bg="#1e1e1e")
        for view in TOGGLE_VIEWS:
            btn = tk.Button(toggle_frame, text=view, command=lambda v=view: self.set_view(v),
                            bg="#333", fg="#fff", width=10)
            btn.pack(side=tk.LEFT, padx=2)
        toggle_frame.pack(fill=tk.X, pady=(0, 5))
        self.summary_view = scrolledtext.ScrolledText(right_top, bg="#1e1e1e", fg="#dcdcdc", height=20)
        self.summary_view.pack(fill=tk.BOTH, expand=True)
        right_outer.add(right_top)
        right_bottom = tk.Frame(right_outer, bg="#1e1e1e")
        self.asset_label = tk.Label(right_bottom, text="📦 Assets", bg="#1e1e1e", fg="#bbb")
        self.asset_label.pack(anchor="w", padx=5, pady=(10, 0))
        self.asset_list = tk.Listbox(right_bottom, bg="#2d2d2d", fg="#ffffff")
        self.asset_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 10))
        right_outer.add(right_bottom)
        layout.add(right_outer)
        bottom_frame = tk.Frame(self, bg="#1e1e1e")
        bottom_frame.pack(fill=tk.X, pady=2)
        for label in ["Admin", "Sales", "Marketing", "Tech"]:
            tk.Button(bottom_frame, text=label, width=15, command=lambda l=label: self.open_dashboard(l),
                      bg="#444", fg="#fff").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.load_projects()

    def set_view(self, view_type): self.current_view = view_type; self.update_summary_panel()
    def load_projects(self): self.folder_list.delete(0, tk.END); [self.folder_list.insert(tk.END, f) for f in os.listdir(DATA_PATH) if os.path.isdir(os.path.join(DATA_PATH, f))]
    def load_chats(self, event): s = self.folder_list.curselection(); self.current_folder = os.path.join(DATA_PATH, self.folder_list.get(s[0])) if s else None; self.chat_list.delete(0, tk.END); [self.chat_list.insert(tk.END, f) for f in os.listdir(self.current_folder) if os.path.isdir(os.path.join(self.current_folder, f))]
    def load_chat_content(self, event): s = self.chat_list.curselection(); self.current_chat = os.path.join(self.current_folder, self.chat_list.get(s[0])) if s else None; p = os.path.join(self.current_chat, "chat.md"); self.chat_view.delete("1.0", tk.END); self.chat_view.insert(tk.END, open(p, encoding="utf-8").read() if os.path.exists(p) else "[No chat.md found]"); self.update_summary_panel(); self.load_assets()
    def update_summary_panel(self): self.summary_view.delete("1.0", tk.END); p = os.path.join(self.current_chat, {"Summary": "README.md", "Description": "description.md", "Inventory": "inventory.md"}.get(self.current_view, "README.md")); self.summary_view.insert(tk.END, open(p, encoding="utf-8").read() if os.path.exists(p) else f"[No {os.path.basename(p)} found]")
    def load_assets(self): self.asset_list.delete(0, tk.END); a = os.path.join(self.current_chat, "assets"); [self.asset_list.insert(tk.END, f) for f in os.listdir(a)] if os.path.exists(a) else None
    def run_search(self): term = self.search_var.get().strip(); self.chat_view.delete("1.0", tk.END); self.chat_view.insert(tk.END, "[search] Please enter a search term." if not term else f"[search] Found {len(query_index(term))} result(s):\n\n" + ''.join(f"- {m}\n" for m in query_index(term)))
    def run_plugin(self): name = self.plugin_var.get().strip(); self.chat_view.delete("1.0", tk.END); self.chat_view.insert(tk.END, "[plugin] Select a plugin to run." if not name else (lambda m: m.run() if hasattr(m, "run") else None)(importlib.import_module(f"plugins.{name}")))
    def open_dashboard(self, label): self.summary_view.insert(tk.END, f"\n[→ Launching {label} Dashboard...]\n")

if __name__ == "__main__":
    app = CommandCoreGUI()
    app.mainloop()
"@

Set-Content -Path ".\interface\gui.py" -Value $guiCode -Encoding UTF8
Write-Host "🎉 GUI restoration complete."
