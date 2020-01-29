# Metadata

`metadata.zip` holds JSON files with metadata (title, description, year) for all videos from [Open Images](https://openbeelden.nl/).

To create `metadata.ndjson` from this ZIP file, unzip the file and then run

    ./json-files-to-ndjson.sh . > metadata.ndjson
