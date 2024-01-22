cdef extern from "cexample.h":
    int fibonacci(int n)

def cfib(n):
    cdef m
    m = fibonacci(n)
    return m