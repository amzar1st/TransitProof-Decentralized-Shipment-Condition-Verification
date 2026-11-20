# Security model

## Trust and provenance

The chain authenticates transaction senders. A custody proposal cannot be overwritten and must be acknowledged by the designated next custodian. Parties are locked by the deployer; the MVP does not implement a separate pre-shipment agreement-signing round, and designation alone is not proof of consent. Checkpoint acknowledgement is explicit acceptance of the checkpoint, not proof of delivery facts. If parties reuse addresses or collude, there are no independent witnesses.

SHA-256 binds the exact image bytes to signed submissions. Photos can be staged, edited or replayed; hidden damage and cause of damage are outside the evidence. The assessment explicitly leaves authenticity and responsibility unresolved.

## AI and consensus

All narrative evidence and image text is untrusted. The prompt rejects embedded instructions, requires positive visual evidence and permits UNKNOWN. AI results must contain exactly three bounded enumerated fields. Each validator independently runs image evaluation and compares every field to the leader; validators do not merely check JSON formatting or trust a leader-supplied verdict. A disagreement rejects consensus rather than silently degrading to acceptance.

This does not eliminate shared model errors, OCR errors or manipulation. Exact categorical agreement may reduce liveness on ambiguous images. The prompt is not a cryptographic authenticity verifier. No money moves in this primitive.

## State and time

Only the deployer registers, once. Custody order and submitting roles are enforced. The second acknowledgement starts inspection. Evidence and disputes freeze when inspection ends; assessments cannot be replaced. Finalization is permissionless only after the application review delay. Missing timely receipts use a conservative timeout. A timely receipt still needs successful AI consensus; no administrator can manufacture a verdict if providers fail.

All time comparisons use transaction-pinned datetime. Proposed checkpoint and acknowledgement must occur by the locked delivery deadline. Network latency can cause a late submission to revert. Application status FINALIZED does not attest network-level protocol finality.

## Data and resource bounds

Two checkpoints, three disputes maximum, bounded notes, and bounded images. Image headers and hashes are checked, but actual decoder validity is left to the vision provider; corrupt but correctly hashed inputs can fail evaluation. There are no arbitrary URL fetches, SSRF surface, external custody services, detached signatures, secrets or upgrade keys. Raw image calldata is public; use only consented non-sensitive evidence. Unit tests mock the VM and do not prove production safety.

Report reproducible security issues privately to the repository owner before public disclosure. This repository has not undergone an independent security audit.
