# Changes from v4.5 to v4.6

**Scope:** the answers received on 2026-10-14 (the Cloudflare Pages endpoint, the catalog digest and the pasted catalog) and the published Zenodo record. Gate B stays open; Gates A and C stay closed.

## Recorded

| Item | Recorded as |
|---|---|
| Fallback endpoint | `https://public-ae3.pages.dev/catalog.json` accepted as a **static availability endpoint**: independent of the PURL service, byte-identical to the GitHub copy, verified 2026-10-14 from the steward's command output. It serves the catalog only and cannot answer CTS requests, so it is not a CTS resolver fallback. The earlier fallback (404, same PURL service) is recorded as replaced. |
| Catalog pin | SHA-256 `7b96fd44f544565d34cbae980ed9cd2b57466c001ee8c4a3c21fbdcd6d4059f9`, reproduced from the pasted file (UTF-8, LF, one trailing newline). Status `digest_recorded`: an immutable copy of this exact file is still pending. |
| Catalog file | `catalog.json` is now in the bundle. The checker verifies its digest, token, authority URI, endpoints and steward against the registry. |
| Zenodo record | `https://zenodo.org/records/23358712` (DOI 10.5281/zenodo.23358712, published 2026-10-14, `public-4.5.1.zip`) recorded in `namespace_authority.archive_records`. Not treated as a pin: the zip was not inspected, and the archived catalog was reported to differ (SHA-256 `21502c57…`). |
| Durability | The earlier wording stays unaccepted; replacement wording is recorded as proposed. |

## Schema and checker

- `catalog_pinning.status` now has three values: `not_implemented`, `digest_recorded`, `implemented`. `implemented` still needs a tag or an archive DOI plus the digest.
- A fallback accepted as a static availability endpoint must state its limits and that it serves no CTS requests.
- `catalog_mirrors` and `archive_records` are new required lists in the authority record.
- 56 checks pass (up from 52). New: the bundled catalog matches the registry pin and declarations; an altered catalog byte is caught; a catalog whose authority URI differs is caught even when its digest is updated to match. The resolver-binding proposal fixtures still pass (10 of 10, run separately).

## Notes

- The catalog's own `schema_version` says `v4.5`. It describes the catalog's format, which did not change in v4.6, so changing it would alter the pinned digest for no reason.
- The digest check covers the file's bytes as I rebuilt them from the pasted text. If your file differs in encoding or whitespace from that, the checker will say so; compare with `sha256sum catalog.json`.

## Still open (Gate B, B1)

- An immutable copy of the pinned catalog: a Zenodo version carrying this exact file, or a tagged release.
- Evidence that the named successor accepts the role.
- Acceptance of the ownership-transfer step (PURL maintainer and Zenodo record) and of the durability wording.
- The primary resolver's hosting provider.
- Gate D: pilot scope and the official CTS parser and harness. The resolver is a stub.
