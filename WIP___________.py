import os.path
import rasterio
import rasterio.plot
import PIL
import pandas as pd
import json

from skimage import io
from shapely import wkt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rasterio.transform import rowcol
from rasterio.plot import show
from rasterio.transform import from_origin
import numpy as np
from PIL import Image, ImageSequence

# 1. Create an image to draw on
# 2.



def load(json_file):
    with open(json_file) as f:
        data = json.load(f)
        return data

def pretty_print(json_file):
    """
    displays formatted json
    """
    with open(json_file) as f:
        data = json.load(f)
    new_json = json.dumps(data, indent=4)
    print(new_json)

def black_tif():
    # Image dimensions (width, height)
    width, height = 1024, 1024

    # Create a black image (all zeros)
    black_image = np.zeros((height, width), dtype=np.uint8)

    # Define geotransform (top-left corner coordinates and pixel size)
    transform = from_origin(0, 0, 1, 1)  # (west, north, x_pixel_size, y_pixel_size)

    # Create a new GeoTIFF file and write the black image
    with rasterio.open(
            './processed/black_image.tif',
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=1,  # number of bands
            dtype=black_image.dtype,
            crs='+proj=latlong',  # coordinate reference system
            transform=transform
    ) as dst:
        dst.write(black_image, 1)
    print(black_image.dtype)


def json_to_image( features, blackImage='./processed/black_image.tif', save_path='processed/fromJSON.png'):
    # Call function to create image to draw on
    black_tif()
    with rasterio.open(blackImage) as src:
        image = src.read(1).squeeze()  # RGB bands
        #print(image)
        # image = (255 * (image / image.max())).astype('uint8')  # Normalize for display

    # fig = figure_object, ax = axes_object for indexing subplots
    fig, ax = plt.subplots(dpi=100, figsize=(10.24, 10.24), )
    ##################################################################################################
    # Quantize into 5 bins: 0–51 -> 0, 52–102 -> 1, ..., 204–255 -> 4
    #image = np.floor(image / 255 * 5)
    #image = np.clip(image, 0, 4).astype(np.uint8)
    ##################################################################################################

    for feature in features:
        # print(feature['properties']['subtype'])
        level_of_destruction = feature['properties']['subtype']
        # print(feature['wkt'])         # Access the polygon string
        wkt_str = feature['wkt']
        polygon = wkt.loads(wkt_str)
        coords = [(x, y) for x, y in polygon.exterior.coords]

        # --- Plot ---
        show(image, ax=ax, cmap='gray')  # Use rasterio to show the image with correct orientation
        # Add polygon overlay
        # Determine color of edge
        color = {
            'no-damage': '#000000',  # gren
            'minor-damage': '#010101',  # yellow
            'moderate-damage': '#020202',  # orange
            'major-damage': '#030303',  # red
            'destroyed': '#040404',  # purple
        }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

        patch = patches.Polygon(coords, closed=True, edgecolor=color, facecolor=color, fill=True,
                                linewidth=0.1)  # create patch with color handling from above
        ax.add_patch(patch)

    # ax.set_title("Polygon Overlay on Image")
    # plt.gca().invert_yaxis()  # Ensure Y-axis matches image direction
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove padding
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    # plt.show()

    print(f"saved to: {save_path}")
    os.remove('./processed/black_image.tif')


    with rasterio.open(save_path) as src:
        image = src.read()
        np.shape(image)
        image = np.delete(image, 0, axis=1)
        image = np.delete(image, 0, axis=2)
        image = np.delete(image, 0, axis=1)
        image = image.squeeze()
        print(np.shape(image))
        print(image)
        finalized = Image.fromarray(image, mode='L')
        finalized.save(f"processed/fromJSON2.png")



def newDisplayImage(PATH, save_path):

    with rasterio.open(PATH) as src:
        display_image = src.read()

    print(display_image)
    print("normalizing...")
    print(display_image.max())
    image_array = (255 * (display_image / display_image.max())).astype(np.uint8)
    composite_image = Image.fromarray(image_array, mode='RGB')
    composite_image.save('./processed/nullified.png')




##################### RUN ME ########################
FILENAME = 'geotiffs/reduced_set_json/mexico-earthquake_00000000_post_disaster.json'
count = 0
data = load(FILENAME)
#print(data.items())
features = data['features']['xy']
#np.set_printoptions(threshold=np.inf, linewidth=512)

json_to_image(features,
              blackImage = './processed/black_image.tif',
              save_path='processed/fromJSON.png')
#newDisplayImage(PATH='processed/fromJSON.png', save_path="000000UTPUT")
#pretty_print(FILENAME)
####################################################


"""
with rasterio.open(FILENAME_img) as src:
    image = src.read(1).squeeze()  # RGB bands
    print(image)
    #image = (255 * (image / image.max())).astype('uint8')  # Normalize for display


fig, ax = plt.subplots(dpi=100, figsize=(10.24, 10.24), ) #create plot to draw polygons
# Quantize into 5 bins: 0–51 -> 0, 52–102 -> 1, ..., 204–255 -> 4
image = np.floor(image / 255 * 5)
image = np.clip(image, 0, 4).astype(np.uint8)


for feature in features:
    #print(feature['properties']['subtype'])
    level_of_destruction = feature['properties']['subtype']
    #print(feature['wkt'])         # Access the polygon string
    wkt_str = feature['wkt']
    polygon = wkt.loads(wkt_str)
    coords = [(x, y) for x, y in polygon.exterior.coords]


# --- Plot ---
    show(image, ax=ax, cmap='gray')  # Use rasterio to show the image with correct orientation
    # Add polygon overlay
    # Determine color of edge
    color = {
        'no-damage': '#010101', #gren
        'minor-damage': '#020202', #yellow
        'moderate-damage': '#030303', #orange
        'major-damage': '#040404', #red
        'destroyed': '#050505', #purple
    }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

    patch = patches.Polygon(coords, closed=True, edgecolor=color, facecolor=color, fill=True, linewidth=0.1)  # create patch with color handling from above
    ax.add_patch(patch)

#ax.set_title("Polygon Overlay on Image")
#plt.gca().invert_yaxis()  # Ensure Y-axis matches image direction
ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove padding
plt.savefig("processed/fromJSON.png", bbox_inches='tight', pad_inches=0)
#plt.show()
print("saved")
"""

"""with rasterio.open('processed/fromJSON.png') as src:
    image = src.read(1).squeeze()  # RGB bands
    print(image)
normalized_image = (image - np.mean(image)) / np.std(image)
print(image)"""
