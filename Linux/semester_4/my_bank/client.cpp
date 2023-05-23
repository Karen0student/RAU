#include <iostream>
#include <sys/ipc.h>
#include <sys/sem.h>
#include <sys/shm.h>
#include "bank.h"
#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <semaphore.h>
#include <unistd.h> //for sleep function


int check_given_account_number(bank_type *bank, int account_number){
     while(true){
        if(account_number >= bank->num_accounts){
            std::cout << "***incorrect number, try again***\n";
            std::cout << "enter account number: ";
            std::cin >> account_number;
            continue;
        }
        break;
    }
    return account_number;
}

int check_account_number(bank_type *bank){
    std::string account_number;
    while(true){
        std::cout << "enter account number: ";
        std::cin >> account_number;
        if(std::stoi(account_number) >= bank->num_accounts){
            std::cout << "***incorrect number, try again***\n";
            continue;
        }
        break;
    }
    return std::stoi(account_number);
}

// union semun {
//     int val;               /* used for SETVAL only */
//     struct semid_ds *buf;  /* used for IPC_STAT and IPC_SET */
//     ushort *array;         /* used for GETALL and SETALL */
// };
void client(bank_type *bank){
    //union semun arg;
    struct sembuf sb = {0, -1, 0};

//taking FREEZE id
    key_t key_semFreeze = ftok("bank.h", 'F');
    if(key_semFreeze == -1){   
        perror("ftok");
        exit(1); 
    }
    int semid_freeze = semget(key_semFreeze, 1, 0);
    if(semid_freeze == -1){
        perror("semget client");
        exit(1);
    }

//taking TRANSFER id
    key_t key_sem_transfer = ftok("bank.h", 'F');
    if(key_sem_transfer == -1){   
        perror("ftok");
        exit(1); 
    }
    int semid_transfer = semget(key_sem_transfer, 1, 0);
    if(semid_transfer == -1){
        perror("semget client");
        exit(1);
    }

//taking MINIMUM BALANCE id
    key_t key_sem_balance_min = ftok("bank.h", 'Min');
    if(key_sem_transfer == -1){   
        perror("ftok");
        exit(1); 
    }
    int semid_balance_min = semget(key_sem_balance_min, 1, 0);
    if(semid_balance_min == -1){
        perror("semget client");
        exit(1);
    }

//taking MAXIMUM BALANCE id
    key_t key_sem_balance_max = ftok("bank.h", 'Max');
    if(key_sem_transfer == -1){   
        perror("ftok");
        exit(1); 
    }
    int semid_balance_max = semget(key_sem_balance_max, 1, 0);
    if(semid_balance_max == -1){
        perror("semget client");
        exit(1);
    }


//TESTING SEMAPHORE
    //std::cout << "semid: " << semid << std::endl;
    // if(semop(semid, &sb, 1) == -1){
    //     perror("semop");
    //     exit(1);
    // }
    // std::cout << "LOCKED\n";
    // sleep(3);
    // sb.sem_op = 1;
    // if(semop(semid, &sb, 1) == -1){
    //     perror("semop");
    //     exit(1);
    // }    std::cout << "UNLOCKED\n";
    
    while(true){
        std::cout << "\n1)display the current/minimum/maximum account balance\n";
        std::cout << "2)display all accounts\n";
        std::cout << "3)freeze/unfreeze an account\n";
        std::cout << "4)transfer X amount of money from account A to account B, X > 0\n";
        std::cout << "5)add/remove from all accounts X units\n";
        std::cout << "6)set the given minimum/maximum possible balance X for the account with the given number A\n";
        std::cout << "7)Exit\n";
        std::cout << "enter option: ";
        std::string option;
        std::cin >> option;

        if(option == "1"){
            int account_number = check_account_number(bank);
            display(bank, account_number);
            continue;
        }
        else if(option == "2"){
            display_all(bank);
            continue;
        }
        else if(option == "3"){
            int account_number = check_account_number(bank);
            // int check_semaphore_value;
            // while(sem_getvalue(sem_FreezeUnfreeze, &check_semaphore_value) == 0){
            //     std::cout << "value: " << sem_getvalue(sem_FreezeUnfreeze, &check_semaphore_value);
            //     std::cout << " waiting...\n";
            //     sleep(1);
            // }
            //sem_wait(sem_FreezeUnfreeze);
            // if(semop(semid, &sb, 1) == -1){ //lock
            //     perror("semop");
            //     exit(1);
            // }
            std::cout << "wait...\n";
            account_freeze(bank, account_number, semid_freeze, sb);
            // sb.sem_op = 1;
            // if(semop(semid, &sb, 1) == -1){ //release
            //     perror("semop");
            //     exit(1);
            // }
            continue;
        }
        else if(option == "4"){
            int account_number1, account_number2;
            std::cout << "Enter first account number: ";
            std::cin >> account_number1;
            account_number1 = check_given_account_number(bank, account_number1);
            std::cout << "Enter second account number: ";
            std::cin >> account_number2;
            account_number2 = check_given_account_number(bank, account_number2);
            std::cout << "Enter amount to transfer: ";
            int amount;
            std::cin >> amount;
            transfer(bank, account_number1, account_number2, amount, semid_transfer, sb);
            continue;
        }
        else if(option == "5"){
            std::cout << "what would you like\n" << "1)add money\n" << "2)withdraw money\n" << "option:";
            int option;
            std::cin >> option;
            int amount;
            std::cout << "Enter amount of money: ";
            std::cin >> amount;
            add_remove_money(bank, amount, option);
            continue;
        }
        else if(option == "6"){
            std::cout << "what would you like\n" << "1)set new maximum balance\n" << "2)set new minimum balance\n" << "option: ";
            int option;
            std::cin >> option;
            if(option == 1){
                std::cout << "Enter account number: ";
                int account_number;
                std::cin >> account_number;
                std::cout << "Enter new maximum balance: ";
                int maximum_balance;
                std::cin >> maximum_balance;
                set_max_balance(bank, account_number, maximum_balance, semid_balance_max, sb);
                continue;
            }
            if(option == 2){
                std::cout << "Enter account number: ";
                int account_number;
                std::cin >> account_number;
                std::cout << "Enter new minimum balance: ";
                int minimum_balance;
                std::cin >> minimum_balance;
                set_min_balance(bank, account_number, minimum_balance, semid_balance_min, sb);
                continue;
            }
        }
        else if(option == "7"){ //exiting client
            return;
        }
        else{
            std::cout << "***incorrect number, try again***\n";
            continue;
        }
    }
    return; // not necessary
}


int main(int argc, char* argv[]){
    if(argc < 2){
        std::cout << "***ERROR: SHOULD BE <number of accounts>***\n";
        exit(1);
    }
    int num_accounts = std::atoi(argv[1]);

    // sem_unlink(SEM_ONE_FNAME); //removing semaphores to be sure it's not working right now
    // sem_unlink(SEM_TWO_FNAME);
    // sem_t *sem_one = sem_open(SEM_ONE_FNAME, IPC_CREAT, 0666, 1);
    // if(sem_one == SEM_FAILED){
    //     std::cout << "***ERROR, CAN'T CREATE SEMAPHORE***\n";
    //     exit(EXIT_FAILURE);
    // }
    // sem_t *sem_two = sem_open(SEM_TWO_FNAME, IPC_CREAT, 0666, 1);
    // if(sem_two == SEM_FAILED){
    //     std::cout << "***ERROR, CAN'T CREATE SEMAPHORE***\n";
    //     exit(EXIT_FAILURE);
    // }

    key_t key = ftok("bank.h", 'R');
    if(key < 0){
        std::cout << "***ERROR, CAN'T GET KEY FOR 'bank.h'***\n";
        exit(1);
    }

    size_t size = sizeof(bank_type) + num_accounts * sizeof(account_type);
    int shm_id = shmget(key, size, 0);
    if(shm_id < 0){
        std::cout << "***ERROR, FAILED TO CREATE SHARED MEMORY***\n";
        exit(1);
    }

    void* memory = shmat(shm_id, NULL, 0);
    if(memory == (void*) -1){
        std::cout << "***ERROR, FAILED TO ATTACH SHARED MEMORY***\n";
        exit(1);
    }

    struct_bank *bank = (bank_type*) memory; //creating object bank + attaching to shared segment

    client(bank);   
    
return 0;
}