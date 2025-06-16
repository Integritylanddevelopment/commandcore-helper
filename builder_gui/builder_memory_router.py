import os
from datetime import datetime
from summary import generate_summary_from_file  # ✅ Adjust if needed

# Root memory folder
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../CommandCore-OS/memory"))
LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/memory_router_log.txt")

# Allowed memory types
ALLOWED_BUCKETS = [
    "short_term",
    "long_term",
    "working_memory",
    "episodic_memory",
    "semantic_memory",
    "procedural_memory"
]

# Make sure the path exists
def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

# Log general usage
def log_event(msg):
    ensure_dir(os.path.dirname(LOG_PATH))
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[EVENT] {datetime.now().isoformat()} — {msg}\n")

# Log violations
def log_violation(msg):
    ensure_dir(os.path.dirname(LOG_PATH))
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[VIOLATION] {datetime.now().isoformat()} — {msg}\n")
    print(msg)

# Save content to a memory bucket
def save_to_memory(bucket, content):
    if bucket not in ALLOWED_BUCKETS:
        log_violation(f"❌ Invalid memory bucket: {bucket}")
        return False

    folder = os.path.join(BASE_PATH, bucket)
    ensure_dir(folder)

    filename = f"entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(folder, filename)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        log_event(f"✅ Saved to {bucket}: {filename}")
        return True
    except Exception as e:
        log_violation(f"❌ Write failed: {e}")
        return False

# Load most recent memory entry from a bucket
def load_latest(bucket):
    if bucket not in ALLOWED_BUCKETS:
        log_violation(f"❌ Invalid bucket for loading: {bucket}")
        return None

    folder = os.path.join(BASE_PATH, bucket)
    if not os.path.exists(folder):
        return None

    files = [f for f in os.listdir(folder) if f.startswith("entry_") and f.endswith(".txt")]
    if not files:
        return None

    latest = max(files, key=lambda f: os.path.getmtime(os.path.join(folder, f)))
    filepath = os.path.join(folder, latest)

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        log_violation(f"❌ Read failed: {e}")
        return None

# Summarize the most recent file in a memory bucket
def summarize_latest(bucket):
    if bucket not in ALLOWED_BUCKETS:
        log_violation(f"❌ Cannot summarize unknown bucket: {bucket}")
        return None

    folder = os.path.join(BASE_PATH, bucket)
    if not os.path.exists(folder):
        return f"❌ No such bucket folder: {folder}"

    files = [f for f in os.listdir(folder) if f.startswith("entry_") and f.endswith(".txt")]
    if not files:
        return "⚠️ No memory entries found to summarize."

    latest = max(files, key=lambda f: os.path.getmtime(os.path.join(folder, f)))
    file_path = os.path.join(folder, latest)

    try:
        summary = generate_summary_from_file(file_path)
        log_event(f"🧠 Summary generated for: {file_path}")
        return summary
    except Exception as e:
        log_violation(f"❌ Summary error: {e}")
        return f"❌ Could not summarize: {str(e)}"
