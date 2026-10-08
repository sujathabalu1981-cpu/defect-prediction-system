import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score
)

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination


# ======================================
# LOAD DATASET
# ======================================

data = pd.read_csv("bayesian_training_data.csv")

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

model_data = data[FEATURES + [TARGET]].copy()


# ======================================
# TRAIN / TEST SPLIT
# ======================================

train_data, test_data = train_test_split(
    model_data,
    test_size=0.20,
    random_state=42,
    stratify=model_data[TARGET]
)


print("======================================")
print("THRESHOLD ANALYSIS")
print("======================================")

print("Training records:", len(train_data))
print("Testing records :", len(test_data))


# ======================================
# CREATE BAYESIAN NETWORK
# ======================================

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


# ======================================
# TRAIN BAYESIAN NETWORK
# ======================================

print()
print("Training Bayesian Network...")

estimator = BayesianEstimator(
    model=model,
    data=train_data
)

cpds = estimator.get_parameters(
    prior_type="BDeu",
    equivalent_sample_size=10
)

model.add_cpds(*cpds)

print("Model trained successfully.")


# ======================================
# CREATE INFERENCE ENGINE
# ======================================

inference = VariableElimination(model)


# ======================================
# GET DEFECT PROBABILITIES
# ======================================

actual = []
probability_yes = []

print()
print("Calculating defect probabilities...")

for _, row in test_data.iterrows():

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

    yes_probability = probabilities[yes_index]

    actual.append(row["defects"])

    probability_yes.append(yes_probability)


# ======================================
# TEST DIFFERENT THRESHOLDS
# ======================================

thresholds = [
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90
]


print()
print("======================================")
print("THRESHOLD RESULTS")
print("======================================")

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1 Score':<12}"
)

print("--------------------------------------")


for threshold in thresholds:

    predicted = []

    for probability in probability_yes:

        if probability >= threshold:
            predicted.append("YES")
        else:
            predicted.append("NO")

    precision = precision_score(
        actual,
        predicted,
        pos_label="YES",
        zero_division=0
    )

    recall = recall_score(
        actual,
        predicted,
        pos_label="YES",
        zero_division=0
    )

    f1 = f1_score(
        actual,
        predicted,
        pos_label="YES",
        zero_division=0
    )

    print(
        f"{threshold:<12.2f}"
        f"{precision:<12.4f}"
        f"{recall:<12.4f}"
        f"{f1:<12.4f}"
    )


print("--------------------------------------")
print("Threshold analysis completed.")