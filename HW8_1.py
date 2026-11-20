"""HW 8, Problem 8.1: Periodogram sampling distribution and inference.

Requires: numpy, scipy, matplotlib
Run: python HW8_1_FINAL.py
Output: HW8_1.png
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2, ncx2
from scipy.optimize import brentq

# Part 3: All 40 observations, in the order given in the assignment.
y = np.array([
    0.9286277042696437, 1.7045034622025108, 1.2050233168496631,
    1.3845192085275169, 0.7431622214379727, -0.5679286290463883,
    -0.48302490734666614, -1.5114589444139053, -1.764577341185066,
    -1.418292052669948, 0.5691222893590951, 1.5289585406721782,
    -0.460701510623547, 1.2776882948506474, -2.6770015657394532,
    -0.08993270340891461, -1.3686260170604216, 0.41212214197362895,
    -1.8219485330400222, -0.9514020560144467, -0.2935061113992405,
    -1.248384532410733, 0.3339742830685172, 0.39336906362403434,
    -0.025834598877514714, -0.811666785526905, 0.6705521440034906,
    0.2112093102712752, 0.6226097153544842, 0.1183604974191117,
    -0.05356324386643412, -0.6882896771055533, -0.4897912650005604,
    -0.09310013954981483, 0.28948660168776613, 2.162314587980623,
    1.9419564408387695, 1.046727620184002, -1.03476056281878,
    -0.12472014892027071
], dtype=float)

n = len(y)
k = 5
assert n == 40, "There should be exactly 40 observations."
t = np.arange(n)

# Calculate the observed periodogram at frequency f5 = 5/40.
a5 = (2 / n) * np.sum(y * np.cos(2 * np.pi * k * t / n))
b5 = (2 / n) * np.sum(y * np.sin(2 * np.pi * k * t / n))
I5 = (n / 2) * (a5**2 + b5**2)

# Independent numerical check using the FFT.
assert np.allclose(I5, (2 / n) * np.abs(np.fft.fft(y)[k])**2)

# Part 1: Simulate the sampling distribution under H0 (no sinusoid).
rng = np.random.default_rng(20261110)
repetitions = 100_000
noise = rng.normal(0, 1, size=(repetitions, n))
I5_samples = (2 / n) * np.abs(np.fft.fft(noise, axis=1)[:, k])**2

# Part 2 and Part 3: Exact chi-square test under H0.
alpha = 0.05
p_value = chi2.sf(I5, df=2)
critical = chi2.ppf(1 - alpha, df=2)
reject = p_value < alpha

# Part 4 (PHYS 590): 95% confidence interval under the specified
# sinusoid + independent N(0,1) noise model.
# I(f5) has a noncentral chi-square distribution with df=2,
# noncentrality lambda = n * alpha5**2 / 2, and E[I(f5)] = 2 + lambda.
# Invert its CDF to obtain confidence limits for lambda >= 0.
def invert_ncx2_cdf(observed, target):
    if ncx2.cdf(observed, 2, 0.0) <= target:
        return 0.0
    upper = max(10.0, observed + 10 * np.sqrt(max(observed, 1)) + 30)
    while ncx2.cdf(observed, 2, upper) > target:
        upper *= 2
    return brentq(
        lambda lam: ncx2.cdf(observed, 2, lam) - target,
        0.0, upper, xtol=1e-11
    )

lambda_lo = invert_ncx2_cdf(I5, 0.975)
lambda_hi = invert_ncx2_cdf(I5, 0.025)
mean_power_lo, mean_power_hi = 2 + lambda_lo, 2 + lambda_hi
amp_abs_lo = np.sqrt(2 * lambda_lo / n)
amp_abs_hi = np.sqrt(2 * lambda_hi / n)

# Create a figure showing the simulated and theoretical null distributions.
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "savefig.dpi": 250
})
fig, ax = plt.subplots(figsize=(11.5, 7))
xmax = max(17, I5 * 1.25)
x = np.linspace(0, xmax, 900)

ax.hist(
    I5_samples, bins=np.linspace(0, xmax, 72), density=True,
    alpha=0.34, color="#5C88C7", edgecolor="white",
    label=f"Simulation: {repetitions:,} noise-only samples"
)
ax.plot(x, chi2.pdf(x, df=2), color="#173B66", linewidth=2.7,
        label=r"Exact null PDF: $\chi^2_2$")
ax.fill_between(
    x, 0, chi2.pdf(x, df=2), where=x >= I5,
    color="#E58B56", alpha=0.4,
    label=f"Right-tail p-value = {p_value:.4f}"
)
ax.axvline(
    critical, color="#8E6FA8", linewidth=2, linestyle="--",
    label=f"5% significance cutoff = {critical:.3f}"
)
ax.axvline(
    I5, color="#B84235", linewidth=2.3,
    label=fr"Observed $I(f_5)$ = {I5:.3f}"
)

ax.set_xlim(0, xmax)
ax.set_ylim(bottom=0)
ax.set_xlabel(r"Periodogram $I(f_5)$ at $f_5 = 5/40 = 0.125$")
ax.set_ylabel("Probability density")
ax.grid(axis="y", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.legend(loc="upper right", fontsize=9, framealpha=0.96)

conclusion = (
    "Reject H0: evidence of a periodic component at f5"
    if reject else
    "Fail to reject H0: insufficient evidence at f5"
)
fig.suptitle(conclusion, fontsize=14, fontweight="bold", y=0.97)
ax.set_title(
    r"$H_0: \alpha_5 = 0$ versus $H_1: \alpha_5 \neq 0$"
    + f"   |   n = {n}   |   p = {p_value:.4f}",
    pad=14
)

ci_text = (
    r"95% CI for underlying $E[I(f_5)]$: "
    + f"[{mean_power_lo:.2f}, {mean_power_hi:.2f}]"
    + "\n" + r"95% CI for signal magnitude $|\alpha_5|$: "
    + f"[{amp_abs_lo:.3f}, {amp_abs_hi:.3f}]"
    + "\n" + r"From noncentral $\chi^2_2(\lambda)$, "
    + r"$\lambda = n\alpha_5^2/2$"
)
ax.text(
    0.985, 0.49, ci_text, transform=ax.transAxes,
    ha="right", va="top", fontsize=9.5,
    bbox=dict(boxstyle="round,pad=0.6", facecolor="#F5F7FA",
              edgecolor="#BCC5D1", alpha=0.98)
)

fig.subplots_adjust(top=0.83, bottom=0.13, left=0.09, right=0.97)
fig.savefig("HW8_1.png", bbox_inches="tight", facecolor="white")
plt.close(fig)

print("--- HW 8, Problem 8.1 ---")
print(f"n = {n}, k = {k}, f5 = {k / n:.5f}")
print(f"a5 = {a5:.8f}, b5 = {b5:.8f}")
print(f"I(f5) = {I5:.8f}")
print(f"Simulated null mean = {I5_samples.mean():.5f}; theory = 2")
print(f"Simulated null variance = {I5_samples.var():.5f}; theory = 4")
print(f"5% critical chi-square value = {critical:.8f}")
print(f"Right-tail p-value = {p_value:.10f}")
print("Decision:", conclusion)
print(f"95% CI for lambda = [{lambda_lo:.5f}, {lambda_hi:.5f}]")
print(f"95% CI for expected I(f5) = [{mean_power_lo:.5f}, {mean_power_hi:.5f}]")
print(f"95% CI for |alpha5| = [{amp_abs_lo:.5f}, {amp_abs_hi:.5f}]")
print("Saved HW8_1.png")
