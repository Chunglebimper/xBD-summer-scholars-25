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
            'black_image.tif',
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

def json_to_image(FILENAME_img, features, save_path='processed/fromJSON.png'):
    with rasterio.open(FILENAME_img) as src:
        image = src.read(1).squeeze()  # RGB bands
        #print(image)
        # image = (255 * (image / image.max())).astype('uint8')  # Normalize for display

    fig, ax = plt.subplots(dpi=100, figsize=(10.24, 10.24), )  # create plot to draw polygons
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
            'no-damage': '0.2',  # gren
            'minor-damage': '0.4',  # yellow
            'moderate-damage': '0.5',  # orange
            'major-damage': '0.8',  # red
            'destroyed': '1.0',  # purple
        }.get(level_of_destruction, '0.0')  # Default to black if level_of_destruction is invalid

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
FILENAME_img = "black_image.tif"
count = 0
data = load(FILENAME)
data.items()
features = data['features']['xy']
np.set_printoptions(threshold=np.inf, linewidth=512)
black_tif()
json_to_image(FILENAME_img, features, save_path='processed/fromJSON.png')
newDisplayImage(PATH='processed/fromJSON.png', save_path="000000UTPUT")
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
