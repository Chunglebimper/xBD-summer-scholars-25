import os.path
import rasterio
import rasterio.plot
import PIL
import pandas as pd
import json
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
    width, height = 512, 512

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


##################### RUN ME ########################
FILENAME = 'geotiffs/reduced_set_json/mexico-earthquake_00000000_post_disaster.json'
FILENAME_img = "black_image.tif"
count = 0
data = load(FILENAME)
data.items()
features = data['features']['xy']
black_tif()
#pretty_print(FILENAME)
####################################################

with rasterio.open(FILENAME_img) as src:
    image = src.read([1])  # RGB bands
    print(image)
    #image = (255 * (image / image.max())).astype('uint8')  # Normalize for display


fig, ax = plt.subplots(dpi=512, figsize=(1, 1), ) #create plot to draw polygons

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
        'no-damage': '#000000', #gren
        'minor-damage': '#404040', #yellow
        'moderate-damage': '#808080', #orange
        'major-damage': '#BFBFBF', #red
        'destroyed': '#FFFFFF', #purple
    }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

    patch = patches.Polygon(coords, closed=True, edgecolor=color, facecolor=color, fill=True, linewidth=0.1)  # create patch with color handling from above
    ax.add_patch(patch)

#ax.set_title("Polygon Overlay on Image")
plt.gca().invert_yaxis()  # Ensure Y-axis matches image direction
ax.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove padding
plt.savefig("processed/fromJSON.png", bbox_inches='tight', pad_inches=0)
#plt.show()
print("saved")