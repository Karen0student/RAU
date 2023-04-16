#include <iostream>
#include <vector>
#include <algorithm>

int rob(std::vector<int>& money_in_house) {
    int n = money_in_house.size();
    if (n == 0) {
        return 0;
    }
    if (n == 1) {
        return money_in_house[0];
    }
    std::vector<int> dp(n);
    dp[0] = money_in_house[0];
    dp[1] = std::max(money_in_house[0], money_in_house[1]);
    for (int i = 2; i < n; i++) {
        dp[i] = std::max(money_in_house[i] + dp[i-2], dp[i-1]);
        std::cout << dp[i] << " ";
    }
    std::sort(dp.begin(), dp.end());
    std::cout << "\nFinal result: ";
    return dp[dp.size() - 1];
}

int main() {
    std::vector<int> money_in_house = {10000, 45000, 22000, 71000, 29000, 10000, 1000};
    std::cout << rob(money_in_house) << std::endl;
    return 0;
}