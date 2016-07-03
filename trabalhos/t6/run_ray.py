#Author: Guilherme Gaiardo
#Description: Script para rodar o ray_trace em um cluster com diferentes parametros

from subprocess import *
import sys

#Tabajara(R)
class estatisticator9001:
	#Its over 9000!
	def __init__(self, levels, n_process):
		self.times = {}
		self.speedups = {}
		self.efficiencies = {}

		self.n_process = n_process
		
		for level in levels:
			self.times[level] = {}
			self.speedups[level] = {}
			self.efficiencies[level] = {}

			for process in n_process:
				self.times[level][process] = 0
				self.speedups[level][process] = 0
				self.efficiencies[level][process] = 0



	def set_time(self, time, level, process):
		self.times[level][process] = time
		return

	def calculate_speedups(self):
		for level in self.times:
			for process in self.n_process:
				speedup = self.times[level][2] / self.times[level][process]
				self.speedups[level][process] = speedup


	def calculate_efficiencies(self):
		for level in self.times:
			for process in self.n_process:
				efficiency = self.speedups[level][process] / (process-1)
				self.efficiencies[level][process] = efficiency


	def get_time(self, level, process):
		return self.times[level][process]

	def get_efficiency(self, level, process):
		return self.efficiencies[level][process]

	def get_speedup(self, level, process):
		return self.speedups[level][process]


	def print_tables(self, output_file = "tables.md"):
		#printa as tabelas em formato Markdown
		counter = 1

		header = self.__format_header()

		with open(output_file, "w") as f:
			#Tabelas de tempos
			lines = []

			identifier = "\n###Tabela " + str(counter) + "- Tempos\n"
			lines = [identifier,header]
			for process in self.n_process:
				line = "|" + str(process) + "\t|"
				for level in self.times:
					line += ("%.2f" % self.get_time(level,process))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

			#Tabelas de speedups
			identifier = "\n###Tabela " + str(counter) + "- Speedups\n"
			lines = [identifier,header]
			for process in self.n_process:
				line = "|" + str(process) + "\t|"
				for level in self.times:
					line += ("%.2f" % self.get_speedup(level,process))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

			#Tabelas de eficiencias
			identifier = "\n###Tabela " + str(counter) + "- Eficiencias\n"
			lines = [identifier,header]
			for process in self.n_process:
				line = "|" + str(process) + "\t|"
				for level in self.times:
					line += ("%.2f" % self.get_efficiency(level,process))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

	def __format_header(self):
		header = "|No. Process|"
		tracinhos = "|-----------|"
		for level in self.times:
			header += "Level="+ str(level) + "|"
			for i in range(len(str(level))+2):
				tracinhos += '-'
			tracinhos += "|"
		header += "\n"
		header += tracinhos + "\n"

		return header


def get_media(times):
	total=0
	for time in times:
		total += time/1000000
	return total/len(times)


def get_run_time(cmd):
	times = []
	media = 0
	for x in range(10):	#executa 5 vezes cada comando para tirar a media do tempo
		exe = Popen(cmd, shell=True, stdout=PIPE)
		(saida, erro) = exe.communicate()	#espera ate finalizar o programa
		saida = saida.decode()
		time = saida.split()[3]
		times.append(float(time))	#pega o tempo de execucao: decodifica a saida para string e converte-a em inteiro
	return get_media(times)

#######################################################
#Parametros que serao variados entre as execucoes
levels = [2,6,10,15]
n_process = [2,3,4,7,10,12]
#######################################################





if (len(sys.argv) < 2):
	print("Usage: $python3 run_ray.py <host_file> <path_to_executable>")
	print("Example1: $python3 run_ray.py ./mpi_hosts ./ray_mpi")
	print("Omit host file if not using any.")
	exit()

if (len(sys.argv) == 3):
	ray_path = sys.argv[2]
	host_file = " -hostfile " + sys.argv[1]
else:
	ray_path = sys.argv[1]
	host_file = ""
statistics = estatisticator9001(levels, n_process)



for level in levels:
	for process in n_process:
		cmd = "mpirun -np " + str(process) + host_file + " " + ray_path + " " + str(level)
		time = get_run_time(cmd)
		statistics.set_time(time, level, process)
		output = "\n\nMedia do tempo de execucao para " + cmd + "\n" + str(time)
		print(output)

statistics.calculate_speedups()
statistics.calculate_efficiencies()
statistics.print_tables()