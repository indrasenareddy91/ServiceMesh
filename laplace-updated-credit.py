import pandas as pd
import numpy as np
import math
import random

df = pd.read_csv("UCI_Credit_Card.csv")

epsilon = 0.5

print("========== LAPLACE MECHANISM IMPLEMENTATION ==========")

def laplace_noise(sensitivity, epsilon):

    b = sensitivity / epsilon

    U = random.uniform(-0.5, 0.5)

    noise = -b * np.sign(U) * math.log(1 - 2 * abs(U))

    return noise


print("\n----- COUNT QUERY -----")

true_count = df["default.payment.next.month"].sum()

sensitivity_count = 1

noise_count = laplace_noise(sensitivity_count, epsilon)

noisy_count = true_count + noise_count

print("True Default Count :", true_count)
print("Noise Added        :", noise_count)
print("Noisy Default Count:", noisy_count)

print("\n----- AVERAGE QUERY -----")

true_avg = df["LIMIT_BAL"].mean()

max_val = df["LIMIT_BAL"].max()
min_val = df["LIMIT_BAL"].min()

n = len(df)

sensitivity_avg = (max_val - min_val) / n

noise_avg = laplace_noise(sensitivity_avg, epsilon)

noisy_avg = true_avg + noise_avg

print("True Average LIMIT_BAL :", true_avg)
print("Noise Added            :", noise_avg)
print("Noisy Average LIMIT_BAL:", noisy_avg)

print("\n----- ADDING LAPLACE NOISE TO DATASET -----")

numeric_columns = [
    "LIMIT_BAL","AGE",
    "BILL_AMT1","BILL_AMT2","BILL_AMT3",
    "BILL_AMT4","BILL_AMT5","BILL_AMT6",
    "PAY_AMT1","PAY_AMT2","PAY_AMT3",
    "PAY_AMT4","PAY_AMT5","PAY_AMT6"
]

df_noisy = df.copy()

for col in numeric_columns:

    sensitivity = df[col].max() - df[col].min()

    noisy_values = []

    for value in df[col]:

        noise = laplace_noise(sensitivity, epsilon)

        noisy_values.append(value + noise)

    df_noisy[col] = noisy_values


df_noisy.to_csv("credit_data_noisy_manual_laplace.csv", index=False)

print("Noisy dataset saved as: credit_data_noisy_manual_laplace.csv")