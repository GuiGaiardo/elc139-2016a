#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

int prime_seq(int n);

int main(int argc, char *argv[])
{
  int n, primes;
  double time1;

  if (argc != 2){
  	printf("Uso: %s <N_MAX>\n", argv[0]);
  	exit(EXIT_FAILURE);
  }
  n = atoi(argv[1]);

  time1 = omp_get_wtime();
  primes = prime_seq(n);
  time1 = omp_get_wtime() - time1;

  printf ("\nTime: %12f", time1);
  
  return 0;
}

/******************************************************************************/
int prime_seq(int n)
/******************************************************************************/
{
  int i;
  int j;
  int prime;
  int total = 0;

  for (i = 2; i <= n; i++)
  {
    prime = 1;
    for (j = 2; j < i; j++)
    {
      if (i % j == 0)
      {
        prime = 0;
        break;
      }
    }
    total = total + prime;
  }
  return total;
}