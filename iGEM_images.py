import sys
import os
import csv
import numpy as np
from math import pi, floor
from scipy.spatial.distance import euclidean
import cv2
from midiutil.MidiFile import MIDIFile

# SAVE THRESHOLDED IMAGES INTO A DESTINATION FOLDER

def img_processing(imgfile, lthresh, uthresh, erode=1, dilate=1, inv=True, show=False):
    ''' STEP-BY-STEP:
       1) Gaussian filtering;
       2) image grayscale + binarization;
       3) image erosion (OPTIONAL)
       4) image dilation;
    '''
    orig = cv2.imread(imgfile)
    if show: cv2.imshow("Original", orig)

    radius = 7
    kernel = cv2.getGaussianKernel(9, 3)
    image = cv2.GaussianBlur(orig,(radius,radius),0)
    if show: cv2.imshow("Blurred", image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if show: cv2.imshow("GrayScale", image)
    ret,image = cv2.threshold(image,lthresh,uthresh,cv2.THRESH_BINARY) # unnessary? should just be INV?
    if show: cv2.imshow("Binarized", image)

    kernel = np.ones((15,15),np.uint8)
    if (erode != 0):
        image = cv2.erode(image,kernel,iterations = erode)
        if show: cv2.imshow("Eroded", image)
    if (dilate != 0):
        image = cv2.dilate(image,kernel,iterations = dilate)
        if show: cv2.imshow("Dilated", image)
    if inv: ret,image = cv2.threshold(image,lthresh,uthresh,cv2.THRESH_BINARY_INV)

    if show: cv2.waitKey(0)
    #final = erImage
    return image, orig

def main(flag, input, dest):
    if flag == "-d": # directory of all images to be processed
        for image in os.listdir(input):
            if not image.startswith('.'):
                img, orig = img_processing(input+image, 83, 255, erode=0, dilate=0)
                cv2.imwrite(dest+image[:-4]+"_"+str(83)+"_"+str(255)+image[-4:], img) # hard-coded
    elif flag == "-f": # .txt file listing paths of all images to be processed
        with open(input) as fileList:
            for file in fileList:
                print(file)
    elif flag == "-c": # .csv file listing paths of all images to be processed and their thresholding values
        with open('eggs.csv', 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                print ', '.join(row)
                # TO BE CODED
    else:
        System.out.println("ERROR: attempted invalid flag (only '-f' and '-d')\n")

if __name__=='__main__':
    # add arguments for image_location for testing... currently in main()
    if len(sys.argv)<=3:
        print "USAGE: python iGEM.py -d directory_containing_images/ dest_directory/\n"
        print "OR: python iGEM.py -f image_filepaths.txt dest_directory/"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
