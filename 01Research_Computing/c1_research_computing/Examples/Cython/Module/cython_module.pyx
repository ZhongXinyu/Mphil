"""
Cython code for fibonnaci numbers
"""
cpdef int fibonacci(int N):
    cdef int i
    cdef int a=0,b=1
    for i in range(N):
        a,b = b,a+b
    return a