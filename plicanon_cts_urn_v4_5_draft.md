# CTS-URN Profile for the Pāli Textual Corpus

**Draft:** 4.5 (authority URI selected; Gate B partly open)  
**Status:** Gates A and C closed 2026-10-10; Gate B partly answered (authority URI selected; fallback, catalog pinning and succession details open); Gate D open; not approved for public identifier minting  
**CTS namespace token:** `plicanon` (confirmed permanent 2026-10-10; its authority URI is selected: `https://purl.archive.org/plicanon/cts/v1`)  
**Companion registry:** `plicanon_registry_v4_5_draft.json` (schema `plicanon_registry_v4_5.schema.json`)  
**Change focus:** the authority URI selected (a PURL fronting the resolver), the succession successor and external-registration answers recorded, and two B1 answers not accepted because they do not match the live configuration (changes from v4.4 are in `plicanon_cts_urn_v4_5_changes_from_v4_4.md`; earlier history is in the v4.3 and v4.2 change logs)

## 0. Executive decision

This proposal treats CTS URNs as a **stable identifier and citation syntax for textgroups, works, versions, exemplars, and logical passages**, not as a complete ontology of Pāli literature. Version 4.3 applies the Gate A decisions to the testable recensional identity rules introduced in 4.2, with every minting precondition held in explicit gates, but it does not pretend that an unchosen authority URI or unreviewed work data can be made production-ready by syntax alone.

The main architectural choice is to use one stable textgroup, `pali`, as the inventory container and move changeable classifications into separate, scoped assertions. A work is not placed in a persistent identifier according to whether a particular tradition regards it as canonical, commentarial, grammatical, historical, or something else. Those claims remain queryable, may coexist, and may be attributed to a specific tradition, source, scholarly authority, or time.

The profile is deliberately conservative about textual identity. It does not assume that every work title names one perfectly stable text across all recensions. Versions may share a work record only where a shared logical citation model can be stated and the relationship to each version can be mapped. Where a reviewer finds, with evidence, that it would conceal real structural disagreement, maintainers register distinct work records connected by reviewed relations rather than invent equivalence; where the question is unresolved, the affected records are held unminted (section 2.9.3).

Minting is gated. Release gates A to D (section 9) and per-record minting states (section 2.9.7) are recorded in the registry. At v4.5 gates A and C are closed, gates B and D are open, and all 80 imported works are `blocked`.

This document is a Pāli-domain profile over CTS URN syntax and protocol. It does **not** redefine the CTS protocol.

## 1. Problem statement and goals

A persistent identifier has a limited job: continue to designate the same referent. It should not double as an evolving taxonomy, bibliographic description, page locator, or claim about religious authority.

The profile must support:

1. stable work and passage citations;
2. edition, recension, translation, script, and exemplar distinctions;
3. tradition-specific classification without making one tradition universal;
4. work relationships such as commentary-on, translation-of, quotation-of, or recension-of;
5. many-to-many and uncertain mappings between versions;
6. page-, line-, scan-, and text-span locations without confusing them with logical citations;
7. machine validation and long-term migration.

### 1.1 Non-goals

This profile does not decide the true canonical status of any text; establish authoritative Pāli titles or abbreviations; settle disputed authorship or attribution; impose one exhaustive genre taxonomy; claim that all editions are equivalent; or make printed page numbers permanent identifiers.

A record imported from the supplied v3 registry remains an **unreviewed assertion** until someone validates its content and provenance. Absence of an assertion means “not recorded,” not “false” or “not applicable.”

## 2. The data model

The registry separates these entities. They must not be collapsed into one field.

### 2.1 Work

A `Work` is a maintained referential record for a notional text-level object that can be cited under a declared logical reference model. Its identifier is a stable registry key, not a compressed title, genre, traditional location, author name, recension label, or bibliographic abbreviation. A `Work` record is a registration decision about the referent; it is not a universal verdict about literary identity or traditional canon status.

The work record carries a preferred display title, title variants, authority identifiers, a shared citation model, classification assertions, relationships, and provenance. Titles and scholarly abbreviations are labels or external identifiers; they are not the work's identity rule.

A work record does not, by itself, claim that all witnesses with a similar title have identical structure or content. If a reviewer finds, with evidence, that no defensible common reference model exists, register separate works/recensions and connect them with a reviewed relation (section 2.9.1); if the question is unresolved, hold the affected records unminted (section 2.9.3).

### 2.2 Version

A CTS `VERSION` identifies one registered textual expression of a work. Typical expressions include an edition, translation, recension as represented in a particular edition, or a digital transcription with its own editorial/transcriptional decisions. It is represented by **one atomic dot-free identifier token**. Do not create a new version merely because the same unchanged file has moved hosts or been copied; record fixed source snapshots and file digests in metadata.

The registry—not punctuation inside the URN—records structured fields such as:

- source or publishing institution;
- edition/title statement and editorial responsibility;
- language (ISO 639-3 where applicable);
- script (ISO 15924 where applicable);
- translator, editor, publication date, release, and digital source;
- the version's own citation and text segmentation details;
- identifiers of the source files and the methods used to produce the digital text.

A source organization is not automatically a version. For example, a publisher or digital repository may publish several versions. A version identifier must distinguish the particular editorial/language/script realization being registered. Do not assume that `pts`, `cscd`, `vri`, `bjt`, `thai`, `bps`, or `sc` alone identifies a unique version.

**Token semantics.** A version token carries no semantics. It must not encode source, language, script, translator, or date, because those are registry metadata that can be corrected, and a minted token is never corrected in place. The form is opaque and sequential and is normative (Gate B decision B4): version tokens match `^v[0-9]{4,}$` (for example `v0001`) and exemplar tokens match `^x[0-9]{4,}$`. Four digits is a minimum width, so numbering can grow past 9999 without a format change.

**Artifact revisions.** A frozen digital artifact is identified by digest and recorded in the version's `artifact_history`. Re-hosting an identical file changes nothing. A revised artifact gets its own history entry with a `change_class`:

- `rehost_identical`: no change to the version record.
- `transcription_correction`: errors corrected without altering the version's declared editorial and segmentation decisions. The version token is kept, the revision is recorded, and services must report which revision they served.
- `editorial_change`: changes to editorial decisions, segmentation, or the set of citable units. This is a new Version.

An artifact that becomes unavailable is marked `missing`; the version stays registered, and alignments that relied on it keep their evidence record and are flagged, not deleted.

### 2.3 Exemplar

A CTS `EXEMPLAR` identifies a particular item/copy of one registered version when item-level identity matters. Examples include a specific physical copy of a print edition, a particular manuscript codex as represented by the declared version model, or a fixed digital facsimile representing one item. An exemplar must belong to exactly one registered version.

**Edition-versus-copy test:** if the item contains independent editorial, transliteration, normalization, translation, segmentation, or transcription decisions that define a distinct textual expression, register those decisions as a separate `VERSION` (and optionally register the input scans as exemplars or source artifacts). If it is simply another copy/rendering of the same defined expression, it may be an `EXEMPLAR`. A digital file hash or URL alone does not decide this ontology; preserve it as artifact provenance either way.

### 2.4 Shared reference model

Each work has one **primary shared reference model** where such a model is defensible. It defines the logical citable nodes whose references can be used across the registered versions of that work. The word “shared” describes a project-level citation contract; it does not mean “Buddhist canonical” and does not assert that the traditions agree about textual status.

A shared reference model may be hierarchical (`16.3.1`) or may use stable opaque node identifiers for structures that do not fit a stable human-readable hierarchy. The registry must define node order, parent/child relationships, labels, and whether a node is a single unit or an aggregate. A human-readable conventional citation can be registered as an alias to a shared reference; aliases do not replace the stable reference identity.

No work may claim a shared model across versions merely because their titles match. A work's model must be reviewed for representability and mapping coverage across its declared versions.

### 2.5 Version-local address and physical location

A version-local citation, paragraph index, line, page, scan index, byte offset, or text span belongs to the version or exemplar where it is observed. It is not automatically a shared logical passage address.

Physical and transcription coordinates live in a separate `witness_locations`/alignment layer. A location can identify a page, line, token span, source-file offset, or a range crossing several pages and lines. Its coordinate system and indexing origin must be declared explicitly. Such values must not be inserted into the CTS passage component unless they are part of the registered shared logical citation scheme.

### 2.6 Classification assertions

Classification is multi-dimensional and contextual. At minimum, the data model must permit separately scoped assertions for:

- literary form or genre;
- textual role (for example, commentary, sub-commentary, grammar, chronicle, manual);
- collection or tradition membership;
- language, script, author attribution, date, and provenance;
- institutional or scholarly classification.

A classification assertion must identify its scheme, value, scope, source/authority where known, and review status. Membership in a collection must include the collection/tradition it belongs to. Do not store a universal `canonical: true/false` flag when the claim is actually tradition-specific. Do not assume a single exclusive genre. A classification may be contested, time-dependent, or unknown.

### 2.7 Work relationships

Each relationship record has a subject and target; the relationship type declares whether its semantics are directional or symmetric. Typical relation types include `comments_on`, `subcomments_on`, `translates`, `quotes`, `derived_from`, `same_work_as`, `related_to`, and `recension_of`.

A title suffix such as “on DN” is not sufficient on its own to create a verified relation. Relationship records need evidence/provenance and review status. Classification and relationship are different: “sub-commentary” is a role assertion; “sub-comments on work X” names a target.

### 2.8 Alignment

Alignment is an explicit, version-aware relation between shared logical references and version-local text spans or local references. It must allow one-to-one, one-to-many, many-to-one, partial overlap, missing material, and unresolved matches. Never force a bijection where the source material does not support one.

Every mapping should record at least its source version, target/local location, relation type, confidence or review grade, method, provenance, and review status. “No mapping known” is a valid state. It is not the same as “the passage does not exist.”

### 2.9 Work, version, and recension identity policy

Identity decisions are registry decisions made under a written test. Structural decisions (Tier 2, section 2.9.8) are recorded in an **Identity Decision Record (IDR)** that a named reviewer approves before any identifier it affects is minted. Routine decisions (Tier 1) carry a Test S summary on the version record instead and need no IDR. The IDR template is `plicanon_identity_decision_record_template.md`; the machine shape is `identityDecision` in the schema.

#### 2.9.1 Decision order

1. **Classification-only difference.** If traditions place the same registered textual object in different collections, baskets, or genres, retain one Work and record scoped classification and membership claims. Classification never creates a new Work.
2. **Evaluate Test S** (section 2.9.2). The verdict is `yes`, `no`, or `uncertain`.
3. **Verdict `yes`:** register a new Version under the same Work, record lineage, and publish mappings from shared nodes to version-local spans. Exception: section 2.9.4.
4. **Verdict `no`:** register separate Work records, each with its own citation model, linked by a **reviewed** relation (`recension_of`, `derived_from`, or `related_to`). An approved IDR is required.
5. **Verdict `uncertain`, or any required evidence missing:** HOLD (section 2.9.3). Nothing is minted for the affected records.
6. **Immutability.** A published URN keeps its referent. Mapping data may be corrected with provenance and release history; the historical referent of a minted URN may not change.

#### 2.9.2 Test S: is a shared citation model defensible?

Test S applies to a Work and the set of versions or recensions under evaluation. Its inputs are the shared model's `review_status` and, for every shared node, one evaluated or unresolved state per version.

- **Evaluated states:** `mapped`, `partial`, `unmatched`. `unmatched` means "evaluated, and this version has no corresponding unit"; it does not weaken the model.
- **Unresolved states:** `uncertain` and `not_evaluated`.

Verdicts:

- **`yes`** only if all of the following hold: the model is `reviewed`; `not_evaluated` is zero; and the unresolved fraction, `(uncertain + not_evaluated) / total nodes`, is at or below the steward-set parameter `shared_model_max_unresolved_fraction`, which Gate A set to **0.05**. A model with fewer than 20 nodes therefore tolerates no unresolved node: one `uncertain` node already exceeds 5%.
- **`no`** only if a named reviewer records a finding of structural irreconcilability with non-empty evidence explaining why shared nodes cannot be defined. Absence of mappings never produces `no`.
- **`uncertain`** in every other case, including an unreviewed model and a finding of irreconcilability that lacks evidence (missing evidence, not a `no`).

Test S does not by itself penalise a high share of `unmatched` nodes. A reviewer who judges that such a share defeats a shared model records a `no` finding with evidence.

The parameter is a governance choice, not a scholarly claim. The fixtures use the same value as the registry, and the checker verifies that they match.

#### 2.9.3 Hold rule

A held record stays in the registry with `minting_state: held_uncertain`. It has no public identifier, no reserved URN, and no entry in `GetCapabilities`. The hold covers the smallest set of identifiers whose referent is in doubt. An already-approved Work proceeds if no outcome of the held question could change its referent.

The reason is irreversibility. Two minted Works cannot later be merged or redirected; a later same-work finding can only add a `same_work_as` assertion between two permanent URNs. An unminted record can still be resolved either way. The hold list, with dates, appears in each registry release note and is resolved only by an approved IDR.

After minting, a shared model may gain nodes. It must never renumber or reassign existing nodes.

#### 2.9.4 Distinct referential scope

Even when Test S returns `yes`, separate Work records are permitted if the IDR documents that the textual objects are maintained as separate objects with materially different referential scope. An assertion of distinct scope without documentation is treated as missing evidence and leads to HOLD.

#### 2.9.5 Relation requirement

A split IDR must cite relation records whose status is `reviewed`. A relation inferred from a title suffix, or any `unreviewed` relation, cannot support a split; the case is held.

#### 2.9.6 Revised branching table

| Situation | Outcome |
|---|---|
| Only collection, tradition, or role placement differs | One Work; scoped assertions |
| Wording, spelling, segmentation, or numbering differs; Test S `yes` | New Version under the same Work. Renumbering alone never splits a Work. |
| Major reordering; Test S `yes` with mappings | New Version under the same Work (reordering is mapped, not split) |
| Test S `no` with evidence and a reviewed relation | Separate Work records plus relation |
| Test S `yes` with documented distinct referential scope | Separate Work records plus relation |
| Test S `uncertain`, unreviewed model, or relation unreviewed | HOLD; nothing minted |
| Old published passage number changes in a new edition | Keep the old shared node; map the new local structure; never reuse the old string |

#### 2.9.7 Minting states and eligibility

Each Work carries `minting_state`: `blocked`, `candidate`, `held_uncertain`, `approved_for_minting`, or `minted`. A record may enter `approved_for_minting` only if all of these hold:

1. Gates A, B, and C are closed and `namespace_authority_uri` is non-null.
2. `citation_model_status` is `defined` and the referenced model's `review_status` is `reviewed`.
3. No open `held_uncertain` decision references the record.
4. Any split decision touching the record is an approved IDR.
5. For versions and exemplars, the version record is reviewed.
6. The citation model's `node_identity_policy` is `hierarchical_ordinal`. Models with `opaque_ids` are excluded from the pilot until node-set storage is specified (D4).
7. `aggregate_status` is `not_aggregate`, or `aggregate` with an approved `compilation_recorded` record (section 2.9.8). The imported value for all 80 works is `not_assessed`, which blocks minting until the work is assessed.

`citation_model_status` distinguishes `defined`, `not_yet_defined` (reviewers determined that none exists yet), and `not_recorded` (the import carried none). v4.1 used a null for all of these.

#### 2.9.8 Decision tiers

Requiring a full IDR for every edition or exemplar would slow ordinary ingestion without adding safety, so decisions are tiered. The boundary was approved at Gate A.

- **Tier 1, routine:** classification-only differences; a new Version whose Test S verdict is `yes`; new exemplars; artifact revisions of class `rehost_identical` or `transcription_correction`; new aliases. These need schema validation and checker recomputation. A new Version carries its own `shared_model_test` summary (node-state counts and verdict), which the checker recomputes. No IDR.
- **Tier 2, structural:** a `separate_work` outcome; any hold or resolution of a hold; documented distinct referential scope; any Test S verdict other than `yes`; removing or renumbering shared nodes before minting (not permitted after). These need an approved IDR.
- **Compilation works (Tier 2):** any work comprising an intentional aggregate of independently circulating texts or canonical excerpts (for example *Khuddaka Pāṭha*) requires an approved Tier 2 record before minting. That record has outcome `compilation_recorded` and documents the compilation boundaries and the node-inheritance rule. Each work carries an `aggregate_status` (`not_assessed`, `not_aggregate`, `aggregate`). As written the criterion is broad; whether a given work meets it is a specialist assessment and is not made in this document.
- **Escalation:** a Tier 1 record whose recomputed verdict is not `yes` is Tier 2.

---

## 3. CTS URN syntax profile

### 3.1 Structure

The URN follows the CTS form:

```text
urn:cts:plicanon:TEXTGROUP.WORK[.VERSION[.EXEMPLAR]]:PASSAGE
```

The work component contains one to four dot-separated tokens: `TEXTGROUP`, `WORK`, `VERSION`, `EXEMPLAR`. CTS requires the work component and its hierarchy delimiters to be parsed in that order. The passage component may be the empty string, but the final colon is still present in the CTS URN. A non-empty passage is a node reference, node range, or permitted CTS subreference according to the adopted CTS URN specification. A non-empty passage must not be accepted on a textgroup-only identifier.

### 3.1.1 CTS namespace token, authority URI, and resolver endpoints

Three things must remain separate:

- **CTS namespace token:** the literal token following `urn:cts:`, currently proposed as `plicanon` (for example, `urn:cts:plicanon:...`). It is part of every minted identifier.
- **Namespace authority URI:** a unique, persistent URI associated with `plicanon` in the CTS namespace catalog/registry. The CTS specification requires the namespace token to resolve to a unique URI. This URI identifies the naming authority; it is not a data-file path and need not be the active API endpoint.
- **Resolver endpoint(s):** changeable service URLs that answer metadata/text requests for identifiers. They are published separately in service discovery/catalog metadata, can be replaced during hosting migrations, and must not appear as physical storage paths in URNs.

**Decision:** retain `plicanon` as the provisional CTS namespace token. Do not switch to `pli` merely because it is shorter. `urn:cts:pli:...` would use `pli` as a different CTS namespace token; it would not itself provide or register the authority URI. It also risks being read as the Pāli language code rather than as this registry's name. A future change to `pli` would require explicit governance approval and migration analysis, not a spelling-only cleanup.

**Authority URI gate:** maintainers must select a URI controlled by a durable project/institutional steward or a governed persistent-identifier service. A plausible-looking URL must not be invented; the URI recorded in this draft is the one the steward selected and supplied. The registry must record the selected URI, its stewardship, the mechanism for resolving `plicanon` to it, and the independently mutable resolver endpoints. If the URI uses HTTP(S), migration policy must preserve dereferenceability through redirects and documented succession/ownership procedures. Production minting is blocked until the URI and stewardship arrangement are adopted. The same Gate B decision must formally confirm `plicanon` as the namespace token, because the token is permanent once any URN is minted, and must decide the work-id policy (section 4.1). Both were decided on 2026-10-10. The steward selected `https://purl.archive.org/plicanon/cts/v1` (2026-10-10). It is a PURL, a governed persistent-identifier service: the PURL name is the authority URI and its redirect target is the resolver endpoint, which can be retargeted without changing any URN. This is permitted because the authority URI "need not be the active API endpoint" is a permission, not a requirement. The accepted risk is that the name contains a service version (`v1`): that PURL must persist indefinitely even if the API later moves to another version, which would get its own PURL and would not change the authority URI. The authority URI value in the catalog and in the registry must be identical.

### 3.2 Textgroup policy

The proposed v4 inventory uses a single textgroup token:

```text
pali
```

This is an organizational container only. It is deliberately not a classification for canonicality, basket, genre, or textual function. This avoids moving a work identifier when an edition or tradition classifies the same work differently.

For this reason, v4.1 does **not** adopt proposed groups such as `tipitaka`, `commentary`, or `subcommentary` as primary textgroups. They may be generated as catalog/browse views from collection membership and textual-role assertions. Creating one CTS textgroup per role would reintroduce classification-driven identifier churn.

The policy is a choice for this registry, not a claim that CTS generally requires one textgroup. New textgroups must not be introduced merely to represent a new genre or a tradition-specific inclusion claim. If a future operational need justifies another textgroup, the change must be assessed as an identifier migration, not an innocuous taxonomy refactor.

### 3.3 Token grammar and URN lexical check

Each single `TEXTGROUP`, `WORK`, `VERSION`, or `EXEMPLAR` token in this profile must match:

```regex
^[a-z][a-z0-9_]*$
```

Tokens are lowercase ASCII and cannot contain a period. The registry must verify each token in its parent context. The CTS-reserved characters `.`, `:`, `@`, `-`, `[`, and `]` must not be used as ordinary token characters. Hyphen-minus is retained for CTS passage/range syntax and is therefore not permitted inside a registered identifier token.

The following regular expression is only a **lexical envelope check**, not a complete CTS parser:

```regex
^urn:cts:plicanon:[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*){0,3}:.*$
```

This enforces the profile's namespace token, one to four dot-separated work-hierarchy tokens, and the required final colon (including the empty passage form). It does **not** verify that each token exists, that parent-child relationships are valid, or that a passage/range/subreference exists in the declared citation scheme. Implementations must run CTS syntax validation and registry/citation-model validation after the lexical check. The passage grammar must follow CTS rules; do not use the token regex as a complete URN validator.

Display titles, Pāli quotations, scripts, and source text remain Unicode. Identifier normalization must never be used to rewrite the source text itself. If Unicode labels are normalized for search or comparison, preserve the original string and make the normalization policy explicit.

### 3.4 Atomic, opaque version tokens

The profile rejects dot-delimited composite version syntax. Do not encode `SOURCE.LANGUAGE.TRANSLATOR` in the VERSION slot: the dot has CTS hierarchy meaning.

A version token is one atomic key with no semantics (section 2.2). Structured metadata lives in the registry:

```json
{
  "id": "v0001",
  "work_id": "dn",
  "source_id": "pts",
  "language": "pli",
  "script": "Latn",
  "version_type": "edition",
  "status": "illustrative_only"
}
```

This example demonstrates data shape only. The token is not mintable until a real, sufficiently identified edition record is approved. If two editions differ, they need distinct tokens even if the publisher is the same.

### 3.5 Examples

The following examples show the proposed shape; the `v0001` and `x0001` tokens are illustrative until registered.

| Meaning | URN |
|---|---|
| Textgroup | `urn:cts:plicanon:pali:` |
| Work record for Dīgha Nikāya | `urn:cts:plicanon:pali.dn:` |
| Shared logical passage reference | `urn:cts:plicanon:pali.dn:16.3` |
| Passage in a registered Pāli edition | `urn:cts:plicanon:pali.dn.v0001:16.3` |
| Passage in a particular exemplar | `urn:cts:plicanon:pali.dn.v0001.x0001:16.3` |
| A range in one citation hierarchy | `urn:cts:plicanon:pali.dn.v0001:16.3-16.5` |
| A version-specific substring/word occurrence | `urn:cts:plicanon:pali.dn.v0001:16.3@nibbāna[2]` |

The above addresses are not statements that a particular edition, exemplar, or reference has already been registered. A syntactically valid URN with an unregistered token is not a valid resolvable identifier in this registry.

### 3.6 Logical passage versus retrieval target

A work-level passage URN such as `urn:cts:plicanon:pali.dn:16.3` identifies the registered shared reference. It is not a license for a text service to silently choose an edition and present it as universal text.

Exact text retrieval must use a registered version-level URN or an explicit version-selection parameter. If the caller requests content without naming a version, a service must either ask for/require one or apply a documented selection policy and report the selected version and returned version-level URN. It must never conceal which witness supplied the content. If the requested version/exemplar is unavailable, the resolver must not silently return the nearest ancestor, adjacent passage, or default witness as if it were the requested content. It may offer an explicitly labelled fallback candidate, including its own URN, reason, and mapping/relation status, but the response must preserve the distinction between the requested target and the fallback.

### 3.7 Subreferences and ranges

CTS range syntax uses a hyphen between the start and end of a range. CTS subreferences such as `@STRING[INDEX]` are language-/version-dependent. In this profile, word occurrences, character spans, and line indices are not considered cross-version-stable merely because they can be written in a URN. They require an explicit version-level context. If a project needs a durable cross-version word alignment, register it in the alignment/annotation layer rather than treating an edition-local token index as a shared passage identity.

## 4. Registry requirements

### 4.1 Work records

Every work record must have:

- a unique, stable `id`;
- a preferred display title and any known title variants;
- a review status and provenance;
- a `citation_model_status` (`defined`, `not_yet_defined`, or `not_recorded`) and, when `defined`, a `citation_model_id`;
- a `minting_state` (section 2.9.7);
- optional scholarly abbreviations and external identifiers, treated as labels/aliases;
- zero or more scoped classification assertions;
- zero or more explicit work relationships.

**Work-id policy.** The 80 imported ids (for example `dn`) are mnemonic. They are retained as non-semantic local keys: a mnemonic is never corrected in place and asserts nothing about a title or abbreviation. Gate B decision B3 (2026-10-10) retains all 80, including the 16 that echo a commentary layer (a base id plus `a`, `mht` or `pmt`). An id is a label, never a claim: it is not evidence of classification or of a commentary relationship, and the readability benefit was weighed against the cost that a misread id is permanent.

The absence of genre, author, date, or collection membership must not be represented as evidence that the value is false. Use “unknown”, “not asserted”, and “not applicable” as different states where the distinction matters.

### 4.2 Version records

Every version record must be nested under a work by a `work_id` and have a unique atomic `id`. It must identify whether it is an edition, translation, transcription, or another explicitly defined manifestation of a work. It should include language and script where known, source/publisher, editor/translator, publication or release information, source URL or archive reference, a cryptographic digest for a frozen digital artifact where applicable, the citation model mapping, and review status.

Each version record carries a `shared_model_test` summary (section 2.9.2); the checker recomputes its verdict, so a stored verdict can never disagree with the rule.

`source_id` must point to a source/agent record, not stand in for the entire version. Translator and editor identifiers must point to named entities rather than being appended as extra dot-separated CTS components.

### 4.3 Exemplar records

Each exemplar must reference exactly one version and a documented physical or digital item identity. Page/scan indexing origins, missing scans, duplicate scans, front/body/back matter, page labels, and physical offsets belong to this level or its location manifest—not in the work identity or shared passage identifiers.

### 4.4 Citation models

A citation model must specify its grammar, levels, node identity policy, display labels, ordering, and alternatives. It must state which references are stable shared references and which are aliases belonging to one version or print convention.

Alternative printed references are not interchangeable by assumption. The model must record explicit mappings. A new or corrected edition must not silently renumber stable shared nodes. Historical printed references can remain as aliases to those nodes.

Each citation model record carries `review_status` and `node_identity_policy` (`hierarchical_ordinal`, `opaque_ids`, or `unspecified`). The 8 imported models are `imported_unreviewed` and `unspecified`. v4.3 still does not specify how the node set of an `opaque_ids` model is stored. Works that need it are excluded from the pilot (Gate A decision D4) and cannot become eligible until it is specified.

For a work with no defensible shared hierarchy, the registry may use stable opaque citable-node IDs and expose human-friendly citations as labels or mappings. It must not fabricate a false hierarchy merely to fit one edition's table of contents.

### 4.5 Classification assertions

Minimum shape:

```json
{
  "scheme_id": "tradition_membership",
  "value": "collection_or_role_id",
  "scope": {"tradition_id": "example_tradition", "work_part": null},
  "asserted_by": "source_or_authority_id",
  "evidence": [],
  "status": "unreviewed"
}
```

A claim with no named authority may be recorded as `unattributed`, but not elevated to a universal fact. Disagreement is represented by multiple scoped assertions, not by overwriting the work's identity.

### 4.6 Alignment records

Alignment data must be separate from the work title registry and support multiple spans. Each mapping needs a stable mapping ID and at least:

- the work/shared reference;
- the version (and exemplar if relevant);
- the local reference or text/physical span;
- a relationship value (`exact`, `contains`, `contained_by`, `overlaps`, `partial`, `unmatched`, or `uncertain`);
- review status, provenance, and confidence/quality information where available.

The schema must not assume that a shared passage always maps to one contiguous range in every witness. A passage may span several local lines or pages. Multiple local locations may jointly realize a shared passage, and a local passage may overlap multiple shared references.

### 4.7 Identity decision records

The registry's `identity_decisions` array holds IDRs for Tier 2 decisions. Each records subject works and versions, the question, the Test S inputs and verdict, any reviewer finding, any distinct-scope documentation, the relation records relied on, the outcome, a rationale, a named reviewer, and a status. An `approved` IDR requires a reviewer and a decision date. A `separate_work` outcome requires at least two subject works and at least one relation reference. A `compilation_recorded` outcome (Tier 2, section 2.9.8) requires a `compilation` object documenting the compilation boundaries and the node-inheritance rule, and carries no Test S summary.

### 4.8 Legacy alias records

The `legacy_aliases` array holds one record per known published legacy URN: `mapped` (with a target URN), `quarantined_ambiguous`, or `rejected`. Gate C closes only when the audit result is recorded, including a recorded result of none.

## 5. Handling disputed membership and genre

The registry does not have an absolute canon boundary field. Membership claims should be recorded against named collections or traditions. For example, if a work is included in collection A and classed differently in collection B, both assertions may be recorded without changing the work URN.

The same applies to literary form. A work may be a narrative, contain verse, function as exegesis, and be classified as a manual within a particular tradition. These are not necessarily mutually exclusive labels. The registry should not force one `genre` value to serve as both literary form and textual role.

A tradition may also define a collection hierarchy. That hierarchy belongs to the collection model and membership claims. It must not be inferred from the `TEXTGROUP` segment.

## 6. Resolver and protocol behavior

### 6.1 CTS conformance boundary

The URN syntax and CTS protocol behavior must conform to the adopted CTS URN/protocol specifications. Standard CTS operations—including `GetCapabilities`, `GetValidReff`, and `GetPassage`—must not be redefined by a custom REST routing convention. HTTP path routes or JSON endpoints may be offered as a separate Pāli registry extension, but they must be documented as extensions, not as CTS core syntax.

### 6.2 Resolution steps

A resolver should:

1. parse syntax without interpreting title, genre, language, or source by guesswork;
2. validate textgroup/work/version/exemplar tokens against the registry and parent relationships;
3. validate the passage under the work's registered shared citation model;
4. locate the requested version's mapping for that shared reference;
5. return the exact version text if a reviewed mapping is available;
6. otherwise return an explicit missing/partial/ambiguous alignment state or a suitable CTS error, never substitute an adjacent or merely similar passage silently;
7. include the resolved version, citation label, alignment status, and provenance in service metadata where the protocol permits.

### 6.3 Discovery and metadata queries

CTS `GetCapabilities` is for discoverable textgroup/work/version inventories. Rich classification filtering, tradition membership browsing, relationship traversal, and alignment queries belong in a documented registry API or linked-data representation. They must not be simulated by multiplying textgroups or by encoding genre into identifier tokens.

### 6.4 Error separation

Implementations should distinguish malformed URNs, syntactically valid but unregistered identifiers, invalid passage references, missing content, missing mappings, ambiguous mappings, and service failures. An alignment gap is not the same as an invalid URN. A title lookup with no result is not a reason to mint a new work record automatically.

## 7. Persistence and migration

### 7.1 Immutable identity rules

Once a public URN has been cited or disseminated, its referent must not be reassigned. Work IDs, version IDs, exemplar IDs, and shared citable-node IDs must never be reused for a different referent. Corrections to a title, genre, author attribution, or collection membership should usually change metadata, not the URN.

If an editorial decision genuinely splits one work record into two, preserve the old identifier as a documented legacy target and publish explicit mappings/relations. Do not transparently redirect a citation to one of the new works if the old referent is now ambiguous.

### 7.2 v2/v3 migration

The proposed v4 model maps legacy textgroups to the single v4 inventory container for **work-level URNs only after the work ID has been confirmed**. For example, a versionless old work URI can be mapped by a documented alias from `...:sutta.dn:` to `...:pali.dn:`.

Version-qualified URNs require special care. The v3 draft writes values such as `sutta.dn.pts.pli`, but standard CTS parsing reads `pts` as VERSION and `pli` as EXEMPLAR. It does not mean one composite version “PTS, Pāli”. The resolver must not automatically reinterpret it as `pts_pli_latn`. Migration requires a curated mapping based on the actual intended and published legacy semantics.

Each known published legacy URN gets a `legacy_aliases` record (section 4.8). Ambiguous forms are quarantined and resolve to an explicit ambiguity response, never to a default or nearest target.

Gate C audit (2026-10-10): the steward reports that no legacy URN was ever published, cited externally, or exposed through a public API, so no alias records are required and `legacy_aliases` stays empty.

Aliases for published identifiers must be retained indefinitely where practical, and at minimum in the authoritative registry. They must not be minted for new citations after their deprecation, but old citations must not lose their defined referent.

### 7.3 Provenance and revisioning

Registry releases must be version-controlled and reproducible. Every material claim correction should record who changed it, when, why, and what evidence was used. Digital-version records should identify immutable source snapshots by digest or archive/version key where possible. A changed transcription is a new artifact/revision; it must not silently replace evidence underlying an old alignment.

## 8. Conformance checklist

An implementation conforms to this profile only if all applicable tests pass:

### Syntax

- Every URN begins `urn:cts:plicanon:`.
- The work component has one to four dot-separated tokens in CTS order.
- A CTS identifier token contains no periods or reserved delimiters and matches the profile's lowercase token grammar.
- A version or exemplar token is registered under its parent.
- The passage is validated against the work's declared citation model.
- Ranges parse as CTS ranges and are not mistaken for characters in an identifier.

### Registry invariants

- Work IDs are unique within the namespace.
- Version IDs are unique within each work; every version points to one work.
- Exemplars point to exactly one registered version.
- A classification assertion never determines or changes a work ID.
- Canonical/collection membership is scoped to a named tradition or collection.
- Every relationship points to registered records and carries provenance/review status.
- Citation-model mappings do not point to unknown nodes.
- A missing alignment remains explicit and never becomes a made-up exact match.
- Test S returns `no` only on a reviewer finding with evidence, and `yes` only with a reviewed model and an unresolved fraction within the steward-set parameter (0.05).
- No work is `approved_for_minting` or `minted` unless its `aggregate_status` is resolved and its citation model has `hierarchical_ordinal` node identity.
- A held record is never minted, listed in `GetCapabilities`, or given a reserved URN.
- No Work is `approved_for_minting` or `minted` while any of gates A, B, C is open or the authority URI is null.
- A split IDR cites reviewed relations only.
- Every stored Test S verdict (in an approved IDR or a reviewed version record) equals the verdict recomputed from its node states, the model's review status, and the registry parameter.
- Within an alignment set: mapping ids are unique; a shared node is exact-mapped at most once per version; a `group_id` group stays within one version; an `unmatched` mapping names no local location.
- Legacy aliases do not collide with newly minted IDs or get automatically reinterpreted.
- Every known published legacy URN has a `legacy_aliases` record.

### Persistence

- Registry edits cannot reuse or reassign previously minted identifiers.
- Citation-model changes are versioned and preserve old aliases.
- Every public version has enough metadata to distinguish it from other editions/translations of the same source.
- A non-version-qualified request never hides which version supplied the returned text.
- A response reports the artifact revision served.
- Version and exemplar tokens match `^v[0-9]{4,}$` and `^x[0-9]{4,}$`.

## 9. Release gates and open decisions

Public minting requires all of gates A, B, and C closed, and gate D passed for the pilot scope. Gate state is recorded in the registry (`registry.release_gates`); at v4.5 **Gates A and C are closed** (2026-10-10), Gate B is **partly answered**, and Gate D is **open**.

**Gate A: identity and recension rules. CLOSED 2026-10-10.** Section 2.9 was approved on the basis of `plicanon_gate_a_review_sheet_v4_3_completed.md`: all 13 walkthrough cases agreed; `shared_model_max_unresolved_fraction` set to 0.05; compilation works made a Tier 2 trigger; reconstructable elision kept as `partial`; classification kept outside the identifier (single textgroup `pali`); script variation with its own editorial decisions kept as a separate Version; `standard_recension` not adopted. The approver is recorded in the registry's gate record. Two items were deferred past the pilot: node-set storage for opaque-ID models (D4) and stemmatic relations between witnesses (D5).

**Gate B: governance** (depends on A). **Partly answered 2026-10-10; item 1 is partly open.**

1. The authority URI associated with `plicanon`, with its stewardship, succession, dereferenceability, and resolver-catalog registration. **Partly answered.** Selected: authority URI `https://purl.archive.org/plicanon/cts/v1`; steward the Plicanon Text Alignment & Metadata Initiative; succession to the Open Pali Text Society / Digital Humanities Archives Committee, with previously minted URNs immutable; no external namespace registration beyond the Internet Archive PURL service. **Open:** an independent fallback endpoint (the one supplied returns 404 and is not independent of the PURL service) or a decision to rely on PURL retargeting; catalog pinning (the PURL still targets a mutable branch; no tag or digest supplied); evidence that the successor accepts the role; a procedure for transferring the PURL maintainer role (one maintainer per domain); a durability statement that matches the observed hosting. Details are in `registry.gate_b_record.b1`.
2. Formal confirmation of `plicanon` as the namespace token. `pli` stays rejected. **Done 2026-10-10.**
3. The work-id policy: retain the 80 mnemonic keys as non-semantic, or move to opaque keys before minting. **Done 2026-10-10: retained (option a).**
4. Confirmation of the opaque version/exemplar token recommendation. **Done 2026-10-10: normative.**

**Gate C: legacy audit. CLOSED 2026-10-10.** The steward reports that v2 and v3 were internal experimental drafts, never published in external catalogues, cited in peer-reviewed literature, or exposed through a public API. The recorded result is none, so no `legacy_aliases` records are required.

**Gate D: pilot and conformance** (depends on A, B, C).

1. A pilot set of works with `citation_model_status: defined`, a reviewed model with `hierarchical_ordinal` node identity, and `aggregate_status` resolved. Works needing opaque node-set storage are excluded (D4).
2. The CTS protocol release and validation harness, named explicitly, passing the positive and negative cases.
3. The controlled relationship vocabulary and review requirements.
4. Specialist review of inherited titles, abbreviations, attributions, membership claims, and passage schemes for the pilot works.

At v4.5, 18 of 80 works have a defined citation model (all `imported_unreviewed`), 62 are `not_recorded`, all 80 are `aggregate_status: not_assessed`, and none has relationships or classification assertions. With no reviewed model, Test S can only return `uncertain` for every work today. The companion registry leaves `versions`, `exemplars`, `collections`, `alignment_sets`, `witness_locations`, `identity_decisions`, and `legacy_aliases` empty until those entities are identified rather than guessed.

## Appendix A. Version 4.1, 4.2 and 4.3 decisions and rationale

### A.1 Namespace choice

Retain the CTS namespace token `plicanon` (confirmed permanent at Gate B, 2026-10-10). The suggested short form `pli` is not an authority URI; it would be a different token and therefore a namespace-level migration if adopted after publication. The authority URI and resolver endpoint registry are different records and must be governed independently. The authority URI is deliberately left unassigned rather than invented.

### A.2 Version versus exemplar

A version identifies a textual expression; an exemplar identifies a particular copy/item of that expression. An independently edited or transcribed text can be a Version even when its input artifact is a scan of another edition. A scan/file's hash and host URL are provenance and do not, by themselves, settle whether it is a Version or Exemplar.

### A.3 Recensional branching

Collection placement, literary role, and textual identity are different claims. Membership differences alone never require a new Work. Textual divergence usually creates a new Version if a shared model remains defensible. Separate Work IDs are used only when a common citation identity would be false or unsafe; the decision must have written rationale and explicit relation/provenance records. This distinction is an operational registry policy, not a claim to have settled scholarly ontology.

### A.4 Fallback resolution

A resolver must never present a nearest ancestor or default witness as though it were the requested exact passage. Fallbacks may be suggested, but only as separately identified candidates with their own URNs and a stated reason/status.

### A.5 Hold instead of provisional split (v4.2)

v4.1 rule 4 kept uncertain cases "distinct provisionally". Combined with the immutability rule, a provisional split would become permanent once minted. v4.2 holds uncertain cases unminted, because an unminted record is the only state that can still be resolved either way.

### A.6 Explicit identity test (v4.2)

v4.1 said "a defensible shared citation model" without criteria. v4.2 defines Test S with three verdicts, makes `no` depend on a reviewer finding with evidence, and treats missing evidence as `uncertain`, so lack of mappings can never push a case toward a split.

### A.7 Opaque tokens and explicit states (v4.2)

Example version tokens that embed source, language, and script would mislead if the metadata were corrected, and a minted token cannot be corrected. v4.2 recommends opaque tokens. v4.2 also replaces the null `citation_model_id` with an explicit `citation_model_status`, separating "not recorded" from "not yet defined".

### A.8 Gate A decisions (v4.3)

Recorded 2026-10-10 from the completed review sheet. D1: the unresolved-fraction parameter is 0.05. D2: compilation or anthology works are a Tier 2 trigger, made operational through `aggregate_status` and the `compilation_recorded` outcome. D3: reconstructable elision stays `partial`. D4 and D5: node-set storage for opaque-ID models and stemmatic relations are deferred past the pilot, and works that need opaque node sets are excluded from it. D6 to D8 confirmed the v4.2 positions on classification, script variation, and `standard_recension`.

### A.9 Gate B and Gate C decisions (v4.4)

Recorded 2026-10-10. B2: `plicanon` confirmed as the permanent token. B3: all 80 mnemonic work ids retained as non-semantic keys. B4: version and exemplar token patterns made normative. Gate C: audit result none, so no alias records. B1 (authority URI, steward durability, succession, resolution mechanism) remains open; the review findings are in the registry's `gate_b_record`.

### A.10 Authority URI and succession (v4.5)

Recorded 2026-10-10. The authority URI is the PURL `https://purl.archive.org/plicanon/cts/v1`, selected over the domain root. An earlier review overstated the separation rule: the spec only says the authority URI need not be the endpoint, so the choice is permitted, with the `v1` risk accepted. Two B1 answers were not accepted because they do not match what was observed: the fallback endpoint (404, not independent) and catalog pinning (the PURL still targets a mutable branch).

## Appendix B. Key decisions and rejected alternatives

### B.1 Eight taxonomy textgroups

Rejected as the primary identifier model. An eight-way group may be a useful browse view, but treating those categories as permanent URN components makes later reclassification an identifier migration and turns one taxonomic view into the identity namespace. It also does not represent overlapping roles or collection-specific membership well.

### B.2 Three Piṭakas plus one `commentarial` group

Better than mixing basket and genre on the same level, but it still assumes the first three groupings are universal identity categories and that everything outside them fits one other group. That is unsuitable as the sole identity rule for works whose placement differs among collections or scholarly descriptions.

### B.3 One primary group per literary genre

Rejected for the same reason and because genre/role can overlap. A work may be a commentary on one work, contain verse, and serve as an independent manual. No single genre needs to own its identifier.

### B.4 One `pali` work inventory plus faceted claims

Selected for this draft. It minimizes assumptions in persistent IDs. Browsing taxonomies can still be generated from assertion and collection records without changing URNs. The trade-off is a flatter `GetCapabilities` tree and a stronger need for a rich registry query API.

### B.5 Source/language/translator as multiple dot-separated VERSION subfields

Rejected because CTS dots separate work hierarchy levels. A version must be a single registered CTS token. Structured bibliographic fields belong in the registry.

### B.6 Automatic alignment based on identical numbers

Rejected. `16.3` in two editions may or may not designate the same unit. Number equality is evidence to evaluate, not proof of textual equivalence. Alignment needs source/target identity, relation type, and review status.

### B.7 Provisional public split of uncertain cases

Rejected (v4.2). See A.5.

### B.8 A fixed numeric coverage threshold in the profile

Rejected (v4.2). The tolerable unresolved fraction is a steward-set governance parameter recorded in the registry, not a number the profile asserts as scholarship.

### B.9 `standard_recension` as an identity or grouping category

Rejected (v4.3, Gate A decision D8). Lineage claims stay unreviewed metadata assertions with no identity or structural effect.

### B.10 Treating all script variation as resolver-layer

Rejected (v4.3, Gate A decision D7). Pure mechanical rendering stays at the resolver layer, but a transliteration or script realisation with its own editorial or transcription decisions is a separate Version (section 2.2).

## Appendix C. Normative references

- The Canonical Text Services URN specification: <https://github.com/cite-architecture/ctsurn_spec/blob/master/md/specification.md>
- The Canonical Text Services protocol specification: <https://github.com/cite-architecture/cts_spec/blob/master/md/specification.md>
- RFC 8141, *Uniform Resource Names (URNs)*, for general URN context: <https://www.rfc-editor.org/rfc/rfc8141>

The CTS URN specification describes the authority component as a single identifier that must resolve to a unique URI, and distinguishes the textgroup/work/version/exemplar hierarchy. RFC 8141 defines the generic URN namespace identifier separately from the namespace-specific string. This profile uses `plicanon` as the CTS namespace token and leaves the corresponding authority URI unresolved until the steward formally adopts one.

The adopted CTS URN/protocol versions must be named explicitly before implementation conformance is claimed.
