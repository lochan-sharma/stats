from scipy import stats

# Given values from Devore Example 7.15
n = 17
s2 = 137324.3
alpha = 0.05

# Degrees of freedom
df = n - 1

# Chi-square critical values
chi_low = stats.chi2.ppf(alpha / 2, df)
chi_high = stats.chi2.ppf(1 - alpha / 2, df)

# Confidence interval for variance
lower = (df * s2) / chi_high
upper = (df * s2) / chi_low

print("95% confidence interval for variance:")
print(lower, upper)
