import pandas as pd

from sklearn.model_selection import train_test_split
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


# ==========================================
# 1. Load dataset
# ==========================================

data = pd.read_csv(
    "bayesian_training_data.csv"
)


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


model_data = data[
    FEATURES + [TARGET]
].copy()


# ==========================================
# 2. Same train/test split
# ==========================================

train_data, test_data = train_test_split(
    model_data,
    test_size=0.20,
    random_state=42,
    stratify=model_data[TARGET]
)


print("======================================")
print("BAYESIAN NETWORK EVALUATION")
print("======================================")

print("Training records:", len(train_data))
print("Testing records:", len(test_data))


# ==========================================
# 3. Define network
# ==========================================

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


# ==========================================
# 4. Train Bayesian Network
# ==========================================

print()
print("Training model...")

estimator = BayesianEstimator(
    model=model,
    data=train_data
)

cpds = estimator.get_parameters(
    prior_type="BDeu",
    equivalent_sample_size=10
)

model.add_cpds(*cpds)

print("Model trained.")


# ==========================================
# 5. Create inference engine
# ==========================================

inference = VariableElimination(model)


# ==========================================
# 6. Predict every test record
# ==========================================

actual = []
predicted = []
probability_yes = []


print()
print("Predicting test records...")


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

    if yes_probability >= 0.50:
        prediction = "YES"
    else:
        prediction = "NO"

    actual.append(row["defects"])
    predicted.append(prediction)
    probability_yes.append(yes_probability)


# ==========================================
# 7. Calculate metrics
# ==========================================

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
    [1 if value == "YES" else 0 for value in actual],
    probability_yes
)


# ==========================================
# 8. Confusion Matrix
# ==========================================

matrix = confusion_matrix(
    actual,
    predicted,
    labels=["NO", "YES"]
)


# ==========================================
# 9. Display results
# ==========================================

print()
print("======================================")
print("MODEL PERFORMANCE")
print("======================================")

print(
    "Accuracy :", round(accuracy, 4)
)

print(
    "Precision:", round(precision, 4)
)

print(
    "Recall   :", round(recall, 4)
)

print(
    "F1 Score :", round(f1, 4)
)

print(
    "ROC-AUC  :", round(auc, 4)
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