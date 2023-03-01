#include <iostream>
#include <string.h>
#include <sys/shm.h>

#define BLOCK_SIZE 1024
#define FILENAME "file.txt"

int main(){
    
    key_t key = ftok(FILENAME, 3);
    int shmid = shmget(key, BLOCK_SIZE, 0);
    if(shmid == -1) {
        perror("shmget error");
        exit(1);
    }

    char *data = (char*)shmat(shmid, NULL, 0);
    if(data == (char*)false){
        perror("shmat error");
        exit(1);
    }

    char element[BLOCK_SIZE];
    while(fgets(element, BLOCK_SIZE, stdin)){
        strncpy(data, element, BLOCK_SIZE-1);
        data[BLOCK_SIZE-1] = '\0';
    }

    if(shmdt(data) == -1){
        perror("shmdt error");
        exit(1);
    }
return 0;
}

