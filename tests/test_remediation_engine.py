
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
    assert "Retry limit" in result["message"]


def test_unknown_incident_is_blocked():
    engine = RemediationEngine()
    result = engine.remediate("INC-106", "unknown_type")
    assert result["status"] == "BLOCKED"
