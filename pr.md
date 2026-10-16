## PliCanon CTS-URN v4.6.2 draft bundle

Adds the complete v4.6.2 draft bundle (25 files). Registry `profile_version` is `4.6.2-draft`; specification text is still v4.6.

**This is a draft. It is not approval to mint public identifiers.**

### What changed since v4.6.1

- `namespace_authority.resolver_hosting` now records `provider_name` as **GMO Internet Pte. Ltd.** with status `established`. Basis: APNIC whois for 163.44.198.58 (block 163.44.198.0 - 163.44.198.255, netname `ZCOM-THAI`), run by the steward and reported 2026-10-16.
- Scope of that claim: it names the holder of the **address block**, not the hosting account. The resolver hostname is under `webstarterz.com`, so a reseller may sit between the steward and GMO. This is stated in the registry `basis` and `note` and is required by the checker.
- B1 open list: `resolver_hosting_provider_name` moved to `answered`. Four items remain open.
- Checker: 72 checks (up from 70). Two assertions tied to the old `not_established` state were rewritten and two checks were added.
- Updated: decision record, one sentence in the spec's Gate B summary, successor acceptance template, README, validation report, SHA256SUMS.
- New: `plicanon_cts_urn_v4_6_2_changes_from_v4_6_1.md` (full list of changes).

### Verification

From the bundle directory:

```bash
python3 check_plicanon_v4_6.py                      # 72/72 checks passed
python3 check_resolver_binding_proposal_v4_3.py     # 10/10 (proposal fixtures)
sha256sum -c plicanon_cts_urn_v4_6_SHA256SUMS.txt   # all OK
sha256sum catalog.json
```

Run from a clean unzip of the bundle: 72/72 and all checksums OK. The checker needs `jsonschema`.

### catalog.json is unchanged

- SHA-256 must be `7b96fd44f544565d34cbae980ed9cd2b57466c001ee8c4a3c21fbdcd6d4059f9` (UTF-8, LF line endings, one trailing newline).
- The PURL for `/plicanon/catalog.json` is served from `main`, so merging this PR changes what it serves. Please confirm the digest on `main` after merge, and that git did not alter line endings.
- Its `"schema_version": "v4.5"` is the catalog format version, not the bundle version. It is deliberately not bumped, because that would change the pinned digest. The README now says so.

### Gate status

- Gates A and C: closed. Gate D: open (resolver is a stub; the official CTS parser has not been run).
- Gate B: open on four B1 items:
  1. `catalog_immutable_copy`: a tagged release or Zenodo version carrying this exact `catalog.json`
  2. `successor_acceptance`: no statement received; the registry still records `not_evidenced`
  3. `purl_and_zenodo_ownership_transfer`
  4. `durability_statement_wording`

### Not in this PR

- No successor statement has been received or recorded.
- Recording a tag or Zenodo version as the immutable catalog copy is a registry change and belongs in a later patch.
- The Zenodo record 10.5281/zenodo.23358712 is the 4.5.1 release; the new bundle will go up as a new version after the tag exists.

### Review checklist

- [ ] Checker 72/72 and SHA256SUMS verify on the PR branch
- [ ] `catalog.json` digest matches the pin; no line-ending changes
- [ ] All 25 files present (the checker needs every file)
- [ ] After merge: tag the merge commit (e.g. `v4.6.2-draft`)
