#!/usr/bin/env bash

TSNE=$1

FILENAME=${TSNE##*/}
FILENAME=${FILENAME%.*}

# Generate output filenames
CSV=grid/$FILENAME.csv
PNG=images/$FILENAME.png
DZI=images/$FILENAME

# Create grid from t-SNE using RasterFairy
./tsne-to-grid.sh $TSNE $CSV

# Mount zipped thumbnails archive with fuse-zip
fuse-zip -r ./thumbnails/thumbnails128x256.zip ./thumbnails/126x256

# Create large PNG from grid using thumbnails
./grid-to-image.sh $CSV $PNG

# Create a Deep Zoom image from this PNG using vips
vips dzsave $PNG $DZI
