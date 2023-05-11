#include <iostream>
#include "bank.h"

int check_account_number(bank_type *bank){
    int account_number;
    while(true){
        std::cout << "enter account number: ";
        std::cin >> account_number;
        if(account_number > bank->num_accounts){
            std::cout << "***incorrect number, try again***\n";
            continue;
        }
        break;
    }
    return account_number;
}

void client(bank_type *bank){
    while(true){
        std::cout << "\n1)display the current/minimum/maximum account balance\n";
        std::cout << "2)freeze/unfreeze an account\n";
        std::cout << "3)transfer amount X from account A to account B, X > 0\n";
        std::cout << "4)credit to all accounts / write off from all accounts X units\n";
        std::cout << "5)set the given minimum/maximum possible balance X for the account with the given number A\n";
        std::cout << "enter option: ";
        int option;
        std::cin >> option;

        if(option == 1){
            int account_number = check_account_number(bank);
            display(bank, account_number);
            continue;
        }
        else if(option == 2){
            int account_number = check_account_number(bank);
            account_freeze(bank, account_number);
            continue;
        }

    }
}