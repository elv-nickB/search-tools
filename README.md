# Search tools

Command line tools for invoking search api. 

## Dependencies

- **Python**
- **elv/qfab_cli**
- **An elv/qfab_cli config file**

## Crawl

#### Params:
- **id** (`string`):
    - index content id to crawl
- **config** (`string`)
    - elv/qfab_cli config file containing hostname and private key
- **use_elv** (`bool`, optional)
    - set to true if your system uses `elv` 
    - Default: `false`
- **finalize** (`bool`, optional)
    - set to true to finalize the index after crawl is finished. Otherwise you will be given a write token afterwards to finalize on your own.  
    - Default: `false`

#### Example
`python crawl.py --id <content-id> --use_elv=true --config config.json --finalize`

## Search

#### Params:
- **id** (`string`):
    - index content id to search
- **config** (`string`)
    - elv/qfab_cli config file containing hostname and private key
- **use_elv** (`bool`, optional)
    - set to true if your system uses `elv` 
    - Default: `false`
- **query** (`string`)
    - query parameters 
    - **Example**: `'{"terms":"hello, "display_fields":"f_display_title", "semantic":true}'` 

#### Example
`python query.py --id <content-id> --config config.json --query '{"terms":"hello", "get_snippets":true}'`