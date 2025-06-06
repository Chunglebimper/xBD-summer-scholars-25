import rasterio
import numpy as np
import os
from PIL import Image

FILENAME_img = "/home/caiden/PycharmProjects/preproccessing/xBD-summer-scholars-25/reduced_size_preprocessing/composite_rgb5.png"  # test one image
# DIRECTORY = "../geotiffs/reduced_set"


my_list = []
reds = np.array(my_list)
greens = np.array(my_list)
blues = np.array(my_list)

##############################################
image = Image.open(FILENAME_img)  # BE SURE TO PLACE A NON-32 BIT IMAGE HERE SIZED TO 1024 x 1024
image_array = np.array(image)
image_array = np.transpose(image_array, (0, 1,))
#np.set_printoptions(threshold=np.inf, linewidth=1024)
rcount = 0
ccount = 0
count = 0
for band in image_array:
    count += 1
    for row in band:
        rcount += 1
        for col in row:
            ccount += 1
print(f'Number of bands: {count}')
print(f'Number of rows: {rcount}')
print(f'Number of cols: {ccount}')
#print(image_array)
1 / 0

"""
np.set_printoptions(threshold=np.inf, linewidth=1024)          
print(image_array)                                             


R, G, B = col
reds = np.append(reds, R)
greens = np.append(greens, G)
blues = np.append(blues, B)

R_mean = np.mean(reds)
G_mean = np.mean(greens)
B_mean = np.mean(blues)
print(R_mean, G_mean, B_mean)


for fname in os.listdir(DIRECTORY): # inside directory
    filepath = os.path.join(DIRECTORY, fname)
"""
