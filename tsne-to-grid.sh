#!/usr/bin/env bash

python3 tsne_to_grid.py \
  -in $1 \
  -out $2

# For example, with tsne_embedding_colour.npy:
# python3 tsne_to_grid.py \
#   -in "source/tsne/tsne_embedding_colour.npy" \
#   -out "output/grid/tsne_embedding_colour.csv"
