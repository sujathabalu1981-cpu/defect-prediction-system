import pandas as pd

from prepare_dataset import load_dataset

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination

from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)


# ============================================================
# 1. LOAD ORIGINAL CONTINUOUS DATA
# ============================================================

print("Loading original NASA continuous data...")

data = load_dataset()

print("Total records:", len(data))


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


PROJECTS = [
    "CM1",
    "JM1",
    "KC1",
    "KC2",
    "PC1"
]


# ============================================================
# 3. MAKE SURE METRICS ARE NUMERIC
# ============================================================

for feature in FEATURES:

    data[feature] = pd.to_numeric(
        data[feature],
        errors="coerce"
    )


if data[FEATURES].isnull().any().any():

    raise ValueError(
        "Invalid metric values found."
    )


# ============================================================
# 4. THRESHOLD CALCULATION
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
# 5. DISCRETIZATION
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


def discretize(
        dataframe,
        thresholds):

    result = pd.DataFrame(
        index=dataframe.index
    )

    for feature in FEATURES:

        low, medium = thresholds[feature]

        result[feature] = dataframe[
            feature
        ].apply(
            lambda value:
                categorize(
                    value,
                    low,
                    medium
                )
        )

    result[TARGET] = dataframe[TARGET]

    return result


# ============================================================
# 6. CREATE BAYESIAN NETWORK
# ============================================================

def create_model():

    return DiscreteBayesianNetwork(
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
# 7. TRAIN MODEL
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
# 8. PREDICT PROBABILITY
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
# 9. STORE ALL PREDICTIONS
# ============================================================

all_actual = []

all_probabilities = []


# ============================================================
# 10. LEAVE-ONE-PROJECT-OUT
# ============================================================

for test_project in PROJECTS:

    print()
    print("==============================================")
    print("TEST PROJECT:", test_project)
    print("==============================================")


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
    # thresholds come ONLY from training data
    # --------------------------------------------------------

    thresholds = calculate_thresholds(
        training_data
    )


    # --------------------------------------------------------
    # Discretize
    # --------------------------------------------------------

    training_discrete = discretize(
        training_data,
        thresholds
    )


    testing_discrete = discretize(
        testing_data,
        thresholds
    )


    # --------------------------------------------------------
    # Train
    # --------------------------------------------------------

    print("Training Bayesian Network...")

    model = train_model(
        training_discrete[
            FEATURES + [TARGET]
        ]
    )


    inference = VariableElimination(
        model
    )


    # --------------------------------------------------------
    # Predict
    # --------------------------------------------------------

    for _, row in testing_discrete.iterrows():

        probability = predict_probability(
            inference,
            row
        )


        actual_value = (
            1
            if row[TARGET] == "YES"
            else 0
        )


        all_actual.append(
            actual_value
        )


        all_probabilities.append(
            probability
        )


    print("Prediction completed.")


# ============================================================
# 11. ROC-AUC
# ============================================================

auc = roc_auc_score(
    all_actual,
    all_probabilities
)


print()
print()
print("==============================================")
print("LEAKAGE-FREE THRESHOLD ANALYSIS")
print("==============================================")


print(
    "Overall ROC-AUC:",
    round(auc, 4)
)


# ============================================================
# 12. TEST DIFFERENT DECISION THRESHOLDS
# ============================================================

thresholds_to_test = [
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50
]


print()
print(
    "Threshold   Precision   Recall   F1 Score"
)


print(
    "------------------------------------------"
)


results = []


for threshold in thresholds_to_test:

    predictions = [

        1
        if probability >= threshold
        else 0

        for probability in all_probabilities

    ]


    precision = precision_score(
        all_actual,
        predictions,
        zero_division=0
    )


    recall = recall_score(
        all_actual,
        predictions,
        zero_division=0
    )


    f1 = f1_score(
        all_actual,
        predictions,
        zero_division=0
    )


    print(
        f"{threshold:<11.2f}"
        f"{precision:<12.4f}"
        f"{recall:<9.4f}"
        f"{f1:.4f}"
    )


    results.append(
        {
            "threshold": threshold,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
    )


# ============================================================
# 13. FIND BEST F1 THRESHOLD
# ============================================================

results_df = pd.DataFrame(
    results
)


best_result = results_df.loc[
    results_df["f1"].idxmax()
]


print()
print()
print("==============================================")
print("BEST F1 THRESHOLD")
print("==============================================")


print(
    "Threshold:",
    best_result["threshold"]
)


print(
    "Precision:",
    round(
        best_result["precision"],
        4
    )
)


print(
    "Recall:",
    round(
        best_result["recall"],
        4
    )
)


print(
    "F1 Score:",
    round(
        best_result["f1"],
        4
    )
)


print()
print("==============================================")
print("ANALYSIS COMPLETE")
print("==============================================")