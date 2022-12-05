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
    std::cout << "entered threadFunc" << std::endl;
    int fd = 0;
    //std::cout << args->num1  << " " << args->num2 << std::endl;
    std::string file_name = "out_" + std::to_string(args->index) + ".txt";
    std::cout << file_name << std::endl;
    fd = open(file_name.c_str(), O_TRUNC | O_CREAT | O_RDWR, 0755);
    if(fd < 0){
        std::cout << "ERROR opening file" << std::endl;
        exit(0);
    }
    std::cout << "after opening file" << std::endl;
    
    
    // int x = ((int*)arg)[1];
    // int y = ((int*)arg)[2];
//change args to args
    //check
    //std::cout << "arg[1] = " << ((std::string*)arg)[1] << " arg[2] = " << ((std::string*)arg)[2] << std::endl;
    std::cout << "x = " << args->num1 << " y = " << args->num2 << std::endl;
    //

    int fda;
    std::cout << args->symbol << std::endl;
    //const std::string* symbol = (((std::string*)arg)[3]).c_str(); 
        if(args->symbol == "s"){
            std::string str = std::to_string(args->num1) + " s " + std::to_string(args->num2) + " = " + std::to_string(args->num1 + args->num2);
            std::cout << str.size() << std::endl;
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
            std::string str = std::to_string(args->num1) + " s " + std::to_string(args->num2) + " = " + std::to_string(pow(args->num1, args->num1) + pow(args->num2, args->num2));
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
    for(int i = 0; i < atoi(argv[1]); ++i){   
        std::cout << "entered cycle" << std::endl;

        std::cout << "before thread" << std::endl;
        thread_data object;
        object.index = i;
        std::cin >> object.num1 >> object.num2 >> object.symbol;

        int threadRes = pthread_create(&tid, NULL, threadFunc, (void*)&object);
        if(threadRes != 0){
            std::cout << "Could not create thread\n";
            exit(0);
        }
        void* retval;
        int join = pthread_join(tid, &retval);
    }
}