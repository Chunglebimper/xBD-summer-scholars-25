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
import rasterio


PATH = "/home/caiden/PycharmProjects/Physics-Informed-Deep-Learning-For-Damage-Assessment/data/gt_post/mexico-earthquake_00000000_post_disaster_target.png"  # Replace with your TIFF file path
PATH = "processed/fromJSON.png"

count = 0
rcount = 0
ccount = 0


def convert_tiff(tiff_path):
    global count
    global rcount
    global ccount
    np.set_printoptions(threshold=np.inf, linewidth=512)
    image_array = np.array(tiff_path)
    print(image_array)


    for i in image_array:
        print(i)
        print(512*512)
    for band in image_array:
        count += 1
        for row in band:
            rcount += 1
            for col in row:
                ccount += 1
    print(f'Number of bands: {count}')
    print(f'Number of rows: {rcount}')
    print(f'Number of items: {ccount}')

    image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
    composite_image = Image.fromarray(image_array, mode='L')
    composite_image.save(f'../reduced_size_preprocessing/composite_rgb{count}.png')
    print(f"Saved:\t composite_rgb{count}.png'")
    count += 1

#synthesis spec files

with rasterio.open(PATH) as src:
    image = src.read()
convert_tiff(image)





