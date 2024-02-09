'''Configuration for the image cropper'''

INPUT = './abc' # directory with uncropped images
OUTPUT = './cba' # directory to save cropped images

IMG_FORMATS = ['png', 'jpg', 'jpeg'] # all files that do not match the allowed formats will ignored

CROP_HEIGHT = 60 # number of pixels to crop on one side

NEW_FILES_NAME = 'initiald' # new file names will start with this
