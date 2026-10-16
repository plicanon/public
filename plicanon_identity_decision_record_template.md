# Identity Decision Record (IDR) template

**Used by:** `plicanon_cts_urn_v4_3_draft.md` section 2.9. **Machine shape:** `identityDecision` in `plicanon_registry_v4_3.schema.json`.

Use an IDR for **Tier 2 (structural)** decisions only (spec 2.9.8): a separate-Work outcome, a hold or its resolution, documented distinct referential scope, a Test S verdict other than `yes`, or a compilation or anthology work (outcome `compilation_recorded`; use section 6a below instead of sections 3 to 5). Routine Tier 1 decisions need no IDR; a new Version carries a Test S summary on its version record instead.

One IDR answers one identity question. An IDR must be `approved`, with a named reviewer and decision date, before any identifier it affects can be minted. An unapproved IDR leaves the affected records `blocked` or `held_uncertain`.

## 1. Header

- **IDR id:** (registry token, for example `idr_0001`)
- **Subject works:** (registry work ids)
- **Subject versions:** (registry version ids, if any)
- **Question:** (one sentence, for example "Do these two recensions share one Work-level citation model?")
- **Status:** draft | under_review | approved | superseded | withdrawn
- **Reviewer (named):**
- **Decided on (ISO date):**

## 2. Classification check (decision order step 1)

Is the only difference a collection, tradition, role, or genre placement?

- [ ] Yes. Outcome is `no_split`. Record the scoped assertions, then stop.
- [ ] No. Continue.

## 3. Test S inputs

- **Shared model id:**
- **Model review status:** imported_unreviewed | under_review | reviewed
- **Node states** (counts over all shared nodes, for the versions under evaluation):

| mapped | partial | unmatched | uncertain | not_evaluated |
|---|---|---|---|---|
|  |  |  |  |  |

- **Unresolved fraction** = (uncertain + not_evaluated) / total nodes:
- **Steward parameter** `shared_model_max_unresolved_fraction`:
- **Reviewer finding of structural irreconcilability:** yes | no
  - If yes, evidence (citable, specific):
- **Distinct referential scope asserted:** yes | no
  - If yes, documentation:

## 4. Verdict

- [ ] `yes` (reviewed model, `not_evaluated` = 0, unresolved fraction within the parameter)
- [ ] `no` (reviewer finding with non-empty evidence; a finding without evidence counts as missing evidence)
- [ ] `uncertain` (any other case)

## 5. Relations relied on (split outcomes only)

| Subject work | Relation type | Target work | Relation status (must be `reviewed`) |
|---|---|---|---|
|  |  |  |  |

A relation inferred from a title suffix, or any `unreviewed` relation, cannot support a split.

## 6. Outcome

- [ ] `no_split`
- [ ] `new_version`
- [ ] `separate_work` (needs at least two subject works, a reviewed relation, and a documented rationale)
- [ ] `held_uncertain` (the smallest affected identifier set stays unminted; list it here):
- [ ] `compilation_recorded` (complete section 6a)

## 6a. Compilation record (compilation or anthology works only)

A compilation work is an intentional aggregate of independently circulating texts or canonical excerpts. Set the work's `aggregate_status` to `aggregate` and record:

- **Component description (optional):**
- **Boundary documentation** (where the compilation starts and ends, and what is in or out of it):
- **Node-inheritance rule** (how citation nodes of the compilation relate to nodes of any component that is also registered or cited independently):

## 7. Rationale

(At least a few sentences: why this outcome, what evidence, what would change it.)

## 8. Effects

- **Records whose `minting_state` changes:**
- **Mappings or alignment sets to publish:**
- **Anything the decision leaves unresolved:**
