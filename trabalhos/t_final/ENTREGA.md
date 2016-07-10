Disciplina: Programação Paralela (elc139-2016a)
Professora: Dra. Andrea Schwertner Charao
Aluno: Guilherme Gaiardo (Matrícula: 201210149)

#Avaliando o módulo Multiprocess em python3 como interface de multithreading
Multiprocess é um módulo nativo de Python e fornece uma interface para execução de processos similar a API do módulo de Multithreading. O trabalho buscou fazer testes de performance com o módulo utilizando a chamada Pool.map para execução de um Produto Interno entre dois vetores de tamanhos variados.

##Produto Interno em Python com multiprocess.Pool
https://github.com/GuiGaiardo/elc139-2016a/blob/master/trabalhos/t_final/dot_prod.py
<br>O código em Python acima basicamente recebe 3 parâmetros como argumentos de chamada: o número de processos a serem utilizados na Pool, o tamanho do trabalho que cada processo executará (eg. tamanho de sua parte dos vetores a serem calculados) e o número de repetições da operação de cálculo do produto interno.<br>
O trecho de código que cada processo irá executar é exatamente a função (l.6)dot_prod.
<br>Os processos são instanciados na chamada
<br>(l.34) sums = pool.map(dot_prod, vecs)<br>
e posteriormente os resultados parciais são agregados em
<br>(l.37) dot = sum(n for n in sums)<br>
O tempo de alocação dos vetores é medido separadamente, e é < 0.5s em todos os casos testados, e por isso desconsiderado.

##Resultados
Os testes foram executados em um servidor com as seguintes características: (...)
Todos os tempos medidos são resultados da média de 5 execuções com 3000 repetições cada.

###Tabela 1- Tempos
|No. Process|vec_size=100000|vec_size=500000|vec_size=1000000|
|-----------|--------|--------|---------|
|1	|45.00	|222.92	|436.28	|
|2	|20.48	|109.67	|220.28	|
|4	|11.24	|57.56	|115.49	|
|8	|11.15	|52.95	|106.39	|

###Tabela 2- Variancias
|No. Process|vec_size=100000|vec_size=500000|vec_size=1000000|
|-----------|--------|--------|---------|
|1	|9.37	|21.33	|43.23	|
|2	|0.08	|2.42	|13.35	|
|4	|0.13	|1.02	|0.39	|
|8	|0.17	|0.29	|5.33	|

###Tabela 3- Speedups
|No. Process|vec_size=100000|vec_size=500000|vec_size=1000000|
|-----------|--------|--------|---------|
|1	|1.00	|1.00	|1.00	|
|2	|2.20	|2.03	|1.98	|
|4	|4.00	|3.87	|3.78	|
|8	|4.04	|4.21	|4.10	|

###Tabela 4- Eficiencias
|No. Process|vec_size=100000|vec_size=500000|vec_size=1000000|
|-----------|--------|--------|---------|
|1	|1.00	|1.00	|1.00	|
|2	|1.10	|1.02	|0.99	|
|4	|1.00	|0.97	|0.94	|
|8	|0.50	|0.53	|0.51	|

###Comentários
Os testes indicam um comportamento bastante linear até o máximo da capacidade física da máquina utilizada nos testes, que  possúi 4 núcleos com hyperthreading habilitado. As eficiências beiram o 1 e até mesmo no caso de 2 processos parecem superar o 1, porém é necessário mais testes para obter melhores estimativas em relação a este caso.
<br>Em todos os casos com apenas 1 processo a variância foi maior que nos casos com mais processos, o que pode indicar um certo nível de infidelidade nos dados de SpeedUp e Eficiência.
<br>Em geral o uso do multiprocess.Pool mostrou-se satisfatório em termos de eficiência, sendo comparável à eficiência observada em
<br>https://github.com/GuiGaiardo/elc139-2016a/blob/master/trabalhos/t3/<br>
onde são analisadas as APIs PThreads e OpenMP para paralelização do produto interno na linguagem C.
