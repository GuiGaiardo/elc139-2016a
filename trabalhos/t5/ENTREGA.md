Disciplina: Programação Paralela (elc139-2016a)
Professora: Dra. Andrea Schwertner Charao
Aluno: Guilherme Gaiardo (Matrícula: 201210149)


##Equipamento utilizado:
O equipamento utilizado foi um Intel Core i3-4030U, o qual possui 2 núcleos com Hyperthreading habilitado (4 núcleos virtuais).


#Versões
Todas as versões foram palalizadas no laço for mais externo. Para as versões 2 e 3 é variado o Chunk Size, que determina a carga de trabalho que cada thread deve realizar.

##Chunk Size
O algoritmo irá se sair melhor ou pior de acordo com a distribuição de trabalho entre as threads, pois a quantia de loops realizados é proporcional ao número a ser testado, portanto se a quantia de trabalho for grande, as threads com os laços finais terão mais trabalho, ocasionando a sobrecarga e perda de eficiência.
Os tamanhos variam entre 1, 10, 1000 e 250000.

###Versão 1:
Na primeira versão a estrategia de paralelização foi a mais simples possível em OpenMP. Apenas foi inserida a diretiva "#pragma omp parallel for" e ficou a cargo da propria biblioteca escolher os parametros. Nesta versão o tamanho do trabalho não é explicitamente escolhido.
(Imagem de execução para N=750000 em 2 threads, em pics/primes1.png)

###Versão 2:
Na segunda versão a diretiva escolhida determina que o escalonamento é estático.
(Imagem de execução para N=750000 em 2 threads com chunk=1, em pics/primes2_1.png)

###Versão 3:
A diferença da terceira versão é que o escalonamento é dinâmico.
(Imagem de execução para N=500000 em 4 threads com chunk=250000, em pics/primes3_250k.png)

##Resumo dos resultados
Todos os tempos são o resultado da média de tempo de 5 medições.
O arquivo tables.md contém todas as tabelas de Tempos, Speedups e Eficiências.

###N = 500000


O tempo sequencial foi de 47.32s.
As melhores versões com 2 threads foram as versões 2 e 3 com chunk = 10 e tiveram eficiência de 82%.
A pior versão com 2 threads foi a versão 2 com chunk = 1 e teve eficiência de 43%.
A melhor versão com 4 threads foi a versão 2 com chunk = 100 e teve eficiência de 54%.
A pior versão com 4 threads foi a versão 3 com chunk = 250000 e teve eficiência de 27%.

###N = 750000
O tempo sequencial foi de 102.87.
A melhor versão com 2 threads foi a versão 2 com chunk = 10 e 100 e tiveram eficiência de 83%.
A pior versão com 2 threads foi a versão 2 com chunk = 1 e teve eficiência de 43%.
A melhor versão com 4 threads foi a versão 2 com chunk = 10 e 100 e tiveram eficiência de 54%.
A pior versão com 4 threads foi a versão 2 com chunk = 1 e teve eficiência de 27%.

###N = 1000000
O tempo sequencial foi de 179.20.
A melhor versão com 2 threads foi a versão 2 com chunk = 10 e teve eficiência de 83%.
A pior versão com 2 threads foi a versão 2 com chunk = 1 e teve eficiência de 43%.
A melhor versão com 4 threads foi a versão 2 com chunk = 100 e 100 e tiveram eficiência de 54%.
A pior versão com 4 threads foi a versão 2 com chunk = 1 e teve eficiência de 30%.