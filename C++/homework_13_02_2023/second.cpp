#include <iostream>
#include <vector>

int Peek(std::vector<int> vec, int left, int right) {
    int mid = (left + right) / 2;
    if(mid > 0 && vec[mid - 1] > vec[mid]){
        return Peek(vec, left, mid - 1);
    } else if (mid < right && vec[mid + 1] > vec[mid]) {
        return Peek(vec, mid + 1, right);
    } else {
        return mid;
    }
}

int Peek1(std::vector<int> vec, int left, int right) {
    int mid = (left + right) / 2;
    
    if (mid < right && vec[mid + 1] > vec[mid]) {
        return Peek(vec, mid + 1, right);
    } 
    else if(mid > 0 && vec[mid - 1] > vec[mid]){
        return Peek(vec, left, mid - 1);
    }
    else {
        return mid;
    }
}

int main() {
    std::vector<int> vec{10, 20, 15, 2, 23, 90, 67};
    
    int result = Peek(vec, 0, vec.size() - 1);
    std::cout <<"Answer: "<< vec[result];
    result = Peek1(vec, 0, vec.size() - 1);
    std::cout <<" OR "<< vec[result] << std::endl;
    return 0;
}
