#include <iostream>
#include <sys/wait.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>

int main(int argc, char** argv){

    if(argc < 1){
        std::cout << "enter arugments";
        exit(errno);
    }

    pid_t pid = fork();
	if(pid == -1){
		std::cout << "Error" << std::endl;
		exit(errno);
	}
    if(pid == 0){ //child
        for(int i = 1; i < argc; ++i){
            char* arg_vec[] = {argv[i], nullptr};
            if(execvp(argv[i], arg_vec) < 0){
                std::cout  << "execvp error on command: " << argv[i] << std::endl;
                continue;
            }
            execvp(argv[i], arg_vec);
            _exit(0);
        }
        
    }

    else{ //parent
        int status;
        waitpid(pid, &status, 0);

    }
    std::cout << "***program finished***" << std::endl;
    return 0;
}