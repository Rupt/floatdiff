CC=cc
CFLAGS=-Wall -Wextra -pedantic -Werror -fsanitize=undefined -std=c99
LDFLAGS=-lm
PYLINTFLAGS=--exit-zero --score n


test: test-c test-py test-numpy


test-py: test.py
	python test.py


test-numpy: test_numpy.py
	python test_numpy.py


test-c: test.c floatdiff.c
	$(CC) test.c -o $@ $(CFLAGS) $(LDFLAGS)
	./$@

.PHONY: test test-py test-numpy test-c


time-numpy:
	python -m timeit -vv -s "\
	from floatdiff_numpy import floatdiff; \
	from time_numpy import init; \
	x, y = init()" \
	"floatdiff(x, y)"


time-numpyf:
	python -m timeit -vv -s "\
	from floatdiff_numpy import floatdiff; \
	from time_numpy import initf; \
	x, y = initf()" \
	"floatdiff(x, y)"


time: time-numpy time-numpyf

.PHONY: time-numpy time-numpyf time


options:
	@echo "CC=${CC}"
	@echo "CFLAGS=${CFLAGS}"
	@echo "LDFLAGS=${LDFLAGS}"
	@echo "PYLINTFLAGS=${PYLINTFLAGS}"


clean:
	rm -f *.pyc test-c
	rm -rf __pycache__


lint:
	# with a grain of salt
	pylint floatdiff $(PYLINTFLAGS)

.PHONY: options clean lint

