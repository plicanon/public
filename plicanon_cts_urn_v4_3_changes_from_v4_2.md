# Changes from v4.2 to v4.3

**Scope:** applying the completed Gate A review (2026-10-10). The v4.1-to-v4.2 history stays in `plicanon_cts_urn_v4_2_changes_from_v4_1.md`.

## Decisions applied

| Gate A item | Applied as |
|---|---|
| 13 walkthrough cases agreed | `plicanon_gate_a_review_sheet_v4_3_completed.md`; walkthrough annotated with the agreed outcome |
| Case 4: renumbering never splits | Explicit sentence in spec 2.9.6 and the branching table; major reordering stays a new Version when Test S is `yes` |
| D1: parameter | `identity_parameters.shared_model_max_unresolved_fraction` = **0.05**, status `set_at_gate_a` |
| D2: compilation or anthology works are Tier 2 | New Tier 2 trigger; work field `aggregate_status` (`not_assessed`, `not_aggregate`, `aggregate`); IDR outcome `compilation_recorded` with a `compilation` object (boundaries, node-inheritance rule); minting eligibility rule 7 |
| D3: reconstructable elision | Stays `partial` within Tier 1 summaries; no schema change |
| D4: opaque node-set storage | Recorded in `registry.deferred_decisions`; minting eligibility rule 6 requires `node_identity_policy: hierarchical_ordinal` |
| D5: stemmatic relations | Recorded in `registry.deferred_decisions` as deferred past the pilot |
| D6, D7, D8 | Confirmed v4.2 positions; D7 and D8 recorded as rejected alternatives B.9 and B.10 |
| Gate A closure | `release_gates` A: `closed`, with `closed_on`, `decided_by` and `basis`; the schema requires those fields on any closed gate |
| Record of the decisions | `registry.gate_a_record` |

## Fixtures and checks

- Fixture parameter is now the registry value (0.05), and the checker fails if the two differ. One fixture (04) was adjusted to stay inside 5%. Four fixtures were added: exactly at the boundary, just above it, a 10-node model with one uncertain node, and a renumbering-only case.
- New eligibility tests start from a fully eligible baseline and break one rule at a time (aggregate not assessed, aggregate without a compilation record, opaque node policy, closed gate without an approver), so each rule is tested on its own rather than being masked by the open gates.
- 34 checks pass.

## Consequences to be aware of

- **The parameter is strict on small models.** With 0.05, a model of fewer than 20 nodes cannot tolerate even one `uncertain` node.
- **The compilation criterion is broad.** "An intentional aggregate of independently circulating texts or canonical excerpts" may apply to many of the 80 imported works, including collections such as the nikāyas. No work was classified. All 80 are `not_assessed`, which blocks minting until each is assessed by a specialist.
- **Gate A does not unlock minting.** Gates B, C and D are open, the authority URI is null, no citation model is reviewed, and so Test S can only return `uncertain` today.

## Still open

- **Approver's name.** The gate record's `decided_by` holds a placeholder: "steward (approver name to be entered before publication)". Enter the name before the bundle is published.
- **Gate B:** authority URI, steward and succession, resolver discovery, `plicanon` token confirmation, work-id policy, opaque version-token recommendation.
- **Gate C:** legacy URN audit.
- **Gate D:** pilot scope, official CTS parser and harness.
- **Deferred past the pilot:** opaque node-set storage and stemmatic relations.

## Addendum: Gate B decision sheet

Added `plicanon_gate_b_decision_sheet_v4_3.md`: fill-in decisions B1 to B4 (authority URI and stewardship, namespace token, work-id policy, version and exemplar token pattern), a Gate A housekeeping item (approver name), and three Gate C input questions. No spec or registry rule changed. The sheet states facts about the imported work ids (14 are another id plus `a`, 2 are base plus `mht`/`pmt`, 5 overlap by accident), and the checker recomputes them from the registry so the sheet cannot drift. No authority URI or steward is proposed; the checker also fails if the sheet contains a URL.

## Addendum: deferred-decision roadmap and resolver binding proposal

Prompted by two risks raised in review. Neither changes an approved rule.

- **Deferred items had no path back in.** `plicanon_deferred_decisions_roadmap_v4_3.md` gives D4 and D5 entry criteria, open design questions, interim options (none adopted), and blank owner and target fields. Each entry in `registry.deferred_decisions` now carries a `roadmap_file`, and the checker verifies the entry exists. Finding recorded in the roadmap: no imported model is marked `opaque_ids`, the policy is set per model rather than per work, and the `abhidhamma` model is shared by 7 works including Paṭṭhāna, so treating one of them differently would first require splitting the model.
- **No binding from a Version to stored bytes.** `plicanon_resolver_binding_design_v4_3.md` proposes rules R1 to R7 (default revision, tier order, same-bytes-only fallback, digest verification, distinct failure states, reporting, dated location changes). Ten synthetic fixtures run separately in `check_resolver_binding_proposal_v4_3.py` and pass. This was outside Gate A's scope; the document recommends deciding it at Gate B and testing it at Gate D. It proposes no URL, host or storage layout.
- Main checker: 38 checks pass.

## Addendum: Gate B reply of 2026-10-10

A reply to the Gate B sheet answered a different set of questions, so only one item was recorded: B2 (token) is marked answered in `plicanon_gate_b_decision_sheet_v4_3.md`. The registry and spec are unchanged until Gate B closes in a v4.4 build. Not recorded: a fallback rule returning structural ancestors or a default witness (conflicts with spec 6.2 step 6, 6.4 and `resolver_fallback_policy.silent_fallback: forbidden`), and a routing description naming a "CTN Information Retrieval layer" and TEI XML source paths (neither appears anywhere in the bundle). B0, B1, B3, B4 and the Gate C fact question remain open.
