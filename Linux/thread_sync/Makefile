compile : sync_mutex.cpp sync_semaphore.cpp sync_spinlock.cpp
	g++ sync_mutex.cpp -o sync_mutex
	g++ sync_semaphore.cpp -o sync_semaphore
	g++ sync_spinlock.cpp -o sync_spinlock
	./sync_mutex
	./sync_semaphore
	./sync_spinlock
	rm sync_mutex sync_semaphore sync_spinlock

clear : time.txt
	rm time.txt