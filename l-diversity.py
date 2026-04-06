import pandas as pd
import numpy as np
import math
from collections import Counter

# =======================================================
# CONFIGURATION
# =======================================================

FILE_PATH = "C:\\Users\\vinee\\OneDrive\\Desktop\\NITW\\DATA_PRIVACY\\anonymized_adult_xy.csv"

QI_COLS = ["age", "education", "marital-status", "occupation"]
SENSITIVE_COL = "income"

L = 2   # l-diversity requirement

OUTPUT_FILE = "C:\\Users\\vinee\\OneDrive\\Desktop\\NITW\\DATA_PRIVACY\\l_diverse_output.csv"
STATS_FILE  = "C:\\Users\\vinee\\OneDrive\\Desktop\\NITW\\DATA_PRIVACY\\l_diverse_stats.csv"

# =======================================================
# HELPER FUNCTIONS
# =======================================================

def entropy(values):
    total = len(values)
    counts = Counter(values)
    ent = 0
    for c in counts.values():
        p = c / total
        ent -= p * math.log2(p)
    return ent

def max_probability(values):
    total = len(values)
    counts = Counter(values)
    return max(c / total for c in counts.values())

def is_bad(distinct, ent):
    return distinct < L or ent < math.log2(L)

# =======================================================
# LOAD DATA
# =======================================================

df = pd.read_csv(FILE_PATH)
print("\nDataset loaded successfully")
print("Total records:", len(df))

# =======================================================
# BUILD EQUIVALENCE CLASSES
# =======================================================

groups = df.groupby(QI_COLS)
ec_info = {}

for name, g in groups:
    vals = list(g[SENSITIVE_COL])
    ec_info[name] = {
        "rows": g.index.tolist(),
        "distinct": len(set(vals)),
        "entropy": entropy(vals)
    }

print("Total equivalence classes formed:", len(ec_info))

# =======================================================
# IDENTIFY BAD & GOOD CLASSES
# =======================================================

bad_classes = []
good_classes = []

for k, v in ec_info.items():
    if is_bad(v["distinct"], v["entropy"]):
        bad_classes.append(k)
    else:
        good_classes.append(k)

print("L-diversity violating classes :", len(bad_classes))
print("L-diversity compliant classes :", len(good_classes))

# =======================================================
# CREATE DONOR POOL
# =======================================================

donor_rows = []
for k in good_classes:
    donor_rows.extend(ec_info[k]["rows"])

np.random.shuffle(donor_rows)

# =======================================================
# FIX BAD CLASSES (ENFORCE L-DIVERSITY)
# =======================================================

for k in bad_classes:
    rows = ec_info[k]["rows"]
    current_vals = list(df.loc[rows, SENSITIVE_COL])
    needed = L - len(set(current_vals))

    if needed <= 0:
        continue

    for _ in range(needed):
        if not donor_rows:
            break

        donor_idx = donor_rows.pop()
        donor_value = df.at[donor_idx, SENSITIVE_COL]

        replace_idx = np.random.choice(rows)
        df.at[replace_idx, SENSITIVE_COL] = donor_value

print("L-diversity enforcement completed")

# =======================================================
# FINAL VERIFICATION + TERMINAL REPORT
# =======================================================

final_groups = df.groupby(QI_COLS)
violations = 0
stats = []

print("\n================ L-DIVERSITY EQUIVALENCE CLASS STATISTICS ================\n")
print(f"{'QI_Values':60} {'Size':5} {'Distinct':8} {'Entropy':8} {'MaxProb':8} Status")

for name, g in final_groups:
    vals = list(g[SENSITIVE_COL])

    size = len(g)
    distinct = len(set(vals))
    ent = entropy(vals)
    maxp = max_probability(vals)

    status = "PASS"
    if is_bad(distinct, ent):
        status = "FAIL"
        violations += 1

    print(f"{str(name):60} {size:5} {distinct:8} {ent:8.3f} {maxp:8.3f} {status}")

    stats.append({
        "QI_Values": name,
        "Group_Size": size,
        "Distinct_Income": distinct,
        "Entropy": round(ent, 3),
        "Max_Probability": round(maxp, 3),
        "Status": status
    })

print("\n==========================================================================")
print("L-DIVERSITY SUMMARY")
print("--------------------------------------------------------------------------")
print("Total equivalence classes :", len(stats))
print("Required l value          :", L)
print("Violating classes         :", violations)
print("Compliant classes         :", len(stats) - violations)
print("==========================================================================\n")

# =======================================================
# SAVE OUTPUT FILES
# =======================================================

df.to_csv(OUTPUT_FILE, index=False)
pd.DataFrame(stats).to_csv(STATS_FILE, index=False)

print("Saved l-diverse dataset  :", OUTPUT_FILE)
print("Saved statistics report :", STATS_FILE)
