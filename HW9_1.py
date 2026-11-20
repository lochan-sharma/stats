# HW9, Problem 1 - 99% confidence intervals for the probability of heads
#
# Given: n = 10 tosses; 4 heads
# p_hat = 4/10 = 0.4; q_hat = 1 - p_hat = 0.6
# alpha = 0.01; z_(alpha/2) = z_0.005 = 2.5758293
#
# (7.10) Score confidence interval (Wilson):
# denominator = 1 + z^2/n
# p_tilde = (p_hat + z^2/(2*n))/denominator
# margin = z*sqrt(p_hat*q_hat/n + z^2/(4*n^2))/denominator
# score CI = (p_tilde - margin, p_tilde + margin)
#
# (7.11) Large-sample confidence interval (Wald):
# margin = z*sqrt(p_hat*q_hat/n)
# CI = (p_hat - margin, p_hat + margin)
# The score interval is preferable for this small sample.

import math

n = 10
heads = 4
p_hat = heads / n
q_hat = 1 - p_hat
z = 2.5758293035489004

# Score interval (Eq. 7.10)
denominator = 1 + z**2 / n
p_tilde = (p_hat + z**2 / (2*n)) / denominator
score_margin = z * math.sqrt(p_hat*q_hat/n + z**2/(4*n**2)) / denominator
score_lower = p_tilde - score_margin
score_upper = p_tilde + score_margin

# Large-sample interval (Eq. 7.11)
large_margin = z * math.sqrt(p_hat*q_hat/n)
large_lower = p_hat - large_margin
large_upper = p_hat + large_margin

print('HW9, Problem 1: 99% Confidence Intervals')
print(f'n = {n}, p_hat = {p_hat:.4f}, q_hat = {q_hat:.4f}')
print(f'Score CI (7.10):        [{score_lower:.4f}, {score_upper:.4f}]')
print(f'Large-sample CI (7.11): [{large_lower:.4f}, {large_upper:.4f}]')
