CC=cc
CFLAGS=-Wall -Wextra -pedantic -Werror -std=c99
LDFLAGS=-lm
PYLINTFLAGS=--exit-zero --score n


clean:
	rm -f *.pyc *.o test-c


test-py:
	python test.py


test-numpy:
	python test_numpy.py


test-c: test.c
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)
	./$@


test: test-c test-py test-numpy


lint:
	pylint dulp.py $(PYLINTFLAGS)
	pylint dulp_numpy.py $(PYLINTFLAGS)
	pylint test.py $(PYLINTFLAGS)
	pylint test_numpy.py $(PYLINTFLAGS)


bench-numpy:
	python -m timeit -vv -s "from bench_numpy import bench" "bench()"


bench-numpyf:
	python -m timeit -vv -s "from bench_numpy import benchf" "benchf()"


bench: bench-numpy bench-numpyf


.PHONY: clean \
	test-py test-numpy test-c test \
	lint \
	bench-numpy bench-numpyf bench
