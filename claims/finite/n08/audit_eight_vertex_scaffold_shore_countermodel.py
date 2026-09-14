#!/usr/bin/env python3
"""Independent exact audits of two k=2 scaffold countermodel families.

This file intentionally imports no project scientific implementation.  It
reconstructs the 105 perfect matchings and evaluates the concrete physical
array over the Laurent ring

    Z[r_01^+-1, r_02^+-1, r_10^+-1, r_12^+-1, r_20^+-1, r_21^+-1].

In X_cd the first listed support entry has weight r_cd and the second has
weight -r_cd^-1.  Thus r_cd=i gives the reported all-i array, while r_cd=1
gives a rational array with weights 1 and -1.  Empty residual polynomials
verify identities simultaneously for every nonzero parameter choice.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path


N = 8
COLOURS = tuple(range(3))
LEFT = tuple(range(4))
RIGHT = tuple(range(4, 8))
MATCHINGS = (
    ((0, 1), (2, 3)),
    ((0, 2), (1, 3)),
    ((0, 3), (1, 2)),
)
SHORE_SUPPORTS = {
    (0, 1): ((0, 0), (1, 2)),
    (0, 2): ((2, 0), (3, 3)),
    (1, 0): ((0, 0), (2, 1)),
    (1, 2): ((1, 1), (3, 2)),
    (2, 0): ((0, 2), (3, 3)),
    (2, 1): ((1, 1), (2, 3)),
}
BINARY_SHORE_SUPPORTS = {
    (0, 1): ((2, 3), (3, 1)),
    (0, 2): ((0, 3), (1, 0)),
    (1, 0): ((1, 2), (3, 3)),
    (1, 2): ((0, 2), (2, 1)),
    (2, 0): ((1, 1), (2, 0)),
    (2, 1): ((0, 0), (3, 2)),
}
MINORITY_COMPONENT_SUPPORTS = {
    (0, 1): ((2, 3), (3, 1)),
    (0, 2): ((0, 3), (1, 0)),
    (1, 0): ((1, 1), (3, 0)),
    (1, 2): ((0, 2), (2, 1)),
    (2, 0): ((1, 3), (2, 2)),
    (2, 1): ((0, 0), (3, 2)),
}
FAMILIES = {
    "monochromatic_shores_v1": SHORE_SUPPORTS,
    "binary_and_monochromatic_shores_v2": BINARY_SHORE_SUPPORTS,
    "independent_minorities_and_component_constants_v3": MINORITY_COMPONENT_SUPPORTS,
}
VARIABLES = tuple(SHORE_SUPPORTS)
VARIABLE_INDEX = {variable: index for index, variable in enumerate(VARIABLES)}
ZERO_EXPONENT = (0,) * len(VARIABLES)
Exponent = tuple[int, ...]
LaurentPolynomial = dict[Exponent, int]
Gaussian = tuple[int, int]


@lru_cache(maxsize=None)
def perfect_matchings(vertices: tuple[int, ...]):
    if not vertices:
        return ((),)
    first = vertices[0]
    output = []
    for position, second in enumerate(vertices[1:], start=1):
        remainder = vertices[1:position] + vertices[position + 1 :]
        for tail in perfect_matchings(remainder):
            output.append(((first, second), *tail))
    return tuple(output)


PERFECT_MATCHINGS = perfect_matchings(tuple(range(N)))


def matching_edges(colour: int) -> set[tuple[int, int]]:
    return {tuple(sorted(edge)) for edge in MATCHINGS[colour]}


def monomial(coefficient: int, variable: tuple[int, int] | None = None, power: int = 0):
    if not coefficient:
        return None
    exponent = [0] * len(VARIABLES)
    if variable is not None:
        exponent[VARIABLE_INDEX[variable]] = power
    return coefficient, tuple(exponent)


def edge_monomial(u: int, v: int, a: int, b: int, supports):
    if (u in LEFT) == (v in LEFT):
        if a != b:
            return None
        local_u = u if u in LEFT else u - 4
        local_v = v if v in LEFT else v - 4
        if tuple(sorted((local_u, local_v))) not in matching_edges(a):
            return None
        return monomial(1)
    if u in RIGHT:
        u, v, a, b = v, u, b, a
    if a == b:
        return None
    support = supports.get((a, b))
    if support is None:
        return None
    position = (u, v - 4)
    if position == support[0]:
        return monomial(1, (a, b), 1)
    if position == support[1]:
        return monomial(-1, (a, b), -1)
    return None


def matching_monomial(word: tuple[int, ...], matching, supports):
    coefficient = 1
    exponent = [0] * len(VARIABLES)
    for u, v in matching:
        edge = edge_monomial(u, v, word[u], word[v], supports)
        if edge is None:
            return None
        edge_coefficient, edge_exponent = edge
        coefficient *= edge_coefficient
        exponent = [left + right for left, right in zip(exponent, edge_exponent, strict=True)]
    return coefficient, tuple(exponent)


def amplitude(word: tuple[int, ...], supports) -> LaurentPolynomial:
    output: LaurentPolynomial = {}
    for matching in PERFECT_MATCHINGS:
        term = matching_monomial(word, matching, supports)
        if term is None:
            continue
        coefficient, exponent = term
        output[exponent] = output.get(exponent, 0) + coefficient
        if output[exponent] == 0:
            del output[exponent]
    return output


def target(word: tuple[int, ...]) -> LaurentPolynomial:
    return ({ZERO_EXPONENT: 1} if len(set(word)) == 1 else {})


def residual(word: tuple[int, ...], supports) -> LaurentPolynomial:
    output = dict(amplitude(word, supports))
    for exponent, coefficient in target(word).items():
        output[exponent] = output.get(exponent, 0) - coefficient
        if output[exponent] == 0:
            del output[exponent]
    return output


def gaussian_add(left: Gaussian, right: Gaussian) -> Gaussian:
    return left[0] + right[0], left[1] + right[1]


def gaussian_power_i(power: int) -> Gaussian:
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[power % 4]


def evaluate_all_i(poly: LaurentPolynomial) -> Gaussian:
    output = (0, 0)
    for exponent, coefficient in poly.items():
        value = gaussian_power_i(sum(exponent))
        output = gaussian_add(output, (coefficient * value[0], coefficient * value[1]))
    return output


def evaluate_all_one(poly: LaurentPolynomial) -> int:
    return sum(poly.values())


def polynomial_json(poly: LaurentPolynomial):
    return [
        {"coefficient": coefficient, "exponents": list(exponent)}
        for exponent, coefficient in sorted(poly.items())
    ]


def composition(word: tuple[int, ...]) -> tuple[int, int, int]:
    counts = Counter(word)
    return tuple(counts[colour] for colour in COLOURS)


def explicit_weights(specialization: str, supports):
    entries = []
    for shore_offset in (0, 4):
        for colour, matching in enumerate(MATCHINGS):
            for u, v in matching:
                entries.append(
                    {
                        "vertices": [u + shore_offset, v + shore_offset],
                        "colours": [colour, colour],
                        "value": [1, 0],
                    }
                )
    for variable, support in supports.items():
        values = ((0, 1), (0, 1)) if specialization == "all_i" else ((1, 0), (-1, 0))
        for (left, right), value in zip(support, values, strict=True):
            entries.append(
                {
                    "vertices": [left, right + 4],
                    "colours": list(variable),
                    "value": list(value),
                }
            )
    return sorted(entries, key=lambda item: (item["vertices"], item["colours"]))


def active_matching_records(word: tuple[int, ...], supports):
    records = []
    for matching in PERFECT_MATCHINGS:
        term = matching_monomial(word, matching, supports)
        if term is None:
            continue
        records.append(
            {
                "matching": [list(edge) for edge in matching],
                "coefficient": term[0],
                "exponents": list(term[1]),
                "all_i_value": list(evaluate_all_i({term[1]: term[0]})),
                "all_one_value": term[0],
            }
        )
    return records


def residual_digest(records) -> str:
    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def hist(records, ordered: bool):
    histogram = Counter()
    for record in records:
        key = tuple(record["composition"])
        if not ordered:
            key = tuple(sorted(key, reverse=True))
        histogram[",".join(map(str, key))] += 1
    return dict(sorted(histogram.items()))


def unique_residuals(records):
    grouped = {}
    for record in records:
        key = json.dumps(record["residual"], sort_keys=True, separators=(",", ":"))
        group = grouped.setdefault(
            key,
            {"residual": record["residual"], "count": 0, "words": []},
        )
        group["count"] += 1
        group["words"].append(record["word"])
    return [grouped[key] for key in sorted(grouped)]


def run_family(name: str, supports) -> dict[str, object]:
    all_r_errors = []
    all_i_errors = []
    all_one_errors = []
    shore_count = 0
    shore_all_r_failures = []
    binary_pair_counts = {pair: 0 for pair in itertools.combinations(COLOURS, 2)}
    binary_pair_failures = {pair: [] for pair in binary_pair_counts}
    independent_minority_indexed_count = 0
    independent_minority_indexed_failures = []
    independent_minority_distinct_count = 0
    component_constant_count = 0
    component_constant_failures = []
    selected_count = 0
    selected_failures = []
    count_at_least_four = 0
    at_least_four_all_r_failures = []
    for word in itertools.product(COLOURS, repeat=N):
        poly = residual(word, supports)
        word_text = "".join(map(str, word))
        word_composition = composition(word)
        record = {
            "word": word_text,
            "composition": list(word_composition),
            "residual": polynomial_json(poly),
        }
        if poly:
            all_r_errors.append(record)
        all_i_value = evaluate_all_i(poly)
        if all_i_value != (0, 0):
            all_i_errors.append(
                {
                    "word": word_text,
                    "composition": list(word_composition),
                    "residual": list(all_i_value),
                }
            )
        all_one_value = evaluate_all_one(poly)
        if all_one_value:
            all_one_errors.append(
                {
                    "word": word_text,
                    "composition": list(word_composition),
                    "residual": all_one_value,
                }
            )

        is_shore = len(set(word[:4])) == 1 or len(set(word[4:])) == 1
        if is_shore:
            shore_count += 1
            if poly:
                shore_all_r_failures.append(record)
        for pair in binary_pair_counts:
            if set(word) <= set(pair):
                binary_pair_counts[pair] += 1
                if poly:
                    binary_pair_failures[pair].append(record)
        is_binary = len(set(word)) <= 2
        admissible_majorities = []
        for majority in COLOURS:
            partner = (1, 2, 3)[majority]
            if all(
                word[u] == majority or word[u ^ partner] == majority
                for u in range(N)
                if u < (u ^ partner)
            ):
                admissible_majorities.append(majority)
        if admissible_majorities:
            independent_minority_distinct_count += 1
            independent_minority_indexed_count += len(admissible_majorities)
            if poly:
                independent_minority_indexed_failures.extend(
                    {"majority": majority, **record} for majority in admissible_majorities
                )
        is_component_constant = len(set(word[:4])) == 1 and len(set(word[4:])) == 1
        if is_component_constant:
            component_constant_count += 1
            if poly:
                component_constant_failures.append(record)
        if name == "binary_and_monochromatic_shores_v2":
            is_selected = is_shore or is_binary
        elif name == "independent_minorities_and_component_constants_v3":
            is_selected = bool(admissible_majorities) or is_component_constant
        else:
            is_selected = is_shore
        if is_selected:
            selected_count += 1
            if poly:
                selected_failures.append(record)
        if max(word_composition) >= 4:
            count_at_least_four += 1
            if poly:
                at_least_four_all_r_failures.append(record)

    if shore_count != 477:
        raise AssertionError(f"monochromatic-shore union has {shore_count} words")
    if shore_all_r_failures:
        raise AssertionError("the claimed MS countermodel fails a shore equation")
    expected_selected_count = {
        "monochromatic_shores_v1": 477,
        "binary_and_monochromatic_shores_v2": 1065,
        "independent_minorities_and_component_constants_v3": 1869,
    }[name]
    if selected_count != expected_selected_count:
        raise AssertionError(f"{name} selected union has {selected_count} words")
    if selected_failures:
        raise AssertionError(f"{name} fails a selected equation")
    if name == "binary_and_monochromatic_shores_v2":
        if any(count != 256 for count in binary_pair_counts.values()):
            raise AssertionError("each binary restriction must contain 256 words")
        if any(binary_pair_failures.values()):
            raise AssertionError("the second family fails a binary equation")
        if len(all_r_errors) != 29 or len(all_one_errors) != 29:
            raise AssertionError("the reported 29 full-word errors were not reconstructed")
        if any(len(set(record["word"])) != 3 for record in all_r_errors):
            raise AssertionError("a second-family error omits one of the three colours")
    elif name == "independent_minorities_and_component_constants_v3":
        if independent_minority_indexed_count != 1875:
            raise AssertionError("the indexed independent-minority count is not 1875")
        if independent_minority_distinct_count != 1863:
            raise AssertionError("the distinct independent-minority count is not 1863")
        if independent_minority_indexed_failures:
            raise AssertionError("the third family fails an independent-minority equation")
        if component_constant_count != 9 or component_constant_failures:
            raise AssertionError("the third family fails a component-constant equation")
        if not all_r_errors:
            raise AssertionError("apparent full GHZ witness requires escalation")
    elif len(all_r_errors) != 27:
        raise AssertionError("the reported 27 first-family errors were not reconstructed")

    if name != "independent_minorities_and_component_constants_v3":
        if [record["word"] for record in all_r_errors] != [
            record["word"] for record in all_i_errors
        ] or [record["word"] for record in all_r_errors] != [
            record["word"] for record in all_one_errors
        ]:
            raise AssertionError("a specialization unexpectedly changes the error support")

    if name == "monochromatic_shores_v1":
        reported_words = ("00012121",)
    elif name == "binary_and_monochromatic_shores_v2":
        reported_words = ("00020011", "01000002")
    else:
        reported_words = (all_r_errors[0]["word"],)
    reported_errors = []
    for word_text in reported_words:
        word = tuple(map(int, word_text))
        poly = amplitude(word, supports)
        records = active_matching_records(word, supports)
        reported_errors.append(
            {
                "word": word_text,
                "target": [0, 0],
                "laurent_amplitude": polynomial_json(poly),
                "all_i_amplitude": list(evaluate_all_i(poly)),
                "all_one_amplitude": evaluate_all_one(poly),
                "active_matching_count": len(records),
                "active_matchings": records,
            }
        )
    if name == "monochromatic_shores_v1":
        if reported_errors[0]["active_matching_count"] != 1:
            raise AssertionError("the first-family singleton was not reconstructed")
        if reported_errors[0]["all_i_amplitude"] != [-1, 0]:
            raise AssertionError("the first-family all-i singleton has the wrong value")
    elif name == "binary_and_monochromatic_shores_v2":
        if [record["all_one_amplitude"] for record in reported_errors] != [-1, 1]:
            raise AssertionError("the reported second-family rational errors have wrong values")
    else:
        if reported_errors[0]["active_matching_count"] != 1:
            raise AssertionError("the third-family singleton was not reconstructed")

    return {
        "name": name,
        "cross_supports": {
            f"X_{left}{right}": [list(position) for position in supports[(left, right)]]
            for left, right in VARIABLES
        },
        "support_entries_sorted": all(
            tuple(sorted(support)) == support for support in supports.values()
        ),
        "all_r_nonzero_parameter_family": {
            "weight_rule": "first support=r_cd; second support=-r_cd^-1",
            "monochromatic_shore_words_checked": shore_count,
            "monochromatic_shore_failures": len(shore_all_r_failures),
            "binary_pair_checks": {
                f"{left}{right}": {
                    "words_checked": binary_pair_counts[(left, right)],
                    "failures": len(binary_pair_failures[(left, right)]),
                }
                for left, right in binary_pair_counts
            },
            "independent_minority_checks": {
                "indexed_evaluations": independent_minority_indexed_count,
                "distinct_words": independent_minority_distinct_count,
                "indexed_failures": len(independent_minority_indexed_failures),
            },
            "component_constant_checks": {
                "words_checked": component_constant_count,
                "failures": len(component_constant_failures),
            },
            "selected_union_definition": (
                "word uses at most two colours or is constant on either four-vertex shore"
                if name == "binary_and_monochromatic_shores_v2"
                else (
                    "word is an independent-minority word for some majority colour or is "
                    "constant on each four-vertex component"
                    if name == "independent_minorities_and_component_constants_v3"
                    else "word is constant on either four-vertex shore"
                )
            ),
            "selected_union_words_checked": selected_count,
            "selected_union_failures": len(selected_failures),
            "words_with_some_colour_count_at_least_four": count_at_least_four,
            "such_word_failures": len(at_least_four_all_r_failures),
            "full_target_words_checked": 3**N,
            "full_target_error_count": len(all_r_errors),
            "all_errors_use_all_three_colours": all(
                len(set(record["word"])) == 3 for record in all_r_errors
            ),
            "full_target_error_histogram_ordered_composition": hist(all_r_errors, True),
            "full_target_error_histogram_unordered_composition": hist(all_r_errors, False),
            "residual_term_count_histogram": dict(
                sorted(Counter(len(record["residual"]) for record in all_r_errors).items())
            ),
            "unique_laurent_residual_count": len(unique_residuals(all_r_errors)),
            "unique_laurent_residuals": unique_residuals(all_r_errors),
            "full_target_errors_sha256": residual_digest(all_r_errors),
            "full_target_errors": all_r_errors,
        },
        "all_i_specialization": {
            "explicit_nonzero_W_entries": explicit_weights("all_i", supports),
            "full_target_error_count": len(all_i_errors),
            "error_histogram_ordered_composition": hist(all_i_errors, True),
            "error_histogram_unordered_composition": hist(all_i_errors, False),
            "errors_sha256": residual_digest(all_i_errors),
            "errors": all_i_errors,
        },
        "rational_all_one_specialization": {
            "explicit_nonzero_W_entries": explicit_weights("all_one", supports),
            "full_target_error_count": len(all_one_errors),
            "error_histogram_ordered_composition": hist(all_one_errors, True),
            "error_histogram_unordered_composition": hist(all_one_errors, False),
            "errors_sha256": residual_digest(all_one_errors),
            "errors": all_one_errors,
        },
        "reported_explicit_errors": reported_errors,
    }


def run_audit() -> dict[str, object]:
    started = time.monotonic()
    if len(PERFECT_MATCHINGS) != 105:
        raise AssertionError("eight vertices must have 105 perfect matchings")
    family_results = {
        name: run_family(name, supports) for name, supports in FAMILIES.items()
    }
    return {
        "schema": "n8-scaffold-countermodel-independent-audit-v3",
        "status": "PASS",
        "scope": {
            "n": N,
            "coefficient_ring": "six-variable integer Laurent ring",
            "primary_scientific_imports": False,
            "full_target_status": "NO_FAMILY_IS_A_FULL_GHZ_WITNESS",
            "global_krenn_gu_status_changed": False,
        },
        "lineage": {
            "predecessor_schema": "n8-scaffold-shore-countermodel-independent-audit-v1",
            "predecessor_family": "monochromatic_shores_v1",
            "second_family": "binary_and_monochromatic_shores_v2",
            "third_family": "independent_minorities_and_component_constants_v3",
        },
        "variables": [f"r_{left}{right}" for left, right in VARIABLES],
        "families": family_results,
        "interpretation": (
            "The Laurent calculations give exact six-parameter countermodels to "
            "their named selected subsystems. The explicitly listed remaining "
            "full-word residuals show that none of the families is a Krenn-Gu "
            "counterexample."
        ),
        "elapsed_seconds": time.monotonic() - started,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_audit()
    payload = json.dumps(result, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8", newline="\n")
    print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
