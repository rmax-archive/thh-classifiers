# -*- coding: utf-8 -*-
from skimage.io import imread
from skimage.color import rgb2gray, hsv2rgb
import matplotlib.pyplot as plt
from skimage import img_as_float
from skimage import measure
from skimage.feature import canny
import numpy as np


img_path = "/media/sf_temp/yahoo.jpg"

img_color = imread(img_path, as_grey=False)
# print img_color
# print img_color[1000][1000][0] * 0.7
# img_data = img_as_float(img_color)
# print img_data.shape
# img_data = img_data[220:300, 220:320]
# print(img_data)
img_grey = rgb2gray((img_color))
# edges = canny( img_grey / 255.)
# from scipy import ndimage as ndi
# fill_parts = ndi.binary_fill_holes(edges)
# print img_grey
# print img_grey.shape
# img_grey = img_color
noisy = img_grey + 0.8 * img_grey.std() * np.random.random(img_grey.shape)
noisy = np.clip(noisy, 0, 1)
img_grey = noisy
contours = measure.find_contours(img_grey, 0.9)

# fig = plt.figure(figsize=(7, 7))
fig = plt.figure()
ax = fig.add_subplot(111)
# ax.imshow(fill_parts, cmap=plt.cm.gray)
ax.imshow(img_grey, cmap=plt.cm.gray)
for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
plt.show()

