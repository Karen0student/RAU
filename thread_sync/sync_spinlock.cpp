#include <iostream>
#include <pthread.h> 
#include <fcntl.h>
#include <unistd.h>

class Integer{
private:
    int value;
    pthread_spinlock_t* spinLock;

public:
    Integer(int val):value(val){
        this->spinLock = new pthread_spinlock_t();
        pthread_spin_init(this->spinLock, PTHREAD_PROCESS_SHARED);
    }   
    
    int get_value(){
        return this->value;
    }
    void set_value(int val){
        this->value = val;
    }
    void inc(){
        pthread_spin_lock(this->spinLock);
        this->value++;
        pthread_spin_unlock(this->spinLock);
    }
    ~Integer() {
        pthread_spin_destroy(this->spinLock);
        delete this->spinLock;
    }
};

void* inc(void* arg){
    Integer* integ = (Integer*) arg;
    int inc_num = 10000;
    for (int i = 0; i < inc_num; i++){
       integ->inc(); 
    }
    return NULL;
}

int main () {
    struct timespec begin, end;
    clock_gettime(CLOCK_REALTIME, &begin);
    int start = clock();
    int thread_num = 56;
    Integer* integ = new Integer(0);
    pthread_t* thrds = new pthread_t[thread_num];
    
    for (int i = 0; i < thread_num; i++){
        if (pthread_create(&thrds[i], NULL, inc, (void*)integ) != 0){
            return 1;
        }
    }
    
    for (int i = 0; i < thread_num; i++){
        if (pthread_join(thrds[i], NULL) != 0){
            return 2;
        }
    }
    // std::cout << integ->get_value() << "\n";
    
    delete [] thrds;
    delete integ;
   
     clock_gettime(CLOCK_REALTIME, &end);
    long seconds = end.tv_sec - begin.tv_sec;
    long milliseconds = end.tv_nsec - begin.tv_nsec;
    std::string result = std::to_string(seconds + milliseconds * 1e-9) + "\n";
    int fd = open("time.txt", O_CREAT | O_RDWR | O_APPEND, 0666);
    write(fd, result.c_str(), result.size());
    if(close(fd) < 0){
        std::cout << "error closing file" << std::endl;
        exit(0);
    }
    std::cout << "***program finished***" << std::endl;
    return 0;
}


