import argparse
import os
import json
from tqdm import tqdm

from common import get_client, merge_metadata, finalize, edit, get_metadata, content_info

def get_link(id: str, path: str) -> dict:
    cmd = [get_client(), 'content', 'describe', id, '--config', args.config]
    try:
        res = os.popen(' '.join(cmd)).read()
        data = json.loads(res)
    except json.JSONDecodeError as e:
        print(f"error with {id}")
        print(res)
        raise e
    hash = data["hash"]
    return {"/": f"/qfab/{hash}/{path}"}

def main():
    links = {}
    if not args.contents:
        # then we just update what's already on the site
        # read qids from site_map
        site_map = get_metadata(args.site, "/site_map/searchables", resolve=False, config=args.config)
        for k, link in tqdm(site_map.items()):
            hash = link["/"].split('/')[2]
            qid = content_info(hash, args.config)["id"]
            l = get_link(qid, args.path)
            links[k] = l
    else:
        with open(args.contents, 'r') as f:
            for i, line in tqdm(enumerate(f)):
                id = line.strip()
                link = get_link(id, args.path)
                print(link)
                links[str(i+1)] = link
    site_data = json.dumps({"site_map": {"searchables": links}})
    tok = edit(args.site, args.config)
    merge_metadata(tok, site_data, args.config)
    if args.finalize:
        print(f"finalizing {tok}")
        finalize(tok, args.config, args.message)
    else:
        print(f"please finalize: {tok}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, type=str)
    parser.add_argument("--contents", required=False, type=str)
    parser.add_argument("--config", type=str)
    parser.add_argument("--path", type=str)
    parser.add_argument("--finalize", action='store_true')
    parser.add_argument(
        "--message",
        type=str,
        help="commit message",
    )
    args = parser.parse_args()
    main()