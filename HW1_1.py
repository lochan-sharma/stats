import numpy as np
import matplotlib.pyplot as plt

# Possible outcomes
a = [0, 1]

# Number of trials from 1 to 1000
n = np.arange(1, 1001)

# Perform 1000 random experiments
results = np.random.choice(a, size=1000)

# Calculate the relative frequency of 1
Rf = np.cumsum(results) / n

# Question 2 answer: For n = 3, there are 2^3 = 8 possible outcomes.

# Plot relative frequency versus the number of trials
plt.plot(n, Rf)
plt.xlabel("n")
plt.ylabel("Relative Frequency")
plt.title("Relative Frequency vs Number of Trials")

# Save and display the graph
plt.savefig("HW1_1.png")
plt.show()
