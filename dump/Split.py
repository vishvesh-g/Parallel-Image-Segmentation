import image_slicer

tiles = image_slicer.slice('image.png', 4, save=False)
print('Slicing')
image_slicer.save_tiles(tiles, prefix='slice', format='png')
print('Saving')
