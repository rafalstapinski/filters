from filters import sobel
import time

x = sobel.Sobel()

start_time = time.time()
x.open('a.png').edges()
x.show()
print 'fast normalize on %f' % (time.time() - start_time)

start_time = time.time()
x.open('a.png').edges(fast_normalize=False)
x.show()
print 'fast normalize off %f' % (time.time() - start_time)

start_time = time.time()
x.open('a.png').edges()
x.show()
print 'blur off %f' % (time.time() - start_time)

start_time = time.time()
x.open('a.png').edges(blur=True)
x.show()
print 'blur on %f' % (time.time() - start_time)
