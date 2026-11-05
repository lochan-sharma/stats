## Statistical Analysis: Mean Z-Test

I used MATLAB to perform a mean Z-test approximation to compare the rise and decay times of 2,868 solar flares observed in 2023. Since both measurements came from the same flare, I calculated the paired differences.

### Hypotheses

**Null Hypothesis (H₀):** The population mean rise time is equal to the population mean decay time.

H₀: μrise − μdecay = 0

**Alternative Hypothesis (H₁):** The population mean rise time is greater than the population mean decay time.

H₁: μrise − μdecay > 0

### Results

- Sample size: 2,868
- Mean rise time: 11.19 minutes
- Mean decay time: 10.24 minutes
- Mean paired difference: 0.95 minutes
- Standard deviation: 40.63 minutes
- Z-statistic: 1.257
- P-value: 0.1045
- Significance level: 0.05

A few extreme observations strongly affected the standard deviation. For example, one flare had a rise time of 2,065 minutes. Excluding this observation reduced the standard deviation from 40.63 to 12.93 minutes. All observations were retained in the main analysis.

### 

The mean rise time was slightly longer than the mean decay time. However, since the p-value (0.1045) was greater than 0.05, **we failed to reject the null hypothesis**. There was insufficient statistical evidence that the population mean rise time was greater than the population mean decay time.
