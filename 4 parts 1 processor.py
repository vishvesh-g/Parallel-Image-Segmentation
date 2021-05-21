import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
import image_slicer
import datetime

a = datetime.datetime.now()

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
    k = 7
    retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # convert data into 8-bit values
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]

    # reshape data into the original image dimensions
    segmented_image = segmented_data.reshape((image.shape))
    #print(segmented_image)
    plt.imshow(segmented_image)
    #plt.show()

    cv2.imwrite('q'+str(v)+'.png', segmented_image)
        
v=0
for i in range(1,3):
    for j in range(1,3): 
        image = cv2.imread("slice_0"+str(i)+"_0"+str(j)+".png")
        print("Segmenting - slice_0"+str(i)+"_0"+str(j)+".png")
        ic(image,v)
        v+=1



from PIL import Image

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

b = datetime.datetime.now()

print('Time Taken - '+str(b-a))
