import sys
import time

import pycuda.driver as cuda
import pycuda.gpuarray as gpuArray
import pycuda.autoinit
import numpy



if len(sys.argv) != 4:
	print("Usage: python3 dot_cuda.py <n_workers> <work_size> <repetitions>")
	exit(1)

n_workers = int(sys.argv[1])
work_size = int(sys.argv[2])
repetitions = int(sys.argv[3])


t1 = time.perf_counter()

vec_a = numpy.float32(numpy.array([0.01 for i in range(work_size*n_workers)]))
vec_b = numpy.float32(numpy.array([1.00 for i in range(work_size*n_workers)]))
gpu_a = gpuArray.to_gpu(vec_a)
gpu_b = gpuArray.to_gpu(vec_b)
t_aloc = time.perf_counter() - t1

t2 = time.perf_counter()
dot = gpuArray.dot(gpu_a, gpu_b)
t_proc = t2-time.perf_counter()

print(dot)
print("Tempo Alocacao: " + str(t_aloc))
print("Tempo Calculos: " + str(t_calc))