#!/usr/bin/env python3

import argparse
import json
import string

def generate_punctuation_table() -> dict:
    table = {}
    for symbol in string.punctuation:
        table[symbol] = None
    return table

def remove_punctuation(str, table) -> str:
    translation_table = str.maketrans(table)
    return str.translate(translation_table)

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here            
            with open("data/movies.json", 'r') as f:
                dic = json.load(f)
                result = []
                
                table = generate_punctuation_table()
                for movie in dic["movies"]:
                    # Simple substring match for demonstration purposes
                    if args.query.lower() in remove_punctuation(movie["title"], table).lower():
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
