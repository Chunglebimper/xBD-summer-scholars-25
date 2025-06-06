import os
from PIL import Image, ImageSequence
import numpy as np
import rasterio
import os



def convert_tiff(tiff_path):
    global COUNT
    image_array = np.array(image)
    image_array = np.transpose(image_array, (1, 2, 0))
    image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
    composite_image = Image.fromarray(image_array, mode='RGB')
    composite_image.save(f'../reduced_size_preprocessing/composite_rgb{COUNT}.png')
    print(f"Saved:\t composite_rgb{COUNT}.png'")
    COUNT += 1

if __name__ == "__main__":
    DIRECTORY = "../geotiffs/reduced_set"
    COUNT = 0
    os.makedirs('../reduced_size_preprocessing', exist_ok=True)
    # ------- INITIATE LOOP -------
    for fname in os.listdir(DIRECTORY):  # inside directory
        tiff_file = os.path.join(DIRECTORY, fname)
        with rasterio.open(tiff_file) as src:
            image = src.read()
        convert_tiff(image)