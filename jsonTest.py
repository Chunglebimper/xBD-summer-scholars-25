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

FILENAME = 'geotiffs/reduced_set_json/mexico-earthquake_00000000_post_disaster.json'
FILENAME_img = 'geotiffs/reduced_set/mexico-earthquake_00000000_post_disaster.tif'
data = load(FILENAME)
data.items()
features = data['features']['xy']

# Open and read filename
with rasterio.open(FILENAME_img) as src:
    image = src.read([1, 2, 3])  # RGB bands
    image = (255 * (image / image.max())).astype('uint8')  # Normalize for display

fig, ax = plt.subplots(figsize=(10, 10)) #create plot to draw polygons

for feature in features:
    print(feature['properties']['subtype'])
    level_of_destruction = feature['properties']['subtype']
    #print(feature['wkt'])         # Access the polygon string
    wkt_str = feature['wkt']
    polygon = wkt.loads(wkt_str)
    coords = [(x, y) for x, y in polygon.exterior.coords]

    # --- Plot ---
    show(image, ax=ax)  # Use rasterio to show the image with correct orientation

    # Add polygon overlay
    # Determine color of edge
    color = {
        'no-damage': '#2ECC71', #gren
        'minor-damage': '#F1C40F', #yellow
        'moderate-damage': '#E67E22', #orange
        'major-damage': '#E74C3C', #red
        'destroyed': '#6C3483', #purple
    }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

    patch = patches.Polygon(coords, closed=True, edgecolor=color, fill=False, linewidth=2)  # create patch with color handling from above
    ax.add_patch(patch)

ax.set_title("Polygon Overlay on Image")
plt.gca().invert_yaxis()  # Ensure Y-axis matches image direction
plt.savefig("processed/my_plot.png")
plt.show()
print("saved")
