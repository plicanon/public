# Changes from v4.3 to v4.4

**Scope:** the Gate B and Gate C answers received on 2026-10-10, and a review of the PURL arrangement the steward supplied. Gate B stays open on item B1. Gate C is closed.

## Applied

| Item | Applied as |
|---|---|
| B0 approver | Recorded in the Gate A and Gate C records (name and role as declared in the steward's published catalog; the reply gave the role only). The Gate A review sheet's placeholder line was filled in. |
| B2 token | `plicanon` confirmed permanent; `token_status: confirmed_permanent` |
| B3 work ids | All 80 mnemonic ids retained as non-semantic keys, including the 16 that echo a commentary layer. `component_policy.work_ids` and spec 4.1 reworded: an id is a label, never a claim. |
| B4 tokens | Normative patterns `^v[0-9]{4,}$` and `^x[0-9]{4,}$`, enforced by the schema (version id, exemplar id, and an exemplar's parent version). Read "four-digit" as a minimum width. |
| Gate C | Closed. Result `none_known_published` in `registry.gate_c_record`; `legacy_aliases` stays empty. |
| Record | `registry.gate_b_record` holds the answers, the B1 declarations, findings, and what is missing. |

## B1 review (verified by fetching the supplied pages on 2026-10-10)

- The PURL domain `/plicanon` exists with two `302` PURLs created on 2026-10-10. `/plicanon/cts/v1` redirects to the resolver host, which returns a plain-text stub, not a CTS response.
- The catalog declares the authority URI as `https://purl.archive.org/plicanon/cts/v1`, the same record as the versioned resolver endpoint, so the authority URI and the endpoint are not separate (spec 3.1.1) and a service version sits in a permanent identifier. I proposed the domain root as an option; it does not resolve today and is recorded as a proposal, not an observation.
- The PURL help page says each domain has a single maintainer, so succession needs a documented transfer procedure; mirroring metadata is not that.
- The declared fallback endpoint returns 404 and is not independent of the PURL service. The catalog is served from a mutable branch reference.
- `namespace_authority_uri` stays null until B1 is settled.

## Not adopted

- The statement that `legacy_aliases` "will remain populated" with internal mappings returning `quarantined_ambiguous`. No legacy URN was published, so there are no records to hold; an unpublished legacy-looking query gets the standard unregistered-identifier error. Internal draft URNs can be added if listed.

## Checks

- 48 checks pass (up from 38): URL provenance (every URL in the decision record was supplied or observed, with proposals listed separately), Gate B and C state, token pattern acceptance and rejection, the approver recorded without a placeholder, and the decision record's sections.
- The resolver-binding proposal fixtures still pass (10 of 10, run separately).

## File naming

A file carries the version in which it last changed. Files unchanged since v4.3 or v4.2 (the fixtures, walkthrough, IDR template, roadmap and resolver-binding proposal) keep those names.

## Still open

- **B1:** authority URI decision, succession procedure, steward durability, an independent fallback endpoint, catalog pinning, and whether any external namespace registration is intended.
- **Gate D:** pilot scope and the official CTS parser and harness. The resolver is currently a stub.
- **Deferred past the pilot:** opaque node-set storage and stemmatic relations.
