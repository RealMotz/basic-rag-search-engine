#!/usr/bin/env python3

import argparse
import json
import os
import string

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "movies.json")

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text

def tokenize(text: str) -> list[str]:
    text = preprocess_text(text)
    text = text.split()
    return text

def has_match(query_tokens, title_tokens) -> bool:
    for query in query_tokens:
        for title in title_tokens:
            if query in title:
                return True
    return False

def load_movies() -> list[dict]:
    with open(DATA_PATH, 'r') as f:
        dic = json.load(f)
    return dic["movies"]

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            result = []
            # Simple substring match for demonstration purposes
            for movie in load_movies():
                title = preprocess_text(movie["title"])
                query = preprocess_text(args.query)
                if has_match(tokenize(query), tokenize(title)):
                    result.append(movie)

            result = result[:5]
            sorted_results = sorted(result, key=lambda m: m["id"])

            print(f"Searching for: {args.query}")
            for movie, idx in zip(sorted_results, range(1, len(sorted_results) + 1)):
                print(f"{idx}. {movie['title']}")
            pass
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
