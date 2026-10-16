from datetime import datetime

import pytest

from src.incident_store import IncidentStore
from src.incident_simulator import generate_incident


def test_all_five_states_and_timestamps():
    store = IncidentStore()
    incident = generate_incident(1)

    assert store.receive(incident) is True

    store.transition(incident["incident_id"], "INVESTIGATING")
    store.transition(incident["incident_id"], "REMEDIATING")
    store.transition(incident["incident_id"], "RESOLVED")

    record = store.get(incident["incident_id"])

    assert record["state"] == "RESOLVED"
    assert [entry["state"] for entry in record["state_history"]] == [
        "RECEIVED",
        "INVESTIGATING",
        "REMEDIATING",
        "RESOLVED",
    ]

    timestamps = [entry["timestamp"] for entry in record["state_history"]]
    assert all(datetime.fromisoformat(ts) for ts in timestamps)
    assert record["created_at"]
    assert record["updated_at"]


def test_failed_state_is_reachable():
    store = IncidentStore()
    incident = generate_incident(2)
    store.receive(incident)

    store.transition(incident["incident_id"], "INVESTIGATING")
    store.transition(incident["incident_id"], "FAILED")

    assert store.get(incident["incident_id"])["state"] == "FAILED"


def test_duplicate_incident_is_rejected():
    store = IncidentStore()
    incident = generate_incident(3)

    assert store.receive(incident) is True
    assert store.receive(incident) is False


def test_terminal_states_cannot_transition():
    store = IncidentStore()
    incident = generate_incident(4)
    store.receive(incident)
    store.transition(incident["incident_id"], "FAILED")

    with pytest.raises(ValueError, match="Transition not allowed"):
        store.transition(incident["incident_id"], "INVESTIGATING")


def test_invalid_state_is_rejected():
    store = IncidentStore()
    incident = generate_incident(5)
    store.receive(incident)

    with pytest.raises(ValueError, match="Invalid state"):
        store.transition(incident["incident_id"], "UNKNOWN")


def test_unknown_incident_is_rejected():
    store = IncidentStore()

    with pytest.raises(KeyError, match="Unknown incident"):
        store.transition("INC-NOT-FOUND", "FAILED")


def test_ten_unique_simulated_incidents():
    store = IncidentStore()
    incidents = [generate_incident(n) for n in range(1, 11)]

    results = [store.receive(incident) for incident in incidents]

    assert all(results)
    assert len({i["incident_id"] for i in incidents}) == 10
    assert all(
        store.get(i["incident_id"])["state"] == "RECEIVED"
        for i in incidents
    )
