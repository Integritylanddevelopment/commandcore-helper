# interface/marketing_dashboard.py
import tkinter as tk

class MarketingDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Marketing Dashboard")
        self.geometry("800x600")
        self.configure(bg="#1e1e1e")

        tk.Label(self, text="Marketing Commands", font=("Segoe UI", 16), fg="#fff", bg="#1e1e1e").pack(pady=20)

        actions = [
            "Publish Blog", "Send Campaign", "Draft Social Post",
            "Sync Mailchimp", "Review Copy"
        ]
        for action in actions:
            tk.Button(self, text=action, width=30, bg="#333", fg="#fff").pack(pady=5)

if __name__ == "__main__":
    app = MarketingDashboard()
    app.mainloop()
