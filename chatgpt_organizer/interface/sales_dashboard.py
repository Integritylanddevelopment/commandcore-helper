# interface/sales_dashboard.py
import tkinter as tk

class SalesDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sales Dashboard")
        self.geometry("800x600")
        self.configure(bg="#1e1e1e")

        tk.Label(self, text="Sales Toolkit", font=("Segoe UI", 16), fg="#fff", bg="#1e1e1e").pack(pady=20)

        actions = [
            "View Stripe Logs", "Send Invoice", "Sync Leads",
            "Generate Proposal", "Tag Client Stage"
        ]
        for action in actions:
            tk.Button(self, text=action, width=30, bg="#333", fg="#fff").pack(pady=5)

if __name__ == "__main__":
    app = SalesDashboard()
    app.mainloop()
