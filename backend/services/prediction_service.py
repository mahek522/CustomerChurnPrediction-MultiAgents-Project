def predict_risk(customer):
    score = 0
    if customer["monthly_charges"] > 80:
        score += 1
    if customer["tenure_months"] < 12:
        score += 1
    if customer["support_tickets"] > 3:
        score += 1
    if score == 3:
        return "High"
    elif score == 2:
        return "Medium"
    return "Low"