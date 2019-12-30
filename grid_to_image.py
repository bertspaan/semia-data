# -*- coding: utf-8 -*-

import argparse
import glob
import numpy as np
from PIL import Image
from pprint import pprint
import random
import sys

def fillImage(img, w, h):
    vw, vh = img.size
    if vw == w and vh == h:
        return img

    # first, resize video
    ratio = 1.0 * w / h
    vratio = 1.0 * vw / vh
    newW = w
    newH = h
    if vratio > ratio:
        newW = h * vratio
    else:
        newH = w / vratio
    # Lanczos = good for downsizing
    resized = img.resize((int(round(newW)), int(round(newH))), resample=Image.LANCZOS)

    # and then crop
    x = 0
    y = 0
    if vratio > ratio:
        x = int(round((newW - w) * 0.5))
    else:
        y = int(round((newH - h) * 0.5))
    x1 = x + w
    y1 = y + h
    cropped = resized.crop((x, y, x1, y1))

    return cropped

def printProgress(step, total):
    sys.stdout.write('\r')
    sys.stdout.write("%s%%" % round(1.0*step/total*100,2))
    sys.stdout.flush()

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="grid/tsne_embedding_all.csv", help="Input CSV file with grid assignments")
parser.add_argument('-images', dest="IMAGE_PATH", default="thumbnails/126x256/thumbnails128x256", help="Image path")
parser.add_argument('-shots', dest="SHOTS_FILE", default="grid/shots.csv", help="Input CSV file shot IDs")
parser.add_argument('-tile', dest="TILE_SIZE", default="128x128", help="Tile size in pixels")
parser.add_argument('-grid', dest="GRID_SIZE", default="321x322", help="Grid size in cols x rows")
parser.add_argument('-out', dest="OUTPUT_FILE", default="images/tsne_embedding_all.png", help="File for output")
a = parser.parse_args()

shots = np.loadtxt(a.SHOTS_FILE, delimiter=",", dtype='str')
grid = np.loadtxt(a.INPUT_FILE, delimiter=",")

tileW, tileH = tuple([int(t) for t in a.TILE_SIZE.split("x")])
gridW, gridH = tuple([int(t) for t in a.GRID_SIZE.split("x")])
imgW, imgH = (gridW * tileW, gridH * tileH)
fileCount = len(grid)

filename = lambda path, video_id, shot_id: path + "/" + video_id + "/" + video_id + "_" + shot_id + ".png"

baseImage = Image.new('RGB', (imgW, imgH), (0,0,0))
i = 0
for xy, shot in zip(grid, shots):
    video_id, shot_id = tuple(shot)
    col, row = tuple(xy)
    x = int(round(col * tileW))
    y = int(round(row * tileH))

    fn = filename(a.IMAGE_PATH, video_id, shot_id)
    im = Image.open(fn)
    im = fillImage(im, tileW, tileH)
    baseImage.paste(im, (x, y))
    printProgress(i + 1, fileCount)
    i += 1

print("Saving image...")
baseImage.save(a.OUTPUT_FILE)
print("Created %s" % a.OUTPUT_FILE)
