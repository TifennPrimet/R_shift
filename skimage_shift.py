# coding: utf-8
"""Registration using optical flow
==================================

Demonstration of image registration using optical flow.

By definition, the optical flow is the vector field *(u, v)* verifying
*image1(x+u, y+v) = image0(x, y)*, where (image0, image1) is a couple of
consecutive 2D frames from a sequence. This vector field can then be
used for registration by image warping.

To display registration results, an RGB image is constructed by
assigning the result of the registration to the red channel and the
target image to the green and blue channels. A perfect registration
results in a gray level image while misregistred pixels appear colored
in the constructed RGB image.

"""
import numpy as np
from matplotlib import pyplot as plt
import cv2 as cv
from skimage.color import rgb2gray
from skimage.data import stereo_motorcycle, vortex
from skimage.transform import warp
from skimage.registration import optical_flow_tvl1, optical_flow_ilk
import scipy.signal
import os
print("Nous sommes ici",os.path.realpath(__file__))
PathMS1 = "C:/Users/tprimet/Documents/REPRISE/MS/MS1_unziped/20220519_134340/imgChannel_8.tiff"
PathMS2 = "C:/Users/tprimet/Documents/REPRISE/MS/MS2_unziped/20220519_134340/imgChannel_8.tiff"
# --- Load the sequence
image0 = cv.imread(PathMS1)#, cv.IMREAD_UNCHANGED)
image1 = cv.imread(PathMS2)  # , cv.IMREAD_UNCHANGED)
print(np.max(image1))
print(np.max(image0))
#image0 = np.floor(255*(image0/np.max(image0)))
#print(image0)
image1 = image1*2**4
image0 = image0*2**4
cv.imshow("MS1", image0)
cv.imshow("MS2", image1)
cv.waitKey(5)
print('images chargées leur tailles sont: \n MS1 : ', image0.shape,'\n MS2 : ', image1.shape)
print("correlat=", scipy.signal.correlate(image0, image1))
# image1.astype(np.uint8)
# image0.astype(np.uint8)
# --- Convert the images to gray level: color is not supported.
image0 = rgb2gray(image0)
image1 = rgb2gray(image1)

# --- Compute the optical flow
v, u = optical_flow_tvl1(image0, image1)

# --- Use the estimated optical flow for registration

nr, nc = image0.shape

row_coords, col_coords = np.meshgrid(np.arange(nr), np.arange(nc),
                                     indexing='ij')

image1_warp = warp(image1, np.array([row_coords + v, col_coords + u]),
                   mode='edge')

seq_im = np.zeros((nr, nc, 3))
seq_im[..., 0] = image1
seq_im[..., 1] = image0
seq_im[..., 2] = image0

# build an RGB image with the registered sequence
reg_im = np.zeros((nr, nc, 3))
reg_im[..., 0] = image1_warp
reg_im[..., 1] = image0
reg_im[..., 2] = image0

# build an RGB image with the registered sequence
target_im = np.zeros((nr, nc, 3))
target_im[..., 0] = image0
target_im[..., 1] = image0
target_im[..., 2] = image0

# --- Show the result

fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(5, 10))

ax0.imshow(seq_im)
ax0.set_title("Unregistered sequence")
ax0.set_axis_off()

ax1.imshow(reg_im)
ax1.set_title("Registered sequence")
ax1.set_axis_off()

ax2.imshow(target_im)
ax2.set_title("Target")
ax2.set_axis_off()

fig.tight_layout()


methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR', 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
cv.imshow("image_warp", image1_warp)
cv.imshow("target_im", target_im)
cv.waitKey(0)
plt.show()
print(image0)
for meth in methods :
    method = eval(meth)
    print('reg_im  = ', reg_im.shape, type(reg_im), "\n target_im = ", target_im.shape, type(target_im))
    res = cv.matchTemplate(target_im, reg_im,  method)