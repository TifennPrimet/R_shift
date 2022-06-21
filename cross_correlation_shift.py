from dataclasses import replace
import numpy as np
import matplotlib.pyplot as plt
from skimage import data
from skimage.registration import phase_cross_correlation
from skimage.registration._phase_cross_correlation import _upsampled_dft
from scipy.ndimage import fourier_shift
from skimage.transform import warp

import cv2 as cv
def cross_correlation_shift(Path, PathBis):
   
    # --- Load the sequence
    image = cv.imread(Path, cv.IMREAD_UNCHANGED)
    offset_image = cv.imread(PathBis , cv.IMREAD_UNCHANGED)
    
    # pixel precision first
    shift, error, diffphase = phase_cross_correlation(image, offset_image, space ="real")
    print(f'Detected pixel offset (y, x): {shift}')
    dt = 0.01
    dx = np.arange(shift[0]-2 , shift[0]+2+dt , dt)
    dy = np.arange(shift[1]-2 , shift[1]+2+dt , dt)
    resX = np.zeros(dx.shape)
    resY = np.zeros(dy.shape)


    for i in range (dx.shape[0] ):
      if dx[i]!=0 :
            offset_image_copy = fourier_shift(np.fft.fftn(offset_image),( dx[i] , 1))
            offset_image_copy = np.fft.ifftn(offset_image_copy)
            shift, error, diffphase = phase_cross_correlation(image, offset_image_copy , upsample_factor=20)
            resX[i] = shift[0]
            
   
    for j in range(dy.shape[0]) :
      if dy[j]!=0 :
          offset_image_copy = fourier_shift(np.fft.fftn(offset_image), (1 , dy[j]))
          offset_image_copy = np.fft.ifftn(offset_image_copy)
          shift, error, diffphase = phase_cross_correlation(image, offset_image_copy,upsample_factor=20)
          resY[j] = shift[1]
          
    fig = plt.figure(figsize=(8, 2))
    ax1 = plt.subplot(1, 2,1)
    ax2 = plt.subplot(1, 2,2)
    
    ax1.plot(dx, np.abs(resX))
    ax1.set_title('X')

    ax2.plot(dy, np.abs(resY))
    ax2.set_title('Y')      

    shiftx = dx[np.where(resX == np.min(np.abs(resX)))[0][0]]
    shifty = dy[np.where(resY == np.min(np.abs(resY)))[0][0]]
    
    print("shift optimal (x, y) =",(shiftx, shifty))
    # offset_image_copy = fourier_shift(np.fft.fftn(offset_image), (shiftx , shifty))
    # offset_image_copy = np.fft.ifftn(offset_image_copy)
    # print("shift trouvé" ,phase_cross_correlation(image, offset_image_copy,upsample_factor=20)[0])
    # res = offset_image.real 
    matrix = np.array([[1,0,shiftx], [0,1,shifty]])
    nr, nc = offset_image.shape

    row_coords, col_coords = np.meshgrid(np.arange(nr), np.arange(nc), indexing='ij')
    warped_image = warp(offset_image, np.array([row_coords - shiftx, col_coords - shifty]), mode='edge')
    print("warped_image",warped_image)
    fig2 = plt.figure(figsize=(8, 2))
    ax12 = plt.subplot(1, 3,1)
    ax22 = plt.subplot(1, 3,2)
    ax32 = plt.subplot(1, 3,3)
    ax12.imshow(offset_image)
    ax12.set_title('image a decaler')
    ax22.imshow(warped_image)
    ax22.set_title('image décaléé')
    ax32.imshow(image)
    ax32.set_title('goal')   

    
    plt.show()
    return warped_image


image = "C:/Users/tprimet/Documents/REPRISE/MS/MS1_unziped/20220519_134340/imgChannel_8.tiff"

offset_image =  "C:/Users/tprimet/Documents/REPRISE/MS/MS2_unziped/20220519_134340/imgChannel_1.tiff"
cross_correlation_shift(image, offset_image)