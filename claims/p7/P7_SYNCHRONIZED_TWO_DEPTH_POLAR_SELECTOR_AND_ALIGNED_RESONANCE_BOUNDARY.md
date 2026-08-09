# Synchronized two-depth polar selection and the aligned-resonance boundary

## Status and legality boundary

**Strictly conditional characteristic-zero theorem.**  Assume that two
principal response tensors from the same graph have been **independently and
legally exposed**:

1. the residual-absent, or pure, tensor `T_0`; and
2. the tensor `T_Q` with the same two residual vertices present.

The exposures must retain the same root cofactor tensors `F_uv` and the same
physical direct blocks `B_uv`.  Under this synchronization, subtracting
`h T_0` from `T_Q` legally removes the direct layer and activates the
rank-two residual response by a residual-null polar contraction.

This assumption is substantive.  A single top `P_7` equation exposes
`T_Q`, not its hidden principal deletion `T_0`.  Nothing below manufactures
`T_0` from that one equation.  Thus this note is a conditional selector
theorem and a sharp boundary for that selector, **not** an unconditional
`P_7` exclusion.

Away from one exact resonance, the direct determinant gives the same
three-boundary incidence law as in the `h=0` theorem.  The later five-mode
row-pair theorem rules out equality through four: at least five blocker
planes contain a coordinate covector.  In the coordinate-monomial residual
branch, the only generic escape is that the residual edge agrees identically
with one target coordinate product.  On this aligned class every scalar
two-depth cancellation necessarily deletes that target colour, so the
rank-three determinant argument cannot continue.

The corrected blocks also satisfy a common matrix-pencil rank condition
across different physical pairs.  In contrast, if the pure blocks are not
observed, the uncorrected `h!=0` responses are affine-surjective and obey no
polynomial equation of their own.

## 1. The synchronized pair of tensors

Let `B` be the seven blocker modes and let `Q={q_0,q_1}`.  Contract the two
residual vertices against fixed vectors `z_0,z_1`.  Write

```text
h=B_(q_0,q_1)(z_0,z_1),
a_u=B_(u,q_0)(-,z_0),
b_u=B_(u,q_1)(-,z_1),                                (1)
```

and define

```text
D_uv=a_u tensor b_v+b_u tensor a_v,
W_uv=h B_uv+D_uv.                                    (2)
```

For five fixed root rows, put

```text
F_uv=P_5(H_w:w in B minus {u,v}).                    (3)
```

The synchronization hypothesis is that legal observations give both

```text
T_0=sum_(u<v) B_uv tensor F_uv
   =sum_(c=0)^2 mu_c e_c^(tensor 7),

T_Q=sum_(u<v) W_uv tensor F_uv
   =sum_(c=0)^2 nu_c e_c^(tensor 7),                 (4)
```

with the same `F_uv,B_uv` in both lines and with `mu_0 mu_1 mu_2!=0`.
For the standard GHZ contraction,

```text
nu_c=mu_c rho_c,             rho_c=z_0[c] z_1[c].    (5)
```

The diagonal form in the first line of (4) is part of the legality
hypothesis.  A hidden graph response `T_0` with unknown values is not enough.

### Theorem 1 (exact two-depth subtraction)

The synchronized difference is

```text
N=T_Q-h T_0
 =sum_(u<v) D_uv tensor F_uv
 =sum_(c=0)^2 (nu_c-h mu_c) e_c^(tensor 7).          (6)
```

Proof.  Substitute `W_uv=hB_uv+D_uv` into the second line of (4).  The
`hB_uv tensor F_uv` terms cancel term by term against `hT_0`.  The target
side is the same scalar linear combination of the two legally exposed
tensors.  No pair face is reconstructed and no division by `h` is used.

## 2. Residual-null polarization at arbitrary `h`

For every blocker `w`, let

```text
K_w=ker a_w intersection ker b_w.                    (7)
```

Fix a pair `{u,v}`, put `S=B minus {u,v}`, and choose nonzero
`kappa_w in K_w` for all `w in S`.  Contract (6) at the five modes in `S`.
Let

```text
s_uv=F_uv((kappa_w)_(w in S))
    =per(H_w(kappa_w):w in S).                       (8)
```

### Theorem 2 (conditional polar isolation)

The contraction is the exact matrix identity

```text
s_uv D_uv
 =sum_(c=0)^2 (nu_c-h mu_c)
    (product_(w in S) kappa_w[c]) e_c tensor e_c.    (9)
```

Proof.  The `{u,v}` summand gives the left side.  Every competing pair meets
`S`; if `w` is in that intersection, then

```text
D_(w,j)(kappa_w,x)
 =a_w(kappa_w)b_j(x)+b_w(kappa_w)a_j(x)=0.           (10)
```

Thus all twenty competing pairs vanish separately.  The diagonal target
contracts to the right side of (9).

### Corollary 3 (nonresonant determinant)

Since `rank D_uv<=2`, taking determinants in (9) gives

```text
0=product_(c=0)^2 (nu_c-h mu_c)
  product_(w in S) product_(c=0)^2 kappa_w[c].       (11)
```

No assumption on `s_uv` is needed.  In the GHZ normalization (5), this is

```text
0=(mu_0 mu_1 mu_2)
  product_(c=0)^2 (z_0[c]z_1[c]-h)
  product_(w in S,c) kappa_w[c].                     (12)
```

Call `K_w` torus-capable if it contains a vector with all three coordinates
nonzero.  At a **nonresonant** residual contraction

```text
Delta(z_0,z_1)=product_(c=0)^2(z_0[c]z_1[c]-h) !=0,  (13)
```

at most four of the seven spaces `K_w` are torus-capable.  Otherwise choose
five such spaces as `S` and use torus vectors in (12).

For a nonzero complex linear subspace `K subset C^3`,

```text
K misses (C^*)^3
 iff K is contained in {x[c]=0} for some c.          (14)
```

Taking annihilators in (7), the conclusion is equivalently

```text
at least three blockers w satisfy
e_c^* in span{a_w,b_w} for some target colour c.     (15)
```

This is exactly the three-boundary incidence conclusion of the `h=0`
selector, now valid at every synchronized nonresonant contraction.

The synchronized tensor `N` in (6) is itself the permanent tensor obtained by
appending the two residual rows `a,b` to the five root rows.  At nonresonance
all three diagonal coefficients are nonzero.  Applying
[`ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md`](../arbitrary-order/ARBITRARY_PERMANENT_FIVE_MODE_ROW_PAIR_INCIDENCE_THEOREM.md)
to the row pair `{a,b}` strengthens (15) to

```text
at least five blockers w satisfy
e_c^* in span{a_w,b_w} for some target colour c.     (16)
```

Equivalently, at most two `K_w` are torus-capable.  The determinant proof
above remains the direct one-pair activation; the fourth and fifth blockers
use the per-colour Hall quotas and the polar-rank exclusions of the complete
equality-at-three and equality-at-four incidence types.

## 3. Coordinate-monomial residuals reduce to aligned resonance

Let `L_0,L_1` be the residual simultaneous-kernel spaces, and work on the
irreducible torus chart in `L_0 x L_1`.  Suppose the exceptional residual
edge has coordinate-monomial form

```text
h(z_0,z_1)=gamma z_0[alpha] z_1[beta]                (17)
```

after restricting coordinate forms to `L_0,L_1`.  Assume that on a dense
open part of this chart at least three blocker null spaces are torus-capable.
The five-boundary theorem then forces `Delta=0` on a dense open set, hence identically.
The coordinate ring is a domain, so one factor in (13) vanishes identically:

```text
h(z_0,z_1)=z_0[c]z_1[c]                              (18)
```

for one fixed colour `c` on `L_0 x L_1`.

Equation (17) is the **target-aligned resonance**.  Equivalently, the two
decomposable bilinear tensors in (16)--(17) agree after restriction.  Thus
the residual coordinate forms at the two endpoints are respectively
proportional to the colour-`c` restrictions, with reciprocal constants.
If the restricted coordinate forms are pairwise nonproportional, this forces
`alpha=beta=c` and the corresponding normalized scalar.

Consequently a non-aligned coordinate-monomial branch satisfies the
three-boundary law on a dense open set.  The reduction does not exclude the
aligned class.

## 4. The aligned class is a sharp boundary for scalar two-depth subtraction

Consider an arbitrary scalar combination

```text
A T_Q+B T_0.                                          (19)
```

Its coefficient on the independent direct layer is `(A h+B)B_uv`.
Therefore cancellation of all arbitrary direct blocks requires

```text
B=-A h.                                               (20)
```

The target coefficient in colour `c` is then

```text
A nu_c+B mu_c=A(nu_c-h mu_c).                        (21)
```

On an aligned GHZ class, `nu_c=h mu_c`, so (20) is zero.  Hence every
nontrivial scalar two-depth cancellation that removes `hB` also removes the
aligned target colour.  The remaining diagonal target has rank at most two,
exactly the universal rank bound on `D_uv`.

This is a no-go for the present determinant method, not a construction of a
full witness.  Pointwise sharpness is immediate: any rank-at-most-two matrix
is a sum of two outer products and can serve as one corrected pair block.

## 5. A common-root matrix-pencil invariant

The two residual channels are shared across every physical pair.  Put

```text
P_u=[a_u b_u],                J=[0 1;1 0].            (22)
```

For disjoint port sets `U,V`, vertically concatenate the `P_u` and `P_v`.
The corrected rectangular block family satisfies

```text
D_(U,V)=(D_uv)_(u in U,v in V)=P_U J P_V^T,
rank D_(U,V)<=2.                                      (23)
```

Thus, whenever the pure and full pair blocks are jointly exposed,

```text
rank(W_(U,V)-h B_(U,V))<=2.                           (24)
```

All `3 x 3` minors vanish.  If `h` is hidden, regard

```text
M_(U,V)(t)=W_(U,V)-t B_(U,V).                         (25)
```

Every `3 x 3` minor polynomial `m_I(t)` has the common finite root `t=h`.
In particular,

```text
Res_t(m_I,m_J)=0                                      (26)
```

for every pair of minors.  These resultants are concrete necessary
invariants.  The exact statement is that all minor polynomials have a common
finite zero.  If at least one minor is nonzero as a polynomial, their
nonzero members have a common gcd of positive degree.  Pairwise resultants
alone need not be sufficient for a whole family.

The invariant is nonvacuous.  Two independent `3 x 3` blocks can specialize
to determinant pencils `t` and `t-1`, whose resultant is one, so a generic
joint `(B,W)` family does not possess the required common scalar.

## 6. Why uncorrected `W` alone has no invariant at `h!=0`

Fix `h!=0` and arbitrary common residual incidence columns `a_u,b_u`.
For an arbitrary desired family of bilinear matrices `W_uv`, define

```text
B_uv=h^(-1)(W_uv-a_u b_v^T-b_u a_v^T).               (27)
```

Then `W_uv=hB_uv+D_uv` identically.  Each direct physical block is an
independent parameter, and reverse orientation is supplied by transpose.
Therefore the projection to the uncorrected `W` family is the entire affine
space, even across arbitrarily many pairs.  Its polynomial vanishing ideal
is zero.

This affine-surjectivity is the sharp reason that the pure layer, a deeper
synchronized response, or another relation involving the same `B_uv` is
indispensable on the `h!=0` branch.

## Scope wall

Proved conditionally:

- exact cancellation of `hB` from two independently exposed synchronized
  depths;
- residual-null isolation of one corrected pair block at arbitrary `h`;
- the direct three-boundary determinant law and its five-boundary
  row-pair strengthening at every nonresonant contraction;
- reduction of a persistent coordinate-monomial escape to target alignment;
- failure of every scalar two-depth determinant selector on the aligned
  colour;
- common-root matrix-pencil minors and resultant invariants when `B,W` are
  jointly exposed;
- affine surjectivity, and hence no equations, for `W` alone when `h!=0`.

Not proved:

- legal exposure of `T_0` from a single top `P_7` equation;
- nonresonance or exclusion of the aligned resonance in every P7 branch;
- simultaneous principal-hafnian realization of a rank-two aligned slice;
- an unconditional `P_7 -> Delta_3` obstruction;
- the global Krenn--Gu conjecture.

All unconditional P7 and global claims remain **UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_synchronized_two_depth_polar_selector_and_aligned_resonance_boundary.py
python claims/p7/audit_p7_synchronized_two_depth_polar_selector_and_aligned_resonance_boundary.py
uv run --with sympy --with ruff python -m ruff check verify_p7_synchronized_two_depth_polar_selector_and_aligned_resonance_boundary.py audit_p7_synchronized_two_depth_polar_selector_and_aligned_resonance_boundary.py
python -m py_compile verify_p7_synchronized_two_depth_polar_selector_and_aligned_resonance_boundary.py audit_p7_synchronized_two_depth_polar_selector_and_aligned_resonance_boundary.py
```

The verifier performs only fixed symbolic checks: the synchronized
subtraction, the twenty-one-pair residual-null ledger, the diagonal
determinant, aligned scalar cancellation, a shared two-channel cross-block,
a nontrivial matrix-pencil resultant, and the affine inverse (26).  It does
not search supports, graphs, colour words, or matching families.
The independent no-import audit uses exact integer matrices and separate rank,
pair-contraction, scalar-cancellation, pencil-root, and affine-inverse checks.
