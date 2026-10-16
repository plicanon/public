# Gate B and Gate C decision record (v4.5)

<!-- facts: works=80 layer_a=14 layer_t=2 overlap=5 -->

**Recorded:** 2026-10-10, from the steward's replies and from the live configuration. **Verified:** the PURL domain page and the published catalog were fetched again on 2026-10-10 before recording. Every URL below was supplied by the steward or observed. **Result:** Gate C is closed. Gate B stays open on B1: four of the six answers are recorded and two are not accepted because they do not match the live setup.

## Status

| Item | Topic | Status |
|---|---|---|
| B0 | Approver recorded in the gate records | Done |
| B1 | Authority URI, stewardship, succession, resolution, endpoints | **Partly open** (below) |
| B2 | Namespace token | Done: `plicanon` confirmed permanent |
| B3 | Work-id policy | Done: retain all 80 mnemonic ids |
| B4 | Version and exemplar token pattern | Done: normative |
| C1 | Legacy URN audit | Done: none known published; Gate C closed |

## B0. Approver (done)

Recorded in the Gate A and Gate C records: Bhikkhu Ido, Lead Systems Architect & Philological Data Steward, as declared in the steward's published catalog.

## B1. Namespace authority URI, stewardship and succession (partly open)

### The six answers

| # | Answer received | Recorded as | Notes |
|---|---|---|---|
| 1 | Keep the declared authority URI `https://purl.archive.org/plicanon/cts/v1` | **Accepted** | See below. |
| 2 | Succession to the Open Pali Text Society / Digital Humanities Archives Committee; minting authority, namespace-catalog records and resolver endpoints transfer; in-flight Gate D work shifts; minted URNs stay immutable | **Accepted as stated**, with two gaps | The successor's acceptance is not evidenced, and the PURL maintainer role is not covered. |
| 3 | Durability through open digital-humanities repository infrastructure, the Internet Archive's PURL persistence and multi-site mirroring | **Recorded, but does not match what was observed** | See below. |
| 4 | Fallback endpoint `https://archive.org/services/purl/plicanon/cts` | **Not accepted** | See below. |
| 5 | Catalog pinned by a tagged immutable GitHub release plus a SHA-256 digest in the registry | **Not implemented** | See below. |
| 6 | No external namespace registration beyond the Internet Archive PURL service and the project's own catalog | **Accepted** | The catalog is a self-declaration. |

### 1. Authority URI

Selected: `https://purl.archive.org/plicanon/cts/v1`. I fetched it on 2026-10-10: it redirects to the resolver host (the PURL page lists `302 Found`). I could not run `curl -I` from my environment, so the redirect status comes from the PURL administration page and the final URL the fetch reported.

I earlier said this choice would need an amendment to the separation rule. That overstated the text: spec 3.1.1 says only that the authority URI "need not be the active API endpoint", so the choice is permitted. The PURL name is the authority URI and its target is the endpoint, which can be retargeted without changing any URN. I added a clarifying paragraph to 3.1.1 recording the accepted risk: the name contains a service version (`v1`), so that PURL must persist indefinitely even if the API moves on (a later version would get its own PURL). The URI in the catalog and the registry must stay identical; the checker verifies the registry copies.

### 2. Succession

Recorded in `registry.namespace_authority.succession` and in appendix A.10. Two gaps:

- I have not verified that the named body exists, and nothing shows it has accepted the role.
- The PURL help page says each domain has a single maintainer. The succession text needs a step that transfers that maintainer role to the successor (the PURL service sends access problems to Internet Archive support). Proposed wording, for you to accept or change: "The PURL domain maintainer role transfers to the successor through the Internet Archive PURL service; the successor records the transfer date in the registry."

### 3. Durability

The statement says the project is hosted within open repository infrastructure backed by the PURL service and multi-site mirroring. What I observed: the PURL service stores redirects only; the resolver is on a third-party hosting subdomain; the catalog is on GitHub; I saw no mirror. The statement also points to `plicanon_gate_status_v4_4_prep_rev3.json`, which is not in the bundle or anything supplied here, so I could not check it. Either the statement should describe the hosting as it is, or the hosting should change to match it.

### 4. Fallback endpoint (not accepted)

The supplied URL leads to `purl.archive.org/plicanon/cts`, which returned 404 on 2026-10-10, and it sits on the same PURL service, so it is not independent. (A re-check from my side was refused today, so this is the earlier observation.) Options:

- [ ] Stand up a second endpoint on a different host, then record it.
- [ ] Rely on PURL retargeting as the continuity mechanism and record that there is no independent fallback (the spec does not require one).
- [ ] Other: ______

Also note that `registry.namespace_authority_policy.resolver_endpoints` is a policy sentence, not an endpoint list, so there is no endpoint entry to verify there.

### 5. Catalog pinning (not implemented)

On 2026-10-10 the PURL `/plicanon/catalog.json` still targets `refs/heads/main`, and the catalog has no tag or digest. A Git tag can be moved or deleted, so the digest is the real control. To implement it:

- Create the tag, retarget the PURL to the tagged file, and compute the digest of that file (for example `sha256sum catalog.json`). Send me the tag name and the digest.
- Then the checker will require a tag and a 64-character SHA-256 digest before pinning can be marked implemented.
- [ ] Alternatively, treat the registry as authoritative and the catalog as a derived copy, and say so.

### 6. External registration

Accepted as stated: no external namespace registration is intended. The registry records the project catalog as the resolution mechanism.

### What still has to be true to close Gate B

1. An independent fallback endpoint, or a decision to rely on PURL retargeting as the continuity mechanism
2. A tagged release for the catalog and its SHA-256 digest, with the PURL retargeted to the tag
3. Evidence that the named successor accepts the role
4. A procedure for transferring the PURL domain maintainer role
5. A durability statement that matches the observed hosting, or the hosting changes to match the statement

## B2. Namespace token (done)

`plicanon` is the permanent token; identifiers read `urn:cts:plicanon:pali.<work>...`.

## B3. Work-id policy (done)

All 80 mnemonic ids retained as non-semantic keys, including the 16 that echo a commentary layer (14 are another work's id plus `a`; 2 are a base plus `mht` or `pmt`). An id is a label, never a claim.

## B4. Version and exemplar tokens (done)

Normative: versions match `^v[0-9]{4,}$`, exemplars match `^x[0-9]{4,}$` (four digits is a minimum width).

## C1. Legacy URN audit (done; Gate C closed)

Result: none known published. v2 and v3 were internal experimental drafts. `legacy_aliases` stays empty.
