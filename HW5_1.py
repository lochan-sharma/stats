import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, t

# Questions 1-4: Linear regression homework
np.random.seed(42)

def experiment(x):
    beta0 = 1
    beta1 = 1
    sigma = 0.2
    eps = np.random.normal(0, sigma, len(x))
    y = beta0 + beta1*x + eps
    return y

# The original class function uses only two endpoints.
def compute(x, y):
    n = len(x)
    beta1 = (y[n-1] - y[0]) / (x[n-1] - x[0])
    beta0 = y[n-1] - beta1*x[n-1]
    return beta0, beta1

# Q2: Calculate ordinary least-squares coefficients using all points.
def compute_ols(x, y):
    beta1 = np.sum((x - np.mean(x))*(y - np.mean(y))) / np.sum((x - np.mean(x))**2)
    beta0 = np.mean(y) - beta1*np.mean(x)
    return beta0, beta1

n = 20
x = np.arange(n) / n
y = experiment(x)
print('Q1 x:', x)
print('Q1 y:', y)

b0, b1 = compute_ols(x, y)
print('\nQ2: calculated by hand equations')
print('b0 =', b0, 'b1 =', b1)

# Q3: SciPy library estimates
res = linregress(x, y)
print('\nQ3: SciPy linregress')
print('b0 =', res.intercept, 'b1 =', res.slope)

# Q4: 95% CI for regression slope (unknown residual variance).
y_fit = b0 + b1*x
residuals = y - y_fit
s = np.sqrt(np.sum(residuals**2) / (n-2))
Sxx = np.sum((x - np.mean(x))**2)
se_b1 = s / np.sqrt(Sxx)
t_critical = t.ppf(0.975, n-2)
ci_low = b1 - t_critical*se_b1
ci_high = b1 + t_critical*se_b1
print('\nQ4: 95% confidence interval for b1:', (ci_low, ci_high))

plt.figure(figsize=(9, 6))
plt.scatter(x, y, label='Simulated data')
plt.plot(x, y_fit, label='OLS fit')
plt.plot(x, 1+x, '--', label='True line: y = 1 + x')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Linear Regression: n=20, sigma=0.2')
plt.grid(alpha=0.2)
plt.legend(loc='upper left')
info = (f'OLS: b0={b0:.4f}, b1={b1:.4f}\n'
        f'SciPy: b0={res.intercept:.4f}, b1={res.slope:.4f}\n'
        f'95% CI for slope: [{ci_low:.4f}, {ci_high:.4f}]')
plt.text(0.02, 0.02, info, transform=plt.gca().transAxes,
         bbox=dict(facecolor='white', alpha=0.9))
plt.tight_layout()
plt.savefig('HW5_1.png', dpi=200)
plt.show()
