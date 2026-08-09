# Arbitrary-order permanent kernel-deletion hierarchy

## Status

This is an exact characteristic-zero theorem for every multilinear
restriction

```text
P_m -> Delta_3,                    m >= 3.
```

It extends the former `P_5` kernel Hall hierarchy and source-row tricolour
cover to every order.  It also excludes the sparsest possible
coordinate-only restriction: no such restriction can have only `3m`
nonzero source-row cells.

The theorem applies in particular to the unresolved `P_7` identity in the
five-root/two-residual cell.  It is a necessary obstruction, not a proof
that arbitrary `P_m -> Delta_3` restrictions do not exist.  The Krenn--Gu
conjecture remains unresolved.

## Setup

Let

```text
phi_i : C^3 -> C^m,                i=0,...,m-1,
r_(i,p)=e_p^* composed with phi_i, p=0,...,m-1,
```

and suppose

```text
P_m(phi_0(x_0),...,phi_(m-1)(x_(m-1)))
  = sum_(c=0)^2 lambda_c product_(i=0)^(m-1) x_i[c],
lambda_0 lambda_1 lambda_2 != 0.                       (1)
```

Here `P_m` is the order-`m` permanent tensor.  For a source-row subset
`S`, put

```text
K_i(S)=intersection_(p in S) ker r_(i,p).              (2)
```

## Theorem 1: all-subset kernel Hall quotas

For every source subset `S` of size

```text
2 <= s=|S| <= m-1
```

and every target colour `c`, at least `s` modes satisfy

```text
e_c^* in span{r_(i,p):p in S}.                         (3)
```

Equivalently, colour `c` is active on `K_i(S)` in at most `m-s` modes.

### Proof

Suppose instead that `c` is active in `m-s+1` modes.  Choose
`t_i in K_i(S)` with `t_i[c] != 0` in those modes and put `x_j=e_c` in
the remaining `s-1` modes.  The right side of (1) is the single nonzero
term

```text
lambda_c product_i t_i[c].                             (4)
```

Every one of the `m-s+1` source vectors `phi_i(t_i)` vanishes on all rows
in `S`.  A permanent monomial would have to assign these modes injectively
to the complement of `S`, which has only `m-s` rows.  This is impossible.
Thus (4) contradicts the left side of (1).  Annihilator duality converts
inactivity on `K_i(S)` into (3).

The argument is purely symbolic.  It is a deletion-capacity theorem: the
`s-1` pure target pins isolate one diagonal colour, while the remaining
source capacity is smaller by exactly one.

## Theorem 2: singleton tricolour cover at every order

For every source row `p` and every target colour `c`, some mode `i` has

```text
r_(i,p) is a nonzero multiple of e_c^*.                 (5)
```

Consequently any restriction (1) has at least `3m` distinct coordinate-row
cells.  Some local map contains at least three coordinate rows.

### Proof

Fix `p` and restrict every mode to `K_i=ker r_(i,p)`.  All permanent
monomials vanish because `m` modes have only `m-1` available source rows.
Equation (1) becomes

```text
sum_(c=0)^2 lambda_c tensor_i(e_c^* restricted to K_i)=0.    (6)
```

A colour-`c` summand is zero exactly when (5) holds in some mode.

Use the elementary full-support three-tensor dependence lemma: if

```text
alpha_0 T_0+alpha_1 T_1+alpha_2 T_2=0,
```

where every `T_c` is a nonzero decomposable tensor and every `alpha_c` is
nonzero, then outside at most one mode their three local factors are
proportional.  If two `T_c` are proportional, the full-support relation
forces the third into the same tensor line.  Otherwise solve for `T_2` as a
nonzero linear combination of `T_0,T_1`.  If the first two differ
projectively in two modes, flatten one such mode against the rest.  The two
left factors and the two complementary factors are both independent, so
the combination has matrix rank two, contradicting rank one of `T_2`.
Thus `T_0,T_1` differ in at most one mode, and factoring their common local
factors forces `T_2` to share them.

The full-support qualification is essential: mere linear dependence would
allow two equal tensors and an unrelated third.  It applies to (6) because
all `lambda_c` are nonzero.

Now classify (6).

1. If all three terms survive, the lemma forces their three local factors
   to be proportional in at least `m-1 >= 2` modes.  But the restrictions
   of the three coordinate covectors span `K_i^*`, of dimension two when
   `r_(i,p) != 0` and dimension three when it is zero.
2. If exactly two terms survive, the killed colour, say `c`, gives a mode
   with `K_i={x_c=0}`.  The other two coordinate restrictions are
   independent on that plane, so the two decomposable tensors cannot be
   proportional factor by factor.
3. One nonzero decomposable tensor cannot sum to zero.

Hence every colour term is killed, proving (5).  The three colours require
three different cells for each `p`, so there are at least `3m` coordinate
cells.

## Theorem 3: exact-minimal coordinate support is impossible

Assume in addition that the entire `m x m` row table has exactly `3m`
nonzero cells.  Then (1) is impossible.

By Theorem 2 all nonzero cells are coordinate rows, with exactly one cell
of each colour above every source row.  For a fixed colour `c`, the pure
coefficient in (1) is nonzero.  Its support has exactly `m` edges, so those
edges form a perfect matching `M_c` between the modes and source rows.
The three matchings are edge-disjoint.  Their union is a properly
three-edge-coloured cubic bipartite graph on `2m>4` vertices.

Bogdanov's matching theorem supplies a nonmonochromatic perfect matching
`F` in that union.  Colour each input mode by the colour of its incident
edge in `F`.  Each `M_c` is a perfect matching, so at each mode there is
exactly one nonzero row of colour `c`.  After filtering by the mixed word,
the coefficient matrix therefore has exactly one nonzero entry in every
mode column, and those entries form `F`.  The coefficient in the left side
of (1) is the single nonzero product of the entries on `F`, whereas the
diagonal target on the right has coefficient zero.  This is a
contradiction.

The matching-existence input is the arbitrary-order theorem reported as
Theorem 1.7 by L. Sunil Chandran, Rishikesh Gajjala, and Abraham M.
Illickan in
[*Krenn-Gu conjecture for sparse graphs*](https://arxiv.org/abs/2407.00303).

No matching or word enumeration is used.

## P5/P6/P7 consequences

```text
P_5 -> Delta_3:  at least 15 coordinate cells;
P_6 -> Delta_3:  at least 18 coordinate cells;
P_7 -> Delta_3:  at least 21 coordinate cells.
```

At every order the exact-minimal `3m`-cell coordinate-only branch is empty.
The displayed Hall-satisfying `P_7` survivor has more than 21 nonzero row
cells, so this theorem does not falsely exclude it.  Extra noncoordinate
cells or extra coordinate cells may create cancellations; controlling those
additional cells is the remaining problem.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_kernel_deletion_hierarchy.py
python claims/arbitrary-order/audit_arbitrary_permanent_kernel_deletion_hierarchy.py
```

The primary script gives symbolic sanity checks for the deletion-capacity
identities, representative quotient strata including the zero row, and the
`3m` bookkeeping.  It also checks a small `K_3,3` one-factorization and a
unique mixed word as a concrete model of the last argument.  The no-import
script repeats these checks with exact rational row reduction.  These
bounded checks do not prove the full-support decomposable-tensor lemma or
the arbitrary-order matching step; the displayed proof and the published
Bogdanov theorem do.

## Boundary

```text
all subset sizes 2,...,m-1:          PROVED;
singleton tricolour cover:           PROVED;
at least 3m coordinate cells:        PROVED;
exactly 3m nonzero cells:            EXCLUDED;
larger/signed P_m restrictions:      UNKNOWN;
P_7 -> Delta_3 in the root cell:     UNKNOWN;
global Krenn-Gu conjecture:           UNRESOLVED.
```
