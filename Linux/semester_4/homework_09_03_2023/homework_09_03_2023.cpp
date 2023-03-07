#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <semaphore.h>
#include <sys/shm.h>
#include <sys/wait.h>
#include <iostream>

int main(int argc, char** argv){

    if(argc < 2){
        perror("not enough arguments");
        exit(EXIT_FAILURE);
    }
    
    key_t shm_key = ftok("text.txt", 3);
    int shm_id = shmget(shm_key, sizeof(int), 0777 | IPC_CREAT);
    if (shm_id < 0)
    {
        perror("shmgget");
        exit(EXIT_FAILURE);
    }
    int* print_value = (int*)shmat(shm_id, NULL, 0);
    *print_value = 0;

    sem_t* semaphore = sem_open("semaphore", O_CREAT | O_EXCL, 0777, 1);

    int quantity = atoi(argv[1]);
    pid_t pid;
    for(int i = 0; i < quantity; i++)
    {
        pid = fork();
        if (pid < 0)
        {
            perror("fork");
            sem_unlink("semaphore");
            sem_close(semaphore);
            exit(EXIT_FAILURE);
        }
        else if (pid == 0){break;}
    }
    
    if(pid == 0)
    {
        //child process
        sem_wait(semaphore);
        //sleep(1);
        *print_value += 1;
        std::cout << *print_value << " ";
        sem_post(semaphore); //release
        exit(EXIT_SUCCESS);
    }
    else{
        //parent process
        while(pid = waitpid(-1, NULL, 0))
            if(errno == ECHILD){break;}

        shmctl(shm_id, IPC_RMID, 0);
        shmdt(print_value);
        sem_unlink("semaphore"); // removes named semaphore
        sem_close(semaphore);    // frees resources
        std::cout << std::endl;
        exit(0);
    }
}
