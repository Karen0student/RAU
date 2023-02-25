#include <iostream>
#include <vector>

int merge(std::vector<int> &vec, int left, int mid, int right){
    int count = 0;
    int index1 = mid - left + 1;
    int index2 = right - mid;
    
    std::vector<int> first_vec(index1);
    std::vector<int> second_vec(index2);

    for(int i = 0; i < index1; ++i)
        first_vec[i] = vec[left + i];
    for(int i = 0; i < index1; ++i)
        second_vec[i] = vec[mid + 1 + i];

    int i = 0;
    int j = 0;
    int k = left;
    while(i < index1 && j < index2){
        if(first_vec[i] < second_vec[j]){
            vec[k] = first_vec[i];
            k++;
            i++;
        }
        else{
            vec[k] = second_vec[j];
            count+= index1 - i;
            k++;
            j++;
        }

    }
    while(i < index1){
        vec[k] = first_vec[i];
        k++;
        i++;
    }
    while(i < index2){
        vec[k] = second_vec[j];
        k++;
        i++;
    }
return count;
}

int merge_sort(std::vector<int> &vec, int left, int right){
    int count = 0;
    if(left < right){
        int mid = (left+right)/2;
        count += merge_sort(vec, left, mid);
        count += merge_sort(vec, mid+1, right);
        count += merge(vec, left, mid, right);
    }
return count;
}
int main(){
    std::vector<int> vec;
    std::cout << "enter array size: ";
    int size;
    std::cin >> size;
    std::cout << "enter elements to sort: ";
    for(int i = 0; i < size; ++i){
        int element;
        std::cin >> element;
        vec.push_back(element);
        //vec[i] = element;
    }
    
    int left = 0;
    int right = vec.size()-1;
    int quantity = merge_sort(vec, left, right);
    std::cout << std::endl << "sorted array: ";
    for(auto el : vec)
        std::cout << el << " ";
        
    std::cout << std::endl << "quantity of swaps: " << quantity << std::endl;

return 0;
}