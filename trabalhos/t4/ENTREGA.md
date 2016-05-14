Disciplina: Programação Paralela (elc139-2016a)
Professora: Dra. Andrea Schwertner Charao
Aluno: Guilherme Gaiardo (Matrícula: 201210149)


###Equipamento utilizado:
O equipamento utilizado foi um Intel Core i3-4030U, o qual possui 2 núcleos com Hyperthreading habilitado (4 núcleos virtuais).

#Paralelizando o Algoritmo de Floyd-Warshall
A versão paralelizada do algoritmo está disponível na pasta floyd_paralelo/floyd_par.cpp.<br>
A unica mudança realizada no código foi de uma linha, para inserção da diretiva de paralelização. A linha em questão é a seguinte:

	(l.36)#pragma omp parallel for private(i,j,w)
	
No algoritmo são utilizados 3 laços 'for' aninhados. Os laços irão aplicar o algoritmo de Djikstra para descobrir o caminho mais curto do vértice i até o vértice j passando por um vértice intermediário k em todos os vértices do grafo.<br>
O laço paralelizado foi o 'for' do meio, pois desta forma o algoritmo só necessitará informações já disponíveis a respeito dos caminhos, visto que ele fará aproximações dos melhores caminhos a cada iteração do laço mais externo, que não é paralelizado. Deste fato decorre que não há necessidade de bloqueio entre as threads pois a propria forma como o algoritmo é paralelizado já é suficiente para garantir a coerência dos dados.

##Resultados
Os resultados obtidos são referentes a 5 execuções para cada parâmetro diferente.<br>
Os parâmetros variados foram o número de threads, 1, 2 e 4, e também o tamanho do grafo (N), que variou entre 500, 750 e 1500.

###Tabela 1- Tempos
|No. Threads|N=1500|N=500|N=750|
|-----------|------|-----|-----|
|1	|261.68	|9.64	|32.91	|
|2	|130.95	|4.83	|16.33	|
|4	|120.94	|4.46	|15.08	|

###Tabela 2- Speedups
|No. Threads|N=1500|N=500|N=750|
|-----------|------|-----|-----|
|1	|1.00	|1.00	|1.00	|
|2	|2.00	|2.00	|2.02	|
|4	|2.16	|2.16	|2.18	|

###Tabela 3- Eficiencias
|No. Threads|N=1500|N=500|N=750|
|-----------|------|-----|-----|
|1	|1.00	|1.00	|1.00	|
|2	|1.00	|1.00	|1.01	|
|4	|0.54	|0.54	|0.55	|