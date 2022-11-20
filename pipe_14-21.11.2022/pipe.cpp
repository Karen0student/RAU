/*Напишите программу, в которой родительский процесс порождает
 две дочерние процессы, которые должны обменяться своими pid.
 Обмен должен быть реализован с помощью каналов. */
#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <cstring>

int main(){
    int pipefd[2];
    int pipe_res = pipe(pipefd);
    
    pid_t pid = fork();
    if(pid < 0){
        std::cout << "ERROR(fork_pid)\n";
        exit(0);
    }
    pid_t pid2 = fork();
    if(pid < 0){
        std::cout << "ERROR(fork_pid2)\n";
        exit(0);
    }

    if(pid == 0 && pid2 == 0){ //child + child^2
        std::cout << "ENTERED CHILD" << std::endl;
        int written = write(pipefd[1], &pid, sizeof(pid_t));
        if(written < 0){
            std::cout << "ERROR(written)" << std::endl;
            exit(0);
        }
        int written2 = write(pipefd[1], &pid2, sizeof(pid_t));
        if(written2 < 0){
            std::cout << "ERROR(written)" << std::endl;
            exit(0);
        }
        int readBytes2 = read(pipefd[0], &pid2, sizeof(pid_t));
        if(readBytes2 < 0){
            std::cout << "ERROR(readBytes2)" << std::endl;
            exit(0);
        }
        int readBytes = read(pipefd[0], &pid, sizeof(pid_t));
        if(readBytes < 0){
            std::cout << "ERROR(readbytes)" << std::endl;
            exit(0);
        }
        _exit(0);
    }

    else{ //parent
        int status;
        waitpid(pid2, &status, 0);
        //waitpid(pid, &status, 0);
        std::cout << "***finished***" << std::endl;
        }
        
}
