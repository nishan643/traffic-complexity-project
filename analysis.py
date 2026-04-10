import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs("results", exist_ok=True)

data = pd.read_csv("data/avalanche_data.csv")
freq = data['size'].value_counts().sort_index()
prob = freq / freq.sum()

# Log-log plot
plt.figure()
plt.loglog(prob.index, prob.values, marker='o')
plt.xlabel("Avalanche Size")
plt.ylabel("Probability")
plt.title("Log-Log Distribution")
plt.grid(True)
plt.savefig("results/loglog_plot.png")

# Power-law fit
log_x = np.log(prob.index)
log_y = np.log(prob.values)

coeffs = np.polyfit(log_x, log_y, 1)
fit_y = np.exp(coeffs[1]) * prob.index**coeffs[0]

plt.figure()
plt.loglog(prob.index, prob.values, 'o', label="Data")
plt.loglog(prob.index, fit_y, label=f"Fit slope={coeffs[0]:.2f}")
plt.legend()
plt.title("Power Law Fit")
plt.savefig("results/powerlaw_fit.png")

# Histogram
plt.figure()
plt.hist(data['size'], bins=30)
plt.title("Avalanche Size Distribution")
plt.xlabel("Size")
plt.ylabel("Count")
plt.savefig("results/histogram.png")

print("Graphs generated. Exponent:", coeffs[0])
