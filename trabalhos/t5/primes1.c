#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

int prime_v1(int n);

int main(int argc, char *argv[])
{
  int n, nthreads;
  int primes;
  double init_time, run_time;

  if (argc != 3){
	printf("Uso: %s <n_threads> <N_MAX>\n", argv[0]);
	exit(EXIT_FAILURE);
  }
  n = atoi(argv[2]);
  nthreads = atoi(argv[1]);

  omp_set_num_threads(nthreads);


  init_time = omp_get_wtime();
  primes = prime_v1(n);
  run_time = omp_get_wtime() - init_time;
  
  printf ("\nTime: %12f", run_time);
  
  return 0;
}

/******************************************************************************/
int prime_v1(int n)
/******************************************************************************/
{
  int i;
  int j;
  int prime;
  int total = 0;

  #pragma omp parallel for private(j,prime)
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
    #pragma omp atomic
    total = total + prime;
  }
  return total;
}