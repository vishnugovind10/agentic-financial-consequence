"""Command line benchmark runner."""

import argparse
import json
from pathlib import Path

from .evaluator import evaluate

ROOT = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the synthetic consequence assurance benchmark.")
    parser.add_argument("command", choices=("benchmark",))
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON results.")
    args = parser.parse_args()
    results = []
    for path in sorted((ROOT / "scenarios").glob("*.json")):
        envelope = json.loads(path.read_text(encoding="utf-8"))
        result = evaluate(envelope)
        if result.final_decision.value != envelope["expected_decision"]:
            raise SystemExit(f"Benchmark regression: {path.stem} expected {envelope['expected_decision']}, got {result.final_decision}")
        results.append(result.to_dict())
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        false_assurance = sum(
            result["final_decision"] == "GO" and result["scenario"] != "clean-execution"
            and result["scenario"] != "delegated-resource"
            for result in results
        )
        if false_assurance:
            raise SystemExit(f"False assurance detected: {false_assurance}")
        print("Agentic Financial Consequence Assurance\n=======================================")
        print(f"\nScenarios: {len(results)}\n")
        for result in results:
            status = {"GO": "PASS", "NO_GO": "FAIL", "ABSTAIN": "ABSTAIN"}[result["final_decision"]]
            print(f"{status:<8} {result['scenario']}")
        print("\nFalse assurance: 0\nBenchmark status: PASS")


if __name__ == "__main__":
    main()
