#include <iostream>
#include <sys/shm.h>
#include <fcntl.h>

#define BLOCK_SIZE 1024
#define FILENAME "file.txt"

int main(){

    int fd = open(FILENAME, O_TRUNC | O_CREAT | O_RDWR, 0777);
    if(fd < 0){
        perror("ERROR: open(fd)");
        return 1;
    }

    key_t key = ftok("file.txt", 3);
    int shm_id = shmget(key, BLOCK_SIZE, IPC_CREAT | IPC_EXCL | 0777);
    if(shm_id  == -1){
        perror("shmget error");
        exit(1);
    }
    std::cout << "init.cpp executed successfully" << std::endl;
return 0;
}

