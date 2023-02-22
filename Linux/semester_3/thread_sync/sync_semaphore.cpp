#include <iostream>
#include <pthread.h> 
#include <semaphore.h>
#include <fcntl.h>
#include <unistd.h>

class Integer{
private:
    int value;
    sem_t* semaph; 
public:
    Integer(int val):value(val){
        this->semaph = new sem_t();
        sem_init(this->semaph, 0, 1);
    }   
    
    int get_value(){
        return this->value;
    }
    void set_value(int val){
        this->value = val;
    }
    void inc(){
        sem_wait(this->semaph);
        this->value++;
        sem_post(this->semaph);
    }
    ~Integer() {
        sem_destroy(this->semaph);
        delete this->semaph;
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
    int thread_num = 56;
    Integer* integ = new Integer(0);
    pthread_t* thrds = new pthread_t[thread_num];
    
    for (int i = 0; i < thread_num; i++){
        if(pthread_create(&thrds[i], NULL, inc, (void*)integ) != 0){
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
    std::string result = "sync_semaphore time is: " + std::to_string(seconds + milliseconds * 1e-9) + "\n";
    int fd = open("time.txt", O_CREAT | O_RDWR | O_APPEND, 0666);
    write(fd, result.c_str(), result.size());
    if(close(fd) < 0){
        std::cout << "error closing file" << std::endl;
        exit(0);
    }
    std::cout << "***program finished***" << std::endl;
    return 0;
}
