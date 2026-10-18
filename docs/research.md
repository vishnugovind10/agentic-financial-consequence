# Research context

External material was checked on 18 October 2026. These sources motivate a bounded consequence-assurance layer; none validates this implementation.

| Existing approach | What it addresses | What this project does differently |
|---|---|---|
| SAFR / OpenSAFR | Runtime identity, controls, dispositions and governance records | Evaluates downstream financial state after execution |
| ERC-8004 | Agent discovery, identity, reputation and validation registries | Treats identity references as inputs, not proof of the resulting institutional consequence |
| MCP / A2A | Tool and agent interaction boundaries | Does not implement those protocols; checks resulting financial state |
| Wallet and smart-account policies | Preventive transaction constraints | Compares observed economic consequence with authorized intent |
| Settlement systems | Financial lifecycle and state transitions | Binds lifecycle evidence back to the agent mandate |
| Institutional assurance | Controls, evidence and decisions | Applies explicit assurance semantics to agent-driven outcomes |

The distinction is complementary, not competitive: governance can permit an action while the subsequent institutional outcome remains unsettled, divergent, stale or outside mandate. BIS Project Agenti's focus on agent payment behavior, intraday liquidity and system stress also makes timing and liquidity states relevant benchmark dimensions.

Sources: [OpenSAFR overview](https://opensafr.com/safr/); [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004); [BIS Project Agenti](https://www.bis.org/node/87745); [Authority-Inference Separation in Agentic Finance](https://arxiv.org/abs/2608.30519); [Governing Agentic AI in FinTech](https://arxiv.org/abs/2608.11344); [Context Is Not Authority](https://arxiv.org/abs/2608.09025).

These documents discuss different scopes and have varying maturity. This repository makes no claim that they establish an exhaustive field survey or that the benchmark has empirical institutional validity.
