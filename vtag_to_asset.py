import argparse
import json
from tqdm import tqdm

from common import merge_metadata, finalize, edit, get_metadata, content_info

def add_vtags(tok: str, config: str) -> None:
    # select video assets (indicated by presence of preview/default entry)
    asset_mdata = get_metadata(tok, '/assets', '/*/preview/default', config)
    if not asset_mdata:
        return
    new_mdata = {"assets": {}}
    for fname, data in tqdm(asset_mdata.items(), desc="Getting metadata from clip mezzanines"):
        # find hash of the clip mezz by inspecting the preview link
        clip_hash = data['preview']['default']['/'].split('/')[2]
        # get content id from hash
        content_id = content_info(clip_hash, config)['id']
        latest_hash = content_info(content_id, config)['hash']
        # get video tag metadata from the clip mezz
        try:
            tag_mdata = get_metadata(content_id, '/video_tags', '/', config)
            if 'metadata_tags' not in tag_mdata:
                print(f"{content_id} has no video tags")
                continue
            else:
                tag_mdata = tag_mdata['metadata_tags']
        except Exception as e:
            print(f"Failed to get metadata from {content_id}")
            raise e
        # convert the relative file link (to tags file) from the clip mezz to an absolute link
        for k, v in list(tag_mdata.items()):
            tag_mdata[k]["/"] = f"/qfab/{latest_hash}{v['/'][1:]}"
        tag_mdata = {"video_tags": {"metadata_tags": tag_mdata}}
        new_mdata["assets"][fname] = tag_mdata
    # merge the new metadata
    merge_metadata(tok, json.dumps(new_mdata), config)

def main():
    # read .txt containing list of contents and process each.
    with open(args.contents, 'r') as f:
        ids = [l.strip() for l in f.readlines()]
    for id in tqdm(ids, desc="Processing contents"):
        print("Processing", id)
        try:
            tok = edit(id, args.config)
            add_vtags(tok, args.config)
            if args.finalize:
                finalize(tok, args.config, args.message)
            else:
                print(f"please finalize {tok}")
        except Exception as e:
            print(f"Failed to process {id}")
            print(e)
            with open(args.failed, 'a') as f:
                f.write(f"{id}\n")
            continue
        # if success
        with open(args.finished, 'a') as f:
            f.write(f"{id}\n")
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--contents", required=True, type=str)
    parser.add_argument("--finalize", action='store_true')
    parser.add_argument("--message", type=str)
    parser.add_argument("--config", type=str)
    parser.add_argument("--failed",type=str)
    parser.add_argument("--finished",type=str)
    args = parser.parse_args()
    main()