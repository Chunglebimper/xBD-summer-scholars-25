# import libraries
import cv2
import os
import matplotlib
from matplotlib import pyplot as plt
from os.path import exists
import numpy as np
from PIL import Image
import rasterio
from matplotlib import cm
from pylab import *

def openTiff(tiff_path):
    with rasterio.open(tiff_path) as src:
        image = src.read()
    return image

def rawTiff2composite(tiff_path):
    """ Converts raw tif image from 3 band image to each individual band as well as composite
    Modified from ChatGPT*
    """
    # np.set_printoptions(threshold=np.inf, linewidth=10)
    image = openTiff(tiff_path)
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
        image_array = np.transpose(image_array, (1, 2, 0))
        # Above line changes order of bands to be read by
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

        # print(f'Before normalizing: {image_array}')
        if image_array.dtype != np.uint8:  # changes all values to something more readable in RGB (aka normalized)
            print("normalizing...")
            image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
        # print(f'After normalizing: {image_array}')

        # saves full composite image
        composite_image = Image.fromarray(image_array, mode='RGB')
        composite_image.save('./processed/composite_rgb.tif')
        print("Saved: composite_rgb.tif")

        # saves greyscale images
        # band_names = ['red', 'green', 'blue']
        # for i, name in enumerate(band_names):
        # band = image_array[:, :, i]  # isolate band as grayscale
        # Image.fromarray(band, mode='L').save(f'./processed/band_{name}_grayscale.tif')
        # print(f"Saved: band_{name}_grayscale.tif")

    except FileNotFoundError:
        print(f"Error: File not found at {tiff_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def printRawTiff2array(tiff_path, pixels_per_line=512):
    image = openTiff(tiff_path)
    count = 0
    rcount = 0
    ccount = 0
    np.set_printoptions(threshold=np.inf, linewidth=pixels_per_line)
    image_array = np.array(image)
    #print(image_array)

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

def loopConvertTiff(DIRECTORY="../geotiffs/reduced_set", ):
    """
    Directory: Directory of files to be converted
    * Automatically creates new directory for storing
    """
    COUNT = 0
    os.makedirs('../Tiff2Composite', exist_ok=True)
    # ------- INITIATE LOOP -------
    for fname in os.listdir(DIRECTORY):  # inside directory
        tiff_file = os.path.join(DIRECTORY, fname)
        with rasterio.open(tiff_file) as src:
            image = src.read()

            global COUNT
            image_array = np.array(image)
            image_array = np.transpose(image_array, (1, 2, 0))
            image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
            composite_image = Image.fromarray(image_array, mode='RGB')
            composite_image.save(f'../reduced_size_preprocessing/{COUNT}{fname}.png')
            print(f"Saved:\t composite_rgb{COUNT}.png'")
            COUNT += 1

def WIP_newMeanStd(tiff_path):
    """
    BEWARE OF THE SHAPE OF THE IMAGE COMING IN
    SHOULD WORK WITH FILE OF SHAPE FROM rawTiff2Composite()
    """
    # Open image and convert to RGB
    image = Image.open(tiff_path).convert("RGB")

    # Get pixel data and reshape to (H, W, 3)
    pixel_data = np.array(image)  # shape: (H, W, 3)

    # Reshape to a 2D array: (num_pixels, 3)
    pixels = pixel_data.reshape(-1, 3)

    # Split into channels
    np.set_printoptions(threshold=np.inf, linewidth=1024)
    reds = pixels[:, 0]
    greens = pixels[:, 1]
    blues = pixels[:, 2]

    # Compute means
    R_mean = np.mean(reds)
    G_mean = np.mean(greens)
    B_mean = np.mean(blues)
    #print(reds)

    print(R_mean, G_mean, B_mean)

def WIP_view_tiff(tiff_path):
    """"
    NOTE: CANNOT ACCEPT 32 BIT IMAGE; must be preprocessed; ROTATES IMAGE
    This function helped me gain an understanding of the PIL library despite its slow functionality
    FUNCTION DOES NOT WORK WITH RASTERIO/ORIGINAL 32 BIT FORMAT
    """
    try:
        image_array = np.array(tiff_path)
        print(image_array)
        img = Image.new("RGBA", (1024, 1024)) #create space to draw
        rcount = 0
        ccount = 0
        #np.set_printoptions(threshold=np.inf, linewidth=1024)
        for row in image_array:
            for col in row:
                temp = ((int(col[0])), int(col[1]), int(col[2]))
                img.putpixel((rcount, ccount), value=temp)
                print(f'img.putpixel(({rcount}, {ccount}), value={temp})')
                ccount += 1
            ccount = 0
            rcount += 1
        img.save(f"../processed/drawn.png")
    except FileNotFoundError:
        print(f"Error: File not found at {tiff_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # automatically handles directory creation
    PATHS = ['processed', 'processed/splits']
    for PATH in PATHS:
        os.makedirs(PATH, exist_ok=True)

    rawTiff2composite("geotiffs/reduced_set/mexico-earthquake_00000000_pre_disaster.tif")
    printRawTiff2array("geotiffs/reduced_set/mexico-earthquake_00000000_pre_disaster.tif")