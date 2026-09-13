"""Exact binomial-quotient obstruction discovery on complete full-word fibres.

Every emitted constraint is checked through integer transport certificates and
guarded by complete fibre supports. Failure to find one leaves weight realization
open; no numerical search or Boolean assignment is promoted to a witness.
"""

from __future__ import annotations

import itertools
from collections import Counter, defaultdict
from dataclasses import dataclass

from krenn_gu.integer_signed_lattice import IntegerSignedLattice


def perfect_matchings(vertices):
    if not vertices:
        yield ()
        return
    for index in range(1, len(vertices)):
        for matching in perfect_matchings(vertices[1:index] + vertices[index + 1:]):
            yield ((vertices[0], vertices[index]), *matching)


@dataclass(frozen=True)
class FibreRelation:
    exponents: tuple[tuple[int, int], ...]
    word: tuple[int, ...]


class FullTensorCancellation:
    def __init__(self, instance):
        if instance.clause_counts["target"] != 3 ** instance.n:
            raise ValueError("full-word cancellation requires the GHZ target")
        self.instance = instance
        matchings = tuple(perfect_matchings(tuple(range(instance.n))))
        self.fibres = {
            word: tuple(tuple(sorted(instance.entry(u, v, word[u], word[v])
                                    for u, v in matching)) for matching in matchings)
            for word in itertools.product(range(3), repeat=instance.n)
        }

    def live_fibres(self, positive):
        return {word: tuple(term for term in terms if all(v in positive for v in term))
                for word, terms in self.fibres.items()}

    @staticmethod
    def difference(first, second):
        row = Counter(first)
        row.subtract(Counter(second))
        return tuple(sorted((v, power) for v, power in row.items() if power))

    def relations(self, live):
        found = {}
        for word, terms in live.items():
            if len(set(word)) == 1 or len(terms) != 2:
                continue
            row = self.difference(*terms)
            if row and row[0][1] < 0:
                row = tuple((v, -power) for v, power in row)
            found.setdefault(row, FibreRelation(row, word))
        return tuple(found.values())

    @staticmethod
    def verify_transport(relations, coefficients, target, sign):
        if len(relations) != len(coefficients) or sign not in (-1, 1):
            return False
        if any(type(value) is not int for value in coefficients):
            return False
        row = Counter()
        for relation, coefficient in zip(relations, coefficients, strict=True):
            for variable, power in relation.exponents:
                row[variable] += coefficient * power
        actual = tuple(sorted((v, power) for v, power in row.items() if power))
        return actual == target and (-1 if sum(coefficients) % 2 else 1) == sign

    def support_cut(self, positive, words):
        """Guard every live monomial and a chosen zero blocker for every dead one."""
        guards = set()
        for word in words:
            for monomial in self.fibres[word]:
                absent = [variable for variable in monomial if variable not in positive]
                if absent:
                    guards.add(-min(absent))
                else:
                    guards.update(monomial)
        if any(-literal in guards for literal in guards):
            raise AssertionError("inconsistent fibre guards")
        return tuple(sorted((-literal for literal in guards), key=lambda x: (abs(x), x)))

    def verify_certificate(self, model, certificate):
        """Re-derive complete fibres and replay the certificate without Smith form."""
        try:
            model_set = set(model)
            if 0 in model_set or any(-literal in model_set for literal in model_set):
                return False
            if not set(self.instance.entries.values()) <= {abs(lit) for lit in model_set}:
                return False
            positive = {literal for literal in model_set if literal > 0}
            live = self.live_fibres(positive)
            relations = []
            for item in certificate["relations"]:
                word = tuple(item["word"])
                if len(set(word)) == 1 or len(live[word]) != 2:
                    return False
                expected = self.difference(*live[word])
                if expected and expected[0][1] < 0:
                    expected = tuple((v, -power) for v, power in expected)
                if tuple(map(tuple, item["exponents"])) != expected:
                    return False
                relations.append(FibreRelation(expected, word))
            used_words = set()

            def replay(coefficients, target, sign):
                if not self.verify_transport(relations, coefficients, target, sign):
                    return False
                used_words.update(r.word for r, k in zip(relations, coefficients, strict=True) if k)
                return True

            kind = certificate["kind"]
            if kind == "odd_integer_kernel":
                if not replay(certificate["coefficients"], (), -1):
                    return False
            elif kind in ("quotient_singleton", "pure_vanishes"):
                word = tuple(certificate["word"])
                terms = tuple(map(tuple, certificate["terms"]))
                if terms != live[word] or (len(set(word)) == 1) != (kind == "pure_vanishes"):
                    return False
                used_words.add(word)
                if len(set(terms)) != len(terms):
                    return False
                from_terms = set()
                edges = []
                for transport in certificate["transports"]:
                    first, second = tuple(transport["from"]), tuple(transport["to"])
                    if first not in terms or second not in terms or first in from_terms or first == second:
                        return False
                    if not replay(transport["coefficients"], self.difference(first, second), transport["sign"]):
                        return False
                    from_terms.add(first)
                    edges.append((first, second, transport["sign"]))
                representatives = set(terms) - from_terms
                sums = {representative: 1 for representative in representatives}
                for _first, second, sign in edges:
                    if second not in representatives:
                        return False
                    sums[second] += sign
                recorded = {tuple(monomial): total for monomial, total in certificate["group_sums"]}
                if len(recorded) != len(certificate["group_sums"]) or sums != recorded:
                    return False
                if kind == "pure_vanishes" and any(sums.values()):
                    return False
                if kind == "quotient_singleton" and sum(value != 0 for value in sums.values()) != 1:
                    return False
            else:
                return False
            if sorted(used_words) != list(map(tuple, certificate["guarded_words"])):
                return False
            return self.support_cut(positive, used_words) == tuple(certificate["cut"])
        except (KeyError, TypeError, ValueError, IndexError):
            return False

    def find_obstruction(self, model, *, max_relations=768, max_variables=256):
        """Return a directly replayed certificate and its guarded cut, or None.

        Dense Smith form is explicitly bounded. A limit raises ValueError; None
        means only this quotient test found no contradiction on the support.
        """
        model = tuple(model)
        model_set = set(model)
        if 0 in model_set or any(-literal in model_set for literal in model_set):
            raise ValueError("invalid Boolean assignment")
        positive = {literal for literal in model_set if literal > 0}
        if not set(self.instance.entries.values()) <= {abs(lit) for lit in model}:
            raise ValueError("incomplete physical support assignment")
        live = self.live_fibres(positive)
        relations = self.relations(live)
        if not relations:
            return None
        variables = sorted({v for relation in relations for v, _ in relation.exponents}
                           | {v for terms in live.values() for term in terms for v in term})
        if len(relations) > max_relations or len(variables) > max_variables:
            raise ValueError("full-fibre quotient exceeds explicit Smith bounds")
        rows = [[dict(relation.exponents).get(v, 0) for v in variables] for relation in relations]
        lattice = IntegerSignedLattice(rows)

        if lattice.has_inconsistent_kernel:
            vector = next(k for k in lattice.kernel_basis if sum(k) % 2)
            if not self.verify_transport(relations, vector, (), -1):
                raise AssertionError("integer kernel replay failed")
            words = {r.word for r, k in zip(relations, vector, strict=True) if k}
            certificate = {"kind": "odd_integer_kernel", "coefficients": vector}
        else:
            cache = {}

            def signature(monomial):
                if monomial not in cache:
                    counts = Counter(monomial)
                    cache[monomial] = lattice.signed_quotient_signature(
                        [counts[v] for v in variables])
                return cache[monomial]

            certificate = None
            words = set()
            for word, terms in live.items():
                groups = defaultdict(list)
                for monomial in terms:
                    key, sign = signature(monomial)
                    groups[key].append((monomial, sign))
                remaining = [group for group in groups.values() if sum(sign for _, sign in group)]
                pure = len(set(word)) == 1
                if not ((pure and not remaining) or (not pure and len(remaining) == 1)):
                    continue
                transports = []
                sums = []
                words.add(word)
                for group in groups.values():
                    representative, base_sign = group[0]
                    subtotal = 1
                    for monomial, sign in group[1:]:
                        difference = self.difference(monomial, representative)
                        dense = dict(difference)
                        vector = lattice.coordinates([dense.get(v, 0) for v in variables])
                        relative = sign * base_sign
                        if vector is None or not self.verify_transport(
                            relations, vector, difference, relative
                        ):
                            raise AssertionError("quotient transport failed exact replay")
                        subtotal += relative
                        words.update(r.word for r, k in zip(relations, vector, strict=True) if k)
                        transports.append({"from": monomial, "to": representative,
                                           "sign": relative, "coefficients": tuple(vector)})
                    sums.append((representative, subtotal))
                if pure:
                    assert all(total == 0 for _, total in sums)
                else:
                    assert sum(total != 0 for _, total in sums) == 1
                certificate = {"kind": "quotient_singleton" if not pure else "pure_vanishes",
                               "word": word, "terms": terms,
                               "transports": transports, "group_sums": sums}
                break
            if certificate is None:
                return None

        cut = self.support_cut(positive, words)
        if any((literal > 0) == (abs(literal) in positive) for literal in cut):
            raise AssertionError("cut does not exclude the originating support")
        vectors = ([certificate["coefficients"]] if certificate["kind"] == "odd_integer_kernel"
                   else [item["coefficients"] for item in certificate["transports"]])
        used = [i for i in range(len(relations)) if any(vector[i] for vector in vectors)]
        if certificate["kind"] == "odd_integer_kernel":
            certificate["coefficients"] = tuple(certificate["coefficients"][i] for i in used)
        else:
            for item in certificate["transports"]:
                item["coefficients"] = tuple(item["coefficients"][i] for i in used)
        certificate.update(relations=[{"exponents": relations[i].exponents, "word": relations[i].word}
                                      for i in used],
                           guarded_words=sorted(words), cut=cut,
                           checked_integer_transport=True)
        if not self.verify_certificate(model, certificate):
            raise AssertionError("standalone certificate replay failed")
        return certificate
