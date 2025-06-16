#!/usr/bin/env python3
"""
search_index_whoosh.py

Searches the Whoosh index created by index_memory_whoosh.py.
Supports context lines and ANSI highlighting for matched terms.

Usage:
  python search_index_whoosh.py "query goes here"
  python search_index_whoosh.py "query goes here" --fuzzy

Dependencies:
  pip install whoosh
"""

import os
import sys
import re
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.query import FuzzyTerm, And

# Set this to your actual index directory
INDEX_DIR = os.path.join("..", "whoosh_index")
# Updated functionality: Search the entire memory folder index.

# Number of lines of context before/after each match
CONTEXT_LINES = 2

# ANSI color for highlighting
HIGHLIGHT_COLOR = "\033[93m"  # yellow
RESET_COLOR = "\033[0m"

def highlight_matches(text, terms):
    """
    Naive highlight approach: highlight each term in text.
    Case-insensitive. We'll do a simple re.sub for each term.
    """
    for term in terms:
        # Use a regex to find term case-insensitively
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        text = pattern.sub(lambda m: f"{HIGHLIGHT_COLOR}{m.group(0)}{RESET_COLOR}", text)
    return text

def get_context_lines(content, match_start, match_end, window):
    """
    Returns the lines around the matched region. We approximate match_start/match_end
    by counting characters. We'll split lines, then figure out which line range
    that matched content belongs to.

    For a more robust approach, you'd rely on Whoosh's highlights. But here's a manual approach.
    """
    lines = content.split("\n")
    char_count = 0
    start_line = None
    end_line = None

    for i, line in enumerate(lines):
        line_len = len(line) + 1  # +1 for newline
        if start_line is None and char_count + line_len > match_start:
            start_line = max(0, i - window)
        if end_line is None and char_count + line_len >= match_end:
            end_line = min(len(lines), i + window + 1)
            break
        char_count += line_len

    if start_line is None: 
        start_line = 0
    if end_line is None: 
        end_line = len(lines)

    snippet = lines[start_line:end_line]
    snippet_str = "\n".join(snippet)
    return snippet_str, start_line, end_line

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Search Whoosh index with optional fuzzy search.")
    parser.add_argument("query", nargs="+", help="Search query")
    parser.add_argument("--fuzzy", action="store_true", help="Enable fuzzy search (edit distance 2)")
    args = parser.parse_args()

    query_terms = args.query
    query_str = " ".join(query_terms)
    fuzzy_search = args.fuzzy

    if not query_terms:
        print("Please provide a search query.")
        sys.exit(1)

    # Ensure the index directory exists
    if not os.path.exists(INDEX_DIR):
        print(f"[ERROR] Whoosh index directory not found: {INDEX_DIR}\nRun index_memory_whoosh.py first.")
        sys.exit(1)

    # Update search logic to query the entire memory folder index
    ix = index.open_dir(INDEX_DIR)
    query_parser = QueryParser("content", schema=ix.schema)
    query = query_parser.parse(query_str)

    with ix.searcher() as searcher:
        if fuzzy_search:
            # Support multi-word fuzzy search
            # Only include non-empty terms for FuzzyTerm
            fuzzy_terms = [term for term in query_terms if term.strip()]
            if not fuzzy_terms:
                print("Please provide a non-empty search query for fuzzy search.")
                sys.exit(1)
            q = And([FuzzyTerm("content", term, maxdist=2) for term in fuzzy_terms])
            results = searcher.search(q, limit=None)
            terms = fuzzy_terms
        else:
            results = searcher.search(query, limit=None)
            terms = query_terms

        if not results:
            print(f"[NO MATCH] No results found for: {query_str}")
            print("Tip: Try --fuzzy for approximate matches.")
            return

        for hit in results:
            filename = hit.get("filename", "<no filename>")
            doc_content = hit.get("content", "")
            print(f"\n=== MATCH in: {filename} ===")

            fragments = hit.highlights("content", top=5, minscore=1)
            if fragments:
                snippet_clean = fragments.replace("<b>", HIGHLIGHT_COLOR).replace("</b>", RESET_COLOR)
                print("WHOOSH snippet:\n", snippet_clean)
            else:
                # Manual fallback
                for match in hit.matches("content"):
                    start_pos = match["startchar"]
                    end_pos = match["endchar"]
                    snippet_str, sline, eline = get_context_lines(doc_content, start_pos, end_pos, CONTEXT_LINES)
                    snippet_str = highlight_matches(snippet_str, terms)
                    print(f"\nContext lines {sline}-{eline}:\n{snippet_str}\n")

        print(f"\n[DONE] Found {len(results)} matching file(s).")

def index_summaries():
    """Index summaries for fast searching."""
    from whoosh.fields import Schema, TEXT, ID
    from whoosh.index import create_in
    from whoosh.qparser import QueryParser

    # Define schema for indexing
    schema = Schema(
        title=TEXT(stored=True),
        path=ID(stored=True),
        content=TEXT
    )

    # Create index directory if it doesn't exist
    index_dir = "whoosh_index"
    os.makedirs(index_dir, exist_ok=True)

    # Create index
    ix = create_in(index_dir, schema)
    writer = ix.writer()

    # Path to summaries
    summaries_dir = "D:/ActiveProjects/CommandCore-Hub_v2025.01.01/memory/logs/summary/summary_logs"

    for filename in os.listdir(summaries_dir):
        if filename.endswith("_summary.md"):
            filepath = os.path.join(summaries_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                writer.add_document(
                    title=filename,
                    path=filepath,
                    content=content
                )

    writer.commit()

if __name__ == "__main__":
    main()
    index_summaries()
