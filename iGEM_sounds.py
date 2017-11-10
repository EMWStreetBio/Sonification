import sys
import os
import csv
import numpy as np
from math import pi, floor
from scipy.spatial.distance import euclidean
from midiutil.MidiFile import MIDIFile

def main(flag, input, dest):

if __name__=='__main__':
    # add arguments for image_location for testing... currently in main()
    if len(sys.argv)<=3:
        print "USAGE: python iGEM.py -d directory_containing_images/ dest_directory/\n"
        print "OR: python iGEM.py -f image_filepaths.txt dest_directory/"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
