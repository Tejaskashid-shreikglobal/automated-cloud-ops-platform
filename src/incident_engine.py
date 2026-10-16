
"""Incident validation and severity classification."""

from datetime import datetime, timezone

VALID_SEVERITIES = {"LOW", "MEDIUM", "HIGH"}

VALID_STATES = {
    "RECEIVED",
    "INVESTIGATING",
    "REMEDIATING",
    "RESOLVED",
    "FAILED",
}

SEVERITY_RULES = {
    "service_unhealthy": "HIGH",
    "config_drift": "MEDIUM",
    "temp_backlog": "LOW",
}

REQUIRED_FIELDS = {
    "incident_id",
    "timestamp",
    "resource_name",
    "incident_type",
    "description",
}


def validate_incident(incident: dict) -> bool:
    """Validate the required fields of an incident."""
    if not isinstance(incident, dict):
        raise ValueError("Incident must be a JSON object")

    missing = REQUIRED_FIELDS - incident.keys()
    if missing:
        raise ValueError(
            f"Missing required fields: {', '.join(sorted(missing))}"
        )

    for field in REQUIRED_FIELDS:
        value = incident[field]
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"Invalid field: {field}")

    try:
        datetime.fromisoformat(
            incident["timestamp"].replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError("Invalid timestamp") from exc

    return True


def classify_severity(incident_type: str) -> str:
    """Return the severity for a supported incident type."""
    if incident_type not in SEVERITY_RULES:
        raise ValueError(
            f"Unsupported incident type: {incident_type}"
        )
    return SEVERITY_RULES[incident_type]
