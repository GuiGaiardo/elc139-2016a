#include <omp.h>
#include <stdio.h>

int main() 
{
	int i = 1;
	#pragma omp parallel
  	printf("Hello World%d\n", i);
	return 0;
}

