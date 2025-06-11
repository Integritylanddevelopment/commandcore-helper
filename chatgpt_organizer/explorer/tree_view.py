import os
from pathlib import Path

def display_tree(base_path='data/organized'):
    print("\nProject Tree:")
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = '  ' * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '  ' * (level + 1)
        for f in files:
            if f.endswith('.json') or f.endswith('.md'):
                print(f"{subindent}{f}")
