import numpy as np
import matplotlib.pyplot as plt

# equation your equation: f(x) = (3x + 2) / (2x + 1)
def f(x):
    return (3*x + 2) / (2*x + 1)

# Asymptote at x = -1/2
x_vals = np.linspace(-2, 2, 50)
x_vals = x_vals[x_vals != -0.5]  # Exclude x = -1/2 to avoid division by zero

# function is
y_vals = f(x_vals)

# plt.spells
plt.figure(figsize=(8, 6))
plt.plot(x_vals, y_vals, label="f(x) = (3x + 2) / (2x + 1)")

# asymptotes
plt.axvline(-0.5, color='r', linestyle='--', label="Vertical Asymptote: x = -0.5")
plt.axhline(3/2, color='g', linestyle='--', label="Horizontal Asymptote: y = 1.5")

# highlight the intercepts
plt.scatter([0], [2], color='blue', zorder=5)
plt.text(0, 2, "(0, 2)", fontsize=12, verticalalignment='bottom')

# title&labels
plt.title("Graph of f(x) = (3x + 2) / (2x + 1)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()
