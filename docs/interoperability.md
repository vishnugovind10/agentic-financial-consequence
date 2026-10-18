# Interoperability boundaries

The envelope is protocol-neutral. An adapter can map identity references (for example ERC-8004 or AGNTCY), governance dispositions (for example SAFR or AgencyOS), tool execution (MCP, A2A or APIs), payment references (x402 or institutional rails), settlement systems and independent evidence into the envelope.

This repository does not implement those standards, verify identity credentials, enforce payment policy, operate a wallet or settle funds. Integrations must preserve source provenance, timestamps, observer scope and uncertainty rather than translating unknown values into success.
