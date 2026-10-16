# Gate B and Gate C decision record (v4.6)

<!-- facts: works=80 layer_a=14 layer_t=2 overlap=5 -->

**Recorded:** 2026-10-14; resolver probe added 2026-10-15. **Sources:** the steward's replies and pasted command output, and the files in this bundle. Command output was reported by the steward; I did not run those commands. **Result:** Gate C is closed. Gate B stays open on B1, with two of the six answers now recorded since v4.5.

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

Bhikkhu Ido, Lead Systems Architect & Philological Data Steward, recorded in the Gate A and Gate C records. The Zenodo record's creator is now the same name.

## B1. Namespace authority URI, stewardship and succession (partly open)

### What is recorded

| # | Topic | Status |
|---|---|---|
| 1 | Authority URI `https://purl.archive.org/plicanon/cts/v1` | Accepted (permitted by spec 3.1.1; the `v1` risk is recorded) |
| 2 | Succession to the named committee; minted URNs immutable | Accepted as stated; acceptance by the successor not evidenced |
| 3 | Durability statement | Original wording not accepted; replacement wording proposed below |
| 4 | Independent fallback | **Accepted as a static availability endpoint** (below) |
| 5 | Catalog pinning | **Digest recorded**; immutable copy of this exact file still pending (below) |
| 6 | External registration | Accepted: none beyond the Internet Archive PURL service |

### The availability endpoint (accepted, with limits)

`https://public-ae3.pages.dev/catalog.json` replaces the earlier fallback, which returned 404 and sat on the same PURL service. Reported 2026-10-14: HTTP 200, `application/json`, served by Cloudflare, and its body has the same SHA-256 as the GitHub `main` copy. That makes it independent of the PURL service and byte-identical to the primary copy.

It serves the catalog only. It cannot answer CTS requests, so passages cannot be resolved while the primary resolver is down. It is therefore recorded as a static availability endpoint and catalog mirror, not as a CTS resolver fallback. If you later want a true resolver fallback, it has to answer CTS requests, which is Gate D work.

### The catalog pin (digest recorded)

- SHA-256 `7b96fd44f544565d34cbae980ed9cd2b57466c001ee8c4a3c21fbdcd6d4059f9`, for UTF-8 text with LF line endings and one trailing newline. I reproduced this digest from the pasted file.
- The exact file is in this bundle as `catalog.json`, and the checker verifies the digest, the authority URI, the token, the endpoints and the steward against the registry. A changed byte now fails the checks.
- Not yet pinned in the full sense: the PURL for the catalog still targets the mutable `main` branch. The Zenodo 4.5.1 archive was reported to hold a different catalog (SHA-256 `21502c57c038d7309555833c169e509d04c991985f71c1659ba310c120b51cc8`; I have not seen that file). An immutable copy of this exact file, a Zenodo version carrying it or a tagged release, is what turns the pin from `digest_recorded` into `implemented`.

### The published Zenodo record

Record `https://zenodo.org/records/23358712` (DOI 10.5281/zenodo.23358712), published 2026-10-14, file `public-4.5.1.zip`. I could not inspect the zip. Its title says 4.5.1, its description says 4.5, and the bundle has no 4.5.1; the repository it points to lacks files the checker needs. Recorded as an archive record, not as a pin.

### Proposed wordings (not yet accepted)

- **Durability:** "Authority metadata and releases are published in three independent places: the Internet Archive PURL service (persistent redirects), GitHub (source and catalog, mirrored on Cloudflare Pages), and Zenodo (archived releases with DOIs). The resolver is hosted separately and can be retargeted through the PURL without changing any URN."
- **Ownership transfer:** "The PURL domain maintainer role transfers to the successor through the Internet Archive PURL service, and ownership of the Zenodo record transfers to the successor or moves into a Zenodo community the successor administers. The successor records the transfer date in the registry."

### The primary resolver's host (address-block holder established)

- The resolver answers from 163.44.198.58 (Apache, PHP 8.0.9), probed 2026-10-15. The steward ran `whois 163.44.198.58` and reported the output on 2026-10-16. IANA refers the query to APNIC, which lists the block 163.44.198.0 - 163.44.198.255 as netname `ZCOM-THAI`, description GMO INTERNET PTE. LTD. (Singapore address), country TH, maintained by GMO Internet Inc (Tokyo).
- Recorded: provider name **GMO Internet Pte. Ltd.**, status `established`, on the basis of that whois record. This is the holder of the address block.
- Not established: who holds the hosting account. The resolver hostname is under `webstarterz.com`, so a reseller or hosting brand may sit between the steward and GMO. The hosting control panel or an invoice would settle it. The registry does not claim it.
- The resolver is not on the mirror's provider (Cloudflare) on the probe evidence: its address is outside the range the mirror uses and it sends no Cloudflare headers. That remains an inference.
- An earlier draft note named a different GMO entity and an AS number; neither appears in the whois output and neither is recorded.

### What still has to be true to close Gate B

1. An immutable copy of the pinned catalog (a Zenodo version carrying this exact file, or a tagged release)
2. Evidence that the named successor accepts the role
3. Acceptance of a step transferring the PURL maintainer role and the Zenodo record or account
4. Acceptance of the durability wording, or a replacement

## B2. Namespace token (done)

`plicanon` is the permanent token; identifiers read `urn:cts:plicanon:pali.<work>...`.

## B3. Work-id policy (done)

All 80 mnemonic ids retained as non-semantic keys, including the 16 that echo a commentary layer (14 are another work's id plus `a`; 2 are a base plus `mht` or `pmt`). An id is a label, never a claim.

## B4. Version and exemplar tokens (done)

Normative: versions match `^v[0-9]{4,}$`, exemplars match `^x[0-9]{4,}$`.

## C1. Legacy URN audit (done; Gate C closed)

Result: none known published. `legacy_aliases` stays empty.
