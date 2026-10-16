# Awkward-case walkthrough (v4.3; Gate A review completed 2026-10-10)

**Companion to:** `plicanon_cts_urn_v4_3_draft.md` section 9, Gate A. **Status:** all 13 cases were reviewed and agreed on 2026-10-10 (`plicanon_gate_a_review_sheet_v4_3_completed.md`); the table below is the agreed treatment. It is a paper walkthrough; the outcomes below are what the v4.2 rules would produce, not scholarly findings about any real text. Cases 1 to 4, 6 to 8, 10 and 13 are also exercised as synthetic fixtures in `plicanon_identity_fixtures_v4_3.json`.

The 12 cases come from design review section 7 (v4.1); case 13 (peyyāla elision) was added in this revision. For each, the table gives the governing rule, the expected treatment, and whether the v4.2 schema can represent it.

| # | Case | Governing rule | Expected treatment | Representable in v4.2? |
|---|---|---|---|---|
| 1 | Text in one tradition's collection, classed differently in another | 2.9.1 step 1 | One Work. Two scoped membership claims in `collections`. | Yes |
| 2 | Work with more than one functional role | 2.9.1 step 1 | One Work. Multiple `textual_role` assertions (the scheme is multi-valued). | Yes |
| 3 | Commentary whose target work needs a verified relation | 2.9.5 | A `comments_on` relation stays `unreviewed` until evidence exists. An unreviewed relation cannot support a split; a title suffix is not evidence. | Yes. Relation `status` is now a closed vocabulary. |
| 4 | Verse collection with edition-specific numbering | 2.9.2 (Test S) | Renumbering alone never splits a Work (2.9.6). If the model is reviewed and nodes are evaluated, the verdict is `yes`: new Version with mappings, and printed numbering kept as aliases. Even major reordering is a new Version when shared nodes can be evaluated and mapped. | Yes, but every imported model is `imported_unreviewed`, so the verdict is `uncertain` today. |
| 5 | Passage split over multiple lines or pages | 2.5 | A `witness_locations` record with several spans. It never enters the CTS passage component. | Yes. `index_origin` is now required. Span structure inside `coordinate` is still free-form and not validated. |
| 6 | Edition lacking a canonical unit | 2.9.2 | The mapping state is `unmatched`, which counts as evaluated. It does not weaken the shared model and is not "does not exist". | Yes |
| 7 | Two local segments mapping to one shared passage | 2.8 | Two mappings sharing one `shared_ref`, relation `contained_by` or `partial`, linked by an optional `group_id`. | Yes. `group_id` is new. |
| 8 | One local passage covering several shared passages | 2.8 | One mapping per shared ref, relation `contains`, sharing one `local_reference`. | Yes |
| 9 | Matrix-like organisation (a Paṭṭhāna analysis) | 4.4 | A model with `node_identity_policy: opaque_ids`. Human labels are display values or aliases. | **Gap.** The field exists, but v4.2 does not specify how the opaque node set is stored. The affected works are excluded from the pilot (D4) until it does. |
| 10 | Same named source, two materially different editions | 2.2 | Two Versions with distinct opaque tokens, one `source_id`. A source is not a version. | Yes |
| 11 | Missing or revised source file behind a published digital version | 2.2 artifact revisions, 7.3 | Entry in `artifact_history` with a `change_class`. A correction keeps the token; an editorial change is a new Version; a vanished file is marked `missing` and dependent alignments are flagged. | Yes. `artifact_history` is new. |
| 12 | Ambiguous legacy versioned URN | 4.8, 7.2 | A `legacy_aliases` record with outcome `quarantined_ambiguous`; the resolver returns an explicit ambiguity response. | Yes. `legacy_aliases` is new. It is empty until Gate C. |
| 13 | Edition-dependent elision (peyyāla): one edition expands a run that another contracts to a repetition marker | 2.9.2, 2.8 | Elision never splits a Work by itself. A contracted run is mapped as one grouped set of mappings (relation `contains`, one `group_id`). Nodes whose content is reconstructable by a recorded rule are `partial`; nodes that are not are `unmatched`; nodes whose rule is unknown are `uncertain` and push the verdict toward a hold. | Yes at the mapping and verdict level (fixtures `fixture_elision_01` to `04`, `align_01` to `03`). **Gate A decision (D3):** reconstructable elision stays `partial`. Which real editions elide what is not recorded and needs specialist input. |

## Gate A outcome (2026-10-10)

All 13 cases agreed. The decisions that were not single cases (D1 to D8) are recorded in the completed review sheet and in `registry.gate_a_record`:

1. `shared_model_max_unresolved_fraction` = 0.05.
2. Compilation or anthology works are a Tier 2 trigger.
3. Reconstructable elision stays `partial` within Tier 1 summaries.
4. Works needing opaque node-set storage are excluded from the pilot.
5. Stemmatic relations are deferred past the pilot.
6. Single textgroup `pali` under `plicanon` stays; classification is a browse-layer view.
7. Mechanical rendering stays at the resolver layer; a transliteration with its own decisions is a separate Version.
8. `standard_recension` is not adopted.
