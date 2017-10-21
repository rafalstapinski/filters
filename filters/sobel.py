from PIL import Image
import numpy as np

class Sobel:

    def __init__(self):

        self.kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

    def open(self, path):

        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.raw = self.image.load()
        self.data = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.output = np.zeros((self.height - 2, self.width - 2, 3), dtype=np.uint8)

    @staticmethod
    def __luminosity__(rgb):
        return (.21 * rgb[0]) + (.72 * rgb[1]) + (.07 * rgb[2])

    @staticmethod
    def __average__(rgb):
        return sum(rgb) / 3

    @staticmethod
    def __lightness__(rgb):
        return (max(rgb) + min(rgb)) / 2

    def __grayscale__(self, scale):

        for x in xrange(0, self.width):
            for y in xrange(0, self.height):
                self.data[y, x] = scale(self.raw[x, y])

    def __edge_x__(self, kernel=None):

        if kernel is None:
            kernel = self.kernel

    def edge_x(self, kernel=None):

        # TODO: error checking for kernel

        if kernel is None:
            pass


    def grayscale(self, mode):
        if mode == None:
            mode = 'lum'

        if mode == 'lum':
            self.__grayscale__(self, self.__luminosity__)
        elif mode == 'avg':
            self.__grayscale__(self, self.__average__)
        elif mode == 'lht':
            self.__grayscale__(self, self.__lightness__)
        else:
            pass
            # TODO: error handling

    def show(self):
        img = Image.fromarray(self.data, 'RGB')
        img.show()
