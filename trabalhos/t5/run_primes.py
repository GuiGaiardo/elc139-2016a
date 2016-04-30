#Author: Guilherme Gaiardo
#Description: Script para rodar o 'primes' com diferentes parametros

from subprocess import *
import sys

#Tabajara(R)
class estatisticator9001:
	#Its over 9000!
	def __init__(self, n_max, chunk_sizes, n_threads, versions):
		self.times = {}
		self.speedups = {}
		self.efficiencies = {}
		self.t_seq = {}

		self.chunk_sizes = chunk_sizes
		self.n_threads = n_threads
		self.versions = []
		for key in versions:
			self.versions.append(key)
		n_versions = len(versions)
		
		for n in n_max:
			self.t_seq[n] = 0
			self.times[n] = [[0 for j in range(len(chunk_sizes))] for i in range(n_versions*len(n_threads))]
			self.speedups[n] = [[0 for j in range(len(chunk_sizes))] for i in range(n_versions*len(n_threads))]
			self.efficiencies[n] = [[0 for j in range(len(chunk_sizes))] for i in range(n_versions*len(n_threads))]

	def set_seq_time(self, n, time):
		self.t_seq[n] = time
		return

	def set_time(self, time, n, chunk, threads, version):
		(line, column) = self.__get_indexes(chunk, threads, version)

		self.times[n][line][column] = time
		return

	def calculate_speedups(self):
		for n in self.times:
			for version in self.versions:
				for threads in n_threads:
					for chunk in chunk_sizes:
						(line, column) = self.__get_indexes(chunk, threads, version)
						speedup = self.t_seq[n] / self.times[n][line][column]
						self.speedups[n][line][column] = speedup


	def calculate_efficiencies(self):
		for n in self.times:
			for version in self.versions:
				for threads in n_threads:
					for chunk in chunk_sizes:
						(line, column) = self.__get_indexes(chunk, threads, version)
						efficiency = self.speedups[n][line][column] / threads
						self.efficiencies[n][line][column] = efficiency


	def __get_indexes(self, chunk, threads, version):
		#pega os indices para acessar a posicao na tabela referente aos parametros
		v = self.versions.index(version)
		t = self.n_threads.index(threads)
		column = self.chunk_sizes.index(chunk)

		line = (len(self.n_threads) * v) + t

		return (line, column)

	def get_time(self, n, chunk, threads, version):
		(line, column) = self.__get_indexes(chunk, threads, version)

		return self.times[n][line][column]

	def get_efficiency(self, n, chunk, threads, version):
		(line, column) = self.__get_indexes(chunk, threads, version)

		return self.efficiencies[n][line][column]


	def get_speedup(self, n, chunk, threads, version):
		(line, column) = self.__get_indexes(chunk, threads, version)

		return self.speedups[n][line][column]


	def print_tables(self, output_file = "tables.md"):
		#printa as tabelas em formato Markdown
		counter = 1

		header = self.__format_header()

		with open(output_file, "w") as f:
			#Tabelas de tempos
			for n in self.times:
				identifier = "\n###Tabela " + str(counter) + "- Tempos para N=" + str(n) + "\n"
				lines = [identifier,header]
				for version in self.versions:
					for threads in self.n_threads:
						line = "|" + str(version) + "|" + str(threads) + "|"
						for chunk in self.chunk_sizes:
							line += str(self.get_time(n,chunk,threads,version)) + "|"
						lines.append(line+"\n")
				f.writelines(lines)
				counter += 1

			#Tabelas de speedups
			for n in self.times:
				identifier = "\n###Tabela " + str(counter) + "- SpeedUps para N=" + str(n) + "\n"
				lines = [identifier,header]
				for version in self.versions:
					for threads in self.n_threads:
						line = "|" + str(version) + "|" + str(threads) + "|"
						for chunk in self.chunk_sizes:
							line += str(self.get_speedup(n,chunk,threads,version)) + "|"
						lines.append(line+"\n")
				f.writelines(lines)
				counter += 1

			#Tabelas de eficiencias
			for n in self.times:
				identifier = "\n###Tabela " + str(counter) + "- Eficiencias para N=" + str(n) + "\n"
				lines = [identifier,header]
				for version in self.versions:
					for threads in self.n_threads:
						line = "|" + str(version) + "|" + str(threads) + "|"
						for chunk in self.chunk_sizes:
							line += str(self.get_efficiency(n,chunk,threads,version)) + "|"
						lines.append(line+"\n")
				f.writelines(lines)
				counter += 1

	
	def __format_header(self):
		header = "|V|#Thr|"
		for chunk in self.chunk_sizes:
			header += "Chunk="+str(chunk)+"|"
		header += "\n"

		return header


def get_media(times):
	total=0
	for time in times:
		total += time
	return total/len(times)


def get_run_time(cmd):
	times = []
	media = 0
	for i in range(5):	#executa 5 vezes cada comando para tirar a media do tempo
		exe = Popen(cmd, shell=True, stdout=PIPE)
		(saida, erro) = exe.communicate()	#espera até finalizar o programa
		saida = saida.decode()
		time = saida.split()[1]
		times.append(float(time))	#pega o tempo de execução: decodifica a saida para string e converte-a em inteiro
	return get_media(times)

############################################
#Parametros que serão variados entre as execuções
progs = {1:"./primes1", 2:"./primes2", 3:"./primes3"}
n_max = [500000, 1000000]
chunk_sizes = [1,10,100,1000]
n_threads = [2,4]
############################################





if (len(sys.argv) != 3):
	print("Usage: $python3 run_primes.py <path_to_executable | all> <output file>")
	print("Example1: $python3 run_primes.py ./primes1 out1.txt")
	print("Example2: $python3 run_primes.py ./primes2 out2.txt")
	print("Example3: $python3 run_primes.py all out.txt")
	exit()

if sys.argv[1] != "all":
	progs = {1:sys.argv[1]}
file_path = sys.argv[2]
statistics = estatisticator9001(n_max, chunk_sizes, n_threads, progs.keys())



with open(file_path, "w") as out_file:
	for n in n_max:
		cmd = "./primes_seq " + str(n)
		time = get_run_time(cmd)
		statistics.set_seq_time(n, time)
		for version in progs:
			for threads in n_threads:
				for chunk in chunk_sizes:
					cmd = "OMP_NUM_THREADS=" + str(threads) + " " + progs[version] + " " + str(n) + " " + str(chunk)
					media = get_run_time(cmd)
					output = "\n\nMedia do tempo de execucao para " + cmd + "\n" + str(media)
					print(output)
					out_file.write(output)
					statistics.set_time(media, n, chunk, threads, version)

statistics.calculate_speedups()
statistics.calculate_efficiencies()
statistics.print_tables()