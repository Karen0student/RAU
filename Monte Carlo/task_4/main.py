import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Metropolis algorithm for random variable simulation
def metropolis_algorithm(pdf, proposal_dist, proposal_pdf, start, iterations=10000):
    samples = []
    x = start
    for i in range(iterations):
        x_proposed = proposal_dist(x)
        acceptance_ratio = min(1, pdf(x_proposed) / pdf(x) * proposal_pdf(x, x_proposed) / proposal_pdf(x_proposed, x))
        if np.random.rand() < acceptance_ratio:
            x = x_proposed
        samples.append(x)
    return np.array(samples)

# 1. Cauchy distribution (ρ(x) = c / (1 + (x-4)^2))
def pdf_cauchy(x):
    return 1 / (1 + (x - 4)**2)

def proposal_cauchy(x):
    return np.random.normal(x, 0.5)  # Normal distribution as proposal

def proposal_pdf_cauchy(x, x_prime):
    return 1 / np.sqrt(2 * np.pi * 0.5**2) * np.exp(-(x_prime - x)**2 / (2 * 0.5**2))

# Compute normalization constant for Cauchy distribution
a, b = -np.inf, np.inf
norm_cauchy, _ = quad(pdf_cauchy, a, b)

# 2. Normal distribution (ρ(x) = (1 / sqrt(2π)) * exp(-(x-4)^2 / 2))
def pdf_normal(x):
    return np.exp(-(x - 4)**2 / 2) / np.sqrt(2 * np.pi)

def proposal_normal(x):
    return np.random.normal(x, 0.5)

def proposal_pdf_normal(x, x_prime):
    return 1 / np.sqrt(2 * np.pi * 0.5**2) * np.exp(-(x_prime - x)**2 / (2 * 0.5**2))

# Compute normalization constant for Normal distribution (already normalized)
norm_normal = 1.0

# 3. Logarithmic distribution (ρ(x) = c * ln(x)), x ∈ [2, 5]
def pdf_log(x):
    return np.log(x) if x > 0 else 0  # Ensure proper domain

def proposal_log(x):
    return np.random.uniform(2, 5)  # Uniform distribution as proposal

def proposal_pdf_log(x, x_prime):
    return 1 / (5 - 2)  # Uniform PDF

# Compute normalization constant for Logarithmic distribution
a, b = 2, 5
norm_log, _ = quad(pdf_log, a, b)

# Generate samples using the Metropolis algorithm
num_of_iterations = 1000000
samples_cauchy = metropolis_algorithm(pdf_cauchy, proposal_cauchy, proposal_pdf_cauchy, 4, 10000)
samples_normal = metropolis_algorithm(pdf_normal, proposal_normal, proposal_pdf_normal, 4, num_of_iterations)
samples_log = metropolis_algorithm(pdf_log, proposal_log, proposal_pdf_log, 3, num_of_iterations)

# Plot histograms with theoretical densities
def plot_histogram_with_density(samples, bins, density, title, xlim, filename, pdf, norm_const):
    plt.figure(figsize=(8, 6))
    plt.hist(samples, bins=bins, density=density, alpha=0.7, color='skyblue', edgecolor='black', label='Simulated')
    
    # Plot theoretical density
    x = np.linspace(xlim[0], xlim[1], 1000)
    y = [pdf(val) / norm_const for val in x]
    plt.plot(x, y, color='red', label='Theoretical', linewidth=2)
    
    plt.title(title)
    plt.xlim(xlim)
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename, format='jpeg')
    plt.close()

# Plot histograms for each distribution
plot_histogram_with_density(samples_cauchy, bins=50, density=True, 
                            title="Cauchy Distribution (ρ(x) = c / (1 + (x-4)^2))", 
                            xlim=(1, 7), filename="cauchy_histogram_with_density.jpeg", 
                            pdf=pdf_cauchy, norm_const=norm_cauchy)

plot_histogram_with_density(samples_normal, bins=50, density=True, 
                            title="Normal Distribution (ρ(x) = (1 / sqrt(2π)) * exp(-(x-4)^2 / 2))", 
                            xlim=(-10, 10), filename="normal_histogram_with_density.jpeg", 
                            pdf=pdf_normal, norm_const=norm_normal)

plot_histogram_with_density(samples_log, bins=50, density=True, 
                            title="Logarithmic Distribution (ρ(x) = c * ln(x))", 
                            xlim=(2, 5), filename="log_histogram_with_density.jpeg", 
                            pdf=pdf_log, norm_const=norm_log)

print("Histograms with theoretical densities saved as JPEG.")
