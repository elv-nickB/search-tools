import argparse
import os
import json

def query(query: str, id: str, config: str, use_elv: bool=False) -> dict:
    client = 'elv' if use_elv else 'qfab_cli'
    cmd = [client, 'content', 'bitcode', 'rep', id, 'search', "'" + query + "'", '--config', config]
    result = os.popen(' '.join(cmd)).read()
    print(json.loads(result))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--use_elv", action='store_true')
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    return query(args.query, args.id, args.config, args.use_elv)

if __name__ == "__main__":
    main()