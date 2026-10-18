import json
from pathlib import Path

from jsonschema import Draft202012Validator

from consequence_assurance import evaluate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas/consequence-envelope.schema.json").read_text())


def test_all_scenarios_match_expected_results_and_schema():
    validator = Draft202012Validator(SCHEMA)
    paths = sorted((ROOT / "scenarios").glob("*.json"))
    assert len(paths) == 12
    for path in paths:
        envelope = json.loads(path.read_text())
        validator.validate(envelope)
        result = evaluate(envelope)
        assert result.final_decision.value == envelope["expected_decision"], path.name


def test_successful_transaction_can_fail_consequence_assurance():
    envelope = json.loads((ROOT / "scenarios/destination-substitution.json").read_text())
    result = evaluate(envelope)
    assert result.checks["authorization"].value == "PASS"
    assert result.checks["execution"].value == "PASS"
    assert result.checks["reconciliation"].value == "PASS"
    assert result.checks["consequence"].value == "FAIL"
    assert result.final_decision.value == "NO_GO"


def test_stale_evidence_abstains_without_claiming_failure():
    envelope = json.loads((ROOT / "scenarios/stale-evidence.json").read_text())
    result = evaluate(envelope)
    assert result.checks["evidence"].value == "ABSTAIN"
    assert result.final_decision.value == "ABSTAIN"


def test_authorized_is_not_assured_when_settlement_is_pending():
    envelope = json.loads((ROOT / "scenarios/settlement-divergence.json").read_text())
    result = evaluate(envelope)
    assert result.checks["authorization"].value == "PASS"
    assert result.checks["settlement"].value == "ABSTAIN"
    assert result.final_decision.value == "ABSTAIN"
