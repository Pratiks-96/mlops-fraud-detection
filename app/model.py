def predict_fraud(
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    oldbalanceDest,
    newbalanceDest
):
    score = 0.0

    # Rule 1
    if oldbalanceOrg > 0:
        ratio = amount / oldbalanceOrg
        score += min(ratio, 1.0) * 0.4

    # Rule 2
    expected_orig = oldbalanceOrg - amount
    error_orig = abs(expected_orig - newbalanceOrig)
    score += min(error_orig / max(oldbalanceOrg, 1), 1.0) * 0.3

    # Rule 3
    expected_dest = oldbalanceDest + amount
    error_dest = abs(expected_dest - newbalanceDest)
    score += min(error_dest / max(amount, 1), 1.0) * 0.3

    probability = min(max(score, 0), 1)

    fraud = probability >= 0.5

    return fraud, probability
