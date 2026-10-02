import math
from scipy import stats

# Given values
xbar = 10
s = 1.03
alpha = 0.01
n = 20

# -------------------------------------------------
# Answer 1: t confidence interval
# -------------------------------------------------

tcrit = stats.t.ppf(1 - alpha/2, n - 1)

margin1 = tcrit * s / math.sqrt(n)

lower1 = xbar - margin1
upper1 = xbar + margin1

print("Answer 1:")
print(lower1, upper1)


# -------------------------------------------------
# Answer 2: z confidence interval
# -------------------------------------------------

zcrit = stats.norm.ppf(1 - alpha/2)

margin2 = zcrit * s / math.sqrt(n)

lower2 = xbar - margin2
upper2 = xbar + margin2

print("\nAnswer 2:")
print(lower2, upper2)


# -------------------------------------------------
# Answer 3
# -------------------------------------------------

print("\nAnswer 3:")

for n in range(5, 101, 5):

    # t critical value changes because n changes
    tcrit = stats.t.ppf(1 - alpha/2, n - 1)

    # Length of t confidence interval
    length1 = 2 * tcrit * s / math.sqrt(n)

    # Length of z confidence interval
    length2 = 2 * zcrit * s / math.sqrt(n)

    print("n =", n, " length1 =", length1, " length2 =", length2)
