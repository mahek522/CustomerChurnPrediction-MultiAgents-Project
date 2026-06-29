def validate_response(result):

    if result["confidence"] < 70:
        return False

    if len(result["evidence"]) == 0:
        return False

    return True