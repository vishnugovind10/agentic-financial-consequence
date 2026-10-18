# Threat model

The benchmark considers amount manipulation, destination and counterparty substitution, unauthorized resources, stale authorization, stale evidence, state and settlement divergence, liquidity/exposure breach, replay, multi-step workflow drift, delegated-authority escalation, post-execution consequence drift, reconciliation failure and partial observability.

**Preventive controls** include mandate checks, transaction limits, approvals and wallet policies outside this evaluator. **Detective controls** include execution and ledger reconciliation, state observation and evidence freshness checks. **Assurance controls** bind the observed consequence to the granted authority and preserve `FAIL` versus `ABSTAIN` distinctions.

The implementation is intentionally limited: it has no cryptographic signatures, replay store, identity verification, live adapters, atomicity guarantees or adversarial production testing. Missing or stale data should abstain; a positively observed boundary violation should fail. Synthetic fixtures do not demonstrate security against a live adversary.
