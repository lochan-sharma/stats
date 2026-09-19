import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Given information
# -----------------------------

n = 100
repeats = 10000
mu = 0
sigma = 1

# Use a fixed seed so the result is reproducible
np.random.seed(1)

# -----------------------------
# Repeat the experiment
# -----------------------------

sample_means = []

for i in range(repeats):
    # Draw 100 values from a Gaussian population
    sample = np.random.normal(mu, sigma, n)

    # Compute the sample average
    x_bar = np.mean(sample)

    # Store the sample average
    sample_means.append(x_bar)

sample_means = np.array(sample_means)

# Average of all the sample averages
average_xbar = np.mean(sample_means)

print("Average of X-bar =", average_xbar)

# -----------------------------
# Plot probability density
# -----------------------------

plt.figure()

plt.hist(sample_means, bins=40, density=True, edgecolor="black")

plt.xlabel("Sample Mean, X-bar")
plt.ylabel("Probability Density")
plt.title("Distribution of X-bar, average = {:.4f}".format(average_xbar))
plt.grid()

# Save the plot
plt.savefig("HW2_3_1.png", dpi=300, bbox_inches="tight")

plt.show()
