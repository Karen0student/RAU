CC = gcc
CFLAGS = -Wall -Wextra -pedantic -O0 -g --coverage

TARGET = qsort

SRCS = qsort.c
OBJS = $(SRCS:.c=.o)

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET) *.gcov *.gcda *.gcno *.info *.o html -r

test:
	./$(TARGET) < test1.txt
	./$(TARGET) < test2.txt
	./$(TARGET) < test3.txt
	./$(TARGET) < test4.txt
	./$(TARGET) < test5.txt
	./$(TARGET) < test6.txt
	./$(TARGET) < test7.txt
	./$(TARGET) < test8.txt
	./$(TARGET) < test9.txt
	./$(TARGET) < test10.txt

coverage:
	lcov --rc lcov_branch_coverage=1 -c -d . -o coverage.info
	genhtml --branch-coverage coverage.info -o html