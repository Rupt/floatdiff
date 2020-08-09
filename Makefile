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
	rm -rf py/dulp/__pycache__


test-py: py/dulp/test.py
	python py/dulp/test.py


test-numpy: py/dulp/test_np.py
	python py/dulp/test_np.py


test-c: c/test.c c/dulp.c
	$(CC) c/test.c -o $@ $(CFLAGS) $(LDFLAGS)
	./$@


test: test-c test-py test-numpy


lint:
	pylint py/dulp $(PYLINTFLAGS)

bench-numpy:
	python -m timeit -vv -s "from py.dulp.bench_np import bench" "bench()"


bench-numpyf:
	python -m timeit -vv -s "from py.dulp.bench_np import benchf" "benchf()"


bench: bench-numpy bench-numpyf


.PHONY: options clean \
	lint \
	bench-numpy bench-numpyf bench
