from PIL import Image
from PIL import ImageChops
from PIL import ImageEnhance

import os

def ela(image_path, image_quality = 95):
    """
    Performs Error Level Analysis on given image (by filepath and quality).
    """
    folder_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path)

    resaved_image_path = folder_path + '/resaved_' + image_name
    ela_image_path = folder_path + '/ela_' + image_name

    # Saving and resaving in different image_quality in order to see the difference in quality
    image = Image.open(image_path)
    image.save(fp = resaved_image_path, quality = image_quality)
    resaved_image = Image.open(resaved_image_path)

    # Calculates difference in quality
    ela_image = ImageChops.difference(image, resaved_image)
    extrema = ela_image.getextrema()
    max_difference = max([ex[1] for ex in extrema])
    scale = 255.0/max_difference

    # Creates new image black and white with brightness corresponding to difference to highlight changes 
    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    print(f'Maximum difference was {max_difference}')

    ela_image.save(ela_image_path)

if __name__ == '__main__':
    ela("../images/test.jpg")