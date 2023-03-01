CC = g++
CFLAGS = -Wall -Wpedantic -Wextra

all: init destroy print set

init: init.cpp
	$(CC) $(CFLAGS) -o init init.cpp

destroy: destroy.cpp
	$(CC) $(CFLAGS) -o destroy destroy.cpp

print: print.cpp
	$(CC) $(CFLAGS) -o print print.cpp

set: set.cpp
	$(CC) $(CFLAGS) -o set set.cpp

check_init_and_destroy: init destroy
	./init
	./destroy

clean:
	rm -f init destroy print set file.txt

