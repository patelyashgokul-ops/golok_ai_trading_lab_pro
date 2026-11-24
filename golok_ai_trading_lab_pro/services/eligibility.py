"""Observed provenance and consumption policy. Labels never grant entitlement."""

def evaluate(origin, mode, *, quarantined=False, as_of_verified=False, authorization_verified=False):
    if quarantined:
        return "QUARANTINED", False
    category = {
        "synthetic": "SYNTHETIC_FIXTURE",
        "imported": "IMPORTED_UNVERIFIED",
        "provider": "HISTORICAL_AVAILABILITY_MODELED",
    }.get(origin, "UNKNOWN")
    if origin == "provider" and as_of_verified is True and authorization_verified is True:
        category = "AUTHORIZED_HISTORICAL"
    allowed = (
        (mode == "descriptive" and category != "UNKNOWN")
        or (mode == "synthetic_replay" and category == "SYNTHETIC_FIXTURE")
        or (mode == "authorized_research" and category == "AUTHORIZED_HISTORICAL")
    )
    return category, allowed
