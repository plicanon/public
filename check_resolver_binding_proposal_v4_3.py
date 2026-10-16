#!/usr/bin/env python3
"""Runs the resolver binding PROPOSAL fixtures (rules R1 to R5). Not part of the approved rule set."""
import json, sys

def resolve(pinned, history, locations, observed):
    if not history:
        return ('no_artifact', None, None)
    if pinned:
        cand = [h for h in history if h['revision_id'] == pinned and h['status'] in ('available', 'superseded')]
    else:
        avail = [h for h in history if h['status'] == 'available']
        cand = [avail[-1]] if avail else []
    if not cand:
        return ('content_unavailable', None, None)
    rev = cand[0]
    order = {'primary': 0, 'mirror': 1, 'archive': 2}
    locs = sorted([l for l in locations if l['artifact_revision_id'] == rev['revision_id'] and l['status'] == 'active'],
                  key=lambda l: (order[l['tier']], l.get('priority', 0)))
    mismatch = False
    for l in locs:
        got = observed.get(l['id'])
        if got is None:
            continue
        if got == rev['digest']:
            return ('serve', rev['revision_id'], l['tier'])
        mismatch = True
    return ('integrity_failure' if mismatch else 'content_unavailable', None, None)

fx = json.load(open('plicanon_resolver_binding_fixtures_v4_3.json', encoding='utf-8'))
bad = []
for c in fx['cases']:
    got = list(resolve(c['pinned'], c['history'], c['locations'], c['observed']))
    ok = got == c['expected']
    print(('PASS ' if ok else 'FAIL ') + c['id'] + '  ' + c['label'])
    if not ok: bad.append(c['id'] + f": got {got}")
print(f"\n{len(fx['cases']) - len(bad)}/{len(fx['cases'])} binding fixtures passed (proposal, not approved rules)")
sys.exit(1 if bad else 0)
