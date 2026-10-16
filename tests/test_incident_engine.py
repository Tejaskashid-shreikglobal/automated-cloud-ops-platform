
import pytest

from src.incident_engine import (
    validate_incident,
    classify_severity,
)


def sample_incident():
    return {
        "incident_id": "INC-0001",
        "timestamp": "2026-10-15T10:00:00Z",
        "resource_name": "app-server-sim-01",
        "incident_type": "service_unhealthy",
        "description": "Simulated service is unhealthy",
    }


def test_valid_incident():
    assert validate_incident(sample_incident()) is True


def test_missing_required_field():
    incident = sample_incident()
    del incident["resource_name"]

    with pytest.raises(ValueError, match="Missing required fields"):
        validate_incident(incident)


def test_severity_classification():
    assert classify_severity("service_unhealthy") == "HIGH"
    assert classify_severity("config_drift") == "MEDIUM"
    assert classify_severity("temp_backlog") == "LOW"


def test_unknown_incident_type():
    with pytest.raises(ValueError, match="Unsupported incident type"):
        classify_severity("unknown_type")
