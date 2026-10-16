
import json
from pathlib import Path

from src.incident_engine import validate_incident, classify_severity
from src.remediation_engine import RemediationEngine


def make_incident(incident_type="service_unhealthy"):
    return {
        "incident_id": "INC-INT-001",
        "timestamp": "2026-10-16T10:00:00Z",
        "resource_name": "app-server-test",
        "incident_type": incident_type,
        "description": "Simulated integration test incident",
    }


def test_valid_incident_flows_to_high_severity():
    incident = make_incident()

    assert validate_incident(incident) is True
    assert classify_severity(incident["incident_type"]) == "HIGH"


def test_all_supported_types_have_expected_severity():
    expected = {
        "service_unhealthy": "HIGH",
        "config_drift": "MEDIUM",
        "temp_backlog": "LOW",
    }

    for incident_type, severity in expected.items():
        incident = make_incident(incident_type)

        assert validate_incident(incident)
        assert classify_severity(incident["incident_type"]) == severity


def test_invalid_incident_stops_before_classification():
    incident = make_incident()
    del incident["resource_name"]

    try:
        validate_incident(incident)
    except ValueError as exc:
        assert "Missing required fields" in str(exc)
    else:
        raise AssertionError("Invalid incident was accepted")


def test_sample_json_file_validates():
    sample_path = (
        Path(__file__).resolve().parents[1]
        / "sample-events"
        / "incident-001.json"
    )

    incident = json.loads(sample_path.read_text(encoding="utf-8"))

    assert validate_incident(incident)
    assert classify_severity(incident["incident_type"]) in {
        "LOW", "MEDIUM", "HIGH"
    }



def test_remediation_engine_accepts_supported_incident():
    engine = RemediationEngine()
    incident = make_incident("service_unhealthy")

    result = engine.remediate(
        incident["incident_id"],
        incident["incident_type"],
    )

    assert result is not None
