import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
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

PROJECTS = [
    "CM1",
    "JM1",
    "KC1",
    "KC2",
    "PC1"
]


# ======================================
# DISPLAY EXPERIMENT INFORMATION
# ======================================

print("======================================")
print("LEAVE-ONE-PROJECT-OUT VALIDATION")
print("======================================")

print()
print("Projects:")
for project in PROJECTS:
    print("-", project)

print()
print("Total records:", len(data))


# ======================================
# STORE RESULTS
# ======================================

all_results = []


# ======================================
# RUN EACH PROJECT AS TEST PROJECT
# ======================================

for test_project in PROJECTS:

    print()
    print("======================================")
    print("TEST PROJECT:", test_project)
    print("======================================")


    # ----------------------------------
    # Select training and testing data
    # ----------------------------------

    train_data = data[
        data["dataset"] != test_project
    ].copy()

    test_data = data[
        data["dataset"] == test_project
    ].copy()


    print(
        "Training records:",
        len(train_data)
    )

    print(
        "Testing records :",
        len(test_data)
    )


    # ----------------------------------
    # Prepare model data
    # ----------------------------------

    train_model_data = train_data[
        FEATURES + [TARGET]
    ].copy()

    test_model_data = test_data[
        FEATURES + [TARGET]
    ].copy()


    # ----------------------------------
    # Create Bayesian Network
    # ----------------------------------

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


    # ----------------------------------
    # Train model
    # ----------------------------------

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

    print("Model trained.")


    # ----------------------------------
    # Create inference engine
    # ----------------------------------

    inference = VariableElimination(model)


    # ----------------------------------
    # Prediction
    # ----------------------------------

    actual = []

    predicted = []

    probability_yes = []


    print(
        "Predicting",
        test_project,
        "records..."
    )


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

        probability_yes.append(
            yes_probability
        )


    # ----------------------------------
    # Calculate metrics
    # ----------------------------------

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


    # ROC-AUC requires both classes
    if len(set(actual)) == 2:

        auc = roc_auc_score(
            [
                1 if value == "YES" else 0
                for value in actual
            ],
            probability_yes
        )

    else:

        auc = 0.0


    # ----------------------------------
    # Store results
    # ----------------------------------

    all_results.append(
        {
            "Project": test_project,
            "Accuracy": accuracy,
            "Precision": precision,
            "Recall": recall,
            "F1": f1,
            "ROC-AUC": auc
        }
    )


    # ----------------------------------
    # Display project result
    # ----------------------------------

    print()
    print("Results for", test_project)

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
        round(auc, 4)
    )


# ======================================
# CREATE RESULTS DATAFRAME
# ======================================

results = pd.DataFrame(all_results)


# ======================================
# CALCULATE AVERAGES
# ======================================

average_accuracy = results["Accuracy"].mean()

average_precision = results["Precision"].mean()

average_recall = results["Recall"].mean()

average_f1 = results["F1"].mean()

average_auc = results["ROC-AUC"].mean()


# ======================================
# DISPLAY FINAL RESULTS
# ======================================

print()
print()
print("======================================")
print("FINAL LOPO RESULTS")
print("======================================")


print(
    results.to_string(
        index=False,
        formatters={
            "Accuracy": "{:.4f}".format,
            "Precision": "{:.4f}".format,
            "Recall": "{:.4f}".format,
            "F1": "{:.4f}".format,
            "ROC-AUC": "{:.4f}".format
        }
    )
)


print()
print("======================================")
print("AVERAGE PERFORMANCE")
print("======================================")


print(
    "Average Accuracy :",
    round(average_accuracy, 4)
)

print(
    "Average Precision:",
    round(average_precision, 4)
)

print(
    "Average Recall   :",
    round(average_recall, 4)
)

print(
    "Average F1 Score :",
    round(average_f1, 4)
)

print(
    "Average ROC-AUC  :",
    round(average_auc, 4)
)


print()
print("======================================")
print("LOPO VALIDATION COMPLETED")
print("======================================")