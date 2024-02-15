'''
Crop a few pixels from the top and bottom of each image in the selected directory.
'''
# interface
import os
import sys

import configparser                # configuration

# annotations
from typing import Iterable, Any

from PIL import Image              # image processing


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
    # read configuration file
    config = configparser.ConfigParser()
    config.read('./config.ini')
    # declare variables
    INPUT  = config.get('storage', 'INPUT')
    OUTPUT = config.get('storage', 'OUTPUT')
    IMG_FORMATS = config.get('filter', 'IMG_FORMATS').split()
    CROP_HEIGHT = config.getint('settings', 'CROP_HEIGHT')
    NEW_FILE_NAMES = config.get('settings', 'NEW_FILE_NAMES')
    '''
    TODO:
    The config file should be just a simple .txt file
    since a .py file must be imported
    but import in the if statement doesn't look good.
    '''
    # get paths to input and output directories
    arg_paths = list(map(os.path.exists, sys.argv[1:]))

    # get path to input directory
    if len(arg_paths) > 0:
        INPUT  = arg_paths[0]
    elif 'conf' in globals() and 'INPUT' in conf.__dir__():
        INPUT = conf.INPUT
    else:
        INPUT = input('Path to input directory: ')

    if len(arg_paths) > 1:
        OUTPUT = arg_paths[1:]
    elif 'conf' in globals() and 'OUTPUT' in conf.__dir__():
        OUTPUT = conf.OUTPUT
    else:
        print('Enter paths to output directories separated by space.')
        OUTPUT = input(': ').split(' ')


    # get a list of image file names
    files = os.listdir(INPUT) # get the contents of the input directory
    files = filter_files(files, IMG_FORMATS) # remove everything except images

    # process images
    for file in files:
        # crop image
        img = Image.open(f'{INPUT}/{file}') # get uncropped image
        img2 = crop_image(img, CROP_HEIGHT)

    	# save image
        number = files.index(file)
        extension = file.split('.')[-1]
        img2.save(f'{OUTPUT}/{NEW_FILE_NAMES}{number}.{extension}')
