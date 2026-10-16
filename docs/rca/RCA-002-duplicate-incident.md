# RCA-002: Duplicate Incident and Remediation

## Status
Simulated scenario; no live AWS incident was observed.

## Summary
The same incident may be delivered or submitted more than once.

## Detection
`RemediationEngine.remediate()` checks the in-memory record for an incident. If the previous status is `SUCCESS`, it returns `SKIPPED` rather than repeating the simulated successful action.

The Lambda handler also uses a DynamoDB conditional put with `attribute_not_exists(incident_id)` to reject an existing incident ID.

## Root Cause
At-least-once message delivery and repeated submissions can produce duplicate processing attempts.

## Impact
Without idempotency controls, a real remediation action could run more than once. The local remediation engine stores records in memory, so its records do not survive a process restart.

## Corrective Action
1. Retain the conditional write for incident IDs.
2. Test duplicate submissions and successful-action skipping.
3. Handle conditional-write conflicts explicitly in the Lambda flow.
4. Use durable state if remediation idempotency must survive process restarts.

## Prevention
Keep duplicate-processing tests in CI and verify DynamoDB behavior in an approved integration environment.

## Evidence
Local code review and `tests/test_remediation_engine.py`. No live DynamoDB behavior is claimed.
