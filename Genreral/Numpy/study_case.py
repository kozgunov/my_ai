import numpy as np
import random

# Broadcasting

a = np.array([1,2,3])
b = np.array([10])

#print(a+b) # 1+10, 2+10, 3+10

c = np.array([1,2,3])
d = np.array([[100], [3000]])

#print(c+d) # 100 + 1,  100 + 2, ... 3000 + 3

e = np.array([100, 3000])
f = np.array([1,2,3])

#print(c+d)  # this is incompatible

g = np.random.random((1,2,1,10,8,1,3))
h = np.random.random((10,2,5,1,1,7,3))

#print(h+g)  # this is compatible, because 1. size is the same, 2. addition is possible: either 1-to-any_number or N-to-N
#print((h+g).shape) # show the obtained shape: (10,2,5,10,8,7,3)

# Indexing

aa = np.array([[1,2,3],[4,5,6],[7,8,9]])

#print(aa[0:4]) # simple operations as with arrays
#print(aa[-1])
#print(aa[:])
#print(aa[-1])
#print(aa[(0,1)]) # [1,2,3] -> 2
#print(aa[[0,2]]) # [1,2,3] & [7,8,9]
#print(aa[:,1]) # [2,5,8]
#print(aa[1,:]) # [4,5,6]

#print(aa[:,1, np.newaxis]) # vertical axis
#print(aa[np.newaxis,:,1]) # horizontal axis

#print(aa[:,[0,2]]) # [[1 3] \n [4 6] \n [7 9]]
#print(aa[[1,2],[0,1]]) # come up with [1,0](i.e. 4) and [2,1](i.e. 8)

#print(aa[[True, False, True]]) # True=take the line, False=not



#  Sorting&Searching

bb = np.array([[5,3,2],[4,9,4],[1,0,5]])
#bb.sort()
#print(bb) # assign bb as sorted

#np.sort(bb, axis=0)
#print(bb)  # nothing changed (because it didn't assigned bb)
#print(np.sort(bb, axis=0)) # [5,...], [4,...], [1,...] -> [1,4,5]
#print(np.sort(bb, axis=1)) # [5,3,2] -> [2,3,5]

#print(np.sort(bb.flatten()).reshape(aa.shape))  # sort the whole array in given 3x3 shape(as in aa)

outputs = np.array([0.01, 0.02, 0.89, 0.05, 0, 0.04])

#print(np.argmax(outputs))
#print(outputs[np.argmax(outputs)]) # simulate classification problems of  the models
#print(np.argmin(outputs))
#print(outputs[np.argmin(outputs)])

#print(np.where(outputs >= 0.04, outputs, 0)) # all number lower than 0.04 becomes 0



# iterating


cc = np.arange(12).reshape(3,4) # your shape of elements

#print(cc)

for element in np.nditer(cc, op_flags=['readwrite']): # shows all elements in a row; order='F' - vertical; ='C' - horizontal; op_flags... is about editing
    element[...]= element ** 2 # here it will square all the numbers
#print(cc, end=' ')



# Masking
import numpy.ma as ma

dd = np.array([1,2,3,np.nan, 20, np.inf])
masked_dd = ma.masked_array(dd, mask=[0,0,0,1,0,1]) # 0 - with us, non-zero - don't count or nothing

#print(masked_dd.mean()) # shows mean value of array under the mask

arr = np.array([[1,2,3],[4,-2,0]])
masked_arr = ma.masked_array(arr, mask=[[0,0,0],[0,0,1]]) # mask satisfies to arr's dim
#print(masked_arr.mean())
#print(ma.getmask(masked_arr)) # get mask
#print(ma.getdata(masked_arr)) # get data
#print(ma.masked_greater(masked_arr, 2)) # greater = --, lower value exists
#print(ma.masked_inside(masked_arr, 2,4)) # inside = --, outside = save
#print(ma.masked_outside(masked_arr, 2,4)) # outside = --, inside = save
#print(ma.masked_where(arr % 2 == 0, arr)) # is  indivisible by 2
#print(ma.masked_invalid(masked_arr)) # shows who is under the mask



#Views & Copies



ee = np.array([1,2,3,4,5])

new_ee = ee.copy() # new_ee = ee as in usual usage
new_ee = ee[0:3] # renew the array  - it's another "view" on the same data.  when we  change new_ee, then origins also be changed
#print(new_ee[0:2].base) #  base shows the origin





# Vectorization



gg = np.array([[1,2,3],[4,5,6],[7,8,9]])

def square_if_even(x):
    if x % 2 == 0:
        return x**2
    else:
        return x

vectorize_square_if_even = np.vectorize(square_if_even)
#print(vectorize_square_if_even(gg))


#print(np.matmul(bb, gg)) # multiplication of 2 matrices
#print(bb @ gg) # the same




# Custom data type




hh =  np.array([1,2.2,3, {'key':'value'}])
#print(hh.dtype)


dt = np.dtype('U10')

new_arr = np.array(['hellooooooooooooooooooo', 'world', 'sth', 'soon', 888888888888888888888888888888888888], dtype=dt) # regularization by size

#print(new_arr)
#print(new_arr.dtype)

dt = np.dtype('i4,  (2,3)f8, f4')
another_arr = np.array([[22,24,55],[1,3444,556],[1,2,3]])
#print(another_arr)
#print(another_arr.dtype)
another_arr = np.array([[22,24,55],[1,3444,556],[1,2,3]], dtype=dt) # assign data type manually
print(another_arr)
print(another_arr.dtype)




