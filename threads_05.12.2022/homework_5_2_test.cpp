#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/wait.h>
#include <pthread.h>
#include <string>
#include <cmath>


void* threadFunc(void* file_number){
    std::cout << "entered threadFunc" << std::endl;
    int fd = 0;
    std::string file_name = "out_" + ((std::string*)file_number)[0] + ".txt";
    fd = open(file_name.c_str(), O_TRUNC | O_CREAT, 0755);
    if(fd < 0){
        std::cout << "ERROR opening file" << std::endl;
        exit(0);
    }
    std::cout << "after opening file" << std::endl;
    int x, y;
    char arg;
    std::cin >> x >> y;
    std::cin >> arg;
    std::string str; 
    int fda;
    switch(arg){
        case 's':// +
            str = std::to_string(x) + " s " + std::to_string(y) + " = " + std::to_string(x + y);
            fda = write(fd, &str, str.size());
            if(fda < 0){
                std::cout << "ERROR(+)" << std::endl;
                exit(0);
            }
            if(close(fd) < 0){
                std::cout << "cant close fd" << std::endl;
                exit(0);
            }
            break; 
        case 'm':// *
            str = std::to_string(x) + " m " + std::to_string(y) + " = " + std::to_string(x * y);
            fda = write(fd, &str, str.size());
            if(fda < 0){
                std::cout << "ERROR(*)" << std::endl;
                exit(0);
            }
            if(close(fd) < 0){
                std::cout << "cant close fd" << std::endl;
                exit(0);
            }
            break;
        case 'ss':// ^, +
            str = std::to_string(x) + " s " + std::to_string(y) + " = " + std::to_string(pow(x, x) + pow(y, y));
        break;
        if(close(fd) < 0){
            std::cout << "cant close fd" << std::endl;
            exit(0);
        }
        default:
            std::cout << "Error! The operator is not correct";
            if(close(fd) < 0){
                std::cout << "cant close fd" << std::endl;
                exit(0);
            }
            break;
    }
    pthread_exit(NULL);
    
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
        int threadRes = pthread_create(&tid, NULL, &threadFunc, (int*) i);
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