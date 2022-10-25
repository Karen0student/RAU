#include <iostream>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

int main(int argc, char** argv){

    if(argc < 2){
        std::cout << "enter arugments" << std::endl;
        exit(errno);
    }

    pid_t pid = fork();
    for(int i = 1; i < argc; ++i){
        if(pid == -1){
            std::cout << "Error" << std::endl;
            exit(errno);
        }
        if(pid == 0){ //child
            
            char* arg_vec[] = {argv[i], nullptr};
            if(execvp(argv[i], arg_vec) < 0){
                std::cout  << "execvp error on command: " << argv[i] << std::endl;
                continue;
            }
            execvp(argv[i], arg_vec);
        }
        
        else{ //parent
            int status;
            wait(&status);

            if(WIFEXITED(status)){
                _exit(0);
            }

        }
    }

    std::cout << "***program finished***" << std::endl;
    return 0;
}