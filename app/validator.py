def validate_record(row):
    errors = []

    if row["High"] < row["Low"]:
        errors.append("High lower than Low")

    if row["Close"] <= 0:
        errors.append("Invalid close")

    if row["Volume"] < 0:
        errors.append("Negative volume")

    return errors