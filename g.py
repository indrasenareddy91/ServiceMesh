

import numpy as np
import matplotlib.pyplot as plt

def compute_sensitivity(weights):
    return np.linalg.norm(weights, ord=2)

def gaussian_mechanism(data, weights, epsilon, delta):

    data = np.array(data)
    weights = np.array(weights)

    true_result = np.dot(weights, data)

    sensitivity = compute_sensitivity(weights)

    sigma = (sensitivity * np.sqrt(2 * np.log(1.25/delta))) / epsilon

    noise = np.random.normal(0, sigma)

    private_result = true_result + noise

    return true_result, private_result, sigma


data = [10, 20,20, 30,30,30, 40, 50]
weights = [1, 2,2, 3,3,3, 1, 1]

epsilon = 0.8
delta = 1e-5

true_result, private_result, sigma = gaussian_mechanism(data, weights, epsilon, delta)

print("Dataset:", data)
print("Weights:", weights)
print("True Query Result:", true_result)
print("Noise Scale (sigma):", sigma)
print("Differentially Private Result:", private_result)

noise_samples = np.random.normal(0, sigma,1000)

plt.hist(noise_samples, bins=30)
plt.title("Gaussian Noise Distribution")
plt.xlabel("Noise Value")
plt.ylabel("Frequency")
plt.show()
