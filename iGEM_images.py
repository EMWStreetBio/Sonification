import sys
import os
import csv
import numpy as np
from math import pi, floor
from scipy.spatial.distance import euclidean
import cv2

# SAVE THRESHOLDED IMAGES INTO A DESTINATION FOLDER

def img_processing(imgfile, lthresh, uthresh, blur=True, erode=1, dilate=1, inv=True, show=False):
    ''' STEP-BY-STEP:
       1) Gaussian filtering;
       2) image grayscale + binarization;
       3) image erosion (OPTIONAL)
       4) image dilation;
    '''
    orig = cv2.imread(imgfile)
    if show: cv2.imshow("Original", orig)
    image = orig

    radius = 7
    kernel = cv2.getGaussianKernel(9, 3)
    if blur: image = cv2.GaussianBlur(orig,(radius,radius),0)
    if show: cv2.imshow("Blurred", image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if show: cv2.imshow("GrayScale", image)
    ret,image = cv2.threshold(image,uthresh,0,cv2.THRESH_TOZERO_INV)
    ret,image = cv2.threshold(image,lthresh,255,cv2.THRESH_BINARY_INV)

    if show: cv2.imshow("Binarized", image)

    kernel = np.ones((15,15),np.uint8)
    if (erode != 0):
        image = cv2.erode(image,kernel,iterations = erode)
        if show: cv2.imshow("Eroded", image)
    if (dilate != 0):
        image = cv2.dilate(image,kernel,iterations = dilate)
        if show: cv2.imshow("Dilated", image)
    # if inv: ret,image = cv2.threshold(image,lthresh,uthresh,cv2.THRESH_BINARY_INV)

    if show: cv2.waitKey(0)
    #final = erImage
    return image, orig

def find_centroids(img, orig, save=""): # finds dark spots only
    # centroidData = find centroids
    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()
    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 255
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 150
    # Filter by Circularity
    params.filterByCircularity = True
    params.minCircularity = 0.8
    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.87
    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.5

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)
    keypoints = detector.detect(img) #type: cv2.Keypoint

    # Create image with centroids
    if save != "":
        im_with_keypoints = cv2.drawKeypoints(orig, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        cv2.imwrite(save, im_with_keypoints)

    return keypoints

def main(flag, arg1, arg2, arg3, arg4, arg5):
    if flag == "-d": # directory of all images to be processed
        for image in os.listdir(input):
            if not image.startswith('.'):
                img, orig = img_processing(input+image, 83, 255, erode=0, dilate=0, blur=False)
                keypoints = find_centroids(img, orig, save="keypoints/"+image[:-4]+"_"+str(83)+"_"+str(255)+image[-4:])
                cv2.imwrite(dest+image[:-4]+"_"+str(83)+"_"+str(255)+image[-4:], img) # hard-coded
    elif flag == "-f": # .txt file listing paths of all images to be processed
        with open(input) as fileList:
            for file in fileList:
                print(file)
    elif flag == "-c": # .csv file listing paths of all images to be processed and their thresholding values
        # enter a blank for values
        with open(arg1, 'rU') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            teamdata = {}
            for row in reader:
                path = row[0]
                fullpath = arg2+path
                teamdata[path] = np.zeros(2)
                print(fullpath)
                img, orig = img_processing(fullpath, int(arg4), int(arg5), erode=0, dilate=0)
                keyimg, orig = img_processing(fullpath, int(arg4), int(arg5), erode=0, dilate=0, blur=True)
                keypoints = find_centroids(keyimg, orig, save="keypoints/"+path[:-4]+"_"+arg4+"_"+arg5+path[-4:])
                teamdata[path][0] = len(keypoints)
                teamdata[path][1] = (img==0).sum() # black pixels
                cv2.imwrite(arg3+path[:-4]+"_"+arg4+"_"+arg5+path[-4:], img) # hard-coded
        csvfile.close()
        with open("output_"+arg4+"_"+arg5+".csv", 'wb') as output:
            writer = csv.writer(output, delimiter=',')
            for image in teamdata:
                writer.writerow([image, teamdata[image][0], teamdata[image][1]])
        output.close()
    elif flag == '-file':
        img, orig = img_processing(input, 100, 105, erode=0, dilate=0, show=True)
    else:
        System.out.println("ERROR: attempted invalid flag\n")

if __name__=='__main__':
    # later use argumentParser
    if len(sys.argv)<=3:
        print "USAGE: python iGEM.py -d directory_containing_images/ dest_directory/"
        print "OR: python iGEM.py -c image_filepaths.csv inp_directory/ dest_directory/ lowthresh uppthresh"
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
