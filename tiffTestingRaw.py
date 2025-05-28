from PIL import Image, ImageSequence
import numpy as np
import rasterio

def view_tiff(tiff_path):
    """"
    NOTE: CANNOT ACCEPT 32 BIT IMAGE; must be preprocessed; ROTATES IMAGE
    This function helped me gain an understanding of the PIL library despite its slow functionality
    """

    try:
        image_array = np.array(image)
        print(image_array)
        img = Image.new("RGBA", (1024, 1024)) #create space to draw
        rcount = 0
        ccount = 0
        np.set_printoptions(threshold=np.inf, linewidth=1024)
        for row in image_array:
            for col in row:
                print(col)

            """
            for col in row:
                temp = ((int(col[0])), int(col[1]), int(col[2]))
                img.putpixel((rcount, ccount), value=temp)
                print(f'img.putpixel(({rcount}, {ccount}), value={temp})')
                ccount += 1
            ccount = 0
            rcount += 1
            """

        img.save("./processed/drawn.tif")
    except FileNotFoundError:
        print(f"Error: File not found at {tiff_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    tiff_file = "geotiffs/tier3/images/joplin-tornado_00000000_post_disaster.tif"  # Replace with your TIFF file path
    with rasterio.open('geotiffs/tier1/images/mexico-earthquake_00000192_post_disaster.tif') as src:
        image = src.read()
    #for i in image:
        #print(i)
    #image = Image.open(tiff_file)  # BE SURE TO PLACE A NON-32 BIT IMAGE HERE SIZED TO 1024 x 1024

    #image = Image.open("./processed/resized.tif") # BE SURE TO PLACE A NON-32 BIT IMAGE HERE SIZED TO 1024 x 1024
    view_tiff(image)