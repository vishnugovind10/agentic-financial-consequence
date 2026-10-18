# Architecture

The evaluator accepts a JSON-compatible consequence envelope and deterministically evaluates authority, execution, settlement, liquidity, reconciliation, evidence freshness, and the resulting economic boundary. It does not authorize or execute payments. Identity, policy and execution systems provide inputs; financial systems provide observed state; the evaluator reports a bounded assurance result.

Decision precedence is conservative: any demonstrated violation yields `NO_GO`; otherwise any unresolved required check yields `ABSTAIN`; only an entirely supported and passing fixture yields `GO`. The current reference has no `CONDITIONAL_GO` path because it does not model approved exceptions.

Evidence age uses the scenario `as_of`. Missing, future-dated or stale evidence abstains. An unexplained reconciliation mismatch also abstains; explicit divergence is represented separately as a failure when observed records positively establish it.
