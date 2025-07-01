import os.path
import rasterio
import rasterio.plot
import PIL
import pandas as pd
import json
import cv2
import skimage
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


def json_to_image(features, save_path='processed/1_fromJSON_matplot.png'):
    X = 0
    Y = 0
    # fig = figure_object, ax = axes_object for indexing subplots
    fig, ax = plt.subplots(dpi=100, figsize=(5.12, 5.12), )

    # For every feature get the class and coordinates for plotting
    for feature in features:
        level_of_destruction = feature['properties']['subtype']
        wkt_str = feature['wkt']
        polygon = wkt.loads(wkt_str)
        coords = [(round(x / 2), round(y / 2)) for x, y in polygon.exterior.coords]

        # Use rasterio to show the image with correct orientation
        show(np.zeros((512, 512)), ax=ax, cmap='gray')

        # Add polygon overlay and determine color of edge
        color = {
            'no-damage': '#010101',
            'minor-damage': '#020202',
            'moderate-damage': '#030303',
            'major-damage': '#040404',
            'destroyed': '#050505',
        }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

        # Create patch with color handling from above
        patch = patches.Polygon(coords, closed=True, edgecolor=color, facecolor=color, fill=True,
                                linewidth=1, aa=None, rasterized=True)

        # print(coords)
        for x, y in coords:
            if x > X:
                X = x
            if y > Y:
                Y = y
        ax.add_patch(patch)

    print(X, Y)
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove padding
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    # plt.show()

    print(f"saved to: {save_path}")
    with rasterio.open(save_path) as src:
        image = src.read()
        print(np.shape(image))

    with rasterio.open(save_path) as src:
        image = src.read()
        print(np.shape(image))
        image = np.delete(image, obj=[1, 2, 3], axis=0)

        print(np.shape(image))
        image = src.read(1).squeeze()
        # print(np.shape(image))
        Image.fromarray(image).save("2_fromJSON_reformed.png")

    # Normalize
    with rasterio.open(
            "/home/caiden/PycharmProjects/Physics-Informed-Deep-Learning-For-Damage-Assessment/data/gt_post/mexico-earthquake_00000000_post_disaster_target.png") as src:
        image = src.read(1).squeeze()
        image = (255 * (image / image.max())).astype('uint8')  # Normalize for display
        print(np.shape(image))
        Image.fromarray(image).save("4_compare_toJunt.png")

    with rasterio.open("2_fromJSON_reformed.png") as src:
        image = src.read(1).squeeze()
        image = (255 * (image / image.max())).astype('uint8')  # Normalize for display
        Image.fromarray(image).save('temp.png')
        img = Image.open('temp.png')
        # print(img.size)

        out = img.resize((512, 512))
        out.save("3_fromJSON_reformed_512_normal.png")

def MODIFIED_json_to_image(features, save_path='processed/1_fromJSON_matplot.png'):
    X = 0
    Y = 0
    # fig = figure_object, ax = axes_object for indexing subplots
    fig, ax = plt.subplots(dpi=100, figsize=(10.24, 10.24), )

    # For every feature get the class and coordinates for plotting
    for feature in features:
        level_of_destruction = feature['properties']['subtype']
        wkt_str = feature['wkt']
        polygon = wkt.loads(wkt_str)
        coords = [(x, y) for x, y in polygon.exterior.coords]

        # Use rasterio to show the image with correct orientation
        show(np.zeros((1024,1024)), ax=ax, cmap='gray')

        # Add polygon overlay and determine color of edge
        color = {
            'no-damage': '#010101',
            'minor-damage': '#020202',
            'moderate-damage': '#030303',
            'major-damage': '#040404',
            'destroyed': '#050505',
        }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

        # Create patch with color handling from above
        patch = patches.Polygon(coords, closed=True, edgecolor=color, facecolor=color, fill=True,
                                linewidth=0, aa = False, rasterized=True)

        #print(coords)
        for x,y in coords:
            if x > X:
                X = x
            if y > Y:
                Y = y
        ax.add_patch(patch)

    print(X, Y)
    ax.axis('off')
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove padding
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0)
    #plt.show()

    print(f"saved to: {save_path}")
    with rasterio.open(save_path) as src:
        image = src.read()
        print(np.shape(image))

    with rasterio.open(save_path) as src:
        image = src.read()
        print(np.shape(image))
        image = np.delete(image, obj=[1,2,3], axis=0)

        print(np.shape(image))
        image = src.read(1).squeeze()
        #print(np.shape(image))
        Image.fromarray(image).save("2_fromJSON_reformed.png")

    # Normalize
    with rasterio.open("/home/caiden/PycharmProjects/Physics-Informed-Deep-Learning-For-Damage-Assessment/data/gt_post/mexico-earthquake_00000000_post_disaster_target.png") as src:
        image = src.read(1).squeeze()
        image = (255 * (image / image.max())).astype('uint8')  # Normalize for display
        print(np.shape(image))
        Image.fromarray(image).save("4_compare_toJunt.png")

    with rasterio.open("2_fromJSON_reformed.png") as src:
        image = src.read(1).squeeze()
        image = (255 * (image / image.max())).astype('uint8')  # Normalize for display
        Image.fromarray(image).save('temp.png')
        img =cv2.imread('temp.png')
        #print(img.size)

        out = skimage.transform.resize(img,
                                     (512, 512),
                                     mode='edge',
                                     anti_aliasing=False,
                                     anti_aliasing_sigma=None,
                                     preserve_range=True,
                                     order=0)

        #out = img.resize((512, 512))
        cv2.imwrite("6_fromJSON_RESIZED_512_normal.png", out)


if __name__ == '__main__':
    # Pseudocode
    # For every file in

    """
        for json,  in DIRECTOR
    print("Normailzing file...")
    
    """

# goal compare the existing Gt to the new gt NORMALIZED

FILENAME = 'geotiffs/reduced_set_json/mexico-earthquake_00000000_post_disaster.json'
data = load(FILENAME)
features = data['features']['xy']
MODIFIED_json_to_image(features)


