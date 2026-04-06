import numpy as np 
import pandas as pd 

np.random.seed(42)
n = 1000
true_smoker_population = 0.30
p_values = [0.6, 0.7, 0.8, 0.9]

true_data = np.random.choice(
    [1,0],
    size=n,
    p=[true_smoker_population, 1-true_smoker_population])
    
true_df = pd.DataFrame({"Smoker" : true_data})
true_df.to_csv("true_dataset.csv",index=False)

print("True dataset saved as true_dataset_saved.csv file")
print("True proportion of smokers : ",round(np.mean(true_data),3))

def randomized_response(data, p):
    noisy = []
    for x in data:
        if np.random.rand() < p:
            noisy.append(x)
        else:
            noisy.append(np.random.choice([0,1]))
    return np.array(noisy)
    
def estimate_true_population(noisy_data, p):
    observed_mean = np.mean(noisy_data)
    estimated_mean = (observed_mean-(1-p)/2)/p
    return estimated_mean
    
results = []

for p in p_values:
    noisy_data = randomized_response(true_data, p)
    
    pd.DataFrame({"Noisy_Response ": noisy_data}).to_csv(f"noisy_dataset{int(p*10)}.csv",index=False)
    
    results.append({
        "p-value":p,
        "Observed-mean": np.mean(noisy_data),
        "Estimated Population":estimate_true_population(noisy_data,p)
    })
    
results_df = pd.DataFrame(results)

print(results_df.round(3))