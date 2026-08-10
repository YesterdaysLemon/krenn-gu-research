# P5 has compressed nonlinear four-hafnian tomography

## Status

**Exact characteristic-zero generic-finiteness theorem, with a target-incidence
boundary.**  In the two-residual `P_5` cell there are three probe roots and
seven named nonroots.  With every root--root block zero, the root tensor has
only 27 channels but is synthesized from 35 principal four-hafnians.  Complete
linear labeling is therefore impossible.

That dimension deficit does not destroy physical observability.  This note
gives one legal fixed integer chart for which the `27 x 35` companion sensor is
surjective and its composite with the physical four-hafnian map has a
full-rank `27 x 21` Jacobian.  Relative to known companion blocks, the full
three-root tensor therefore determines the 21 nonroot edges up to finitely
many algebraic branches on a nonempty open set.  Equivalently, the eight
linear directions lost by the sensor are transverse to the physical
four-hafnian tangent space at the certified point.

This is not a GHZ witness.  The certified all-one graph produces a nondiagonal
root tensor.  At that non-target point the physical image tangent contains no
nonzero diagonal target direction, but no physical intersection with the
diagonal target is constructed or excluded.

The result is symbolic.  The proof evaluates three named integer minors on a
single displayed chart.  Their nonzero modular residues are exact certificates
that the corresponding characteristic-zero determinants are nonzero; they are
not finite-field heuristics.  Neither replay enumerates graphs, supports,
words, or parameter candidates.

## 1. Three-root matching expansion

Let `R={0,1,2}` be the roots and `N={0,...,6}` the nonroots.  After fixing one
vector at every nonroot, write

```text
h_(i,u) in V_i^*,                 dim V_i=3,            (1)
```

for the root factor of the edge `i--u`, and let `L_ij` be the root--root
bilinear form.  Set

```text
L_ij=0                         for every root pair.     (2)
```

For a deletion triple `D subset N`, define

```text
G_D=sum_(f:R -> D bijective) tensor_(i in R) h_(i,f(i)). (3)
```

Every surviving root must then match a distinct member of `D`; the remaining
four nonroots match internally.  Hence the exact root tensor is

```text
T_R=sum_(D subset N, |D|=3) G_D H_(N minus D),          (4)
```

where `H_S` is the principal hafnian of the nonroot graph on the four-set `S`.
Thus

```text
Gamma_3:K^35 -> tensor_(i in R) V_i^*,
e_D |-> G_D                                                   (5)
```

is the companion synthesis map.  Its 35 columns cannot be independent in 27
channels, so individual recovery of the entire named four-deck is impossible.

## 2. A legal integer chart

Put

```text
x_i=(1,1,1),                    w_i in {1,2,4},         (6)
```

with `w_i=2^i`.  Name the nonroots `b_0,...,b_4,q_0,q_1`.  For endpoint `u`
put `t=u+1` and use

```text
h_(i,b_u)=e_0+t^(w_i)e_1+t^(2w_i)e_2,                  (7)
h_(i,q_s)=e_0+t^(w_i)e_1-(1+t^(w_i))e_2.              (8)
```

Then

```text
h_(i,b_u)(x_i)=1+t^(w_i)+t^(2w_i) != 0,
h_(i,q_s)(x_i)=0.                                      (9)
```

Thus all five blockers are active and both `q_0,q_1` are genuine residual
nonblockers.  Realize each root--nonroot edge as

```text
B_(i,u)=h_(i,u) tensor ell_u,          ell_u(z_u)=1,   (10)
```

and use the transpose in the reverse orientation.  These are legal symmetric
loopless graph blocks over the integers.  The nonroot graph remains an
independent 21-parameter family.

## 3. The compressed sensor and its physical restriction

Order the 35 deletion triples lexicographically and the 27 tensor rows by the
ternary words

```text
000,001,...,222.                                         (11)
```

Let `M` be the resulting integer matrix for `Gamma_3`.  Its first 27 columns
form a named square submatrix satisfying

```text
det M[:,0:27] mod 1,000,003 = 772,431 != 0,
det M[:,0:27] mod 1,000,033 = 356,742 != 0.             (12)
```

Therefore

```text
rank Gamma_3=27,                 dim ker Gamma_3=8.     (13)
```

In particular every formal root tensor, including every diagonal tensor, has
an eight-dimensional affine fiber of four-deck labels.  This is only a linear
label-space statement: almost all label vectors are not hafnian decks of a
graph.

Let `A` be the symmetric zero-diagonal matrix of the seven-nonroot graph and
write

```text
F_4(A)=(H_(N minus D)(A))_(|D|=3),
Psi(A)=Gamma_3 F_4(A).                                  (14)
```

At the all-one graph the derivative of `H_(N minus D)` with respect to edge
`a_uv` is one precisely when `{u,v} subset N minus D`.  Thus `dF_4` is the
fixed complement-inclusion matrix `K` of size `35 x 21`, and

```text
dPsi=M K.                                               (15)
```

The submatrix of `dPsi` in ternary rows 0 through 20 has

```text
det (M K)[0:21,:] mod 1,000,003 = 953,249 != 0,
det (M K)[0:21,:] mod 1,000,033 = 541,617 != 0.        (16)
```

Hence `dPsi` has rank 21 at the all-one graph.  In tangent language,

```text
ker Gamma_3 intersect im(dF_4)=0                       (17)
```

there: the physical variety avoids all eight compressed-away directions to
first order.

### Theorem 1 (compressed P5 physical tomography)

For the legal three-root, five-blocker, two-residual chart (6)--(10), the
physical root-tensor morphism `Psi:A^21 -> A^27` has image dimension 21 and is
generically finite onto its image.  Consequently, relative to these known
companion blocks, a generic root tensor recovers the seven-nonroot graph up to
finitely many algebraic branches.

Indeed, (16) gives a full-domain-rank differential at one point.  The image
therefore has the full domain dimension 21, and the generic fiber-dimension
theorem makes the generic fiber zero-dimensional.

This is a nonlinear algebraic compression theorem, not a hidden recovery of
all 35 labels.  It also cannot give global uniqueness: because every
four-hafnian is quadratic in the edges,

```text
F_4(A)=F_4(-A),                   Psi(A)=Psi(-A).       (18)
```

There may be further branches and singular exceptional fibers.

The natural neighboring framework is Breiding--Gesmundo--Michalek--
Vannieuwenhoven, [*Algebraic compressed
sensing*](https://arxiv.org/abs/2108.13208): the structured signal variety is
the Zariski closure

```text
X_4=closure(F_4(A^21)) subset A^35,                    (19)
```

and `Gamma_3` is a linear measurement map.  Certificate (16) proves local
recoverability and generic finite recoverability for this particular legal,
not generic, measurement operator.  Global recovery of the deck point would
require control of the affine difference variety `X_4-X_4`: two deck points
collide precisely when their difference lies in `ker Gamma_3`.  Recovery of
the graph from its deck has its own unavoidable sign branch.  Algebraic-
matroid language records the same local fact through Jacobian independence,
but does not by itself determine either finite fiber degree.  This translation
suggests a new exact object for the remaining P5 problem:

```text
collision scheme C_Gamma={(A,A'):F_4(A)-F_4(A') in ker Gamma_3}. (20)
```

Its unavoidable components `A'=A` and `A'=-A` include the diagonal and the
sign branch (18).  Proving that these are the only dominant components, or
finding another one, would upgrade the generic-finite theorem without
enumerating graphs.

## 4. Diagonal target tangent boundary

Let

```text
Delta=span{e_0^(tensor 3),e_1^(tensor 3),e_2^(tensor 3)}. (21)
```

Its pure-word rows are `0,13,26`.  Append these three columns to `dPsi`.  In
rows `0,...,22,26`, the resulting named `24 x 24` minor satisfies

```text
det [dPsi|Delta][{0,...,22,26},:] mod 1,000,003 = 686,920,
det [dPsi|Delta][{0,...,22,26},:] mod 1,000,033 = 559,439. (22)
```

Consequently

```text
im(dPsi) intersect Delta={0}                            (23)
```

at the all-one graph.  But the all-one output is itself not diagonal; for
example its `001` coordinate equals `420,840`.  Equation (23) is therefore
only a target-direction tangent exclusion at a fixed non-target point.  It is
not transversality of a physical target intersection and says nothing by
itself about existence elsewhere.

Surjectivity (13) makes formal target incidence automatic in unconstrained
label space: for each `J in Delta`, the fiber `Gamma_3^(-1)(J)` is an affine
eight-plane.  The unresolved question is whether such a fiber contains a
physical four-hafnian deck with all required blocker and graph conditions.

### Theorem 2 (compressed target-incidence correspondence)

The correct ambient incidence object in this surjective regime is not the
intersection of the sensor image with `Delta`; that image is all of `K^27`.
Make the standard base change to an algebraic closure; emptiness there is the
stronger statement.  Let

```text
X=projective closure of {[F_4(A)]:F_4(A)!=0} in P^34. (24)
```

The rank-21 deck Jacobian makes the affine image cone 21-dimensional, so
`X` is irreducible of dimension 20.  For an arbitrary surjective sensor
`Gamma:K^35 -> K^27`, put

```text
L_Gamma=Gamma^(-1)(Delta),             dim L_Gamma=11. (25)
```

A nonzero physical diagonal target requires
`P(L_Gamma) intersect X != empty`.  In `Gr(11,35)`, the locus of 11-planes
meeting `X` has codimension at least four.

Indeed, the incidence correspondence of pairs `([v],L)` with `[v] in X` and
`[v] in P(L)` has dimension

```text
dim X + dim Gr(10,34)=20+10(34-10)=260,
dim Gr(11,35)=11(35-11)=264.
```

Its proper projection to the Grassmannian is closed and has dimension at
most 260.  Moreover, as arbitrary surjective `Gamma` varies, the map
`Gamma |-> L_Gamma` covers `Gr(11,35)`.  Thus ambient surjective sensors with
a possibly nonzero physical target lie in a proper locus of codimension at
least four.

This **compressed target-incidence correspondence** is the P5 analogue of
the output-space Schubert loci in P6 and P7.  It is deliberately an ambient
theorem.  The legal companion family could map entirely into the exceptional
locus, and even a meeting point of `P(L_Gamma)` with `X` may lie in
`P(ker Gamma)` and hence produce the zero tensor.  Proving the legal pullback
proper, or proving that its nonkernel part is empty, remains the actual GHZ
problem.

## 5. The revised P5/P6/P7 observability staircase

| cell | linear companion labels | physical graph observability relative to known companions |
|---|---|---|
| `P_5` | 35 labels in 27 channels; complete labeling impossible | generically finite by Theorem 1 |
| `P_6` | all 70 four-deck labels linearly selectable | generically finite from the four-deck |
| `P_7` | all 219 four-, six-, and eight-deck labels selectable | rational on the pinned full-sensor open |

Thus raw label capacity is no longer a generic graph-observability objection
in any of the two-residual `P_5/P_6/P_7` cells.  The common remaining problem
is diagonal target incidence inside the physical hafnian image, together with
branch and singular-locus control.

## 6. Scope wall

```text
three-root deletion depths with L_ij=0:              ONLY DEPTH FOUR;
legal five-blocker/two-residual chart:               CONSTRUCTED;
Gamma_3 rank and kernel dimension:                   27 AND 8;
complete linear recovery of 35 named H4 labels:      IMPOSSIBLE;
composite physical Jacobian rank:                    21 (FULL DOMAIN RANK);
relative nonroot-edge recovery:                      GENERICALLY FINITE;
global or rational edge recovery:                    FALSE/NOT CLAIMED;
sign ambiguity A <-> -A:                             PRESENT;
formal diagonal-target label fibers:                 AFFINE DIMENSION EIGHT;
all-one physical tensor is diagonal target:          FALSE;
nonzero diagonal tangent at the all-one point:       EXCLUDED;
physical diagonal-target incidence elsewhere:        UNKNOWN;
GHZ-compatible point in the generic-finite open:     UNKNOWN;
ambient compressed target-incidence codimension:    AT LEAST FOUR;
legal pullback of compressed target incidence:      UNKNOWN;
P5 obstruction:                                      UNKNOWN;
global Krenn--Gu:                                    UNRESOLVED.       (26)
```

## Replay

```powershell
python verify_p5_compressed_h4_physical_tomography_and_target_tangent_boundary.py
python audit_p5_compressed_h4_physical_tomography_and_target_tangent_boundary.py
python -m py_compile verify_p5_compressed_h4_physical_tomography_and_target_tangent_boundary.py audit_p5_compressed_h4_physical_tomography_and_target_tangent_boundary.py
uv run --with ruff ruff check verify_p5_compressed_h4_physical_tomography_and_target_tangent_boundary.py audit_p5_compressed_h4_physical_tomography_and_target_tangent_boundary.py
```

The primary replay builds every companion column by a recursive permanent and
checks the first prime in (12), (16), (22).  The independent standard-library
audit rebuilds the sensor with Ryser's formula and checks the second prime.
Neither imports the other or searches a graph, support, word, or parameter
family.
