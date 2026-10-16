
from src.remediation_engine import RemediationEngine


def test_service_restart_simulation():
    engine = RemediationEngine()
    result = engine.remediate("INC-101", "service_unhealthy")
    assert result["status"] == "SUCCESS"


def test_high_risk_requires_approval():
    engine = RemediationEngine()
    result = engine.remediate("INC-102", "config_drift")
    assert result["status"] == "AWAITING_APPROVAL"


def test_approved_configuration_restore():
    engine = RemediationEngine()
    result = engine.remediate(
        "INC-103", "config_drift", approved=True
    )
    assert result["status"] == "SUCCESS"


def test_successful_action_not_repeated():
    engine = RemediationEngine()
    engine.remediate("INC-104", "service_unhealthy")
    result = engine.remediate("INC-104", "service_unhealthy")
    assert result["status"] == "SKIPPED"


def test_failed_remediation_can_recover_and_audit_both_attempts():
    engine = RemediationEngine(max_attempts=3)
    incident_id = "INC-RECOVERY-001"
    incident_type = "service_unhealthy"

    first = engine.remediate(
        incident_id, incident_type, simulate_failure=True
    )
    second = engine.remediate(
        incident_id, incident_type, simulate_failure=False
    )

    assert first["status"] == "FAILED"
    assert second["status"] == "SUCCESS"
    assert len(engine.audit_log) == 2
    assert engine.records[incident_id]["attempts"] == 2
    assert all(entry["timestamp"] for entry in engine.audit_log)


def test_retry_limit():
    engine = RemediationEngine(max_attempts=2)
    engine.remediate("INC-105", "service_unhealthy", simulate_failure=True)
    engine.remediate("INC-105", "service_unhealthy", simulate_failure=True)
    result = engine.remediate(
        "INC-105", "service_unhealthy", simulate_failure=True
    )
    assert result["status"] == "BLOCKED"
    assert result["message"] == "Retry limit reached"


def test_unknown_incident_is_blocked():
    engine = RemediationEngine()
    result = engine.remediate("INC-106", "unknown_type")
    assert result["status"] == "BLOCKED"
    assert result["message"] == "No approved action for incident type"


def test_retry_limit():
    engine = RemediationEngine(max_attempts=2)
    engine.remediate(
        "INC-105", "service_unhealthy", simulate_failure=True
    )
    engine.remediate(
        "INC-105", "service_unhealthy", simulate_failure=True
    )
    result = engine.remediate(
        "INC-105", "service_unhealthy", simulate_failure=True
    )
    assert result["status"] == "BLOCKED"
    assert result["message"] == "Retry limit reached"


def test_unknown_incident_is_blocked():
    engine = RemediationEngine()
    result = engine.remediate("INC-106", "unknown_type")
    assert result["status"] == "BLOCKED"
    assert result["message"] == "No approved action for incident type"
