#Author: Guilherme Gaiardo
#Description: Script para rodar o 'primes' com diferentes parametros

from subprocess import *
import json
import sys

#Tabajara(R)
class estatisticator9001:
	#Its over 9000!
	def __init__(self, ns, n_threads):
		self.times = {}
		self.speedups = {}
		self.efficiencies = {}

		self.n_threads = n_threads
		
		for n in ns:
			self.times[n] = {}
			self.speedups[n] = {}
			self.efficiencies[n] = {}

			for threads in n_threads:
				self.times[n][threads] = 0
				self.speedups[n][threads] = 0
				self.efficiencies[n][threads] = 0



	def set_time(self, time, n, threads):
		self.times[n][threads] = time
		return

	def calculate_speedups(self):
		for n in self.times:
			for threads in n_threads:
				speedup = self.times[n][1] / self.times[n][threads]
				self.speedups[n][threads] = speedup


	def calculate_efficiencies(self):
		for n in self.times:
			for threads in n_threads:
				efficiency = self.speedups[n][threads] / threads
				self.efficiencies[n][threads] = efficiency


	def get_time(self, n, threads):
		return self.times[n][threads]

	def get_efficiency(self, n, threads):
		return self.efficiencies[n][threads]

	def get_speedup(self, n, threads):
		return self.speedups[n][threads]


	def print_tables(self, output_file = "tables.md"):
		#printa as tabelas em formato Markdown
		counter = 1

		header = self.__format_header()

		with open(output_file, "w") as f:
			#Tabelas de tempos
			lines = []

			identifier = "\n###Tabela " + str(counter) + "- Tempos\n"
			lines = [identifier,header]
			for threads in self.n_threads:
				line = "|" + str(threads) + "\t|"
				for n in self.times:
					line += ("%.2f" % self.get_time(n,threads))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

			#Tabelas de speedups
			identifier = "\n###Tabela " + str(counter) + "- Speedups\n"
			lines = [identifier,header]
			for threads in self.n_threads:
				line = "|" + str(threads) + "\t|"
				for n in self.times:
					line += ("%.2f" % self.get_speedup(n,threads))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

			#Tabelas de eficiencias
			identifier = "\n###Tabela " + str(counter) + "- Eficiencias\n"
			lines = [identifier,header]
			for threads in self.n_threads:
				line = "|" + str(threads) + "\t|"
				for n in self.times:
					line += ("%.2f" % self.get_efficiency(n,threads))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

	def __format_header(self):
		header = "|No. Threads|"
		tracinhos = "|-----------|"
		for n in self.times:
			header += "N="+ str(n) + "|"
			for i in range(len(str(n))+2):
				tracinhos += '-'
			tracinhos += "|"
		header += "\n"
		header += tracinhos + "\n"

		return header


def get_media(times):
	total=0
	for time in times:
		total += time
	return total/len(times)


def get_run_time(cmd):
	times = []
	media = 0
	for x in range(5):	#executa 5 vezes cada comando para tirar a media do tempo
		exe = Popen(cmd, shell=True, stdout=PIPE)
		(saida, erro) = exe.communicate()	#espera até finalizar o programa
		saida = saida.decode()
		time = saida.split()[1]
		times.append(float(time))	#pega o tempo de execução: decodifica a saida para string e converte-a em inteiro
	return get_media(times)

#######################################################
#Parametros que serão variados entre as execuções
ns = [500,750,1500]
#ns = [100,200]
n_threads = [1,2,4]
#######################################################





if (len(sys.argv) != 2):
	print("Usage: $python3 run_floyds.py <path_to_executable>")
	print("Example1: $python3 run_floyds.py /floyd_paralelo/floyd_par")
	exit()

floyd_path = sys.argv[1]
statistics = estatisticator9001(ns, n_threads)



for n in ns:
	for threads in n_threads:
		cmd = "OMP_NUM_THREADS=" + str(threads) + " " + floyd_path + " " + str(n)
		time = get_run_time(cmd)
		statistics.set_time(time, n, threads)
		output = "\n\nMedia do tempo de execucao para " + cmd + "\n" + str(time)
		print(output)

statistics.calculate_speedups()
statistics.calculate_efficiencies()
#statistics.dump("dump.data")
statistics.print_tables()