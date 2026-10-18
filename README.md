# Agentic Financial Consequence Assurance

**A reference implementation and benchmark for verifying that autonomous financial actions remain within their authorized economic consequences.**

> Did what actually happened financially remain inside what the agent was authorized to do?

An action can be authorized and execute successfully while producing the wrong institutional state. This small deterministic reference implementation binds an authorized intent to observed execution, settlement, liquidity, reconciliation, evidence and economic consequence.

```text
AUTHORIZED ≠ EXECUTED ≠ SETTLED ≠ RECONCILED ≠ ASSURED
INTENT → AUTHORITY → EXECUTION → SETTLEMENT → LIQUIDITY → RECONCILIATION → CONSEQUENCE → ASSURANCE
```

## Run the benchmark

```bash
python -m pip install -e ".[dev]"
python -m consequence_assurance.cli benchmark
python -m consequence_assurance.cli benchmark --json
pytest
ruff check .
```

The benchmark has twelve synthetic fixtures. `PASS` means a check is supported by the supplied fixture; `FAIL` means an observed boundary violation; `ABSTAIN` means material state is unknown, stale or unreconciled. A demonstrated violation maps to `NO_GO`; unresolved required evidence maps to `ABSTAIN`.

| Scenario | Expected decision |
|---|---|
| Clean execution | GO |
| Transaction drift | NO_GO |
| Destination substitution | NO_GO |
| Settlement divergence | ABSTAIN |
| Liquidity breach | NO_GO |
| Stale evidence | ABSTAIN |
| Counterparty change | NO_GO |
| Multi-step drift | NO_GO |
| Unauthorized resource | NO_GO |
| Reconciliation mismatch | ABSTAIN |
| Valid delegated resource | GO |
| Post-execution consequence breach | NO_GO |

## Canonical demonstration

The destination-substitution fixture records valid authority and a successfully executed transaction, yet the observed destination maps to a different beneficiary. Reconciliation can agree on the observed records while the consequence still violates the mandate. The result is `NO_GO`. This demonstrates why transaction success alone does not establish an acceptable institutional outcome.

## What this is

This is a research prototype and regression benchmark. It is not production security software, legal advice, a compliance certification, or a replacement for identity, authorization, wallet, payment, settlement or assurance systems. The fixtures are synthetic; evidence freshness is evaluated against each fixture's `as_of`, not the machine clock.

## Design lineage and research

See [design lineage](docs/design-lineage.md), [research context](docs/research.md), [architecture](docs/architecture.md), [benchmark methodology](docs/benchmark-methodology.md), [interoperability](docs/interoperability.md), and [threat model](docs/threat-model.md). Relevant source projects include [agent-trust-probe](https://github.com/vishnugovind10/agent-trust-probe), [institutional-settlement-state-machine](https://github.com/vishnugovind10/institutional-settlement-state-machine), [control-probe](https://github.com/vishnugovind10/control-probe), [liquid-witness](https://github.com/vishnugovind10/liquid-witness), [liquid-proofpack](https://github.com/vishnugovind10/liquid-proofpack), [institutional-digital-asset-assurance](https://github.com/vishnugovind10/institutional-digital-asset-assurance), and [institutional-digital-collateral-stack](https://github.com/vishnugovind10/institutional-digital-collateral-stack).

## License

MIT. See [LICENSE](LICENSE).
