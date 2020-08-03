CC=cc
CFLAGS=-Wall -Wextra -pedantic -Werror -std=c99
LDFLAGS=-lm
PYLINTFLAGS=--exit-zero --score n


clean:
	rm -f *.pyc *.o test-c perf.*
	rm -rf {.,c,py}/__pycache__ 


test-py:
	python py/test.py


test-numpy:
	python py/test_numpy.py


test-c: c/test.c c/dulp.c
	$(CC) c/test.c -o $@ $(CFLAGS) $(LDFLAGS)
	./$@


test: test-c test-py test-numpy


lint:
	pylint py/dulp.py $(PYLINTFLAGS)
	pylint py/dulp_numpy.py $(PYLINTFLAGS)
	pylint py/test.py $(PYLINTFLAGS)
	pylint py/test_numpy.py $(PYLINTFLAGS)


bench-numpy:
	python -m timeit -vv -s "from py.bench_numpy import bench" "bench()"


bench-numpyf:
	python -m timeit -vv -s "from py.bench_numpy import benchf" "benchf()"


bench: bench-numpy bench-numpyf


.PHONY: clean \
	test-py test-numpy test-c test \
	lint \
	bench-numpy bench-numpyf bench
