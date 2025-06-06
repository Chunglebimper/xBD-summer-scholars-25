from PIL import Image, ImageSequence
import numpy as np
import rasterio
import os


def viewRaw_tiff(tiff_path):
    """ Converts raw tif image from 3 band image to each individual band as well as composite
    Modified from ChatGPT*
    """
    #np.set_printoptions(threshold=np.inf, linewidth=10)
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
        #Above line changes order of bands to be read by
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

        #print(f'Before normalizing: {image_array}')
        if image_array.dtype != np.uint8:           #changes all values to something more readable in RGB (aka normalized)
            print("normalizing...")
            image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
        #print(f'After normalizing: {image_array}')
        # saves full composite image
        composite_image = Image.fromarray(image_array, mode='RGB')
        composite_image.save('./processed/composite_rgb.tif')
        print("Saved: composite_rgb.tif")
        # saves greyscale images
        band_names = ['red', 'green', 'blue']
        for i, name in enumerate(band_names):
            band = image_array[:, :, i]  # isolate band as grayscale
            Image.fromarray(band, mode='L').save(f'./processed/band_{name}_grayscale.tif')
            print(f"Saved: band_{name}_grayscale.tif")

    except FileNotFoundError:
        print(f"Error: File not found at {tiff_path}")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    os.makedirs('./processed', exist_ok=True)
    tiff_file = "geotiffs/tier3/images/joplin-tornado_00000000_post_disaster.tif"  # Replace with your TIFF file path
    with rasterio.open(tiff_file) as src:
        image = src.read()
    viewRaw_tiff(image)



