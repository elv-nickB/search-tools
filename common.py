import os
import json

def edit(id: str, config: str) -> str:
    cmd = [get_client(), 'content', 'edit', id, '--config', config]
    print(' '.join(cmd))
    stream = os.popen(' '.join(cmd))
    tok = json.loads(stream.read())['q']['write_token']
    return tok

def merge_metadata(tok: str, data: str, config: str) -> str:
    cmd = [get_client(), 'content', 'meta', 'merge', tok, f"'{data}'", '--config', config]
    return os.popen(' '.join(cmd)).read()

def finalize(tok: str, config: str) -> str:
    cmd = [get_client(), 'content', 'finalize', tok, '--config', config]
    return os.popen(' '.join(cmd)).read()

def get_client() -> str:
    if os.getenv('FABRIC_CLIENT'):
        return os.getenv('FABRIC_CLIENT')
    else:
        return 'qfab_cli'
