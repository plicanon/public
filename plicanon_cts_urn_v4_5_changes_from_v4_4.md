# Changes from v4.4 to v4.5

**Scope:** the six B1 answers received on 2026-10-10, checked against the live configuration. Gate B stays open; Gates A and C stay closed.

## Recorded

| Answer | Recorded as |
|---|---|
| 1. Authority URI | `https://purl.archive.org/plicanon/cts/v1` set in `namespace_authority_uri`, `namespace_authority_policy.authority_uri`, and the new `namespace_authority` record. Spec 3.1.1 gains a paragraph on this PURL-fronted URI and the accepted risk that a service version (`v1`) sits inside a permanent identifier. |
| 2. Succession | Named successor, what transfers, the immutability of minted URNs, in `namespace_authority.succession`. Status: successor's acceptance not evidenced; PURL maintainer-role transfer is a gap. |
| 3. Durability | Recorded with status "stated, partly inconsistent with observed hosting". |
| 6. External registration | None beyond the Internet Archive PURL service; the project catalog is the resolution mechanism. |

## Not accepted

- **4. Fallback endpoint.** `https://archive.org/services/purl/plicanon/cts` returned 404 on 2026-10-10 and is on the same PURL service, so it is not independent.
- **5. Catalog pinning.** The PURL `/plicanon/catalog.json` still targets `refs/heads/main`, and no tag or digest has been supplied.

## A correction to my earlier review

I said keeping the versioned PURL as the authority URI would need an amendment to the separation rule. The spec says only that the authority URI "need not be the active API endpoint", so the choice is permitted. v4.5 records it with the `v1` risk stated.

## Checks

- 52 pass (up from 48). New: the authority URI is identical in the three registry places and was supplied by the steward; B1's answered and open items are listed; the unaccepted answers stay unaccepted; a fallback cannot be marked accepted without independence and verification; catalog pinning cannot be marked implemented without a tag and a 64-character SHA-256 digest; Gate B cannot close with open B1 items. The rules are tested one at a time from a fully eligible baseline.
- The resolver-binding proposal fixtures still pass (10 of 10, run separately).

## Still open

- **Gate B (B1):** an independent fallback or a decision to rely on PURL retargeting; a tagged catalog release with its digest and the PURL retargeted; evidence the successor accepts the role; a PURL maintainer-transfer step; a durability statement that matches the hosting.
- **Gate D:** pilot scope and the official CTS parser and harness. The resolver is a stub.
- **Deferred past the pilot:** opaque node-set storage and stemmatic relations.
