#include <iostream>
#include <vector>
#include <algorithm>


int count(std::vector<int> &vec, std::vector<int> &vec_s){
    int count = 0;
    for(int i = 0; i < vec.size(); ++i){
        if(vec[i] != vec_s[i])
            count++;
    }
    if(count %2 != 0)
        count++;
    count /= 2;

    return count;
}

std::vector<int>sort_vec(std::vector<int> vec){
    std::sort(vec.begin(), vec.end());
return vec;
}

int main(){
    std::vector<int> vec{4, 7, 6, 8, 2, 3, 5};
    std::vector<int> vec_s = sort_vec(vec); // 2, 3, 4, 5, 6, 7, 8
    // for(auto el : vec_s)
    // 		std::cout << el << " ";
    // std::cout << std::endl;
    int result = count(vec, vec_s);
    std::cout << "quantity of swaps are: " << result << std::endl;


return 0;
}