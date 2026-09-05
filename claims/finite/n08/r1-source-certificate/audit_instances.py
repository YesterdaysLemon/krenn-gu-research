"""Independent semantic audit of the frozen n=8 r=1 certificate package.

No producer, generator, SAT solver, or third-party module is imported.
Matchings come from all 8! vertex orders; the fixed-matching stabilizer and
its orbits come from generator closure/BFS. Clauses are rebuilt from semantic
descriptors, not variable maps or claimed acceptance flags. Stable IDs use the
public wire order: unknown half-edges, allowed pure witnesses, allowed equality
witnesses, then first-encounter nonconstant memberships in core/word/PM order.
Clause order is deliberately irrelevant to the independent multiset comparison;
the raw DIMACS byte hash is checked separately against the frozen spec.

This checker validates the source-to-CNF bridge. It does NOT check DRAT proofs.
"""
from collections import Counter, deque
from copy import deepcopy
from hashlib import sha256
from itertools import combinations, permutations
from pathlib import Path
import argparse
import json
import re

SPEC_SHA256 = '34d3f3557e952d0c2d03c3b2f8fcb04c2f786400209f76e8e39a7dcbc9e31b8d'


class AuditError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise AuditError(message)


def integer(value):
    return type(value) is int


def canonical_matching(raw):
    require(isinstance(raw, list) and len(raw) == 4, 'matching must have four edges')
    edges = []
    for edge in raw:
        require(isinstance(edge, list) and len(edge) == 2, 'edge must have two endpoints')
        require(all(integer(v) and 0 <= v < 8 for v in edge), 'invalid endpoint')
        require(edge[0] != edge[1], 'loop in matching')
        edges.append(tuple(sorted(edge)))
    require(sorted(v for edge in edges for v in edge) == list(range(8)),
            'matching does not cover the eight vertices exactly once')
    return tuple(sorted(edges))


def transform(matching, permutation):
    return tuple(sorted(tuple(sorted((permutation[u], permutation[v])))
                        for u, v in matching))


def mathematical_domain():
    # Different from the producer's recursive least-vertex generator.
    matchings = sorted({tuple(sorted(tuple(sorted((order[i], order[i + 1])))
                                     for i in (0, 2, 4, 6)))
                        for order in permutations(range(8))})
    require(len(matchings) == 105, 'independent matching count')
    positions = {m: i for i, m in enumerate(matchings)}
    edges = tuple(combinations(range(8), 2))
    edge_number = {e: i for i, e in enumerate(edges)}
    masks = [sum(1 << edge_number[e] for e in m) for m in matchings]
    fixed = ((0, 1), (2, 3), (4, 5), (6, 7))
    require(matchings[0] == fixed, 'canonical colour-zero matching')
    allowed = [i for i, mask in enumerate(masks) if not mask & masks[0]]
    raw_pairs = {(i, j) for i in allowed for j in allowed if not masks[i] & masks[j]}
    require(len(allowed) == 60 and len(raw_pairs) == 1884, 'independent raw cover')

    generators = []
    for i in range(4):
        p = list(range(8))
        p[2 * i], p[2 * i + 1] = p[2 * i + 1], p[2 * i]
        generators.append(tuple(p))
    for i in range(3):
        p = list(range(8))
        for offset in (0, 1):
            a, b = 2 * i + offset, 2 * i + 2 + offset
            p[a], p[b] = p[b], p[a]
        generators.append(tuple(p))
    group = {tuple(range(8))}
    queue = deque(group)
    while queue:
        p = queue.popleft()
        for g in generators:
            image = tuple(g[p[v]] for v in range(8))
            if image not in group:
                group.add(image)
                queue.append(image)
    require(len(group) == 384, 'independent stabilizer order')
    require(all(transform(fixed, p) == fixed for p in group), 'stabilizer fixes M0')
    actions = [[positions[transform(m, g)] for m in matchings] for g in generators]
    unseen = set(raw_pairs)
    orbits = {}
    while unseen:
        representative = min(unseen)
        orbit = {representative}
        queue = deque([representative])
        while queue:
            a, b = queue.popleft()
            for action in actions:
                image = (action[a], action[b])
                require(image in raw_pairs, 'group action leaves raw cover')
                if image not in orbit:
                    orbit.add(image)
                    queue.append(image)
        require(orbit <= unseen, 'independent orbits overlap')
        orbits[representative] = orbit
        unseen -= orbit
    incidence = [tuple(int(e in m) for e in edges) for m in matchings]
    return {'matchings': matchings, 'positions': positions, 'edges': edges,
            'fixed': fixed, 'raw_pairs': raw_pairs, 'group': group, 'orbits': orbits,
            'incidence': incidence, 'allowed': allowed}


def validate_cover(cases, domain):
    require(isinstance(cases, list), 'cases must be a list')
    seen_ids, covered, sizes = set(), set(), []
    expected_representatives = sorted(domain['orbits'])
    for number, case in enumerate(cases):
        require(isinstance(case, dict), 'case object required')
        ident = case.get('id')
        require(isinstance(ident, str) and re.fullmatch(r'r1-scaffold-\d{3}', ident),
                'invalid case id')
        require(ident not in seen_ids, 'duplicate case id')
        seen_ids.add(ident)
        require(ident == f'r1-scaffold-{number:03d}', 'case ordering/id mismatch')
        raw = case.get('matchings')
        require(isinstance(raw, list) and len(raw) == 3, 'three selected matchings required')
        triple = tuple(canonical_matching(m) for m in raw)
        require(triple[0] == domain['fixed'], 'case does not fix M0')
        require(all(not set(triple[i]) & set(triple[j]) for i, j in combinations(range(3), 2)),
                'selected pure matchings overlap')
        pair = tuple(domain['positions'][m] for m in triple[1:])
        require(pair in domain['orbits'], 'case is not independently canonical')
        require(number < len(expected_representatives) and pair == expected_representatives[number],
                'canonical case order differs from independent orbit order')
        orbit = domain['orbits'][pair]
        require(not covered & orbit, 'scaffold orbit overlap')
        covered |= orbit
        stabilizer = sum(transform(triple[1], p) == triple[1]
                         and transform(triple[2], p) == triple[2]
                         for p in domain['group'])
        require(case.get('orbit_size') == len(orbit), 'wrong orbit size metadata')
        require(case.get('stabilizer_size') == stabilizer
                and stabilizer * len(orbit) == 384, 'wrong stabilizer size metadata')
        sizes.append(len(orbit))
    require(covered == domain['raw_pairs'], 'scaffold cover is not exhaustive')
    distribution = Counter(sum(i == a for a, _ in domain['raw_pairs']) for i in domain['allowed'])
    return {'all_perfect_matchings': len(domain['matchings']),
            'm2_count_per_m1_distribution': {str(k): v for k, v in sorted(distribution.items())},
            'matchings_disjoint_from_fixed_m0': len(domain['allowed']),
            'orbit_size_distribution': {str(k): v for k, v in sorted(Counter(sizes).items())},
            'ordered_disjoint_m1_m2_pairs_for_fixed_m0': len(domain['raw_pairs']),
            'ordered_three_disjoint_matchings_without_fixing_m0': 105 * len(domain['raw_pairs']),
            'representative_count': len(cases), 'stabilizer_group_order': len(domain['group'])}


def validate_core(core, domain):
    require(isinstance(core, dict), 'core object required')
    words, pairs, signs = (core.get(name) for name in ('words', 'pairs', 'signs'))
    require(all(isinstance(x, list) and len(x) == 3 for x in (words, pairs, signs)),
            'core must contain three words, pairs, and signs')
    require(all(isinstance(w, str) and len(w) == 8 and set(w) <= set('012')
                and len(set(w)) > 1 for w in words), 'core word is not a mixed ternary word')
    require(len(set(words)) == 3, 'core words are not distinct')
    require(all(integer(s) and s in (-1, 1) for s in signs), 'core signs must be integers +/-1')
    require(sum(signs) % 2 == 1, 'core coefficient sum is not odd')
    vectors = []
    for pair in pairs:
        require(isinstance(pair, list) and len(pair) == 2
                and all(integer(k) and 0 <= k < 105 for k in pair) and pair[0] != pair[1],
                'core pair must contain distinct matching ids')
        vectors.append(tuple(a - b for a, b in zip(domain['incidence'][pair[0]],
                                                  domain['incidence'][pair[1]])))
    total = [sum(s * v[e] for s, v in zip(signs, vectors)) for e in range(28)]
    require(total == [0] * 28, 'core integer exponent relation is nonzero')


def reconstruct_case(case, domain):
    """Allocate wire IDs, then independently construct semantic clause families."""
    fixed = {e: colour for colour, raw in enumerate(case['matchings'])
             for e in canonical_matching(raw)}
    names, identifiers = [], {}
    def allocate(descriptor):
        if descriptor not in identifiers:
            names.append(descriptor)
            identifiers[descriptor] = len(names)
        return identifiers[descriptor]
    for edge in domain['edges']:
        if edge not in fixed:
            for vertex in edge:
                for colour in range(3):
                    allocate(('half', edge, vertex, colour))
    words = []
    for matching in domain['matchings']:
        row = [None] * 8
        for edge in matching:
            for vertex in edge:
                row[vertex] = ('fixed', fixed[edge]) if edge in fixed else ('half', edge, vertex)
        words.append(row)
    for k, row in enumerate(words):
        for colour in range(3):
            if not any(x[0] == 'fixed' and x[1] != colour for x in row):
                allocate(('pure', k, colour))
    for k, l in combinations(range(105), 2):
        if not any(x[0] == y[0] == 'fixed' and x[1] != y[1]
                   for x, y in zip(words[k], words[l])):
            allocate(('equal', k, l))
    base_names = tuple(names)
    memberships, requirements = {}, {}
    def member(word, k):
        lookup = (word, k)
        if lookup in memberships:
            return memberships[lookup]
        literals = []
        for vertex, descriptor in enumerate(words[k]):
            colour = int(word[vertex])
            if descriptor[0] == 'fixed':
                if descriptor[1] != colour:
                    memberships[lookup] = False
                    return False
            else:
                literals.append(identifiers[('half', descriptor[1], descriptor[2], colour)])
        if not literals:
            memberships[lookup] = True
            return True
        variable = allocate(('member', word, k))
        memberships[lookup] = variable
        requirements[variable] = tuple(literals)
        return variable
    require(isinstance(case.get('cores'), list), 'case cores must be a list')
    learned = []
    for core in case['cores']:
        validate_core(core, domain)
        clause = set()
        for word, pair in zip(core['words'], core['pairs']):
            for k in range(105):
                value, expected = member(word, k), k in pair
                if type(value) is bool:
                    literal_value = (not value) if expected else value
                    require(not literal_value, 'frozen cut contains a constant-true literal')
                else:
                    clause.add(-value if expected else value)
        require(not any(-x in clause for x in clause), 'tautological frozen core clause')
        learned.append(tuple(sorted(clause)))

    # Clause construction is separate from allocation/producer append order.
    clauses = []
    for edge in domain['edges']:
        if edge in fixed:
            continue
        for vertex in edge:
            values = [identifiers[('half', edge, vertex, c)] for c in range(3)]
            clauses.append(tuple(values))
            clauses.extend((-a, -b) for a, b in combinations(values, 2))
    choices = [[] for _ in range(105)]
    for descriptor in base_names:
        kind, *args = descriptor
        variable = identifiers[descriptor]
        if kind == 'pure':
            k, colour = args
            choices[k].append(variable)
            for x in words[k]:
                if x[0] == 'half':
                    clauses.append((-variable, identifiers[('half', x[1], x[2], colour)]))
        elif kind == 'equal':
            k, l = args
            choices[k].append(variable)
            choices[l].append(variable)
            for x, y in zip(words[k], words[l]):
                if x == y:
                    continue
                if x[0] == 'fixed':
                    clauses.append((-variable, identifiers[('half', y[1], y[2], x[1])]))
                elif y[0] == 'fixed':
                    clauses.append((-variable, identifiers[('half', x[1], x[2], y[1])]))
                else:
                    for colour in range(3):
                        a = identifiers[('half', x[1], x[2], colour)]
                        b = identifiers[('half', y[1], y[2], colour)]
                        clauses.extend(((-variable, -a, b), (-variable, a, -b)))
    clauses.extend(tuple(x) for x in choices)
    reverse_indices = []
    for descriptor in names[len(base_names):]:
        require(descriptor[0] == 'member', 'unexpected extended descriptor')
        variable = identifiers[descriptor]
        req = requirements[variable]
        clauses.extend((-variable, lit) for lit in req)
        reverse_indices.append(len(clauses))
        clauses.append(tuple([variable] + [-lit for lit in req]))
    learned_indices = list(range(len(clauses), len(clauses) + len(learned)))
    clauses.extend(learned)
    # These are direct semantic constant checks, not spec-provided booleans.
    require(member('00000000', 0) is True and member('11111111', 0) is False,
            'fixed matching membership constants')
    return len(names), clauses, reverse_indices, learned_indices


def parse_dimacs(raw):
    try:
        text = raw.decode('ascii')
    except UnicodeDecodeError as exc:
        raise AuditError('DIMACS is not ASCII') from exc
    variables = count = None
    clauses, current = [], []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('c'):
            continue
        if line.startswith('p'):
            require(variables is None and not clauses and not current, 'duplicate/late DIMACS header')
            fields = line.split()
            require(len(fields) == 4 and fields[:2] == ['p', 'cnf'], 'invalid DIMACS header')
            try:
                variables, count = map(int, fields[2:])
            except ValueError as exc:
                raise AuditError('noninteger DIMACS header') from exc
            require(variables >= 0 and count >= 0, 'negative DIMACS dimensions')
            continue
        require(variables is not None, 'DIMACS data precedes header')
        try:
            numbers = list(map(int, line.split()))
        except ValueError as exc:
            raise AuditError('noninteger DIMACS literal') from exc
        for literal in numbers:
            if literal == 0:
                clauses.append(tuple(current))
                current = []
            else:
                require(abs(literal) <= variables, 'out-of-range DIMACS literal')
                current.append(literal)
    require(variables is not None and not current, 'missing header or unterminated DIMACS clause')
    require(len(clauses) == count, 'DIMACS header clause count mismatch')
    return variables, clauses


def compare_clauses(actual_variables, actual_clauses, expected_variables, expected_clauses):
    require(actual_variables == expected_variables, 'semantic variable count mismatch')
    require(len(actual_clauses) == len(expected_clauses), 'semantic clause count mismatch')
    require(Counter(tuple(sorted(c)) for c in actual_clauses)
            == Counter(tuple(sorted(c)) for c in expected_clauses), 'semantic clause multiset mismatch')


def self_tests(spec, domain):
    """Mutations invoke semantic validators directly, bypassing raw hash checks."""
    results = []
    def reject(label, action, fragment):
        try:
            action()
        except AuditError as exc:
            require(fragment in str(exc), label + ' rejected for wrong reason: ' + str(exc))
            results.append({'control': label, 'rejected': True})
        else:
            raise AuditError(label + ' was incorrectly accepted')
    example = next(case for case in spec['cases'] if case['cores'])
    core = example['cores'][0]
    validate_core(core, domain)
    results.append({'control': 'valid integer core', 'accepted': True})
    bad = deepcopy(core)
    bad['signs'][0] *= -1
    reject('changed core sign', lambda: validate_core(bad, domain), 'integer exponent')
    badword = deepcopy(core)
    badword['words'][0] = '00000000'
    reject('pure word used as zero target', lambda: validate_core(badword, domain), 'mixed ternary')
    badpair = deepcopy(core)
    badpair['pairs'][0][1] = badpair['pairs'][0][0]
    reject('repeated matching in binomial', lambda: validate_core(badpair, domain), 'distinct matching')
    reject('missing final scaffold orbit', lambda: validate_cover(spec['cases'][:-1], domain),
           'not exhaustive')
    nv, expected, backwards, cuts = reconstruct_case(example, domain)
    compare_clauses(nv, expected, nv, expected)
    results.append({'control': 'valid clause multiset and fixed membership constants', 'accepted': True})
    require(backwards, 'self-test needs a nonconstant membership')
    missing_iff = list(expected)
    missing_iff[backwards[0]] = expected[0]  # Keep dimensions valid while losing reverse implication.
    reject('missing membership reverse implication',
           lambda: compare_clauses(nv, missing_iff, nv, expected), 'multiset')
    repair_index = next(i for i in cuts if any(x > 0 for x in expected[i]))
    dropped_repair = list(expected)
    clause = list(dropped_repair[repair_index])
    clause.remove(next(x for x in clause if x > 0))
    dropped_repair[repair_index] = tuple(clause)
    reject('omitted possible extra matching from exact-fibre cut',
           lambda: compare_clauses(nv, dropped_repair, nv, expected), 'multiset')
    reject('incorrect variable header', lambda: compare_clauses(nv + 1, expected, nv, expected),
           'variable count')
    reject('unterminated DIMACS clause', lambda: parse_dimacs(b'p cnf 1 1\n1\n'), 'unterminated')
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', '--spec', dest='certificate', type=Path,
                        default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--instance-dir', type=Path)
    parser.add_argument('--self-test-only', action='store_true')
    args = parser.parse_args()
    require(args.instance_dir is not None or args.self_test_only, '--instance-dir is required')
    raw = args.certificate.read_bytes()
    digest = sha256(raw).hexdigest()
    require(digest == SPEC_SHA256, 'frozen certificate.json hash mismatch')
    spec = json.loads(raw)
    require(spec.get('schema_version') == 1 and spec.get('n') == 8 and spec.get('colours') == 3,
            'unsupported mathematical dimensions/schema')
    domain = mathematical_domain()
    require(canonical_matching(spec.get('fixed_matching')) == domain['fixed'], 'fixed matching mismatch')
    counts = validate_cover(spec.get('cases'), domain)
    require(counts == spec.get('cover_counts'), 'cover metadata differs from independent counts')
    cases = []
    core_count = 0
    for case in spec['cases']:
        nv, expected, _, _ = reconstruct_case(case, domain)
        core_count += len(case['cores'])
        frozen = case.get('cnf')
        require(isinstance(frozen, dict) and frozen.get('variables') == nv
                and frozen.get('clauses') == len(expected), 'frozen CNF dimensions differ from reconstruction')
        if args.self_test_only:
            continue
        path = args.instance_dir / (case['id'] + '.cnf')
        data = path.read_bytes()
        require(len(data) == frozen.get('bytes'), 'CNF byte count mismatch: ' + case['id'])
        require(sha256(data).hexdigest() == frozen.get('sha256'), 'CNF raw hash mismatch: ' + case['id'])
        actual_nv, actual = parse_dimacs(data)
        compare_clauses(actual_nv, actual, nv, expected)
        cases.append({'id': case['id'], 'variables': nv, 'clauses': len(expected),
                      'cores': len(case['cores']), 'cnf_sha256': frozen['sha256']})
    require(core_count == 39, 'frozen algebraic core count')
    controls = self_tests(spec, domain)
    print(json.dumps({'status': 'PASS', 'certificate_sha256': digest,
                      'independent_cover': counts, 'integer_cores_checked': core_count,
                      'instances_checked': len(cases), 'self_tests': controls,
                      'scope': 'Independent source-to-CNF semantics only; DRAT proofs are NOT checked here.',
                      'producer_or_solver_imports': False, 'cases': cases}, indent=2))


if __name__ == '__main__':
    main()
