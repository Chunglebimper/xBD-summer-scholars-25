# xBD-summer-scholars-25
### tiffTestingRaw.py 
- This function reads tiff files of 32-bits using the rasterio library. By a process of converting the image to an array, and transposing the bands, the image is normalized and split into multiple RGB bands before being saved with a full composite image. 
________________________________
### patchWork.py (Old)
- display() makes the standard .tiff (32-bit) image visible in RGB range
    - enlarges image for unknown reason: could cause data loss
- tiffManage() resizes enlarged image from display() back to 1024 x 1024
    - could cause data loss as pixels are manipulated to resize image
- TweakedDisplay() reads np.array of image using skimage library and displays in 3D matplotlib graph
    - generally not useful and taxing on processing time (maybe useful to visualize .tiff files)
    - 
### tiffTestingDownscaled.py (Old)
- view_tiff() uses PIL/pillow library to read image as an array and manually draw image
    - has some issues and was made to be used on images output by tiffManage()

