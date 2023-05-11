#include "bank.h"
#include <iostream>
#include <sys/shm.h>

void *destroy_bank(){
    key_t key = ftok("bank.h", 'R');
    if(key < 0){
        std::cout << "ERROR, CAN'T GET KEY FOR 'bank.h'\n";
        return NULL;
    }

    int shm_id = shmget(key, sizeof(struct_bank), 0666);
    if(shm_id < 0){
        std::cout << "ERROR, FAILED TO GET SHARED MEMORY\n";
        return NULL;
    }

    if(shmctl(shm_id, IPC_RMID, NULL) < 0){
        std::cout << "ERROR, FAILED TO DELETE SHARED MEMORY\n";
        return NULL;
    }

    std::cout << "MEMORY DELETED SUCCESSFULLY\n";
    return NULL;
}

int main(){
    destroy_bank();
    exit(0);
}