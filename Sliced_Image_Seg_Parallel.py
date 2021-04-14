import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from multiprocessing import Process


def ic(image,v):
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

    k = 5
    retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # convert data into 8-bit values
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    # reshape data into the original image dimensions
    segmented_image = segmented_data.reshape((image.shape))
    #print(segmented_image)
    plt.imshow(segmented_image)
    print('done')
    #plt.show()

    print('Saving - '+str(os.getpid()))
    cv2.imwrite('q'+str(v)+'.png', segmented_image)

def callThis():
    image=[]
    for i in range(1,3):
        for j in range(1,3):
            image.append(cv2.imread("slice_0"+str(i)+"_0"+str(j)+".png"))
            print("Segmenting - slice_0"+str(i)+"_0"+str(j)+".png")

    if __name__=='__main__':
        process1=Process(target=ic, args=([image[0],0]))
        process2=Process(target=ic, args=([image[1],1]))
        process3=Process(target=ic, args=([image[2],2]))
        process4=Process(target=ic, args=([image[3],3]))
        
        process1.start()
        process2.start()
        process3.start()
        process4.start()

        process1.join()
        process2.join()
        process3.join()
        process4.join()
