import pandas as pd
import numpy as np
from collections import Counter
import math

FILE_PATH = "anonymized_adult_xy.csv"

QI_COLS = ["age", "education", "marital-status", "occupation"]
SENSITIVE = "income"

T = 0.2   

OUT_DATA = "t_closeness_output.csv"
OUT_STATS = "t_closeness_stats.csv"

df = pd.read_csv(FILE_PATH)
print("\nDataset loaded")
print("Records:", len(df))

global_counts = Counter(df[SENSITIVE])
total = len(df)
GLOBAL_DIST = {k: v/total for k,v in global_counts.items()}

print("\nGlobal Sensitive Attribute Distribution:")
for k,v in GLOBAL_DIST.items():
    print(f"{k}: {round(v,3)}")


def emd(dist1, dist2):
    keys = set(dist1.keys()).union(dist2.keys())
    return sum(abs(dist1.get(k,0) - dist2.get(k,0)) for k in keys) / 2


groups = df.groupby(QI_COLS)

def class_distribution(values):
    c = Counter(values)
    total = len(values)
    return {k: v/total for k,v in c.items()}

bad_classes = []
good_classes = []

for name, g in groups:
    cd = class_distribution(list(g[SENSITIVE]))
    d = emd(cd, GLOBAL_DIST)

    if d > T:
        bad_classes.append(name)
    else:
        good_classes.append(name)

print("\nT-closeness violating classes:", len(bad_classes))
print("T-closeness compliant classes:", len(good_classes))



donors = []
for k in good_classes:
    donors.extend(groups.get_group(k).index.tolist())

np.random.shuffle(donors)



for k in bad_classes:
    rows = groups.get_group(k).index.tolist()

    for _ in range(2):   # two small adjustments
        if not donors:
            break

        donor = donors.pop()
        newval = df.at[donor, SENSITIVE]

        r = np.random.choice(rows)
        df.at[r, SENSITIVE] = newval

print("t-closeness enforcement completed")



final_groups = df.groupby(QI_COLS)
viol = 0
stats = []

print("\n=============== T-CLOSENESS REPORT ===============\n")
print(f"{'QI_Values':60} {'Size':5} {'Distance':8} Status")

for name, g in final_groups:
    cd = class_distribution(list(g[SENSITIVE]))
    d = emd(cd, GLOBAL_DIST)

    status="PASS"
    if d > T:
        status="FAIL"
        viol+=1

    print(f"{str(name):60} {len(g):5} {d:8.3f} {status}")

    stats.append({
        "QI_Values": name,
        "Group_Size": len(g),
        "EMD_Distance": round(d,3),
        "Status": status
    })

print("\n==============================================")
print("Total Classes :", len(stats))
print("Violations    :", viol)
print("Compliant     :", len(stats)-viol)
print("==============================================\n")



df.to_csv(OUT_DATA, index=False)
pd.DataFrame(stats).to_csv(OUT_STATS, index=False)

print("Saved t-closeness dataset:", OUT_DATA)
print("Saved statistics:", OUT_STATS)
