from PIL import Image
import numpy as np

class Sobel:

    def open(self, path):

        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.data = np.array(self.image)
        # self.data = np.zeros((self.height, self.width), dtype=np.dtype('f8'))
        # self.edge = np.zeros((self.height - 2, self.width - 2), dtype=np.dtype('f8'))
        # self.output = np.zeros((self.height - 2, self.width - 2), dtype=np.uint8)

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


    def __channel__(self, i):
        for x in xrange(0 , self.width):
            for y in xrange(0 , self.height):
                self.data[y, x] = self.raw[x, y][i]

    def __edge_x__(self, k):

        for x in xrange(1 , self.width - 1):
            for y in xrange(1 , self.height - 1):
                self.x[y-1, x -1] = (self.data[y-1, x-1] * k[0][0]) + (self.data[y-1, x-0] * k[0][1]) + (self.data[y-1, x+1] * k[0][2]) + \
                                        (self.data[y-0, x-1] * k[1][0]) + (self.data[y-0, x-0] * k[1][1]) + (self.data[y-0, x+1] * k[1][2]) + \
                                        (self.data[y+1, x-1] * k[2][0]) + (self.data[y+1, x-0] * k[2][1]) + (self.data[y+1, x+1] * k[2][2])

        avg = np.mean(self.x)

        for x in xrange(0 , self.width - 2):
            for y in xrange(0 , self.height - 2):
                if self.x[y, x] < avg:
                    self.x[y, x] += (2 * (avg-self.x[y, x]))

        factor = abs(np.amax(self.x)) + abs(np.amin(self.x))
        self.x = (self.x - np.amin(self.x)) / factor * 255


    def __edge_y__(self, k):

        for x in xrange(1 , self.width - 1):
            for y in xrange(1 , self.height - 1):
                self.y[y-1, x -1] = (self.data[y-1, x-1] * k[0][0]) + (self.data[y-1, x-0] * k[0][1]) + (self.data[y-1, x+1] * k[0][2]) + \
                                        (self.data[y-0, x-1] * k[1][0]) + (self.data[y-0, x-0] * k[1][1]) + (self.data[y-0, x+1] * k[1][2]) + \
                                        (self.data[y+1, x-1] * k[2][0]) + (self.data[y+1, x-0] * k[2][1]) + (self.data[y+1, x+1] * k[2][2])

        avg = np.mean(self.y)

        for x in xrange(0 , self.width - 2):
            for y in xrange(0 , self.height - 2):
                if self.y[y, x] < avg:
                    self.y[y, x] += (2 * (avg-self.y[y, x]))

        factor = abs(np.amax(self.y)) + abs(np.amin(self.y))
        self.y = (self.y - np.amin(self.y)) / factor * 255


    def __blur__(self):

        for x in xrange(1 , self.width - 1):
            for y in xrange(1 , self.height - 1):
                self.data[y-1, x -1] = (self.data[y-1, x-1] / 16) + (self.data[y-1, x-0] / 8) + (self.data[y-1, x+1] / 16) + \
                                        (self.data[y-0, x-1] / 8) + (self.data[y-0, x-0] / 4) + (self.data[y-0, x+1] / 8) + \
                                        (self.data[y+1, x-1] / 16) + (self.data[y+1, x-0] / 8) + (self.data[y+1, x+1] / 16)


    def calc_x(self, kernel=None):

        # TODO: error checking for kernel

        if kernel == None:
            kernel = ((-1, 0, 1),
                    (-2, 0, 2),
                    (-1, 0, 1))

        self.__edge_x__(kernel)

        for x in xrange(0 , self.width - 2):
            for y in xrange(0 , self.height - 2):
                self.output[y, x] = self.x[y, x].astype(int)


    def calc_y(self, kernel=None):

        # TODO: error checking for kernel

        if kernel == None:
            kernel = ((-1, -2, -1),
                    (0, 0, 0),
                    (1, 2, 1))

        self.__edge_y__(kernel)

        for x in xrange(0 , self.width - 2):
            for y in xrange(0 , self.height - 2):
                self.output[y, x] = self.y[y, x].astype(int)


    def calc(self, channel=None, Lcomp=None):


        pass

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


    def channel(self, c):

        if c == 'R':
            i = 0
        elif c == 'G':
            i = 1
        elif c == 'B':
            i = 2
        else:
            # TODO: error handling
            pass

        self.__channel__(i)

    def show_d(self):
        img = Image.fromarray(self.output, 'L')
        img.show()

    def show(self):
        img = Image.fromarray(self.output, 'L')
        img.show()
