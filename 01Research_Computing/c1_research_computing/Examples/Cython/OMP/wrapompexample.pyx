cdef extern from "ompexample.h":
    int pointlesssum(int n)

def ompsum(n):
    cdef m
    m = pointlesssum(n)
    return m