import pandas as pd

from prepare_dataset import load_dataset

from decision_engine import make_decision

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination


# ============================================================
# 1. LOAD NASA DATA
# ============================================================

print("Loading NASA dataset...")

data = load_dataset()

print(
    "Total records:",
    len(data)
)


# ============================================================
# 2. RENAME FEATURES
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
# 3. CALCULATE THRESHOLDS
# ============================================================

def calculate_thresholds(data):

    thresholds = {}

    for feature in FEATURES:

        low = data[feature].quantile(0.50)

        medium = data[feature].quantile(0.75)

        thresholds[feature] = (
            low,
            medium
        )

    return thresholds


# ============================================================
# 4. CONVERT VALUE TO LOW / MEDIUM / HIGH
# ============================================================

def categorize(
        value,
        low,
        medium):

    if value <= low:

        return "LOW"

    elif value <= medium:

        return "MEDIUM"

    else:

        return "HIGH"


# ============================================================
# 5. DISCRETIZE DATASET
# ============================================================

def discretize(
        data,
        thresholds):

    result = pd.DataFrame(
        index=data.index
    )

    for feature in FEATURES:

        low, medium = thresholds[feature]

        result[feature] = data[
            feature
        ].apply(
            lambda value:
                categorize(
                    value,
                    low,
                    medium
                )
        )

    result[TARGET] = data[TARGET]

    return result


# ============================================================
# 6. CREATE BAYESIAN NETWORK
# ============================================================

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


# ============================================================
# 7. PREPARE TRAINING DATA
# ============================================================

thresholds = calculate_thresholds(data)

training_data = discretize(
    data,
    thresholds
)


# ============================================================
# 8. TRAIN BAYESIAN NETWORK
# ============================================================

print()
print("Training Bayesian Network...")

estimator = BayesianEstimator(
    model=model,
    data=training_data
)

cpds = estimator.get_parameters(
    prior_type="BDeu",
    equivalent_sample_size=10
)

model.add_cpds(*cpds)

print("Bayesian Network trained successfully.")


# ============================================================
# 9. CREATE INFERENCE ENGINE
# ============================================================

inference = VariableElimination(
    model
)


# ============================================================
# 10. SELECT ONE REAL SOFTWARE MODULE
# ============================================================

sample = training_data.iloc[0]


# ============================================================
# 11. CREATE EVIDENCE
# ============================================================

evidence = {
    feature: sample[feature]
    for feature in FEATURES
}


# ============================================================
# 12. PREDICT DEFECT PROBABILITY
# ============================================================

result = inference.query(
    variables=["defects"],
    evidence=evidence
)


states = result.state_names["defects"]

probabilities = result.values

yes_index = states.index("YES")

defect_probability = probabilities[
    yes_index
]


# ============================================================
# 13. SEND PROBABILITY TO DECISION ENGINE
# ============================================================

decision = make_decision(
    defect_probability
)


# ============================================================
# 14. DISPLAY COMPLETE RESULT
# ============================================================

print()
print()
print("================================================")
print("SOFTWARE DEFECT RISK ANALYSIS")
print("================================================")


print()
print("INPUT METRICS")
print("-----------------------------------------------")


for feature in FEATURES:

    print(
        f"{feature:<22}:",
        sample[feature]
    )


print()
print("PREDICTION")
print("-----------------------------------------------")


print(
    "Defect Probability:",
    f"{defect_probability:.4f}"
)


print(
    "Defect Probability:",
    f"{defect_probability * 100:.2f}%"
)


print()
print("DECISION")
print("-----------------------------------------------")


print(
    "Risk Level:",
    decision["risk_level"]
)


print(
    "Action:",
    decision["action"]
)


print(
    "Message:",
    decision["message"]
)


print()
print("================================================")
print("END-TO-END PREDICTION COMPLETE")
print("================================================")