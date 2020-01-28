# The Sensory Moving Image Archive: Data, scripts and tools

This repository contains scripts and data needed to run the Visualization and exploration tool of the Sensory Moving Image Archive.

__[Explore the Sensory Moving Image Archive](https://bertspaan.nl/semia/)!__

[![](https://github.com/bertspaan/semia/raw/master/public/semia.jpg)](https://bertspaan.nl/semia/)

This project depends on two other repositories:

- [`semia`](https://github.com/bertspaan/semia): Visualization and exploration tool, made with Vue;
- [`semia-api`](https://github.com/bertspaan/semia-api): JSON API for metadata and search, running on [Glitch](https://glitch.com/edit/#!/semia-api).

For more information about the project, see the [About page](https://bertspaan.nl/semia/#/about).

## Data, scripts and tools

The Visualization and exploration tool and its API need the following three things to work:

1. A [Deep Zoom](https://en.wikipedia.org/wiki/Deep_Zoom) image grid of all 103,273 shots grouped by color, based on [t-SNE](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding) data provided by the University of Amsterdam.
2. A grid index which holds video and shot IDs for each shot in each row and column in the grid. This data is needed so the app knows what video to load when the user clicks on an thumbnail in the image grid.
3. A JSON file with metadata and similarity data for each movie. This data is shown when the user is watching a movie and it's used by the search index running on [Glitch](https://glitch.com/edit/#!/semia-api).

This repository uses both Node.js and Python.

## Image grid

This project was inspired by Brian Foo's [visualization of 13,212 digitized images from the American Museum of Natural History](https://amnh-sciviz.github.io/image-collection/index.html). The scripts `tsne_to_grid.py` and `grid_to_image.py` in this repository where taken from the [source code of this project](https://github.com/amnh-sciviz/image-collection).

First, create a virtual environment:

    python3 -m venv env

Then, activate this virtual environment:

    source ./env/bin/activate

Or, if you're using [fish](http://fishshell.com/):

    source ./env/bin/activate.fish

Install dependencies:

    pip install numpy h5py Pillow

And install the Python 3 version of [RasterFairy](https://github.com/Quasimondo/RasterFairy) (included in this repository):

    cd RasterFairy
    pip install .
    cd ..

Now, we can run [`tsne_to_grid.py`](tsne_to_grid.py) which uses RasterFairy to turn t-SNE data into a rectangular grid:

    python3 tsne_to_grid.py \
        -in "source/tsne/tsne_embedding_colour.npy" \
        -out "output/grid/tsne_embedding_colour.csv"

The outcome of this first step is [`tsne_embedding_colour.csv`](output/grid/tsne_embedding_colour.csv), a CSV file that contains video and shot IDs in this rectangular grid.

To turn this into an image grid, we first need the thumbnails of each shot of each move. See the README in the [`source/thumbnails`](source/thumbnails) directory on how to download these.

After downloading the ZIP file with all thumbnails, we can unzip them or use [fuse-zip](https://bitbucket.org/agalanin/fuse-zip/wiki/Home) to mount this ZIP archive as a file system.

Install fuse-zip (on MacOS):

    brew install vips

Mount the thumbnails archive with 128 x 256 pixel images:

    cd source/thumbnails
    fuse-zip -r thumbnails128x256.zip ./126x256

Now, run [`grid_to_image.py`](grid_to_image.py) to turn this CSV file into a large PNG (2.32 GB):

    python3 grid_to_image.py \
        -in "output/grid/tsne_embedding_colour.csv" \
        -tile "128x128" \
        -grid "321x322" \
        -out "output/images/tsne_embedding_colour.png"

This PNG file is much to large to display in a web application. With [vips](https://github.com/libvips/libvips), we can turn this PNG into [Deep Zoom](https://en.wikipedia.org/wiki/Deep_Zoom) tiles.

Install vips (on MacOS):

    brew install vips

Then, run vips:

    vips dzsave output/images/tsne_embedding_colour.png output/tiles/tsne_embedding_colour.dzi

## Grid index

To create the grid-to-shot index, we need the CSV file produced by `tsne_to_grid.py` in the previous step. We also need a way to connect the array indices in the CSV file to video and shot IDs. We'll do this with the file [`shots.csv`](output/shots.csv), created by running the following command:

    python3 create_shots_csv.py \
        -in "source/attributes/openbeelden_colour.hdf5" \
        -out "output/shots.csv"

THe Node.js script [`grid-to-shot-index.js`](grid-to-shot-index.js) created a two-dimensional JSON array that can be used to find the right video and shot ID for a certain row/column in the image grid. First, install its dependencies:

    npm install

Then, run it on the CSV file `tsne_embedding_colour.csv`:

    ./grid-to-shot-index.js \
        output/grid/tsne_embedding_colour.csv \
        output/shots.csv > tsne_embedding_colour.json
