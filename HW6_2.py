import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats

# Data from Devore, Example 12.18 (as provided in the homework)
x = np.array([55.10, 44.83, 46.32, 51.10, 49.89, 45.20, 48.18,
              46.70, 54.31, 41.50, 47.50, 52.00, 52.25, 50.86,
              51.66, 54.77, 57.06, 57.84, 55.22])
y = np.array([49.10, 31.20, 32.80, 42.60, 42.50, 32.70, 36.21,
              40.40, 37.42, 30.80, 35.34, 44.80, 41.75, 39.35,
              44.07, 43.40, 45.30, 39.08, 41.89])

n = len(x)
assert n == len(y), 'x and y must contain the same number of observations'
x_bar = np.mean(x)
y_bar = np.mean(y)
Sxx = np.sum((x - x_bar)**2)
Syy = np.sum((y - y_bar)**2)
Sxy = np.sum((x - x_bar)*(y - y_bar))
r = Sxy / np.sqrt(Sxx*Syy)

# Student t test for H0: population correlation rho = 0, two-sided.
nu = n - 2  # Greek nu (v): degrees of freedom
t_stat = r * np.sqrt(nu / (1 - r**2))
P = 2 * stats.t.sf(abs(t_stat), df=nu)

# Fisher's z transform and its standardized normal-test statistic.
# These are printed as additional information: they are NOT the t statistic.
z_fisher = np.arctanh(r)
z_score = z_fisher * np.sqrt(n - 3)

slope = Sxy / Sxx
intercept = y_bar - slope * x_bar

print('Homework 6.2: Regression Part II')
print(f'n                 = {n}')
print(f'Sxx               = {Sxx:.6f}')
print(f'Syy               = {Syy:.6f}')
print(f'Sxy               = {Sxy:.6f}')
print(f'r                 = {r:.6f}')
print(f'v (df = n-2)      = {nu}')
print(f't test statistic  = {t_stat:.6f}')
print(f'P (two-sided)     = {P:.8g}')
print(f'Fisher z          = {z_fisher:.6f}')
print(f'Fisher z-score    = {z_score:.6f}')
print(f'regression line   = {intercept:.4f} + {slope:.4f} x')

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(x, y, color='royalblue', s=65, edgecolors='black', linewidths=0.5, label='Observed data')
x_line = np.linspace(x.min(), x.max(), 200)
ax.plot(x_line, intercept + slope*x_line, color='darkorange', linewidth=2, label='Least-squares line')
ax.text(0.04, 0.96, f'r = {r:.4f}\nP = {P:.3g}', transform=ax.transAxes,
        ha='left', va='top', fontsize=12,
        bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', boxstyle='round,pad=0.4'))
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Devore Example 12.18: Scatter Plot of y vs. x')
ax.grid(alpha=0.25)
ax.legend(loc='lower right')
fig.tight_layout()
fig.savefig('HW6_2.png', dpi=300)
plt.close(fig)
print('Saved HW6_2.png')
