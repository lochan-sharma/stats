import numpy as np

def dft(y, method='slow'):

  n = len(y)
  if n % 2 == 0:
    q = n // 2
  else:
    q = (n - 1) // 2

  i = np.arange(1, q+1)
  f = i / n
  a0 = np.mean(y)

  if method == 'slow':
    a = np.full(q, np.nan)
    b = np.full(q, np.nan)
    for k in range(q):
      a[k] = 0
      b[k] = 0
      for t in range(n):
        a[k] = a[k] + y[t] * np.cos(2 * np.pi * (k+1) * t / n)
        b[k] = b[k] + y[t] * np.sin(2 * np.pi * (k+1) * t / n)

      a[k] = 2 * a[k] / n
      b[k] = 2 * b[k] / n

  if method == 'fast':
    yfft = np.fft.fft(y)[1:q+1]
    a = (2 / n) * np.real(yfft)
    b = -(2 / n) * np.imag(yfft)

  if n % 2 == 0:
    a[-1] = a[-1] / 2

  return a0, a, b, i, f


def dft_plot(i, a, b, y):
  import matplotlib.pyplot as plt
  figure, axes = plt.subplots(3, 1, figsize=(8.5, 11), layout='constrained')
  axes[0].plot(np.arange(len(y)), y, marker='o', ls='none', color='k')
  axes[0].set(xlabel='Sample index ($t$)', ylabel='$y_t$')
  axes[0].grid(True)

  axes[1].plot(i, a, label='$a_i$', marker='o', ls='none', ms=8)
  axes[1].plot(i, b, label='$b_i$', marker='o', ls='none', ms=6)
  axes[1].set(xlabel='DFT index ($i$)')
  axes[1].legend()
  axes[1].grid(True)

  power = np.asarray(a)**2 + np.asarray(b)**2
  axes[2].plot(i, power, marker='o', ls='none', color='k')
  axes[2].set(xlabel='DFT index ($i$)', ylabel='$a_i^2 + b_i^2$')
  axes[2].grid(True)
  axes[2].sharex(axes[1])
  axes[2].grid(True)

  # Modify all x labels so fractions are never shown (x values are always integer)
  from matplotlib.ticker import MaxNLocator
  axes[0].xaxis.set_major_locator(MaxNLocator(integer=True))
  axes[1].xaxis.set_major_locator(MaxNLocator(integer=True))
  axes[2].xaxis.set_major_locator(MaxNLocator(integer=True))

  #plt.show()


def dft_print(a0, a, b, i, f):
  print(f'  {"i":>4} {"a_i":>12} {"b_i":>12} {"f_i":>12}')
  print(f'  {0:4d} {a0:12.4f} {" ":12s} {0:12.4f}')
  for idx in range(len(a)):
    print(f'  {i[idx]:4d} {a[idx]:12.4f} {b[idx]:12.4f} {f[idx]:12.4f}')


def dft_test(y):
  # Verify that the slow and fast methods of computing the DFT give the same results
  a0_s, a_s, b_s, i_s, f_s = dft(y, method='slow')
  a0_f, a_f, b_f, i_f, f_f = dft(y, method='fast')
  assert np.all(a0_s == a0_f)
  assert np.allclose(a_s, a_f, rtol=1e-10, atol=1e-12)
  assert np.allclose(b_s, b_f, rtol=1e-10, atol=1e-12)
  assert np.all(i_s == i_f)
  assert np.all(f_s == f_f)
  print("All tests passed.")


def savefig(fname):
  import matplotlib.pyplot as plt
  plt.savefig(fname, dpi=300)
  print(f"Wrote {fname}")


def fisher_g(y):
  # For later HW
  _, a, b, i, f = dft(y, method='fast')
  power = (a**2 + b**2)[f < 0.5]
  total_power = np.sum(power)
  return np.max(power) / total_power


def fisher_g_test(y):
  # For later HW
  """Return Fisher's upper-tail p-value for equally spaced Gaussian white noise."""
  from math import comb, floor

  g = fisher_g(y)
  m = (len(y) - 1) // 2
  if g <= 1 / m:
    return 1.0

  p = 0.0
  for index in range(1, floor(1 / g) + 1):
    term = (-1)**(index - 1) * comb(m, index) * (1 - index * g)**(m - 1)
    p += term
  return float(np.clip(p, 0, 1))


def part1():
  y = [0, 1, 0, -1]
  a0, a, b, i, f = dft(y, method='slow')

  print("--Part 1--")
  print(f"  y = {y}")
  print("DFT")
  dft_print(a0, a, b, i, f)

  dft_plot(i, a, b, y)
  savefig('HW6_1_1.png')

def part2():
  y = [0, -1, 0, 1]
  a0, a, b, i, f = dft(y, method='slow')

  print("--Part 2--")
  print(f"  y = {y}")
  print("DFT")
  dft_print(a0, a, b, i, f)

  dft_plot(i, a, b, y)
  savefig('HW6_1_2.png')

def part3():
  n = 40 # When n = 4, gives same result as part 1
  y = np.full(n, np.nan)
  i = 1 # The frequency index for the sine wave. i = 1 means the sine wave
        # will have a frequency of i/n cycles per sample and a period of n/i samples.
  for t in range(n):
    y[t] = np.sin(2 * np.pi * (i/n) * t )

  a0, a, b, i, f = dft(y, method='slow')

  print("--Part 3--")
  dft_plot(i, a, b, y)

  dft_print(a0, a, b, i, f)
  savefig('HW6_1_3.png')

def part4():
  """
  Modify the values in y so that the DFT has the following values:
  DFT
     i          a_i          b_i          f_i
     0       0.0000                    0.0000
     1       1.0000      -0.0000       0.2500
     2       0.0000       0.0000       0.5000
  """

  y = [0, 1, 0, -1]
  a0, a, b, i, f = dft(y, method='slow')

  print("--Part 4-")
  print(f"  y = {y}")
  print("DFT")
  dft_print(a0, a, b, i, f)

  dft_plot(i, a, b, y)
  savefig('HW6_1_4.png')

def part5():
  """
  Keep n the same, but modify the equation for y[t] so that 
  a_3 = b_3 = 1; otherwise, all a_i and b_i are 0.
  """

  n = 40
  y = np.full(n, np.nan)
  i = 1
  for t in range(n):
    y[t] = np.sin(2 * np.pi * (i/n) * t )

  a0, a, b, i, f = dft(y, method='slow')

  print("--Part 5--")
  dft_plot(i, a, b, y)

  dft_print(a0, a, b, i, f)
  savefig('HW6_1_5.png')

def part6():
  """
  Keep n the same, but modify the equation for y[t] so that 
  a_3 = b_3 = 1 and a_6 = 1; otherwise, all a_i and b_i are 0.
  """

  n = 40
  y = np.full(n, np.nan)
  i = 1 # The frequency index for the sine wave. i = 1 means the sine wave
        # will have a frequency of i/n cycles per sample and a period of n/i samples.
  for t in range(n):
    y[t] = np.sin(2 * np.pi * (i/n) * t )

  a0, a, b, i, f = dft(y, method='slow')

  print("--Part 6--")
  dft_plot(i, a, b, y)

  dft_print(a0, a, b, i, f)
  savefig('HW6_1_6.png')


def part7():
  """
  Here we want to determine from the plot of a^2 + b^2 when you can "see"
  evidence of the sine wave at DFT index i (frequency i/40). For small sigma,
  you should see a clear spike in the bottom plot (for the magnitude squared
  of the DFT coefficients).

  Increase sigma until it is your opinion that, visually, you can not see the
  spike in the bottom plot.

  Later we will compare your visual assessment with a more quantitative measure.
  """

  n = 40
  y = np.full(n, np.nan)
  i = 5 # The frequency index for the sine wave. i = 1 means the sine wave
         # will have a frequency of i/n cycles per sample and a period of n/i samples.
  sigma = 0.01 # Standard deviation of the noise
  for t in range(n):
    epsilon = np.random.normal(loc=0, scale=sigma)
    y[t] = epsilon + np.sin(2 * np.pi * (i/n) * t )

  a0, a, b, i, f = dft(y, method='slow')

  print("--Part 7--")
  dft_plot(i, a, b, y)

  dft_print(a0, a, b, i, f)
  savefig('HW6_1_7.png')

part1()
part2()
part3()
part4()
part5()
part6()
part7()

