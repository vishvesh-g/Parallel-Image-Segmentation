import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from multiprocessing import Process
import image_slicer
from PIL import Image
import datetime


def get_concat_h_cut(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, min(im1.height, im2.height)))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_v_cut(im1, im2):
    dst = Image.new('RGB', (min(im1.width, im2.width), im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst

def merging():
    im1 = Image.open('q0.png')
    im2 = Image.open('q1.png')
    im3 = Image.open('q2.png')
    im4 = Image.open('q3.png')

    get_concat_h_cut(im1, im2).save('Top Half.png')
    print('Saving top half')

    get_concat_h_cut(im3, im4).save('Lower Half.png')
    print('Saving lower half')

    im1 = Image.open('Top Half.png')
    im2 = Image.open('Lower Half.png')
    print('Saving Final Image')

    get_concat_v_cut(im1, im2).save('Final Segmented.png')

def slicing():
    tiles = image_slicer.slice('im.png', 4, save=False)
    print('Slicing')
    image_slicer.save_tiles(tiles, prefix='slice', format='png')
    print('Saving')

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

    k = 2
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

def a1():
    image=[]    
    for i in range(1,3):
        for j in range(1,3):
            image.append(cv2.imread("slice_0"+str(i)+"_0"+str(j)+".png"))
            print("Segmenting - slice_0"+str(i)+"_0"+str(j)+".png")
    return image

if __name__=='__main__':
    a = datetime.datetime.now()
    
    slicing()
    image = a1()
    
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

    merging()
    
    b = datetime.datetime.now()

    print('Time Taken - '+str(b-a))



