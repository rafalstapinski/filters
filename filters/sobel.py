from PIL import Image
import numpy as np

class Sobel:

    def __init__(self):

        self.kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]

    def open(self, path):

        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.raw = self.image.load()
        self.data = np.zeros((self.height, self.width, 3), dtype=np.dtype('f8'))
        self.output = np.zeros((self.height, self.width, 3), dtype=np.dtype('f8'))
        self.display = np.zeros((self.height - 2, self.width - 2, 3), dtype=np.uint8)

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

    def __edge_x__(self, kernel):

        for x in xrange(1 , self.width - 1):
            for y in xrange(1 , self.height - 1):
                self.output[y-1, x -1] = (self.data[y-1, x-1] * -1) + (self.data[y-1, x-0] * 0) + (self.data[y-1, x+1] * 1) + \
                                        (self.data[y-0, x-1] * -2) + (self.data[y-0, x-0] * 0) + (self.data[y-0, x+1] * 2) + \
                                        (self.data[y+1, x-1] * -1) + (self.data[y+1, x-0] * 0) + (self.data[y+1, x+1] * 1)

        print np.amax(self.output)
        print np.amin(self.output)

        factor = abs(np.amax(self.output)) + abs(np.amin(self.output))

        for x in xrange(0 , self.width):
            for y in xrange(0 , self.height):
                self.output[y, x] = (self.output[y, x] - np.amin(self.output)) / factor * 255
                self.output[y, x] = self.output[y, x].astype(int)


    def __blur__(self):

        for x in xrange(1 , self.width - 1):
            for y in xrange(1 , self.height - 1):
                self.data[y-1, x -1] = (self.data[y-1, x-1] / 16) + (self.data[y-1, x-0] / 8) + (self.data[y-1, x+1] / 16) + \
                                        (self.data[y-0, x-1] / 8) + (self.data[y-0, x-0] / 4) + (self.data[y-0, x+1] / 8) + \
                                        (self.data[y+1, x-1] / 16) + (self.data[y+1, x-0] / 8) + (self.data[y+1, x+1] / 16)


    def edge_x(self, kernel=None):

        # TODO: error checking for kernel

        if kernel == None:
            self.__edge_x__(self.kernel)
        else:
            self.__edge_x__(kernel)

    def grayscale(self, mode=None):
        if mode == None:
            mode = 'lum'

        if mode == 'lum':
            self.__grayscale__(self.__luminosity__)
        elif mode == 'avg':
            self.__grayscale__(self.__average__)
        elif mode == 'lht':
            self.__grayscale__(self.__lightness__)
        else:
            pass
            # TODO: error handling

    def __show__(self, o):

        for x in xrange(0, self.width - 2):
            for y in xrange(0, self.height - 2):
                self.display[y, x] = o[y, x].astype(int)

        img = Image.fromarray(self.display, 'RGB')
        img.show()

        #
        # img = Image.fromarray(self.display, 'RGB')
        # img.show()
        #
        # for x in o:
        #     print x
        #     break
        #
        # for x in o.astype(int):
        #     print x
        #     break


    def show(self):
        img = Image.fromarray(self.display, 'RGB')
        img.show()
