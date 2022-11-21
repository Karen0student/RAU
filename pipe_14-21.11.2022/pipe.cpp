#include <iostream>
#include <unistd.h>
#include <sys/wait.h>

int main(int argc, char** argv){
    int fd1[2];
    int fd2[2];

    if(pipe(fd1) == -1){
        std::cout << "ERROR" << std::endl;
    }
    if(pipe(fd2) == -1){
        std::cout << "ERROR" << std::endl;
    }
    pid_t child1, child2;
    (child1 = fork()) && (child2 = fork());

    if(child1 == 0){
        close(fd1[0]);
        int pid_of_child1 = getpid();
        write(fd1[1], &pid_of_child1, sizeof(int));
        close(fd1[1]);

        close(fd2[1]);
        int recieved_pid_of_child1;
        read(fd2[0], &recieved_pid_of_child1, sizeof(int));
        close(fd2[0]);
        std::cout << "First: my pid is: " << pid_of_child1 << std::endl;
    }
    else if(child2 == 0){
        close(fd2[0]);
        int pid_of_child2 = getpid();
        write(fd2[1], &pid_of_child2, sizeof(int));
        close(fd2[1]);

        close(fd1[1]);
        int recieved_pid_of_child2;
        read(fd1[0], &recieved_pid_of_child2, sizeof(int));
        close(fd1[0]);
        std::cout << "Second: my pid is: " << pid_of_child2 << std::endl;
    }

    else{
        if(wait(NULL) == -1){
            std::cout << "ERROR(wait)" << std::endl;
            exit(0);
        }
    }

    
} 