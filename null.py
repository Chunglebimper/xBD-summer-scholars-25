import numpy as np
from PIL import Image

my_list = []
reds = np.array(my_list)
greens = np.array(my_list)
blues = np.array(my_list)
FILENAME_img = "/home/caiden/PycharmProjects/preproccessing/xBD-summer-scholars-25/reduced_size_preprocessing/composite_rgb5.png"  # test one image
counting = 0
image = Image.open(FILENAME_img)  # Replace "your_image.jpg" with your image file path
image = image.convert("RGB")
pixel_data = np.array(image.getdata())
for R, G, B in pixel_data:
    reds = np.append(reds, R)
    greens = np.append(greens, G)
    blues = np.append(blues, B)
    print(counting)
    counting += 1
# -------------------------
R_mean = np.mean(reds)
G_mean = np.mean(greens)
B_mean = np.mean(blues)
print(R_mean, G_mean, B_mean)