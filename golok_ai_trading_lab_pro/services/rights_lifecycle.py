def state(today, expiry, retention, revoked, storage):
    """Classify the locally enforceable disposition of a permission record."""
    if revoked:
        return "revoked"
    if retention and retention < today:
        return "retention_expired"
    if not expiry or expiry < today:
        return "authorization_expired"
    if storage not in ("archive", "fixed", "transient") or (storage == "fixed" and not retention):
        return "insufficient"
    if storage == "transient":
        return "transient"
    return "active"


def can_persist(status, storage):
    return status == "active" and storage in ("archive", "fixed")
