#include "cexample.h"

int fibonacci(int n){
	
	int i,a,b,tmp;
	a=0;
	b=1;
	for (i=0;i<(n-1);i++){
		tmp = a+b;
		a = b;
		b = tmp;
	}
	return b;
}