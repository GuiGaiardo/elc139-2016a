Disciplina: Programação Paralela (elc139-2016a)
Professora: Dra. Andrea Schwertner Charao
Aluno: Guilherme Gaiardo (Matrícula: 201210149)


##Ray Trace com MPI
https://github.com/GuiGaiardo/elc139-2016a/blob/master/trabalhos/t6/ray.cpp

Para gerar a imagem em paralelo ela é dividida em N faixas horizontais, sendo que cada processo (exceto o mestre) é responsável pelo processamento de uma destas faixas.
O tempo é medido pelo mestre com a função gettimeofday() da biblioteca time.h em quatro momentos: ao inicio e ao fim dos recebimentos das partes calculadas pelos processos e também ao inicio e ao fim da escrita do arquivo com a imagem.


#Resultados

##Cluster da Amazon
Características: 3 nós virtuais do tipo t2.micro (1Gb memória, 1CPU virtual). Mais detalhes em https://aws.amazon.com/ec2/details/

###Tabela 1- Tempos
|No. Process|Level=2|Level=10|Level=6|
|-----------|---|----|---|
|2	|18.23	|250.25	|115.82	|
|4	|12.91	|193.13	|160.88	|
|7	|7.38	|69.51	|67.04	|
|10	|4.32	|41.41	|30.43	|
|12	|3.61	|34.18	|24.30	|

###Tabela 2- Speedups
|No. Process|Level=2|Level=10|Level=6|
|-----------|---|----|---|
|2	|1.00	|1.00	|1.00	|
|4	|1.41	|1.30	|0.72	|
|7	|2.47	|3.60	|1.73	|
|10	|4.23	|6.04	|3.81	|
|12	|5.05	|7.32	|4.77	|

###Tabela 3- Eficiencias
|No. Process|Level=2|Level=10|Level=6|
|-----------|---|----|---|
|2	|1.00	|1.00	|1.00	|
|4	|0.47	|0.43	|0.24	|
|7	|0.41	|0.60	|0.29	|
|10	|0.47	|0.67	|0.42	|
|12	|0.46	|0.67	|0.43	|

###Comentários
Os resultados podem ser inconsistentes pois são a média de 3 execuções e foram observados picos bastante fora da média durante testes (em level=6 com 2 e 4 processos), possivelmente devido as características do ambiente pouco controlado onde foram executados os testes. Em geral os tempos foram bem comportados com mais processos proporcionando speedups maiores. No caso da imagem mais complexa (level=10) as eficiências para 10 e 12 processos foram semelhantes, sendo com 12 processos de 0.67 (speedup de 7.32).


##Servidor no LSC
Características: ?


###Tabela 1- Tempos
|No. Process|Level=2|Level=10|Level=6|
|-----------|---|----|---|
|2	|1.19	|6.65	|5.09	|
|3	|0.68	|4.63	|3.05	|
|4	|0.49	|3.34	|2.63	|
|7	|0.41	|3.68	|2.26	|
|10	|0.39	|3.20	|2.10	|
|12	|0.36	|3.39	|1.93	|

###Tabela 2- Speedups
|No. Process|Level=2|Level=10|Level=6|
|-----------|---|----|---|
|2	|1.00	|1.00	|1.00	|
|3	|1.75	|1.44	|1.67	|
|4	|2.41	|1.99	|1.94	|
|7	|2.88	|1.81	|2.25	|
|10	|3.07	|2.08	|2.42	|
|12	|3.29	|1.96	|2.64	|

###Tabela 3- Eficiencias
|No. Process|Level=2|Level=10|Level=6|
|-----------|---|----|---|
|2	|1.00	|1.00	|1.00	|
|3	|0.87	|0.72	|0.83	|
|4	|0.80	|0.66	|0.65	|
|7	|0.48	|0.30	|0.38	|
|10	|0.34	|0.23	|0.27	|
|12	|0.30	|0.18	|0.24	|

###Comentários
Em geral os resultados apontam um comportamento estável, com mais processos melhorando o desempenho, porém não de forma linear. Os casos aparte foram o da imagem mais complexa (level=10), a versão com 4 processos teve um desempenho melhor do que a versão com 7 processos, o mesmo ocorreu com 10 processos em relação a 12.
