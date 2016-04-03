Disciplina: Programação Paralela (elc139-2016a)
Professora: Dra. Andrea Schwertner Charao
Aluno: Guilherme Gaiardo (Matrícula: 201210149)

# Parte I: Pthreads
## A)
As etapas de particionamento de aglomeração são implementadas em conjunto. Ainda que seja possível particionar o produto interno dos dois vetores de tamanho N em N partes, isso não necessariamente resultaria em speedup, pois seriam necessários N núcleos para tirar proveito disso. Como resultado, as operações são aglomeradas conforme o número de threads a serem utilizadas na execução.
Agloremação definida como worksize (parametro passado para a execução):

	(l.123)dotdata.wsize = wsize;

A comunicação é feita em apenas um momento, quando o somatorio parcial de cada thread é adicionado em dodata.c.
	(l.45)pthread_mutex_lock (&mutexsum);
	(l.46)dotdata.c += mysum;
	(l.47)pthread_mutex_unlock (&mutexsum);

O mapeamento é feito pelo SO, nenhuma thread é mapeada diretamente à algum núcleo. Apenas são iniciadas as threads com um trecho de código e o SO é responsável por escalonalas.
	for (i = 0; i < nthreads; i++)
		pthread_create(&threads[i], &attr, dotprod_worker, (void *) i);

## B)
O speedup de 1 thread para 2 threads foi de aproximadamente 2.

## D)
Tabelas de speedup conforme variações nos parâmetros. (Tempo é o tempo médio de 5 execuções, calculados via script run_dotprod.py).

###Tabela 1- Tamanho Vetor=100000
|No. Threads|Repetições	|Tempo(s)	|speedup	|Eficiencia(%)	|
|-----------|-----------|-----------|-----------|---------------|
|1		 	|1000		|0.53	 	|1			|100			|
|2			|1000		|0.26	 	|2.03		|100			|
|4			|1000		|0.21		|2.52		|63				|
|1			|2000		|1.06		|1			|100			|
|2			|2000		|0.53		|2			|100			|
|4			|2000		|0.42		|2.52		|63				|
|1			|3000		|1.59		|1			|100			|
|2			|3000		|0.79		|2.01		|100			|
|4			|3000		|0.63		|2.52		|63				|

###Tabela 2- Tamanho Vetor=500000
|No. Threads|Repetições	|Tempo(s)	|speedup	|Eficiencia(%)	|
|-----------|-----------|-----------|-----------|---------------|
|1		 	|1000		|2.77	 	|1			|100			|
|2			|1000		|1.36	 	|2.03		|100			|
|4			|1000		|1.08		|2.56		|64				|
|1			|2000		|5.55		|1			|100			|
|2			|2000		|2.74		|2.02		|100			|
|4			|2000		|2.15		|2.58		|64				|
|1			|3000		|8.37		|1			|100			|
|2			|3000		|4.09		|2.04		|100			|
|4			|3000		|3.43		|2.44		|61				|

###Tabela 3- Tamanho Vetor=1000000
|No. Threads|Repetições	|Tempo(s)	|speedup	|Eficiencia(%)	|
|-----------|-----------|-----------|-----------|---------------|
|1		 	|1000		|5.68	 	|1			|100			|
|2			|1000		|2.83	 	|2			|100			|
|4			|1000		|2.18		|2.60		|65				|
|1			|2000		|11.15		|1			|100			|
|2			|2000		|5.65		|1.97		|98				|
|4			|2000		|4.35		|2.56		|64				|
|1			|3000		|16.7		|1			|100			|
|2			|3000		|8.48		|1.96		|98				|
|4			|3000		|6.55		|2.54		|63				|

## E) A diferença entre um e outro é a seguinte:
		(l.45)pthread_mutex_lock (&mutexsum);
   		(l.46)dotdata.c += mysum;
   		(l.47)pthread_mutex_unlock (&mutexsum);
Sem o mutex o código está errado, pois pode chegar ao resultado errado em função de condições de corrida.


#Parte II: OpenMP
##A)
A implementação encontra-se em ./openmp/omp_dotprod.c e seu executável em ./openmp/omp_dotprod.

##B)
Tabelas de speedup conforme variação nos parâmetros.

###Tabela 4- Tamanho Vetor=100000
|No. Threads|Repetições	|Tempo(s)	|speedup	|Eficiencia(%)	|
|-----------|-----------|-----------|-----------|---------------|
|1		 	|1000		|0.53	 	|1			|100			|
|2			|1000		|0.27	 	|1.96		|98				|
|4			|1000		|0.22		|2.40		|60				|
|1			|2000		|1.07		|1			|100			|
|2			|2000		|0.54		|1.98		|99 			|
|4			|2000		|0.44		|2.43		|60				|
|1			|3000		|1.60		|1			|100			|
|2			|3000		|0.81		|1.97		|98				|
|4			|3000		|0.66		|2.42		|60				|

###Tabela 5- Tamanho Vetor=500000
|No. Threads|Repetições	|Tempo(s)	|speedup	|Eficiencia(%)	|
|-----------|-----------|-----------|-----------|---------------|
|1		 	|1000		|2.87	 	|1			|100			|
|2			|1000		|1.47	 	|1.95		|97				|
|4			|1000		|1.22		|2.35		|58				|
|1			|2000		|5.63		|1			|100			|
|2			|2000		|2.86		|1.96		|98				|
|4			|2000		|2.43		|2.31		|57				|
|1			|3000		|8.44		|1			|100			|
|2			|3000		|4.31		|1.95		|97 			|
|4			|3000		|3.83		|2.20		|55				|

###Tabela 6- Tamanho Vetor=1000000
|No. Threads|Repetições	|Tempo(s)	|speedup	|Eficiencia(%)	|
|-----------|-----------|-----------|-----------|---------------|
|1		 	|1000		|5.63	 	|1			|100			|
|2			|1000		|2.91	 	|1.93		|96				|
|4			|1000		|2.43		|2.35		|57				|
|1			|2000		|11.16		|1			|100			|
|2			|2000		|5.97		|1.86		|93				|
|4			|2000		|5.04		|2.21		|55				|
|1			|3000		|17.26		|1			|100			|
|2			|3000		|8.78		|1.96		|98 			|
|4			|3000		|7.33		|2.35		|58				|

Em comparação com Posix Threads, OpenMP tem um desempenho levemente menor para todos os parâmetros testados.
