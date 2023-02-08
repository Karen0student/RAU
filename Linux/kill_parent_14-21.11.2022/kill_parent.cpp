/*Напишите программу, в которой родительский процесс порождает дочерний процесс,
 который должeн убить своего родителя. Проверить может ли дочерний процесс
  убить своего родителя, если да, то что станет с дочерним процессом.*/
#include <iostream>
#include <signal.h>
#include <sys/wait.h>

int main(){
    pid_t pid = fork();
    if(pid == 0){
        pid_t parent_pid = getppid();
        kill(parent_pid, SIGKILL);
        std::cout << "child killed parent" << std::endl;
    }
    else{
        int status;
        waitpid(pid, &status, 0);
    }
}