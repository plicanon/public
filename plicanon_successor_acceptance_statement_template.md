# Successor Acceptance Statement: `plicanon` CTS URN namespace

<!--
TEMPLATE. This file is not evidence. It becomes evidence only when a copy has every {{placeholder}} replaced,
is issued by the named successor through a channel listed in section 8, and is recorded in the registry
(namespace_authority.succession.acceptance.evidence) with its SHA-256. The checker rejects an evidence file
that still contains "{{".

Steward notes (delete this comment in the issued copy):
- Send the successor the registry version and catalog digest named below, and the transfer items in section 4.
- Do not fill the successor's fields yourself. The statement must come from the successor.
- Use the channel the successor can actually meet. A PGP signature is welcome but optional.
-->

**Registry version:** {{registry profile_version, e.g. 4.6.2-draft}}
**Namespace token:** `plicanon` (`urn:cts:plicanon:`)
**Authority URI:** `https://purl.archive.org/plicanon/cts/v1`
**Pinned catalog SHA-256:** `{{64-hex digest of the catalog.json the successor was shown}}`
**Successor named in the registry:** Open Pali Text Society / Digital Humanities Archives Committee

## 1. Statement

{{Name of the committee or institution}} ("the successor") states that it has read the registry version above and accepts the role of successor steward of the `plicanon` namespace as described in sections 2 to 5, to take effect on the trigger in section 4.

This statement records acceptance of a role. It does not approve any gate, does not approve minting of public identifiers, and does not endorse any text of the registry that the registry itself records as unaccepted.

## 2. Date of acceptance

**Date this statement was issued:** {{YYYY-MM-DD}}

(This is the date of acceptance. The date any transfer takes effect is a separate field in section 4.)

## 3. What the successor commits to

1. **Immutability.** The successor will not change or reassign the meaning of any URN minted under `urn:cts:plicanon:`, and will not point a minted URN at a different text. This is the registry's invariant ("previously minted URNs remain immutable").
2. **Resolution endpoints may move.** The successor may retarget the resolver endpoint behind the authority URI through the PURL service, provided minted URNs keep their meaning. The successor is not promising that any particular host stays in use.
3. **Authority metadata.** The successor will maintain, or arrange for the maintenance of, the authority catalog and registry records that it takes over under section 4.
4. **Rules in force.** The successor accepts the version, exemplar and work-identifier rules of the registry version named above. Changes after the transfer takes effect are decided by the successor under its own process; the successor is not bound by registry versions it has not seen.
5. **In-flight work.** The successor acknowledges that Gate D conformance work (pilot scope and the official CTS parser run) passes to it at the trigger below, as the registry records.

## 4. Transfer

**Trigger for succession:** {{event or date, e.g. steward's written notice, incapacity, or a stated date}}
**Date the transfer takes effect:** {{YYYY-MM-DD, or "on trigger"}}

The successor agrees the following items. For each, state the method and who acts.

| Item | Method agreed | Acts on it |
|---|---|---|
| PURL domain `plicanon`: maintainer role (the PURL service allows one maintainer per domain) | {{method}} | {{steward / successor}} |
| Zenodo record 10.5281/zenodo.23358712 and later versions: ownership transfer, or move into a Zenodo community the successor administers | {{method}} | {{steward / successor}} |
| GitHub repository `plicanon/public`: ownership or admin rights | {{method}} | {{steward / successor}} |
| Primary resolver: hosting account and domain registration | {{method; the resolver answers from 163.44.198.58, an address block held by GMO Internet Pte. Ltd.; the hosting account holder is not yet known}} | {{steward / successor}} |
| Registry record of the transfer date | The successor records the date in the registry | successor |

## 5. Durability

The successor has been shown the registry's durability statement and its recorded status. This statement does not endorse that wording; wording still recorded as proposed or unaccepted remains so until the steward and successor accept it separately.

## 6. What this statement does not do

It does not transfer anything before the date in section 4, and it does not bind any person or body other than the successor named above.

## 7. Authority to issue

I confirm that I am authorized to accept this role for the successor, on the basis of: {{resolution, minutes, bylaws clause, or written delegation, with its date and reference}}

## 8. Sign-off and channel

- **Name of authorized representative:** {{name}}
- **Title or role:** {{title}}
- **Institution or committee:** {{name}}
- **Contact email (institutional address):** {{email}}
- **Channel by which this copy reached the steward** (one of: `signed_statement_pgp`, `institutional_email`, `successor_controlled_commit`, `committee_minutes`, `other_verifiable`): {{channel}}
- **PGP fingerprint (optional, recommended):** {{fingerprint or "none"}}
- **Signature or equivalent:** {{signature}}
