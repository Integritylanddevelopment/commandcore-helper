# chatgpt_organizer/interface/admin_dashboard.py

import tkinter as tk
import subprocess
import os
import json
from tkinter.simpledialog import askstring
from tkinter import filedialog, messagebox

class AdminDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("800x600")
        self.configure(bg="#1e1e1e")

        tk.Label(self, text="Admin Controls", font=("Segoe UI", 16), fg="#fff", bg="#1e1e1e").pack(pady=20)

        tk.Button(self, text="🔗 Link Assistant to Project", width=40, command=self.link_assistant, bg="#333", fg="#fff").pack(pady=10)
        tk.Button(self, text="⬇️ Sync From GPT", width=40, command=self.sync_from_gpt, bg="#333", fg="#fff").pack(pady=10)
        tk.Button(self, text="🔄 Rebuild Index", width=40, command=self.rebuild_index, bg="#333", fg="#fff").pack(pady=10)

    def link_assistant(self):
        project = askstring("Project Name", "Enter local project name:")
        assistant_id = askstring("Assistant ID", "Enter OpenAI Assistant ID:")
        thread_id = askstring("Thread ID", "Enter OpenAI Thread ID:")

        if project and assistant_id and thread_id:
            subprocess.run([
                "python", "agents/assistant_link.py",
                "--project", project,
                "--assistant", assistant_id,
                "--thread", thread_id
            ], shell=True)

    def sync_from_gpt(self):
        project = askstring("Project Name", "Enter project name to sync:")
        if not project:
            return

        try:
            with open("config/assistant_links.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load assistant_links.json\n\n{e}")
            return

        link = data.get(project)
        if not link:
            messagebox.showerror("Error", f"No assistant/thread linked for project: {project}")
            return

        subprocess.run([
            "python", "agents/assistant_sync.py",
            "--thread", link["thread_id"],
            "--project", project,
            "--chat", "chat_from_gpt"
        ], shell=True)

    def rebuild_index(self):
        subprocess.run(["python", "search/index_builder.py", "--folder", "data/organized", "--test"], shell=True)

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
