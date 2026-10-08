import pandas as pd

from prepare_dataset import load_dataset

from decision_engine import make_decision

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination


# ============================================================
# SOFTWARE DEFECT PREDICTION + EXPLAINABILITY + DECISION
# ============================================================


# ============================================================
# 1. LOAD NASA DATA
# ============================================================

print()
print("================================================")
print("SOFTWARE DEFECT RISK ANALYSIS")
print("================================================")

print()
print("Loading NASA dataset...")

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


# ============================================================
# 3. CALCULATE DISCRETIZATION THRESHOLDS
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
# 4. CONVERT NUMERIC VALUE
#    INTO LOW / MEDIUM / HIGH
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
# 12. PREDICT ORIGINAL DEFECT PROBABILITY
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
# 13. EXPLAINABILITY
#
# Leave-one-feature-out analysis
#
# We remove one observed metric at a time and compare
# the resulting posterior probability with the original.
# ============================================================

feature_impacts = []


for feature in FEATURES:

    reduced_evidence = evidence.copy()

    del reduced_evidence[feature]

    reduced_result = inference.query(
        variables=["defects"],
        evidence=reduced_evidence
    )

    reduced_states = (
        reduced_result.state_names["defects"]
    )

    reduced_probabilities = (
        reduced_result.values
    )

    reduced_yes_index = (
        reduced_states.index("YES")
    )

    probability_without_feature = (
        reduced_probabilities[
            reduced_yes_index
        ]
    )

    impact = (
        defect_probability
        - probability_without_feature
    )

    feature_impacts.append(
        {
            "feature": feature,
            "state": evidence[feature],
            "impact": impact
        }
    )


# ============================================================
# 14. SORT FEATURES BY ABSOLUTE IMPACT
# ============================================================

feature_impacts.sort(
    key=lambda item:
        abs(item["impact"]),
    reverse=True
)


# ============================================================
# 15. GET TOP THREE FEATURES
# ============================================================

top_features = feature_impacts[:3]


# ============================================================
# 16. SEND PROBABILITY TO DECISION ENGINE
# ============================================================

decision = make_decision(
    defect_probability
)


# ============================================================
# 17. DISPLAY INPUT METRICS
# ============================================================

print()
print("================================================")
print("INPUT METRICS")
print("================================================")

for feature in FEATURES:

    print(
        f"{feature:<22}:",
        evidence[feature]
    )


# ============================================================
# 18. DISPLAY PREDICTION
# ============================================================

print()
print("================================================")
print("PREDICTION")
print("================================================")

print(
    "Defect Probability:",
    f"{defect_probability:.4f}"
)

print(
    "Defect Probability:",
    f"{defect_probability * 100:.2f}%"
)


# ============================================================
# 19. DISPLAY EXPLAINABILITY
# ============================================================

print()
print("================================================")
print("EXPLAINABILITY")
print("================================================")

print()
print("Top Risk Factors:")
print("-----------------------------------------------")


for number, item in enumerate(
        top_features,
        start=1):

    impact = item["impact"]

    print()
    print(
        f"{number}. {item['feature']}"
    )

    print(
        "   Observed State:",
        item["state"]
    )

    print(
        "   Posterior Impact:",
        f"{impact:+.4f}"
    )


# ============================================================
# 20. DISPLAY INTERPRETATION
# ============================================================

print()
print("Interpretation:")
print("-----------------------------------------------")

positive_factors = [
    item
    for item in top_features
    if item["impact"] > 0
]


if positive_factors:

    for item in positive_factors:

        print(
            f"- {item['feature']} "
            f"in the observed {item['state']} state "
            f"is associated with increased posterior "
            f"defect risk."
        )

else:

    print(
        "No strong positive risk factors were "
        "identified by this analysis."
    )


# ============================================================
# 21. DISPLAY DECISION
# ============================================================

print()
print("================================================")
print("DECISION")
print("================================================")

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


# ============================================================
# 22. END
# ============================================================

print()
print("================================================")
print("END-TO-END ANALYSIS COMPLETE")
print("================================================")