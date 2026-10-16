# PliCanon CTS-URN v4.6.2 draft: changes from v4.6.1

**Why a patch version:** the registry's resolver-hosting record changed state (`not_established` to `established`), the checker's assertions about it changed, and the B1 open list went from five items to four. The specification text, the catalog, the schema and the carried-over fixtures are unchanged. The registry's `profile_version` is `4.6.2-draft`. File names keep the `v4_6` they were last changed in, except where noted.

## Resolver hosting: address-block holder established

- The steward ran `whois 163.44.198.58` and reported the output on 2026-10-16. IANA refers to APNIC, which lists 163.44.198.0 - 163.44.198.255 as netname `ZCOM-THAI`, description GMO INTERNET PTE. LTD. (Singapore address), country TH, maintained by GMO Internet Inc (Tokyo), last modified 2023-02-09.
- `namespace_authority.resolver_hosting.provider_name` is now `GMO Internet Pte. Ltd.` with `provider_name_status` `established` and the whois record as its basis.
- **Scope of the claim:** this is the holder of the address block. The hosting account holder is not established. The resolver hostname is under `webstarterz.com`, so a reseller or hosting brand may sit between the steward and GMO. The hosting control panel or an invoice would settle it. The record's `basis` and `note` say so, and the checker requires `hosting account` to appear in the basis.
- **Correction of an earlier note:** a note pasted before the whois run named a different GMO entity and an AS number. Neither appears in the whois output, and neither is recorded.
- `gate_b_record.b1`: `resolver_hosting_provider_name` moved from `open` to `answered`, and its entry was removed from `missing`. B1 now has four open items: `catalog_immutable_copy`, `successor_acceptance`, `purl_and_zenodo_ownership_transfer`, `durability_statement_wording`. Gate B stays open.

## Checker

- The resolver-hosting check now asserts the established state, the whois source, the APNIC and `ZCOM-THAI` basis, the hosting-account caveat, and the B1 answered/open/missing lists.
- New checks: the decision record names the provider; an established provider name without a basis is caught. 72 checks, up from 70.

## Other files

- Decision record: new section on the resolver's host; item 5 removed from the Gate B closing list.
- Specification text: one sentence in the Gate B item 1 summary (recorded, no longer open). No rule changed.
- Successor acceptance template: the example registry version is `4.6.2-draft`, and the resolver row describes the address-block holder and the unknown hosting account holder.
- README: version and status line, and a note that catalog.json's `schema_version` (`v4.5`) is the catalog format version, not the bundle version. Validation report regenerated. SHA256SUMS regenerated.

## Not changed

Acceptance is still `not_evidenced`. No successor statement has been received. The catalog digest is still `7b96fd44f544565d34cbae980ed9cd2b57466c001ee8c4a3c21fbdcd6d4059f9`, and there is still no immutable copy of that exact file. The resolver is still a stub; Gate D is not started.
