import tkinter as tk
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
from memory_router import save_to_memory, load_latest  # ✅ Router import

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up paths
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "chat_log.txt")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Append to chat log
def log_chat_entry(role, message):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{role.upper()}] {datetime.now().isoformat()}\n{message}\n\n")

# Call OpenAI
def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# Track last messages
last_user_message = ""
last_ai_message = ""

# Save last message to STM via router
def save_to_stm():
    global last_user_message, last_ai_message
    if not last_user_message or not last_ai_message:
        print("[INFO] No messages to save.")
        return

    save_to_memory("short_term", f"USER: {last_user_message}\nAI: {last_ai_message}")

# Load latest STM via router
def load_from_stm():
    content = load_latest("short_term")
    if content:
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"[STM Memory]\n{content}\n\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.see(tk.END)
    else:
        print("[INFO] No STM memory found.")

# Send message logic
def send_message():
    global last_user_message, last_ai_message
    user_msg = entry.get()
    if not user_msg.strip():
        return

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"You: {user_msg}\n")
    log_chat_entry("user", user_msg)
    entry.delete(0, tk.END)

    ai_msg = get_ai_response(user_msg)
    chat_log.insert(tk.END, f"AI: {ai_msg}\n\n")
    log_chat_entry("ai", ai_msg)

    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)

    save_to_memory("long_term", f"USER: {user_msg}\nAI: {ai_msg}")  # ✅ Routed save
    last_user_message = user_msg
    last_ai_message = ai_msg

# GUI layout
root = tk.Tk()
root.title("CommandCore Chat Interface")
root.configure(bg="#1e1e1e")

chat_log = tk.Text(
    root, wrap=tk.WORD, state=tk.DISABLED,
    width=80, height=30,
    bg="#1e1e1e", fg="#ffffff",
    insertbackground="#ffffff",
    highlightbackground="#3c3c3c", highlightcolor="#3c3c3c"
)
chat_log.pack(padx=10, pady=10)

entry = tk.Entry(
    root, width=80,
    bg="#2d2d2d", fg="#ffffff",
    insertbackground="#ffffff",
    highlightbackground="#3c3c3c", highlightcolor="#3c3c3c"
)
entry.pack(padx=10, pady=(0, 10))
entry.focus()

send_button = tk.Button(
    root, text="Send", command=send_message,
    bg="#3c3c3c", fg="#ffffff",
    activebackground="#2d2d2d", activeforeground="#ffffff"
)
send_button.pack()

scrollbar = tk.Scrollbar(root, bg="#3c3c3c", troughcolor="#1e1e1e", activebackground="#2d2d2d")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_log.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_log.yview)

save_stm_button = tk.Button(
    root, text="Save to STM", command=save_to_stm,
    bg="#3c3c3c", fg="#ffffff",
    activebackground="#2d2d2d", activeforeground="#ffffff"
)
save_stm_button.pack()

load_stm_button = tk.Button(
    root, text="Load from STM", command=load_from_stm,
    bg="#3c3c3c", fg="#ffffff",
    activebackground="#2d2d2d", activeforeground="#ffffff"
)
load_stm_button.pack()

root.mainloop()
