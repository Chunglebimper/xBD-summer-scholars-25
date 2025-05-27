from skimage import io
import split_image
import skimage
import matplotlib.pyplot as plt
import cv2
import numpy as np
import sys



def display(PATH):
    img = io.imread(PATH)                   # read the image stack
    plt.imshow(img, cmap='gray')
    plt.tight_layout()
    # show the image
    plt.axis('off')
    plt.savefig('output.jpg', transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.0)   # save the image
    plt.savefig('output2.tif', transparent=True, dpi=300, bbox_inches="tight", pad_inches=0.0)



#############################################################################################################



GEO_PATH = "/home/crota/Pictures/geotiffs/tier3/images/joplin-tornado_00000000_post_disaster.tif" # change to image location

display(GEO_PATH)
splits = split_image.split_image('output.jpg', 8, 8, False, True, output_dir='./processed')

#print(skimage.io.imread((f'{GEO_PATH}/joplin-tornado_00000000_post_disaster.tif'))) #displays rgb values