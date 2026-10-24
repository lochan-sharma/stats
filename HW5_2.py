import numpy as np


def dft(y):
    """Calculate the real Fourier series coefficients of a 1-D signal.

    Returns a0 (scalar), a (cosine coefficients), b (sine coefficients).
    For even N, the final Nyquist cosine coefficient is scaled by 1/N
    and its corresponding sine coefficient equals zero.
    """
    y = np.asarray(y, dtype=float)
    if y.ndim != 1 or len(y) == 0:
        raise ValueError("y must be a nonempty one-dimensional array")

    N = len(y)
    q = N // 2
    t = np.arange(N)
    a0 = float(np.sum(y) / N)
    a = np.zeros(q)
    b = np.zeros(q)

    for i in range(1, q + 1):
        angle = 2 * np.pi * i * t / N
        if N % 2 == 0 and i == q:
            a[i - 1] = np.sum(y * np.cos(angle)) / N
            b[i - 1] = 0.0
        else:
            a[i - 1] = 2 * np.sum(y * np.cos(angle)) / N
            b[i - 1] = 2 * np.sum(y * np.sin(angle)) / N

    # Eliminate tiny roundoff errors when an exact zero is expected.
    a[np.isclose(a, 0, atol=1e-12)] = 0.0
    b[np.isclose(b, 0, atol=1e-12)] = 0.0
    return a0, a, b


if __name__ == "__main__":
    # Test provided in Question 2
    y = np.array([0, -1, 0, 1])
    a0, a, b = dft(y)
    print("a0:", a0)
    print("a:", a)
    print("b:", b)
