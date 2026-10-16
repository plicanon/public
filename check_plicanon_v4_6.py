#!/usr/bin/env python3
"""Checks for the PliCanon CTS-URN v4.6 draft bundle.
Run from the bundle directory:  python3 check_plicanon_v4_6.py
Exit status 0 only if every check passes. Not an official CTS parser."""
import copy, json, re, sys
import jsonschema

REG = 'plicanon_registry_v4_6_draft.json'
SCH = 'plicanon_registry_v4_6.schema.json'
FIX = 'plicanon_identity_fixtures_v4_3.json'
results = []

def check(name, ok, detail=''):
    results.append((name, bool(ok), detail))
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{detail}]' if detail else ''))

# ---- decision function for spec 2.9 -------------------------------------
def shared_model_verdict(i, tau):
    ns = i['node_states']
    total = sum(ns.values())
    if i.get('structural_irreconcilable'):
        return 'no' if i.get('irreconcilable_evidence') else 'uncertain'
    if tau is None or not i.get('model_reviewed') or total == 0 or ns['not_evaluated'] > 0:
        return 'uncertain'
    unresolved = (ns['uncertain'] + ns['not_evaluated']) / total
    return 'yes' if unresolved <= tau else 'uncertain'

def decide(i, tau):
    if i['classification_only']:
        return 'no_split'
    v = shared_model_verdict(i, tau)
    if v == 'uncertain':
        return 'held'
    if v == 'yes':
        if i.get('distinct_scope_asserted'):
            return 'separate_work' if i.get('distinct_scope_documented') else 'held'
        return 'new_version'
    return 'separate_work' if i.get('relation_status') == 'reviewed' else 'held'

def test_inputs(t, model_reviewed):
    """Adapt a stored sharedModelTest record to the decision function's inputs."""
    rf = t.get('reviewer_finding') or {}
    ds = t.get('distinct_referential_scope') or {}
    return {'classification_only': False, 'model_reviewed': model_reviewed, 'node_states': t['node_states'],
            'structural_irreconcilable': rf.get('structural_irreconcilable', False),
            'irreconcilable_evidence': rf.get('evidence', []),
            'distinct_scope_asserted': ds.get('asserted', False),
            'distinct_scope_documented': bool(ds.get('documentation')), 'relation_status': None}

def alignment_problems(a):
    """Rules over one alignment set that JSON Schema cannot express (cross-mapping)."""
    p = []
    ids = [m['id'] for m in a['mappings']]
    if len(ids) != len(set(ids)): p.append('duplicate mapping ids')
    exact = [(m['shared_ref'], m['version_id']) for m in a['mappings'] if m['relation'] == 'exact']
    if len(exact) != len(set(exact)): p.append('shared node exact-mapped more than once in one version')
    groups = {}
    for m in a['mappings']:
        if m.get('group_id'): groups.setdefault(m['group_id'], set()).add(m['version_id'])
    if any(len(v) > 1 for v in groups.values()): p.append('group spans more than one version')
    if any(m['relation'] == 'unmatched' and (m.get('local_reference') or m.get('local_spans')) for m in a['mappings']):
        p.append('unmatched mapping names a local location')
    return p

# ---- registry invariants -------------------------------------------------
def invariants(reg):
    """Return a list of problem strings."""
    p = []
    tok = re.compile(r'^[a-z][a-z0-9_]*$')
    works = reg['works']
    ids = [w['id'] for w in works]
    if len(ids) != len(set(ids)): p.append('duplicate work ids')
    p += [f'bad token {i}' for i in ids if not tok.match(i)]
    models = {m['id']: m for m in reg['citation_models']}
    gates = {g['id']: g['status'] for g in reg['registry']['release_gates']}
    held = {w for d in reg['identity_decisions'] if d['outcome'] == 'held_uncertain' and d['status'] != 'superseded' for w in d['subject_work_ids']}
    approved_split = {w for d in reg['identity_decisions'] if d['outcome'] == 'separate_work' and d['status'] == 'approved' for w in d['subject_work_ids']}
    compiled = {w for d in reg['identity_decisions'] if d['outcome'] == 'compilation_recorded' and d['status'] == 'approved' for w in d['subject_work_ids']}
    any_split = {w for d in reg['identity_decisions'] if d['outcome'] == 'separate_work' for w in d['subject_work_ids']}
    rel = {(w['id'], r['type'], r['target_work_id']): r['status'] for w in works for r in w['relationships']}
    for w in works:
        m = models.get(w.get('citation_model_id'))
        if w['citation_model_status'] == 'defined':
            if not m: p.append(f"{w['id']}: defined but model missing")
            elif w['id'] not in m['applies_to']: p.append(f"{w['id']}: not in applies_to of {m['id']}")
        elif w['citation_model_id'] is not None:
            p.append(f"{w['id']}: status {w['citation_model_status']} but model id set")
        if w['minting_state'] in ('approved_for_minting', 'minted'):
            for g in 'ABC':
                if gates[g] != 'closed': p.append(f"{w['id']}: gate {g} open")
            if not reg['registry']['namespace_authority_uri']: p.append(f"{w['id']}: authority URI null")
            if w['citation_model_status'] != 'defined' or not m or m['review_status'] != 'reviewed':
                p.append(f"{w['id']}: no reviewed citation model")
            if m and m['node_identity_policy'] != 'hierarchical_ordinal':
                p.append(f"{w['id']}: node_identity_policy {m['node_identity_policy']} not eligible (D4)")
            agg = w['aggregate_status']
            if agg == 'not_assessed': p.append(f"{w['id']}: aggregate_status not assessed")
            elif agg == 'aggregate' and w['id'] not in compiled: p.append(f"{w['id']}: aggregate without approved compilation record")
            if w['id'] in held: p.append(f"{w['id']}: open hold")
            if w['id'] in any_split and w['id'] not in approved_split: p.append(f"{w['id']}: split IDR not approved")
    for d in reg['identity_decisions']:
        for r in d.get('relation_refs', []):
            st = rel.get((r['subject_work_id'], r['type'], r['target_work_id']))
            if d['outcome'] == 'separate_work' and st != 'reviewed':
                p.append(f"{d['id']}: relation not reviewed/not found")
        for w in d['subject_work_ids']:
            if w not in ids: p.append(f"{d['id']}: unknown work {w}")
    tau = reg['registry']['identity_parameters']['shared_model_max_unresolved_fraction']
    def model_ok(mid): return bool(models.get(mid)) and models[mid]['review_status'] == 'reviewed'
    rel_rank = {'reviewed': 2, 'under_review': 1, 'unreviewed': 0}
    for d in reg['identity_decisions']:
        t = d.get('shared_model_test')
        if not t: continue
        inp = test_inputs(t, model_ok(t.get('model_id')))
        if t.get('model_reviewed') is not None and t['model_reviewed'] != inp['model_reviewed']:
            p.append(f"{d['id']}: stored model_reviewed differs from registry")
        if d['outcome'] != 'no_split' and d['status'] == 'approved':
            v = shared_model_verdict(inp, tau)
            if t['verdict'] != v: p.append(f"{d['id']}: stored verdict {t['verdict']} != recomputed {v}")
            refs = [rel.get((r['subject_work_id'], r['type'], r['target_work_id'])) for r in d.get('relation_refs', [])]
            inp['relation_status'] = 'reviewed' if refs and all(x == 'reviewed' for x in refs) else 'unreviewed'
            exp = decide(inp, tau)
            if d['outcome'] == 'held_uncertain': exp = 'held_uncertain' if exp == 'held' else exp
            if d['outcome'] != exp: p.append(f"{d['id']}: outcome {d['outcome']} != rule outcome {exp}")
    for v in reg['versions']:
        if v['review_status'] == 'reviewed':
            t = v.get('shared_model_test')
            if not t: p.append(f"{v['id']}: reviewed version lacks shared_model_test"); continue
            inp = test_inputs(t, model_ok(t.get('model_id')))
            if shared_model_verdict(inp, tau) != 'yes' or t['verdict'] != 'yes':
                p.append(f"{v['id']}: Tier 1 version needs a recomputed Test S yes (otherwise Tier 2, IDR)")
    for a in reg['alignment_sets']:
        p += [f"{a['id']}: {x}" for x in alignment_problems(a)]
    na = reg['registry'].get('namespace_authority')
    if na:
        fb, pin = na['fallback_endpoint'], na['catalog_pinning']
        if fb['status'] == 'accepted' and not (fb.get('independent_of_purl') is True and fb.get('verified_on')):
            p.append('fallback endpoint accepted without independence and verification')
        if fb['status'] == 'accepted' and fb.get('serves_cts_requests') is False and not fb.get('limits'):
            p.append('static availability endpoint accepted without stated limits')
        if pin['status'] in ('digest_recorded', 'implemented') and not re.fullmatch(r'[0-9a-f]{64}', pin.get('digest_sha256', '')):
            p.append('catalog pinning implemented without a tag and a SHA-256 digest' if pin['status'] == 'implemented' else 'catalog pinning digest_recorded without a SHA-256 digest')
        if pin['status'] == 'implemented' and not (pin.get('tag') or pin.get('archive_doi')):
            p.append('catalog pinning implemented without a tag and a SHA-256 digest')
    if na:
        sc = na['succession']; ac = sc['acceptance']
        if ac['status'] == 'verified':
            if not ac['evidence']: p.append('successor acceptance verified without evidence')
            if any(not (e.get('effective_date') or e.get('trigger')) for e in ac['evidence']): p.append('successor acceptance evidence lacks an effective date or trigger')
        elif ac['evidence']:
            p.append('successor acceptance has evidence entries but is not marked verified')
        if (sc['status'] == 'acceptance_evidenced') != (ac['status'] == 'verified'):
            p.append('succession status and acceptance status disagree')
        if any(g['id'] == 'B' and g['status'] == 'closed' for g in reg['registry']['release_gates']) and ac['status'] != 'verified':
            p.append('gate B closed without verified successor acceptance')
    if na and na.get('resolver_hosting'):
        rh = na['resolver_hosting']
        if rh['provider_name_status'] == 'established' and not rh.get('provider_name'): p.append('resolver provider marked established without a name')
        if rh.get('provider_name') and not rh.get('basis'): p.append('resolver provider named without a basis')
        if rh['provider_name_status'] != 'established' and rh.get('provider_name'): p.append('resolver provider named but not marked established')
    gbr = reg['registry'].get('gate_b_record')
    if gbr and any(g['id'] == 'B' and g['status'] == 'closed' for g in reg['registry']['release_gates']):
        if gbr['b1']['status'] != 'closed' or gbr['b1']['open']:
            p.append('gate B closed with open B1 items')
    for g in reg['registry']['release_gates']:
        if g['status'] == 'closed':
            if not g.get('decided_by') or not g.get('closed_on'): p.append(f"gate {g['id']} closed without decided_by/closed_on")
            for dep in g['depends_on']:
                if gates[dep] != 'closed': p.append(f"gate {g['id']} closed before {dep}")
    return p

def main():
    reg = json.load(open(REG, encoding='utf-8'))
    sch = json.load(open(SCH, encoding='utf-8'))
    V = jsonschema.Draft202012Validator(sch)
    jsonschema.Draft202012Validator.check_schema(sch)
    check('schema is valid Draft 2020-12', True)
    errs = list(V.iter_errors(reg))
    check('registry validates against schema', not errs, f'{len(errs)} errors')
    probs = invariants(reg)
    check('registry invariants hold', not probs, '; '.join(probs[:3]))
    ws = reg['works']
    check('80 works, unique ids', len(ws) == 80 and len({w['id'] for w in ws}) == 80)
    from collections import Counter
    c = Counter(w['citation_model_status'] for w in ws); print('     citation_model_status:', dict(c))
    check('all works blocked at v4.6', all(w['minting_state'] == 'blocked' for w in ws))
    gs = {g['id']: g['status'] for g in reg['registry']['release_gates']}
    check('gates A and C closed; gates B and D open', gs == {'A': 'closed', 'B': 'open', 'C': 'closed', 'D': 'open'}, str(gs))
    na = reg['registry']['namespace_authority']
    check('authority URI is the selected PURL in the registry, the policy and the authority record',
          reg['registry']['namespace_authority_uri'] == na['authority_uri'] == reg['registry']['namespace_authority_policy']['authority_uri'] == 'https://purl.archive.org/plicanon/cts/v1')
    check('parameter set to 0.05 at Gate A', reg['registry']['identity_parameters']['shared_model_max_unresolved_fraction'] == 0.05)
    check('all 80 works aggregate_status not_assessed (blocks minting until assessed)', all(w['aggregate_status'] == 'not_assessed' for w in ws))
    check('no versions/exemplars/IDRs/legacy aliases invented',
          not any(reg[k] for k in ('versions', 'exemplars', 'identity_decisions', 'legacy_aliases')))

    # lexical envelope regex
    env = re.compile(reg['urn_syntax']['lexical_envelope_regex'])
    good = ['urn:cts:plicanon:pali:', 'urn:cts:plicanon:pali.dn:', 'urn:cts:plicanon:pali.dn:16.3',
            'urn:cts:plicanon:pali.dn.v0001:16.3', 'urn:cts:plicanon:pali.dn.v0001.x0001:16.3',
            'urn:cts:plicanon:pali.dn.v0001:16.3-16.5', 'urn:cts:plicanon:pali.dn.v0001:16.3@nibbāna[2]']
    bad = ['urn:cts:pli:pali.dn:1', 'urn:cts:plicanon:pali.dn.a.b.c:1', 'urn:cts:plicanon:pali-x.dn:1',
           'urn:cts:plicanon:pali.dn', 'urn:cts:plicanon:Pali.dn:1', 'urn:cts:plicanon::1']
    check(f'envelope accepts {len(good)} valid shapes', all(env.match(u) for u in good))
    check(f'envelope rejects {len(bad)} invalid shapes', not any(env.match(u) for u in bad))
    check('identifier examples use opaque tokens', all('pts1' not in e['urn'] and 'copy01' not in e['urn'] for e in reg['identifier_examples']))

    # fixtures
    fx = json.load(open(FIX, encoding='utf-8'))
    tau = fx['parameters']['shared_model_max_unresolved_fraction']
    check('fixture parameter equals registry parameter (no drift)', tau == reg['registry']['identity_parameters']['shared_model_max_unresolved_fraction'])
    bad_fx = []
    for case in fx['cases']:
        t = case['override_parameter'] if 'override_parameter' in case else tau
        got = decide(case['inputs'], t)
        if got != case['expected']: bad_fx.append(f"{case['id']}: got {got}, expected {case['expected']}")
    check(f"{len(fx['cases'])} identity fixtures produce expected outcomes", not bad_fx, '; '.join(bad_fx))

    # negative self-tests: the checker and schema must reject broken registries
    def mutated(fn):
        r = copy.deepcopy(reg); fn(r); return r
    def schema_fails(r): return bool(list(V.iter_errors(r)))
    def inv_fails(r): return bool(invariants(r))
    def set_minted(r): r['works'][0]['minting_state'] = 'approved_for_minting'
    check('negative: minting while gates open is flagged', inv_fails(mutated(set_minted)))
    def defined_null(r): r['works'][0]['citation_model_status'] = 'defined'; r['works'][0]['citation_model_id'] = None
    check('negative: schema rejects defined status with null model', schema_fails(mutated(defined_null)))
    def idr_split_one(r):
        r['identity_decisions'].append({"id": "idr_x", "subject_work_ids": ["dn"], "question": "q", "outcome": "separate_work",
          "shared_model_test": {"model_id": None, "node_states": {"mapped": 0, "partial": 0, "unmatched": 0, "uncertain": 0, "not_evaluated": 0}, "verdict": "no"},
          "rationale": "a rationale long enough to pass", "status": "draft"})
    check('negative: schema rejects split IDR with one work and no relation', schema_fails(mutated(idr_split_one)))
    def idr_approved_noreviewer(r):
        r['identity_decisions'].append({"id": "idr_y", "subject_work_ids": ["dn"], "question": "q", "outcome": "no_split",
          "shared_model_test": {"model_id": None, "node_states": {"mapped": 0, "partial": 0, "unmatched": 0, "uncertain": 0, "not_evaluated": 0}, "verdict": "uncertain"},
          "rationale": "a rationale long enough to pass", "status": "approved", "reviewer": None, "decided_on": None})
    check('negative: schema rejects approved IDR without reviewer/date', schema_fails(mutated(idr_approved_noreviewer)))
    def gate_order(r):
        for g in r['registry']['release_gates']:
            if g['id'] == 'D': g['status'] = 'closed'; g['closed_on'] = '2026-10-10'; g['decided_by'] = 'x'; g['basis'] = 'x'
    check('negative: gate D closed while gate B is open is flagged', any('before B' in x for x in invariants(mutated(gate_order))))
    def bad_wl(r): r['witness_locations'].append({"id": "wl1", "work_id": "dn", "version_id": "v0001", "coordinate_system": "page", "coordinate": {}, "review_status": "draft"})
    check('negative: schema rejects witness location without index_origin', schema_fails(mutated(bad_wl)))

    # alignment fixtures: schema-valid, then cross-mapping rules
    AV = jsonschema.Draft202012Validator({"$ref": "#/$defs/alignmentSet", "$defs": sch['$defs']})
    bad_al = []
    for af in fx['alignment_fixtures']:
        a = af['alignment_set']
        if list(AV.iter_errors(a)): bad_al.append(f"{af['id']}: schema"); continue
        got = 'invalid' if alignment_problems(a) else 'valid'
        if got != af['expect']: bad_al.append(f"{af['id']}: got {got}, expected {af['expect']}")
    check(f"{len(fx['alignment_fixtures'])} alignment fixtures (contraction, expansion, unmatched, conflicts)", not bad_al, '; '.join(bad_al))

    # stored Test S results must agree with the one decision function (no drift)
    def idr(outcome, verdict, ns, status='approved', reviewed=False, extra=None):
        d = {"id": "idr_z", "subject_work_ids": ["dn"], "question": "q", "outcome": outcome,
             "shared_model_test": {"model_id": "nikaya_sutta", "model_reviewed": reviewed, "node_states": ns, "verdict": verdict},
             "rationale": "a rationale long enough to pass", "status": status, "reviewer": "r", "decided_on": "2026-10-10"}
        if extra: d.update(extra)
        return d
    ns0 = {"mapped": 10, "partial": 0, "unmatched": 0, "uncertain": 0, "not_evaluated": 0}
    def add_idr(d): return lambda r: r['identity_decisions'].append(d)
    def yes_with_null_param(r):
        r['registry']['identity_parameters']['shared_model_max_unresolved_fraction'] = None
        r['citation_models'][0]['review_status'] = 'reviewed'
        r['identity_decisions'].append(idr('new_version', 'yes', ns0, reviewed=True))
    check('negative: approved IDR claiming yes while the parameter is null is flagged',
          any('recomputed' in x for x in invariants(mutated(yes_with_null_param))))
    def set_param_and_idr(r):
        r['registry']['identity_parameters']['shared_model_max_unresolved_fraction'] = 0.05
        r['citation_models'][0]['review_status'] = 'reviewed'
        r['identity_decisions'].append(idr('new_version', 'yes', ns0, reviewed=True))
    check('positive: consistent approved IDR passes once parameter set and model reviewed', not inv_fails(mutated(set_param_and_idr)))
    def wrong_verdict(r):
        set_param_and_idr(r); r['identity_decisions'][-1]['shared_model_test']['verdict'] = 'no'
    check('negative: stored verdict differing from recomputed verdict is flagged', inv_fails(mutated(wrong_verdict)))
    def reviewed_version_no_test(r):
        r['versions'].append({"id": "v0001", "work_id": "dn", "version_type": "edition", "review_status": "reviewed"})
    check('negative: reviewed (Tier 1) version without a Test S summary is flagged', inv_fails(mutated(reviewed_version_no_test)))

    # the Gate A review sheet must be keyed to the walkthrough's actual cases
    def walk_rows(path):
        out = []
        for line in open(path, encoding='utf-8'):
            if re.match(r'^\| \d+ \|', line):
                out.append([x.strip() for x in line.strip().strip('|').split('|')])
        return out
    walk = walk_rows('plicanon_identity_case_walkthrough_v4_3.md')
    sheet = open('plicanon_gate_a_review_sheet_v4_3_completed.md', encoding='utf-8').read()
    heads = re.findall(r'^### Case (\d+): (.+)$', sheet, flags=re.M)
    defaults = re.findall(r'^- \*\*v4\.2 default:\*\* (.+)$', sheet, flags=re.M)
    in_step = (len(walk) == 13 and [(w[0], w[1]) for w in walk] == heads and [w[3] for w in walk] == defaults)
    check('review sheet is keyed to the walkthrough (13 cases, same titles and defaults)', in_step)

    # targeted eligibility tests: start from a baseline where 'dn' is fully eligible, then break one rule at a time
    def eligible(r):
        for g in r['registry']['release_gates']:
            g['status'] = 'closed'; g['closed_on'] = '2026-10-10'; g['decided_by'] = 'steward'; g['basis'] = 'test'
        r['registry']['namespace_authority_uri'] = 'https://example.invalid/authority'
        r['registry']['gate_b_record']['b1']['status'] = 'closed'; r['registry']['gate_b_record']['b1']['open'] = []
        fb = r['registry']['namespace_authority']['fallback_endpoint']; fb.update({'status': 'accepted', 'independent_of_purl': True, 'verified_on': '2026-10-10'})
        pn = r['registry']['namespace_authority']['catalog_pinning']; pn.update({'status': 'implemented', 'tag': 't', 'digest_sha256': 'a' * 64})
        sc = r['registry']['namespace_authority']['succession']
        sc['status'] = 'acceptance_evidenced'; sc['acceptance']['status'] = 'verified'
        sc['acceptance']['evidence'] = [{'file': 'x.md', 'sha256': 'b' * 64, 'channel': 'institutional_email', 'received_on': '2026-10-20', 'signer_name': 'n', 'signer_role': 'r', 'institution': 'i', 'authority_basis': 'b', 'covers_transfer_items': True, 'trigger': 't'}]
        w = next(x for x in r['works'] if x['id'] == 'dn')
        mdl = next(m for m in r['citation_models'] if m['id'] == w['citation_model_id'])
        mdl['review_status'] = 'reviewed'; mdl['node_identity_policy'] = 'hierarchical_ordinal'
        w['minting_state'] = 'approved_for_minting'; w['aggregate_status'] = 'not_aggregate'
    check('positive: fully eligible work passes every invariant', not invariants(mutated(eligible)), '; '.join(invariants(mutated(eligible))[:2]))
    def with_(fn):
        def go(r): eligible(r); fn(r)
        return invariants(mutated(go))
    check('negative: aggregate_status not_assessed blocks minting',
          any('aggregate_status not assessed' in x for x in with_(lambda r: next(x for x in r['works'] if x['id'] == 'dn').__setitem__('aggregate_status', 'not_assessed'))))
    check('negative: aggregate without an approved compilation record blocks minting',
          any('aggregate without approved compilation' in x for x in with_(lambda r: next(x for x in r['works'] if x['id'] == 'dn').__setitem__('aggregate_status', 'aggregate'))))
    def comp_ok(r):
        next(x for x in r['works'] if x['id'] == 'dn')['aggregate_status'] = 'aggregate'
        r['identity_decisions'].append({"id": "idr_c", "subject_work_ids": ["dn"], "question": "compilation boundaries", "outcome": "compilation_recorded",
          "compilation": {"boundary_documentation": "synthetic boundary documentation text", "node_inheritance_rule": "synthetic node inheritance rule text"},
          "rationale": "a rationale long enough to pass", "status": "approved", "reviewer": "r", "decided_on": "2026-10-10"})
    check('positive: aggregate with an approved compilation record is eligible', not with_(comp_ok))
    check('negative: opaque_ids citation model blocks minting (D4)',
          any('node_identity_policy' in x for x in with_(lambda r: next(m for m in r['citation_models'] if 'dn' in m['applies_to']).__setitem__('node_identity_policy', 'opaque_ids'))))
    check('negative: closed gate without decided_by is flagged',
          any('without decided_by' in x for x in with_(lambda r: r['registry']['release_gates'][0].__setitem__('decided_by', ''))))
    def comp_schema_bad(r):
        r['identity_decisions'].append({"id": "idr_d", "subject_work_ids": ["dn"], "question": "q", "outcome": "compilation_recorded",
          "rationale": "a rationale long enough to pass", "status": "draft"})
    check('negative: schema rejects a compilation record without compilation details', schema_fails(mutated(comp_schema_bad)))
    check('negative: a fallback endpoint cannot be accepted without independence and verification',
          any('fallback endpoint accepted' in x for x in with_(lambda r: r['registry']['namespace_authority']['fallback_endpoint'].update({'independent_of_purl': False}))))
    check('negative: catalog pinning cannot be implemented without a tag and a SHA-256 digest',
          any('catalog pinning implemented' in x for x in with_(lambda r: r['registry']['namespace_authority']['catalog_pinning'].update({'digest_sha256': 'xyz'}))))
    check('negative: gate B cannot close with open B1 items',
          any('gate B closed with open B1' in x for x in with_(lambda r: r['registry']['gate_b_record']['b1'].update({'open': ['catalog_pinning']}))))

    # Gate B / Gate C decision record: items present, facts true, URLs only ones supplied or observed
    rec = open('plicanon_gate_b_gate_c_decision_record_v4_6.md', encoding='utf-8').read()
    spec = open('plicanon_cts_urn_v4_6_draft.md', encoding='utf-8').read()
    i = spec.index('**Gate B: governance**'); j = spec.index('**Gate C: legacy audit.')
    spec_items = re.findall(r'^\d+\. ', spec[i:j], flags=re.M)
    rec_items = re.findall(r'^## ([BC]\d)\. ', rec, flags=re.M)
    check('decision record has one section per Gate B item and the Gate C item', len(spec_items) == 4 and rec_items == ['B0', 'B1', 'B2', 'B3', 'B4', 'C1'], str(rec_items))
    titles = {w['id']: w['preferred_title'] for w in ws}
    ids_sorted = sorted(titles)
    prs = [(a, b) for a in ids_sorted for b in ids_sorted if a != b and b.startswith(a) and len(a) >= 2]
    la = [(a, b) for a, b in prs if b == a + 'a']
    lt = [(a, b) for a, b in prs if b[len(a):] in ('mht', 'pmt')]
    ov = len(prs) - len(la) - len(lt)
    m = re.search(r'<!-- facts: works=(\d+) layer_a=(\d+) layer_t=(\d+) overlap=(\d+) -->', rec)
    facts_ok = bool(m) and tuple(map(int, m.groups())) == (len(ids_sorted), len(la), len(lt), ov)
    titles_ok = all(('ṭṭha' in titles[b] or 'ṭīkā' in titles[b]) for _, b in la + lt)
    check('decision record facts about work ids match the registry', facts_ok and titles_ok, f'{len(la)} + {len(lt)} layer ids, {ov} overlaps')
    b1r = reg['registry']['gate_b_record']['b1']
    seen = set(b1r['urls_seen']) | set(b1r['urls_proposed'])
    check('proposed URLs are labelled and never also listed as observed', not (set(b1r['urls_proposed']) & set(b1r['urls_seen'])) and bool(b1r.get('urls_proposed_note')))
    urls = {u.rstrip('.,);`') for u in re.findall(r'https?://[^\s`<>)]+', rec)}
    stray = sorted(u for u in urls if u not in seen)
    check('every URL in the decision record was supplied or observed (registry urls_seen)', not stray, '; '.join(stray[:3]))
    gb = reg['registry']['gate_b_record']; gc = reg['registry']['gate_c_record']
    check('Gate B open on B1 only; B0, B2, B3, B4 answered', gb['status'] == 'open' and gb['b1']['status'] == 'open' and set(gb['answers']) == {'B0', 'B2', 'B3', 'B4'})
    check('B1 is open with its answered and open items listed, and the authority URI was supplied by the steward',
          set(gb['b1']['answered']) == {'authority_uri', 'succession_successor', 'steward_durability_statement', 'external_registration', 'fallback_endpoint', 'catalog_digest', 'resolver_hosting_provider_name'} and bool(gb['b1']['open'])
          and reg['registry']['namespace_authority_uri'] in set(gb['b1']['urls_seen']))
    fbk = na['fallback_endpoint']
    check('fallback accepted only as an independent static availability endpoint with its limits stated',
          fbk['status'] == 'accepted' and fbk['independent_of_purl'] is True and fbk['serves_cts_requests'] is False and bool(fbk.get('limits')) and bool(fbk.get('verified_on')))
    check('catalog pinned at digest_recorded; immutable copy still pending (not claimed as implemented)',
          na['catalog_pinning']['status'] == 'digest_recorded' and na['catalog_pinning']['immutable_copy']['status'] == 'pending')
    check('Gate C recorded as none known published; legacy_aliases empty', gc['result'] == 'none_known_published' and reg['legacy_aliases'] == [])
    check('token confirmed permanent', reg['registry']['namespace_authority_policy']['token_status'] == 'confirmed_permanent')
    check('closed gates name an approver (no placeholder)', all('to be entered' not in g.get('decided_by', '') and g.get('decided_by') for g in reg['registry']['release_gates'] if g['status'] == 'closed'))
    vp, xp = re.compile(reg['registry']['token_policy']['patterns']['version']), re.compile(reg['registry']['token_policy']['patterns']['exemplar'])
    check('identifier examples use tokens that match the normative patterns',
          all((not e.get('version_id') or vp.match(e['version_id'])) and (not e.get('exemplar_id') or xp.match(e['exemplar_id'])) for e in reg['identifier_examples']))
    def ver(i): return {"id": i, "work_id": "dn", "version_type": "edition", "review_status": "draft"}
    def exe(i, v='v0001'): return {"id": i, "work_id": "dn", "version_id": v, "item_type": "copy", "review_status": "draft"}
    def add_ver(i): return lambda r: r['versions'].append(ver(i))
    def add_exe(i, v='v0001'): return lambda r: r['exemplars'].append(exe(i, v))
    check('positive: schema accepts version v0001 and exemplar x0001', not schema_fails(mutated(add_ver('v0001'))) and not schema_fails(mutated(add_exe('x0001'))))
    check('negative: schema rejects version tokens that break the pattern (pts1_pli_latn, v001, 0001)',
          all(schema_fails(mutated(add_ver(x))) for x in ('pts1_pli_latn', 'v001', 'v0001a')))
    check('negative: schema rejects exemplar tokens that break the pattern, and a non-version parent',
          schema_fails(mutated(add_exe('copy01'))) and schema_fails(mutated(add_exe('x0001', 'edition_a'))))

    # the bundled catalog.json must match the registry pin and the recorded declarations
    import hashlib
    def catalog_problems(reg_, raw):
        q = []
        pin = reg_['registry']['namespace_authority']['catalog_pinning']
        if hashlib.sha256(raw).hexdigest() != pin['digest_sha256']: q.append('catalog digest differs from the registry pin')
        try:
            cat = json.loads(raw.decode('utf-8'))
        except Exception:
            return q + ['catalog is not valid UTF-8 JSON']
        nau = reg_['registry']['namespace_authority']
        if cat.get('authority_uri') != nau['authority_uri']: q.append('catalog authority_uri differs from the registry')
        if cat.get('cts_namespace_token') != reg_['registry']['namespace_authority_policy']['cts_namespace_token']: q.append('catalog token differs from the registry')
        eps = {e['role']: e['url'] for e in cat.get('resolver_endpoints', [])}
        if eps.get('service_availability_fallback') != nau['fallback_endpoint']['url']: q.append('catalog fallback differs from the registry')
        if eps.get('primary') != reg_['registry']['gate_b_record']['b1']['declared']['resolver_target']: q.append('catalog primary endpoint differs from the registry')
        if cat.get('steward', {}).get('name') != nau['steward']: q.append('catalog steward differs from the registry')
        return q
    raw_cat = open('catalog.json', 'rb').read()
    cp = catalog_problems(reg, raw_cat)
    check('bundled catalog.json matches the registry pin and declarations (digest, token, authority URI, endpoints, steward)', not cp, '; '.join(cp))
    check('negative: an altered catalog byte is caught by the digest', any('digest differs' in x for x in catalog_problems(reg, raw_cat.replace(b'plicanon', b'plicanoN', 1))))
    def retarget(r):
        c = json.loads(raw_cat.decode()); c['authority_uri'] = 'https://example.invalid/other'
        raw2 = (json.dumps(c, indent=2, ensure_ascii=False) + "\n").encode()
        r['registry']['namespace_authority']['catalog_pinning']['digest_sha256'] = hashlib.sha256(raw2).hexdigest()
        return raw2
    r2 = copy.deepcopy(reg); raw2 = retarget(r2)
    check('negative: a catalog whose authority URI differs from the registry is caught even with a matching digest',
          catalog_problems(r2, raw2) == ['catalog authority_uri differs from the registry'])

    # successor acceptance: template content, evidence record, and the files behind it
    def template_problems(txt):
        q = []
        for need in ('## 2. Date of acceptance', '## 4. Transfer', 'Date the transfer takes effect', 'PURL domain', 'Zenodo record', '## 7. Authority to issue', 'does not approve any gate'):
            if need not in txt: q.append('template lacks: ' + need)
        for bad in ('guarantees', 'never be invalidated', 'binding declaration', '(and subsequent normative versions)'):
            if bad in txt: q.append('template overreaches: ' + bad)
        return q
    def acceptance_problems(reg_, read):
        q = []
        for e in reg_['registry']['namespace_authority']['succession']['acceptance']['evidence']:
            try:
                raw_e = read(e['file'])
            except OSError:
                q.append(f"{e['file']}: evidence file missing"); continue
            if hashlib.sha256(raw_e).hexdigest() != e['sha256']: q.append(f"{e['file']}: evidence digest differs from the registry")
            txt = raw_e.decode('utf-8', 'replace')
            if '{{' in txt: q.append(f"{e['file']}: evidence still has unfilled placeholders")
            if not re.search(r'\*\*Pinned catalog SHA-256:\*\* `[0-9a-f]{64}`', txt): q.append(f"{e['file']}: evidence does not name the catalog digest shown to the successor")
            if '## 4. Transfer' not in txt: q.append(f"{e['file']}: evidence lacks the transfer section")
        return q
    sacc = na['succession']['acceptance']
    tpl = open(sacc['template_file'], encoding='utf-8').read()
    check('successor acceptance template covers acceptance date, transfer step, authority to issue, and avoids overreach', not template_problems(tpl), '; '.join(template_problems(tpl)))
    check('successor acceptance not yet evidenced: registry says so, no evidence entries, and the template is not counted as evidence',
          sacc['status'] == 'not_evidenced' and sacc['evidence'] == [] and na['succession']['status'] == 'stated_acceptance_by_successor_not_evidenced' and '{{' in tpl)
    good_txt = tpl.replace('{{64-hex digest of the catalog.json the successor was shown}}', 'a' * 64)
    import re as _re
    good_txt = _re.sub(r'\{\{[^}]*\}\}', 'filled', good_txt)
    def ev_reg(txt, **over):
        r_ = copy.deepcopy(reg); sc_ = r_['registry']['namespace_authority']['succession']
        sc_['status'] = 'acceptance_evidenced'; sc_['acceptance']['status'] = 'verified'
        e_ = {'file': 'ev.md', 'sha256': hashlib.sha256(txt.encode()).hexdigest(), 'channel': 'institutional_email', 'received_on': '2026-10-20', 'signer_name': 'n', 'signer_role': 'r', 'institution': 'i', 'authority_basis': 'minutes', 'covers_transfer_items': True, 'trigger': 'notice'}
        e_.update(over); sc_['acceptance']['evidence'] = [e_]
        return r_
    rd = lambda txt: (lambda path: txt.encode())
    check('positive: a filled statement recorded with a matching digest passes schema, invariants and file checks',
          not schema_fails(ev_reg(good_txt)) and not invariants(ev_reg(good_txt)) and not acceptance_problems(ev_reg(good_txt), rd(good_txt)))
    check('negative: evidence whose file digest differs from the registry is caught',
          any('digest differs' in x for x in acceptance_problems(ev_reg(good_txt), rd(good_txt + ' '))))
    check('negative: an evidence file with unfilled placeholders is caught',
          any('unfilled placeholders' in x for x in acceptance_problems(ev_reg(tpl), rd(tpl))))
    check('negative: evidence missing the transfer section is caught',
          any('transfer section' in x for x in acceptance_problems(ev_reg(good_txt.replace('## 4. Transfer', '## 4. Other')), rd(good_txt.replace('## 4. Transfer', '## 4. Other')))))
    bare = copy.deepcopy(reg); bare['registry']['namespace_authority']['succession']['acceptance']['status'] = 'verified'
    check('negative: acceptance marked verified with no evidence is caught', any('without evidence' in x for x in invariants(bare)))
    mism = ev_reg(good_txt); mism['registry']['namespace_authority']['succession']['status'] = 'stated_acceptance_by_successor_not_evidenced'
    check('negative: succession status and acceptance status must agree', any('disagree' in x for x in invariants(mism)))
    check('negative: evidence outside the allowed channels, or not covering the transfer items, fails the schema',
          schema_fails(ev_reg(good_txt, channel='hearsay')) and schema_fails(ev_reg(good_txt, covers_transfer_items=False)))
    gate_b = copy.deepcopy(reg)
    for g in gate_b['registry']['release_gates']:
        if g['id'] == 'B': g.update({'status': 'closed', 'closed_on': '2026-10-20', 'decided_by': 'steward', 'basis': 'test'})
    check('negative: closing Gate B without verified successor acceptance is caught', any('without verified successor acceptance' in x for x in invariants(gate_b)))

    # resolver hosting observation
    rh = na['resolver_hosting']
    check('resolver hosting recorded: address, headers and steward-reported whois; address-block holder established with a basis; hosting account holder not claimed',
          rh['ip'] == '163.44.198.58' and rh['provider_name'] == 'GMO Internet Pte. Ltd.' and rh['provider_name_status'] == 'established' and rh['shares_provider_with_catalog_mirror'] is False
          and 'steward-reported' in rh['verified_by'] and 'whois' in rh['verified_by'] and 'APNIC' in rh['basis'] and 'ZCOM-THAI' in rh['basis'] and 'hosting account' in rh['basis']
          and 'resolver_hosting_provider_name' in b1r['answered'] and 'resolver_hosting_provider_name' not in b1r['open'] and 'resolver_hosting_provider_name' not in ' '.join(b1r['missing']))
    check('decision record names the established address-block holder', rh['provider_name'] in rec)
    check('decision record states the recorded resolver address', rh['ip'] in rec)
    named = copy.deepcopy(reg)
    named['registry']['namespace_authority']['resolver_hosting']['provider_name_status'] = 'not_established'
    unnamed = copy.deepcopy(reg); unnamed['registry']['namespace_authority']['resolver_hosting']['provider_name'] = None
    check('negative: a provider name without an established status, or established without a name, is caught',
          any('not marked established' in x for x in invariants(named)) and any('without a name' in x for x in invariants(unnamed)))
    nobasis = copy.deepcopy(reg); del nobasis['registry']['namespace_authority']['resolver_hosting']['basis']
    check('negative: an established provider name without a basis is caught', any('without a basis' in x for x in invariants(nobasis)))
    nover = copy.deepcopy(reg); del nover['registry']['namespace_authority']['resolver_hosting']['verified_by']
    check('negative: a resolver observation without its source fails the schema', schema_fails(nover))

    # every deferred decision points at a roadmap that has an entry for it
    miss = []
    for d in reg['registry']['deferred_decisions']:
        rf = d.get('roadmap_file')
        try:
            body = open(rf, encoding='utf-8').read() if rf else ''
        except OSError:
            body = ''
        if not re.search(r'^## ' + re.escape(d['id']) + r'\. ', body, flags=re.M): miss.append(d['id'])
    check('every deferred decision has a roadmap entry with entry criteria', not miss, ', '.join(miss))

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)}/{len(results)} checks passed")
    sys.exit(1 if failed else 0)

if __name__ == '__main__':
    main()
