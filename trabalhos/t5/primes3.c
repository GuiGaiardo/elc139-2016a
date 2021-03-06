#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

int prime_v3(int n, int chunk_size);

int main(int argc, char *argv[])
{
  int n, chunk_size, nthreads;
  int primes;
  double init_time, run_time;

  if (argc != 4){
  printf("Uso: %s <n_threads> <N_MAX> <chunk size>\n", argv[0]);
  exit(EXIT_FAILURE);
  }
  n = atoi(argv[2]);
  chunk_size = atoi(argv[3]);

  nthreads = atoi(argv[1]);
  omp_set_num_threads(nthreads);

  init_time = omp_get_wtime();
  primes = prime_v3(n, chunk_size);
  run_time = omp_get_wtime() - init_time;
  
  printf ("\nTime: %12f", run_time);
  
  return 0;
}

/******************************************************************************/
int prime_v3(int n, int chunk_size)
/******************************************************************************/
{
  int i;
  int j;
  int prime;
  int total = 0;

  #pragma omp parallel for private(j, prime) schedule(dynamic, chunk_size)
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
    #pragma omp critical
    total = total + prime;
  }
  return total;
}