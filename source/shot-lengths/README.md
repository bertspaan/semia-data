# Shot lengths

Start and end times of every shot in all videos.

To create `shot-lengths.ndjson` from `shot-lengths.json` use [jq](https://stedolan.github.io/jq/):

    cat shot-lengths.json | jq '.[]' -r -M -c > shot-lengths.ndjson
