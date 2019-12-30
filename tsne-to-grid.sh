#!/usr/bin/env bash

python3 tsne_to_grid.py \
  -in $1 \
  -out $2

# For example, with tsne_embedding_colour.npy:
# python tsne_to_grid.py \
#   -in "tsne/tsne_embedding_colour.npy" \
#   -out "grid/tsne_embedding_colour.csv"
