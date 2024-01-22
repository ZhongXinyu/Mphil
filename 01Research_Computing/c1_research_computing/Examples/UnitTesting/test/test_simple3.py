from src import simple 

def test_perm_factor():
    """
        Test perm_factor
    """
    assert( simple.perm_factor(1,1,1)==1)
    assert( simple.perm_factor(1,1,2)==3)
    assert( simple.perm_factor(1,2,1)==3)
    assert( simple.perm_factor(2,1,1)==3)
    assert( simple.perm_factor(1,2,3)==6)