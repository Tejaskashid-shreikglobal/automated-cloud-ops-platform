
from src.incident_store import IncidentStore


def test_resolved_incident_cannot_reenter_remediation():
    store = IncidentStore()
    store.receive({"incident_id": "INC-0003"})

    store.transition("INC-0003", "INVESTIGATING")
    store.transition("INC-0003", "RESOLVED")

    try:
        store.transition("INC-0003", "REMEDIATING")
    except ValueError as error:
        print("BLOCKED:", error)
    else:
        raise AssertionError(
            "Unsafe transition was not blocked"
        )


if __name__ == "__main__":
    test_resolved_incident_cannot_reenter_remediation()
    print("TEST PASSED")
