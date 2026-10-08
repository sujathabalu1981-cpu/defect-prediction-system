import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.estimators import BayesianEstimator
from pgmpy.inference import VariableElimination


# ==========================================
# 1. Load prepared training data
# ==========================================

DATA_FILE = "bayesian_training_data.csv"

data = pd.read_csv(DATA_FILE)

print("======================================")
print("BAYESIAN NETWORK TRAINING")
print("======================================")

print("Total records:", len(data))


# ==========================================
# 2. Select Bayesian Network variables
# ==========================================

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


# Keep only variables required by the model

model_data = data[
    FEATURES + [TARGET]
].copy()


# ==========================================
# 3. Split training and testing data
# ==========================================

train_data, test_data = train_test_split(
    model_data,
    test_size=0.20,
    random_state=42,
    stratify=model_data[TARGET]
)


print()
print("Training records:", len(train_data))
print("Testing records:", len(test_data))


# ==========================================
# 4. Define Bayesian Network structure
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
# 5. Learn probability tables
# ==========================================

print()
print("Learning Bayesian probabilities...")

estimator = BayesianEstimator(
    model=model,
    data=train_data
)

cpds = estimator.get_parameters(
    prior_type="BDeu",
    equivalent_sample_size=10
)

model.add_cpds(*cpds)

print("Bayesian Network trained successfully.")


# ==========================================
# 6. Save trained Bayesian Network
# ==========================================

MODEL_FILE = "bayesian_model.pkl"

joblib.dump(model, MODEL_FILE)

print()
print("Bayesian Network model saved successfully.")
print("Saved model:", MODEL_FILE)


# ==========================================
# 7. Create inference engine
# ==========================================

inference = VariableElimination(model)


# ==========================================
# 8. Test one example
# ==========================================

example = {
    "LOC": "HIGH",
    "Cyclomatic": "HIGH",
    "Essential": "HIGH",
    "Design": "HIGH",
    "HalsteadVolume": "HIGH",
    "HalsteadDifficulty": "HIGH",
    "HalsteadEffort": "HIGH",
    "BranchCount": "HIGH"
}


result = inference.query(
    variables=["defects"],
    evidence=example
)


print()
print("======================================")
print("EXAMPLE DEFECT PREDICTION")
print("======================================")

print(result)

print()
print(
    "Probability of NO defect:",
    result.values[0]
)

print(
    "Probability of YES defect:",
    result.values[1]
)


print()
print("======================================")
print("TRAINING COMPLETE")
print("======================================")