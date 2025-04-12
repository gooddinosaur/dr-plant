def predict_health(moisture, light, temperature, humidity):
    if moisture < 30:
        return "Needs Water"
    elif temperature > 40:
        return "Too Hot"
    elif humidity < 30:
        return "Too Dry"
    elif light < 200:
        return "Needs More Sunlight"
    return "Healthy"
