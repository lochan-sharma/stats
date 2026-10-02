import numpy as np
from scipy import stats
import math

# True population values
mu = 10
sigma = 2

# Sample size
n = 20

# Number of experiments
N = 1000

# 95% confidence interval
alpha = 0.05

# Count how many confidence intervals contain mu
trapped = 0

for i in range(N):

    # Take a random sample
    sample = np.random.normal(mu, sigma, n)

    # Calculate sample mean
    xbar = np.mean(sample)

    # Calculate sample standard deviation
    s = np.std(sample, ddof=1)

    # t critical value
    tcrit = stats.t.ppf(1 - alpha/2, n - 1)

    # Margin of error
    margin = tcrit * s / math.sqrt(n)

    # Confidence interval
    lower = xbar - margin
    upper = xbar + margin

    # Check if true mean is inside the interval
    if lower <= mu <= upper:
        trapped = trapped + 1

# Calculate percentage
percentage = trapped / N * 100

print("Number of intervals =", N)
print("Intervals that trapped mu =", trapped)
print("Percentage that trapped mu =", percentage, "%")
