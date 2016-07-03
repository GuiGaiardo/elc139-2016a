from multiprocessing import Pool
import time
import sys


def dot_prod(vecs):
	u,v = vecs
	for x in range(repetitions):
		my_sum = 0.0
		for i in range(len(u)):
			my_sum += u[i]*v[i]

	return my_sum



if len(sys.argv) != 4:
	print("Usage: python3 dot_prod.py <n_workers> <work_size> <repetitions>")
	exit(1)

n_workers = int(sys.argv[1])
work_size = int(sys.argv[2])
repetitions = int(sys.argv[3])

t1 = time.perf_counter()
vec_a = [[0.01 for x in range(work_size)] for i in range(n_workers)]
vec_b = [[1.0 for x in range(work_size)] for i in range(n_workers)]
vecs = [(vec_a[i],vec_b[i]) for i in range(n_workers)]
t_aloc = time.perf_counter() - t1

pool = Pool(processes=n_workers)
#map
t2 = time.perf_counter()
sums = pool.map(dot_prod, vecs)

#reduce
dot = sum(n for n in sums)
t_calc = time.perf_counter() - t2

print("Tempo Alocacao: " + str(t_aloc))
print("Tempo Calculos: " + str(t_calc))