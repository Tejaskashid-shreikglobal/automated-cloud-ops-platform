
"""Local incident state management and audit trail."""

from datetime import datetime, timezone

VALID_STATES = {
    "RECEIVED",
    "INVESTIGATING",
    "REMEDIATING",
    "RESOLVED",
    "FAILED",
}

ALLOWED_TRANSITIONS = {
    "RECEIVED": {"INVESTIGATING", "FAILED"},
    "INVESTIGATING": {"REMEDIATING", "RESOLVED", "FAILED"},
    "REMEDIATING": {"RESOLVED", "FAILED"},
    "RESOLVED": set(),
    "FAILED": set(),
}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class IncidentStore:
    def __init__(self):
        self._incidents = {}

    def receive(self, incident: dict) -> bool:
        incident_id = incident["incident_id"]

        if incident_id in self._incidents:
            return False

        now = utc_now()
        self._incidents[incident_id] = {
            "incident": incident.copy(),
            "state": "RECEIVED",
            "created_at": now,
            "updated_at": now,
            "state_history": [
                {"state": "RECEIVED", "timestamp": now}
            ],
            "remediation_attempted": False,
        }
        return True

    def transition(self, incident_id: str, new_state: str):
        if new_state not in VALID_STATES:
            raise ValueError(f"Invalid state: {new_state}")

        record = self._incidents.get(incident_id)
        if record is None:
            raise KeyError(f"Unknown incident: {incident_id}")

        old_state = record["state"]

        if new_state not in ALLOWED_TRANSITIONS[old_state]:
            raise ValueError(
                f"Transition not allowed: {old_state} -> {new_state}"
            )

        now = utc_now()
        record["state"] = new_state
        record["updated_at"] = now
        record["state_history"].append({
            "state": new_state,
            "timestamp": now,
        })

    def get(self, incident_id: str):
        return self._incidents.get(incident_id)
