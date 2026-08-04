#!/usr/bin/env python3
"""Modular exploration of SPECIAL SLOPE divisors for the weighted H22
pencils on the disjoint mixed-star (eighth) pure-P4 component.

The generic theorem (P5_H22_DISJOINT_MIXED_STAR_COMPONENT_GENERIC_OBSTRUCTION.md)
works over K=C(a,b,f)[phi]/(Phi) with the slope r transcendental.  Its
t-free elimination divides by four single-1-word own-extension
coefficients whose factors include (r-1) (three of the four D_23
denominators) and (r+1).  This script explores the DEGENERATE slopes
r=1, r=-1, r=0 (and a generic control slope) at finite-field component
points, recording:

  * mixed 14x8 rank structure over all p^4 markings t;
  * the marking loci with nonzero kernel;
  * which markings carry GENUINE survivors (both diagonals nonzero);
  * mode-0..3 one-marked ranks on every genuine projective direction;
  * whether the generic theorem's mode-zero Fitting minors
    (0,1,3,7),(0,1,5,7) stay nonzero, and the intersection of
    always-nonzero minors.

Finite-field evidence only; the characteristic-zero certificates are in
the companion scripts.
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

# ----------------------------------------------------------------------
# Component data (from verify_p5_h22_disjoint_mixed_star_component_...py)
# ----------------------------------------------------------------------

SAMPLES = {
    11: (1, 2, 7, 3),
    13: (1, 3, 5, 10),
}

BITS4 = tuple(itertools.product((0, 1), repeat=4))
BITS3 = tuple(itertools.product((0, 1), repeat=3))
MIXED = tuple(b for b in BITS4 if b not in ((0, 0, 0, 0), (1, 1, 1, 1)))
FITTING_ROWS = ((0, 1, 3, 7), (0, 1, 5, 7))
ROWS4 = tuple(itertools.combinations(range(8), 4))


def component_basis(p):
    a, b, f, phi = SAMPLES[p]
    j = (f + b * phi * phi) % p
    kappa = phi * (b * f + 1) % p
    eta = -(b * f + 1) % p
    alpha = (
        (0, 0, 1, -1),
        (-a * f + 1, -a * f - 1, f + phi, f - phi),
        (-a * j + eta, -a * j - eta, j + kappa, j - kappa),
        (1, -1, 0, 0),
    )
    beta = (
        (a + b, a - b, 0, 2),
        (1, 1, 0, 0),
        (1, 1, 0, 0),
        (0, 0, 1, 1),
    )
    alpha = tuple(tuple(v % p for v in row) for row in alpha)
    beta = tuple(tuple(v % p for v in row) for row in beta)
    val = (
        a * a * b * f * phi * phi + a * a * f * f
        - b * b * f * f + b * b * phi * phi - b * f - 1
    ) % p
    assert val == 0, "sample not on component"
    return (a, b, f, phi), alpha, beta


def weighted3(row, direction, r, p):
    if direction == "01":
        return ((r * row[0] + row[1]) % p, row[2] % p, row[3] % p)
    if direction == "23":
        return (row[0] % p, row[1] % p, (r * row[2] + row[3]) % p)
    raise ValueError(direction)


def perm3(rows, p):
    (a0, a1, a2), (b0, b1, b2), (c0, c1, c2) = rows
    return (
        a0 * (b1 * c2 + b2 * c1)
        + a1 * (b0 * c2 + b2 * c0)
        + a2 * (b0 * c1 + b1 * c0)
    ) % p


def perm4(rows, p):
    states = [0] * 16
    states[0] = 1
    for row in rows:
        updated = [0] * 16
        for mask, value in enumerate(states):
            if not value:
                continue
            for column, entry in enumerate(row):
                bit = 1 << column
                if mask & bit == 0:
                    updated[mask | bit] = (
                        updated[mask | bit] + value * entry
                    ) % p
        states = updated
    return states[15]


# ----------------------------------------------------------------------
# Fast multilinear evaluation of M(t):
# coefficient(word, slot m) = perm3 over the OTHER three rows' weighted
# 3-columns; expanding beta_j(t)=beta_j+t_j alpha_j multilinearly gives
#   sum over T subset of marked-others: prod t_j * P3[m][pattern]
# with pattern = which others remain beta.
# ----------------------------------------------------------------------

def pattern_table(walpha, wbeta, p):
    """P3[m][pattern] with pattern over others of m (increasing order):
    bit=1 means the unmarked beta row, bit=0 the alpha row."""
    table = []
    for m in range(4):
        others = [j for j in range(4) if j != m]
        row = {}
        for pattern in itertools.product((0, 1), repeat=3):
            rows = tuple(
                wbeta[j] if bit else walpha[j]
                for j, bit in zip(others, pattern)
            )
            row[pattern] = perm3(rows, p)
        table.append(row)
    return table


def coeff(bits, m, t, table, p):
    others = [j for j in range(4) if j != m]
    marked = [j for j in others if bits[j] == 1]
    total = 0
    for k in range(len(marked) + 1):
        for T in itertools.combinations(marked, k):
            prod = 1
            for j in T:
                prod = prod * t[j] % p
            pattern = tuple(
                1 if (bits[j] == 1 and j not in T) else 0
                for j in others
            )
            total = (total + prod * table[m][pattern]) % p
    return total


def build_rows(t, table, p):
    """Return (mixed 14x8, diagA 8-vector, diagB 8-vector)."""
    rows = {}
    for bits in BITS4:
        row = [0] * 8
        for m in range(4):
            c = coeff(bits, m, t, table, p)
            if bits[m] == 0:
                row[m] = c
            else:
                row[4 + m] = c
        rows[bits] = row
    mixed = [rows[bits] for bits in MIXED]
    return mixed, rows[(0, 0, 0, 0)], rows[(1, 1, 1, 1)]


# ----------------------------------------------------------------------
# Linear algebra mod p
# ----------------------------------------------------------------------

def rref_nullspace(matrix, p):
    work = [[e % p for e in row] for row in matrix]
    rows, cols = len(work), len(work[0])
    pivots = []
    pr = 0
    for c in range(cols):
        piv = next((r for r in range(pr, rows) if work[r][c]), None)
        if piv is None:
            continue
        work[pr], work[piv] = work[piv], work[pr]
        inv = pow(work[pr][c], -1, p)
        work[pr] = [v * inv % p for v in work[pr]]
        for r in range(rows):
            if r != pr and work[r][c]:
                s = work[r][c]
                work[r] = [
                    (x - s * y) % p for x, y in zip(work[r], work[pr])
                ]
        pivots.append(c)
        pr += 1
    free = [c for c in range(cols) if c not in pivots]
    basis = []
    for fc in free:
        v = [0] * cols
        v[fc] = 1
        for r, pc in enumerate(pivots):
            v[pc] = -work[r][fc] % p
        basis.append(tuple(v))
    return len(pivots), tuple(basis)


def rank_mod(matrix, p):
    return rref_nullspace(matrix, p)[0]


def det_mod(matrix, p):
    work = [[e % p for e in row] for row in matrix]
    n = len(work)
    res = 1
    for c in range(n):
        piv = next((r for r in range(c, n) if work[r][c]), None)
        if piv is None:
            return 0
        if piv != c:
            work[piv], work[c] = work[c], work[piv]
            res = -res
        pv = work[c][c]
        res = res * pv % p
        inv = pow(pv, -1, p)
        for r in range(c + 1, n):
            s = work[r][c] * inv % p
            for k in range(c, n):
                work[r][k] = (work[r][k] - s * work[c][k]) % p
    return res % p


def dot(row, vec, p):
    return sum(x * y for x, y in zip(row, vec)) % p


def projective_directions(dim, p):
    for pivot in range(dim):
        for tail in itertools.product(range(p), repeat=dim - pivot - 1):
            yield (0,) * pivot + (1,) + tail


def combine(direction, basis, p):
    return tuple(
        sum(direction[i] * basis[i][c] for i in range(len(basis))) % p
        for c in range(8)
    )


# ----------------------------------------------------------------------
# One-marked maps
# ----------------------------------------------------------------------

def one_marked_map(mode, alpha_d, beta_d, p):
    rows = []
    others = [m for m in range(4) if m != mode]
    for bits in BITS3:
        chosen = [
            beta_d[m] if bit else alpha_d[m]
            for m, bit in zip(others, bits)
        ]
        row = []
        for col in range(4):
            basis = tuple(int(i == col) for i in range(4))
            row.append(perm4((basis,) + tuple(chosen), p))
        rows.append(row)
    return rows


def survivor_analysis(t, z, alpha, beta, direction, r, p):
    walpha = [
        weighted3(alpha[m], direction, r, p) + (z[m],) for m in range(4)
    ]
    wbeta = []
    for m in range(4):
        marked = tuple(
            (beta[m][c] + t[m] * alpha[m][c]) % p for c in range(4)
        )
        wbeta.append(
            weighted3(marked, direction, r, p) + (z[4 + m],)
        )
    out = {}
    for mode in range(4):
        marked_map = one_marked_map(mode, walpha, wbeta, p)
        out[mode] = {
            "rank": rank_mod(marked_map, p),
            "matrix": marked_map,
        }
    return out


# ----------------------------------------------------------------------
# Main survey
# ----------------------------------------------------------------------

def survey(p, direction, r, minor_budget=4000):
    params, alpha, beta = component_basis(p)
    walpha = [weighted3(alpha[m], direction, r, p) for m in range(4)]
    wbeta = [weighted3(beta[m], direction, r, p) for m in range(4)]
    table = pattern_table(walpha, wbeta, p)

    # cross-check the multilinear evaluation against direct permanents
    import random

    rng = random.Random(12345)
    for _ in range(5):
        t = tuple(rng.randrange(p) for _ in range(4))
        zc = tuple(rng.randrange(p) for _ in range(8))
        mixed, dA, dB = build_rows(t, table, p)
        rows_a = [walpha[m] + (zc[m],) for m in range(4)]
        rows_b = [
            tuple(
                (wbeta[m][c] + t[m] * walpha[m][c]) % p for c in range(3)
            )
            + (zc[4 + m],)
            for m in range(4)
        ]
        for bits, row in zip(MIXED, mixed):
            direct = perm4(
                tuple(
                    rows_b[m] if bits[m] else rows_a[m] for m in range(4)
                ),
                p,
            )
            assert dot(row, zc, p) == direct, (bits, t)
        direct_a = perm4(tuple(rows_a), p)
        direct_b = perm4(tuple(rows_b), p)
        assert dot(dA, zc, p) == direct_a
        assert dot(dB, zc, p) == direct_b

    rank_hist = {}
    kernel_markings = []
    survivors = []
    genuine_total = 0
    min_marked_rank = {m: 4 for m in range(4)}
    fitting_failures = []  # genuine directions where BOTH minors vanish
    common_nonzero_mode0 = set(ROWS4)
    minors_checked = 0
    for t in itertools.product(range(p), repeat=4):
        mixed, dA, dB = build_rows(t, table, p)
        rank, kernel = rref_nullspace(mixed, p)
        rank_hist[rank] = rank_hist.get(rank, 0) + 1
        if not kernel:
            continue
        kernel_markings.append((t, rank))
        restA = [dot(dA, v, p) for v in kernel]
        restB = [dot(dB, v, p) for v in kernel]
        if not any(restA) or not any(restB):
            continue
        genuine = []
        for direction_vec in projective_directions(len(kernel), p):
            z = combine(direction_vec, kernel, p)
            if dot(dA, z, p) and dot(dB, z, p):
                genuine.append(z)
        assert genuine
        survivors.append(
            {
                "t": t,
                "rank": rank,
                "kernel_dim": len(kernel),
                "genuine": len(genuine),
            }
        )
        genuine_total += len(genuine)
        for z in genuine:
            info = survivor_analysis(t, z, alpha, beta, direction, r, p)
            for mode in range(4):
                min_marked_rank[mode] = min(
                    min_marked_rank[mode], info[mode]["rank"]
                )
            m0 = info[0]["matrix"]
            d1 = det_mod([m0[i] for i in FITTING_ROWS[0]], p)
            d2 = det_mod([m0[i] for i in FITTING_ROWS[1]], p)
            if d1 == 0 and d2 == 0:
                fitting_failures.append({"t": t, "z": z})
            if minors_checked < minor_budget:
                nonzero = {
                    rows
                    for rows in ROWS4
                    if det_mod([m0[i] for i in rows], p)
                }
                common_nonzero_mode0 &= nonzero
                minors_checked += 1
    return {
        "p": p,
        "sample_a_b_f_phi": list(params),
        "direction": direction,
        "slope": r,
        "rank_histogram": {str(k): v for k, v in sorted(rank_hist.items())},
        "markings_with_kernel": len(kernel_markings),
        "survivor_markings": len(survivors),
        "genuine_directions_total": genuine_total,
        "survivors_sample": survivors[:40],
        "survivor_t_patterns": sorted(
            {
                tuple(int(ti == 0) for ti in s["t"])
                for s in survivors
            }
        ),
        "min_marked_rank_per_mode": min_marked_rank,
        "fitting_both_minors_vanish_count": len(fitting_failures),
        "fitting_failures_sample": fitting_failures[:10],
        "common_nonzero_mode0_minors": sorted(common_nonzero_mode0)[:30]
        if genuine_total
        else None,
        "minors_checked": minors_checked,
    }


def main():
    out_dir = Path(__file__).resolve().parent.parent
    jobs = []
    for p in (11, 13):
        for direction in ("23", "01"):
            for r in (1, p - 1, 0, 2):
                jobs.append((p, direction, r))
    selected = sys.argv[1:] or None
    results = []
    for p, direction, r in jobs:
        tag = f"p{p}_{direction}_r{r}"
        if selected and tag not in selected:
            continue
        res = survey(p, direction, r)
        results.append(res)
        slope_name = {1: "1", 0: "0", 2: "2(control)"}.get(
            r, "-1" if r == p - 1 else str(r)
        )
        print(
            f"[p={p} D_{direction} r={slope_name}] "
            f"kernel markings {res['markings_with_kernel']}, "
            f"survivors {res['survivor_markings']}, "
            f"genuine dirs {res['genuine_directions_total']}, "
            f"min marked ranks {res['min_marked_rank_per_mode']}, "
            f"both-Fitting-minors-vanish {res['fitting_both_minors_vanish_count']}"
        )
        sys.stdout.flush()
    path = out_dir / "slope_divisor_modular_survey.json"
    merged = {}
    if path.exists():
        for entry in json.loads(path.read_text()):
            merged[(entry["p"], entry["direction"], entry["slope"])] = (
                entry
            )
    for entry in results:
        merged[(entry["p"], entry["direction"], entry["slope"])] = entry
    ordered = [merged[key] for key in sorted(merged)]
    path.write_text(json.dumps(ordered, indent=2) + "\n")
    print(f"wrote {path} ({len(ordered)} entries)")


if __name__ == "__main__":
    main()
