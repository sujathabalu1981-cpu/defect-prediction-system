import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
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


# ======================================
# PROJECT-WISE SPLIT
# ======================================

TRAIN_PROJECTS = [
    "CM1",
    "JM1",
    "KC1",
    "KC2"
]

TEST_PROJECT = "PC1"


train_data = data[
    data["dataset"].isin(TRAIN_PROJECTS)
].copy()

test_data = data[
    data["dataset"] == TEST_PROJECT
].copy()


print("======================================")
print("PROJECT-WISE BAYESIAN NETWORK EVALUATION")
print("======================================")

print()
print("Training projects:")
for project in TRAIN_PROJECTS:
    print("-", project)

print()
print("Testing project:")
print("-", TEST_PROJECT)

print()
print("Training records:", len(train_data))
print("Testing records :", len(test_data))


# ======================================
# CREATE MODEL DATA
# ======================================

train_model_data = train_data[
    FEATURES + [TARGET]
].copy()

test_model_data = test_data[
    FEATURES + [TARGET]
].copy()


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
# TRAIN MODEL
# ======================================

print()
print("Training Bayesian Network...")

estimator = BayesianEstimator(
    model=model,
    data=train_model_data
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
# PREDICT TEST PROJECT
# ======================================

actual = []
predicted = []
probability_yes = []


print()
print("Predicting unseen project:", TEST_PROJECT)


for _, row in test_model_data.iterrows():

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

    # Current threshold
    threshold = 0.20

    if yes_probability >= threshold:
        prediction = "YES"
    else:
        prediction = "NO"

    actual.append(row["defects"])
    predicted.append(prediction)
    probability_yes.append(yes_probability)


# ======================================
# CALCULATE PERFORMANCE
# ======================================

accuracy = accuracy_score(
    actual,
    predicted
)

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

auc = roc_auc_score(
    [
        1 if value == "YES" else 0
        for value in actual
    ],
    probability_yes
)


# ======================================
# DISPLAY PERFORMANCE
# ======================================

print()
print("======================================")
print("PROJECT-WISE PERFORMANCE")
print("======================================")

print("Accuracy :", round(accuracy, 4))
print("Precision:", round(precision, 4))
print("Recall   :", round(recall, 4))
print("F1 Score :", round(f1, 4))
print("ROC-AUC  :", round(auc, 4))


# ======================================
# CONFUSION MATRIX
# ======================================

matrix = confusion_matrix(
    actual,
    predicted,
    labels=["NO", "YES"]
)


print()
print("======================================")
print("CONFUSION MATRIX")
print("======================================")

print("              Predicted")
print("              NO       YES")

print(
    "Actual NO   ",
    matrix[0][0],
    "     ",
    matrix[0][1]
)

print(
    "Actual YES  ",
    matrix[1][0],
    "     ",
    matrix[1][1]
)


# ======================================
# CLASSIFICATION REPORT
# ======================================

print()
print("======================================")
print("CLASSIFICATION REPORT")
print("======================================")

print(
    classification_report(
        actual,
        predicted,
        labels=["NO", "YES"],
        zero_division=0
    )
)


print()
print("======================================")
print("PROJECT-WISE EVALUATION COMPLETED")
print("======================================")