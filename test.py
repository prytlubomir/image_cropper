''' Test cropping '''

from PIL import Image

from main import crop_image


if __name__ == "__main__":
    img = Image.open('./Input/Знімок екрана (311).png')
    res = crop_image(img, 60)
    res.save('cropped.png')
