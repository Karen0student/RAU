#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>
#include <pthread.h>
#include <string>
#include <cmath>
#include <cstring>

struct thread_data{
    int index;
    int num1;
    int num2;
    std::string symbol;
};

void* threadFunc(void* arg){
    thread_data* args = (thread_data*) arg;
    int fd = 0;
    std::string file_name = "out_" + std::to_string(args->index) + ".txt";
    fd = open(file_name.c_str(), O_TRUNC | O_CREAT | O_RDWR, 0666);
    if(fd < 0){
        std::cout << "ERROR opening file" << std::endl;
        exit(0);
    }

    int fda; 
        if(args->symbol == "s"){
            std::string str = std::to_string(args->num1) + " s " + std::to_string(args->num2) + " = " + std::to_string(args->num1 + args->num2);
            fda = write(fd, str.c_str(), str.size());
            if(fda < 0){
                std::cout << "ERROR(+)" << std::endl;
                exit(0);
            }
            if(close(fd) < 0){
                std::cout << "cant close fd" << std::endl;
                exit(0);
            }
            pthread_exit(NULL);
        }
        if(args->symbol == "m"){// *
            std::string str = std::to_string(args->num1) + " m " + std::to_string(args->num2) + " = " + std::to_string(args->num1 * args->num2);
            fda = write(fd, str.c_str(), str.size());
            if(fda < 0){
                std::cout << "ERROR(*)" << std::endl;
                exit(0);
            }
            if(close(fd) < 0){
                std::cout << "cant close fd" << std::endl;
                exit(0);
            }
            pthread_exit(NULL);
        }
        if(args->symbol == "ss"){// ^, +
            std::string str = std::to_string(args->num1) + " ss " + std::to_string(args->num2) + " = " + std::to_string(pow(args->num1, 2) + pow(args->num2, 2));
            fda = write(fd, str.c_str(), str.size());
            if(fda < 0){
                std::cout << "ERROR(+)" << std::endl;
                exit(0);
            }
            if(close(fd) < 0){
                std::cout << "cant close fd" << std::endl;
                exit(0);
            }
            pthread_exit(NULL);
        }
        else{
            std::cout << "Error! The operator is not correct";
            if(close(fd) < 0){
                std::cout << "cant close fd" << std::endl;
                exit(0);
            }
            pthread_exit(NULL);
        }
    
}

int main(int argc, char** argv){
    pthread_t tid;
    thread_data object;
    for(int i = 0; i < atoi(argv[1]); ++i){   
        object.index = i;
        std::cin >> object.num1 >> object.num2 >> object.symbol;
        int threadRes = pthread_create(&tid, NULL, threadFunc, (void*)&object);
        if(threadRes != 0){
            std::cout << "Could not create thread\n";
            exit(0);
        }
    }
    for(int i = 0; i < atoi(argv[1]); ++i){
        int join = pthread_join(tid, NULL);
    }
}