#include <iostream>
#include <unistd.h>
#include <sys/wait.h>


int main(int argc, char** argv) {
    if (argc == 1) {
        return 2;
    }

    pid_t pid = fork();
    if (pid == -1) {
        return 1;
    }

    if (pid == 0) {  // child
    std::cout << "asdasdad";
        std::cout << "*argv + 1 = " << *argv + 1;
        execvp(argv[1], argv + 1);
        
    } else {  // parent
        int status;
        waitpid(pid, &status, 0);
        std::cout << "*** Program Finished ***" << std::endl;
    }
}
