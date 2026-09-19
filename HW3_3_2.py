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
# Generate S_b^2 values
# -----------------------------

sb2_values = []

for i in range(repeats):
    # Draw 10 values from a normal distribution
    sample = np.random.normal(mu, sigma, n)

    # Compute sample mean
    x_bar = np.mean(sample)

    # Compute biased sample variance S_b^2
    sb2 = np.sum((sample - x_bar) ** 2) / n

    # Store it
    sb2_values.append(sb2)

sb2_values = np.array(sb2_values)

# Average and variance of the 10,000 S_b^2 values
average_sb2 = np.mean(sb2_values)
variance_sb2 = np.var(sb2_values)

print("Average of S_b^2 =", average_sb2)
print("Variance of S_b^2 =", variance_sb2)

# -----------------------------
# Plot
# -----------------------------

plt.figure()

plt.hist(sb2_values, bins=40, density=True, edgecolor="black")

plt.xlabel("S_b^2")
plt.ylabel("Probability Density")
plt.title(
    "Sampling Distribution of S_b^2\n"
    "Average = {:.4f}, Variance = {:.4f}".format(
        average_sb2, variance_sb2
    )
)

plt.grid()

# Save plot
output_file = Path.cwd() / "HW3_3_2.png"
plt.savefig(output_file, dpi=300, bbox_inches="tight")

print("Plot saved here:")
print(output_file)

plt.show()
