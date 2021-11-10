from ext.image_copy_move_detection import detect

import os

def clone_detection(image_path, block_size = 32):
    """
    Performs clone detection on given image (by filepath and block size).
    """
    folder_path = os.path.dirname(image_path)
    detect.detect(image_path, folder_path, block_size)

if __name__ == '__main__':
    clone_detection("../images/test_2.jpg", 16)