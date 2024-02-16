'''
Crop a few pixels from the top and bottom of each image in the selected directory.
'''
import os                          # file system

import sys                         # interface

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
    crop_rectangle = (0, crop_height, width, height - crop_height)

    cropped = image.crop(crop_rectangle)

    return cropped


if __name__ == "__main__":
    # read configuration file
    config = configparser.ConfigParser()
    config.read('./config.ini')

    # declare variables
    INPUT  = config.get('storage', 'INPUT', fallback=None)
    OUTPUT = config.get('storage', 'OUTPUT', fallback=None)

    IMG_FORMATS = config.get('filter', 'IMG_FORMATS', fallback='').split()
    CROP_HEIGHT = config.getint('settings', 'CROP_HEIGHT', fallback=None)

    NEW_FILE_NAMES = config.get('settings', 'NEW_FILE_NAMES', fallback=None)


    # read command line arguments
    # command line arguments have advantage over configuration file
    arg_paths = list(filter(os.path.exists, sys.argv[1:]))
    arg_crop  = list(filter(lambda x: x.isdigit(), sys.argv[1:]))

    # NEW_FILE_NAMES and IMG_FORMATS
    arg_str   = list(filter(lambda x: not x.isdigit() and not os.path.exists(x), sys.argv[1:]))

    '''TODO: clear following code'''
    # get path to input directory
    if len(arg_paths) > 0:
        INPUT  = arg_paths[0]
    elif INPUT == None:
        INPUT = input('Path to input directory: ')

    # get path to output directory
    if len(arg_paths) > 1:
        OUTPUT = arg_paths[1]
    elif OUTPUT == None:
        OUTPUT = input('Path to output directory: ')

    # get crop heigth
    if len(arg_crop) > 0:
        CROP_HEIGHT = arg_crop[0]
        # validation
        if not CROP_HEIGHT.isdigit():
            print('Crop height must be digit!') # error message
            sys.exit() # stop program
        # convertation
        CROP_HEIGHT = int(CROP_HEIGHT)
    elif CROP_HEIGHT == None:
        CROP_HEIGHT = input("How much pixels do you want to crop? : ")
        # validation
        if not CROP_HEIGHT.isdigit():
            print('Crop height must be digit!') # error message
            sys.exit() # stop program
        # convertation
        CROP_HEIGHT = int(CROP_HEIGHT)

    # get first part of new file names
    if len(arg_str) > 0:
        NEW_FILE_NAMES = arg_str[0]
    elif NEW_FILE_NAMES == None:
        NEW_FILE_NAMES = input("First part of new file names: ")

    # get a list of image formats
    if len(arg_str) > 1:
        IMG_FORMATS = arg_str[1:]
    elif IMG_FORMATS == []:
        print("Enter image formats you want to crop separated by space")
        # get string
        # separate it by space to list
        IMG_FORMATS = input(": ").split(' ')
    # make all items lowercase
    IMG_FORMATS = list(map(lambda x: x.lower(), IMG_FORMATS))

    # get a list of image file names

    print("Searching files...")

    files = os.listdir(INPUT) # get the contents of the input directory
    files = filter_files(files, IMG_FORMATS) # remove everything except images

    print("Files find.")


    # process images

    print("Start cropping images...")

    for file in files:
        # crop image
        img = Image.open(f'{INPUT}/{file}') # get uncropped image
        img2 = crop_image(img, CROP_HEIGHT)

        print(f"Image {file} cropped.")


    	# save image
        number = files.index(file)
        extension = file.split('.')[-1]
        new_file_name = f'{NEW_FILE_NAMES}{number}.{extension}'
        img2.save(f'{OUTPUT}/{new_file_name}')

        print(f"Image {file} saved as {new_file_name}")
