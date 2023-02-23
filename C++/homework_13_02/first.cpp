#include <iostream>
#include <vector>
#include <unordered_map>
#include <algorithm>

//12 11 13 5 6   
void insertion_sort(std::vector<int> &vec1, std::vector<int> &vec2){
    int j;
    for(int i = 1; i < vec2.size(); ++i){
        j = i;
        while(j > 0 && vec2[j-1] < vec2[j]){
            std::swap(vec2[j-1], vec2[j]);
            std::swap(vec1[j-1], vec1[j]);
            j--;
        }
    }
}

void sort_map(std::vector<int> &vec){
    std::unordered_map<int, int> my_map;
    for(auto el : vec)
        my_map[el]++;

    std::vector<int> vec1, vec2;
    for(auto el : my_map)
        vec1.push_back(el.first);

    for(auto el : my_map)
        vec2.push_back(el.second);


    insertion_sort(vec1, vec2);
    for(int i = 0; i < vec1.size(); ++i){
        while(vec2[i] > 0){
            std::cout << vec1[i] << " ";
            vec2[i]--;
        }
    }
}

int main(){
    std::vector<int> vec {3, 6, 3, 9, 6, 4, 9, 9};
    //insertion_sort(vec);
    sort_map(vec);
    std::cout << std::endl;
return 0;
}