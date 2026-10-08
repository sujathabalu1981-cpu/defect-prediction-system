from fastapi import FastAPI
from pydantic import BaseModel
import joblib

from pgmpy.inference import VariableElimination

from decision_engine import make_decision


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI(
    title="Software Defect Prediction API",
    description="API for software defect risk prediction",
    version="1.0"
)


# ==========================================
# Load trained Bayesian Network
# ==========================================

MODEL_FILE = "bayesian_model.pkl"

model = joblib.load(MODEL_FILE)

inference = VariableElimination(model)

print("Bayesian Network model loaded successfully.")


# ==========================================
# Bayesian Network Features
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


# ==========================================
# Convert Numeric Metrics to Bayesian States
# ==========================================

def discretize_metrics(request):

    evidence = {

        "LOC":
            "LOW"
            if request.LOC <= 19
            else "MEDIUM"
            if request.LOC <= 40
            else "HIGH",

        "Cyclomatic":
            "LOW"
            if request.Cyclomatic <= 3
            else "MEDIUM"
            if request.Cyclomatic <= 6
            else "HIGH",

        "Essential":
            "LOW"
            if request.Essential <= 1
            else "MEDIUM"
            if request.Essential <= 3
            else "HIGH",

        "Design":
            "LOW"
            if request.Design <= 2
            else "MEDIUM"
            if request.Design <= 4
            else "HIGH",

        "HalsteadVolume":
            "LOW"
            if request.HalsteadVolume <= 187.65
            else "MEDIUM"
            if request.HalsteadVolume <= 564.945
            else "HIGH",

        "HalsteadDifficulty":
            "LOW"
            if request.HalsteadDifficulty <= 8.33
            else "MEDIUM"
            if request.HalsteadDifficulty <= 17.27
            else "HIGH",

        "HalsteadEffort":
            "LOW"
            if request.HalsteadEffort <= 1618.61
            else "MEDIUM"
            if request.HalsteadEffort <= 9565.61
            else "HIGH",

        "BranchCount":
            "LOW"
            if request.BranchCount <= 5
            else "MEDIUM"
            if request.BranchCount <= 11
            else "HIGH"
    }

    return evidence


# ==========================================
# Prediction Request
# ==========================================

class PredictionRequest(BaseModel):

    LOC: float
    Cyclomatic: float
    Essential: float
    Design: float
    HalsteadVolume: float
    HalsteadDifficulty: float
    HalsteadEffort: float
    BranchCount: float


# ==========================================
# Home
# ==========================================

@app.get("/")
def home():

    return {
        "message":
            "Software Defect Prediction API is running"
    }


# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health():

    return {
        "status": "OK"
    }


# ==========================================
# Get Defect Probability
# ==========================================

def get_defect_probability(evidence):

    result = inference.query(
        variables=["defects"],
        evidence=evidence
    )

    states = result.state_names["defects"]

    probabilities = result.values

    yes_index = states.index("YES")

    return float(probabilities[yes_index])


# ==========================================
# Explain Prediction
# ==========================================

def generate_explanation(
        evidence,
        full_probability):

    impacts = []


    # --------------------------------------
    # Remove one feature at a time
    # --------------------------------------

    for feature in FEATURES:

        reduced_evidence = evidence.copy()

        del reduced_evidence[feature]

        probability_without_feature = \
            get_defect_probability(
                reduced_evidence
            )

        impact = (
            full_probability
            - probability_without_feature
        )

        impacts.append(
            {
                "feature":
                    feature,

                "state":
                    evidence[feature],

                "probability_without":
                    probability_without_feature,

                "impact":
                    impact
            }
        )


    # --------------------------------------
    # Sort by absolute impact
    # --------------------------------------

    impacts.sort(
        key=lambda x: abs(x["impact"]),
        reverse=True
    )


    # --------------------------------------
    # Separate positive and negative impacts
    # --------------------------------------

    risk_increasing = [

        item
        for item in impacts

        if item["impact"] > 0
    ]


    risk_reducing = [

        item
        for item in impacts

        if item["impact"] < 0
    ]


    # --------------------------------------
    # Create human-readable explanations
    # --------------------------------------

    explanations = []


    for item in risk_increasing[:3]:

        explanations.append(
            {
                "feature":
                    item["feature"],

                "state":
                    item["state"],

                "impact":
                    round(
                        item["impact"],
                        4
                    ),

                "effect":
                    "INCREASES defect risk",

                "message":
                    (
                        f"{item['feature']} = "
                        f"{item['state']} "
                        f"is associated with "
                        f"increased posterior "
                        f"defect risk."
                    )
            }
        )


    for item in risk_reducing[:3]:

        explanations.append(
            {
                "feature":
                    item["feature"],

                "state":
                    item["state"],

                "impact":
                    round(
                        item["impact"],
                        4
                    ),

                "effect":
                    "DECREASES defect risk",

                "message":
                    (
                        f"{item['feature']} = "
                        f"{item['state']} "
                        f"is associated with "
                        f"reduced posterior "
                        f"defect risk."
                    )
            }
        )


    # --------------------------------------
    # If no positive factors exist
    # --------------------------------------

    if len(risk_increasing) == 0:

        explanations.insert(
            0,
            {
                "feature":
                    None,

                "state":
                    None,

                "impact":
                    0.0,

                "effect":
                    "NO STRONG POSITIVE FACTORS",

                "message":
                    (
                        "No strong positive risk "
                        "factors were identified "
                        "by the leave-one-feature-out "
                        "analysis."
                    )
            }
        )


    return explanations


# ==========================================
# Prediction + Explainability + Decision
# ==========================================

@app.post("/predict")
def predict(request: PredictionRequest):


    # --------------------------------------
    # 1. Convert numeric metrics
    #    into LOW / MEDIUM / HIGH states
    # --------------------------------------

    evidence = discretize_metrics(request)


    # --------------------------------------
    # 2. Bayesian prediction
    # --------------------------------------

    defect_probability = \
        get_defect_probability(
            evidence
        )


    # --------------------------------------
    # 3. Explainability
    # --------------------------------------

    explanations = \
        generate_explanation(
            evidence,
            defect_probability
        )


    # --------------------------------------
    # 4. Decision Engine
    # --------------------------------------

    decision = make_decision(
        defect_probability
    )


    # --------------------------------------
    # 5. Final API response
    # --------------------------------------

    return {

        "defect_probability":
            round(
                defect_probability,
                4
            ),

        "defect_probability_percent":
            round(
                defect_probability * 100,
                2
            ),

        "risk_level":
            decision["risk_level"],

        "action":
            decision["action"],

        "message":
            decision["message"],

        "explanation":
            explanations,

        "input_metrics":
            evidence
    }