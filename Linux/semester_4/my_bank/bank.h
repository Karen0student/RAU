#ifndef BANK_H
#define BANK_H

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

bank_type *create_bank(int num_accounts, int max_balance);
void client(bank_type *bank);
void display(const bank_type *bank, int account_num);
void account_freeze(bank_type *bank, int account_num);


#endif