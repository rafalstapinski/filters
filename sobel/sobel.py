from PIL import Image

class Open:

    def __init__(self, image_path):

        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.raw = self.image.load()
        self.data = [[None for x in range(self.width)] for y in range(self.height)]

    @staticmethod
    def luminosity(rgb):
        return (.21 * rgb[0]) + (.72 * rgb[1]) + (.07 * rgb[2])

    @staticmethod
    def average(rgb):
        return sum(rgb) / 3

    @staticmethod
    def lightness(rgb):
        return (max(rgb) + min(rgb)) / 2

    def grayscale(self, mode=None):

        if mode == None:
            mode = 'lum'

        if mode == 'lum':
            scale = self.luminosity
        elif mode == 'avg':
            scale = self.average
        elif mode == 'lht':
            scale = self.lightness
        else:
            pass
            # TODO: error handling

        for x in xrange(1, self.width - 1):
            for y in xrange(1, self.height - 1):
                self.data[x, y] = scale(self.raw[x ,y])
                print self.data[x, y]
