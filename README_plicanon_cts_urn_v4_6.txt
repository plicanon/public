PliCanon CTS-URN v4.6 Draft Bundle

A file carries the version in which it last changed; files unchanged since v4.5 or earlier keep those names.

Current (bundle v4.6.2; specification text is still v4.6):
- plicanon_cts_urn_v4_6_draft.md: profile specification
- plicanon_cts_urn_v4_6_2_changes_from_v4_6_1.md: what changed in v4.6.2 (resolver address-block holder recorded)
- plicanon_cts_urn_v4_6_1_changes_from_v4_6.md: what changed in v4.6.1 (successor acceptance evidence)
- plicanon_cts_urn_v4_6_changes_from_v4_5.md: what changed in v4.6, what stays open
- plicanon_gate_b_gate_c_decision_record_v4_6.md: record of the Gate B and Gate C answers and what is needed to close Gate B
- plicanon_registry_v4_6_draft.json and plicanon_registry_v4_6.schema.json: registry (80 imported works) and its schema
- catalog.json: the pinned catalog, byte for byte (SHA-256 7b96fd44f544565d34cbae980ed9cd2b57466c001ee8c4a3c21fbdcd6d4059f9)
- check_plicanon_v4_6.py: validator (needs Python 3 and jsonschema); run from this directory: python3 check_plicanon_v4_6.py
- plicanon_cts_urn_v4_6_validation_report.md: results of running it
- plicanon_successor_acceptance_statement_template.md: template for the successor's acceptance statement (a template is not evidence; see the registry's succession.acceptance)
- plicanon_cts_urn_v4_6_SHA256SUMS.txt: checksums (exclude themselves and the archive)

The checker needs every file in this bundle, including the carried-over fixtures, walkthrough and Gate A sheet below. A partial copy will fail with a missing-file error.

Unchanged since v4.5 or earlier:
- plicanon_gate_a_review_sheet_v4_3_completed.md, plicanon_identity_case_walkthrough_v4_3.md, plicanon_identity_decision_record_template.md, plicanon_identity_fixtures_v4_3.json
- plicanon_deferred_decisions_roadmap_v4_3.md (proposal), plicanon_resolver_binding_design_v4_3.md, plicanon_resolver_binding_fixtures_v4_3.json, check_resolver_binding_proposal_v4_3.py (proposal and its ten fixtures; run separately)
- change history: plicanon_cts_urn_v4_5_changes_from_v4_4.md, plicanon_cts_urn_v4_4_changes_from_v4_3.md, plicanon_cts_urn_v4_3_changes_from_v4_2.md, plicanon_cts_urn_v4_2_changes_from_v4_1.md

Where each rule lives
- JSON Schema: structure, enums and conditionals inside one record. The checker runs it first.
- Checker: rules that look across records, files or computed values (gate dependencies, minting eligibility, Test S recomputation, alignment-set rules, URL provenance, the availability endpoint and pin conditions, offline verification of catalog.json).
- Spec: the reasons for each rule.

Status: Gates A and C are closed. Gate B is open on B1 (immutable catalog copy, successor acceptance, ownership transfer, durability wording). Gate D is open. The resolver is a stub and the availability endpoint serves the catalog only. This is not approval to mint public identifiers.
