# Resolver binding design (v4.3 proposal)

**Status:** proposal; not part of the approved rules. I recommend deciding it at Gate B (it affects what the registry must record) and testing it at Gate D (it is what the protocol harness exercises). Gate A's scope was identity and recension rules, so it did not cover this. No URL, host, or storage layout is proposed here; locators are data the steward supplies.

## The gap

The v4.3 spec defines how a request is parsed, validated, and mapped (section 6.2), keeps storage paths out of URNs and endpoints separate from the authority URI (section 3.1.1), and identifies frozen artifacts by digest (section 2.2). It does not define the step from a registered Version to the bytes behind it: which artifact revision is served by default, where the bytes live, what happens when a location fails or returns the wrong bytes, or what the response must say. Step 5 of section 6.2 ("return the exact version text") assumes the content is retrievable. The version record's `source_artifact` is a free-form object with no required locator or digest.

## Layers

| Layer | Identifies | Mutable? |
|---|---|---|
| URN | the Version (and passage) | never |
| Version record | its artifact revisions | revisions are added; old ones are never edited |
| Artifact revision | one frozen file, by digest | no |
| Location | where the bytes of one revision can be fetched, with a tier | yes, with a dated record |
| Endpoint | a service that answers requests | yes |

## Proposed rules

- **R1. Default revision.** An unpinned request resolves to the latest revision with status `available`. It never falls back to a `superseded` or `missing` revision. A request may pin a revision explicitly; a pinned `superseded` revision is served and reported as superseded.
- **R2. Tier order.** Try locations of that revision in the order primary, then mirror, then archive, using an optional priority within a tier.
- **R3. Same bytes only.** Moving between locations of the same revision is allowed, because the bytes are identical by digest. This is different from the forbidden silent fallback to different content (section 6.4 and the `resolver_fallback_policy`).
- **R4. Integrity.** The resolver verifies fetched bytes against the revision's digest. A mismatch is never served; the resolver tries the next location.
- **R5. Distinct failures.** If no location returns the right bytes, the response is `content_unavailable` (nothing retrievable) or `integrity_failure` (something was retrieved but failed verification). A version with no artifact is `no_artifact`. All three are separate from an invalid URN, a missing mapping, and an ambiguous mapping.
- **R6. Reporting.** Every successful response states the version, the artifact revision, its digest, and the tier served. This extends item 7 of section 6.2.
- **R7. Location changes.** A locator may change without any change to a URN or an identity decision, but each change is a dated record, and the digest remains the stable key.

## Proposed registry shape (not in the schema yet)

An `artifact_locations` collection with records of the form: `id`, `version_id`, `artifact_revision_id`, `tier` (`primary`, `mirror`, `archive`), `locator_kind`, `locator`, `status` (`active`, `retired`), `priority`, `verified_on`. Physical exemplars would carry holding metadata only; they are not routed as bytes.

## Open decisions for the steward

1. Which tiers are used in production, and who operates each.
2. Whether the default revision policy in R1 is acceptable, or whether pinning should be mandatory for some uses.
3. Whether a degraded mode may serve unverified bytes. I recommend no, but it is your call.
4. How physical exemplars are described when no digital bytes exist.
5. Where this lands: a Gate B item (alongside B1's endpoint publication), a Gate D conformance item, or both.

## Tests

`plicanon_resolver_binding_fixtures_v4_3.json` holds ten synthetic cases for R1 to R5, run by `check_resolver_binding_proposal_v4_3.py`. The fixtures use `example.invalid` locators and are not part of the main checker, because the rules are not approved.
