import numpy as np

a = np.arange(20)
a = a.reshape(2,2,5)
print a
print type(a)
print a.ndim
print a.shape,a.dtype,a.size

raw=[112,11,23,45,54]
a=np.array(raw)
print a

d = (4,5)
b=np.zeros(d,dtype=int)
print b

#0-1 random
print np.random.rand(2,4)