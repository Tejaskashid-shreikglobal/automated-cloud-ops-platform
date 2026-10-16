import json
import os
import boto3
from botocore.exceptions import ClientError

if __package__:
    from .incident_engine import validate_incident, classify_severity
else:
    from incident_engine import validate_incident, classify_severity

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.environ.get("AWS_REGION", "ap-south-1"),
)


def lambda_handler(event, context):
    table_name = os.environ.get("INCIDENT_TABLE")

    if not table_name:
        raise RuntimeError("INCIDENT_TABLE environment variable is missing")

    table = dynamodb.Table(table_name)
    records = event.get("Records", [])
    results = []

    for record in records:
        body = record.get("body", "{}")
        incident = json.loads(body)

        validate_incident(incident)
        severity = classify_severity(incident["incident_type"])

        item = {
            **incident,
            "severity": severity,
            "state": "RECEIVED",
        }

        try:
            table.put_item(
                Item=item,
                ConditionExpression="attribute_not_exists(incident_id)",
            )
        except ClientError as exc:
            error_code = exc.response.get("Error", {}).get("Code")

            if error_code == "ConditionalCheckFailedException":
                results.append({
                    "incident_id": incident["incident_id"],
                    "status": "DUPLICATE",
                })

                print(json.dumps({
                    "event": "duplicate_incident",
                    "incident_id": incident["incident_id"],
                }))
                continue

            raise

        results.append({
            "incident_id": incident["incident_id"],
            "status": "RECEIVED",
        })

        print(json.dumps({
            "event": "incident_received",
            "incident_id": incident["incident_id"],
            "severity": severity,
        }))

    return {
        "processed": len(results),
        "results": results,
    }