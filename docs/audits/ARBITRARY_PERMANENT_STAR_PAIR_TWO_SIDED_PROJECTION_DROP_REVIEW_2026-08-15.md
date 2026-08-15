# Hostile review of the star-pair two-sided projection-drop theorem

## Verdict and scope

**PASS, for the stated explicit `(4,1)` star-pair, pointwise,
characteristic-zero, full-`Delta_3` scope.**  No mathematical,
case-exhaustiveness, dependency, characteristic, or implementation blocker
survived hostile review.

For the displayed star pair, every exact `P_6 -> Delta_3` extension has a
rank-at-most-two local mode in each of the two mixed-factor projection
families:

```text
min_t rank(Phi_1|L_t) <= 2,
min_t rank(Phi_2|L_t) <= 2.
```

This is a necessary boundary condition for this one active-support-four
pair.  It does not exclude the locus where both families have rank-drop
modes, does not treat the inequivalent `(3,1)` orbit, and does not classify
active-support-five or active-support-six equality-five pairs.  It is not a
proof of unrestricted permanent nonrestriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_STAR_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  verify_arbitrary_permanent_star_pair_two_sided_projection_drop.py
  audit_arbitrary_permanent_star_pair_two_sided_projection_drop.py
```

The load-bearing predecessors reviewed and replayed were the exact `r=4`
pair-orbit classification, the fixed-pair two-sided projection-drop package
whose hyperplane-plane lemmas are reused, and the fixed-pair full-projection
package supplying the four-hyperplane permanent-zero corollary.

During hostile review, the theorem's slice-space proof was corrected from
"a symmetric rank-one tensor is a cube" to the field-safe statement "a
nonzero scalar multiple of a cube."  The former wording need not hold over
a non-algebraically-closed characteristic-zero field because the scalar may
have no cube root.  The corrected argument retains the nonzero scalar and
is valid over every stated field.  No other theorem or verifier change was
needed.

## 1. Pair algebra and projections

Independent square-free multiplication reproduced all nine pair products.
Their span has dimension five, the six mixed products span the two-plane
`M=span{m_1,m_2}`, and the three diagonal products are independent modulo
`M`.  Edge complementation gives

```text
star(m_1)=x_4x_5 x_3 ell_1,
star(m_2)=x_4x_5 z_0 ell_2,

star(d_0)=x_4x_5(
  x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3),
star(d_1)=-x_4x_5 x_2(x_0+x_1-x_3),
star(d_2)= 2x_4x_5 x_0x_3.
```

Thus the two mixed zero tensors are pullbacks of the four-variable
permanent through

```text
Phi_1=(x_3,x_4,x_5,ell_1),
Phi_2=(z_0,x_4,x_5,ell_2),

ell_1=x_0+x_1-x_2,
z_0=x_0-x_3,
ell_2=x_1-x_2.
```

The orbit-classification predecessor independently confirms that this is a
Delta-admissible equality-five `(4,1)` frame.  Its active-support
annihilator graph is `K_(1,3)`, whereas the earlier fixed `(4,2)` pair has
graph `K_(2,2)`, so transport from the fixed pair was not assumed.

## 2. Common-factor cells and the two directions

For a common missing `Phi_1` factor `phi` and common missing `Phi_2` factor
`psi`, exact coefficient extraction gives the complete ambient sensor-rank
table

```text
                       psi
                 z_0   x_4   x_5   ell_2
phi  x_3          1     0     0      2
     x_4          0     0     0      0
     x_5          0     0     0      0
     ell_1        3     0     0      1.
```

All cells except `(ell_1,z_0)` have rank at most two.  An exact diagonal
target supplies three independent functionals on the five-dimensional
pair-product space, so those fifteen cells are impossible.  This uses the
ambient common kernel only as an upper bound on the actual four local
planes; it does not reverse containment.

Assume first that all four `Phi_1` restrictions have rank three.  The
four-hyperplane permanent-zero corollary makes their images one coordinate
hyperplane.  Missing `x_4` or `x_5` kills all three pure quartics; missing
`x_3` kills `star(d_2)`.  Therefore every local plane lies in
`ker(ell_1)`.  On that hyperplane, the kernel of `Phi_2` is exactly

```text
K N,  N=x_1+x_2.
```

Conversely, if all four `Phi_2` restrictions have rank three, their common
missing factor is either `z_0` or `ell_2`; the other two possibilities again
kill all pure quartics.  On each of `ker(z_0)` and `ker(ell_2)`, the kernel
of `Phi_1` is the same line `K N`.  Hence the same secondary rank-profile
argument genuinely applies in both directions, even though the star frame
has no displayed swap symmetry analogous to the fixed pair.

## 3. Exhaustion of all secondary rank profiles

On any of the three relevant primary hyperplanes, a secondary projection
has rank two or three.  It has rank two exactly when its local plane
contains `N`.  Calling such a mode low, the hostile split is exhaustive:

```text
number of low modes    disposition
0                      common coordinate cell
1                      common coordinate cell
2                      common cell or the unique exceptional HHPP family
3                      impossible by common-kernel contractions
4                      impossible by common-kernel contractions
```

With no low mode, the secondary mixed zero tensor and the four-hyperplane
corollary give a common coordinate.  With one low mode, group two of the
three hyperplanes against the remaining hyperplane and plane.  The
hyperplane-hyperplane and hyperplane-plane product spaces both have
dimension at least three and are orthogonal in a six-space, hence both have
dimension three.  The first is a coordinate `W_i^2`; its self-orthogonal
complement and the sharp containment corollary put the other hyperplane and
plane in the same `W_i`.  These cases therefore land in the table above.

For a low mode, write

```text
N=alpha_0 y_0+alpha_1 y_1+alpha_2 y_2.
```

The single contraction of `star(d_2)` by `N` vanishes identically, so the
nonzero colour-two target forces `alpha_2=0`.  At two distinct low modes,
direct double contraction gives

```text
i_N i_N star(m_1)=i_N i_N star(m_2)=i_N i_N star(d_2)=0,
i_N i_N star(d_0)=i_N i_N star(d_1)=-2J,

J(y,z)=x_4(y)x_5(z)+x_5(y)x_4(z).
```

The equal `d_0,d_1` ambient tensors have target support at different colour
entries, so every pair of low modes satisfies

```text
alpha_(s,0)alpha_(t,0)=0,
alpha_(s,1)alpha_(t,1)=0.
```

For at least two low modes, each nonzero coefficient vector is supported on
one of the two singleton labels and any pair uses different labels.  The
pigeonhole principle excludes three and four lows.  With exactly two, the
low vectors normalize to `N=y_(s,0)` and `N=y_(t,1)`.

## 4. The unique two-low cancellation family

The sharp `(3,3,2,2)` permanent-zero classification was re-derived from the
hyperplane-plane equality cases.  Every zero tuple is either a common
coordinate tuple or, in factor coordinates, has the form

```text
P_2=P_3=P=span{z_k,z_l},
H_+=P direct-sum K(z_i+t z_j),
H_-=P direct-sum K(z_i-t z_j),  t!=0.
```

The common-coordinate branch is already handled by the sensor table.  In
the exceptional branch, contract the full `B^*`-valued target in the two
low slots selected at different colours.  Every target coordinate is zero,
whereas both possibly nonzero ambient diagonal coordinates are `-2J`.
Therefore

```text
J(H_+,H_-)=0.
```

In either projection's factor space, `J` has rank two and its radical is the
plane spanned by the two factors other than `x_4,x_5`.  Passing to the
nondegenerate two-dimensional quotient shows that two mutually
`J`-orthogonal hyperplanes must both contain the radical.  Their intersection
in the exceptional normal form is `P`, so `P` is exactly the radical.  Both
low planes consequently have `x_4=x_5=0`.

Every pure quartic has the common factors `x_4x_5`.  Those factors would
then have to be supplied by the two high modes, and the sum of their two
assignments is precisely `J(H_+,H_-)=0`.  All pure sensors vanish, contrary
to the exact target.  The exceptional family is impossible.

## 5. The rank-three dangerous cell

The sole cell not excluded by ambient sensor rank is

```text
K=ker(ell_1) intersect ker(z_0).
```

Its first-four-coordinate part has basis

```text
r_0=x_0+x_2+x_3,
r_1=x_1+x_2,
```

so a vector has coordinates

```text
y=s r_0+t r_1+a x_4+b x_5.
```

Direct substitution into the three diagonal complementary quadratics gives

```text
d_0: st-t^2,
d_1:-st-t^2,
d_2: 2s^2.
```

Consequently the exact combination

```text
d_0+2d_1-(1/24)d_2
```

restricts to

```text
-(1/12)(s+6t)^2 x_4x_5.
```

All three combination coefficients are nonzero.  Its target is therefore a
weighted three-term diagonal fourth-order tensor with tensor rank exactly
three: the displayed decomposition gives the upper bound and a mode
flattening gives the lower bound.

Put `r=s+6t` and let `P=pol(r^2x_4x_5)` on the three-space with coordinates
`(r,x_4,x_5)`.  The target is the pullback of a nonzero scalar multiple of
`P` through four evaluation maps from the local three-planes.  Each target
mode flattening has rank three, so every evaluation map has rank three and
is an isomorphism.  Existence of the target would therefore make `P`
`GL_3^4`-equivalent to a rank-three weighted diagonal tensor.

This is impossible.  The first-mode slice space of `P` is

```text
S=span{sym(r x_4x_5), sym(r^2x_5), sym(r^2x_4)}.
```

It is three-dimensional, so `P` is concise.  Every element of `S` is a
symmetric three-tensor.  A nonzero symmetric rank-one three-tensor over the
stated field is a nonzero scalar multiple of

```text
(alpha r+beta x_4+gamma x_5)^3.
```

Every tensor in `S` has zero coefficients at `r^3,x_4^3,x_5^3`; retaining
the nonzero scalar makes those three equations force
`alpha=beta=gamma=0`.  Thus `S` contains no nonzero rank-one tensor.

If a concise four-tensor had tensor rank at most three, any three-term
rank-one decomposition would have independent first-mode factors.  Its
three nonzero rank-one residual factors would then belong to its first-mode
slice space.  Since `S` contains none, `tensor-rank(P)>3`, contradicting the
weighted diagonal target.  This closes the dangerous cell over every
characteristic-zero field, without assuming algebraic closure.

## 6. Full-target and characteristic boundaries

The exact full `Delta_3` tensor is load-bearing.  Tensor-wide mixed zeros
invoke the hyperplane-product classifications; single and double
contractions are identities on all remaining modes; and the exceptional
branch contracts the entire `B^*`-valued target.  Hamming-one or
Hamming-two shells alone do not supply these identities.  No radius-two
claim is made.

Characteristic zero is correctly stated.  The proof uses `2!=0`, the
opposite-sign exceptional hyperplanes, the nonzero `-2J` contraction, and
the rational coefficient `-1/24`.  The odd-prime finite computations are
audits of identities and case structure, not substitutes for the written
characteristic-zero proof.

## 7. Computational replay and independence

The primary verifier uses exact SymPy arithmetic to reconstruct the pair,
all five complementary quartics, the three relevant restricted kernels,
the complete sixteen-cell table, the common-kernel contractions, the
exceptional product geometry, the exact rational square, and the concise
slice space.

The independent audit imports neither the primary verifier nor SymPy.  It
uses a custom modular square-free algebra and row reducer.  In particular,
it independently found

```text
HP equality cases over F_3:
  coordinate/support-one: 52,
  support-two:             12;

ordered zero HHPP tuples over F_3:
  common coordinate:      676,
  opposite exceptional:    12.
```

It also replayed the pair and all missing-factor ranks over `F_5,F_7`,
checked all common-kernel basis contractions, enumerated mutually
`J`-orthogonal hyperplane pairs, and found no nonzero cube in the dangerous
slice space over `F_5,F_7`.  These are genuinely different implementation
checks; the written linear algebra is the proof.

Focused replay after the field-safe wording correction passed:

```text
new primary exact verifier:                      PASS;
new independent no-import audit:                 PASS;
pair-orbit classification primary/audit:         PASS/PASS;
fixed-pair two-sided predecessor primary/audit:  PASS/PASS;
full-projection predecessor primary/audit:       PASS/PASS;
py_compile:                                      PASS;
Ruff:                                            PASS;
git diff --check:                                PASS.
```

The new package was absent from `origin/main` commit
`4efbbd2c4dc364930809cfceb5486268fa3fd00f`.  This is a repository-level
novelty observation only, not an external priority claim.

## 8. Accepted boundary

```text
star (4,1) pair, four full Phi_1 ranks:              EXCLUDED;
star (4,1) pair, four full Phi_2 ranks:              EXCLUDED;
star (4,1) pair, a drop in each family:              PROVED NECESSARY;
dangerous common cell:                               EXCLUDED;
simultaneous projection-drop residual:              OPEN;
radius-two version:                                  NOT PROVED;
Delta-admissible (3,1) orbit:                        NOT TREATED;
active-support-five/six equality-five pairs:         OPEN;
unrestricted P_6 -> Delta_3:                         UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

Any integration that changes the live frontier must update the canonical
frontier and theorem-ledger artifacts under the repository contract.  This
review does not perform that integration.

## Final reviewed hashes

```text
new theorem:
76AEBB661CA3E89DF3E4228954B0D7CB3D736414A4AB22C2EBC9A2C84A774D62

new primary verifier:
223B61126635FE59987B75684CFA6FCA1173737913CEAD0F46D98AA3A8C3DF1B

new independent audit:
CD4D833DB7CB132FCFED02A0BD2353799E184DAC3DFAC9EC5F714F998F614311

pair-orbit theorem:
4B7FCCCCF68B55E1DDEACB7328B7469A8A82F36AA2AB0303E9094519A95FC5BC

fixed-pair two-sided theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36

full-projection predecessor theorem:
727F39246FA64C899D1F51377FCB3C58640174C044510F727C796C888798F7C2
```
