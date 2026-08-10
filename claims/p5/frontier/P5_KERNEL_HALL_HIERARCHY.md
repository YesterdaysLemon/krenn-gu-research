# `P_5` kernel Hall hierarchy

## Status

This is an exact global incidence theorem over `C`.  It strengthens the
coordinate-plane pair cover from source pairs to every source subset of
size two, three, or four.

For a hypothetical restriction `P_5 -> Delta_3`, let `r_(i,s)` be row
`s` of local map `i`.  For every source set `S` of size `s in {2,3,4}`
and every target colour `c`,

```text
e_c^* belongs to span{r_(i,p) : p in S}
for at least s of the five modes i.                    (1)
```

This is a necessary condition, not yet a complete contradiction.

## Kernel form

Suppose

```text
P_5(phi_0(x_0),...,phi_4(x_4))
  = sum_(c=0)^2 lambda_c product_(i=0)^4 x_i[c],
lambda_c != 0.                                         (2)
```

For a source subset `S`, put

```text
K_i(S) = intersection_(p in S) ker r_(i,p).            (3)
```

Call colour `c` **active** in `K_i(S)` if some `t in K_i(S)` has
`t[c] != 0`.

**Kernel Hall lemma.**  If `|S|=s in {2,3,4}`, then a fixed colour is
active in at most `5-s` modes.

Assume instead that colour `c` is active in a set `I` of

```text
|I| = 6-s
```

modes.  Choose `t_i in K_i(S)` with `t_i[c] != 0` for `i in I`, and
put `x_j=e_c` in every other mode.  The target value in (2) is

```text
lambda_c product_(i in I) t_i[c] != 0.                 (4)
```

Every source vector `phi_i(t_i)`, for `i in I`, vanishes on `S`.
Those `6-s` modes would have to receive distinct coordinates from the
complement of `S`, which has only `5-s` elements.  Hence every
permanent monomial is zero, contradicting (4).

This proves the kernel statement.

## Dual incidence quotas

Linear annihilator duality gives

```text
colour c is inactive in K_i(S)
iff e_c^* belongs to span{r_(i,p) : p in S}.            (5)
```

At most `5-s` active modes means at least `s` inactive modes, proving
(1).  Explicitly:

| source rows in `S` | modes whose row span contains each fixed `e_c^*` |
|---:|---:|
| 2 | at least 2 |
| 3 | at least 3 |
| 4 | at least 4 |

For `s=2`, the three colours contribute at least six incidences across
five two-row spans.  Each span contains at least one coordinate point
by the five-row incidence lemma, and at least one span must contain two
coordinate points.  That span is a coordinate plane.  Thus the earlier
ten-pair coordinate-plane cover is a direct corollary.

## Axial `4+1` consequences

Normalize an axial local map so that source rows `0,1,2,3` lie in
`<e_0^*,e_1^*>` and row `4` is proportional to `e_2^*`.

- For `S={0,1,2,3}`, mode zero lacks `e_2^*` in the row span, so all
  other four modes must contain `e_2^*` in the span of those four rows.
- For every triple `S subset {0,1,2,3}`, at least three of the other
  four modes contain `e_2^*` in the corresponding triple-row span.
- For a pair inside `{0,1,2,3}`, at least two other modes contain
  `e_2^*` in that pair span.
- For a star pair `{4,p}`, at least two other modes contain each of
  `e_0^*,e_1^*`, and at least one other mode contains `e_2^*`.

These are simultaneous quotas on the four maps that would also have to
compress the three axial quartic slices to three different pure
tensors.

## Verification

Run:

```text
python claims/p5/frontier/verify_p5_kernel_hall_hierarchy.py
python claims/p5/frontier/audit_p5_kernel_hall_hierarchy.py
```

The primary verifier checks every subset size and every possible active
mode mask, exhausts all relevant source assignments, and reconstructs
the pair-cover incidence count.  The independent audit enumerates all
five-tuples of projective kernel subspaces over `F_7` that lie in a
coordinate hyperplane and checks the active-count-to-dual-incidence
conversion directly.

## Boundary

For a single forbidden source coordinate, all five modes would be
needed to defeat a perfect matching, leaving no unused mode in which to
place `e_c` and isolate one diagonal term.  The clean Hall evaluation
therefore starts at `|S|=2`.  The hierarchy constrains, but does not by
itself solve, the remaining multiple-coordinate and axial branches.
