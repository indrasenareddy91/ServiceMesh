import pandas as pd
import numpy as np

print("--------------------------------------------------")
print(" DIFFERENTIAL PRIVACY USING EXPONENTIAL MECHANISM ")
print("--------------------------------------------------")

print("\nStep 1 : Loading Netflix Dataset")

df = pd.read_csv("netflix_titles.csv")

print("Dataset loaded successfully")
print("Number of records :", len(df))
print("Number of columns :", len(df.columns))

print("\nFirst 5 rows of dataset")
print(df.head())

print("\n--------------------------------------------------")
print("Step 2 : Identify Non-Numeric Columns")
print("--------------------------------------------------")

categorical_columns = df.select_dtypes(include=['object']).columns.tolist()

print("Categorical Columns Found:")
print(categorical_columns)

print("\n--------------------------------------------------")
print("Step 3 : Privacy Parameter")
print("--------------------------------------------------")

epsilon = 1.0
print("Epsilon =", epsilon)

print("\n--------------------------------------------------")
print("Step 4 : Apply Exponential Mechanism")
print("--------------------------------------------------")

df_noisy = df.copy()

for col in categorical_columns:

    print("\n========================================")
    print("Processing Column :", col)
    print("========================================")

    column_data = df[col].dropna()

    counts = column_data.value_counts()

    categories = counts.index.to_numpy()
    utilities = counts.values.astype(float)

    sensitivity = 1

    scores = (epsilon * utilities) / (2 * sensitivity)

    # Stability trick
    scores = scores - np.max(scores)

    exp_scores = np.exp(scores)

    probabilities = exp_scores / np.sum(exp_scores)

    noisy_values = np.random.choice(
        categories,
        size=len(column_data),
        p=probabilities
    )

    df_noisy.loc[column_data.index, col] = noisy_values

    # 🔥 PRINT DETAILS

    print("\nTop 5 Original Categories (by frequency):")
    for i in range(min(5, len(categories))):
        print(f"{categories[i]} → count = {utilities[i]}")

    print("\nTop 5 Selection Probabilities:")
    for i in range(min(5, len(categories))):
        print(f"{categories[i]} → probability = {probabilities[i]:.4f}")

    print("\nSample Comparison (Original vs Noisy):")
    sample_indices = column_data.index[:5]

    for idx in sample_indices:
        print(f"Original: {df.loc[idx, col]}  →  Noisy: {df_noisy.loc[idx, col]}")


print("\n--------------------------------------------------")
print("Step 5 : Save Differentially Private Dataset")
print("--------------------------------------------------")

output_file = "netflix_exponential_dp_dataset.csv"

df_noisy.to_csv(output_file, index=False)

print("Noisy dataset saved as :", output_file)

print("\n--------------------------------------------------")
print("FINAL SUMMARY")
print("--------------------------------------------------")

print("Dataset Used :", "netflix_titles.csv")
print("Privacy Mechanism :", "Exponential Mechanism")
print("Privacy Budget (epsilon) :", epsilon)
print("Columns Processed :", len(categorical_columns))
print("Output Dataset :", output_file)

print("\nDifferential Privacy successfully applied using Exponential Mechanism")
