
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read dataset
data = pd.read_csv(r"medical.csv")

# Privacy parameters
epsilon = 1.0
sensitivity = 1

# Exponential mechanism function
def exponential_mechanism(categories, utilities, epsilon, sensitivity):
    scores = np.exp((epsilon * utilities) / (2 * sensitivity))
    probabilities = scores / np.sum(scores)
    selected = np.random.choice(categories, p=probabilities)
    return selected, probabilities

# Candidate outputs (possible categories)
conditions = data["Medical Condition"].unique()

# Utility of each category = frequency count in the dataset
utilities = data["Medical Condition"].value_counts().reindex(conditions).values

# Run exponential mechanism
selected_condition, probabilities = exponential_mechanism(
    conditions, utilities, epsilon, sensitivity
)

# Print results
print("\nDifferential Privacy using Exponential Mechanism\n")
print("Categories:", conditions)
print("Utility Scores:", utilities)
print("Selection Probabilities:", probabilities)
print("Selected Output:", selected_condition)

# Plot probabilities
plt.bar(conditions, probabilities)
plt.xlabel("Medical Condition")
plt.ylabel("Selection Probability")
plt.title("Probability Distribution of Exponential Mechanism")
plt.show()
