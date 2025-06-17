# import libraries
import cv2
import os
import matplotlib
from matplotlib import pyplot as plt
from os.path import exists
import numpy as np
from PIL import Image
from matplotlib import cm
from pylab import *
"""
a = b = count_0 = count_1 = count_2 = count_3 = count_4 = 0


def conv_to_rgb(data):
	data = data.flatten()
	norm = matplotlib.colors.Normalize(vmin=min(data), vmax=max(data), clip=True)
	mapper = cm.ScalarMappable(norm=norm, cmap=cm.Greys_r)
	node_color = [(r, g, b) for r, g, b, a in mapper.to_rgba(data)]

# for file_number in [0,1,2,3,4,7,8,9,11,13,15,17,18,19,20,21,23,24,27,29,30,31,32,33,34,35,37,39,40,41,42,43,44,46,47,48,49,52,53,55,57,59,64,66,67,68,70,72,74,75,78,79,82,83,84,85,86,87,88,89,92,93,96,98,100,101,
# 102,103,104,105,107,108,110,111,112,114,115,118,119,120,122,125,126,127,128,129,132,136,138,140,141,142,143,144,146,148,150,151,152,153,154,155,158,159,160,164,166,168,171,172,173,176,177,179,181,182,184,185,186,191,192]:

# 0,1,2,3,4,7,8,9,11,13,15,17,18,19,20,21,23,24,27,29,30,31,32,33,34,35,37,39,40,41,42,43,44,46,47,48,49,52,53,55,57,59,64,66,67,68,70,72,74,75,78,79,82,83,84,85,86,87,88,89,92,93,96,98,
for file_number in [0, 1, 2, 3, 4, 7, 8, 9, 11, 13, 15, 17, 18, 19, 20, 21, 23, 24, 27, 29, 30, 31, 32, 33, 34, 35, 37,
                    39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 52, 53, 55, 57, 59, 64, 66, 67, 68, 70, 72, 74, 75, 78, 79,
                    82, 83, 84, 85, 86, 87, 88, 89, 92, 93, 96, 98, 100, 101, 102, 103, 104, 105, 107, 108, 110, 111,
                    112, 114, 115, 118, 119, 120, 122, 125, 126, 127, 128, 129, 132, 136, 138, 140, 141, 142, 143, 144,
                    146, 148, 150, 151, 152, 153, 154, 155, 158, 159, 160, 164, 166, 168, 171, 172, 173, 176, 177, 179,
                    181, 182, 184, 185, 186, 191, 192]:

    if file_number < 10:
        file_number_o = '0000000' + str(file_number)
    elif (file_number > 10 and file_number < 100):
        file_number_o = '000000' + str(file_number)
    else:
        file_number_o = '00000' + str(file_number)

    print("file number is :" + str(file_number_o))

    if os.path.exists('../train/img_pre/mexico-earthquake_%s_pre_disaster.png' % file_number_o):
        # print("file number is :")
        # print(file_number)
        # reading images
        # Image1 = plt.imread('../train/img_pre/mexico-earthquake_%s_pre_disaster.png'%file_number_o)
        # Image2 = plt.imread('../train/img_post/mexico-earthquake_%s_post_disaster.png'%file_number_o)
        # Image3 = plt.imread('../train/gt_pre/mexico-earthquake_%s_pre_disaster_target.png'%file_number_o)
        # Image3 = (Image3 - 0)*255
        Image4 = plt.imread('../train/gt_post/mexico-earthquake_%s_post_disaster_target.png' % file_number_o)
        Image4 = (Image4 - 0) * 255
    Image4.flatten()
    print(Image4)
    count_0 = (Image4 == 0).sum()
    count_1 = (Image4 == 1).sum()
    count_2 = (Image4 == 2).sum()
    count_3 = (Image4 == 3).sum()
    count_4 = (Image4 == 4).sum()

    a = count_0 + count_1 + a
    b = count_2 + count_3 + count_4 + b

    print(a)
    print(b)

print(b / a)

# create figure
fig = plt.figure(figsize=(20, 15))
fig.suptitle("earthquake disaster before-after pair " + str(file_number_o))
fig.text(0, 1, '0: background,1:no damage 2: minor damage,3: major damage, 4:destroyed')

# setting values to rows and column variables.
rows = 2
columns = 2

# Adds a subplot at the 1st position
fig.add_subplot(rows, columns, 1)

# showing image
Image1 = Image1
plt.imshow(Image1)
plt.axis('off')
plt.title("pre_earthquake")

# Adds a subplot at the 2nd position
fig.add_subplot(rows, columns, 2)

# showing image
plt.imshow(Image2)
plt.axis('off')
plt.title("post_earthquake")

# Adds a subplot at the 3rd position
fig.add_subplot(rows, columns, 3)

# showing image
plt.imshow(Image3)
plt.colorbar()
plt.axis('off')
plt.title("pre_disaster,'0: background,1:no damage 2: minor damage,3: major damage, 4:destroyed'")

# Adds a subplot at the 4th position
fig.add_subplot(rows, columns, 4)

# showing image
plt.imshow(Image4)
plt.colorbar()
plt.axis('off')
plt.title("post_disaster, '0: background,1:no damage 2: minor damage,3: major damage, 4:destroyed'")

plt.show()

# else:
# file_number = file_number + 1
"""

def tiff_from(tiff_path):
    """ Converts raw tif image from 3 band image to each individual band as well as composite
    Modified from ChatGPT*
    """
    #np.set_printoptions(threshold=np.inf, linewidth=10)
    try:
        image_array = np.array(image)

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


        # begin processing
        # image_array = np.transpose(image_array, (1, 2, 0))
        #Above line changes order of bands to be read by
        # shape:       (bands, height, width)
        # Transpose to (height, width, bands)
        """
        When you load a multi-band image with rasterio.read(), the shape of the data is:
            (bands, height, width)
        => (3, 1024, 1024)  # for an RGB image
        However, most image libraries (like Pillow or OpenCV) expect images in the shape:
            (height, width, channels)
        => (1024, 1024, 3)
        """

        #print(f'Before normalizing: {image_array}')
        if image_array.dtype != np.uint8:           #changes all values to something more readable in RGB (aka normalized)
            print("normalizing...")
            image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
        #print(f'After normalizing: {image_array}')
        # saves full composite image
        composite_image = Image.fromarray(image_array, mode='L')
        composite_image.save('./processed/BWtest.tif')
        print("Saved: composite_rgb.tif")
        # saves greyscale images
        #band_names = ['red', 'green', 'blue']
        #for i, name in enumerate(band_names):
            #band = image_array[:, :, i]  # isolate band as grayscale
            #Image.fromarray(band, mode='L').save(f'./processed/band_{name}_grayscale.tif')
            #print(f"Saved: band_{name}_grayscale.tif")

    except FileNotFoundError:
        print(f"Error: File not found at {tiff_path}")
    except Exception as e:
        print(f"An error occurred: {e}")














