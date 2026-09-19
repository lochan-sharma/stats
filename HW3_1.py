import numpy as np
import matplotlib.pyplot as plt
import math

# -----------------------------
# Given information
# -----------------------------

days = 1000
hours_per_day = 24
total_hours = days * hours_per_day

# Probability of a flare in one hour
p = 900 / total_hours

print("Probability of flare in one hour =", p)

# Use a fixed seed so the same random result is produced each time
np.random.seed(1)

# -----------------------------
# Part 1: Simulate flare data
# -----------------------------

# 1 = flare
# 0 = no flare
hourly_data = np.random.binomial(1, p, total_hours)

# Convert hourly data into daily data
daily_data = hourly_data.reshape(days, hours_per_day)

# Count number of flares each day
daily_flares = np.sum(daily_data, axis=1)

# Possible values of x
x_values = np.arange(0, np.max(daily_flares) + 1)

# -----------------------------
# Simulated probability Ps(x)
# -----------------------------

Ps = []

for x in x_values:
    probability = np.sum(daily_flares == x) / days
    Ps.append(probability)

Ps = np.array(Ps)

# -----------------------------
# Poisson probability Pp(x)
# -----------------------------

# Average number of flares per day
mean_daily = p * hours_per_day

Pp = []

for x in x_values:
    probability = (mean_daily ** x) * np.exp(-mean_daily) / math.factorial(x)
    Pp.append(probability)

Pp = np.array(Pp)

# -----------------------------
# Binomial probability Pb(x)
# -----------------------------

Pb = []

for x in x_values:
    probability = (
        math.comb(hours_per_day, x)
        * (p ** x)
        * ((1 - p) ** (hours_per_day - x))
    )
    Pb.append(probability)

Pb = np.array(Pb)

# -----------------------------
# Plot Part 1
# -----------------------------

plt.figure()

plt.plot(x_values, Ps, "o-", label="Simulation")
plt.plot(x_values, Pp, "s-", label="Poisson")
plt.plot(x_values, Pb, "^-", label="Binomial")

plt.xlabel("Number of flares per day")
plt.ylabel("Probability")
plt.title("X-ray Flares Per Day")
plt.legend()
plt.grid()

# Save first figure
plt.savefig("HW3_1.png", dpi=300, bbox_inches="tight")

plt.show()

# -----------------------------
# Part 2: Time between flares
# -----------------------------

# Find the hours where a flare happened
flare_times = np.where(hourly_data == 1)[0]

# Find time between consecutive flares
time_between = np.diff(flare_times)

# Plot histogram
plt.figure()

plt.hist(time_between, bins=20, edgecolor="black")

plt.xlabel("Time Between Flares (hours)")
plt.ylabel("Number of Occurrences")
plt.title("Time Between X-ray Flares")
plt.grid()

# Save second figure
plt.savefig("HW3_2.png", dpi=300, bbox_inches="tight")

plt.show()
