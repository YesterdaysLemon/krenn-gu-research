"""Exact bounded probe for the GLS9 opposite-colour pure-Pi survivor.

The probe works with the complete six-slot contracted target equality (GLS9
equation (8)).  It deliberately relaxes the complementary permanents other
than ``Pi_Q`` to independent tensors.  Emptiness of this larger module model
therefore excludes every incidence-integrable contracted target point in the
two GLS9 support normal forms.

This is discovery code, not an independently audited theorem and not a global
Krenn--Gu resolution.  It also does not replace the maximum-root hypotheses
by the contracted incidence gates recorded below.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from itertools import permutations, product
from math import comb, prod

import sympy as sp

COLOURS = tuple(range(3))
ROOTS = tuple(range(4))
Q0, Q1 = 0, 1
PORTS = tuple(range(4))
OUTSIDE_POSITIONS = tuple(range(6))

Word = tuple[int, ...]


def tensor_symbols(prefix: str) -> dict[Word, sp.Symbol]:
    """Return one independent labelled four-slot ternary tensor."""

    return {
        word: sp.Symbol(f"{prefix}_{''.join(map(str, word))}")
        for word in product(COLOURS, repeat=4)
    }


@dataclass
class RelaxedContractedModel:
    """Full equation (8) after one GLS9 support-normal-form substitution."""

    normal_form: str
    i: int
    j: int
    k: int
    support: tuple[int, ...]
    coordinate_index: int
    second_coordinate_index: int | None
    h_matrix: sp.Matrix
    mu: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
    nu: sp.Symbol
    local_a: dict[int, tuple[sp.Expr, sp.Expr, sp.Expr]]
    local_c: dict[int, tuple[sp.Expr, sp.Expr, sp.Expr]]
    companions_a: dict[int, dict[Word, sp.Symbol]]
    companions_c: dict[int, dict[Word, sp.Symbol]]
    parameters: dict[str, sp.Expr]
    saturation_factors: tuple[sp.Expr, ...]

    def _complement_word(self, word: Word, excluded: tuple[int, int]) -> Word:
        return tuple(
            word[position] for position in OUTSIDE_POSITIONS if position not in excluded
        )

    def a_contribution(self, word: Word) -> sp.Expr:
        """Contribution from the q0-to-port edge family."""

        if word[Q0] != self.i:
            return sp.Integer(0)
        answer = sp.Integer(0)
        for port in self.support:
            port_position = 2 + port
            local = self.local_a[port][word[port_position]]
            complement = self._complement_word(word, (Q0, port_position))
            answer += local * self.companions_a[port][complement]
        return sp.expand(answer)

    def c_contribution(self, word: Word) -> sp.Expr:
        """Contribution from the q1-to-port edge family."""

        if word[Q1] != self.j:
            return sp.Integer(0)
        answer = sp.Integer(0)
        for port in self.support:
            port_position = 2 + port
            local = self.local_c[port][word[port_position]]
            complement = self._complement_word(word, (Q1, port_position))
            answer += local * self.companions_c[port][complement]
        return sp.expand(answer)

    def coefficient_equation(self, word: Word) -> sp.Expr:
        """Return LHS-RHS for the exact labelled coefficient of equation (8)."""

        answer = self.a_contribution(word) + self.c_contribution(word)
        if all(word[2 + port] == self.k for port in PORTS):
            answer += self.h_matrix[word[Q0], word[Q1]] * self.nu
        if len(set(word)) == 1:
            answer -= self.mu[word[0]]
        return sp.expand(answer)

    def full_equations(self) -> tuple[sp.Expr, ...]:
        """Materialize all 3^6=729 unprojected coefficient equations."""

        equations = tuple(
            self.coefficient_equation(word) for word in product(COLOURS, repeat=6)
        )
        assert len(equations) == 729
        return equations


def projected_h_matrix(
    i: int, j: int, k: int, prefix: str
) -> tuple[sp.Matrix, dict[str, sp.Symbol]]:
    """Parameterize the exact GLS9 projected-H full-rank normal form."""

    names = ("hii", "hij", "hik", "hjj", "hkj", "hkk")
    symbols = sp.symbols(" ".join(f"{prefix}_{name}" for name in names))
    parameters = dict(zip(names, symbols, strict=True))
    answer = sp.zeros(3)
    answer[i, i] = parameters["hii"]
    answer[i, j] = parameters["hij"]
    answer[i, k] = parameters["hik"]
    answer[j, j] = parameters["hjj"]
    answer[k, j] = parameters["hkj"]
    answer[k, k] = parameters["hkk"]
    assert sp.expand(answer.det()) == sp.expand(
        parameters["hii"] * parameters["hjj"] * parameters["hkk"]
    )
    return answer, parameters


def singleton_model(
    i: int,
    j: int,
    k: int,
    port: int,
    a: int,
    b: int,
    prefix: str,
) -> RelaxedContractedModel:
    """Build one exact singleton coordinate chart."""

    h_matrix, h_parameters = projected_h_matrix(i, j, k, prefix)
    alpha, beta, nu = sp.symbols(f"{prefix}_alpha {prefix}_beta {prefix}_nu")
    mu = sp.symbols(" ".join(f"{prefix}_mu{colour}" for colour in COLOURS))
    local_a = [sp.Integer(0)] * 3
    local_c = [sp.Integer(0)] * 3
    local_a[a] = alpha
    local_c[b] = beta
    companions_a = {port: tensor_symbols(f"{prefix}_A{port}")}
    companions_c = {port: tensor_symbols(f"{prefix}_C{port}")}
    saturation = (
        alpha,
        beta,
        nu,
        *mu,
        h_parameters["hii"],
        h_parameters["hjj"],
        h_parameters["hkk"],
    )
    return RelaxedContractedModel(
        normal_form="singleton",
        i=i,
        j=j,
        k=k,
        support=(port,),
        coordinate_index=a,
        second_coordinate_index=b,
        h_matrix=h_matrix,
        mu=mu,
        nu=nu,
        local_a={port: tuple(local_a)},
        local_c={port: tuple(local_c)},
        companions_a=companions_a,
        companions_c=companions_c,
        parameters={
            **h_parameters,
            "alpha": alpha,
            "beta": beta,
        },
        saturation_factors=saturation,
    )


def two_port_model(
    i: int,
    j: int,
    k: int,
    coordinate_port: int,
    other_port: int,
    a: int,
    prefix: str,
) -> RelaxedContractedModel:
    """Build one two-port chart before choosing a nonzero alpha_t coordinate."""

    h_matrix, h_parameters = projected_h_matrix(i, j, k, prefix)
    sigma, tau, nu = sp.symbols(f"{prefix}_sigma {prefix}_tau {prefix}_nu")
    b_vector = sp.symbols(" ".join(f"{prefix}_b{colour}" for colour in COLOURS))
    mu = sp.symbols(" ".join(f"{prefix}_mu{colour}" for colour in COLOURS))
    coordinate_vector = [sp.Integer(0)] * 3
    coordinate_vector[a] = sigma
    local_a = {
        coordinate_port: tuple(coordinate_vector),
        other_port: tuple(b_vector),
    }
    local_c = {
        coordinate_port: tuple(tau * entry for entry in coordinate_vector),
        other_port: tuple(-tau * entry for entry in b_vector),
    }
    companions_a = {
        port: tensor_symbols(f"{prefix}_A{port}")
        for port in (coordinate_port, other_port)
    }
    companions_c = {
        port: tensor_symbols(f"{prefix}_C{port}")
        for port in (coordinate_port, other_port)
    }
    saturation = (
        sigma,
        tau,
        nu,
        *mu,
        h_parameters["hii"],
        h_parameters["hjj"],
        h_parameters["hkk"],
    )
    return RelaxedContractedModel(
        normal_form="two_port",
        i=i,
        j=j,
        k=k,
        support=(coordinate_port, other_port),
        coordinate_index=a,
        second_coordinate_index=None,
        h_matrix=h_matrix,
        mu=mu,
        nu=nu,
        local_a=local_a,
        local_c=local_c,
        companions_a=companions_a,
        companions_c=companions_c,
        parameters={
            **h_parameters,
            "sigma": sigma,
            "tau": tau,
            **{f"b{colour}": b_vector[colour] for colour in COLOURS},
        },
        saturation_factors=saturation,
    )


def port_word(
    q0_colour: int,
    q1_colour: int,
    port_colours: dict[int, int],
) -> Word:
    """Assemble one labelled outside word."""

    return (q0_colour, q1_colour) + tuple(port_colours[port] for port in PORTS)


def singleton_minor_certificate(model: RelaxedContractedModel) -> sp.Expr:
    """Verify the four-coefficient rank-one certificate on a singleton chart."""

    (port,) = model.support
    other_ports = tuple(candidate for candidate in PORTS if candidate != port)

    def selected(row_colour: int, other_colour: int) -> Word:
        colours = {candidate: other_colour for candidate in other_ports}
        colours[port] = row_colour
        return port_word(model.i, model.i, colours)

    word_ii = selected(model.i, model.i)
    word_kk = selected(model.k, model.k)
    word_i_k = selected(model.i, model.k)
    word_k_i = selected(model.k, model.i)
    a_ii = model.a_contribution(word_ii)
    a_kk = model.a_contribution(word_kk)
    a_i_k = model.a_contribution(word_i_k)
    a_k_i = model.a_contribution(word_k_i)
    outer_minor = sp.expand(a_ii * a_kk - a_i_k * a_k_i)
    assert outer_minor == 0

    equation_ii = model.coefficient_equation(word_ii)
    equation_kk = model.coefficient_equation(word_kk)
    equation_i_k = model.coefficient_equation(word_i_k)
    equation_k_i = model.coefficient_equation(word_k_i)
    h_product = model.parameters["hii"] * model.nu
    certificate = sp.expand(
        equation_ii * equation_kk
        - h_product * equation_ii
        + model.mu[model.i] * equation_kk
        - equation_i_k * equation_k_i
        - outer_minor
    )
    expected = sp.expand(model.mu[model.i] * h_product)
    assert sp.expand(certificate - expected) == 0
    return expected


def two_port_slice_matrix(
    model: RelaxedContractedModel,
    inactive_colour: int,
) -> sp.Matrix:
    """Return the A-family matrix in the two active port slots at q0=q1=i."""

    coordinate_port, other_port = model.support
    inactive_ports = tuple(
        port for port in PORTS if port not in (coordinate_port, other_port)
    )
    return sp.Matrix(
        3,
        3,
        lambda row, column: model.a_contribution(
            port_word(
                model.i,
                model.i,
                {
                    coordinate_port: row,
                    other_port: column,
                    **{port: inactive_colour for port in inactive_ports},
                },
            )
        ),
    )


def verify_two_port_line_forcing(
    model: RelaxedContractedModel,
    target_colour: int,
    target_scalar: sp.Expr,
) -> dict[int, sp.Expr]:
    """Return exact coefficient certificates forcing alpha_t onto one line.

    This is called only when the coordinate factor ``sigma*e_a`` is not on
    the requested target line ``e_c``.  Row c of the module matrix is then
    ``y_c*b^T``.  If its target is ``delta*E_cc``, the identity

        b_c E_cd - b_d E_cc = delta b_d

    forces every off-line b_d to vanish after localizing at delta.
    """

    assert model.coordinate_index != target_colour
    matrix = two_port_slice_matrix(model, target_colour)
    coordinate_port, other_port = model.support
    inactive_ports = tuple(
        port for port in PORTS if port not in (coordinate_port, other_port)
    )

    def equation(row: int, column: int) -> sp.Expr:
        word = port_word(
            model.i,
            model.i,
            {
                coordinate_port: row,
                other_port: column,
                **{port: target_colour for port in inactive_ports},
            },
        )
        expected = target_scalar if row == column == target_colour else 0
        actual_equation = model.coefficient_equation(word)
        assert sp.expand(actual_equation - (matrix[row, column] - expected)) == 0
        return actual_equation

    diagonal_equation = equation(target_colour, target_colour)
    b_target = model.parameters[f"b{target_colour}"]
    certificates: dict[int, sp.Expr] = {}
    for colour in COLOURS:
        if colour == target_colour:
            continue
        off_diagonal_equation = equation(target_colour, colour)
        b_colour = model.parameters[f"b{colour}"]
        certificate = sp.expand(
            b_target * off_diagonal_equation - b_colour * diagonal_equation
        )
        expected_certificate = sp.expand(target_scalar * b_colour)
        assert sp.expand(certificate - expected_certificate) == 0
        certificates[colour] = expected_certificate
    return certificates


def classify_two_port_chart(i: int, j: int, k: int, a: int, pivot: int) -> str:
    """Classify one legitimate coordinate/nonzero chart by the line lemma."""

    if a == j:
        return "two_incompatible_required_lines"
    required_other_line = k if a == i else i
    if pivot != required_other_line:
        return "required_line_meets_wrong_nonzero_pivot"
    return "residual_coordinate_line_then_pure_j_gap"


def verify_two_port_chart_base(model: RelaxedContractedModel) -> None:
    """Check both line-forcing slices and the final pure-j coefficient."""

    h_i = model.parameters["hii"] * model.nu
    if model.coordinate_index != model.i:
        verify_two_port_line_forcing(model, model.i, model.mu[model.i])
    if model.coordinate_index != model.k:
        verify_two_port_line_forcing(model, model.k, -h_i)

    if model.coordinate_index not in (model.i, model.k):
        return
    required_other_line = model.k if model.coordinate_index == model.i else model.i
    substitution = {
        model.parameters[f"b{colour}"]: (
            model.parameters[f"b{colour}"] if colour == required_other_line else 0
        )
        for colour in COLOURS
    }
    all_j = (model.j,) * 6
    pure_j_equation = sp.expand(model.coefficient_equation(all_j).subs(substitution))
    assert pure_j_equation == -model.mu[model.j]


def verify_response_normal_forms() -> None:
    """Replay literal pair-response zero for both local normal forms."""

    # The singleton has no pair of active ports.
    singleton = singleton_model(0, 1, 2, 0, 0, 1, "response_singleton")
    assert len(singleton.support) == 1

    # For the two active ports, A_s*C_t + A_t*C_s cancels coefficientwise.
    two_port = two_port_model(0, 1, 2, 0, 1, 0, "response_two")
    s, t = two_port.support
    for q0_colour, q1_colour, s_colour, t_colour in product(COLOURS, repeat=4):
        first = (
            int(q0_colour == two_port.i)
            * two_port.local_a[s][s_colour]
            * int(q1_colour == two_port.j)
            * two_port.local_c[t][t_colour]
        )
        second = (
            int(q0_colour == two_port.i)
            * two_port.local_a[t][t_colour]
            * int(q1_colour == two_port.j)
            * two_port.local_c[s][s_colour]
        )
        assert sp.expand(first + second) == 0


def permanent4(columns: tuple[tuple[int, ...], ...]) -> int:
    """Exact 4 by 4 permanent for the GLS9 rational source control."""

    assert len(columns) == 4
    assert all(len(column) == 4 for column in columns)
    return sum(
        (
            columns[0][assignment[0]]
            * columns[1][assignment[1]]
            * columns[2][assignment[2]]
            * columns[3][assignment[3]]
        )
        for assignment in permutations(ROOTS)
    )


def incidence_pi_coefficient(
    incidence: dict[int, tuple[tuple[int, ...], ...]],
    excluded_positions: tuple[int, int],
    complement_word: Word,
) -> int:
    """Evaluate one exact complementary-permanent coefficient."""

    complement = tuple(
        position for position in OUTSIDE_POSITIONS if position not in excluded_positions
    )
    assert len(complement) == len(complement_word) == 4
    columns = tuple(
        tuple(incidence[position][root][colour] for root in ROOTS)
        for position, colour in zip(complement, complement_word, strict=True)
    )
    return permanent4(columns)


def matrix_rank(matrix: tuple[tuple[int, ...], ...]) -> int:
    return int(sp.Matrix(matrix).rank())


def gls9_source_control() -> dict[str, object]:
    """Check the theorem's exact GLS4-gated, full-target-failing control."""

    f0, f1, f2, f3 = (tuple(int(row == column) for column in ROOTS) for row in ROOTS)
    zero = (0, 0, 0, 0)

    def rows_from_columns(
        columns: tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]],
    ) -> tuple[tuple[int, ...], ...]:
        return tuple(
            tuple(columns[colour][root] for colour in COLOURS) for root in ROOTS
        )

    incidence = {
        Q0: rows_from_columns((f0, f1, zero)),
        Q1: rows_from_columns((f2, f0, zero)),
        2: rows_from_columns((f1, f2, f0)),
        3: rows_from_columns((f2, f3, f1)),
        4: rows_from_columns((f3, zero, f2)),
        5: rows_from_columns((zero, zero, f3)),
    }
    ranks = tuple(matrix_rank(incidence[position]) for position in OUTSIDE_POSITIONS)
    assert ranks == (2, 2, 3, 3, 2, 1)
    corank_sum = sum(3 - rank for rank in ranks)
    assert corank_sum == 5

    pi_q = {
        word: incidence_pi_coefficient(incidence, (Q0, Q1), word)
        for word in product(COLOURS, repeat=4)
    }
    assert {word: value for word, value in pi_q.items() if value} == {(2, 2, 2, 2): 1}
    raw_p_coefficient = (
        incidence[Q0][1][1] * incidence[Q1][2][0]
        + incidence[Q0][2][1] * incidence[Q1][1][0]
    )
    assert raw_p_coefficient == 1

    model = two_port_model(0, 1, 2, 0, 1, 0, "source_control")
    substitution: dict[sp.Expr, sp.Expr | int] = {
        model.parameters["hii"]: 1,
        model.parameters["hij"]: 0,
        model.parameters["hik"]: 0,
        model.parameters["hjj"]: 1,
        model.parameters["hkj"]: 0,
        model.parameters["hkk"]: 1,
        model.parameters["sigma"]: 1,
        model.parameters["tau"]: 1,
        model.parameters["b0"]: 0,
        model.parameters["b1"]: 1,
        model.parameters["b2"]: 0,
        model.nu: 1,
        **{mu: 1 for mu in model.mu},
    }
    for port, tensor in model.companions_a.items():
        excluded = (Q0, 2 + port)
        substitution.update(
            {
                symbol: incidence_pi_coefficient(incidence, excluded, word)
                for word, symbol in tensor.items()
            }
        )
    for port, tensor in model.companions_c.items():
        excluded = (Q1, 2 + port)
        substitution.update(
            {
                symbol: incidence_pi_coefficient(incidence, excluded, word)
                for word, symbol in tensor.items()
            }
        )

    residuals = {}
    for word in product(COLOURS, repeat=6):
        value = sp.expand(model.coefficient_equation(word).subs(substitution))
        assert not value.free_symbols
        if value:
            residuals["".join(map(str, word))] = int(value)
    assert residuals["002222"] == 1
    return {
        "incidence_ranks_q0_q1_u0_u1_u2_u3": ranks,
        "corank_sum": corank_sum,
        "pi_q_nonzero_coefficients": {"2222": 1},
        "raw_p_root_pair_12_q_colours_10": raw_p_coefficient,
        "det_h": 1,
        "h_at_all_ones": 3,
        "full_729_residual_nonzero_count": len(residuals),
        "full_729_residuals": residuals,
        "classification": (
            "exact maximum-root/raw-GLS4-gate control from GLS9; quotient "
            "survival is not verified, and it is not a complete contracted "
            "target or witness"
        ),
    }


def source_gate_atlas() -> dict[str, object]:
    """Count the exact constructible incidence charts available to GLS4."""

    rank_profiles = tuple(
        ranks
        for ranks in product((1, 2, 3), repeat=6)
        if sum(3 - rank for rank in ranks) <= 6
    )
    exact_rank_minor_chart_instances = sum(
        prod(comb(4, rank) * comb(3, rank) for rank in ranks) for ranks in rank_profiles
    )
    return {
        "incidence_variables": "six labelled 4x3 matrices L_u",
        "rank_corank_gate": (
            "rank(L_u)>=1 and sum_u(3-rank(L_u))<=6; exact-rank strata "
            "use all larger-minor zero equations and one selected rank-minor open"
        ),
        "rank_profiles": len(rank_profiles),
        "selected_minor_chart_instances_with_overlap": exact_rank_minor_chart_instances,
        "pi_q_pure_gate": ("80 permanent coefficients zero, Pi_Q[kkkk]=nu, D(nu)"),
        "raw_p_gate": (
            "union over a root pair and q0/q1 coordinate pair of "
            "D(L_q0[r,a]L_q1[s,b]+L_q0[s,a]L_q1[r,b])"
        ),
        "raw_p_coefficient_charts": comb(4, 2) * 3 * 3,
        "quotient_survival": (
            "no extra contracted polynomial: on an actual GLS4 source, "
            "Pi_Q!=0 implies individual order-two quotient survival"
        ),
        "maximum_root_warning": (
            "maximum-root nonexistence for every five-set is not encoded by "
            "contracted incidence ranks and is not silently inferred"
        ),
    }


def full_equation_summary() -> dict[str, object]:
    """Materialize representative full systems, not merely selected slices."""

    singleton_counts = {}
    singleton_variable_counts = set()
    for a, b in product(COLOURS, repeat=2):
        model = singleton_model(0, 1, 2, 0, a, b, f"full_s_{a}_{b}")
        equations = model.full_equations()
        singleton_counts[f"a{a}_b{b}"] = sum(equation != 0 for equation in equations)
        singleton_variable_counts.add(
            len(set().union(*(equation.free_symbols for equation in equations)))
        )
        assert model.coefficient_equation((2,) * 6) == (
            model.parameters["hkk"] * model.nu - model.mu[2]
        )

    two_port_counts = {}
    two_port_variable_counts = set()
    for a in COLOURS:
        model = two_port_model(0, 1, 2, 0, 1, a, f"full_t_{a}")
        equations = model.full_equations()
        two_port_counts[f"a{a}"] = sum(equation != 0 for equation in equations)
        two_port_variable_counts.add(
            len(set().union(*(equation.free_symbols for equation in equations)))
        )
        assert model.coefficient_equation((2,) * 6) == (
            model.parameters["hkk"] * model.nu - model.mu[2]
        )

    assert singleton_variable_counts == {174}
    assert two_port_variable_counts == {339}
    return {
        "equations_per_chart": 729,
        "singleton_relaxed_variables": 174,
        "two_port_relaxed_variables": 339,
        "singleton_structurally_nonzero_equations": singleton_counts,
        "two_port_structurally_nonzero_equations": two_port_counts,
        "relaxation": (
            "all active Pi_P other than pure Pi_Q are independent tensors; "
            "actual common-incidence permanents form a subset"
        ),
    }


def chart_audit() -> dict[str, object]:
    """Verify every discrete colour/support/coordinate chart."""

    singleton_certificates = 0
    for i, j, k in permutations(COLOURS):
        for port in PORTS:
            for a, b in product(COLOURS, repeat=2):
                model = singleton_model(
                    i,
                    j,
                    k,
                    port,
                    a,
                    b,
                    f"audit_s_{i}{j}{k}_{port}_{a}{b}",
                )
                certificate = singleton_minor_certificate(model)
                assert certificate in (
                    model.mu[i] * model.parameters["hii"] * model.nu,
                )
                singleton_certificates += 1
    assert singleton_certificates == 6 * 4 * 3 * 3 == 216

    two_port_classes: Counter[str] = Counter()
    verified_bases = set()
    for i, j, k in permutations(COLOURS):
        for coordinate_port, other_port in permutations(PORTS, 2):
            for a in COLOURS:
                base = (i, j, k, coordinate_port, other_port, a)
                if base not in verified_bases:
                    model = two_port_model(
                        i,
                        j,
                        k,
                        coordinate_port,
                        other_port,
                        a,
                        f"audit_t_{i}{j}{k}_{coordinate_port}{other_port}_{a}",
                    )
                    verify_two_port_chart_base(model)
                    verified_bases.add(base)
                for pivot in COLOURS:
                    two_port_classes[classify_two_port_chart(i, j, k, a, pivot)] += 1
    assert len(verified_bases) == 6 * 12 * 3 == 216
    assert sum(two_port_classes.values()) == 6 * 12 * 3 * 3 == 648
    assert two_port_classes == Counter(
        {
            "two_incompatible_required_lines": 216,
            "required_line_meets_wrong_nonzero_pivot": 288,
            "residual_coordinate_line_then_pure_j_gap": 144,
        }
    )
    return {
        "singleton_discrete_charts": singleton_certificates,
        "singleton_result": (
            "unit after D(mu_i*h_ii*nu): required 2x2 minor is nonzero, "
            "singleton companion flattening has rank at most one"
        ),
        "two_port_covering_chart_instances": sum(two_port_classes.values()),
        "two_port_chart_classes": dict(sorted(two_port_classes.items())),
        "two_port_saturation": ("D(sigma*tau*b_pivot*nu*mu0*mu1*mu2*hii*hjj*hkk)"),
        "two_port_residual_ideals": (
            "a=i gives (b_i,b_j) on D(b_k); a=k gives (b_j,b_k) "
            "on D(b_i), with indices interpreted as the ordered (i,j,k) colours"
        ),
        "two_port_final_gap": (
            "after either residual ideal, the original all-j coefficient is -mu_j"
        ),
    }


def main() -> None:
    verify_response_normal_forms()
    equation_summary = full_equation_summary()
    charts = chart_audit()
    source_control = gls9_source_control()
    report = {
        "status": "candidate_compact_refutation_of_the_GLS9_pure_Pi_contracted_locus",
        "field": "characteristic zero (the certificates use only field arithmetic)",
        "normal_forms": ["singleton", "two_port_with_nonzero_tau"],
        "full_equation_model": equation_summary,
        "chart_audit": charts,
        "gls4_source_gate_atlas": source_gate_atlas(),
        "exact_source_control": source_control,
        "complete_contracted_target_points": [],
        "actual_maximum_root_witnesses": [],
        "quotient_survival_points": [],
        "quotient_survival_scope": (
            "an actual GLS4 source carries quotient survival, but the displayed "
            "off-target control does not verify that conclusion; the relaxed "
            "module refutation does not need it"
        ),
        "smallest_invariant_gap": {
            "singleton": (
                "four coefficients give the forbidden minor "
                "-mu_i*nu*h_ii (rank 2 required versus rank <=1)"
            ),
            "two_port": (
                "the i-slices force local lines {e_i,e_k}; one original all-j "
                "coefficient then reduces to -mu_j"
            ),
        },
        "scope_warning": (
            "candidate proof-producing discovery only; independent hostile review "
            "and theorem/frontier integration are still required. The determinant "
            "divisor and broader GLS7 response patterns remain open."
        ),
        "global_conjecture": "UNRESOLVED",
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
