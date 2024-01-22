#include "ompexample.h"
#include <omp.h>

int pointlesssum(int n){
	
	int i,sum;
	sum = 0;
	
	#pragma omp parallel for deafult(none) private(i) shared(n) reduction(+:sum)
	for(i=0;i<n;i++){
		sum += i;
	}
	return sum;
}