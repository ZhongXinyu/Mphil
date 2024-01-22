from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

ompexample_extension = Extension(
    name="wrapompexample",            
    sources=["wrapompexample.pyx"],
    libraries=["ompexample"],
    library_dirs=["lib"],
    include_dirs=["lib"]
)

setup(
    name="wrapompexample",
    ext_modules=cythonize([ompexample_extension])
)