# HW 9.2: Credible Interval on a Proportion
#
# Given:
# Total coin tosses = 10
# Number of heads = 4
# Number of tails = 6
#
# Observed proportion of heads = 4/10 = 0.4
#
# theta = unknown true probability of getting heads
# Prior probability: p(theta) = 1 for 0 <= theta <= 1

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from math import comb

# --------------------------------------------
# QUESTION 1: Find likelihood P(D|theta)
# --------------------------------------------
# Binomial formula:
# P(D|theta) = C(n,k) * theta^k * (1-theta)^(n-k)
# n = 10, k = 4, C(10,4) = 210
# Answer: P(D|theta) = 210 * theta^4 * (1-theta)^6

n = 10
k = 4
C = comb(n, k)

def likelihood(theta):
    return C * theta**k * (1-theta)**(n-k)

print('QUESTION 1')
print('Likelihood = 210 * theta^4 * (1-theta)^6')
print()

# --------------------------------------------
# QUESTION 2: Find P(D)
# --------------------------------------------
# P(D) = integral from 0 to 1 of P(D|theta) * p(theta) dtheta
# Since p(theta) = 1:
# P(D) = integral from 0 to 1 of 210 * theta^4 * (1-theta)^6 dtheta
# Answer: P(D) = 1/11 = 0.090909...

P_D, error = quad(likelihood, 0, 1)

print('QUESTION 2')
print('P(D) =', P_D)
print()

# --------------------------------------------
# QUESTION 3: Plot posterior p(theta|D)
# --------------------------------------------
# Bayes theorem: p(theta|D) = P(D|theta) * p(theta) / P(D)
# Since p(theta) = 1:
# p(theta|D) = P(D|theta) / P(D)
# Answer: p(theta|D) = 2310 * theta^4 * (1-theta)^6
# The posterior density peaks at theta = 0.4.

def posterior(theta):
    return likelihood(theta) / P_D

theta = np.linspace(0, 1, 500)
y = posterior(theta)

plt.figure(figsize=(8, 5))
plt.plot(theta, y, color='blue', linewidth=2)
plt.axvline(0.4, color='red', linestyle='--', label='theta = 0.4')
plt.xlabel('Theta', fontsize=12)
plt.ylabel('Posterior Density', fontsize=12)
plt.title('Posterior Probability Density', fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('HW9_2.png', dpi=300)
plt.show()

print('QUESTION 3')
print('Posterior = 2310 * theta^4 * (1-theta)^6')
print('Graph saved as HW9_2.png')
print()

# --------------------------------------------
# QUESTION 4: Calculate integral from 0 to a
# --------------------------------------------
# Integral from 0 to a of p(theta|D) dtheta
# = Integral from 0 to a of 2310 * theta^4 * (1-theta)^6 dtheta
# Given: a = 0.02, 0.04, 0.06, 0.08, 0.10
# The integral is the area under the posterior curve from 0 to a.

a_values = [0.02, 0.04, 0.06, 0.08, 0.10]

print('QUESTION 4')
print('Area under posterior from 0 to a')
print()

for a in a_values:
    area, error = quad(posterior, 0, a)
    print('a =', a, '  Area =', round(area, 10))
