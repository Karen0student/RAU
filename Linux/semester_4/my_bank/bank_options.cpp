#include <iostream>
#include "bank.h"

void display(const bank_type *bank, int account_num) {
    if(account_num >= bank->num_accounts) {
        std::cout << "***Invalid account number***\n";
        return;
    }

    std::cout << "\naccount number: " << account_num << "     balance: " <<  bank->accounts[account_num].balance << "      minimum balance: " <<  bank->accounts[account_num].min_balance << "      maximum balance: " << 
        bank->accounts[account_num].max_balance << "     account status: ";
        if(bank->accounts[account_num].frozen == true){
            std::cout << "frozen\n";
        }
        else{
            std::cout << "not frozen\n";
        }
}

void account_freeze(bank_type *bank, int account_num) {
    if (account_num >= bank->num_accounts) {
        std::cout << "***Invalid account number***\n";
        return;
    }
    while(true){
        std::cout << "\nWhat do you want\n";
        std::cout << "1) Freeze account\n" << "2) Unfreeze account\n" << "option:";
        int option;
        std::cin >> option;
        if(option == 1){
            if(bank->accounts[account_num].frozen == true){
                std::cout << "Account already frozen\n";
                break;
            }
            bank->accounts[account_num].frozen = true;
            std::cout << "Account has been frozen\n";
            break;
        }
        else if(option == 2){
            if(bank->accounts[account_num].frozen == false){
                std::cout << "Account already unfrozen\n";
                break;
            }
            bank->accounts[account_num].frozen = false;
            std::cout << "Account has been unfrozen\n";
            break;
        }
        else{
            std::cout << "***INVALID NUMBER, TRY AGAIN***\n";
            continue;
        }
        break;
    }
}

