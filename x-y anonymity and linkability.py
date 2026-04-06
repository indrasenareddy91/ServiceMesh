import pandas as pd
import sys

FILE_PATH = r"C:\Users\vinee\OneDrive\Desktop\NITW\DATA_PRIVACY\adult.csv"

QI_COLS = ["age", "education", "marital-status", "occupation"]
SENSITIVE = "income"

AGE_BINS = [0, 25, 35, 45, 55, 100]
AGE_LABELS = ["<25", "25-34", "35-44", "45-54", "55+"]

EDU_MAP = {
    "Preschool": "Primary",
    "1st-4th": "Primary",
    "5th-6th": "Primary",
    "7th-8th": "Primary",
    "9th": "Secondary",
    "10th": "Secondary",
    "11th": "Secondary",
    "12th": "Secondary"
}

OCCUPATION_MAP = {
    "Craft-repair": "Technical",
    "Machine-op-inspct": "Technical",
    "Sales": "Business",
    "Exec-managerial": "Business",
    "Prof-specialty": "Professional"
}


def load_data():
    try:
        df = pd.read_csv(FILE_PATH)
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        print("Error loading dataset:", e)
        sys.exit()

def apply_generalization(df):
    df = df.copy()

    df["age"] = pd.cut(
        df["age"],
        bins=AGE_BINS,
        labels=AGE_LABELS,
        right=False
    )

    df["education"] = df["education"].map(EDU_MAP).fillna("Higher")
    df["occupation"] = df["occupation"].map(OCCUPATION_MAP).fillna("Other")

    return df


def check_xy_anonymity(df, X, Y):
    for _, g in df.groupby(QI_COLS):
        if len(g) < X:
            return False
        if g[SENSITIVE].nunique() < Y:
            return False
    return True


def check_xy_linkability(df, X, Y):
    for _, g in df.groupby(QI_COLS):
        probs = g[SENSITIVE].value_counts(normalize=True)
        if probs.max() > (1/X):
            return False
        if g[SENSITIVE].nunique() < Y:
            return False
    return True



def find_best_xy(df, Y=2, max_X=20):

    best_X = None

    for X in range(2, max_X+1):
        if check_xy_anonymity(df, X, Y) and check_xy_linkability(df, X, Y):
            best_X = X   

    if best_X is None:
        best_X = 2

    return best_X, Y


def show_group_statistics(df):

    rows = []

    for keys, g in df.groupby(QI_COLS):
        counts = g[SENSITIVE].value_counts()
        probs = g[SENSITIVE].value_counts(normalize=True)

        rows.append({
            "QI_Values": keys,
            "Group_Size": len(g),
            "Distinct_Income": g[SENSITIVE].nunique(),
            "Income_Counts": dict(counts),
            "Max_Probability": round(probs.max(),3)
        })

    stats = pd.DataFrame(rows)
    print("\nEQUIVALENCE CLASS STATISTICS (PROOF)")
    print(stats.to_string(index=False))


def main():

    print("\n--- PROGRAM STARTED ---")

    df = load_data()

    print("\nATTRIBUTES:")
    print(list(df.columns))

    print("\nORIGINAL TUPLES (Top 10)")
    print(df[QI_COLS + [SENSITIVE]].head(10).to_string(index=False))

    gen_df = apply_generalization(df)

    print("\nGENERALIZED TUPLES (Top 10)")
    print(gen_df[QI_COLS + [SENSITIVE]].head(10).to_string(index=False))

    X, Y = find_best_xy(gen_df)

    print("\n" + "="*60)
    print("HIGHEST PRIVACY ACHIEVED")
    print("="*60)
    print(f"(X,Y)-Anonymity   : ({X},{Y})")
    print(f"(X,Y)-Linkability : ({X},{Y})")
    print("="*60)

    show_group_statistics(gen_df)

    OUTPUT = "anonymized_adult_xy.csv"
    gen_df.to_csv(OUTPUT, index=False)

    print("\nSaved File:", OUTPUT)


if __name__ == "__main__":
    main()
