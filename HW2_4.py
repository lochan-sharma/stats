import numpy as np
import matplotlib.pyplot as plt
from math import comb, sqrt, pi, exp

# Given values
n = 100
p = 0.4
q = 1 - p
N = 10000

# -------------------------
# Part 1: Simulation
# -------------------------

results = np.random.binomial(n, p, N)

x = np.arange(0, n + 1)

counts = np.bincount(results, minlength=n + 1)

P_sim = counts / N

# -------------------------
# Exact Binomial Probability
# -------------------------

P_exact = []

for k in x:
    prob = comb(n, k) * (p ** k) * (q ** (n - k))
    P_exact.append(prob)

# -------------------------
# Part 2: Normal Approximation
# -------------------------

P_normal = []

for k in x:
    prob = (1 / sqrt(2 * pi * n * p * q)) * \
           exp(-((k - n * p) ** 2) / (2 * n * p * q))
    P_normal.append(prob)

# -------------------------
# Plot
# -------------------------

plt.plot(x, P_sim, 'o', label='Simulation')
plt.plot(x, P_exact, label='Exact Binomial')
plt.plot(x, P_normal, label='Normal Approximation')

plt.xlabel('x')
plt.ylabel('P(x)')
plt.title('Binomial Distribution: n = 100, p = 0.4')

plt.legend()
plt.grid()

plt.savefig('HW2_4.png')
plt.show()
