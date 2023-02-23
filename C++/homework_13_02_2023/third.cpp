#include <iostream>
#include <vector>

std::vector<int> closest_element(std::vector<int>& vec, int target, int quantity){
    int left = 0, right = vec.size() - 1;
    while (left <= right){
        int mid = left + (right - left) / 2;
        if (vec[mid] == target){ //target is the value of vector
            left = mid;
            break;
        }
        else if (target > vec[mid])
            left = mid + 1;
        else
            right = mid - 1; //for o(logn) // we don't use right side of mid value

    }

    int i = left - 1, j = left;
    //std::cout << "check values: " << i << " " << j << std::endl;

    while (quantity > 0 && (i >= 0 || j < vec.size())){
        if (i < 0){
            j++;
        }
        else if (j >= vec.size())
            i--;
        
        else if (target - vec[i] <= vec[j] - target)
            i--;
        
        else
            j++;
        
        quantity--;
    }

    std::vector<int> result;
    for (int index = i + 1; index < j; index++){
        result.push_back(vec[index]);
    }
    
return result;
}

int main(){    
    // std::vector<int> vec = {10, 12, 15, 17, 18, 20, 25};
    // int target = 16;
    // int quantity = 4;
    std::vector<int> vec;
    int vector_size;
    std::cout << "Input vector size: ";
    std::cin >> vector_size;

    std::cout << "Input target: ";
    int target;
    std::cin >> target;

    std::cout << "Input quantity of similar elements: ";
    int quantity;
    std::cin >> quantity;

    std::cout << "Input vector values: ";
    while(vector_size > 0){
        int el;
        std::cin >> el;
        vec.push_back(el);
        vector_size--;
    }

    std::vector<int> result = closest_element(vec, target, quantity);

    for (int i = 0; i < result.size(); i++){
        std::cout << result[i] << " ";
    }
    std::cout << std::endl;

return 0;
}