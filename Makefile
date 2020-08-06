CC=cc
CFLAGS=-Wall -Wextra -pedantic -Werror -std=c99 -fsanitize=undefined
LDFLAGS=-lm
PYLINTFLAGS=--exit-zero --score n


options:
	@echo "CC=${CC}"
	@echo "CFLAGS=${CFLAGS}"
	@echo "LDFLAGS=${LDFLAGS}"
	@echo "PYLINTFLAGS=${PYLINTFLAGS}"


clean:
	rm -f *.pyc *.o test-c perf.*
	rm -rf {.,py}/__pycache__


test-py: py/test.py
	python py/test.py


test-numpy: py/test_numpy.py
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


.PHONY: options clean \
	lint \
	bench-numpy bench-numpyf bench
