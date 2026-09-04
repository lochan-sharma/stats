import numpy as np

# Question 1 answer:
# There are 2^3 = 8 possible step configurations.
# Sample space:
# (-1, -1, -1), (-1, -1, 1), (-1, 1, -1), (-1, 1, 1),
# (1, -1, -1), (1, -1, 1), (1, 1, -1), (1, 1, 1)

# Number of times to repeat the three-step experiment
number_of_experiments = 100000

# Generate three random steps for every experiment
steps = np.random.choice([-1, 1], size=(number_of_experiments, 3))

# Calculate the final position after each three-step experiment
final_positions = np.sum(steps, axis=1)

# Estimate the probability that the final position is 1
probability = np.mean(final_positions == 1)

print("Estimated probability:", probability)
