#Author: Guilherme Gaiardo
#Description: Script para rodar o dotprod com diferentes parametros

from subprocess import *
import sys


def get_media(times):
	total=0
	for time in times:
		total += time/1000000	#converte para segundos
	return total/len(times)

############################################
#Parametros que serão variados entre as execuções
n_threads=[1,2,4]
vector_size=[100000,500000,1000000]
repetitions=[1000,2000,3000]
############################################





if (len(sys.argv) != 2):
	print("Usage: $python3 run_dotprod.py path_to_executable")
	print("Example1: $python3 run_dotprod.py ./openmp/omp_dotprod")
	print("Example2: $python3 run_dotprod.py ./pthreads_dotprod/pthreads_dotprod")
	exit()

exec_path = sys.argv[1]

for size in vector_size:
	for repetition in repetitions:
		for threads in n_threads:
			cmd = exec_path + " " + str(threads) + " " + str(size/threads) + " " + str(repetition)
			times = []
			media = 0
			for i in range(5):	#executa 5 vezes cada comando para tirar a media
				exe = Popen(cmd, shell=True, stdout=PIPE)
				(saida, erro) = exe.communicate()	#espera até finalizar o dotprod
				saida = saida.decode()
				time = saida.split()[3]
				times.append(int(time))	#pega o tempo de execução: decodifica a saida para string e converte-a em inteiro
			media = get_media(times)
			print("\n\nMedia do tempo de execucao para " + cmd + "\n" + str(media))