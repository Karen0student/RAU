#include <iostream>
 
int fib(int number)
{
    if (number <= 1)
        return number;
    
    return fib(number- 1) + fib(number - 2);
}
 
int main()
{
    int number;
    std::cout << "enter Fibonacci number for output value: ";
    std::cin >> number;
    std::cout << "output is: " << fib(number) << std::endl;
    return 0;
}