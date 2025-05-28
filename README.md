# xBD-summer-scholars-25
### patchWork.py
- display() makes the standard .tiff (32-bit) image visible in RGB range
    - enlarges image for unknown reason: could cause data loss
- tiffManage() resizes enlarged image from display() back to 1024 x 1024
    - could cause data loss as pixels are manipulated to resize image
- TweakedDisplay() reads np.array of image using skimage library and displays in 3D matplotlib graph
    - generally not useful and taxing on processing time (maybe useful to visualize .tiff files)
    - 
### tiffTestingDownscaled.py
- view_tiff() uses PIL/pillow library to read image as an array and manually draw image
    - has some issues and was made to be used on images output by tiffManage()

### tiffTestingRaw.py (WIP)
Will be used to read a tiff file directly and translate to a visible image. Uses rasterio library instead of the limited PIL library
which cannot read raw .tiff files. rasterio can read geospatial files with multiple layers.