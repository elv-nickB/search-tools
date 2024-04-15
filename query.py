import argparse
import os

from common import get_client

def query(query: str, id: str, config: str) -> dict:
    cmd = [get_client(), 'content', 'bitcode', 'rep', id, 'search', "'" + query + "'", '--config', config]
    return os.popen(' '.join(cmd)).read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    print(query(args.query, args.id, args.config))

if __name__ == "__main__":
    main()