#!/usr/bin/env python3
"""Regenerate frozen n=8 matrix-unit source CNFs with the Python stdlib.

This is a deterministic generator, not a search or a DRAT checker. It checks
every stored odd integer relation and each generated CNF's exact byte/count
pins. Cover completeness and DRAT acceptance are separate verification steps.
DIMACS output always uses explicit ASCII CRLF bytes on every platform.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    u = vertices[0]
    for v in vertices[1:]:
        for rest in perfect_matchings(tuple(x for x in vertices if x not in (u, v))):
            yield ((u, v),) + rest


MATCHINGS = list(perfect_matchings(tuple(range(8))))
EDGES = list(itertools.combinations(range(8), 2))
INCIDENCE = [tuple(int(edge in matching) for edge in EDGES) for matching in MATCHINGS]


class VariablePool:
    def __init__(self):
        self.by_name = {}
        self.names = []

    def id(self, name):
        if name not in self.by_name:
            self.names.append(name)
            self.by_name[name] = len(self.names)
        return self.by_name[name]

    @property
    def top(self):
        return len(self.names)


def validate_core(core):
    words, pairs, signs = core['words'], core['pairs'], core['signs']
    require(len(words) == len(pairs) == len(signs) == 3, 'A core must have three fibres')
    require(all(isinstance(w, str) and re.fullmatch(r'[012]{8}', w) and len(set(w)) > 1
                for w in words), 'Core words must be mixed ternary words of length eight')
    require(len(set(words)) == 3, 'Core words must be distinct')
    for pair in pairs:
        require(len(pair) == 2 and all(type(k) is int and 0 <= k < 105 for k in pair)
                and pair[0] != pair[1], 'Core pair must name two distinct matching indices')
    require(all(type(s) is int and s in (-1, 1) for s in signs), 'Invalid core signs')
    require(sum(signs) % 2 == 1, 'Core relation must have odd sign sum')
    total = [sum(s * (INCIDENCE[pair[0]][e] - INCIDENCE[pair[1]][e])
                 for s, pair in zip(signs, pairs)) for e in range(28)]
    require(total == [0] * 28, 'Core does not have the claimed integer exponent relation')


def generate_case(case):
    """Preserve frozen base, membership-definition, and learned-clause order."""
    fixed = {}
    require(len(case['matchings']) == 3, 'Three scaffold matchings are required')
    for colour, matching in enumerate(case['matchings']):
        require(len(matching) == 4 and all(len(edge) == 2 for edge in matching)
                and sorted(v for edge in matching for v in edge) == list(range(8)),
                'Scaffold is not a perfect matching')
        for edge in matching:
            require(all(type(v) is int for v in edge), 'Scaffold vertices must be integers')
            edge = tuple(sorted(edge))
            require(edge not in fixed, 'Scaffold matchings must be edge-disjoint')
            fixed[edge] = colour
    require(len(fixed) == 12, 'Scaffold must have twelve fixed edges')
    pool, clauses, half = VariablePool(), [], {}
    for edge in EDGES:
        if edge in fixed:
            continue
        for vertex in edge:
            literals = [pool.id(('half', edge, vertex, colour)) for colour in range(3)]
            half[edge, vertex] = literals
            clauses.append(literals)
            clauses.extend([[-x, -y] for x, y in itertools.combinations(literals, 2)])
    words = []
    for matching in MATCHINGS:
        word = [None] * 8
        for edge in matching:
            for vertex in edge:
                word[vertex] = fixed[edge] if edge in fixed else half[edge, vertex]
        words.append(word)
    witnesses = [[] for _ in MATCHINGS]
    for k, word in enumerate(words):
        for colour in range(3):
            if any(isinstance(x, int) and x != colour for x in word):
                continue
            pure = pool.id(('pure', k, colour))
            witnesses[k].append(pure)
            for x in word:
                if not isinstance(x, int):
                    clauses.append([-pure, x[colour]])
    for k, ell in itertools.combinations(range(len(MATCHINGS)), 2):
        pair = list(zip(words[k], words[ell]))
        if any(isinstance(x, int) and isinstance(y, int) and x != y for x, y in pair):
            continue
        equal = pool.id(('equal', k, ell))
        witnesses[k].append(equal)
        witnesses[ell].append(equal)
        for x, y in pair:
            if x == y:
                continue
            if isinstance(x, int):
                clauses.append([-equal, y[x]])
            elif isinstance(y, int):
                clauses.append([-equal, x[y]])
            else:
                for a, b in zip(x, y):
                    clauses.extend([[-equal, -a, b], [-equal, a, -b]])
    clauses.extend(witnesses)

    membership = {}

    def member(word, k):
        key = (word, k)
        if key in membership:
            return membership[key]
        literals = []
        for edge in MATCHINGS[k]:
            for vertex in edge:
                colour = int(word[vertex])
                if edge in fixed:
                    if fixed[edge] != colour:
                        membership[key] = False
                        return False
                else:
                    literals.append(half[edge, vertex][colour])
        if not literals:
            membership[key] = True
            return True
        result = pool.id(('member', word, k))
        membership[key] = result
        for literal in literals:
            clauses.append([-result, literal])
        clauses.append([result] + [-literal for literal in literals])
        return result

    for core in case['cores']:
        validate_core(core)
        learned = []
        for word, pair in zip(core['words'], core['pairs']):
            for k in range(105):
                value = member(word, k)
                expected = k in pair
                if isinstance(value, bool):
                    term = (not value) if expected else value
                    require(not term, 'Pinned core clause is unexpectedly tautological')
                else:
                    learned.append(-value if expected else value)
        learned = sorted(set(learned), key=lambda x: (abs(x), x < 0))
        require(not any(-x in learned for x in learned), 'Pinned core clause has opposite literals')
        clauses.append(learned)
    return pool, clauses


def dimacs_bytes(pool, clauses):
    lines = [f'p cnf {pool.top} {len(clauses)}']
    lines.extend(' '.join(map(str, clause)) + ' 0' for clause in clauses)
    return ('\r\n'.join(lines) + '\r\n').encode('ascii')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path, default=Path(__file__).with_name('certificate.json'))
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--maps', action='store_true', help='Also write stable variable maps')
    args = parser.parse_args()
    raw = args.certificate.read_bytes()
    certificate = json.loads(raw)
    require(certificate.get('schema_version') == 1 and certificate.get('n') == 8
            and certificate.get('colours') == 3, 'Unsupported certificate schema or dimensions')
    cases = certificate['cases']
    require(len(cases) == 18, 'This certificate must contain all eighteen cases')
    ids = [case['id'] for case in cases]
    require(len(set(ids)) == 18 and all(re.fullmatch(r'r1-scaffold-\d{3}', ident) for ident in ids),
            'Invalid or duplicate case identifiers')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    generated = []
    for case in cases:
        pool, clauses = generate_case(case)
        data = dimacs_bytes(pool, clauses)
        actual = {'variables': pool.top, 'clauses': len(clauses), 'bytes': len(data),
                  'sha256': hashlib.sha256(data).hexdigest()}
        require(actual == case['cnf'], f'Frozen CNF mismatch for {case["id"]}: {actual}')
        path = args.output_dir / (case['id'] + '.cnf')
        path.write_bytes(data)
        if args.maps:
            mapping = {'scaffold': case['matchings'], 'perfect_matchings': MATCHINGS,
                       'variables': [{'id': k, 'meaning': name} for k, name in enumerate(pool.names, 1)]}
            path.with_suffix('.map.json').write_bytes((json.dumps(mapping, indent=2) + '\n').encode('utf-8'))
        generated.append({'id': case['id'], **actual})
    receipt = {'certificate_sha256': hashlib.sha256(raw).hexdigest(), 'cases': generated,
               'all_pins_match': True, 'core_count': sum(len(case['cores']) for case in cases),
               'solver_used': False, 'proofs_replayed': False}
    (args.output_dir / 'generation-receipt.json').write_bytes((json.dumps(receipt, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({'cases': len(generated), 'core_count': receipt['core_count'], 'all_pins_match': True,
                      'certificate_sha256': receipt['certificate_sha256']}))


if __name__ == '__main__':
    main()
