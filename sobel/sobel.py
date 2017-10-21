from PIL import Image

class Sobel:

    def __init__(self, image_path):

        self.image = Image.open(image_path)

        self.image.show()
