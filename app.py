from filters import sobel

x = sobel.Sobel()

x.open('a.png').edges()
x.show()
x.open('b.png').edges()
x.show()
x.open('c.png').edges()
x.show()
