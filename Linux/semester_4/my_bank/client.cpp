#include <iostream>
#include <sys/shm.h>
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

void client(bank_type *bank){
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
            account_freeze(bank, account_number);
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
            transfer(bank, account_number1, account_number2, amount);
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
                set_max_balance(bank, account_number, maximum_balance);
                continue;
            }
            if(option == 2){
                std::cout << "Enter account number: ";
                int account_number;
                std::cin >> account_number;
                std::cout << "Enter new minimum balance: ";
                int minimum_balance;
                std::cin >> minimum_balance;
                set_min_balance(bank, account_number, minimum_balance);
                continue;
            }
        }
        else if(option == "7"){
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