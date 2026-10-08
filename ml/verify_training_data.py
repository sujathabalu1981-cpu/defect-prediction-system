import pandas as pd


FILE = "bayesian_training_data.csv"


data = pd.read_csv(FILE)


FEATURES = [
    "LOC",
    "Cyclomatic",
    "Essential",
    "Design",
    "HalsteadVolume",
    "HalsteadDifficulty",
    "HalsteadEffort",
    "BranchCount"
]


print("====================================")
print("BAYESIAN TRAINING DATA VERIFICATION")
print("====================================")

print()

print("Total records:", len(data))

print()


for feature in FEATURES:

    print("------------------------------------")
    print("Metric:", feature)

    print(
        data[feature]
        .value_counts()
        .sort_index()
    )

    print()


print("------------------------------------")
print("Defect distribution")

print(
    data["defects"]
    .value_counts()
)

print()


print("------------------------------------")
print("Dataset distribution")

print(
    data["dataset"]
    .value_counts()
)

print()

print("Verification complete.")