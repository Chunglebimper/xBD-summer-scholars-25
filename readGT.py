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

def convert_tiff(tiff_path):
    global COUNT
    image_array = np.array(tiff_path)
    print(image_array)

    for i in image_array:
        print(i)
    image_array = np.transpose(image_array, (0, 1, 2))
    image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
    composite_image = Image.fromarray(image_array, mode='L')
    composite_image.save(f'../reduced_size_preprocessing/composite_rgb{COUNT}.png')
    print(f"Saved:\t composite_rgb{COUNT}.png'")
    COUNT += 1

#synthesis spec files

with rasterio.open(PATH) as src:
    image = src.read()
convert_tiff(image)
COUNT = 0




