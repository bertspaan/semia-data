#!/usr/bin/env bash

# source ./env/bin/activate
source ./env/bin/activate.fish

TSNE=$1

FILENAME=${TSNE##*/}
FILENAME=${FILENAME%.*}

# Generate output filenames
GRID=output/grid/$FILENAME.csv
SHOTS=output/shots.csv
GRID_TO_SHOT=output/grid-to-shot/$FILENAME.json
PNG=output/images/$FILENAME.png
DZI=output/tiles/$FILENAME

# Create grid from t-SNE using RasterFairy
./tsne-to-grid.sh $TSNE $CSV

# Create grid-to-shot index
./grid-to-shot-index.js $GRID $SHOTS > $GRID_TO_SHOT

# Mount zipped thumbnails archive with fuse-zip
"fuse-zip" -r ./source/thumbnails/thumbnails128x256.zip ./source/thumbnails/126x256

# Create large PNG from grid using thumbnails
./grid-to-image.sh $CSV $PNG

# Create a Deep Zoom image from this PNG using vips
vips dzsave $PNG $DZI
