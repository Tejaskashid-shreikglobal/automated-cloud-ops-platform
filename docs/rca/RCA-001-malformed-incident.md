# RCA-001: Malformed Incident Payload

## Status
Simulated scenario; no live AWS incident was observed.

## Summary
An incident message is missing a required field, contains an empty value, or has an invalid timestamp.

## Detection
The `validate_incident()` function in `src/incident_engine.py` checks required fields, non-empty string values, and ISO-formatted timestamps. Invalid input raises `ValueError`.

## Root Cause
The producer supplied an incident payload that did not meet the application's validation contract.

## Impact
The invalid payload cannot be safely processed by the incident validation flow. Live SQS retry or dead-letter queue behavior has not been verified.

## Corrective Action
1. Validate incident payloads before processing.
2. Record a clear validation error without logging secrets.
3. Test missing fields, empty values, and invalid timestamps.
4. Verify queue retry and DLQ behavior separately if AWS integration is later approved.

## Prevention
Keep schema validation and negative test cases in CI.

## Evidence
Local validation code review. Attach test output after running the relevant tests.
