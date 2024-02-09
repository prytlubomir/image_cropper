'''
Crop a few pixels from the top and bottom of each image in the selected directory.
'''
import os                          # interface

from typing import Iterable, Any   # annotations

from PIL import Image              # image processing

import config as conf              # configuration


def filter_files(filenames: Iterable[Any], formats: Iterable[Any]) -> list:
    '''Filter files by supported formats'''
    result = []
    for filename in filenames:
        if filename.split('.')[-1] in formats:
            result.append(filename)
    return result


def crop_image(image: Image, crop_height: int) -> Image:
    '''Crop a few pixels from the top and bottom of the selected image.'''
    width, height = image.size
    crop_rectangle = (0, 60, width, height - crop_height)

    cropped = image.crop(crop_rectangle)

    return cropped


if __name__ == "__main__":

    # get a list of image file names
    files = os.listdir(conf.INPUT) # get the contents of the input directory
    files = filter_files(files, conf.IMG_FORMATS) # remove everything except images

    # process images
    for file in files:
        # crop image
        img = Image.open(f'{conf.INPUT}/{file}') # get uncropped image
        img2 = crop_image(img, conf.CROP_HEIGHT)

    	# save image
        number = files.index(file)
        extension = file.split('.')[-1]
        img2.save(f'{conf.OUTPUT}/{conf.NEW_FILES_NAME}{number}.{extension}')
