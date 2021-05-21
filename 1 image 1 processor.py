import cv2
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import datetime

a = datetime.datetime.now()

image = cv2.imread('im.png')

print('Segmenting')

image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# Reshaping the image into a 2D array of pixels and 3 color values (RGB)
pixel_vals = image.reshape((-1,3))

# Convert to float type
pixel_vals = np.float32(pixel_vals)
pixel_vals
#the below line of code defines the criteria for the algorithm to stop running,
#which will happen is 100 iterations are run or the epsilon (which is the required accuracy)
#becomes 85%
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 1000, 0.8)

# then perform k-means clustering wit h number of clusters defined as 3
#also random centres are initally chosed for k-means clustering
k = 2
retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# convert data into 8-bit values
centers = np.uint8(centers)
segmented_data = centers[labels.flatten()]

# reshape data into the original image dimensions
segmented_image = segmented_data.reshape((image.shape))

#plt.imshow(segmented_image)

print('Done')

#plt.show()

print('Saving')

cv2.imwrite('One Go segmentation ('+str(k)+' Segments).png',segmented_image)

b = datetime.datetime.now()

print('Time Taken - '+str(b-a))


