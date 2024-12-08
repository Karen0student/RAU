import numpy as np
import matplotlib.pyplot as plt
import os

# Parameters
N_steps = [10, 20, 40, 80, 160, 320, 640, 1280]
k = 10  # number of trials for averaging
num_trials = 5  # Number of trials for smoother results

# Random walk function
def random_walk_2d(n_steps):
    x, y = 0, 0  # starting point
    for _ in range(n_steps):
        direction = np.random.choice(["up", "down", "left", "right"])
        if direction == "up":
            y += 1
        elif direction == "down":
            y -= 1
        elif direction == "right":
            x += 1
        elif direction == "left":
            x -= 1
    return np.sqrt(x**2 + y**2)  # final distance from origin

# Theoretical values for sqrt(N_step)
theoretical_d = [np.sqrt(N) for N in N_steps]

# Initialize storage for distances and uncertainties across trials
trial_distances = np.zeros((num_trials, len(N_steps)))
trial_uncertainties = np.zeros((num_trials, len(N_steps)))

# Perform trials
for trial in range(num_trials):
    for i, N in enumerate(N_steps):
        distances = [random_walk_2d(N) for _ in range(k)]
        mean_d = np.mean(distances)
        disp_d = np.var(distances, ddof=1)
        uncertainty_d = np.sqrt(disp_d)
        trial_distances[trial, i] = mean_d
        trial_uncertainties[trial, i] = uncertainty_d

# Weighted averaging across trials
avg_d = []
delta_d = []

for i in range(len(N_steps)):
    weights = 1 / trial_uncertainties[:, i]**2  # Weights inverse to the square of errors
    avg_distance = np.sum(trial_distances[:, i] * weights) / np.sum(weights)
    avg_uncertainty = 1 / np.sqrt(np.sum(weights))  # Combined uncertainty
    avg_d.append(avg_distance)
    delta_d.append(avg_uncertainty)

# Plot results
plt.figure(figsize=(10, 6))
plt.errorbar(N_steps, avg_d, yerr=delta_d, fmt='o', capsize=5, color='blue', label='Weighted <d>')
plt.plot(N_steps, theoretical_d, 'r--', label='Expected d = sqrt(N)')
plt.xlabel("N_step")
plt.ylabel("Distance d")
plt.title("Weighted Average Distance d from Origin after N Steps in 2D Random Walk")
plt.xscale("log")
plt.yscale("log")
plt.legend()
plt.grid(True)

# Save the plot
os.makedirs("plots", exist_ok=True)
plt.savefig("plots/weighted_random_walk.png")
plt.show()
