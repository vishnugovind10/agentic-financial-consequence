# Benchmark methodology

The benchmark measures lifecycle integrity across twelve fixed synthetic envelopes. Each scenario declares an expected final decision; CI compares evaluator output with that declared result and validates the envelope against the JSON Schema.

It exercises deviation detection, false-assurance prevention, abstention on stale or missing evidence, reconciliation integrity and state-sensitive authority continuity. It does not measure LLM intelligence, transaction throughput, live system integration or real-world detection rates. The priority is avoiding a false `GO`, not throughput.

Scenarios use deterministic records and a fixed `as_of`; no wall-clock reads or network calls affect outcomes. Changes to expected results require deliberate fixture review and a corresponding explanation in documentation.
