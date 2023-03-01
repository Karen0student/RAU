#include <iostream>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <unistd.h>

#define BLOCK_SIZE 1024
#define FILENAME "file.txt"

int main(){

    key_t key = ftok(FILENAME, 3);
    int shm_id = shmget(key, BLOCK_SIZE, 0);
    if(shm_id == -1){
        perror("shmget error");
        exit(1);
    }

    char *data = (char*)shmat(shm_id, NULL, 0);
    if(data == (char*)false){
        perror("shmat error");
        exit(1);
    }

    while(true){
        std::cout << data << " ";
        sleep(5);
    }

    if(shmdt(data) == -1){
        perror("shmdt error");
        exit(1);
    }
return 0;
}

