import argparse
import os
import json
import tempfile
import time
from loguru import logger

from common import edit, finalize, get_client

def crawl(tok: str, config: str) -> None:
    logger.debug(f"Write token: {tok}")
    with tempfile.NamedTemporaryFile() as fp:
        finished = False
        logger.debug(f"Awaiting crawl")
        lro = search_update(tok, fp, config)
        logger.info(f"lro handle: {lro}")
        while not finished:
            state = status(tok, lro, fp.name, config)
            finished = state == "terminated"
            time.sleep(7)

def search_update(tok: str, temp_file: any, config: str) -> str:
    cmd = [get_client(), 'content', 'bitcode', 'call', tok, 'search_update', '\"\"', temp_file.name, '--config', config, '--finalize=false', '--post']
    os.popen(' '.join(cmd)).read()
    lro = json.load(temp_file)
    return json.dumps(lro)

def status(tok: str, lro: str, f: str, config: str) -> str:
    cmd = [get_client(), 'content', 'bitcode', 'call', tok, 'crawl_status', "'" + lro + "'", f, '--config', config, '--post']
    os.popen(' '.join(cmd)).read()
    with open(f, 'r') as ff:
        status = ff.read()
    logger.info(status)
    return json.loads(status)["state"]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", required=True, nargs='+')
    parser.add_argument("--finalize", action='store_true')
    parser.add_argument("--config", type=str)
    parser.add_argument(
        "--message",
        type=str,
        help="commit message",
    )
    args = parser.parse_args()
    for id in args.ids:
        tok = edit(id, args.config)
        crawl(tok, args.config)
        if args.finalize:
            print(finalize(tok, args.config, args.message))
        else: 
            logger.info(f'please finalize the token {tok}')

if __name__ == "__main__":
    main()
