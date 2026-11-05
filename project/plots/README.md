## Statistical Analysis: Mean Z-Test (Devore Section 9.1)

I used MATLAB to compare the mean rise and decay times of 2,868 solar flares observed in 2023. The analysis followed the two-sample mean Z-test formula from Devore's Chapter 9, Section 9.1, using sample standard deviations in a large-sample approximation.

### Hypotheses

**Null Hypothesis (H₀):** The population mean rise time is equal to the population mean decay time.

H₀: μrise − μdecay = 0

**Alternative Hypothesis (H₁):** The population mean rise time is greater than the population mean decay time.

H₁: μrise − μdecay > 0

### Results

- Sample size: 2,868 solar flares
- Mean rise time: 11.19 minutes
- Mean decay time: 10.24 minutes
- Mean difference: 0.95 minutes
- Standard error: 0.780 minutes
- Z-statistic: 1.222
- One-tailed p-value: 0.1109
- Significance level: 0.05

### Conclusion

The mean rise time was slightly longer than the mean decay time. However, since the p-value (0.1109) was greater than 0.05, we failed to reject the null hypothesis. The difference was not statistically significant at the 5% level.
