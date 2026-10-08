import pandas as pd

from prepare_dataset import load_dataset

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# 1. LOAD ORIGINAL CONTINUOUS NASA DATA
# ============================================================

print("Loading original NASA continuous data...")

data = load_dataset()

print("Total records loaded:", len(data))


# ============================================================
# 2. RENAME ORIGINAL METRICS
# ============================================================

data = data.rename(
    columns={
        "loc": "LOC",
        "v(g)": "Cyclomatic",
        "ev(g)": "Essential",
        "iv(g)": "Design",
        "v": "HalsteadVolume",
        "d": "HalsteadDifficulty",
        "e": "HalsteadEffort",
        "branchCount": "BranchCount"
    }
)


# ============================================================
# 3. FEATURES
# ============================================================

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

TARGET = "defects"


# ============================================================
# 4. DATASET NAMES
# ============================================================

PROJECTS = [
    "CM1",
    "JM1",
    "KC1",
    "KC2",
    "PC1"
]


# ============================================================
# 5. CHECK DATA
# ============================================================

print()
print("Checking metric data types...")

for feature in FEATURES:

    data[feature] = pd.to_numeric(
        data[feature],
        errors="coerce"
    )


if data[FEATURES].isnull().any().any():

    print(
        "ERROR: Missing or invalid metric values found."
    )

    print(
        data[FEATURES].isnull().sum()
    )

    raise ValueError(
        "Metric data contains invalid numeric values."
    )


print("All metric columns are numeric.")


# ============================================================
# 6. CALCULATE TRAINING THRESHOLDS
# ============================================================

def calculate_thresholds(training_data):

    thresholds = {}

    for feature in FEATURES:

        low_threshold = (
            training_data[feature]
            .quantile(0.50)
        )

        medium_threshold = (
            training_data[feature]
            .quantile(0.75)
        )

        thresholds[feature] = (
            low_threshold,
            medium_threshold
        )

    return thresholds


# ============================================================
# 7. CONVERT CONTINUOUS VALUE
#    TO LOW / MEDIUM / HIGH
# ============================================================

def categorize(
        value,
        low_threshold,
        medium_threshold):

    if value <= low_threshold:

        return "LOW"

    elif value <= medium_threshold:

        return "MEDIUM"

    else:

        return "HIGH"


# ============================================================
# 8. APPLY TRAINING THRESHOLDS
# ============================================================

def discretize(
        dataframe,
        thresholds):

    result = pd.DataFrame(
        index=dataframe.index
    )

    for feature in FEATURES:

        low_threshold, medium_threshold = (
            thresholds[feature]
        )

        result[feature] = dataframe[
            feature
        ].apply(
            lambda value:
                categorize(
                    value,
                    low_threshold,
                    medium_threshold
                )
        )

    result[TARGET] = dataframe[TARGET]

    return result


# ============================================================
# 9. CREATE BAYESIAN NETWORK
# ============================================================

def create_model():

    model = DiscreteBayesianNetwork(
        [
            ("LOC", "defects"),
            ("Cyclomatic", "defects"),
            ("Essential", "defects"),
            ("Design", "defects"),
            ("HalsteadVolume", "defects"),
            ("HalsteadDifficulty", "defects"),
            ("HalsteadEffort", "defects"),
            ("BranchCount", "defects")
        ]
    )

    return model


# ============================================================
# 10. TRAIN BAYESIAN NETWORK
# ============================================================

def train_model(training_data):

    model = create_model()

    estimator = BayesianEstimator(
        model=model,
        data=training_data
    )

    cpds = estimator.get_parameters(
        prior_type="BDeu",
        equivalent_sample_size=10
    )

    model.add_cpds(*cpds)

    return model


# ============================================================
# 11. GET DEFECT PROBABILITY
# ============================================================

def predict_probability(
        inference,
        row):

    evidence = {
        feature: row[feature]
        for feature in FEATURES
    }

    result = inference.query(
        variables=["defects"],
        evidence=evidence
    )

    states = result.state_names["defects"]

    probabilities = result.values

    yes_index = states.index("YES")

    return probabilities[yes_index]


# ============================================================
# 12. LEAVE-ONE-PROJECT-OUT VALIDATION
# ============================================================

all_results = []


for test_project in PROJECTS:

    print()
    print("================================================")
    print("TEST PROJECT:", test_project)
    print("================================================")

    # --------------------------------------------------------
    # Separate training and testing projects
    # --------------------------------------------------------

    training_data = data[
        data["dataset"] != test_project
    ].copy()

    testing_data = data[
        data["dataset"] == test_project
    ].copy()

    print(
        "Training records:",
        len(training_data)
    )

    print(
        "Testing records:",
        len(testing_data)
    )


    # --------------------------------------------------------
    # IMPORTANT:
    # Calculate thresholds ONLY from training data
    # --------------------------------------------------------

    thresholds = calculate_thresholds(
        training_data
    )


    # --------------------------------------------------------
    # Display training thresholds
    # --------------------------------------------------------

    print()
    print("Training thresholds:")

    for feature in FEATURES:

        low, medium = thresholds[feature]

        print(
            feature,
            "LOW <=",
            round(low, 4),
            "| MEDIUM <=",
            round(medium, 4)
        )


    # --------------------------------------------------------
    # Discretize training data
    # --------------------------------------------------------

    training_discrete = discretize(
        training_data,
        thresholds
    )


    # --------------------------------------------------------
    # Discretize test data
    #
    # IMPORTANT:
    # Use ONLY thresholds learned from training data
    # --------------------------------------------------------

    testing_discrete = discretize(
        testing_data,
        thresholds
    )


    # --------------------------------------------------------
    # Train Bayesian Network
    # --------------------------------------------------------

    print()
    print("Training Bayesian Network...")

    model = train_model(
        training_discrete[
            FEATURES + [TARGET]
        ]
    )

    inference = VariableElimination(
        model
    )

    print("Model trained.")


    # --------------------------------------------------------
    # Predictions
    # --------------------------------------------------------

    actual = []

    predicted = []

    probabilities = []


    for _, row in testing_discrete.iterrows():

        probability = predict_probability(
            inference,
            row
        )

        probabilities.append(
            probability
        )


        # Actual defect value

        actual_value = (
            1
            if row[TARGET] == "YES"
            else 0
        )


        # Current candidate threshold = 0.20

        predicted_value = (
            1
            if probability >= 0.20
            else 0
        )


        actual.append(
            actual_value
        )

        predicted.append(
            predicted_value
        )


    # --------------------------------------------------------
    # Evaluation
    # --------------------------------------------------------

    accuracy = accuracy_score(
        actual,
        predicted
    )

    precision = precision_score(
        actual,
        predicted,
        zero_division=0
    )

    recall = recall_score(
        actual,
        predicted,
        zero_division=0
    )

    f1 = f1_score(
        actual,
        predicted,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        actual,
        probabilities
    )


    # --------------------------------------------------------
    # Display results
    # --------------------------------------------------------

    print()
    print("RESULTS")

    print(
        "Accuracy :",
        round(accuracy, 4)
    )

    print(
        "Precision:",
        round(precision, 4)
    )

    print(
        "Recall   :",
        round(recall, 4)
    )

    print(
        "F1 Score :",
        round(f1, 4)
    )

    print(
        "ROC-AUC  :",
        round(roc_auc, 4)
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    all_results.append(
        {
            "project": test_project,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "roc_auc": roc_auc
        }
    )


# ============================================================
# 13. AVERAGE RESULTS
# ============================================================

results_df = pd.DataFrame(
    all_results
)


print()
print()
print("================================================")
print("LEAKAGE-FREE LOPO AVERAGE")
print("================================================")


print(
    "Average Accuracy :",
    round(
        results_df["accuracy"].mean(),
        4
    )
)


print(
    "Average Precision:",
    round(
        results_df["precision"].mean(),
        4
    )
)


print(
    "Average Recall   :",
    round(
        results_df["recall"].mean(),
        4
    )
)


print(
    "Average F1 Score :",
    round(
        results_df["f1"].mean(),
        4
    )
)


print(
    "Average ROC-AUC  :",
    round(
        results_df["roc_auc"].mean(),
        4
    )
)


print()
print("================================================")
print("LEAKAGE-FREE EVALUATION COMPLETE")
print("================================================")