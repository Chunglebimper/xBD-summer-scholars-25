from PIL import Image
import numpy as np

FILENAME_img = "/home/caiden/PycharmProjects/preproccessing/xBD-summer-scholars-25/reduced_size_preprocessing/composite_rgb5.png"

# Open image and convert to RGB
image = Image.open(FILENAME_img).convert("RGB")

# Get pixel data and reshape to (H, W, 3)
pixel_data = np.array(image)  # shape: (H, W, 3)

# Reshape to a 2D array: (num_pixels, 3)
pixels = pixel_data.reshape(-1, 3)

# Split into channels
reds = pixels[:, 0]
greens = pixels[:, 1]
blues = pixels[:, 2]

# Compute means
R_mean = np.mean(reds)
G_mean = np.mean(greens)
B_mean = np.mean(blues)

print(255/R_mean, 255/G_mean, 255/B_mean)