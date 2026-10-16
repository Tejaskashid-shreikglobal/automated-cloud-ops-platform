
import json
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Load the locally built Lambda package.
ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "build" / "lambda"

if str(PACKAGE) not in sys.path:
    sys.path.insert(0, str(PACKAGE))

from src import lambda_handler


@pytest.fixture
def mock_table(monkeypatch):
    table = Mock()
    dynamodb = Mock()
    dynamodb.Table.return_value = table

    monkeypatch.setattr(lambda_handler, "dynamodb", dynamodb)
    monkeypatch.setenv("INCIDENT_TABLE", "test-incidents")

    return table


def make_event(incident=None):
    if incident is None:
        incident = {
            "incident_id": "INC-TEST-001",
            "timestamp": "2026-10-16T10:00:00Z",
            "resource_name": "app-server-test",
            "incident_type": "service_unhealthy",
            "description": "Simulated service health failure",
        }

    return {
        "Records": [
            {"body": json.dumps(incident)}
        ]
    }


def test_valid_incident_is_saved(mock_table):
    result = lambda_handler.lambda_handler(make_event(), None)

    assert result["processed"] == 1
    assert result["results"][0]["incident_id"] == "INC-TEST-001"
    assert result["results"][0]["status"] == "RECEIVED"

    mock_table.put_item.assert_called_once()
    saved = mock_table.put_item.call_args.kwargs

    assert saved["Item"]["incident_id"] == "INC-TEST-001"
    assert saved["Item"]["severity"] == "HIGH"
    assert saved["Item"]["state"] == "RECEIVED"
    assert (
        saved["ConditionExpression"]
        == "attribute_not_exists(incident_id)"
    )


def test_missing_table_environment_variable(monkeypatch):
    monkeypatch.delenv("INCIDENT_TABLE", raising=False)

    with pytest.raises(
        RuntimeError,
        match="INCIDENT_TABLE environment variable is missing",
    ):
        lambda_handler.lambda_handler({"Records": []}, None)


def test_invalid_json_is_rejected(mock_table):
    event = {"Records": [{"body": "{invalid-json"}]}

    with pytest.raises(json.JSONDecodeError):
        lambda_handler.lambda_handler(event, None)

    mock_table.put_item.assert_not_called()


def test_missing_incident_field_is_rejected(mock_table):
    incident = {
        "incident_id": "INC-TEST-002",
        "timestamp": "2026-10-16T10:00:00Z",
    }

    with pytest.raises((ValueError, KeyError)):
        lambda_handler.lambda_handler(make_event(incident), None)

    mock_table.put_item.assert_not_called()


def test_database_error_is_propagated(mock_table):
    mock_table.put_item.side_effect = RuntimeError("simulated database error")

    with pytest.raises(RuntimeError, match="simulated database error"):
        lambda_handler.lambda_handler(make_event(), None)
