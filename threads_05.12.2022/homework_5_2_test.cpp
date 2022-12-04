#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>
#include <pthread.h>
#include <string>
#include <cmath>
#include <cstring>


void* threadFunc(void* arg){
    std::cout << "entered threadFunc" << std::endl;
    int fd = 0;
    std::string file_name = "out_" + ((std::string*)arg)[0] + ".txt";
    std::cout << file_name << std::endl;
    fd = open(file_name.c_str(), O_TRUNC | O_CREAT, 0755);
    if(fd < 0){
        std::cout << "ERROR opening file" << std::endl;
        exit(0);
    }
    std::cout << "after opening file" << std::endl;
    
    int *x = &((int*)arg)[1];
    int *y = &((int*)arg)[2];
    
    //check
    std::cout << "arg[1] = " << ((std::string*)arg)[1] << " arg[2] = " << ((std::string*)arg)[2] << std::endl;
    std::cout << "x = " << x << " y = " << y << std::endl;
    //

    int fda;
    std::cout << ((std::string*)arg)[3] << std::endl;
    //const std::string* symbol = (((std::string*)arg)[3]).c_str(); 
        if(((std::string*)arg)[3] == "s"){
            std::string str = ((std::string*)arg)[1] + " s " + ((std::string*)arg)[2] + " = " + std::to_string(&x + &y);
            std::cout << str.size() << std::endl;
            fda = write(fd, &str, str.size());
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
        if(((std::string*)arg)[3] == "m"){// *
            std::string str = std::to_string(x) + " m " + std::to_string(y) + " = " + std::to_string(x * y);
            fda = write(fd, &str, str.size());
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
        if(((std::string*)arg)[3] == "ss"){// ^, +
            std::string str = std::to_string(x) + " s " + std::to_string(y) + " = " + std::to_string(pow(x, x) + pow(y, y));
            fda = write(fd, &str, str.size());
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
    // if(atoi(argv[1]) <= 0 || argc <= 1){
    //     std::cout << "***program finished, nothing passed***" << std::endl;
    //     exit(0);
    // }
    pthread_t tid;
    for(int i = 0; i < atoi(argv[1]); ++i){   
        std::cout << "entered cycle" << std::endl;
        //char* arg[1] = {(char*)i};
        // char* arg = new char;
        // arg = (char*)i;
        std::cout << "before thread" << std::endl;
        std::string x, y, argument;
        std::cin >> x >> y >> argument;

        std::string arg [4] = {std::to_string(i), x, y, argument};
        int threadRes = pthread_create(&tid, NULL, &threadFunc, (std::string*)&arg);
        if(threadRes != 0){
            std::cout << "Could not create thread\n";
            exit(0);
        }
        void* retval;
        int join = pthread_join(tid, &retval);
        //delete arg;
    }

    // for(int i = 0; i < atoi(argv[1]); ++i){
        
    // }

}