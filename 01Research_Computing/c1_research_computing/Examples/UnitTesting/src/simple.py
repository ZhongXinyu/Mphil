def addtwo(x):
    """
        Add 2 to x
    """
    return x+1

def add02(x):
    """
        Add 0.3 to x
    """
    return x+0.2

def test_addtwo_inside():
    """
        Test addtwo
    """
    assert( addtwo(3)==5)

def perm_factor(i,j,k):
    if (i==j):
        if (j==k):
            factor = 1
        else:
            factor = 3
    else:
        if (j==k):
            factor = 3
        # elif (i==k):
        #     factor = 3
        else:
            factor = 6
    
    return factor



x = 7

y = addtwo(x)

print(y)
