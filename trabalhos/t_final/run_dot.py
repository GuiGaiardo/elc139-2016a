#Author: Guilherme Gaiardo
#Description: Script para rodar o dotprod.py com diferentes parametros

from subprocess import *
import sys

#Tabajara(R)
class Estatisticator9001:
	#Its over 9000!
	def __init__(self, vec_size, n_process):
		self.times = {}
		self.speedups = {}
		self.efficiencies = {}
		self.variances = {}

		self.n_process = n_process
		
		for vec in vec_size:
			self.times[vec] = {}
			self.speedups[vec] = {}
			self.efficiencies[vec] = {}
			self.variances[vec] = {}

			for process in n_process:
				self.times[vec][process] = 0
				self.speedups[vec][process] = 0
				self.efficiencies[vec][process] = 0
				self.variances[vec][process] = {}

	def set_time(self, time, vec_size, process):
		self.times[vec_size][process] = time

	def set_variance(self, variance, vec_size, process):
		self.variances[vec_size][process] = variance

	def calculate_speedups(self):
		for vec_size in self.times:
			for process in self.n_process:
				speedup = self.times[vec_size][1] / self.times[vec_size][process]
				self.speedups[vec_size][process] = speedup

	def calculate_efficiencies(self):
		for vec_size in self.times:
			for process in self.n_process:
				efficiency = self.speedups[vec_size][process] / process
				self.efficiencies[vec_size][process] = efficiency

	def get_time(self, vec_size, process):
		return self.times[vec_size][process]

	def get_variance(self, vec_size, process):
		return self.variances[vec_size][process]

	def get_efficiency(self, vec_size, process):
		return self.efficiencies[vec_size][process]

	def get_speedup(self, vec_size, process):
		return self.speedups[vec_size][process]

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
				for vec_size in self.times:
					line += ("%.2f" % self.get_time(vec_size,process))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1
			
			#Tabelas de variancia
			identifier = "\n###Tabela " + str(counter) + "- Variancias\n"
			lines = [identifier,header]
			for process in self.n_process:
				line = "|" + str(process) + "\t|"
				for vec_size in self.times:
					line += ("%.2f" % self.get_variance(vec_size,process))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

			#Tabelas de speedups
			identifier = "\n###Tabela " + str(counter) + "- Speedups\n"
			lines = [identifier,header]
			lines = [identifier,header]
			for process in self.n_process:
				line = "|" + str(process) + "\t|"
				for vec_size in self.times:
					line += ("%.2f" % self.get_speedup(vec_size,process))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

			#Tabelas de eficiencias
			identifier = "\n###Tabela " + str(counter) + "- Eficiencias\n"
			lines = [identifier,header]
			for process in self.n_process:
				line = "|" + str(process) + "\t|"
				for vec_size in self.times:
					line += ("%.2f" % self.get_efficiency(vec_size,process))+ "\t|"
				lines.append(line+"\n")
			f.writelines(lines)
			counter += 1

	def __format_header(self):
		header = "|No. Process|"
		tracinhos = "|-----------|"
		for vec_size in self.times:
			header += "vec_size="+ str(vec_size) + "|"
			for i in range(len(str(vec_size))+2):
				tracinhos += '-'
			tracinhos += "|"
		header += "\n"
		header += tracinhos + "\n"

		return header


def average_and_variance(times):
	average = sum(times)/len(times)
	variance = sum([(n-average)**2 for n in times])/len(times)
	return average, variance

def get_run_time(cmd):
	times = []
	media = 0
	for x in range(5):	#executa 5 vezes cada comando para tirar a media do tempo
		exe = Popen(cmd, shell=True, stdout=PIPE)
		(saida, erro) = exe.communicate()	#espera ate finalizar o programa
		saida = saida.decode()
		time = saida.split()[5]
		times.append(float(time))	#pega o tempo de execucao: decodifica a saida para string e converte-a em inteiro
		print(time)
	return average_and_variance(times)

def start_tests(statistics, script):
	for vec in vec_size:
		for process in n_process:
			work_size = vec/process
			cmd = "python3 " + script + " " + str(process) + " " + str(int(work_size)) + " " + str(repetitions)
			time, variance = get_run_time(cmd)
			with open("times_bckp", "a") as backup_file:
				line = str(vec) + " " + str(process) + " " + str(time) + ", " + str(variance) + "\n"
				backup_file.write(line)
			statistics.set_time(time, vec, process)
			statistics.set_variance(variance, vec, process)
			output = "\n\nMedia do tempo de execucao para " + cmd + "\n" + str(time)
			print(output)

def load_times(statistics, times_file):
	with open(times_file, "r") as f:
		lines = f.readlines()
	times = []
	variances = []
	
	for line in lines:
		line = line.split(" ")
		time = float(line[0][:len(line[0])-1])
		
		times.append(time)
		variances.append(float(line[1]))

	for vec in vec_size:
		for process in n_process:
			statistics.set_time(times.pop(0), vec, process)
			statistics.set_variance(variances.pop(0), vec, process)


#######################################################
#Parametros que serao variados entre as execucoes
vec_size = [100000, 500000, 1000000]
repetitions = 3000
n_process = [1,2,4,8]
#######################################################


statistics = Estatisticator9001(vec_size, n_process)

if len(sys.argv) >= 2:
	if sys.argv[1] == '-l':
		times_file = sys.argv[2]
		load_times(statistics, times_file)
	else:
		script = sys.argv[1]
		start_tests(statistics, script)

else:
	print("Usage: $python3 run_dot.py [-l] <path_to_file>")
	print("Example1: $python3 run_dot.py ./dot_prod.py")
	print("Example1: $python3 -l ./times_bckp")
	exit()



statistics.calculate_speedups()
statistics.calculate_efficiencies()
statistics.print_tables()