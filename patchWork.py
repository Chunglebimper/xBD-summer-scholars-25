from skimage import io
import split_image
import skimage
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys
import tifffile as tiff
from PIL import Image
import os


def display(PATH):
    """
    figure is NOT raw and is increased in size for unknown reason
    :param PATH: import path of data to be processed
    :return: none, figs are saved according to the plt.savefig name
    """
    img = io.imread(PATH)  # read the image stack
    plt.imshow(img, cmap='gray')
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




#############################################################################################################
PATHS = ['processed']
for PATH in PATHS:
    os.makedirs(PATH, exist_ok=True)        #automatically handles directory creation

"""CONSTANTS"""
GEO_PATH = "geotiffs/tier3/images/joplin-tornado_00000000_post_disaster.tif" # change to image location

#############################################################################################################

if __name__ == '__main__':
    display(GEO_PATH)
    tiffManage('./processed/output.tif') #WILL NOT IDENTIFY 32 BIT FILE
    #splits = split_image.split_image('output2.tif', 8, 8, False, False, output_dir='./processed')
    #print(skimage.io.imread((GEO_PATH))) # displays rgb values
