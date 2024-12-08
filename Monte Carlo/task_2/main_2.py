import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chisquare
import math

# Constants for Lehmer Algorithm
N1 = 48271
N2 = 0
N3 = 10**6
X0 = 12345
n_numbers = 126000  # Size for k=7

# Lehmer Algorithm Pseudo-Random Number Generator
def lehmer_generator(n, x0, n1, n2, n3):
    x = np.zeros(n)
    x[0] = x0
    for i in range(1, n):
        x[i] = (n1 * x[i - 1] + n2) % n3
    return x / n3  # Normalize to [0, 1]

# Generate the random numbers
random_numbers = lehmer_generator(n_numbers, X0, N1, N2, N3)

# Function to perform Chi-squared tests for different orders
def chi_squared_test(random_numbers, max_order):
    observed_probs = []
    expected_probs = []
    p_values = []
    
    for order in range(3, max_order + 1):
        k_factorial = math.factorial(order)
        bin_counts = np.zeros(k_factorial)

        # Count occurrences of each tuple of length 'order'
        for i in range(len(random_numbers) - order):
            tuple_value = tuple(random_numbers[i:i + order])
            index = int(sum(x * (10 ** idx) for idx, x in enumerate(tuple_value))) % k_factorial
            bin_counts[index] += 1

        # Normalize observed frequencies
        total_count = np.sum(bin_counts)
        f_obs = bin_counts
        f_exp = np.full(k_factorial, total_count / k_factorial)  # Scale expected frequencies to match total count

        # Observed and expected probabilities
        observed_probs.append(f_obs / total_count)
        expected_probs.append(f_exp / total_count)

        # Perform Chi-squared test
        chisq_stat, p_value = chisquare(f_obs, f_exp=f_exp)
        p_values.append(p_value)
        print(f"Order {order}: Chi-squared Statistic = {chisq_stat:.2f}, P-value = {p_value:.2e}")

    return observed_probs, expected_probs, p_values

# Perform tests for increasing and decreasing orders
observed_probs_inc, expected_probs_inc, p_values_inc = chi_squared_test(random_numbers, 7)
observed_probs_dec, expected_probs_dec, p_values_dec = chi_squared_test(random_numbers[::-1], 7)

# Plot observed vs expected probabilities
orders = range(3, 8)
plt.figure(figsize=(12, 8))

# Shift value
shift = 0.1  # Increased to reduce overlap

# Plot increasing order
for i, order in enumerate(orders):
    plt.errorbar(
        order + shift,  # Shift for increasing order
        np.mean(observed_probs_inc[i]),
        yerr=np.std(observed_probs_inc[i]),
        fmt='o', markersize=10, alpha=0.8, color='blue',
        label=f'Order {order} Observed (Increasing)'
    )
    plt.plot(
        order + shift,
        np.mean(expected_probs_inc[i]),
        'rx', markersize=10, alpha=0.8,
        label=f'Order {order} Expected (Increasing)'
    )

# Plot decreasing order
for i, order in enumerate(orders):
    plt.errorbar(
        order - shift,  # Shift for decreasing order
        np.mean(observed_probs_dec[i]),
        yerr=np.std(observed_probs_dec[i]),
        fmt='s', markersize=10, alpha=0.8, color='green',
        label=f'Order {order} Observed (Decreasing)'
    )
    plt.plot(
        order - shift,
        np.mean(expected_probs_dec[i]),
        'g+', markersize=10, alpha=0.8,
        label=f'Order {order} Expected (Decreasing)'
    )

# Log scale and labels
plt.yscale('log')
plt.title('Observed vs Expected Probabilities (Log Scale)', fontsize=14)
plt.xlabel('Order', fontsize=12)
plt.ylabel('Probability (Log Scale)', fontsize=12)

# Move the legend outside the plot
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), fontsize=10)

# Adjust layout to make space for the legend
plt.tight_layout()

# Save and show the plot
plt.grid(True, which="both", linestyle='--', linewidth=0.5)
plt.savefig("probability_plot.jpg", bbox_inches='tight')  # Save with proper spacing for the legend
plt.show()
