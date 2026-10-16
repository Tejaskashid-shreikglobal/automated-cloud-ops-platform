
"""Generate sample incidents for local testing."""

import json
from datetime import datetime, timezone
from pathlib import Path

INCIDENT_TYPES = [
    "service_unhealthy",
    "config_drift",
    "temp_backlog",
]

DESCRIPTIONS = {
    "service_unhealthy": "Simulated application service is unhealthy",
    "config_drift": "Simulated configuration differs from expected state",
    "temp_backlog": "Simulated temporary-file backlog detected",
}


def generate_incident(number: int) -> dict:
    incident_type = INCIDENT_TYPES[(number - 1) % len(INCIDENT_TYPES)]

    return {
        "incident_id": f"INC-{number:04d}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "resource_name": f"app-resource-sim-{number:02d}",
        "incident_type": incident_type,
        "description": DESCRIPTIONS[incident_type],
    }


def main():
    output_dir = Path("sample-events")
    output_dir.mkdir(parents=True, exist_ok=True)

    for number in range(1, 11):
        incident = generate_incident(number)
        output_file = output_dir / f"incident-{number:03d}.json"

        output_file.write_text(
            json.dumps(incident, indent=2),
            encoding="utf-8",
        )

        print(
            f"Generated {incident['incident_id']}: "
            f"{incident['incident_type']}"
        )

    print("TOTAL GENERATED: 10")


if __name__ == "__main__":
    main()
