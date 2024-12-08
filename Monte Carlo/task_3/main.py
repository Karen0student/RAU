import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import root_scalar
import os


def pdf_1(x, c):
    return c * x * np.exp(-x**2)

def pdf_2(x, c):
    return c * x * np.cos(x**2)

def pdf_3(x, c):
    return c * np.exp(x)

def pdf_4(x, c):
    return c * x / (1 + x**2)

def calculate_c(pdf, a, b):
    integral, _ = quad(lambda x: pdf(x, 1), a, b)
    return 1 / integral


# Rejection Sampling for both PDFs
def rejection_sampling(pdf, c, a, b, max_pdf, n_samples):
    samples = []
    while len(samples) < n_samples:
        x = np.random.uniform(a, b)
        y = np.random.uniform(0, max_pdf)
        if y < pdf(x, c):
            samples.append(x)
    return np.array(samples)


# Inverse CDF Sampling for PDFs
def inverse_cdf_sampling(cdf_inv, n_samples):
    u = np.random.uniform(0, 1, n_samples)  # Generate U(0,1) samples
    return np.array([cdf_inv(ui) for ui in u])


# PDF 1: Inverse CDF using root-finding
def cdf_inv_pdf_1(u, c):
    def equation(x):
        return quad(lambda t: pdf_1(t, c), 1, x)[0] - u
    return root_scalar(equation, bracket=[1, 3]).root


# PDF 3: Analytic Inverse CDF (since it's exponential over [0, 2])
def cdf_inv_pdf_3(u, c):
    x = np.log(u * (np.exp(2) - 1) + 1)
    return min(max(x, 0), 2)  # Ensure x is within [0, 2]


def simulate_pdf_1(n_samples, method='rejection'):
    a, b = 1, 3
    c = calculate_c(pdf_1, a, b)
    max_pdf = pdf_1(1, c)
    if method == 'rejection':
        return rejection_sampling(pdf_1, c, a, b, max_pdf, n_samples)
    else:
        return inverse_cdf_sampling(lambda u: cdf_inv_pdf_1(u, c), n_samples)


def simulate_pdf_2(n_samples, method='rejection'):
    a, b = 0, np.pi / 3
    c = calculate_c(pdf_2, a, b)
    x_vals = np.linspace(a, b, 1000)
    max_pdf = np.max(pdf_2(x_vals, c))  # Find the maximum value of the PDF
    if method == 'rejection':
        return rejection_sampling(pdf_2, c, a, b, max_pdf, n_samples)
    else:
        return rejection_sampling(pdf_2, c, a, b, max_pdf, n_samples)


def simulate_pdf_3(n_samples, method='rejection'):
    a, b = 0, 2
    c = calculate_c(pdf_3, a, b)
    max_pdf = pdf_3(b, c)
    if method == 'rejection':
        return rejection_sampling(pdf_3, c, a, b, max_pdf, n_samples)
    else:
        return inverse_cdf_sampling(lambda u: cdf_inv_pdf_3(u, c), n_samples)


def simulate_pdf_4(n_samples, method='rejection'):
    a, b = 0, 4  # Valid range for this PDF
    c = calculate_c(pdf_4, a, b)
    x_vals = np.linspace(a, b, 1000)
    max_pdf = np.max(pdf_4(x_vals, c))  # Find the maximum value of the PDF
    if method == 'rejection':
        return rejection_sampling(pdf_4, c, a, b, max_pdf, n_samples)
    else:
        return rejection_sampling(pdf_4, c, a, b, max_pdf, n_samples)


def plot_histogram(samples, pdf, c, a, b, title, filename, bins=50):
    plt.figure()
    plt.hist(samples, bins=bins, density=True, alpha=0.6, color='b', label="Sampled Data")
    x_vals = np.linspace(a, b, 1000)
    theoretical_pdf = pdf(x_vals, c)
    plt.plot(x_vals, theoretical_pdf, 'r', label="Theoretical PDF")
    plt.legend()
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("Density")
    os.makedirs("histograms", exist_ok=True)
    plt.savefig(f"histograms/{filename}.png")
    plt.close()


n_samples = 10000  # Increased number of samples
# PDF 1 - Rejection and Inverse CDF Sampling
samples_pdf_1_rejection = simulate_pdf_1(n_samples, method='rejection')
samples_pdf_1_inverse = simulate_pdf_1(n_samples, method='inverse')

print("First 10 samples (Rejection Sampling) for PDF 1:", samples_pdf_1_rejection[:10])
print("First 10 samples (Inverse CDF Sampling) for PDF 1:", samples_pdf_1_inverse[:10])

plot_histogram(samples_pdf_1_rejection, pdf_1, calculate_c(pdf_1, 1, 3), 1, 3, "PDF 1 - Rejection Sampling", "pdf_1_rejection")
plot_histogram(samples_pdf_1_inverse, pdf_1, calculate_c(pdf_1, 1, 3), 1, 3, "PDF 1 - Inverse CDF Sampling", "pdf_1_inverse")


# PDF 2 - Rejection and Inverse CDF Sampling
samples_pdf_2_rejection = simulate_pdf_2(n_samples, method='rejection')
samples_pdf_2_inverse = simulate_pdf_2(n_samples, method='inverse')

print("First 10 samples (Rejection Sampling) for PDF 2:", samples_pdf_2_rejection[:10])
print("First 10 samples (Inverse CDF Sampling) for PDF 2:", samples_pdf_2_inverse[:10])

plot_histogram(samples_pdf_2_rejection, pdf_2, calculate_c(pdf_2, 0, np.pi / 3), 0, np.pi / 3, "PDF 2 - Rejection Sampling", "pdf_2_rejection")
plot_histogram(samples_pdf_2_inverse, pdf_2, calculate_c(pdf_2, 0, np.pi / 3), 0, np.pi / 3, "PDF 2 - Inverse CDF Sampling", "pdf_2_inverse")


# PDF 3 - Rejection and Inverse CDF Sampling
samples_pdf_3_rejection = simulate_pdf_3(n_samples, method='rejection')
samples_pdf_3_inverse = simulate_pdf_3(n_samples, method='inverse')

print("First 10 samples (Rejection Sampling) for PDF 3:", samples_pdf_3_rejection[:10])
print("First 10 samples (Inverse CDF Sampling) for PDF 3:", samples_pdf_3_inverse[:10])

plot_histogram(samples_pdf_3_rejection, pdf_3, calculate_c(pdf_3, 0, 2), 0, 2, "PDF 3 - Rejection Sampling", "pdf_3_rejection")
plot_histogram(samples_pdf_3_inverse, pdf_3, calculate_c(pdf_3, 0, 2), 0, 2, "PDF 3 - Inverse CDF Sampling", "pdf_3_inverse")


# PDF 4 - Rejection and Inverse CDF Sampling
samples_pdf_4_rejection = simulate_pdf_4(n_samples, method='rejection')
samples_pdf_4_inverse = simulate_pdf_4(n_samples, method='inverse')

print("First 10 samples (Rejection Sampling) for PDF 4:", samples_pdf_4_rejection[:10])
print("First 10 samples (Inverse CDF Sampling) for PDF 4:", samples_pdf_4_inverse[:10])

plot_histogram(samples_pdf_4_rejection, pdf_4, calculate_c(pdf_4, 0, 4), 0, 4, "PDF 4 - Rejection Sampling", "pdf_4_rejection")
plot_histogram(samples_pdf_4_inverse, pdf_4, calculate_c(pdf_4, 0, 4), 0, 4, "PDF 4 - Inverse CDF Sampling", "pdf_4_inverse")
