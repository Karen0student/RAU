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

    for(int i = 1; i < argc; ++i){
        pid_t pid = fork();
        if(pid == -1){
            std::cout << "Error" << std::endl;
            exit(errno);
        }
        if(pid == 0){ //child
            char* arg_vec[] = {argv[i], nullptr};
            if(execvp(argv[i], arg_vec) < 0){
                _exit(2);
            }
            execvp(argv[i], arg_vec);
            _exit(0);
        }

        if(pid > 0){ //parent
            int status;
            wait(&status);
            //std::cout << WIFEXITED(status) << " " << WEXITSTATUS(status) << std::endl;
            if(WIFEXITED(status) == 1 && WEXITSTATUS(status) == 0){
                std::cout << "***program finished***" << std::endl;
                exit(0);
            }
        }
    }
    
    std::cout << "***program finished, nothing passed***" << std::endl;

    return 0;
}