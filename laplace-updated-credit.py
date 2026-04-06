import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("healthcare_dataset.csv")

# Disease we want to query
disease_name = "Diabetes"

# Compute true statistics
true_count = (df["Medical Condition"] == disease_name).sum()
n = len(df)

print("Total records:", n)
print(f"True count of {disease_name}:", true_count)
print("True proportion:", true_count / n)


# Laplace Mechanism Function
def laplace_mechanism(true_value, sensitivity, epsilon):

    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale)

    return true_value + noise


# Different epsilon values
epsilon_values = [0.1, 0.5, 1.0, 2.0]

print("\nDifferentially Private Results:\n")

for eps in epsilon_values:

    noisy_count = laplace_mechanism(
        true_value=true_count,
        sensitivity=1,
        epsilon=eps
    )

    noisy_proportion = noisy_count / n

    print(f"Epsilon = {eps}")
    print("  Noisy Count     :", round(noisy_count, 2))
    print("  Noisy Proportion:", round(noisy_proportion, 4))
    print()


# -----------------------------
# Plot Laplace Distributions
# -----------------------------

x = np.linspace(-10, 10, 500)

plt.figure(figsize=(8,5))

for eps in epsilon_values:

    scale = 1 / eps   # sensitivity = 1

    # Laplace PDF
    y = (1/(2*scale)) * np.exp(-np.abs(x)/scale)

    plt.plot(x, y, label=f"ε = {eps}")

plt.title("Laplace Noise Distribution for Different ε")
plt.xlabel("Noise Value")
plt.ylabel("Probability Density")
plt.legend()
plt.grid()

plt.show()
