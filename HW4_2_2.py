import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Given values
n = 10
sigma = 1
N = 10000

# Store simulated values
values = []

for i in range(N):

    # Generate a sample of 10 values from N(0, 1)
    sample = np.random.normal(0, sigma, n)

    # Sample variance using n - 1
    S2 = np.var(sample, ddof=1)

    # Calculate (n - 1)S^2 / sigma^2
    value = (n - 1) * S2 / sigma**2

    values.append(value)

# -------------------------------------------------
# Histogram of simulated results
# -------------------------------------------------

plt.hist(values, bins=50, density=True, alpha=0.6)

# -------------------------------------------------
# Theoretical chi-square distribution
# -------------------------------------------------

x = np.linspace(0, 30, 500)

y = stats.chi2.pdf(x, df=n - 1)

plt.plot(x, y)

plt.xlabel("(n - 1)S^2 / sigma^2")
plt.ylabel("Probability Density")
plt.title("Simulation vs Chi-Square Distribution")

plt.savefig("HW4_2_2.png")
plt.show()
