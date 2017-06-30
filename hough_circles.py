import cv2
import numpy as np
import pysynth as ps
from scipy.spatial.distance import euclidean
from matplotlib import pyplot as plt

image = cv2.imread("images/dj_jeff_resize.png")
# image = cv2.imread("BlobTest.jpg")
#cv2.imshow("Original", image)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("GrayScale", gray)

kernel = cv2.getGaussianKernel(9, 3)
gfImage = cv2.GaussianBlur(gray,(7, 7), 0)
#cv2.imshow("Gaussian", gfImage)

# PARAMETERS
dp=0.5
param1=200
param2=30
minRadius=30
maxRadius=50 #max diam = ~100 px

edges = cv2.Canny(gray, 100, param1, param2)
edges3 = cv2.cvtColor(edges,cv2.COLOR_GRAY2RGB)
output = edges3.copy()

plt.subplot(121),plt.imshow(image,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()

circles = cv2.HoughCircles(gfImage, cv2.HOUGH_GRADIENT, dp, minRadius*2, param1=param1, param2=param2,
minRadius=minRadius, maxRadius=maxRadius)

# ensure at least some circles were found
if circles is not None:
    print "Labels: dp, minDist, param1, param2, minRadius, maxRadius"
    print "Parameters:", dp, minRadius*2, param1, param2, minRadius, maxRadius
    print "Number of circles found:", circles.shape[1]
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")

    index = 0
    # loop over the (h, k) center coordinates and radius of the circles
    for (h, k, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (h, k), r, (0, 255, 0), 1)
        cv2.rectangle(output, (h - 5, k - 5), (h + 5, k + 5), (0, 128, 255), -1)

        white_sum = 0.0 #running total
        print "circle", index, "of", (h,k,r)
        for i in range((2*r)+1): # for entire span of circle, diameter
            x = i - r
            y = int(((r**2) - (x**2)) ** 0.5)
            #print "at", x+h, ",", y+k, "px value of", edges[x+h,y+k]
            if edges[x+h,y+k] == 255:
                white_sum += 1.0
            if y != 0:
                #print "at", x+h, ",", (-y)+k, "px value of", edges[x+h,(-y)+k]
                if edges[x+h,y+k] == 255: white_sum += 1.0
        print white_sum / ((4*r)+2)
        index += 1
    # show the output image
    cv2.imshow("output", np.hstack([edges3, output]))
    cv2.waitKey(0)

'''
maxRad = ((image.shape[0] + image.shape[1])/4)-250
circles = cv2.HoughCircles(final, cv2.HOUGH_GRADIENT,1,1,
                            param1=200,param2=35,minRadius=0,maxRadius=maxRad)
circles = np.uint16(np.around(circles))
print "circles", circles

for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(final,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(final,(i[0],i[1]),2,(0,0,255),3)

#cv2.namedWindow( "Hough Circle Transform Demo", CV_WINDOW_AUTOSIZE )
cv2.imshow( "Hough Circle Transform Demo", final)

cv2.waitKey(0)
'''
'''
kernel = np.ones((10,10),np.uint8)
erosion = cv2.erode(binarized,kernel,iterations = 1)
cv2.imshow("Eroded", erosion)

#kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(erosion,kernel,iterations = 1)
cv2.imshow("Dilated", dilation)

ret,dilationInv = cv2.threshold(dilation,127,255,cv2.THRESH_BINARY_INV)

final = dilationInv

# centroidData = find centroids
# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Change thresholds
params.minThreshold = 10;
params.maxThreshold = 255;

# Filter by Area.
params.filterByArea = True
params.minArea = 150

# Filter by Circularity
params.filterByCircularity = True
params.minCircularity = 0.4

# Filter by Convexity
params.filterByConvexity = True
params.minConvexity = 0.87

# Filter by Inertia
params.filterByInertia = True
params.minInertiaRatio = 0.5

# Create a detector with the parameters
detector = cv2.SimpleBlobDetector_create(params)
keypoints = detector.detect(final)
print "10", len(keypoints)

print "SEE OUTPUT10"
for point in keypoints:
    print "keypoint: " + str(point.pt)

kernel = np.ones((15,15),np.uint8)
erosion = cv2.erode(binarized,kernel,iterations = 1)
cv2.imshow("Eroded", erosion)

#kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(erosion,kernel,iterations = 1)
cv2.imshow("Dilated", dilation)

ret,dilationInv = cv2.threshold(dilation,127,255,cv2.THRESH_BINARY_INV)

final = dilationInv

detector = cv2.SimpleBlobDetector_create(params)
keypoints2 = detector.detect(final)
print "15", len(keypoints2)

total = np.append(keypoints, keypoints2)

print "SEE OUTPUT15_total"
for point in total:
    print "keypoint: " + str(point.pt)


# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(image, total, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show centroids
cv2.imshow("Keypoints", im_with_keypoints)

cv2.waitKey(0) # press any key while image is selected to escape

center = ((image.shape[0]/2.0), (image.shape[1]/2.0))
top_center = ((image.shape[0]/2.0), 0.0)
rad_dist = np.zeros(len(keypoints))
for i in range(len(keypoints)):
    rad_dist[i] = euclidean(keypoints[i].pt, center)
staff = zip(rad_dist, keypoints)
staff.sort()

for i in range(len(staff)):
    print staff[i][0], staff[i][1].pt
'''
