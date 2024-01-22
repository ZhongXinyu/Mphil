# compilers, flags and libraries 
CC = gcc-9
CFLAGS := -g -O3 -xHost 

# librarys
LIBS := 
    
# Directories code objects and librarys     
LIBDIR := lib

# source file(s) without suffix 
CFILES = ompexample

# dependany says wrap depends on all files in LIBDIR
# matching anything in CFILES but with 'lib' on the front and '.a' on the end
wrap : $(LIBDIR)/$(CFILES:%=lib%.a)
	python setup.py build_ext --inplace

# for anything in CFILES but with 'lib' on the front and '.a' on the end
# dependent on anything in CFILES with '.o' on the end
$(LIBDIR)/$(CFILES:%=lib%.a) : $(LIBDIR)/$(CFILES:%=%.o)
	ar rcs $@ $^

# everything that ends in '.o' should be made from the same file with '.c' instead
$(LIBDIR)/%.o : $(LIBDIR)/%.c
	$(CC) -c $< -o $@
    
clean : 
	rm *.c *.so $(LIBDIR)/*.a $(LIBDIR)/*.o