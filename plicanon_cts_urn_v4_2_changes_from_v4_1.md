# Changes from v4.1 to v4.2

**Scope:** the identity and recension rules (Gate A) and the registry fields that enforce them. Namespace token, textgroup policy, passage syntax, and resolver rules are unchanged from v4.1. The v4.1 design review remains the rationale for those unchanged decisions.

## Rule changes

| # | v4.1 | v4.2 | Where |
|---|---|---|---|
| 1 | Rule 4 kept uncertain cases "distinct provisionally"; combined with immutability, a provisional split becomes permanent once minted. | Uncertain cases are **held unminted** (`held_uncertain`). The smallest affected identifier set is held; no reserved URN, no `GetCapabilities` entry. | Spec 2.9.3, A.5 |
| 2 | "A defensible shared citation model" had no criteria. | **Test S** with verdicts yes / no / uncertain. `yes` needs a reviewed model, no unevaluated nodes, and an unresolved fraction within a steward-set parameter. `no` needs a reviewer finding with evidence. Anything else is `uncertain`. | 2.9.2, A.6 |
| 3 | No decision record. | **Identity Decision Record** (template plus `identityDecision` schema). Approval needs a named reviewer and date; a split needs at least two works and a reviewed relation. | 2.9.1, 4.7 |
| 4 | Split relation could rest on an unreviewed relation. | A split IDR must cite `reviewed` relations; title-suffix relations cannot support a split. Relation `status` is now a closed vocabulary. | 2.9.5 |
| 5 | Distinct referential scope appeared only in the design review. | Explicit exception in the rules: documented distinct scope permits a split even when Test S is `yes`; undocumented scope is a hold. | 2.9.4 |
| 6 | Shared model growth after minting was implied. | Stated: additive only; never renumber or reassign nodes. | 2.9.3 |

## Registry and schema changes

| Change | Detail |
|---|---|
| `citation_model_status` | Replaces reliance on a null `citation_model_id`. Values `defined` (18 works), `not_yet_defined`, `not_recorded` (62 works, because the v4.1 import carried none). Schema enforces that `defined` has a model id and the others have none. |
| `minting_state` | Per work: blocked / candidate / held_uncertain / approved_for_minting / minted. All 80 are `blocked`. |
| `release_gates` | Gates A to D in `registry`, all open, with dependencies. |
| `identity_parameters` | `shared_model_max_unresolved_fraction`, null until Gate A sets it. |
| Opaque tokens | Version and exemplar example tokens are now `v0001` and `x0001` instead of `pts1_pli_latn` and `copy01`. Recommended policy, confirmed at Gate B. |
| Citation models | Added `review_status` and `node_identity_policy`. All 8 are `imported_unreviewed` and `unspecified`. |
| `artifact_history` | On versions; change classes `rehost_identical`, `transcription_correction`, `editorial_change`. |
| `legacy_aliases` | New array, empty until Gate C. |
| `index_origin` | Now required on witness locations (v4.1 required it in prose only). |
| `group_id` | Optional on alignment mappings. |

## Deliberately not changed

- The 80 mnemonic work ids (for example `dn`) are retained as non-semantic keys. Replacing them with opaque keys is a Gate B decision and is cheapest before minting.
- No numeric value for the unresolved-fraction parameter is proposed. It is a governance choice.
- No versions, exemplars, relationships, classification assertions, alignments, IDRs, or legacy aliases were invented.
- The authority URI stays null; `plicanon` stays the provisional token and `pli` stays rejected.

## Known gaps carried forward

- How to store the node set of an `opaque_ids` citation model is not specified (walkthrough case 9). Works that need it cannot become eligible.
- The internal structure of witness-location `coordinate` objects is still free-form.
- None of the 8 imported citation models has been reviewed, so Test S can only return `uncertain` for every work today.
- The official CTS parser and protocol harness have not been run.

## Revision 2 (after external evaluation of the first v4.2 bundle)

| Point raised | Finding | Change |
|---|---|---|
| Dual maintenance of schema and script could drift | Partly valid. The script held an unchecked gap: stored Test S verdicts in records were never recomputed. The cross-record and arithmetic rules cannot be written in JSON Schema. | The checker now recomputes every stored verdict through the one decision function, and the README lists which rule lives where. |
| An IDR for every variant would slow ingestion | Valid. Spec 2.9 read as if every identity decision needed an IDR. | Two tiers (spec 2.9.8, `registry.decision_tiers`): routine decisions carry a Test S summary on the version record and need no IDR; structural decisions need an approved IDR. The boundary is a Gate A decision. |
| Fixtures should cover peyyāla expansion and contraction | Valid. The first bundle had no elision cases and no witness-hierarchy modelling. | Four elision verdict fixtures and three elision-related alignment fixtures, plus four alignment-set rules (walkthrough case 13). Fixtures are synthetic and name no real edition. |

Not changed: witness hierarchies and stemmatic relations between witnesses are still not modelled (`witness_locations` records places in a witness, not relations between witnesses). Whether reconstructable elision should stay `partial` or get its own relation value is open for Gate A. There is no CI pipeline; the checker only makes one possible.

## Revision 3

Added `plicanon_gate_a_review_sheet_v4_2.md`: an agree/revise sheet generated from the walkthrough's 13 cases, eight further Gate A decisions (D1 to D8), and a table showing where an earlier external review's items landed. The checker verifies that the sheet's case titles and v4.2 defaults match the walkthrough. Only case 13 is pre-filled (carried, to be confirmed); every other verdict is blank.
