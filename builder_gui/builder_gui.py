import tkinter as tk
from datetime import datetime
import os
import openai
from dotenv import load_dotenv
import json
import tkinter.filedialog
import tkinter.messagebox
import math
import sys
import glob

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up paths
MEMORY_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../CommandCore-OS/memory/"))
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs", "chat_log.txt")

# Ensure log directory exists
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

# Memory write (to long-term memory for now)
def write_to_memory(bucket, content):
    filename = f"{MEMORY_ROOT}{bucket}/entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(content)

# Append to chat log
def log_chat_entry(role, message):
    with open(LOG_PATH, "a") as f:
        f.write(f"[{role.upper()}] {datetime.now().isoformat()}\n{message}\n\n")

# Update the get_ai_response function to use OpenAI's API
def get_ai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

# Function to save the last user and AI message pair to short-term memory
last_user_message = ""
last_ai_message = ""

def save_to_stm():
    global last_user_message, last_ai_message
    if not last_user_message or not last_ai_message:
        print("[INFO] No messages to save to STM.")
        return

    stm_filename = os.path.join(MEMORY_ROOT, "short_term", f"entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    os.makedirs(os.path.dirname(stm_filename), exist_ok=True)
    with open(stm_filename, "w") as f:
        f.write(f"USER: {last_user_message}\nAI: {last_ai_message}")
    print(f"[INFO] Saved to STM: {stm_filename}")

# Function to load the most recent file from short-term memory and display its content
def load_from_stm():
    stm_dir = os.path.join(MEMORY_ROOT, "short_term")
    if not os.path.exists(stm_dir):
        print("[INFO] STM directory does not exist.")
        return

    # Find the most recent file based on timestamp in filename
    files = [f for f in os.listdir(stm_dir) if f.startswith("entry_") and f.endswith(".txt")]
    if not files:
        print("[INFO] No STM files found.")
        return

    most_recent_file = max(files, key=lambda f: os.path.getmtime(os.path.join(stm_dir, f)))
    most_recent_path = os.path.join(stm_dir, most_recent_file)

    with open(most_recent_path, "r", encoding="utf-8") as f:
        content = f.read()

    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"[STM Memory]\n{content}\n\n")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)

    print(f"[INFO] Loaded from STM: {most_recent_path}")

# Function to summarize short-term memory (placeholder logic)
def summarize_stm():
    summary = "This is a placeholder summary for short-term memory."
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, f"[STM Summary]\n{summary}\n\n")
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)

# Update GUI layout and functionality
root = tk.Tk()
root.title("Builder GUI")

# Input field for user prompt
prompt_label = tk.Label(root, text="Prompt:")
prompt_label.pack()
prompt_entry = tk.Entry(root, width=80)
prompt_entry.pack(padx=10, pady=5)

# Optional field for system prompt
system_prompt_label = tk.Label(root, text="System Prompt:")
system_prompt_label.pack()
system_prompt_entry = tk.Entry(root, width=80)
system_prompt_entry.insert(0, "You are a helpful assistant.")
system_prompt_entry.pack(padx=10, pady=5)

# Output display
output_display = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED, width=80, height=20, bg="#1e1e1e", fg="#ffffff", insertbackground="#ffffff", highlightbackground="#3c3c3c", highlightcolor="#3c3c3c")
output_display.pack(padx=10, pady=10)

# Functionality for buttons
def send_to_openai():
    user_prompt = prompt_entry.get()
    system_prompt = system_prompt_entry.get()
    if not user_prompt.strip():
        return

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        reply = response['choices'][0]['message']['content'].strip()
        output_display.config(state=tk.NORMAL)
        output_display.insert(tk.END, f"AI: {reply}\n\n")
        output_display.config(state=tk.DISABLED)

        # Handle session naming and logging
        handle_session_naming_and_logging(user_prompt, reply)
    except Exception as e:
        output_display.config(state=tk.NORMAL)
        output_display.insert(tk.END, f"Error: {str(e)}\n\n")
        output_display.config(state=tk.DISABLED)

# Session filename variable
session_filename = None

# Functionality to handle session naming and rolling memory log
def handle_session_naming_and_logging(prompt, response):
    global session_filename

    # If session filename is not set, generate it
    if session_filename is None:
        try:
            system_prompt = "Give this working session a short semantic filename (2–5 words, underscore style, no punctuation). Return only the name."
            gpt_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": response}
                ]
            )
            session_filename = gpt_response['choices'][0]['message']['content'].strip() + ".md"
            session_filepath = os.path.join(MEMORY_ROOT, "working_memory", "working_today", session_filename)
            os.makedirs(os.path.dirname(session_filepath), exist_ok=True)

            # Create the session file
            with open(session_filepath, "w", encoding="utf-8") as f:
                f.write(f"# Session Log: {session_filename}\n\n")
            print(f"[INFO] Session file created: {session_filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to generate session filename: {e}")
            return

    # Append the new exchange to the session file
    try:
        session_filepath = os.path.join(MEMORY_ROOT, "working_memory", "working_today", session_filename)
        timestamp = datetime.now().strftime("%H:%M")
        with open(session_filepath, "a", encoding="utf-8") as f:
            f.write(f"## 🔹 [{timestamp}] Response\n")
            f.write(f"**Prompt:**\n{prompt}\n\n")
            f.write(f"**Response:**\n{response}\n\n")
        print(f"[INFO] Exchange appended to session file: {session_filepath}")
    except Exception as e:
        print(f"[ERROR] Failed to append exchange to session file: {e}")

def save_response():
    response_text = output_display.get("1.0", tk.END).strip()
    if not response_text:
        return

    os.makedirs("logs/response", exist_ok=True)
    filename = os.path.join("logs/response", f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(response_text)

def load_last_response():
    response_dir = "logs/response"
    if not os.path.exists(response_dir):
        return

    files = [f for f in os.listdir(response_dir) if f.endswith(".md")]
    if not files:
        return

    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(response_dir, f)))
    with open(os.path.join(response_dir, latest_file), "r", encoding="utf-8") as f:
        content = f.read()

    output_display.config(state=tk.NORMAL)
    output_display.insert(tk.END, f"[Loaded Response]\n{content}\n\n")
    output_display.config(state=tk.DISABLED)

def export_task():
    user_prompt = prompt_entry.get()
    system_prompt = system_prompt_entry.get()
    task = {
        "prompt": user_prompt,
        "system_prompt": system_prompt
    }
    with open("task.json", "w", encoding="utf-8") as f:
        json.dump(task, f, indent=4)

# Functionality for uploading folder contents to GPT with improved filtering and processing
def upload_folder_to_gpt():
    folder_path = tkinter.filedialog.askdirectory(title="Select Folder")
    if not folder_path:
        print("[INFO] No folder selected.")
        return

    combined_content = ""
    file_count = 0
    excluded_folders = {"venv", "__pycache__", ".git", "node_modules", ".vscode", "logs", "__archive"}
    excluded_extensions = {".zip", ".exe", ".dll", ".png", ".jpg", ".pdf"}
    accepted_extensions = {".py", ".md", ".txt", ".json", ".yaml", ".yml"}

    for root, dirs, files in os.walk(folder_path):
        # Exclude specific folders
        dirs[:] = [d for d in dirs if d not in excluded_folders]

        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file)[1].lower()

            # Skip excluded files
            if file_extension in excluded_extensions or os.path.getsize(file_path) > 1 * 1024 * 1024:
                continue

            # Process accepted files
            if file_extension in accepted_extensions:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        combined_content += f.read() + "\n"
                        file_count += 1
                except Exception as e:
                    print(f"[ERROR] Failed to read file {file_path}: {e}")

    if not combined_content.strip():
        print("[INFO] No content to send to GPT.")
        return

    # Token estimation
    token_count = math.ceil(len(combined_content) / 4)  # Approximation: 4 chars = 1 token
    input_cost = token_count * 0.0005 / 1000
    output_cost = token_count * 0.0015 / 1000
    total_cost = input_cost + output_cost

    proceed = tkinter.messagebox.askyesno(
        "Cost Estimate",
        f"Files processed: {file_count}\nEstimated total tokens: {token_count}\nEstimated input+output cost: ${total_cost:.4f}\nProceed?"
    )

    if not proceed:
        print("[INFO] User canceled the operation.")
        return

    # Chunking logic
    max_tokens_per_chunk = 10000
    chunks = []
    lines = combined_content.splitlines()
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) > max_tokens_per_chunk * 4:  # Approximation: 4 chars = 1 token
            chunks.append(current_chunk)
            current_chunk = ""
        current_chunk += line + "\n"

    if current_chunk:
        chunks.append(current_chunk)

    # Send chunks sequentially
    combined_reply = ""
    for i, chunk in enumerate(chunks):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": chunk.strip()}]
            )
            reply = response['choices'][0]['message']['content'].strip()
            combined_reply += reply + "\n"
            print(f"[INFO] Chunk {i+1}/{len(chunks)} processed.")
        except Exception as e:
            print(f"[ERROR] Failed to process chunk {i+1}: {e}")

    # Display combined reply in GUI
    output_display.config(state=tk.NORMAL)
    output_display.insert(tk.END, f"AI: {combined_reply}\n\n")
    output_display.config(state=tk.DISABLED)

# Buttons
send_button = tk.Button(root, text="Send", command=send_to_openai, bg="#3c3c3c", fg="#ffffff", activebackground="#2d2d2d", activeforeground="#ffffff")
send_button.pack(pady=5)

save_button = tk.Button(root, text="Save", command=save_response, bg="#3c3c3c", fg="#ffffff", activebackground="#2d2d2d", activeforeground="#ffffff")
save_button.pack(pady=5)

load_last_button = tk.Button(root, text="Load Last", command=load_last_response, bg="#3c3c3c", fg="#ffffff", activebackground="#2d2d2d", activeforeground="#ffffff")
load_last_button.pack(pady=5)

export_button = tk.Button(root, text="Export as task.json", command=export_task, bg="#3c3c3c", fg="#ffffff", activebackground="#2d2d2d", activeforeground="#ffffff")
export_button.pack(pady=5)

upload_button = tk.Button(root, text="Upload Folder to GPT", command=upload_folder_to_gpt, bg="#3c3c3c", fg="#ffffff", activebackground="#2d2d2d", activeforeground="#ffffff")
upload_button.pack(pady=5)

# Functionality to handle GUI window close event
def on_close():
    print("[INFO] GUI window closed.")
    sys.exit()

# Bind the on_close event to the tkinter WM_DELETE_WINDOW
root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
