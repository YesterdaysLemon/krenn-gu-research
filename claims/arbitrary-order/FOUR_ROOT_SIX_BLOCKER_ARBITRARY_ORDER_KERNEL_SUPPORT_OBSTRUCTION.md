# Arbitrary-order four-root/six-blocker kernel-support obstruction

## Status

**Exact arbitrary-order characteristic-zero necessary theorem.**  In a
hypothetical global Krenn--Gu witness, let four fully supported pairwise-zero
roots have total blocker union exactly six.  Their root--blocker covectors
define six four-row, three-column matrices `H_u`.  The exact surplus-two
cofactor expansion places a torus point in

```text
J_H=Lambda_H(ker Lambda_H^off).
```

Consequently the order-twelve kernel theorems apply without any order-twelve
truncation or effective-block factorization.  At most two blocker modes can
admit a kernel vector supported on at least two target colours.  For every
pair of kernel vectors with nonempty support intersection, deleting those two
blockers must leave a weighted pure or binary diagonal restriction of `P_4`.

This is a genuine arbitrary-order local-to-global reduction for the
four-root/six-blocker cell.  It does not exclude cells with at most two
non-coordinate kernel modes, classify rank-three common-row matrices, close
the remaining `P_5/P_6` fibres, or prove the global conjecture.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## Global setup

Let `Omega` be the even vertex set of a hypothetical matching identity

```text
H_Omega((z_v))=sum_(c=0)^2 product_(v in Omega) z_v[c].       (1)
```

Fix four fully supported pairwise-zero roots

```text
R={r_0,r_1,r_2,r_3}
```

and assume their total blocker union is

```text
B={u_0,...,u_5}.                                            (2)
```

Put `Q=Omega\(R union B)`.  Since `|Omega|`, `|R|`, and `|B|`
are even, `|Q|` is even.  Every `q in Q` blocks no colour for `R`, so the
simultaneous kernel

```text
K_q=intersection_(i=0)^3 ker B_(r_i q)(x_i,-)
```

is not contained in any target coordinate hyperplane.  Over `C`, choose

```text
z_q in K_q intersect (C^*)^3.                              (3)
```

## The global cofactor is the local map `Lambda_H`

At blocker `u`, form the common-row matrix

```text
H_u[i,c]=B_(r_i u)(x_i,e_c),       i=0,...,3.               (4)
```

For `u<v` define the actual residual matching block

```text
W_uv[c,d]
 =H_(Q union {u,v})((z_q)_(q in Q),e_c at u,e_d at v).      (5)
```

After fixing the four roots and all vertices in `Q`, every surviving matching
pairs the roots bijectively with four of the six blockers.  If `{u,v}` is the
unused blocker pair, the remaining matching is exactly (5).  Hence the
surplus-two expansion is

```text
[w]T
 =sum_(u<v) W_uv[w_u,w_v]
   per([H_m[i,w_m]]_(i=0,...,3; m in B\{u,v}))
 = [w]Lambda_H(W).                                         (6)
```

This is a termwise perfect-matching bijection and holds for every even size of
`Q`.  No order-twelve assumption is used.

Restricting the global identity (1) gives

```text
T=sum_(c=0)^2 d_c e_c^6,
d_c=product_(i=0)^3 x_i[c] product_(q in Q) z_q[c] !=0.     (7)
```

Thus `W in ker Lambda_H^off` and its diagonal image is a coefficient-torus
point.  In particular,

```text
J_H intersects (C^*)^3.                                   (8)
```

## Imported exact kernel consequences

The double- and triple-contraction theorem
[`SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md`](SIX_BLOCKER_ORDER12_KERNEL_SUPPORT_COVER_NO_TORUS_P6.md)
applies to the arbitrary blocks (5).  It says that for
`k_u in ker H_u`, `k_v in ker H_v`, every nonempty intersection

```text
S_uv=supp(k_u) intersect supp(k_v)
```

has size at most two and forces the complementary four-mode cofactor to be a
weighted diagonal on exactly `S_uv`.  Two fully supported kernel modes are
therefore impossible.

The compatibility theorem
[`SIX_BLOCKER_ORDER12_THREE_KERNEL_PURE_COFACTOR_COMPATIBILITY_OBSTRUCTION.md`](SIX_BLOCKER_ORDER12_THREE_KERNEL_PURE_COFACTOR_COMPATIBILITY_OBSTRUCTION.md)
excludes the only three-mode support-two pattern left by the triple cover.
Consequently

```text
at most two of H_(u_0),...,H_(u_5)
admit a kernel vector supported on at least two colours.     (9)
```

The word ``order-twelve'' in those dependency titles describes where the
six-mode cofactor map was first isolated.  Their proofs concern `Lambda_H`
with arbitrary `3 x 3` blocks.  Equation (6) supplies exactly such blocks at
arbitrary ambient order, so their conclusions transfer verbatim.

## Consequence for larger local systems

Whenever four roots inside a five-root/six-blocker configuration still have
all six vertices in their blocker union, (9) constrains that four-root
deletion.  If a four-root deletion has only five blockers, it instead enters
the already isolated one-port `P_5` route.  This separates two finite local
frontiers but does not exclude either one by itself.

## Boundary

```text
four roots, exactly six blockers, arbitrary even ambient order: REDUCED;
torus J_H for the induced six-mode cofactor map: FORCED;
three support-at-least-two kernel modes: EXCLUDED;
at most two such modes: UNKNOWN;
rank-three and coordinate-kernel blocker modes: UNKNOWN;
arbitrary-order local-to-global reduction in full: UNKNOWN;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

Replay the imported packages first:

```text
python claims/arbitrary-order/verify_two_port_seven_blocker_reduction.py
python claims/arbitrary-order/audit_two_port_seven_blocker_reduction.py

uv run --with sympy python claims/arbitrary-order/verify_six_blocker_order12_kernel_support_cover_no_torus_p6.py
python claims/arbitrary-order/audit_six_blocker_order12_kernel_support_cover_no_torus_p6.py

uv run --with sympy python claims/arbitrary-order/verify_six_blocker_order12_three_kernel_pure_cofactor_compatibility_obstruction.py
python claims/arbitrary-order/audit_six_blocker_order12_three_kernel_pure_cofactor_compatibility_obstruction.py
```

Then run:

```text
python claims/arbitrary-order/verify_four_root_six_blocker_arbitrary_order_kernel_support_obstruction.py
python claims/arbitrary-order/audit_four_root_six_blocker_arbitrary_order_kernel_support_obstruction.py
```

The primary verifier checks the exact matching bijection for residual sets of
sizes zero, two, and four and verifies the torus coefficient product.  The
independent audit uses weighted rational hafnians and a separate dynamic
program.  The finite computations audit the constant-size combinatorics; the
written matching bijection proves the arbitrary-order characteristic-zero
statement.  No finite-field inference is used.
