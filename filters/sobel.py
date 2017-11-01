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


    @staticmethod
    def _luminosity(r, g, b):
        return (.21 * r) + (.72 * g) + (.07 * b)


    @staticmethod
    def __average__(r, g, b):
        return (r + g + b) / 3


    @staticmethod
    def _lightness(r, g, b):
        return (max((r, g, b)) + min((r, g, b))) / 2


    def _channel(self, channel):
        for j in xrange(0 , self.width):
            for i in xrange(0 , self.height):
                self.ONE_data.itemset((i, j), self.RGB_data.item(i, j, channel))


    def _set_channel(self, channel, comp):

        if channel == 'L':
            if comp == 'luminosity':
                c = self._luminosity
            elif comp == 'average':
                c = self.__average
            elif comp == 'lightness':
                c = self._lightness
            else:
                raise ValueError('Invalid Luminosity calc method specified. ')

            for j in xrange(0, self.width):
                for i in xrange(0, self.height):
                    self.ONE_data.itemset((i, j), c(self.RGB_data.item(i, j, 0),
                                                    self.RGB_data.item(i, j, 1),
                                                    self.RGB_data.item(i, j, 2)))

        elif channel == 'R':
            self._channel(0)

        elif channel == 'G':
            self._channel(1)

        elif channel == 'B':
            self._channel(2)

        else:
            raise ValueError('Invalid channel provided. ')






    def edges(self, channel='L', comp='luminosity', blur=False,
            vk=[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
            hk=[[-1, -2, -1], [0, 0, 0], [1, 2, 1]], fast_normalize=True):

            # TODO: check for square kernels

            self._set_channel(channel, comp)

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

            if fast_normalize:
                amax = 255 * 4
                amin = 0
            else:
                amax = np.amax(self.edge_data)
                amin = np.amin(self.edge_data)

            factor = abs(amax) + abs(amin)
            self.edge_data = (self.edge_data - np.amin(self.edge_data)) / factor

    def show(self):
        img = Image.fromarray(np.uint8(self.edge_data * 255), 'L')
        img.show()
