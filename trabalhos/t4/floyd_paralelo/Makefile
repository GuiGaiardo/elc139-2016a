CXX=g++
#CXXFLAGS=-Wall -I. -O2 -DNDEBUG
CXXFLAGS=-Wall -fopenmp -I. 
OBJS=Graph.o floyd_par.o
PROGS=floyd_par
floyd_par: $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS)
all: $(PROGS)
clean:
	rm -f *.o $(PROGS)
