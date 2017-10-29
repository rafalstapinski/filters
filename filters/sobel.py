from PIL import Image
import numpy as np
import math

class Sobel:

    def open(self, path):

        self.image = Image.open(path)
        self.width, self.height = self.image.size
        self.RGB_data = np.array(self.image)
        self.ONE_data = np.zeros((self.height, self.width), dtype=np.uint8)
        self.edge_data = np.zeros((self.height - 4, self.width - 4), dtype=np.dtype('f8'))

        return self

        # self.data = np.zeros((self.height, self.width), dtype=np.dtype('f8'))
        # self.edge = np.zeros((self.height - 2, self.width - 2), dtype=np.dtype('f8'))
        # self.output = np.zeros((self.height - 2, self.width - 2), dtype=np.uint8)

    @staticmethod
    def __luminosity__(r, g, b):
        return (.21 * r) + (.72 * g) + (.07 * b)

    @staticmethod
    def __average__(r, g, b):
        return (r + g + b) / 3

    @staticmethod
    def __lightness__(r, g, b):
        return (max((r, g, b)) + min((r, g, b))) / 2

    def __grayscale__(self, scale):

        for i in xrange(0, self.width):
            for j in xrange(0, self.height):
                pass

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


    def __set_channel__(self, channel, comp):

        if channel == 'L':
            if comp == 'luminosity':
                c = self.__luminosity__

        # TODO: Investigate: is converting to float array better for quality

        for j in xrange(0, self.width):
            for i in xrange(0, self.height):
                self.ONE_data.itemset((i, j), c(self.RGB_data.item(i, j, 0),
                                                self.RGB_data.item(i, j, 1),
                                                self.RGB_data.item(i, j, 2)))




    def edges(self, channel='L', comp='luminosity', blur=False,
            vk=[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
            hk=[[-1, -2, -1], [0, 0, 0], [1, 2, 1]]):

            # TODO: check for square kernels

            self.__set_channel__(channel, comp)

            # TODO: estimate max min by applying max value, min value to kernels
            # actually this would be static, assuming a drastic change of
            # 255 to 0
            # that would be 255 * 4 magnitude
            # flat would be 0 magnitude
            # check that out later performance wise vs finding all vals
            # and then normalizing

            for j in xrange(2, self.width - 2):
                for i in xrange(2, self.height - 2):

                    if blur:

                        ul = (self.ONE_data.item(i-2, j-2) / 16) + (self.ONE_data.item(i-1, j-2) / 8) + (self.ONE_data.item(i-0, j-2) / 16) + \
                             (self.ONE_data.item(i-2, j-1) / 8) + (self.ONE_data.item(i-1, j-1) / 4) + (self.ONE_data.item(i-0, j-1) / 8) + \
                             (self.ONE_data.item(i-2, j-0) / 16) + (self.ONE_data.item(i-1, j-0) / 8) + (self.ONE_data.item(i-0, j-0) / 16)

                        uc = (self.ONE_data.item(i-1, j-2) / 16) + (self.ONE_data.item(i-0, j-2) / 8) + (self.ONE_data.item(i+1, j-2) / 16) + \
                             (self.ONE_data.item(i-1, j-1) / 8) + (self.ONE_data.item(i-0, j-1) / 4) + (self.ONE_data.item(i+1, j-1) / 8) + \
                             (self.ONE_data.item(i-1, j-0) / 16) + (self.ONE_data.item(i-0, j-0) / 8) + (self.ONE_data.item(i+1, j-0) / 16)

                        ur = (self.ONE_data.item(i-0, j-2) / 16) + (self.ONE_data.item(i+1, j-2) / 8) + (self.ONE_data.item(i+2, j-2) / 16) + \
                             (self.ONE_data.item(i-0, j-1) / 8) + (self.ONE_data.item(i+1, j-1) / 4) + (self.ONE_data.item(i+2, j-1) / 8) + \
                             (self.ONE_data.item(i-0, j-0) / 16) + (self.ONE_data.item(i+1, j-0) / 8) + (self.ONE_data.item(i+2, j-0) / 16)

                        ml = (self.ONE_data.item(i-2, j-1) / 16) + (self.ONE_data.item(i-1, j-1) / 8) + (self.ONE_data.item(i-0, j-1) / 16) + \
                             (self.ONE_data.item(i-2, j-0) / 8) + (self.ONE_data.item(i-1, j-0) / 4) + (self.ONE_data.item(i-0, j-0) / 8) + \
                             (self.ONE_data.item(i-2, j+1) / 16) + (self.ONE_data.item(i-1, j+1) / 8) + (self.ONE_data.item(i-0, j+1) / 16)

                        mc = (self.ONE_data.item(i-1, j-1) / 16) + (self.ONE_data.item(i-0, j-1) / 8) + (self.ONE_data.item(i+1, j-1) / 16) + \
                             (self.ONE_data.item(i-1, j-0) / 8) + (self.ONE_data.item(i-0, j-0) / 4) + (self.ONE_data.item(i+1, j-0) / 8) + \
                             (self.ONE_data.item(i-1, j+1) / 16) + (self.ONE_data.item(i-0, j+1) / 8) + (self.ONE_data.item(i+1, j+1) / 16)

                        mr = (self.ONE_data.item(i-0, j-1) / 16) + (self.ONE_data.item(i+1, j-1) / 8) + (self.ONE_data.item(i+2, j-1) / 16) + \
                             (self.ONE_data.item(i-0, j-0) / 8) + (self.ONE_data.item(i+1, j-0) / 4) + (self.ONE_data.item(i+2, j-0) / 8) + \
                             (self.ONE_data.item(i-0, j+1) / 16) + (self.ONE_data.item(i+1, j+1) / 8) + (self.ONE_data.item(i+2, j+1) / 16)

                        bl = (self.ONE_data.item(i-2, j+0) / 16) + (self.ONE_data.item(i-1, j+0) / 8) + (self.ONE_data.item(i-0, j+0) / 16) + \
                             (self.ONE_data.item(i-2, j+1) / 8) + (self.ONE_data.item(i-1, j+1) / 4) + (self.ONE_data.item(i-0, j+1) / 8) + \
                             (self.ONE_data.item(i-2, j+2) / 16) + (self.ONE_data.item(i-1, j+2) / 8) + (self.ONE_data.item(i-0, j+2) / 16)

                        bc = (self.ONE_data.item(i-1, j+0) / 16) + (self.ONE_data.item(i-0, j+0) / 8) + (self.ONE_data.item(i+1, j+0) / 16) + \
                             (self.ONE_data.item(i-1, j+1) / 8) + (self.ONE_data.item(i-0, j+1) / 4) + (self.ONE_data.item(i+1, j+1) / 8) + \
                             (self.ONE_data.item(i-1, j+2) / 16) + (self.ONE_data.item(i-0, j+2) / 8) + (self.ONE_data.item(i+1, j+2) / 16)

                        br = (self.ONE_data.item(i-0, j+0) / 16) + (self.ONE_data.item(i+1, j+0) / 8) + (self.ONE_data.item(i+2, j+0) / 16) + \
                             (self.ONE_data.item(i-0, j+1) / 8) + (self.ONE_data.item(i+1, j+1) / 4) + (self.ONE_data.item(i+2, j+1) / 8) + \
                             (self.ONE_data.item(i-0, j+2) / 16) + (self.ONE_data.item(i+1, j+2) / 8) + (self.ONE_data.item(i+2, j+2) / 16)

                    else:
                        ul = self.ONE_data.item(i-1, j-1)
                        uc = self.ONE_data.item(i-0, j-1)
                        ur = self.ONE_data.item(i+1, j-1)
                        ml = self.ONE_data.item(i-1, j-0)
                        mc = self.ONE_data.item(i-0, j-0)
                        mr = self.ONE_data.item(i+1, j-0)
                        bl = self.ONE_data.item(i-1, j+1)
                        bc = self.ONE_data.item(i-0, j+1)
                        br = self.ONE_data.item(i+1, j+1)

                    v = (ul * -1) + (uc * 0) + (ur * 1) + \
                        (ml * -2) + (mc * 0) + (mr * 2) + \
                        (bl * -1) + (bc * 0) + (br * 1)

                    h = (ul * -1) + (uc * -2) + (ur * -1) + \
                        (ml * 0) + (mc * 0) + (mr * 0) + \
                        (bl * 1) + (bc * 2) + (br * 1)

                    self.edge_data.itemset((i-2,j-2), int(math.sqrt(v*v + h*h)))

            factor = abs(np.amax(self.edge_data)) + abs(np.amin(self.edge_data))
            self.edge_data = (self.edge_data - np.amin(self.edge_data)) / factor


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
        img = Image.fromarray(np.uint8(self.edge_data * 255), 'L')
        img.show()
