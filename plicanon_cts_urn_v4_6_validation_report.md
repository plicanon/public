# PliCanon CTS-URN v4.6.2 Draft: Validation Report

**Status:** automated structural and rule checks only; not CTS certification or philological review. Produced by running `check_plicanon_v4_6.py` on the files in this bundle.

## Result

```text
PASS schema is valid Draft 2020-12
PASS registry validates against schema  [0 errors]
PASS registry invariants hold
PASS 80 works, unique ids
     citation_model_status: {'defined': 18, 'not_recorded': 62}
PASS all works blocked at v4.6
PASS gates A and C closed; gates B and D open  [{'A': 'closed', 'B': 'open', 'C': 'closed', 'D': 'open'}]
PASS authority URI is the selected PURL in the registry, the policy and the authority record
PASS parameter set to 0.05 at Gate A
PASS all 80 works aggregate_status not_assessed (blocks minting until assessed)
PASS no versions/exemplars/IDRs/legacy aliases invented
PASS envelope accepts 7 valid shapes
PASS envelope rejects 6 invalid shapes
PASS identifier examples use opaque tokens
PASS fixture parameter equals registry parameter (no drift)
PASS 23 identity fixtures produce expected outcomes
PASS negative: minting while gates open is flagged
PASS negative: schema rejects defined status with null model
PASS negative: schema rejects split IDR with one work and no relation
PASS negative: schema rejects approved IDR without reviewer/date
PASS negative: gate D closed while gate B is open is flagged
PASS negative: schema rejects witness location without index_origin
PASS 7 alignment fixtures (contraction, expansion, unmatched, conflicts)
PASS negative: approved IDR claiming yes while the parameter is null is flagged
PASS positive: consistent approved IDR passes once parameter set and model reviewed
PASS negative: stored verdict differing from recomputed verdict is flagged
PASS negative: reviewed (Tier 1) version without a Test S summary is flagged
PASS review sheet is keyed to the walkthrough (13 cases, same titles and defaults)
PASS positive: fully eligible work passes every invariant
PASS negative: aggregate_status not_assessed blocks minting
PASS negative: aggregate without an approved compilation record blocks minting
PASS positive: aggregate with an approved compilation record is eligible
PASS negative: opaque_ids citation model blocks minting (D4)
PASS negative: closed gate without decided_by is flagged
PASS negative: schema rejects a compilation record without compilation details
PASS negative: a fallback endpoint cannot be accepted without independence and verification
PASS negative: catalog pinning cannot be implemented without a tag and a SHA-256 digest
PASS negative: gate B cannot close with open B1 items
PASS decision record has one section per Gate B item and the Gate C item  [['B0', 'B1', 'B2', 'B3', 'B4', 'C1']]
PASS decision record facts about work ids match the registry  [14 + 2 layer ids, 5 overlaps]
PASS proposed URLs are labelled and never also listed as observed
PASS every URL in the decision record was supplied or observed (registry urls_seen)
PASS Gate B open on B1 only; B0, B2, B3, B4 answered
PASS B1 is open with its answered and open items listed, and the authority URI was supplied by the steward
PASS fallback accepted only as an independent static availability endpoint with its limits stated
PASS catalog pinned at digest_recorded; immutable copy still pending (not claimed as implemented)
PASS Gate C recorded as none known published; legacy_aliases empty
PASS token confirmed permanent
PASS closed gates name an approver (no placeholder)
PASS identifier examples use tokens that match the normative patterns
PASS positive: schema accepts version v0001 and exemplar x0001
PASS negative: schema rejects version tokens that break the pattern (pts1_pli_latn, v001, 0001)
PASS negative: schema rejects exemplar tokens that break the pattern, and a non-version parent
PASS bundled catalog.json matches the registry pin and declarations (digest, token, authority URI, endpoints, steward)
PASS negative: an altered catalog byte is caught by the digest
PASS negative: a catalog whose authority URI differs from the registry is caught even with a matching digest
PASS successor acceptance template covers acceptance date, transfer step, authority to issue, and avoids overreach
PASS successor acceptance not yet evidenced: registry says so, no evidence entries, and the template is not counted as evidence
PASS positive: a filled statement recorded with a matching digest passes schema, invariants and file checks
PASS negative: evidence whose file digest differs from the registry is caught
PASS negative: an evidence file with unfilled placeholders is caught
PASS negative: evidence missing the transfer section is caught
PASS negative: acceptance marked verified with no evidence is caught
PASS negative: succession status and acceptance status must agree
PASS negative: evidence outside the allowed channels, or not covering the transfer items, fails the schema
PASS negative: closing Gate B without verified successor acceptance is caught
PASS resolver hosting recorded: address, headers and steward-reported whois; address-block holder established with a basis; hosting account holder not claimed
PASS decision record names the established address-block holder
PASS decision record states the recorded resolver address
PASS negative: a provider name without an established status, or established without a name, is caught
PASS negative: an established provider name without a basis is caught
PASS negative: a resolver observation without its source fails the schema
PASS every deferred decision has a roadmap entry with entry criteria

72/72 checks passed
```

## What these checks establish

- The v4.6 schema is a valid JSON Schema (Draft 2020-12) and the registry validates against it with 0 errors.
- The bundled `catalog.json` hashes to the registry's pinned SHA-256 and agrees with the registry on token, authority URI, primary and availability endpoints and steward. An altered byte is caught, and a catalog with a different authority URI is caught even when its digest is updated to match.
- The availability endpoint is accepted only as a static endpoint that states its limits; the catalog pin sits at `digest_recorded` and is not claimed as implemented.
- Isolated tests from a fully eligible baseline cover the fallback, pin and gate-closure rules; each fails on its own specific rule.
- Every URL in the decision record was supplied by the steward or observed.
- All earlier checks still pass: token patterns, the identity decision function over 23 fixtures, 7 alignment fixtures, Test S recomputation, eligibility rules, the review sheet keyed to the walkthrough, and deferred-decision roadmap links.
- Separately, the ten resolver-binding proposal fixtures pass (`python3 check_resolver_binding_proposal_v4_3.py`).

## Important limits

- The checks verify bytes and records, not liveness. The Cloudflare Pages and GitHub observations were reported by the steward from command output on 2026-10-14.
- The catalog digest covers the file as rebuilt from pasted text (UTF-8, LF, one trailing newline). I have not seen the original file.
- The resolver address-block holder comes from whois output the steward ran and reported on 2026-10-16; I did not run it. It names the holder of the address block, not the hosting account holder.
- No immutable copy of this exact catalog exists yet; the published Zenodo record was reported to hold a different catalog and its zip was not inspected.
- The resolver is a stub, not a CTS protocol response, and the availability endpoint cannot answer CTS requests. The envelope regex is a lexical check, not the official CTS parser; Gate D is not started.
- No work can reach `approved_for_minting`: Gate B is open, no citation model is reviewed, and every work is `not_assessed` for the compilation criterion.
- I have not verified that the named successor body exists or has accepted the role.
- The schema `$id` uses `example.invalid` by design; publish at a steward-controlled URI before production use.
