MODULE funcs
  
  CONTAINS
    
  SUBROUTINE fibonacci(n,m)
    IMPLICIT none
    INTEGER, INTENT(in) :: n
    INTEGER, INTENT(out) :: m
    INTEGER :: i,a,b,tmp
    a = 0
    b = 1
    DO i=1,n
      tmp = a+b
      a = b
      b = tmp
    END DO
    m = b
  END SUBROUTINE fibonacci
  
END MODULE funcs