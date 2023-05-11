#include <iostream>
#include "bank.h"

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
    int account_number;
    while(true){
        std::cout << "enter account number: ";
        std::cin >> account_number;
        if(account_number >= bank->num_accounts){
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
        std::cout << "3)transfer X amount of money from account A to account B, X > 0\n";
        std::cout << "4)add/remove from all accounts X units\n";
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
        else if(option == 3){
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
            transfer(bank, account_number1, account_number2, amount);
            continue;
        }
        else if(option == 4){
            std::cout << "what would you like\n" << "1)add money\n" << "2)withdraw money\n" << "option:";
            int option;
            std::cin >> option;
            int amount;
            std::cout << "Enter amount of money: ";
            std::cin >> amount;
            add_remove_money(bank, amount, option);
            continue;
        }
    }
}