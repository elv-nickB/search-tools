import argparse
import os
import json
import tempfile
import time

def crawl(id: str, config: str, use_elv: bool=False, do_finalize: bool=False):
    client = 'elv' if use_elv else 'qfab_cli'
    tok = edit(client, id, config)
    print("write token", tok)
    with tempfile.NamedTemporaryFile() as fp:
        finished = False
        print('awaiting crawl')
        lro = search_update(client, tok, fp, config)
        print("lro handle", lro)
        while not finished:
            state = status(tok, lro, fp.name, config)
            finished = state == "terminated"
            time.sleep(15)
        
    if do_finalize:
        print(finalize(tok, config))
    else: 
        print('please finalize the token', tok)

def search_update(client: str, tok: str, temp_file: any, config: str) -> str:
    cmd = [client, 'content', 'bitcode', 'call', tok, 'search_update', '\"\"', temp_file.name, '--config', config, '--finalize=false', '--post']
    os.popen(' '.join(cmd)).read()
    lro = json.load(temp_file)
    return json.dumps(lro)

def edit(client: str, id: str, config: str) -> str:
    cmd = [client, 'content', 'edit', id, '--config', config]
    stream = os.popen(' '.join(cmd))
    tok = json.loads(stream.read())['q']['write_token']
    return tok

def status(tok: str, lro: str, f: str, config: str) -> str:
    cmd = ['qfab_cli', 'content', 'bitcode', 'call', tok, 'crawl_status', "'" + lro + "'", f, '--config', config, '--post']
    os.popen(' '.join(cmd)).read()
    with open(f, 'r') as ff:
        status = ff.read()
    print(status)
    return json.loads(status)["state"]

def finalize(tok: str, config: str) -> str:
    cmd = ['qfab_cli', 'content', 'finalize', tok, '--config', config]
    return os.popen(' '.join(cmd)).read()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id")
    parser.add_argument("--use_elv", action='store_true')
    parser.add_argument("--finalize", action='store_true')
    parser.add_argument("--config", type=str)
    args = parser.parse_args()
    crawl(args.id, args.config, use_elv=args.use_elv, do_finalize=args.finalize)

if __name__ == "__main__":
    main()
