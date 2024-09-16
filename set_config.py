import argparse
import json

from common import edit, merge_metadata, get_metadata, finalize

def main():
    with open(args.source) as f:
        config = json.load(f)
    tok = edit(args.dest, args.config)
    merge_metadata(tok, json.dumps(config), args.config)
    if args.finalize:
        finalize(tok, args.config, args.message)
    else:
        print(f'Please finalize token {tok}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="Path to the config file")
    parser.add_argument("--source", type=str, help="json file containing index config")
    parser.add_argument("--dest", type=str, help="QID of the index to copy config to")
    parser.add_argument("--message", type=str)
    parser.add_argument("--finalize", action="store_true")
    args = parser.parse_args()
    main()