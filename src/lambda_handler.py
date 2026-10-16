
"""Lambda entry point for incident processing."""

import json
import os

import boto3

from incident_engine import validate_incident, classify_severity

dynamodb = boto3.resource("dynamodb")


def lambda_handler(event, context):
    table_name = os.environ.get("INCIDENT_TABLE")

    if not table_name:
        raise RuntimeError("INCIDENT_TABLE environment variable is missing")

    table = dynamodb.Table(table_name)
    results = []

    for record in event.get("Records", []):
        try:
            incident = json.loads(record["body"])
            validate_incident(incident)

            incident_id = incident["incident_id"]
            severity = classify_severity(incident["incident_type"])

            table.put_item(
                Item={
                    "incident_id": incident_id,
                    "resource_name": incident["resource_name"],
                    "incident_type": incident["incident_type"],
                    "severity": severity,
                    "state": "RECEIVED",
                    "description": incident["description"],
                    "timestamp": incident["timestamp"],
                },
                ConditionExpression="attribute_not_exists(incident_id)",
            )

            results.append({
                "incident_id": incident_id,
                "severity": severity,
                "status": "RECEIVED",
            })

        except Exception as exc:
            print(json.dumps({
                "event": "incident_processing_failed",
                "error": str(exc),
            }))
            raise

    print(json.dumps({
        "event": "incident_batch_processed",
        "count": len(results),
        "results": results,
    }))

    return {"processed": len(results), "results": results}
