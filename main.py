'''
Crop a few pixels from the top and bottom of each image in the selected directory.
'''
import os                          # file system

import sys                         # interface

import configparser                # configuration

# annotations
from typing import Type, Callable, Iterable, Any

from PIL import Image              # image processing


def diverse_input(
    filtered_args: Iterable[Any],
    config_data: Any,
    args_index: int=0,
    input_message: str="Enter data: ",
    converter: Callable = lambda data: data
) -> Any:
    '''
    Guarantees receipt of required parametest by getting them in multiple ways.
    Some ways have advantage over others in the following order:

        argument > config > input    

    Arguments:

     - filtered_args: list - must be a list of command line argument filtered by some type of data,
                    but you can pass whatever list you want;

     - config_data: Any - return of "configparse.ConfigParser.get()" or similar method;

     - args_index: int - expected index of expected data in "filtered_args";

     - input_message: str - will be used as an offer to enter data for user, if no data given;
    '''
    # get data from attributes
    if len(filtered_args) > args_index:
        data = filtered_args[args_index]
        data = converter(data)
        if data:
            return data

    # return data from config
    data = converter(config_data)
    if data:
        return data

    # ask user to insert data
    data = input(input_message)
    data = converter(data)
    if data:
        return data

    # display message if no data provided
    print("You given wrong data! QUITING!")
    sys.exit()


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


def instance_converter(_type: Type) -> Callable:
    '''Generate converter for passed type.'''
    def converter(data: Any) -> Any | None:
        '''Return data if data is instance of _type else return None'''
        if isinstance(data, _type):
            return data
        return None

    return converter


def path_converter(data: Any) -> str | None:
    '''Return data, if data is directory, else return None'''
    if os.path.isdir(data):
        return data
    return None


def formats_converter(data: Any) -> Iterable | None:
    '''Return data, if data is Iterable[str], else return None'''
    if isinstance(data, Iterable):
        return None

    for item in data:
        if not isinstance(item, str):
            return None

    return data


def number_converter(data: Any) -> int | None:
    '''Return data if data is number else return None'''
    if isinstance(data, int):
        return data
    if isinstance(data, float):
        return round(data)
    if isinstance(data, str):
        if data.isdigit():
            return int(data)
        splitted = data.split('.')
        if len(splitted) == 2 and all(filter(str.isdigit, splitted)):
            return round(float(data))


    return None


if __name__ == "__main__":
    # read configuration file
    config = configparser.ConfigParser()
    config.read('./config.ini')

    # declare variables
    INPUT  = config.get('storage', 'INPUT', fallback=None)
    OUTPUT = config.get('storage', 'OUTPUT', fallback=None)

    IMG_FORMATS = config.get('filter', 'IMG_FORMATS', fallback='').split()

    CROP_HEIGHT = config.get('settings', 'CROP_HEIGHT', fallback=None)

    NEW_FILE_NAMES = config.get('settings', 'NEW_FILE_NAMES', fallback=None)


    # read command line arguments
    # command line arguments have advantage over configuration file
    arg_paths = list(filter(os.path.exists, sys.argv[1:]))
    arg_crop  = list(filter(number_converter, sys.argv[1:]))

    # NEW_FILE_NAMES and IMG_FORMATS
    arg_str   = list(filter(lambda x: not number_converter(x) and not os.path.exists(x), sys.argv[1:]))

    '''TODO: clear following code'''
    # path to input dir
    INPUT = diverse_input(arg_paths, INPUT, 0, "Path to the input directory", path_converter)
    # path to output dir
    OUTPUT = diverse_input(arg_paths, OUTPUT, 1, 'Path to output directory: ', path_converter)
    # get first part of new file names
    NEW_FILE_NAMES = diverse_input(arg_str, NEW_FILE_NAMES, 0, "First part of new file names: ")

    # get crop heigth
    __crhmsg = "How much pixels do you want to crop? : "
    CROP_HEIGHT = diverse_input(arg_crop, CROP_HEIGHT, 0, __crhmsg, number_converter)

    # get a list of image formats
    if len(arg_str) > 1:
        IMG_FORMATS = arg_str[1:]
    elif not IMG_FORMATS:
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

    print("Files found.")


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
