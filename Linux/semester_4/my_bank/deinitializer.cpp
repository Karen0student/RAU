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
    key_t key_semFreeze = ftok("bank.h", 'F');
    if(key_semFreeze == -1){   
        perror("ftok");
        exit(1);
    }
    //std::cout << "key_FREEZE: " << key_sem << std::endl;

    int semid_freeze = semget(key_semFreeze, 1, 0);
    if(semid_freeze == -1){
        perror("semget deinitializer");
        exit(1);
    }
    //arg.val = 1;
    //std::cout << "semid: " << semid << std::endl;
    //int value = semctl(semid, 0, GETVAL);
    //std::cout << "value of semaphore: " << value << std::endl;
    if(semctl(semid_freeze, 0, IPC_RMID, arg) == -1){
        perror("semctl");
        exit(1); 
    }


    key_t key_sem_transfer = ftok("bank.h", 'T');
    if(key_sem_transfer == -1){   
        perror("ftok");
        exit(1);
    }
    //std::cout << "key_FREEZE: " << key_sem << std::endl;

    int semid_transfer = semget(key_sem_transfer, 1, 0);
    if(semid_transfer == -1){
        perror("semget deinitializer");
        exit(1);
    }
    //arg.val = 1;
    //std::cout << "semid: " << semid << std::endl;
    //int value = semctl(semid_transfer, 0, GETVAL);
    //std::cout << "value of semaphore: " << value << std::endl;
    if(semctl(semid_transfer, 0, IPC_RMID, arg) == -1){
        perror("semctl");
        exit(1); 
    }


    key_t key_sem_balance_min = ftok("bank.h", 'Min');
    if(key_sem_balance_min == -1){   
        perror("ftok");
        exit(1);
    }
    int semid_balance_min = semget(key_sem_balance_min, 1, 0);
    if(semid_balance_min == -1){
        perror("semget deinitializer");
        exit(1);
    }
    if(semctl(semid_balance_min, 0, IPC_RMID, arg) == -1){
        perror("semctl");
        exit(1); 
    }


    key_t key_sem_balance_max = ftok("bank.h", 'Max');
    if(key_sem_balance_max == -1){   
        perror("ftok");
        exit(1);
    }
    int semid_balance_max = semget(key_sem_balance_max, 1, 0);
    if(semid_balance_max == -1){
        perror("semget deinitializer");
        exit(1);
    }
    if(semctl(semid_balance_max, 0, IPC_RMID, arg) == -1){
        perror("semctl");
        exit(1); 
    }
    exit(0);
}