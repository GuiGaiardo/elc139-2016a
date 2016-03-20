#Implementacao em Python3 de um algoritmo para calcular o Produto Escalar (dot product) entre 2 vetores



import sys
import cProfile
import profile
import time


#tempo de CPU (melhor para precisão!)
def wtime():
	return time.process_time()



#Inicializa os vetores
def init_vectors(n):
	a = [0.5 for i in range(n)]
	b = [1.0 for i in range(n)]

	return a, b
	


#Calcula o produto escalar 1 ou mais vezes
def dot_product(a, b, n, repeat):
	for k in range(repeat):
		dot = 0.0
		for i in range(n):
			dot += a[i] * b[i]

	return dot


def main():
	n = int(sys.argv[1])
	repeat = int(sys.argv[2])


	a, b = init_vectors(n)

	start_time = wtime()
	dot = dot_product(a, b, n, repeat)
	end_time = wtime()

	print("Produto escalar: ", dot)
	print("Tempo de calculo:", (end_time - start_time)*1000000, "usec")





if(len(sys.argv) != 4):
		print("Uso: " +sys.argv[0] + " <tamanho dos vetores> <repeticoes> <profiler>\nProfilers: cProfile, profile")
		exit()


if(sys.argv[3] == 'cProfile'):
	cProfile.run('main()')

elif(sys.argv[3] == 'profile'):
	profile.run('main()')
else:
	print("ERRO! Profiler invalido.\nProfilers: cProfile, profile")