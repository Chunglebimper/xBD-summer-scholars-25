from skimage import io
#import tkinter as tk
#import split_image
import skimage
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
import cv2
import numpy as np
import sys
import tifffile as tiff
from PIL import Image
import os
import tkinter as tk


def display(PATH):
    """
    figure is NOT raw and is increased in size for unknown reason
    :param PATH: import path of data to be processed
    :return: none, figs are saved according to the plt.savefig name
    """
    img = io.imread(PATH)  # read the image stack
    plt.imshow(img, alpha=1, interpolation_stage='rgba', filternorm=False, resample=False)
    plt.tight_layout()
    # show the image
    plt.axis('off')
    plt.savefig('./processed/output.tif', transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.0)   # save the image

def tiffManage(PATH):
    """
    figure is resized to compensate for expansion in display();
    WARNING: MAY BE REMOVING DATA
    :param PATH: import path of data to be processed
    :return: none, image is saved as according to image.save
    """
    img = Image.open(PATH)
    print(img.size)
    out = img.resize((1024,1024))
    out.save('./processed/resized.tif')


def TweakedDisplay(PATH):
    """
    trying to keep RGBA rather than RGB; MODIFIED FROM matplot.lib website
    :param PATH: import path of data to be processed
    :return: none, figs are saved according to the plt.savefig name
    """


    img = io.imread(PATH)  # read the image stack
    image_array = np.array(img)
    np.set_printoptions(threshold=np.inf, linewidth=120)
    print(image_array)
    #np.savetxt("./processed/out.csv", image_array, delimiter=",", fmt="%d")

    # Example 3D array if you don't have one:
    # image_array = np.random.randint(0, 2, size=(30, 30, 30))  # binary volume
    # image_array = np.random.rand(30, 30, 30) > 0.95  # sparse volume

    # Ensure it's a 3D numpy array
    assert image_array.ndim == 3, "image_array must be 3D (depth, height, width)"

    # Get coordinates of non-zero voxels
    z, y, x = np.nonzero(image_array)  # Note the order (z, y, x)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    # Normalize color based on intensity, if needed
    values = image_array[z, y, x]
    colors = values / values.max() if values.max() > 0 else values

    # Scatter plot of non-zero voxels
    scatter = ax.scatter(x, y, z, c=colors, cmap='hsv', marker='o')

    # Add colorbar for intensity if useful
    fig.colorbar(scatter, ax=ax, label='Intensity')

    # Label axes
    ax.set_xlabel('X (width)')
    ax.set_ylabel('Y (height)')
    ax.set_zlabel('Z (depth)')

    ax.set_title('3D Visualization of image_array')
    ax.view_init(elev=30, azim=45)

    plt.savefig("./processed/3Darray.png")
    plt.show()



#############################################################################################################
PATHS = ['processed', 'processed/splits']
for PATH in PATHS:
    os.makedirs(PATH, exist_ok=True)        #automatically handles directory creation

"""CONSTANTS"""
GEO_PATH = 'geotiffs/reduced_set/mexico-earthquake_00000049_post_disaster.tif'
#GEO_PATH = "geotiffs/tier3/images/joplin-tornado_00000000_post_disaster.tif" # change to image location

#############################################################################################################

if __name__ == '__main__':
    #TweakedDisplay(GEO_PATH)
    #display(GEO_PATH)
    location = "/home/caiden/PycharmProjects/Physics-Informed-Deep-Learning-For-Damage-Assessment/data/gt_post/mexico-earthquake_00000002_post_disaster_target.png"
    location = "processed/fromJSON.png"
    display(location)
    #tiffManage('./processed/output.tif') #WILL NOT IDENTIFY 32 BIT FILE
    #splits = split_image.split_image('processed/composite_rgb.tif', 64, 64, False, False, output_dir='./processed/splits') # NOT EFFICIENT AT ALL
    #print(skimage.io.imread((GEO_PATH))) # displays rgb values
