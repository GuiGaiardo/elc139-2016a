Disciplina: Programação Paralela (elc139-2016a)
Professora: Dra. Andrea Schwertner Charao
Aluno: Guilherme Gaiardo (Matrícula: 201210149)

Parte 1: Profiling do 'dotprod_seq'
	A) O perfil é afetado pelas opções de configuração?
		Sim, bastante. Rodando N configurações diferentes, obtemos resultados significativamente diferentes.

		Index 	Config 			Tempo 	(tempo automedido)
		[1]		"3000 10": 		0.00s 	(381usec)
		[2]		"3000 50": 		0.00s 	(1929usec)
		[3]		"3000 100": 	0.00s 	(3798usec)
		[4]		"300000 10":	0.01s 	(18315usec)
		[5]		"300000 50":	0.11s 	(107926usec)
		[6]		"300000 100":	0.16s 	(170587usec)	
		[7]		"30000000 10":	1.98s 	(1664306usec)
		[8]		"30000000 50":	8.92s 	(8582102usec)
		[9]		"30000000 100":	17.30s 	(16937012usec)

		Para as configurações [1], [2] e [3] o gprof não mostrou tempos (tempo < 0.01s), apenas contagem de chamadas às funções.
		Até a configuração [6] o tempo da função 'init_vectors' era desprezível (<0.01s)
		Para a configuração [7] a função 'init_vectors' ocupou 15.33% (0.30s) do tempo.
		Para a configuração [8] a função 'init_vectors' ocupou 3.64% (0.32s) do tempo.
		Para a configuração [9] a função 'init_vectors' ocupou 1.88% (0.32s) do tempo.
		Para todas as configurãções a função 'wtime' possui tempo desprezível.

	B) Sim. A função 'dot_product' ocupa a maior parte do tempo de execução para todas as configurações, podendo ser uma possível candidata a paralelização, supondo ser possível a paralelização da mesma.


Parte 2: Profiling do dot_product em python 3
	Nota) Levando em conta que o algoritmo em C coletava o tempo decorrido no sistema, e não somente tempo de CPU, preferi utilizar uma metrica diferente na reimplementação, para avaliar somente o tempo passado em CPU.

	A)cProfile e profile.
		São dois módulos nativos em Python que possibilitam realizar o profiling de uma função. Os módulos são semelhantes e mostram, basicamente: Número de chamadas a uma determinada função, tempo total da função, tempo por chamada, tempo acumulado e tempo acumulado por chamada.
		A principal diferença entre os módulos é que o 'cProfile' é uma extensão em C e possui overhead menor do que o 'profile'. Já o 'profile' possuio um overhead maior, porém é um módulo em Python puro, o que facilita no trabalho de extensão de suas ferramentas.

	B)Realizando os testes para as mesmas configurações os resultados são:
		
		B.1) Com o 'profile'
		Index 	Config 			Tempo 	(tempo automedido)
		[1]		"3000 10": 		0.006s 	(5943usec)
		[2]		"3000 50": 		0.028s 	(27732usec)
		[3]		"3000 100": 	0.045s 	(44459usec)
		[4]		"300000 10":	0.459s 	(424582usec)
		[5]		"300000 50":	2.204s 	(2170986usec)
		[6]		"300000 100":	4.181s 	(4150874usec)
		[7]		"30000000 10":	49.225s	(46492604usec)
		[8]		"30000000 50":	217.561s(214832117usec)
		[9]		"30000000 100":	428.052s(425211164usec)


		B.2) Com o 'cProfile'
		Index 	Config 			Tempo 	(tempo automedido)
		[10]	"3000 10": 		0.004s 	(4051usec)
		[11]	"3000 50": 		0.021s 	(20897usec)
		[12]	"3000 100": 	0.041s 	(40637usec)
		[13]	"300000 10":	0.446s 	(410478usec)
		[14]	"300000 50":	2.075s 	(2046507usec)
		[15]	"300000 100":	4.169s 	(4114988usec)
		[16]	"30000000 10":	46.198s	(43309620usec)
		[17]	"30000000 50":	221.417s(218409014usec)
		[18]	"30000000 100":	436.154s(432986279usec)

		A coluna Tempo se refere ao tempo indicado na medição da chamada da função 'main()' e é indicada pelo profiler.
		A coluna tempo automedido se refere à medição de tempo de CPU feita no proprio programa (chamada da função dot_product()).
		É possível notar que os tempos não tiveram uma variação muito significativa comparando os resultados dos dois profilers.
		Para as configurações [4], [5], [6], [13], [14], [15] o tempo da função 'init_vectors' variou entre 0.027s e 0.036s.
		Para as configurações [7], [8], [9], [16], [17], [18] o tempo da funçãoo 'init_vectors' variou entre 2.72s e 2.85s.
		Em todos os casos a função 'dot_product()' ocupa a maior parte do tempo, sendo a principal candidata a uma possível estratégia de paralelização.





Referências:
Python 3 documentation. https://docs.python.org/3/library/profile.html