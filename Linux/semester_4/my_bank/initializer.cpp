#include "bank.h"
#include <iostream>
#include <sys/shm.h>
#include <sys/sem.h>

bank_type *create_bank(int num_accounts, int max_balance){
    if(num_accounts <= 0){
        std::cout << "ARGUMENT LESS THAN 0\n";
        return NULL;
    }

    key_t key = ftok("bank.h", 'R');
    if(key < 0){
        std::cout << "ERROR, CAN'T GET KEY FOR 'bank.h'\n";
        return NULL;
    }
    size_t size = sizeof(bank_type) + num_accounts * sizeof(account_type);
    int shm_id = shmget(key, size, IPC_CREAT | IPC_EXCL | 0666);
    if(shm_id < 0){
        std::cout << "ERROR, FAILED TO CREATE SHARED MEMORY\n";
        return NULL;
    }

    void* memory = shmat(shm_id, NULL, 0);
    if(memory == (void*) -1){
        std::cout << "ERROR, FAILED TO ATTACH SHARED MEMORY\n";
        return NULL;
    }

    //creating objects with pointers (to attached memory)
    struct_bank *bank = (bank_type*) memory;
    account_type *accounts = (account_type*) ((char*) memory + sizeof(bank_type));

    bank->num_accounts = num_accounts;
    //bank->accounts = accounts;

    for(int i = 0; i < num_accounts; i++) {
        bank->accounts[i].balance = 10;
        //std::cout << i << ": " << bank->accounts[i].balance << std::endl; //checking
        bank->accounts[i].min_balance = 0;
        bank->accounts[i].max_balance = max_balance;
        bank->accounts[i].frozen = false;
    }
    //client(*bank);
    // for(int i = 0; i < num_accounts; i++) {
    //     std::cout << accounts[i].balance << std::endl;
    //     std::cout << accounts[i].min_balance << std::endl;
    //     std::cout << accounts[i].max_balance << std::endl;
    //     if(accounts[i].frozen == true){
    //         std::cout << "true\n";
    //     }
    //     else{
    //         std::cout << "false\n";
    //     }
    // }
    return bank;
}

union semun {
    int val;               /* used for SETVAL only */
    struct semid_ds *buf;  /* used for IPC_STAT and IPC_SET */
    ushort *array;         /* used for GETALL and SETALL */
};

int main(int argc, char* argv[]){
    if(argc < 3){
        std::cout << "NOT ENOUGH ARGUMENTS FOR '" << argv[0] << "'\n SHOULD BE <number of accounts> <maximum balance for accounts>\n";
        return 1;
    }
    int num_accounts, max_balance;
    num_accounts = std::atoi(argv[1]);
    max_balance = std::atoi(argv[2]);
    bank_type *bank = create_bank(num_accounts, max_balance);
    //std::cout <<  "1: " << bank->accounts[1].balance << std::endl; //checking

//freeze/unfreeze semaphore
    union semun arg;
    key_t key_semFreeze = ftok("bank.h", 'F');
    if(key_semFreeze == -1){
        perror("ftok");
        exit(1); 
    }
    int semid_freeze = semget(key_semFreeze, 1, 0666 | IPC_CREAT);
    if(semid_freeze == -1){
        perror("semget initializer");
        exit(1);
    }
    arg.val = 1;
    int value = semctl(semid_freeze, 0, GETVAL);
    if(semctl(semid_freeze, 0, SETVAL, arg) == -1){
        perror("semctl");
        exit(1);
    }

//transfer semaphore
    key_t key_sem_transfer = ftok("bank.h", 'T');
    if(key_sem_transfer == -1){
        perror("ftok");
        exit(1); 
    }
    //std::cout << "key_FREEZE: " << key_sem << std::endl;
    int semid_transfer = semget(key_sem_transfer, 1, 0666 | IPC_CREAT);
    if(semid_transfer == -1){
        perror("semget initializer");
        exit(1);
    }
    arg.val = 1;
    //std::cout << "semid: " << semid << std::endl;
    //int value = semctl(semid, 0, GETVAL);
    //std::cout << "value of semaphore: " << value << std::endl;
    if(semctl(semid_transfer, 0, SETVAL, arg) == -1){
        perror("semctl");
        //semctl(semid, 0, IPC_RMID);
        exit(1);
    }


//minimum balance semaphore
    key_t key_sem_balance_min = ftok("bank.h", 'Min');
    if(key_sem_balance_min == -1){
        perror("ftok");
        exit(1); 
    }
    int semid_balance_min = semget(key_sem_balance_min, 1, 0666 | IPC_CREAT);
    if(semid_balance_min == -1){
        perror("semget initializer");
        exit(1);
    }
    arg.val = 1;
    if(semctl(semid_balance_min, 0, SETVAL, arg) == -1){
        perror("semctl");
        exit(1);
    }



//maximum balance semaphore
    key_t key_sem_balance_max = ftok("bank.h", 'Max');
    if(key_sem_balance_max == -1){
        perror("ftok");
        exit(1); 
    }
    int semid_balance_max = semget(key_sem_balance_max, 1, 0666 | IPC_CREAT);
    if(semid_balance_max == -1){
        perror("semget initializer");
        exit(1);
    }
    arg.val = 1;
    if(semctl(semid_balance_max, 0, SETVAL, arg) == -1){
        perror("semctl");
        exit(1);
    }
    return 0;
}