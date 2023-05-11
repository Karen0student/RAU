#include "bank.h"
#include <iostream>
#include <sys/shm.h>

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
    int shm_id = shmget(key, size, IPC_CREAT | 0666);
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
        bank->accounts[i].balance = 0;
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

    client(bank);
    return 0;
}