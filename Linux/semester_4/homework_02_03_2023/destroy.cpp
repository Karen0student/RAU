#include <iostream>
#include <sys/shm.h>

#define FILENAME "file.txt"

int main(){

    key_t key = ftok(FILENAME, 3);
    int shm_id = shmget(key, 0, 0);
    if(shm_id == -1){
        perror("shmget error");
        exit(1);
    }

    if(shmctl(shm_id, IPC_RMID, NULL) == -1){
        perror("shmctl error");
        exit(1);
    }

    if(std::remove(FILENAME) == -1){
        perror("remove file error");
        exit(1);
    }
    
    std::cout << "destroy.cpp executed successfully" << std::endl;
return 0;
}

