def make_decision(defect_probability):

    if defect_probability < 0.25:

        return {
            "risk_level": "LOW",
            "action": "ALLOW",
            "message": "Defect risk is low. Pipeline can continue."
        }

    elif defect_probability < 0.50:

        return {
            "risk_level": "MEDIUM",
            "action": "WARN",
            "message": "Potential defect risk detected. Warn developer and consider additional tests."
        }

    else:

        return {
            "risk_level": "HIGH",
            "action": "BLOCK",
            "message": "High defect risk detected. Pipeline should require review before merge."
        }


# Test the decision engine only when this file is run directly
if __name__ == "__main__":

    print()
    print("================================================")
    print("SOFTWARE DEFECT RISK DECISION ENGINE")
    print("================================================")

    test_probabilities = [
        0.05,
        0.18,
        0.24,
        0.25,
        0.30,
        0.49,
        0.50,
        0.72,
        0.90
    ]

    for probability in test_probabilities:

        decision = make_decision(probability)

        print()
        print("----------------------------------------")
        print("Defect Probability:", probability)
        print("Risk Level:", decision["risk_level"])
        print("Action:", decision["action"])
        print("Message:", decision["message"])

    print()
    print("================================================")
    print("DECISION ENGINE TEST COMPLETE")
    print("================================================")