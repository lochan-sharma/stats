import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# Q5 (PHYS 590 only): Test whether the 95% CI captures the true
# slope beta1=1 in approximately 95% of repeated experiments.
np.random.seed(123)

def experiment(x):
    beta0 = 1
    beta1 = 1
    sigma = 0.2
    eps = np.random.normal(0, sigma, len(x))
    return beta0 + beta1*x + eps

def compute_ols(x, y):
    beta1 = np.sum((x-np.mean(x))*(y-np.mean(y))) / np.sum((x-np.mean(x))**2)
    beta0 = np.mean(y) - beta1*np.mean(x)
    return beta0, beta1

n = 20
x = np.arange(n)/n
ne = 10000
true_slope = 1
contained = np.zeros(ne, dtype=bool)
Sxx = np.sum((x-np.mean(x))**2)
t_critical = t.ppf(0.975, n-2)

for i in range(ne):
    y = experiment(x)
    b0, b1 = compute_ols(x, y)
    residuals = y - (b0+b1*x)
    s = np.sqrt(np.sum(residuals**2)/(n-2))
    se_b1 = s/np.sqrt(Sxx)
    lower = b1 - t_critical*se_b1
    upper = b1 + t_critical*se_b1
    contained[i] = lower <= true_slope <= upper

coverage = np.mean(contained)
print('Number of experiments =', ne)
print('Intervals containing true slope =', np.sum(contained))
print('Coverage percentage =', coverage*100)

plt.figure(figsize=(8, 5))
plt.bar(['Contains true slope', 'Misses true slope'],
        [coverage*100, (1-coverage)*100])
plt.ylabel('Percentage (%)')
plt.title('95% Confidence Interval Coverage')
plt.ylim(0, 105)
plt.tight_layout()
plt.savefig('HW5_1_test.png', dpi=200)
plt.show()
