import numpy as np
import pandas as pd

# -------------------------------
# Step 1: Setup parameters
# -------------------------------
np.random.seed(42)

n = 1000
true_smoker_proportion = 0.30
p_values = [0.6, 0.7, 0.8, 0.9]

# -------------------------------
# Step 2: Generate true dataset
# -------------------------------
true_data = np.random.choice(
    [1, 0],
    size=n,
    p=[true_smoker_proportion, 1 - true_smoker_proportion]
)

true_df = pd.DataFrame({"Smoker": true_data})
true_df.to_csv("true_dataset.csv", index=False)

print("True dataset saved as: true_dataset.csv")
print("True proportion of smokers:", round(np.mean(true_data), 3))


# -------------------------------
# Step 3: Randomized Response
# -------------------------------
def randomized_response(data, p):

    noisy = []

    for x in data:

        # With probability p -> truthful answer
        if np.random.rand() < p:
            noisy.append(x)

        # Otherwise random answer
        else:
            noisy.append(np.random.choice([0,1]))

    return np.array(noisy)


# -------------------------------
# Step 4: Estimate true proportion
# -------------------------------
def estimate_true_proportion(noisy_data, p):

    observed_mean = np.mean(noisy_data)

    estimated = (observed_mean - (1 - p) / 2) / p

    return estimated


# -------------------------------
# Step 5: Run experiment
# -------------------------------
results = []

for p in p_values:

    noisy_data = randomized_response(true_data, p)

    filename = f"noisy_dataset_p{int(p*10)}.csv"

    pd.DataFrame({"Noisy_Response": noisy_data}).to_csv(filename, index=False)

    observed = np.mean(noisy_data)

    estimated = estimate_true_proportion(noisy_data, p)

    results.append([p, observed, estimated])

    print(f"Noisy dataset saved as: {filename}")


# -------------------------------
# Step 6: Display results
# -------------------------------
print("\nFinal Results")
print("--------------------------------------")
print("p-value | Observed Mean | Estimated Proportion")
print("--------------------------------------")

for r in results:
    print(f"{r[0]:.1f}     | {r[1]:.3f}        | {r[2]:.3f}")
true_df
