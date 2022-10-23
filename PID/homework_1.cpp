#include <iostream>
#include <sys/wait.h>
#include <unistd.h>
int main(int argc, char **argv) {

  if (argc < 1) {
    std::cout << "enter arguments";
    exit(0);
  }
  for (int i = 1; i < argc; ++i) {
    char *arg = argv[i];
    pid_t pid = fork();
    if (pid == -1) {
      std::cout << "false";
      return -1;
    }

    // child
    if (pid == 0) {
      std::cout << "child pid is: " << pid << std::endl;
      char *insert_command[]{arg, nullptr};
      execvp(arg, insert_command);
    }
    // parent
    else {
      int status;
      waitpid(pid, &status, 0);
      std::cout << " Parrent pid is: " << pid << std::endl
                << "**process finished**" << std::endl;
    }
  }

  std::cout << "***program finished***" << std::endl;
}
