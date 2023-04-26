#include "bank.h"

void display(){

}

void change_freeze(){

}

void transfer(){

}

void credit(){

}

void set_balance(){

}

void menu(){
    while(true){
        std::cout << "enter option:\n1)display the current/minimum/maximum account balance\n";
        std::cout << "2)freeze/unfreeze an account\n";
        std::cout << "3)transfer amount X from account A to account B, X > 0\n";
        std::cout << "4)credit to all accounts / write off from all accounts X units\n";
        std::cout << "5)set the given minimum/maximum possible balance X for the account with the given number A\n";
        std::cout << "option: ";
        int option;
        std::cin >> option;
        if(option == 1){
            system("clear");
            display();
        }
        else if(option == 2){
            system("clear");
            change_freeze();
        }
        else if(option == 3){
            system("clear");
            transfer();
        }
        else if(option == 4){
            system("clear");
            credit();
        }
        else if(option == 5){
            system("clear");
            set_balance();
        }
        else{
            std::cout << "\n**CHOOSE BETWEEN 1-6, TRY AGAIN**\n\n";
            continue;
        }
    }
}

int main(int argc, char** argv){
    if(argc < 2){
        perror("***NOT ENOUGH ARGUMENTS***");
        exit(0); //SUCCESS ? 
    }

    check.resize(atoi(argv[1]));
    menu();
}