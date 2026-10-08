import pandas as pd
from pathlib import Path


# NASA dataset location
DATASET_FOLDER = Path(
    r"D:\Fourth year projects\Sw metrics\NASA-promise-dataset-repository-main"
)


# Dataset files
DATASETS = {
    "CM1": ("cm1.csv", "defects"),
    "JM1": ("jm1.csv", "defects"),
    "KC1": ("kc1.csv", "defects"),
    "KC2": ("kc2.csv", "problems"),
    "PC1": ("pc1.csv", "defects")
}


# The 8 metrics selected for our Bayesian Network
FEATURES = [
    "loc",
    "v(g)",
    "ev(g)",
    "iv(g)",
    "v",
    "d",
    "e",
    "branchCount"
]


def standardize_columns(data):

    column_mapping = {}

    for column in data.columns:

        clean_name = column.strip()

        # Convert different capitalization to our standard names
        lower_name = clean_name.lower()

        if lower_name == "loc":
            column_mapping[column] = "loc"

        elif lower_name == "v(g)":
            column_mapping[column] = "v(g)"

        elif lower_name == "ev(g)":
            column_mapping[column] = "ev(g)"

        elif lower_name == "iv(g)":
            column_mapping[column] = "iv(g)"

        elif lower_name == "v":
            column_mapping[column] = "v"

        elif lower_name == "d":
            column_mapping[column] = "d"

        elif lower_name == "e":
            column_mapping[column] = "e"

        elif lower_name == "branchcount":
            column_mapping[column] = "branchCount"

        elif lower_name == "defects":
            column_mapping[column] = "defects"

        elif lower_name == "problems":
            column_mapping[column] = "problems"

    return data.rename(columns=column_mapping)


def load_dataset():

    all_data = []

    for dataset_name, (file_name, target_column) in DATASETS.items():

        file_path = DATASET_FOLDER / file_name

        print(f"Loading {dataset_name}...")

        data = pd.read_csv(file_path)

        print("Rows:", len(data))
        print("Columns:", len(data.columns))

        # Standardize column names
        data = standardize_columns(data)

        # Rename target column to common name
        if target_column != "defects":

            data = data.rename(
                columns={
                    target_column: "defects"
                }
            )

        # Select only required columns
        selected_columns = FEATURES + ["defects"]

        data = data[selected_columns].copy()

         # Standardize defect labels
        data["defects"] = (
        data["defects"]
        .astype(str)
        .str.strip()
        .str.lower()
         .map({
        "true": "YES",
        "yes": "YES",
        "false": "NO",
        "no": "NO"
        })
         )

        # Add dataset name
        data["dataset"] = dataset_name

        all_data.append(data)

    combined_data = pd.concat(
        all_data,
        ignore_index=True
    )

    return combined_data


if __name__ == "__main__":

    data = load_dataset()

    print()
    print("================================")
    print("NASA DATASET PREPARATION")
    print("================================")

    print("Total records:", len(data))

    print()
    print("Selected features:")

    for feature in FEATURES:
        print("-", feature)

    print()
    print("Defect distribution:")
    print(data["defects"].value_counts())

    print()
    print("Dataset distribution:")
    print(data["dataset"].value_counts())

    print()
    print("First 5 records:")
    print(data.head())