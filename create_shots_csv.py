# -*- coding: utf-8 -*-

import argparse
import os
import numpy as np
import h5py
import sys

# input
parser = argparse.ArgumentParser()
parser.add_argument('-in', dest="INPUT_FILE", default="source/attributes/openbeelden_colour.hdf5", help="Path to HDF5 file")
parser.add_argument('-out', dest="OUTPUT_FILE", default="output/shots.csv", help="Output CSV file")
a = parser.parse_args()

file = h5py.File(a.INPUT_FILE, 'r')
shot_ids = file['shotids'][:]

# TODO: WHY do all shot IDs appear as b'22989_1'???
strings = [str(shot_id).replace("b", "").replace("'", "").split('_') for shot_id in shot_ids]
np.savetxt(a.OUTPUT_FILE, strings, fmt="%s", delimiter=",")
