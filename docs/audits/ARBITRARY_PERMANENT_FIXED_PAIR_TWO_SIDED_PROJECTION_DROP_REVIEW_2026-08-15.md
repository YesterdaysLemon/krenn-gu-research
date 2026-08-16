# Hostile review of the fixed-pair two-sided projection-drop theorem

## Verdict and scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero, full-target
scope.**  No mathematical, case-exhaustiveness, dependency, characteristic,
or implementation blocker survived hostile review.

For the fixed equality-five pair in the theorem, every exact
`P_6 -> Delta_3` extension has at least one rank-at-most-two local mode in
each of the two projection families:

```text
min_t rank(Phi_1|L_t) <= 2,
min_t rank(Phi_2|L_t) <= 2.
```

The proof does not exclude the simultaneous projection-drop residual, does
not normalize an arbitrary equality-five pair to the fixed pair, and does
not prove unrestricted permanent nonrestriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  verify_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
  audit_arbitrary_permanent_fixed_pair_two_sided_projection_drop.py
```

The load-bearing predecessor is:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md
  verify_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
  audit_arbitrary_permanent_fixed_pair_dimension_five_full_projection_boundary.py
```

The new package was absent from `origin/main` commit
`4efbbd2c4dc364930809cfceb5486268fa3fd00f`.  This is only a repository-level
novelty observation, not an external priority claim.

## 1. Fixed algebra and the two projection families

Independent square-free multiplication reproduced the five complementary
quartics

```text
star(m_1)=x_4 x_5 x_1 ell_1,
star(m_2)=x_4 x_5 x_0 ell_2,
star(d_0)=x_4 x_5 (x_1+x_2)(x_3-x_0),
star(d_1)=x_4 x_5 (x_0+x_2)(x_3-x_1),
star(d_2)=-2x_4 x_5 x_0x_1.
```

Thus the two mixed radical tensors are the pullbacks of the four-variable
permanent through

```text
Phi_1=(x_1,x_4,x_5,ell_1),
Phi_2=(x_0,x_4,x_5,ell_2).
```

For an exact target, `T_(m_1)=T_(m_2)=0`, while the three pure components
are nonzero diagonal fourth powers.  The proof consistently uses these
identities pointwise for the actual four planes and their actual colour
bases.

## 2. Hyperplane-plane product classification

Let `H=ker(alpha)` be a hyperplane and `P` a two-plane in the four-factor
space `E`.  The annihilator of `HP` consists exactly of symmetric
zero-diagonal matrices `C` satisfying

```text
C(P) subset K alpha.
```

Row reduction on the six matrix entries, independently organized by the
support size of `alpha`, gives:

```text
support(alpha)=1:
  dim(HP)=3 iff P is contained in the coordinate hyperplane H;

support(alpha)=2:
  dim(HP)=3 iff P is the complementary coordinate two-plane;

support(alpha)=3 or 4:
  dim(HP)>=4 for every P.
```

In the support-one case the product is the full three-dimensional
`W_i^2`.  In the support-two case, after naming the support `{i,j}` and its
complement `{k,l}`, one obtains

```text
H=span{z_k,z_l,z_i+t z_j},
P=span{z_k,z_l},
t!=0,

HP=span{z_kz_l,
        z_iz_k+t z_jz_k,
        z_iz_l+t z_jz_l}.
```

This independently verifies both the lower bound `dim(HP)>=3` and the exact
two-case equality classification.  The corollary

```text
HP subset W_i^2  =>  H=W_i and P subset W_i
```

also follows directly: choose nonzero `p in P intersect W_i`; the missing
`z_i z_j` coefficients of every `hp` first force `H=W_i`, after which they
force `P subset W_i`.

## 3. Exhaustion of the `(3,3,2,2)` zero-permanent tuples

For hyperplanes `H_0,H_1` and planes `P_2,P_3`, vanishing of the four-linear
permanent makes

```text
H_0P_2 perpendicular H_1P_3,
H_0P_3 perpendicular H_1P_2
```

under the perfect six-dimensional edge-complement pairing.  Every product
space has dimension at least three, so all four have dimension exactly
three.

If any equality is the support-one case, its product is self-orthogonal
`W_i^2`; the preceding corollary forces both hyperplanes to equal `W_i` and
both planes to lie in `W_i`.

Otherwise all four equalities are support-two cases.  A support-two
hyperplane has a unique complementary coordinate plane, so
`P_2=P_3=P`.  Both hyperplanes use the same coordinate partition.  Pairing
their displayed product bases gives

```text
HP(t) perpendicular HP(s) iff s=-t.
```

This yields exactly the exceptional family

```text
H(t), H(-t), P, P.
```

The common-coordinate and exceptional alternatives are disjoint in
characteristic zero and exhaust the possibilities.  There is no omitted
cancellation family.

## 4. Localization after one side has four full ranks

Assume all four `Phi_1` restrictions have rank three.  The predecessor's
four-hyperplane zero-permanent corollary makes their images one common
coordinate hyperplane.  Missing `x_4` or `x_5` kills all pure quartics, and
missing `x_1` kills `star(d_2)`.  Therefore the only possibility is

```text
L_t subset ker(ell_1) for every t.
```

On `ker(ell_1)`, the kernel of `Phi_2` is exactly

```text
K N,  N=x_2+x_3.
```

Since each `L_t` has dimension three, every `Phi_2(L_t)` has dimension two
or three, and it has dimension two exactly when `N in L_t`.  Call these
modes low.

With no low mode, the predecessor corollary gives a common missing
`Phi_2` coordinate.  With one low mode, group two of the three hyperplane
images against the remaining hyperplane and plane.  Orthogonality and the
hyperplane/hyperplane and hyperplane/plane lower bounds force equality;
the hyperplane product is `W_i^2`, and the containment corollary puts all
four images in that same `W_i`.

In either case all four original planes lie in

```text
ker(ell_1) intersect ker(psi),
psi in {x_0,x_4,x_5,ell_2}.
```

The predecessor's exact 16-cell table gives ambient sensor rank at most two
on each of these four common kernels.  The actual sensor is a subspace of
that full-space pullback.  The three pure products, however, induce three
independent functionals on the five-dimensional fixed pair product space.
This is a valid rank contradiction; the theorem does not reverse the
containment or silently specialize a generic statement.

## 5. Single and double common-kernel contractions

At a low mode write the common kernel vector in the local colour basis as

```text
N=alpha_0 y_0+alpha_1 y_1+alpha_2 y_2.
```

The single contraction of `star(d_2)` with `N` is identically zero.
Contracting its nonzero colour-two diagonal target therefore forces
`alpha_2=0`.

For two distinct low modes, direct double contraction gives

```text
i_N i_N star(m_1)=i_N i_N star(m_2)=i_N i_N star(d_2)=0,
i_N i_N star(d_0)=i_N i_N star(d_1)=2J,
J(y,z)=x_4(y)x_5(z)+x_5(y)x_4(z).
```

The two equal ambient bilinear tensors have target supports at the distinct
entries `(0,0)` and `(1,1)`.  Equality in the two remaining local colour
spaces consequently forces

```text
alpha_(s,0) alpha_(t,0)=0,
alpha_(s,1) alpha_(t,1)=0.
```

Each nonzero coefficient pair is therefore supported on one of the two
singletons, and every pair of low modes must use different singletons.
Three low modes are impossible.  With exactly two, rescaling and naming the
modes gives precisely

```text
N=y_(s,0),  N=y_(t,1).
```

This verifies the single-contraction, double-contraction, and pigeonhole
steps without a hidden genericity or noncancellation assumption.

## 6. The exceptional two-low family

With two high and two low `Phi_2` images, the preceding `(3,3,2,2)`
classification applies to `T_(m_2)=0`.  Its common-coordinate case returns
to the 16-cell contradiction.  In its only exceptional case, write

```text
(z_0,z_1,z_2,z_3)=(x_0,x_4,x_5,ell_2),
H_+=P+K(z_i+t z_j),
H_-=P+K(z_i-t z_j).
```

Contracting the complete `B^*`-valued target in the two low slots
`y_(s,0),y_(t,1)` kills all five target coordinates: the mixed two were
already zero, while each diagonal term needs the same colour in both low
slots.  The ambient double-contraction identities therefore imply

```text
J(H_+,H_-)=0.
```

The radical of `J` is `R=span{z_0,z_3}`.  Passing to the nondegenerate
two-dimensional quotient by `R`, mutual orthogonality gives
`dim(bar H_+)+dim(bar H_-)<=2`.  Each quotient image is nonzero because a
three-dimensional hyperplane cannot lie in the two-dimensional radical.
Thus both quotient images have dimension one and both hyperplanes contain
`R`.  Since the exceptional hyperplanes intersect exactly in their
two-plane `P`, it follows that `P=R`.

The two original low planes hence have `x_4=x_5=0`.  In every complementary
quartic the `x_4,x_5` factors must then be supplied by the two high modes;
their two assignments are exactly the pairing `J`, already zero.  All three
pure coefficients vanish, contradicting the exact target.  This closes the
last cancellation family.

Swapping `x_0,x_1` exchanges the two projection families and colours
`0,1`, preserves the fixed pair and the diagonal target, and repeats the
argument on the other side.  The two-sided conclusion follows.

## 7. Full-target and characteristic boundaries

The full exact `Delta_3` hypothesis is load-bearing.  In particular:

- tensor-wide mixed identities are needed to invoke the hyperplane product
  classifications;
- the single contraction of a pure tensor is an identity on all three
  remaining modes;
- the double contractions compare complete bilinear slices; and
- the exceptional step contracts the entire `B^*`-valued target.

Hamming-one equations, Hamming-two equations, or their union do not by
themselves supply all of these tensor identities.  The theorem correctly
does not claim a radius-two exclusion.

Characteristic zero is also correctly stated.  The hyperplane-plane and
coincident-hyperplane calculations, the opposite-sign exceptional family,
the `2J` contraction, and the separation of `H(t)` from `H(-t)` all require
`2!=0`.  Characteristic two is outside scope.  The modular audits in odd
characteristic are checks of identities and case structure, not a claimed
positive-characteristic proof.

The active-support-four orbit classification is not used: this theorem is
only about the displayed fixed `(4,2)` pair.  In particular it cannot be
transported automatically to the inequivalent `(3,1)` or `(4,1)` pair
orbits.

## 8. Computational replay and independence

The primary verifier uses SymPy exact arithmetic to reconstruct all five
quartics, the `x_0/x_1` symmetry, the restricted common kernel, the single
and double contractions, both equality models, the exceptional product
orthogonality, the rank-two radical, and the `ell_1` row of the predecessor
sensor table.

The no-import audit does not import the primary verifier or SymPy.  It uses
a custom modular reducer to enumerate all 130 two-planes and 40
hyperplanes of `F_3^4`.  It finds exactly

```text
HP equality cases:
  coordinate/support-one: 52,
  support-two:             12;

ordered zero HHPP tuples:
  common coordinate:      676,
  opposite exceptional:    12.
```

It separately replays the contraction identities over `F_3,F_5,F_7`,
exhausts the compatible common-kernel coefficient pairs over `F_3`, and
enumerates the mutually `J`-orthogonal hyperplane pairs.  This is genuinely
different implementation evidence, while the written characteristic-zero
linear algebra remains the proof.

Focused final replay passed:

```text
new primary exact verifier:              PASS;
new independent no-import audit:         PASS;
full-projection predecessor primary:     PASS;
full-projection predecessor audit:       PASS;
py_compile:                              PASS;
Ruff:                                    PASS.
```

## 9. Accepted scope and remaining obligations

```text
fixed pair, four full Phi_1 ranks:                    EXCLUDED;
fixed pair, four full Phi_2 ranks:                    EXCLUDED;
fixed pair, a drop in each projection family:        PROVED NECESSARY;
simultaneous projection-drop residual:               OPEN;
radius-two version of this theorem:                  NOT PROVED;
transport to other equality-five pair orbits:        NOT JUSTIFIED;
unrestricted P_6 -> Delta_3:                         UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

Any integration that changes the live frontier must update the canonical
frontier/navigation and theorem-ledger artifacts under the repository
contract.  This review does not perform that integration.

## Final reviewed hashes

```text
new theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36

new primary verifier:
E170A513301ECD84A8989066A29B51B89635FD54B0CEF88DCEBBEEDBAAF641DE

new independent audit:
47A30C8C09E3931526C4CFAC2E9ABE66B7FD10B4EA95336C93E12D63C360E6B2

predecessor theorem:
727F39246FA64C899D1F51377FCB3C58640174C044510F727C796C888798F7C2

predecessor primary verifier:
7975FF892EE6A1FC4CB0CA12FA02D426AD25E60FBCB9AA88CF2874D605B600B0

predecessor independent audit:
AF66CD5BA787B80BC96F5C33316DC0A6CEAA7233DAC4B8D2D48159884E2A6C2B
```
