#include <iostream>
#include <vector>

std::vector<int> merge(const std::vector<int> &first, const std::vector<int> &second){
    std::vector<int> result;
    int i = 0, j = 0;

    while (i < first.size() && j < second.size()) {
        if (first[i] < second[j]) {
            result.push_back(first[i]);
            i++;
        } else {
            result.push_back(second[j]);
            j++;
        }
    }

    while (i < first.size()) {
        result.push_back(first[i]);
        i++;
    }

    while (j < second.size()) {
        result.push_back(second[j]);
        j++;
    }

    return result;
}

std::vector<int> merge_sort(const std::vector<int> &vec, int start, int end){
    if(end - start == 1)
        return {vec[start]};

    int middle = (end + start) / 2;
    return merge(merge_sort(vec, start, middle), merge_sort(vec, middle, end));
}

std::vector<int> merge_sort(std::vector<int> &vec){
    return merge_sort(vec, 0, vec.size());
}

int main() {
    std::vector<int> vec{12, 5, 6, 8, 4, 8, 8, 6, 2, 3, 9};

    vec = merge_sort(vec);

    for (const auto &v : vec)
        std::cout << v << " ";
    std::cout << std::endl;

    return 0;
}