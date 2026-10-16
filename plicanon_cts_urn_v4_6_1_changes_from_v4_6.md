# PliCanon CTS-URN v4.6.1 draft: changes from v4.6

**Why a patch version:** the registry schema gained a required block and the checker gained 10 rules, so a consumer that validated against v4.6 would now see a different rule set. The specification text, the Gate B and Gate C decision record, the catalog and the carried-over fixtures are unchanged. File names keep the `v4_6` they were last changed in, except where noted; the registry's `profile_version` is `4.6.1-draft`.

## Successor acceptance evidence

- New `plicanon_successor_acceptance_statement_template.md`. Compared with the first draft template, it separates the date of acceptance from the date a transfer takes effect, adds the transfer step (PURL maintainer role, Zenodo record, GitHub repository, resolver hosting), states the immutability invariant without promising that endpoints never move, does not ask the successor to endorse durability wording still recorded as unaccepted, binds the successor only to the registry version it has seen, and asks for the basis of the signer's authority. A PGP signature is optional.
- `namespace_authority.succession.acceptance` is new and required: `status` (`not_evidenced` or `verified`), `template_file`, and an `evidence` list. Each entry names the file, its SHA-256, the channel (`signed_statement_pgp`, `institutional_email`, `successor_controlled_commit`, `committee_minutes`, `other_verifiable`), the receipt date, the signer, the institution, the authority basis, and `covers_transfer_items: true`, plus an effective date or trigger.
- `succession.status` gains `acceptance_evidenced`. It must agree with `acceptance.status`, and Gate B cannot close unless acceptance is `verified`.
- The checker (70 checks, up from 56; 4 of them for the resolver observation below) verifies the template's content, that an evidence file's digest matches the registry, that it has no unfilled `{{placeholders}}`, that it names the catalog digest shown to the successor and has a transfer section, and that each rule fails when broken.
- The registry still records acceptance as `not_evidenced`. No statement has been received.

## Resolver hosting observation (2026-10-15)

- New optional `namespace_authority.resolver_hosting`, recorded from steward-reported `curl -sI` and `dig +short` output: the resolver answers HTTP 200 from 163.44.198.58 with `Server: Apache` and `X-Powered-By: PHP/8.0.9`; the Pages mirror resolves to 172.66.44.153 and 172.66.47.103.
- On that evidence the resolver is not on the mirror's provider: its address is outside Cloudflare's published ranges (as recalled, not fetched) and it sends no Cloudflare headers. This is an inference, recorded as such.
- The provider's name is **not** established: the output names software, not a company. `provider_name` is null, `provider_name_status` is `not_established`, and the B1 open item is renamed `resolver_hosting_provider_name`. A whois or ASN lookup, or the hosting account, would close it.
- The checker requires the observation's source and rejects a provider name without a basis. The decision record now states the address, and the checker confirms it matches the registry.

## Recording evidence when it arrives

1. Put the statement file in the bundle.
2. Add an entry to `succession.acceptance.evidence` with its SHA-256 and the other required fields.
3. Set `acceptance.status` to `verified` and `succession.status` to `acceptance_evidenced`.
4. Remove `successor_acceptance` from `gate_b_record.b1.open` (the checker does not do this for you) and update the decision record.
5. Regenerate `plicanon_cts_urn_v4_6_SHA256SUMS.txt`.
