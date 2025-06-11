import os
from explorer.tree_view import display_tree
from explorer.preview_pane import show_preview
from explorer.folder_contents import show_folder_contents
from explorer.chat_replay import replay_chat
from search.query import run as search_query

def handle_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return

    cmd = parts[0].lower()
    args = parts[1:]

    if cmd == ":tree":
        display_tree()
    elif cmd == ":preview" and args:
        show_preview(args[0])
    elif cmd == ":contents" and args:
        show_folder_contents(args[0])
    elif cmd == ":replay" and args:
        replay_chat(args[0])
    elif cmd == ":search" and args:
        search_query(' '.join(args))
    elif cmd == ":exit":
        print("Exiting...")
        exit()
    else:
        print(f"Unknown command: {cmd}")
