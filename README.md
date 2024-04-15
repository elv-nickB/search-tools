# Search tools

Command line tools for helping automate search index management and running search.

## Dependencies

- **Python**
- **elv/qfab_cli**
- **An elv/qfab_cli config file**

## Setup
1. `pip install .`
2. `export FABRIC_CLIENT=elv` (if using mac)

## Crawl

#### Params:
- **id** (`string`):
    - index content id to crawl
- **config** (`string`)
    - elv/qfab_cli config file containing hostname and private key
- **finalize** (`bool`, optional)
    - set to true to finalize the index after crawl is finished. Otherwise you will be given a write token afterwards to finalize on your own.  
    - Default: `false`

#### Example
`python crawl.py --id <content-id> --config config.json --finalize`

## Search

#### Params:
- **id** (`string`):
    - index content id to search
- **config** (`string`)
    - elv/qfab_cli config file containing hostname and private key
- **query** (`string`)
    - query parameters 
    - **Example**: `'{"terms":"hello, "display_fields":"f_display_title", "semantic":true}'` 

#### Example
`python query.py --id <content-id> --config config.json --query '{"terms":"hello", "get_snippets":true}'`