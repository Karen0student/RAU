#include <iostream>
#include "bank.h"
#include <semaphore.h>
#include <unistd.h> // for sleep function
#include <sys/sem.h>

void display(const bank_type *bank, int account_num) {
    if(account_num >= bank->num_accounts){
        std::cout << "***Invalid account number***\n";
        return;
    }
    //system("clear");
    std::cout << "\naccount number: " << account_num << "     balance: " <<  bank->accounts[account_num].balance << "$      minimum balance: " <<  bank->accounts[account_num].min_balance << "$      maximum balance: " << 
            bank->accounts[account_num].max_balance << "$     account status: ";
    if(bank->accounts[account_num].frozen == true){
        std::cout << "frozen\n";
    }
    else{
        std::cout << "not frozen\n";
    }
}
void display_all(const bank_type *bank) {
    //system("clear");
    for(int i = 0; i < bank->num_accounts; ++i){
        std::cout << "\naccount number: " << i << "     balance: " <<  bank->accounts[i].balance << "$      minimum balance: " <<  bank->accounts[i].min_balance << "$      maximum balance: " << 
                bank->accounts[i].max_balance << "$     account status: ";
        if(bank->accounts[i].frozen == true){
            std::cout << "frozen\n";
        }
        else{
            std::cout << "not frozen\n";
        }
    }
}

void account_freeze(bank_type *bank, int account_num, int &semid_freeze, struct sembuf &sb) {
    if (account_num >= bank->num_accounts) {
        std::cout << "***Invalid account number***\n";
        return;
    }
    //sem_wait(sem_FreezeUnfreeze);
    sb.sem_op = -1;
    std::cout << "wait...\n";
    if(semop(semid_freeze, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }    
    while(true){
        std::cout << "\nWhat do you want\n";
        std::cout << "1) Freeze account\n" << "2) Unfreeze account\n" << "option:";
        int option;
        std::cin >> option;
        if(option == 1){
            if(bank->accounts[account_num].frozen == true){
                //system("clear");
                std::cout << "*Account already frozen*\n";
                break;
            }
            std::cout << "proccessing...\n";
            sleep(5);
            bank->accounts[account_num].frozen = true;
            //system("clear");
            std::cout << "*Account has been frozen*\n";
            break;
        }

        else if(option == 2){
            if(bank->accounts[account_num].frozen == false){
                //system("clear");
                std::cout << "*Account already unfrozen*\n";
                break;
            }
            std::cout << "proccessing...\n";
            sleep(5);
            bank->accounts[account_num].frozen = false;
            //system("clear");
            std::cout << "*Account has been unfrozen*\n";
            break;
        }
        else{
            std::cout << "***INVALID NUMBER, TRY AGAIN***\n";
            continue;
        }
        break;
    }
    //sem_post(sem_FreezeUnfreeze);
    sb.sem_op = 1;
    if(semop(semid_freeze, &sb, 1) == -1){ //release
        perror("semop client");
        exit(1);
    }  
}

void transfer(bank_type *bank, int account1, int account2, int amount, int &semid_transfer, struct sembuf &sb) {
    if(account1 >= bank->num_accounts || account2 >= bank->num_accounts) {
        std::cout << "***Invalid account number***\n";
        return;
    }
    if(bank->accounts[account1].frozen || bank->accounts[account2].frozen) {
        std::cout << "***Can't transfer, one or both of accounts are frozen***\n";
        return;
    }
    if(bank->accounts[account1].balance - amount < bank->accounts[account1].min_balance) {
        std::cout << "***Invalud amount of transfer: balance < minimum balance***\n";
        return;
    }

    if(bank->accounts[account2].balance + amount > bank->accounts[account2].max_balance) {
        std::cout << "***Invalud amount of transfer: balance > maximum balance***\n";
        return;
    }
    // int check_semaphore_value;
    // while(sem_getvalue(sem_transfer, &check_semaphore_value) != 2){
    //     std::cout << "waiting...\n";
    //     sleep(1);
    // }
    // for(int i = 0; i < 2; ++i){
    //     sem_wait(sem_transfer);
    // }
    sb.sem_op = -1;
    std::cout << "wait...\n";
    if(semop(semid_transfer, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    std::cout << "processing...\n";
    sleep(5);
    bank->accounts[account1].balance -= amount;
    bank->accounts[account2].balance += amount;
    //system("clear");
    std::cout << "Transferred: " << amount << "$ from account: "<< account1 << " to account: " << account2 << std::endl;
    // for(int i = 0; i < 2; ++i){
    //     sem_post(sem_transfer);
    // }
    sb.sem_op = 1;
    if(semop(semid_transfer, &sb, 1) == -1){ //release
        perror("semop client");
        exit(1);
    }
}

void add_remove_money(bank_type *bank, int amount, int option, int &semid_transfer, int &semid_freeze, int &semid_balance_min, int &semid_balance_max, int &semid_money, struct sembuf &sb){
    if(amount <= 0){
        std::cout <<"***Invalid amount***\n";
        return;
    }
    std::cout << "wait...\n";
    sb.sem_op = -1;
    if(semop(semid_freeze, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    sb.sem_op = -1;
    std::cout << "LOCKED FREEZE\n";

    if(semop(semid_transfer, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    sb.sem_op = -1;
    std::cout << "LOCKED TRANSFER\n";
    if(semop(semid_balance_min, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    sb.sem_op = -1;
    std::cout << "LOCKED BALANCE_MIN\n";
    if(semop(semid_balance_max, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    sb.sem_op = -1;
    std::cout << "LOCKED BALANCE_MAX\n";
    if(semop(semid_money, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    std::cout << "LOCKED MONEY\n";

    if(option == 1){
        //system("clear");
        std::cout << "processing...\n";
        for(int i = 0; i < bank->num_accounts; ++i){
            if(bank->accounts[i].frozen == true){
                std::cout << "*account: " << i << " frozen, SKIPPING*\n";
                continue;
            }
            if(bank->accounts[i].balance + amount > bank->accounts[i].max_balance && bank->accounts[i].frozen != true){ // second argument for additional protection
                std::cout << "***reached maximum balance limit for account:" << i << "  SKIPPING***\n";
                continue;
            }
            bank->accounts[i].balance += amount;
        }
    sb.sem_op = 1;
    if(semop(semid_freeze, &sb, 1) == -1){ //releaze
        perror("semop client");
        exit(1);
    }
    sb.sem_op = 1;
    std::cout << "UNLOCKED FREEZE\n";
    if(semop(semid_transfer, &sb, 1) == -1){ //releaze
        perror("semop client");
        exit(1);
    }
    sb.sem_op = 1;
    std::cout << "UNLOCKED TRANSFER\n";
    if(semop(semid_balance_min, &sb, 1) == -1){ //releaze
        perror("semop client");
        exit(1);
    }
    sb.sem_op = 1;
    std::cout << "UNLOCKED BALANCE_MIN\n";
    if(semop(semid_balance_max, &sb, 1) == -1){ //releaze
        perror("semop client");
        exit(1);
    }
    sb.sem_op = 1;
    std::cout << "UNLOCKED BALANCE_MAX\n";
    sleep(5);
    if(semop(semid_money, &sb, 1) == -1){ //releaze
        perror("semop client");
        exit(1);
    }
    std::cout << "UNLOCKED MONEY\n";
        std::cout << "**money added successfully**\n";
        return;
    }
    else if(option == 2){
        //system("clear");
        std::cout << "processing...\n";
        for(int i = 0; i < bank->num_accounts; ++i){
            if(bank->accounts[i].frozen == true){
                std::cout << "*account: " << i << " frozen, SKIPPING*\n";
                continue;
            }
            if(bank->accounts[i].balance - amount < bank->accounts[i].min_balance && bank->accounts[i].frozen != true){ // second argument for additional protection
                std::cout << "***reached minimum balance limit for account:" << i << "  SKIPPING***\n";
                continue;
            }
            bank->accounts[i].balance -= amount;
        }
        sb.sem_op = 1;
        if(semop(semid_freeze, &sb, 1) == -1){ //releaze
            perror("semop client");
            exit(1);
        }
        sb.sem_op = 1;
        std::cout << "UNLOCKED FREEZE\n";
        if(semop(semid_transfer, &sb, 1) == -1){ //releaze
            perror("semop client");
            exit(1);
        }
        sb.sem_op = 1;
        std::cout << "UNLOCKED TRANSFER\n";
        if(semop(semid_balance_min, &sb, 1) == -1){ //releaze
            perror("semop client");
            exit(1);
        }
        sb.sem_op = 1;
        std::cout << "UNLOCKED BALANCE_MIN\n";
        if(semop(semid_balance_max, &sb, 1) == -1){ //releaze
            perror("semop client");
            exit(1);
        }
        sb.sem_op = 1;
        std::cout << "UNLOCKED BALANCE_MAX\n";
        sleep(5);
        if(semop(semid_money, &sb, 1) == -1){ //releaze
            perror("semop client");
            exit(1);
        }
        std::cout << "UNLOCKED MONEY\n";
        std::cout << "**money withdrawed successfully**\n";
        return;
    }
}

void set_min_balance(bank_type *bank, int account_num, int min_balance, int &semid_balance_min, struct sembuf &sb) {
    if(account_num >= bank->num_accounts){
        std::cout << "***Invalid account number***\n";
        return;
    }
    if(bank->accounts[account_num].balance < min_balance){
        std::cout << "***FAILED: balance is less than new minimum balance***\n";
        return;
    }
    sb.sem_op = -1;
    std::cout << "wait...\n";
    if(semop(semid_balance_min, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    std::cout << "processing...\n";
    bank->accounts[account_num].min_balance = min_balance;
    sleep(5);
    sb.sem_op = 1;
    if(semop(semid_balance_min, &sb, 1) == -1){ //release
        perror("semop client");
        exit(1);
    }
    //system("clear");
    std::cout << "**MINIMUM BALANCE SET SUCCESSFULLY**\n";
    return;
}

void set_max_balance(bank_type *bank, int account_num, int max_balance, int &semid_balance_max, struct sembuf &sb) {
    if(account_num >= bank->num_accounts){
        std::cout << "***Invalid account number***\n";
        return;
    }
    if(bank->accounts[account_num].balance > max_balance){
        std::cout << "***FAILED: balance is more than new minimum balance***\n";
        return;
    }sb.sem_op = -1;
    std::cout << "wait...\n";
    if(semop(semid_balance_max, &sb, 1) == -1){ //lock
        perror("semop client");
        exit(1);
    }
    std::cout << "processing...\n";
    bank->accounts[account_num].max_balance = max_balance;
    sleep(5);
    sb.sem_op = 1;
    if(semop(semid_balance_max, &sb, 1) == -1){ //release
        perror("semop client");
        exit(1);
    }
    //system("clear");
    std::cout << "**MAXIMUM BALANCE SET SUCCESSFULLY**\n";
    return;
}
