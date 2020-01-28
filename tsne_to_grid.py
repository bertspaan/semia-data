# -*- coding: utf-8 -*-

import argparse
import math
import numpy as np
import os
from pprint import pprint
import rasterfairy
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="input/tsne/tsne_embedding_all.npy", help="Input data file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/grid/tsne_embedding_all.csv", help="Output data file")
a = parser.parse_args()

model = np.load(a.INPUT_FILE)
count = len(model)

print("Determining grid assignment...")

gridAssignment = rasterfairy.transformPointCloud2D(model)
grid, gridShape = gridAssignment
print("Resulting shape:")
print(gridShape)

print("Saving grid assignment file %s..." % a.OUTPUT_FILE)
np.savetxt(a.OUTPUT_FILE, grid, delimiter=",")
print("Done.")
