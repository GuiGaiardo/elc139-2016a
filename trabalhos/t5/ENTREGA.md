Disciplina: Programação Paralela (elc139-2016a)
Professora: Dra. Andrea Schwertner Charao
Aluno: Guilherme Gaiardo (Matrícula: 201210149)


##Equipamento utilizado:
O equipamento utilizado foi um Intel Core i3-4030U, o qual possui 2 núcleos com Hyperthreading habilitado (4 núcleos virtuais).


#Versões
Todas as versões foram palalizadas no laço for mais externo. Para as versões 2 e 3 é variado o Chunk Size, que determina a carga de trabalho que cada thread deve realizar.

##Chunk Size
O algoritmo irá se sair melhor ou pior de acordo com a distribuição de trabalho entre as threads, pois a quantia de loops realizados é proporcional ao número a ser testado, portanto se a quantia de trabalho for grande, os laços finais serão muito grandes, e portanto, mal distribuídos entre as threads ocasionando a sobrecarga e perda de eficiência.
Os tamanhos variam entre 1, 10, 100 e 1000.

###Versão 1:
Na primeira versão a estrategia de paralelização foi a mais simples possível em OpenMP. Apenas foi inserida a diretiva "#pragma omp parallel for" e ficou a cargo da propria biblioteca escolher os parametros. Nesta versão o tamanho do trabalho não é explicitamente escolhido.

###Versão 2:
Na segunda versão a diretiva escolhida determina que o escalonamento é estático.

###Versão 3:
A diferença da terceira versão é que o escalonamento é dinâmico.

##Resultados
###N = 500000
O tempo sequencial foi de ?????.
A melhor versão com 2 threads foi a versão 2 com chunk = 1000.
A pior versão com 2 threads foi a versão 2 com chunk = 1.
A melhor versão com 4 threads foi a versão 2 com chunk = 10.
A pior versão com 4 threads foi a versão 2 com chunk = 1.

###N = 750000
O tempo sequencial foi de ?????.
A melhor versão com 2 threads foi a versão 2 com chunk = 1000.
A pior versão com 2 threads foi a versão 2 com chunk = 1.
A melhor versão com 4 threads foi a versão 2 com chunk = 10.
A pior versão com 4 threads foi a versão 2 com chunk = 1.

###N = 1000000