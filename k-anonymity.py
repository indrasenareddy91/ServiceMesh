import pandas as pd

df_original = pd.read_csv("medical.csv")

def generalize_data(df, k):
    df = df.copy()

    if k == 2:
        bins = [0, 30, 50, 70, 120]
        labels = ['<30', '30-50', '50-70', '70+']
        df['Age'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
        df['Gender'] = df['Gender'].astype(str).str.strip()
        df['Blood Type'] = df['Blood Type'].astype(str).str.strip().apply(
            lambda x: x[0] if x.startswith(('A', 'B', 'O')) else 'AB'
        )
        df['Insurance Provider'] = df['Insurance Provider'].astype(str).str.strip().apply(
            lambda x: 'Public' if x == 'Medicare' else 'Private'
        )
        df['Admission Type'] = df['Admission Type'].astype(str).str.strip()

    elif k == 3:
        bins = [0, 50, 120]
        labels = ['<50', '50+']
        df['Age'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
        df['Gender'] = 'Person'
        df['Blood Type'] = 'Any'
        df['Insurance Provider'] = df['Insurance Provider'].astype(str).str.strip().apply(
            lambda x: 'Public' if x == 'Medicare' else 'Private'
        )
        df['Admission Type'] = 'Any'

    elif k == 4:
        df['Age'] = df['Age'].apply(lambda x: '<50' if x < 50 else '50+')
        df['Gender'] = 'Person'
        df['Blood Type'] = 'Any'
        df['Insurance Provider'] = 'Any'
        df['Admission Type'] = 'Any'

    return df

def check_k_anonymity_and_print(df, quasi_identifiers, k):
    eq_classes = (
        df.groupby(quasi_identifiers)
          .size()
          .reset_index(name='count')
    )

    achieved = eq_classes[eq_classes['count'] >= k]
    violating = eq_classes[eq_classes['count'] < k]

    print("\n" + "-" * 60)
    print(f"{k}-ANONYMITY RESULTS")
    print("-" * 60)

    if not achieved.empty:
        print(f"\nSegments ACHIEVING {k}-Anonymity:")
        print(achieved)
    else:
        print(f"\nNo segments achieve {k}-Anonymity")

    if not violating.empty:
        print(f"\nSegments VIOLATING {k}-Anonymity:")
        print(violating)
    else:
        print(f"\nNo violating segments for {k}-Anonymity")

    return violating.empty

quasi_identifiers = [
    'Age',
    'Gender',
    'Blood Type',
    'Insurance Provider',
    'Admission Type'
]

results = {}

for k in [2, 3]:
    print("\n" + "=" * 70)
    print(f"PROCESSING {k}-ANONYMITY")
    print("=" * 70)

    df_gen = generalize_data(df_original, k)
    results[k] = check_k_anonymity_and_print(df_gen, quasi_identifiers, k)
    df_gen.to_csv(f"medical_{k}_anonymized.csv", index=False)
    print(f"\nSaved file: medical_{k}_anonymized.csv")

print("\n" + "=" * 70)
print("PROCESSING 4-ANONYMITY (FULL DATASET)")
print("=" * 70)

df_k4_full = generalize_data(df_original, 4)
results[4] = check_k_anonymity_and_print(df_k4_full, quasi_identifiers, 4)
df_k4_full.to_csv("medical_4_anonymized_full.csv", index=False)
print("\nSaved file: medical_4_anonymized_full.csv")

print("\n" + "=" * 70)
print("FINAL CONCLUSION")
print("=" * 70)

for k, status in results.items():
    if status:
        print(f"{k}-Anonymity: ACHIEVED for entire dataset")
    else:
        print(f"{k}-Anonymity: PARTIALLY achieved")
