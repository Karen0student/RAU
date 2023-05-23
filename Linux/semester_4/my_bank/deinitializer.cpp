#include "bank.h"
#include <iostream>
#include <sys/shm.h>
#include <sys/sem.h>

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

union semun {
    int val;               /* used for SETVAL only */
    struct semid_ds *buf;  /* used for IPC_STAT and IPC_SET */
    ushort *array;         /* used for GETALL and SETALL */
};

int main(){
    destroy_bank();
    union semun arg;
    key_t key_FreezeUnfreeze = ftok("bank.h", 'T');
    if(key_FreezeUnfreeze == -1){   
        perror("ftok");
        exit(1);
    }
    //std::cout << "key_FREEZE: " << key_FreezeUnfreeze << std::endl;

    int semid_FreezeUnfreeze = semget(key_FreezeUnfreeze, 1, 0);
    if(semid_FreezeUnfreeze == -1){
        perror("semget deinitializer");
        exit(1);
    }
    //arg.val = 1;
    //std::cout << "semid_FreezeUnfreeze: " << semid_FreezeUnfreeze << std::endl;
    int value = semctl(semid_FreezeUnfreeze, 0, GETVAL);
    //std::cout << "value of semaphore: " << value << std::endl;
    if(semctl(semid_FreezeUnfreeze, 0, IPC_RMID, arg) == -1){
        perror("semctl");
        exit(1); 
    }
    exit(0);
}