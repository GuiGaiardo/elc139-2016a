#include <stdlib.h>
#include <stdio.h>
#include <omp.h>

<<<<<<< HEAD
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
=======
int prime_v1(int n);
int prime_v2(int n);
int prime_v3(int n);

int main(int argc, char *argv[])
{
  int n;
  int primes;
  double time1;
  double time2;
  double time3;

  n = 524288;

  printf("\n");
  printf("                                V1            V2            V3\n");
  printf("         N     Pi(N)          Time          Time          Time\n");
  printf("\n");


  time1 = omp_get_wtime();
  primes = prime_v1(n);
  time1 = omp_get_wtime() - time1;

  time2 = omp_get_wtime();
  primes = prime_v2(n);
  time2 = omp_get_wtime() - time2;
  
  time3 = omp_get_wtime();
  primes = prime_v3(n);
  time3 = omp_get_wtime() - time3;
  
  printf ("  %8d  %8d  %12f  %12f  %12f\n", n, primes, time1, time2, time3);
>>>>>>> upstream/master
  
  return 0;
}

/******************************************************************************/
<<<<<<< HEAD
int prime_seq(int n)
=======
int prime_v1(int n)
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

/******************************************************************************/
int prime_v2(int n)
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

/******************************************************************************/
int prime_v3(int n)
>>>>>>> upstream/master
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
<<<<<<< HEAD
}
=======
}


>>>>>>> upstream/master
