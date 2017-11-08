import sys
import os
import numpy as np
from math import pi, floor
from scipy.spatial.distance import euclidean
import cv2
from midiutil.MidiFile import MIDIFile


def main(flag, input, dest):
    if flag == "-d": # directory of all images to be processed
        for image in os.listdir(input):
            if not image.startswith('.'):
                print(image)
    elif flag == "-f": # .txt file listing paths of all images to be processed
        with open(input) as fileList:
            for file in fileList:
                print(file)
    elif flag == "-c": # .csv file listing paths of all images to be processed and their thresholding values
    else:
        System.out.println("ERROR: attempted invalid flag (only '-f' and '-d')\n")

if __name__=='__main__':
    # add arguments for image_location for testing... currently in main()
    if len(sys.argv)<=3:
        print "USAGE: python iGEM.py -d directory_containing_images/ dest_directory/\n"
        print "OR: python iGEM.py -f image_filepaths.txt dest_directory/"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
