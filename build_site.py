import argparse
import os
import json

from common import get_client, merge_metadata, finalize, edit

def get_link(id: str, path: str) -> dict:
    cmd = [get_client(), 'content', 'describe', id, '--config', args.config]
    data = json.loads(os.popen(' '.join(cmd)).read())
    hash = data["hash"]
    return {"/": f"/qfab/{hash}/{path}"}

def main():
    links = {}
    with open(args.contents, 'r') as f:
        for i, line in enumerate(f):
            id = line.strip()
            link = get_link(id, args.path)
            links[str(i+1)] = link
    site_data = json.dumps({"site_map": {"searchables": links}})
    tok = edit(args.site, args.config)
    merge_metadata(tok, site_data, args.config)
    if args.finalize:
        finalize(tok, args.config)
    else:
        print(f"please finalize: {tok}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=str)
    parser.add_argument("--contents", required=True, type=str)
    parser.add_argument("--config", type=str)
    parser.add_argument("--path", type=str)
    parser.add_argument("--finalize", type=bool)
    args = parser.parse_args()
    main()