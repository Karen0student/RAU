#ifndef BANK_H
#define BANK_H

#include <fcntl.h>           /* For O_* constants */
#include <sys/stat.h>        /* For mode constants */
#include <semaphore.h>

//#include <stddef.h>

typedef struct struct_account account_type;
typedef struct struct_bank bank_type;

struct struct_account {
    int balance;
    int min_balance;
    int max_balance;
    bool frozen;
};

struct struct_bank {
    int num_accounts;
    account_type accounts[]; //object name for struct_account
};

//bank.accounts[i]

// extern const char* semaphoreNameTransfer = "transfer";
const int semaphoreInitialTransferValue = 2;
// extern const char* semaphoreNameFreezeUnfreeze = "freeze_unfreeze";
const int semaphoreInitialFreezeUnfreezeValue = 1;

bank_type *create_bank(int num_accounts, int max_balance);
void client(bank_type *bank);
void display(const bank_type *bank, int account_num);
void display_all(const bank_type *bank);
void account_freeze(bank_type *bank, int account_num);
void transfer(bank_type *bank, int account1, int account2, int amount, sem_t *sem_transfer);
void add_remove_money(bank_type *bank, int amount, int option);
void set_min_balance(bank_type *bank, int account_num, int min_balance);
void set_max_balance(bank_type *bank, int account_num, int max_balance);
#endif