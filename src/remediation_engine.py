
"""Safe, simulated remediation engine."""

from datetime import datetime, timezone


APPROVED_ACTIONS = {
    "service_unhealthy": "restart_service",
    "temp_backlog": "clear_temp_backlog",
    "config_drift": "restore_configuration",
}

HIGH_RISK_ACTIONS = {"restore_configuration"}


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class RemediationEngine:
    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts
        self.records = {}
        self.audit_log = []

    def remediate(
        self,
        incident_id,
        incident_type,
        approved=False,
        simulate_failure=False,
    ):
        action = APPROVED_ACTIONS.get(incident_type)

        if action is None:
            return self._record(
                incident_id, None, "BLOCKED",
                "No approved action for incident type"
            )

        if action in HIGH_RISK_ACTIONS and not approved:
            return self._record(
                incident_id, action, "AWAITING_APPROVAL",
                "Manual approval required"
            )

        previous = self.records.get(incident_id)

        if previous and previous["status"] == "SUCCESS":
            return self._record(
                incident_id, action, "SKIPPED",
                "Remediation already completed"
            )

        if previous and previous["attempts"] >= self.max_attempts:
            return self._record(
                incident_id, action, "BLOCKED",
                "Retry limit reached"
            )

        attempts = previous["attempts"] + 1 if previous else 1

        if simulate_failure:
            status = "FAILED"
            message = "Simulated remediation failure"
        else:
            status = "SUCCESS"
            message = f"Simulated action completed: {action}"

        self.records[incident_id] = {
            "action": action,
            "attempts": attempts,
            "status": status,
        }

        return self._record(
            incident_id, action, status, message
        )

    def _record(self, incident_id, action, status, message):
        entry = {
            "timestamp": utc_now(),
            "incident_id": incident_id,
            "action": action,
            "status": status,
            "message": message,
        }
        self.audit_log.append(entry)
        return entry

