#!/usr/bin/env bash

python3 grid_to_image.py \
  -in $1 \
  -tile "128x128" \
  -grid "321x322" \
  -out $2

# For example, with tsne_embedding_colour.csv:
# python3 grid_to_image.py \
#   -in "output/grid/tsne_embedding_colour.csv" \
#   -tile "128x128" \
#   -grid "321x322" \
#   -out "output/images/tsne_embedding_colour.png"
