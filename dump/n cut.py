import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import builtins
from skimage import color
 
def compute_pdfs(imfile, imfile_scrib):

     rgb = mpimg.imread(imfile)[:,:,:3]
     yuv = color.rgb2yiq(rgb)
     rgb_s = mpimg.imread(imfile_scrib)[:,:,:3]
     yuv_s = color.rgb2yiq(rgb_s)

     scribbles = find_marked_locations(rgb, rgb_s)
     imageo = np.zeros(yuv.shape)

     comps = defaultdict(lambda:np.array([]).reshape(0,3))
     for (i, j) in scribbles:
          imageo[i,j,:] = rgbs[i,j,:]

          comps[tuple(imageo[i,j,:])] = np.vstack([comps[tuple(imageo[i,j,:])], yuv[i,j,:]])
          mu, Sigma = {}, {}

     for c in comps:
          mu[c] = np.mean(comps[c], axis=0)
          Sigma[c] = np.cov(comps[c].T)
     return (mu, Sigma)

if __name__=='__main__':

     print (compute_pdfs('im.png','im (2).png'))
    
     
