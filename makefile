CC=gcc
CFLAGS=-Wall -Wextra -pedantic -Werror -std=c89
LDFLAGS=-lm

test-exe: test.c
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS)

test-py:
	python test.py

test-numpy:
	python test_numpy.py

test-c: test-exe
	./test-exe

clean:
	rm -f *.pyc *.o run_test

.PHONY: test-py test-numpy test-c clean
