import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -----------------------------
# Given information
# -----------------------------

n = 10
repeats = 10000
mu = 0
sigma = 1

np.random.seed(1)

# -----------------------------
# Generate sample means
# -----------------------------

sample_means = []

for i in range(repeats):
    sample = np.random.normal(mu, sigma, n)
    x_bar = np.mean(sample)
    sample_means.append(x_bar)

sample_means = np.array(sample_means)

# Average of the 10,000 sample means
average_xbar = np.mean(sample_means)

# Fraction of sample means above 1/sqrt(n)
limit = 1 / np.sqrt(n)
fraction_above = np.sum(sample_means > limit) / repeats

print("Average of X-bar =", average_xbar)
print("1/sqrt(n) =", limit)
print("Fraction above 1/sqrt(n) =", fraction_above)

# -----------------------------
# Plot
# -----------------------------

plt.figure()

plt.hist(sample_means, bins=40, density=True, edgecolor="black")

plt.xlabel("Sample Mean, X-bar")
plt.ylabel("Probability Density")
plt.title(
    "Sampling Distribution of X-bar\n"
    "Average = {:.4f}, Fraction above 1/sqrt(n) = {:.4f}".format(
        average_xbar, fraction_above
    )
)

plt.grid()

# Save plot
output_file = Path.cwd() / "HW3_3_1.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

print("Plot saved here:")
print(output_file)

plt.show()
