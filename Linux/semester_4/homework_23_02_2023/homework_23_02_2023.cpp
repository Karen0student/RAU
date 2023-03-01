#include <iostream>
#include <pthread.h>
#include <stdbool.h>

pthread_mutex_t lock;
pthread_cond_t condition;
int number_char = 0;
int number_ten = 0;
int number_fifty = 0;

void *check(void *arg) {
    pthread_mutex_lock(&lock);
    while(number_fifty == 0){
        if(number_char > 10 && number_ten == 0){
            std::cout << "> 10" << std::endl;
            number_ten = 1;
        }

        if(number_char > 50){
            std::cout << "> 50" << std::endl;
            number_fifty = 1;
            break;
        }
        pthread_cond_wait(&condition, &lock);
    }

    pthread_mutex_unlock(&lock);
}

int main(){
    pthread_t thread;
    pthread_create(&thread, NULL, check, NULL);

    while(true){
        char el;
        std::cin >> el;
        if (el == EOF)
            break;

        pthread_mutex_lock(&lock);
        number_char++;
        pthread_cond_signal(&condition);
        pthread_mutex_unlock(&lock);
    }

    pthread_join(thread, NULL);

    std::cout << "characters read: " <<  number_char << std::endl;

}