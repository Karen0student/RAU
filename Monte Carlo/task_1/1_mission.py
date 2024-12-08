import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Exact integrals
def I1_exact():
    return quad(lambda x: x * np.exp(-x**2), -1, 3)[0]

def I2_exact():
    return quad(lambda x: x * np.sin(x**2), 0, 2)[0]

def I3_exact():
    return quad(lambda x: x / (1 + x**2), 0.5, 2.5)[0]

def I4_exact():
    return quad(lambda x: x**2 * np.exp(-x**3), 0, 1)[0]

# Simple Monte Carlo method
def simple_monte_carlo(f, a, b, N):
    random_points = np.random.uniform(a, b, N)
    return (b - a) * np.mean(f(random_points))

# Geometric Monte Carlo method
def geometric_monte_carlo(f, a, b, N):
    random_points = np.random.uniform(a, b, N)
    #weights = np.abs(f(random_points))  # Absolute function values
    weights = f(random_points)
    #return (b - a) * np.sum(weights) / N
    return (b - a) * np.mean(weights)

# Functions and bounds
functions = [
    (lambda x: x * np.exp(-x**2), (-1, 3)),
    (lambda x: x * np.sin(x**2), (0, 2)),
    (lambda x: x / (1 + x**2), (0.5, 2.5)),
    (lambda x: x**2 * np.exp(-x**3), (0, 1)),
]

# Exact integral values
I_exact = [I1_exact(), I2_exact(), I3_exact(), I4_exact()]

# MC parameters
N_tot_values = [100, 1000, 10000, 100000, 1000000]

# Arrays to store errors
eps_simple = np.zeros((4, len(N_tot_values)))
eps_geometric = np.zeros((4, len(N_tot_values)))

# Monte Carlo Integration
for i, ((f, (a, b)), I) in enumerate(zip(functions, I_exact)):
    print(f"Analyzing Integral {i+1}...")
    for j, N_tot in enumerate(N_tot_values):
        # Simple Monte Carlo
        I_mc_simple = simple_monte_carlo(f, a, b, N_tot)
        eps_simple[i, j] = np.abs(I - I_mc_simple)

        # Geometric Monte Carlo
        I_mc_geometric = geometric_monte_carlo(f, a, b, N_tot)
        eps_geometric[i, j] = np.abs(I - I_mc_geometric)

        # Log results
        print(f"  N_tot={N_tot}: Simple MC={I_mc_simple:.6f}, Geometric MC={I_mc_geometric:.6f}, Exact={I:.6f}")

# Plotting Errors
plt.figure(figsize=(12, 8))

for i in range(4):
    plt.plot(N_tot_values, eps_simple[i], label=f'I{i+1} Simple MC', linestyle='--', marker='o')
    plt.plot(N_tot_values, eps_geometric[i], label=f'I{i+1} Geometric MC', linestyle='-', marker='s')

plt.xscale('log')
plt.yscale('log')
plt.xlabel(r'$N_{\mathrm{tot}}$', fontsize=14)
plt.ylabel(r'$\epsilon = |\mathrm{I}_{\mathrm{exact}} - \mathrm{I}_{\mathrm{MC}}|$', fontsize=14)
plt.legend(fontsize=12)
plt.title('Error $\epsilon$ as a function of $N_{\mathrm{tot}}$', fontsize=16)
plt.grid(True)

plt.savefig("monte_carlo_errors_plot.jpg")
#plt.show()
