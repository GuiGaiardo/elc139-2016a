/*
 *  Exemplo de programa para calculo de produto escalar em paralelo, usando POSIX threads.
 *  andrea@inf.ufsm.br
 */

#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <time.h>

typedef struct 
 {
   double *a;
   double *b;
   double c; 
   int wsize;
   int repeat; 
 } dotdata_t;

// Variaveis globais, acessiveis por todas threads
dotdata_t dotdata;
pthread_mutex_t mutexsum;


/* 
 * Distribui o trabalho entre nthreads
 */
void dotprod_threads(int nthreads)
{
   int i, k;
   double *a = dotdata.a;
   double *b = dotdata.b;     
   double mysum;
   int end = nthreads * dotdata.wsize;

   #pragma omp parallel shared(a,b,end) private(i,k,mysum)
   {
      for (k = 0; k < dotdata.repeat; k++) {
         mysum = 0.0;
         #pragma omp for schedule(dynamic,dotdata.wsize)
         for (i = 0; i < end ; i++)  {
            mysum += (a[i] * b[i]);
         }
      }
      #pragma omp critical
         dotdata.c += mysum;
   }
}


/*
 * Tempo (wallclock) em microssegundos
 */ 
long wtime()
{
   struct timeval t;
   gettimeofday(&t, NULL);
   return t.tv_sec*1000000 + t.tv_usec;
}

/*
 * Preenche vetor
 */ 
void fill(double *a, int size, double value)
{  
   int i;
   for (i = 0; i < size; i++) {
      a[i] = value;
   }
}

/*
 * Funcao principal
 */ 
int main(int argc, char **argv)
{
   int nthreads, wsize, repeat;
   long start_time, end_time;

   if ((argc != 4)) {
      printf("Uso: %s <nthreads> <worksize> <repetitions>\n", argv[0]);
      exit(EXIT_FAILURE);
   }

   nthreads = atoi(argv[1]); 
   wsize = atoi(argv[2]);  // worksize = tamanho do vetor de cada thread
   repeat = atoi(argv[3]); // numero de repeticoes dos calculos (para aumentar carga)

   //Set OMP number of threads
   omp_set_num_threads(nthreads);
   

   // Cria vetores
   dotdata.a = (double *) malloc(wsize*nthreads*sizeof(double));
   fill(dotdata.a, wsize*nthreads, 0.01);
   dotdata.b = (double *) malloc(wsize*nthreads*sizeof(double));
   fill(dotdata.b, wsize*nthreads, 1.0);
   dotdata.c = 0.0;
   dotdata.wsize = wsize;
   dotdata.repeat = repeat;

   // Calcula c = a . b em nthreads, medindo o tempo
   start_time = wtime();
   dotprod_threads(nthreads);
   end_time = wtime();

   // Mostra resultado e estatisticas da execucao
   printf("%f\n", dotdata.c);
   printf("%d thread(s), %ld usec\n", nthreads, (long) (end_time - start_time));
   fflush(stdout);

   free(dotdata.a);
   free(dotdata.b);

   return EXIT_SUCCESS;
}

