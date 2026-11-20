# Verified deployment

Verified 20 November 2026, 15:17 Asia/Colombo.

## Live contract

- Network: GenLayer Studio / Studionet (stable hosted Studio).
- Mode: Normal (Full Consensus); Simulation Mode disabled.
- Built-in Studio account: `0xd410A16A05022918E5F8FBC0f4aCBA41AD86F00C`. No external wallet was connected.
- Address: [`0x219f1297398dDA9e95020c4900d085C8C1E44c27`](https://explorer-studio.genlayer.com/address/0x219f1297398dDA9e95020c4900d085C8C1E44c27).
- Source commit: `ef76c7404f0ddeebcd5fd02f431050cfe578b89a`.
- Contract source SHA-256: `926d24fc491d792159861554ec04ef5a0663a71c1498550405dc7fa39daf68f7`.

## Live smoke test results

Completed one synthetic shipment through registration, two proposed and countersigned custody checkpoints, receipt, actual multimodal validator evaluation, and finalization. The explorer showed all nine transactions as FINALIZED, GenVM SUCCESS, consensus Accepted. The contract state read returned `FINALIZED` and verdict `ACCEPTED`, with packaging/physical/identity all PASS. Responsibility remains NOT_DETERMINED and authenticity NOT_ESTABLISHED.

**Test scope:** the same built-in account held all roles, and the same explicitly labeled synthetic illustration was submitted for dispatch and arrival. This demonstrates contract execution, image transport, integrity checks, validator evaluation and finalization. It is not validation of real photographic accuracy or independent physical custody. Separate role authorization and disagreement rejection are covered by local tests.

| Operation | Transaction |
| --- | --- |
| deploy | [`0x4ba718ccbb…`](https://explorer-studio.genlayer.com/tx/0x4ba718ccbb8e4f1a549f753a1470847338a9156428154ea009dfe7904a446f0e) |
| register | [`0x5ea87efe82…`](https://explorer-studio.genlayer.com/tx/0x5ea87efe82910a5a6375377b8ab365427c5724ce5e0d4b95285e30c9ab1945db) |
| dispatch | [`0xb496d8af48…`](https://explorer-studio.genlayer.com/tx/0xb496d8af48c68a0f566d147c983aa6850c3995b0ff05b4608d8e7d4265c68cf3) |
| dispatch_ack | [`0x5d2dc78b4e…`](https://explorer-studio.genlayer.com/tx/0x5d2dc78b4e96ed120e81b0567bbecb0045e098262fe2fcc861e69c6dc58fa319) |
| arrival | [`0xcfa29d964d…`](https://explorer-studio.genlayer.com/tx/0xcfa29d964d2be444cc2104caabbba98f24ea1de8038a9330d5bd85e6d721db1d) |
| arrival_ack | [`0xd0a9b7df31…`](https://explorer-studio.genlayer.com/tx/0xd0a9b7df31fcf802943d3b049998dbec487aa20e54557b6778e345b05ff48c5c) |
| receipt | [`0xf20b8bcbe6…`](https://explorer-studio.genlayer.com/tx/0xf20b8bcbe6883acf8f277e3f372014dea24bf23b728080a66468fd3c00b745fd) |
| verify | [`0xf3c577f2ed…`](https://explorer-studio.genlayer.com/tx/0xf3c577f2edcde1c3be024c9eb8ed73d33509251dd0b95730b02528689eb4e821) |
| finalize | [`0x014d9b5717…`](https://explorer-studio.genlayer.com/tx/0x014d9b5717527f32f1caedfdb51b5ec1757432c5b037845eff79950ae3701dd7) |

## Automated checks

- 12 local behavior tests passed with the GenLayer host mocked.
- Python compilation passed.
- [GitHub Actions run 44713546027](https://github.com/amzar1st/TransitProof-Decentralized-Shipment-Condition-Verification/actions/runs/44713546027) succeeded for the source commit above.

The live instance is consumed by the finalized demonstration. Deploy a fresh instance for another shipment; registration is intentionally one-time. Hosted Studio availability and state retention are controlled by GenLayer.

Machine-readable addresses, hashes and transaction IDs are in [`deployment.json`](../deployment.json).
