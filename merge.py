from loguru import logger
import argparse

from common import edit, finalize, merge_metadata

def main():
    tok = edit(args.id, args.config)
    with open(args.data, 'r') as f:
        data = f.read()
    merge_metadata(tok, data, args.config)
    if args.finalize:
        finalize(tok, args.config)
    else:
        logger.info('please finalize the token', tok)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--data", required=True)
    parser.add_argument("--finalize", action='store_true')
    args = parser.parse_args()
    main()