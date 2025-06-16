from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID
import os

# Define the schema for indexing
schema = Schema(
    name=TEXT(stored=True),
    path=ID(stored=True, unique=True),
    content=TEXT
)

def index_memory(folder_path, index_dir):
    """
    Indexes all text files in the specified folder using Whoosh.

    Args:
        folder_path (str): Path to the folder containing memory files.
        index_dir (str): Path to the directory where the index will be stored.
    """
    if not os.path.exists(index_dir):
        os.makedirs(index_dir)

    ix = create_in(index_dir, schema)
    writer = ix.writer()

    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                writer.add_document(
                    name=file,
                    path=os.path.relpath(file_path, folder_path),
                    content=content
                )

    writer.commit()
    print(f"Index created in {index_dir}")

if __name__ == "__main__":
    memory_folder = os.path.dirname(os.path.abspath(__file__))  # Current folder
    index_directory = os.path.join(memory_folder, "whoosh_index")
    index_memory(memory_folder, index_directory)
