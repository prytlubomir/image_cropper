'''
Cut some from top and bottom of every images in selected directory.
'''
import os
from typing import Iterable, Any

from PIL import Image

import config as conf


def file_filter(filenames: Iterable[Any], formats: Iterable[Any]) -> list:
    '''Filter files by supported formats'''
    result = []
    for filename in filenames:
        if filename.split('.')[-1] in formats:
            result.append(filename)
    return result


def crop_image(image: Image, crop_height: int) -> Image:
    '''Cut some pixels from top and bottom of selected image.'''
    width, height = image.size
    crop_rectangle = (0, 60, width, height - crop_height)

    cropped = image.crop(crop_rectangle)

    return cropped


if __name__ == "__main__":

    files = os.listdir(conf.INPUT)
    files = file_filter(files, conf.IMG_FORMATS)

    for file in files:
        img = Image.open(f'{conf.INPUT}/{file}')
        img2 = crop_image(img, conf.CROP_HEIGHT)

        number = files.index(file)
        extention = file.split('.')[-1]
        img2.save(f'{conf.OUTPUT}/{conf.NEW_FILES_NAME}{number}.{extention}')
