import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
from configparser import ConfigParser
import subprocess
import json

config = ConfigParser()
config.read("config/settings.ini")
DATA_PATH = config.get("paths", "data_path", fallback="data/organized")
TOGGLE_VIEWS = ["Description", "Summary", "Inventory"]
PROJECT_MODES = ["Projects", "Chats", "Sidebar"]

class CommandCoreGUI(tk.Tk):
    def load_projects(self):
        self.folder_list.delete(0, tk.END)
        mode = self.project_mode.get()
        if mode == "Projects":
            for folder in os.listdir(DATA_PATH):
                path = os.path.join(DATA_PATH, folder)
                if os.path.isdir(path):
                    self.folder_list.insert(tk.END, folder)
        elif mode == "Chats":
            self.folder_list.insert(tk.END, "[All Loose Chats]")
        elif mode == "Sidebar":
            self.folder_list.insert(tk.END, "[Favorite Assistants]")
        def load_chats(self, event):
            selection = self.folder_list.curselection()
            if not selection:
                return
            selected = self.folder_list.get(selection[0])
            self.current_folder = os.path.join(DATA_PATH, selected)
            self.chat_list.delete(0, tk.END)
            if os.path.exists(self.current_folder):
                for chat in os.listdir(self.current_folder):
                    path = os.path.join(self.current_folder, chat)
                    if os.path.isdir(path):
                        self.chat_list.insert(tk.END, chat)
    def dictate_to_prompt(self):
        import speech_recognition as sr

        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.chat_view.insert(tk.END, "\n🎙 Listening...\n")
            try:
                audio = r.listen(source, timeout=5)
                text = r.recognize_google(audio)
                self.gpt_prompt.set(text)
                self.chat_view.insert(tk.END, f"🎤 Transcribed: {text}\n")
            except sr.UnknownValueError:
                self.chat_view.insert(tk.END, "❌ Could not understand audio\n")
            except sr.RequestError:
                self.chat_view.insert(tk.END, "❌ Error reaching speech API\n")
            except Exception as e:
                self.chat_view.insert(tk.END, f"❌ Dictation error: {e}\n")
    def __init__(self):
        super().__init__()
        self.title("CommandCore OS")
        self.geometry("1400x850")
        self.configure(bg="#1e1e1e")
        self.current_folder = None
        self.current_chat = None
        self.current_view = "Summary"

        layout = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, bg="#1e1e1e")
        layout.pack(fill=tk.BOTH, expand=True)

        left_panel = tk.PanedWindow(layout, orient=tk.VERTICAL, bg="#1e1e1e", sashrelief=tk.RAISED)
        mode_frame = tk.Frame(left_panel, bg="#1e1e1e")
        self.project_mode = tk.StringVar(value="Projects")
        for mode in PROJECT_MODES:
            b = tk.Radiobutton(mode_frame, text=mode, variable=self.project_mode, value=mode,
                           bg="#333", fg="#fff", selectcolor="#444", width=10,
                           command=self.load_projects)
            b.pack(side=tk.LEFT, padx=2, pady=5)
        mode_frame.pack(fill=tk.X)

        self.folder_list = tk.Listbox(left_panel, width=30, bg="#2d2d2d", fg="#ffffff")
        self.folder_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.folder_list.bind("<<ListboxSelect>>", self.load_chats)

        self.chat_list = tk.Listbox(left_panel, width=30, bg="#2d2d2d", fg="#ffffff")
        self.chat_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.chat_list.bind("<<ListboxSelect>>", self.load_chat_content)

        layout.add(left_panel)

        center_panel = tk.Frame(layout, bg="#1e1e1e")
        topbar = tk.Frame(center_panel, bg="#1e1e1e")
        self.search_var = tk.StringVar()
        tk.Entry(topbar, textvariable=self.search_var, width=50).pack(side=tk.LEFT, padx=(10, 5), pady=5)
        tk.Button(topbar, text="🔍 Search GPT Data", command=self.run_search).pack(side=tk.LEFT, pady=5)
        tk.Button(topbar, text="🎙 Dictate", command=self.dictate_to_prompt, bg="#222", fg="#fff").pack(side=tk.RIGHT, padx=(0, 5))
        tk.Button(topbar, text="📂 Browse Local Folder", command=self.browse_folder).pack(side=tk.RIGHT, padx=10, pady=5)
        topbar.pack(fill=tk.X)

        self.chat_view = scrolledtext.ScrolledText(center_panel, bg="#1e1e1e", fg="#dcdcdc", wrap=tk.WORD)
        self.chat_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        plugin_bar = tk.Frame(center_panel, bg="#1e1e1e")
        tk.Label(plugin_bar, text="🛠 Manual Tools", bg="#1e1e1e", fg="#bbbbbb").pack(side=tk.LEFT, padx=(10, 5))
        self.manual_var = tk.StringVar()
        manual_menu = ttk.Combobox(plugin_bar, textvariable=self.manual_var, width=25)
        manual_menu["values"] = [
            "blog", "mailchimp_sync", "social", "firebase_sync",
            "github_push", "zap_trigger", "firestore_updater",
            "zip_uploader", "project_linker"
    ]
        manual_menu.pack(side=tk.LEFT)
        tk.Button(plugin_bar, text="▶", command=lambda: self.run_manual_plugin(), bg="#333", fg="#fff").pack(side=tk.LEFT, padx=(5, 20))

        tk.Label(plugin_bar, text="🧠 Auto Processors", bg="#1e1e1e", fg="#bbbbbb").pack(side=tk.RIGHT, padx=(5, 5))
        self.auto_var = tk.StringVar()
        auto_menu = ttk.Combobox(plugin_bar, textvariable=self.auto_var, width=25)
        auto_menu["values"] = [
            "auto_summary", "meta_writer", "tagger", "content_indexer",
            "chat_formatter", "chat_stats", "duplicate_finder",
            "chat_cleaner", "chat_merger"
    ]
        auto_menu.pack(side=tk.RIGHT)
        tk.Button(plugin_bar, text="▶", command=self.run_auto_plugin, bg="#333", fg="#fff").pack(side=tk.RIGHT, padx=(5, 10))
        plugin_bar.pack(fill=tk.X, pady=(5, 10))

        layout.add(center_panel)

        right_panel = tk.PanedWindow(layout, orient=tk.VERTICAL, bg="#1e1e1e", sashrelief=tk.RAISED)
        summary_top = tk.Frame(right_panel, bg="#1e1e1e")
        toggle_frame = tk.Frame(summary_top, bg="#1e1e1e")
        self.summary_view = scrolledtext.ScrolledText(summary_top, bg="#1e1e1e", fg="#dcdcdc", height=15)
        self.summary_view.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.current_view = tk.StringVar(value="Summary")
        for view in TOGGLE_VIEWS:
            b = tk.Radiobutton(toggle_frame, text=view, variable=self.current_view, value=view,
                              bg="#333", fg="#fff", selectcolor="#444", width=10,
                              command=self.update_summary_panel)
            b.pack(side=tk.LEFT, padx=2, pady=5)
        toggle_frame.pack(fill=tk.X)
        toggle_frame.pack_propagate(False)
        summary_top.pack(fill=tk.BOTH, expand=True)

        summary_bottom = tk.Frame(right_panel, bg="#1e1e1e")
        tk.Label(summary_bottom, text="📦 Assets", bg="#1e1e1e", fg="#bbb").pack(anchor="w", padx=10, pady=(10, 0))
        self.asset_list = tk.Listbox(summary_bottom, bg="#2d2d2d", fg="#ffffff")
        self.asset_list.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.asset_list.bind("<Double-Button-1>", self.open_asset)
        right_panel.add(summary_top)
        right_panel.add(summary_bottom)

        layout.add(right_panel)
        
        bottom = tk.Frame(self, bg="#1e1e1e")
        bottom.pack(fill=tk.X, pady=2)
        dashboard_colors = {
            "Admin": "#6C5B7B",
            "Sales": "#44dd88",
            "Marketing": "#ffaa00",
            "Tech": "#ff5555"
        }
        for label in ["Admin", "Sales", "Marketing", "Tech"]:
            tk.Button(bottom, text=label, width=15, command=lambda l=label: self.open_dashboard(l),
                    bg=dashboard_colors[label], fg="#fff").pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.load_projects()

        gpt_prompt_bar = tk.Frame(center_panel, bg="#1e1e1e")
        gpt_prompt_bar.pack(fill=tk.X, pady=(5, 0), padx=10)

        self.gpt_prompt = tk.StringVar()
        tk.Entry(gpt_prompt_bar, textvariable=self.gpt_prompt, width=100).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        tk.Button(gpt_prompt_bar, text="Ask GPT", command=self.ask_gpt, bg="#444", fg="#fff").pack(side=tk.RIGHT)
     
    def load_projects(self):
        self.folder_list.delete(0, tk.END)
        mode = self.project_mode.get()
        if mode == "Projects":
            for folder in os.listdir(DATA_PATH):
                path = os.path.join(DATA_PATH, folder)
                if os.path.isdir(path):
                    self.folder_list.insert(tk.END, folder)
        elif mode == "Chats":
            self.folder_list.insert(tk.END, "[All Loose Chats]")
        elif mode == "Sidebar":
            self.folder_list.insert(tk.END, "[Favorite Assistants]")

    def load_chats(self, event):
        selection = self.folder_list.curselection()
        if not selection:
            return
        selected = self.folder_list.get(selection[0])
        self.current_folder = os.path.join(DATA_PATH, selected)
        self.chat_list.delete(0, tk.END)
        if os.path.exists(self.current_folder):
            for chat in os.listdir(self.current_folder):
                path = os.path.join(self.current_folder, chat)
                if os.path.isdir(path):
                    self.chat_list.insert(tk.END, chat)

    def load_chat_content(self, event):
        selection = self.chat_list.curselection()
        if not selection:
            return
        selected = self.chat_list.get(selection[0])
        self.current_chat = os.path.join(self.current_folder, selected)
        chat_file = os.path.join(self.current_chat, "chat.md")
        self.chat_view.delete("1.0", tk.END)
        if os.path.exists(chat_file):
            with open(chat_file, encoding="utf-8") as f:
                self.chat_view.insert(tk.END, f.read())
        else:
            self.chat_view.insert(tk.END, "[No chat.md found]")
        self.update_summary_panel()
        self.load_assets()

    def update_summary_panel(self):
        self.summary_view.delete("1.0", tk.END)
        if not self.current_chat:
            return
        filename = {
            "Summary": "README.md",
            "Description": "description.md",
            "Inventory": "inventory.md"
        }.get(self.current_view.get(), "README.md")
        path = os.path.join(self.current_chat, filename)
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                self.summary_view.insert(tk.END, f.read())
        else:
            self.summary_view.insert(tk.END, f"[No {filename} found]")

    def load_assets(self):
        self.asset_list.delete(0, tk.END)
        if not self.current_chat:
            return
        asset_folder = os.path.join(self.current_chat, "assets")
        if os.path.exists(asset_folder):
            for f in os.listdir(asset_folder):
                self.asset_list.insert(tk.END, f)

    def open_asset(self, event):
        selection = self.asset_list.curselection()
        if not selection:
            return
        filename = self.asset_list.get(selection[0])
        full_path = os.path.join(self.current_chat, "assets", filename)
        os.startfile(full_path) if os.name == "nt" else subprocess.call(["open", full_path])

    def browse_folder(self):
        path = filedialog.askdirectory(title="Browse Local Folder")
        if path:
            self.chat_view.delete("1.0", tk.END)
            self.chat_view.insert(tk.END, f"[📂 Browsed: {path}]\n")
            for f in os.listdir(path):
                self.chat_view.insert(tk.END, f" - {f}\n")

    def run_search(self):
        term = self.search_var.get().strip()
        self.chat_view.delete("1.0", tk.END)
        if not term:
            self.chat_view.insert(tk.END, "[search] Please enter a term.\n")
            return
        try:
            with open("data/indexes/global_index.json", "r", encoding="utf-8") as f:
                index = json.load(f)
            matches = index.get(term.lower(), [])
            if matches:
                self.chat_view.insert(tk.END, f"[search] {len(matches)} result(s):\n\n")
                for m in set(matches):
                    self.chat_view.insert(tk.END, f"- {m}\n")
            else:
                self.chat_view.insert(tk.END, "[search] No matches found.\n")
        except Exception as e:
            self.chat_view.insert(tk.END, f"[search] Error: {e}")

    def run_manual_plugin(self):
        name = self.manual_var.get().strip()
        self.chat_view.delete("1.0", tk.END)
        if not name or not self.current_chat:
            self.chat_view.insert(tk.END, "[plugin] Select a plugin and chat first.\n")
            return
        subprocess.run(["python", f"plugins/{name}.py", "--folder", self.current_chat, "--test"], shell=True)

    def run_auto_plugin(self):
        name = self.auto_var.get().strip()
        self.chat_view.delete("1.0", tk.END)
        if not name or not self.current_chat:
            self.chat_view.insert(tk.END, "[auto plugin] Select plugin and chat first.\n")
            return
        subprocess.run(["python", f"plugins/{name}.py", "--folder", self.current_chat, "--test"], shell=True)

    def open_dashboard(self, label):
        path = f"interface/{label.lower()}_dashboard.py"
        self.chat_view.insert(tk.END, f"[dashboard] Launching {label} → {path}\n")
        if os.path.exists(path):
            subprocess.Popen(["python", path], shell=True)
        else:
            self.chat_view.insert(tk.END, f"[dashboard] Missing file: {path}\n")

    def ask_gpt(self):
        print("ask_gpt was triggered")
        from openai import OpenAI
        from dotenv import load_dotenv
        import os

        load_dotenv()

        prompt = self.gpt_prompt.get().strip()
        if not prompt:
            self.chat_view.insert(tk.END, "\n[GPT] No prompt provided.\n")
            return

        try:
            self.chat_view.insert(tk.END, f"\n[GPT] Asking: {prompt}\n")
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are CommandCoreOS. Respond clearly and intelligently."},
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content
            self.chat_view.insert(tk.END, f"\n[GPT Reply]\n{reply}\n")

            if self.current_chat:
                out_path = os.path.join(self.current_chat, "chat.md")
                with open(out_path, "a", encoding="utf-8") as f:
                    f.write(f"\n\nUser:\n{prompt}\n\nAssistant:\n{reply}\n")

        except Exception as e:
            self.chat_view.insert(tk.END, f"\n[GPT ERROR] {str(e)}\n")
    

def launch_gui():
    app = CommandCoreGUI()
    app.mainloop()

launch_gui()

