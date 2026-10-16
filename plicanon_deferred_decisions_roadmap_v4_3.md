# Deferred decisions roadmap (v4.3): D4 and D5

**Status:** proposal for steward review. It sets entry criteria and open design questions for the two items Gate A deferred past the pilot. It does not decide them, set dates, or name owners; those blanks are yours.

**What "deferred" means here:** the work records stay in the registry, but works that depend on the deferred capability cannot reach `approved_for_minting`. The registry records both items in `registry.deferred_decisions`.

## D4. Node-set storage for opaque-ID citation models

### Current state (checked against the registry)

- All 8 imported citation models have `node_identity_policy: unspecified` and `review_status: imported_unreviewed`. None is marked `opaque_ids`.
- The `abhidhamma` model covers 7 works, including Paṭṭhāna (`patth`), and is `defined` for each.
- Minting eligibility rule 6 requires `hierarchical_ordinal`, so all 18 works with a defined model are already ineligible while the policy is `unspecified`. The D4 exclusion therefore starts to mean something only when a reviewer sets a policy: `opaque_ids` for a work that needs it, or `hierarchical_ordinal` for one that does not.
- The policy is set per model, not per work. If only some of the 7 Abhidhamma works need opaque node ids, their shared model has to be split into separate models first.

### Entry criteria

A work that needs opaque nodes may enter the pilot or a later release only when all of these hold:

1. **E1.** A node-set storage specification is written and approved at a gate.
2. **E2.** Node ids are opaque, stable, and never reused, and carry no semantics.
3. **E3.** Display labels and printed numbering are kept as aliases or labels, separate from node identity.
4. **E4.** Nodes map to version-local spans using the existing node states (`mapped`, `partial`, `unmatched`, `uncertain`, `not_evaluated`), so Test S applies unchanged.
5. **E5.** The structure is stated: either a parent/order structure or an explicit flat set, together with how a passage reference is validated against the set.
6. **E6.** After minting, the node set changes additively only (already rule 2.9.3).
7. **E7.** The citation model is `reviewed` with policy `opaque_ids`, and a synthetic matrix-like fixture set passes in the checker.
8. **E8.** A specialist confirms that the node set reflects how the work is actually cited. Nothing in this bundle has had that review.

### Design questions for the steward

- **Q1.** Flat opaque ids, or hierarchical opaque ids?
- **Q2.** How are matrix-like coordinates represented: as aliases on a flat set, as structured coordinates, or as separate dimensions?
- **Q3.** Where is the node set stored: inline in the registry, or in separate files keyed by model id and checked by digest? Large sets argue for separate files.
- **Q4.** How does the adopted CTS release carry an opaque id in the passage component? This is answered at Gate D against the chosen protocol release.

### Interim options (none adopted)

- **O1. Keep unminted** until E1 to E8 are met. This is the current default.
- **O2. Work-level-only minting.** Mint the Work URN only, with no passage references or versions, so the work is citable as a whole. This needs a new minting state and a gate decision. Later node-set decisions could not change the Work URN, but Test S could not run until versions exist.
- **O3. Treat the work as hierarchical** with a documented simplification. This is a claim about the text, not a modelling shortcut, so it needs specialist agreement. I do not recommend it without one.

### Sequencing

After Gate D (the pilot) as a separate phase. Trigger: Gate D passed and the steward schedules it. **Owner:** ______  **Target:** ______

## D5. Stemmatic (inter-witness) relations

### Current state

`witness_locations` records places within a witness. Nothing in the bundle relates one witness to another. Identity rules do not depend on stemmatic structure: Test S works on shared nodes and mappings only.

### Entry criteria

1. **E1.** Decide whether witnesses are registered entities with their own ids, distinct from Versions and Exemplars.
2. **E2.** Define a relation vocabulary, with evidence and a review status on every relation.
3. **E3.** State the boundary: a Version or Exemplar is not automatically a node in a stemma, and no stemmatic claim changes a minted identifier.
4. **E4.** Add synthetic fixtures and checker rules, tested one rule at a time.
5. **E5.** Specialist review of the vocabulary and the claims it can express.

### Sequencing

After the pilot. It can proceed independently of D4. **Owner:** ______  **Target:** ______
