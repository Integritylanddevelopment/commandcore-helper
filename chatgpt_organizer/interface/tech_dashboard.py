# interface/tech_dashboard.py
import tkinter as tk

class TechDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tech Dashboard")
        self.geometry("800x600")
        self.configure(bg="#1e1e1e")

        tk.Label(self, text="Developer Tools", font=("Segoe UI", 16), fg="#fff", bg="#1e1e1e").pack(pady=20)

        actions = [
            "Push to Firestore", "Build Indexes", "Re-tag Chats",
            "Run LLM Labeler", "Check Error Logs"
        ]
        for action in actions:
            tk.Button(self, text=action, width=30, bg="#333", fg="#fff").pack(pady=5)

if __name__ == "__main__":
    app = TechDashboard()
    app.mainloop()
