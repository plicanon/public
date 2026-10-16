# Gate A review sheet (completed), v4.3

**Completed by:** the steward, 2026-10-10: Bhikkhu Ido, Lead Systems Architect & Philological Data Steward (name and role as declared in the steward's published catalog; recorded in v4.4). **Applied in:** `plicanon_cts_urn_v4_3_draft.md`; recorded in `registry.gate_a_record`. **Keyed to:** `plicanon_identity_case_walkthrough_v4_3.md` (case titles and defaults below are generated from it, and `check_plicanon_v4_3.py` verifies they match).

## Part 1: the 13 cases

### Case 1: Text in one tradition's collection, classed differently in another

- **Governing rule:** 2.9.1 step 1
- **v4.2 default:** One Work. Two scoped membership claims in `collections`.
- **Representable in v4.3:** Yes
- **Verdict:** [x] Agree
- **Notes / revision:** Keeps one Work and manages collection variations via `collections` scope metadata without changing the canonical URN.

### Case 2: Work with more than one functional role

- **Governing rule:** 2.9.1 step 1
- **v4.2 default:** One Work. Multiple `textual_role` assertions (the scheme is multi-valued).
- **Representable in v4.3:** Yes
- **Verdict:** [x] Agree
- **Notes / revision:** Keeps one Work with multiple `textual_role` assertions.

### Case 3: Commentary whose target work needs a verified relation

- **Governing rule:** 2.9.5
- **v4.2 default:** A `comments_on` relation stays `unreviewed` until evidence exists. An unreviewed relation cannot support a split; a title suffix is not evidence.
- **Representable in v4.3:** Yes. Relation `status` is now a closed vocabulary.
- **Verdict:** [x] Agree
- **Notes / revision:** `comments_on` stays `unreviewed` until evidence exists. Unreviewed relations cannot support a split.

### Case 4: Verse collection with edition-specific numbering

- **Governing rule:** 2.9.2 (Test S)
- **v4.2 default:** Renumbering alone never splits a Work (2.9.6). If the model is reviewed and nodes are evaluated, the verdict is `yes`: new Version with mappings, and printed numbering kept as aliases. Even major reordering is a new Version when shared nodes can be evaluated and mapped.
- **Representable in v4.3:** Yes, but every imported model is `imported_unreviewed`, so the verdict is `uncertain` today.
- **Verdict:** [x] Agree
- **Notes / revision:** Renumbering alone never splits a Work (added explicitly to section 2.9.6). In accordance with Test S, even major reordering is treated as a new Version when shared nodes can be evaluated and mapped.

### Case 5: Passage split over multiple lines or pages

- **Governing rule:** 2.5
- **v4.2 default:** A `witness_locations` record with several spans. It never enters the CTS passage component.
- **Representable in v4.3:** Yes. `index_origin` is now required. Span structure inside `coordinate` is still free-form and not validated.
- **Verdict:** [x] Agree
- **Notes / revision:** Physical layout locators belong in `witness_locations` and never enter the CTS passage coordinate.

### Case 6: Edition lacking a canonical unit

- **Governing rule:** 2.9.2
- **v4.2 default:** The mapping state is `unmatched`, which counts as evaluated. It does not weaken the shared model and is not "does not exist".
- **Representable in v4.3:** Yes
- **Verdict:** [x] Agree
- **Notes / revision:** Unmatched mapping status is treated as evaluated without weakening the underlying shared model.

### Case 7: Two local segments mapping to one shared passage

- **Governing rule:** 2.8
- **v4.2 default:** Two mappings sharing one `shared_ref`, relation `contained_by` or `partial`, linked by an optional `group_id`.
- **Representable in v4.3:** Yes. `group_id` is new.
- **Verdict:** [x] Agree
- **Notes / revision:** Handled via `group_id` links with `contained_by` or `partial` relations.

### Case 8: One local passage covering several shared passages

- **Governing rule:** 2.8
- **v4.2 default:** One mapping per shared ref, relation `contains`, sharing one `local_reference`.
- **Representable in v4.3:** Yes
- **Verdict:** [x] Agree
- **Notes / revision:** Handled via `contains` relations sharing a single `local_reference`.

### Case 9: Matrix-like organisation (a Paṭṭhāna analysis)

- **Governing rule:** 4.4
- **v4.2 default:** A model with `node_identity_policy: opaque_ids`. Human labels are display values or aliases.
- **Representable in v4.3:** **Gap.** The field exists, but v4.2 does not specify how the opaque node set is stored. The affected works are excluded from the pilot (D4) until it does.
- **Verdict:** [x] Agree
- **Notes / revision:** Handled via `opaque_ids` policy. Node-set storage is handled under D4.

### Case 10: Same named source, two materially different editions

- **Governing rule:** 2.2
- **v4.2 default:** Two Versions with distinct opaque tokens, one `source_id`. A source is not a version.
- **Representable in v4.3:** Yes
- **Verdict:** [x] Agree
- **Notes / revision:** Distinct version tokens under one `source_id`.

### Case 11: Missing or revised source file behind a published digital version

- **Governing rule:** 2.2 artifact revisions, 7.3
- **v4.2 default:** Entry in `artifact_history` with a `change_class`. A correction keeps the token; an editorial change is a new Version; a vanished file is marked `missing` and dependent alignments are flagged.
- **Representable in v4.3:** Yes. `artifact_history` is new.
- **Verdict:** [x] Agree
- **Notes / revision:** Tracked via `artifact_history` and `change_class` without mutating existing version tokens.

### Case 12: Ambiguous legacy versioned URN

- **Governing rule:** 4.8, 7.2
- **v4.2 default:** A `legacy_aliases` record with outcome `quarantined_ambiguous`; the resolver returns an explicit ambiguity response.
- **Representable in v4.3:** Yes. `legacy_aliases` is new. It is empty until Gate C.
- **Verdict:** [x] Agree
- **Notes / revision:** Quarantined via `legacy_aliases` returning an explicit ambiguity response.

### Case 13: Edition-dependent elision (peyyāla): one edition expands a run that another contracts to a repetition marker

- **Governing rule:** 2.9.2, 2.8
- **v4.2 default:** Elision never splits a Work by itself. A contracted run is mapped as one grouped set of mappings (relation `contains`, one `group_id`). Nodes whose content is reconstructable by a recorded rule are `partial`; nodes that are not are `unmatched`; nodes whose rule is unknown are `uncertain` and push the verdict toward a hold.
- **Representable in v4.3:** Yes at the mapping and verdict level (fixtures `fixture_elision_01` to `04`, `align_01` to `03`). **Gate A decision (D3):** reconstructable elision stays `partial`. Which real editions elide what is not recorded and needs specialist input.
- **Verdict:** [x] Agree (confirmed)
- **Notes / revision:** Contracted runs are mapped as grouped sets. Reconstructable elisions remain `partial` within Tier 1 summaries.

## Part 2: Gate A decisions that are not single cases

**D1. Unresolved-fraction parameter** (`shared_model_max_unresolved_fraction`): **0.05**.

**D2. Tier 1 / Tier 2 boundary:** [x] Add "compilation or anthology work" as a Tier 2 trigger.
- Criterion: any work comprising an intentional aggregate of independently circulating texts or canonical excerpts (for example *Khuddaka Pāṭha*) requires an approved Tier 2 record before minting.

**D3. Reconstructable elision:** [x] Keep `partial` within Tier 1 summaries.

**D4. Node-set storage for opaque-ID citation models:** [x] Exclude works that need it from the pilot.

**D5. Stemmatic (inter-witness) relations:** [x] Defer past the pilot.

**D6. Textgroup and classification:** [x] Keep v4.2: a single textgroup `pali` under `plicanon`; `tipitaka`, `commentary` and `subcommentary` are generated strictly at the browse/view layer.

**D7. Script and transliteration:** [x] Keep v4.2: pure mechanical rendering stays at the resolver layer; transliterations involving distinct editorial decisions or transcription choices are separate Versions.

**D8. `standard_recension` grouping:** [x] Not adopted: lineage claims remain unreviewed metadata assertions without identity or structural implications.
