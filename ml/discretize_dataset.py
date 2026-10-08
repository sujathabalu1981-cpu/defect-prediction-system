import pandas as pd
from pathlib import Path

from prepare_dataset import load_dataset


# Output file
OUTPUT_FILE = Path("bayesian_training_data.csv")


def categorize(value, low_threshold, medium_threshold):

    if value <= low_threshold:
        return "LOW"

    elif value <= medium_threshold:
        return "MEDIUM"

    else:
        return "HIGH"


def discretize_dataset(data):

    data["LOC"] = data["loc"].apply(
        lambda x: categorize(x, 19, 40)
    )

    data["Cyclomatic"] = data["v(g)"].apply(
        lambda x: categorize(x, 3, 6)
    )

    data["Essential"] = data["ev(g)"].apply(
        lambda x: categorize(x, 1, 3)
    )

    data["Design"] = data["iv(g)"].apply(
        lambda x: categorize(x, 2, 4)
    )

    data["HalsteadVolume"] = data["v"].apply(
        lambda x: categorize(x, 187.65, 564.945)
    )

    data["HalsteadDifficulty"] = data["d"].apply(
        lambda x: categorize(x, 8.33, 17.27)
    )

    data["HalsteadEffort"] = data["e"].apply(
        lambda x: categorize(x, 1618.61, 9565.61)
    )

    data["BranchCount"] = data["branchCount"].apply(
        lambda x: categorize(x, 5, 11)
    )

    # Keep only Bayesian Network columns
    result = data[
        [
            "LOC",
            "Cyclomatic",
            "Essential",
            "Design",
            "HalsteadVolume",
            "HalsteadDifficulty",
            "HalsteadEffort",
            "BranchCount",
            "defects",
            "dataset"
        ]
    ].copy()

    return result


if __name__ == "__main__":

    print("Loading NASA dataset...")

    data = load_dataset()

    print("Discretizing metrics...")

    result = discretize_dataset(data)

    result.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print()
    print("==============================")
    print("DISCRETIZATION COMPLETE")
    print("==============================")

    print("Total records:", len(result))

    print()
    print("Example records:")

    print(result.head())

    print()
    print("Output file:")

    print(OUTPUT_FILE.resolve())