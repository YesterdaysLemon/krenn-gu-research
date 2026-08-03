# Lower mixed-root jets label deletion cofactors exactly on an incidence-selector chart

## Status

**Exact characteristic-zero observability theorem, sharp chart, and proof-route
no-go.**  The lower mixed-root expansion does contain physically named
deletion classes.  It can therefore label an individual complementary
cofactor, but only when the corresponding aggregate companion form has a
linear selector modulo all the other companion forms.  The selector condition
is necessary and sufficient.

If it fails, the ambiguity is not merely a choice of notation.  The complete
fiber of cofactor arrays giving the same mixed jet contains

```text
ker(Gamma_I) tensor W,                                  (1)
```

where `Gamma_I` is the companion-incidence synthesis map and `W` is the
remaining blocker tensor space.  This translation group can change an
individual deletion cofactor without changing the observed jet.  Hence a
cofactor-span conclusion alone cannot legally be substituted into a labeled
nested-hafnian stress equation.

The boundary is sharp.  For every even residual order `q`, there is a legal
symmetric companion chart using `q` varied roots and `q` named residual
endpoints on which all `2^(q-1)` even deletion classes are simultaneously
labeled.  In natural bases its incidence matrix is diagonal, with entries

```text
(q-|A|-1)!!,                 A subset Q even,           (2)
```

and is therefore invertible in characteristic zero.  At `q=4` its determinant
is `3`; at `q=6` it is `15*3^15`.

This sharp chart is an existence theorem, not a forced chart theorem.  In the
standard balanced `P_m` cell with `r` roots and `q=m-r` residual nonblockers,
the `q=4` and `q=6` cells inside `P_5`, `P_6`, and `P_7` do not have `q`
varied roots.  A single common-core lower jet therefore cannot expose the
complete even cofactor tower by this or any other injective synthesis map.
Selected labels can still be observable, and several jets could help only
after an additional theorem identifies their different root-deletion cores.

Finally, if cross-depth observations expose the full square-free deletion
algebra and its multiplication, the arbitrary linear cofactor gauge collapses
to permutation and diagonal rescaling.  Present lower-frame theorems do not
expose that multiplication, so this conditional gauge collapse cannot yet be
imported into `P_5`, `P_6`, or `P_7`.

No graph support, blocker word, or parameter family is enumerated.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. The exact jet synthesis map

Let `I` be a set of `t>=2` varied roots.  Restrict the tangent at root `i` to
a two-plane `S_i` on which every differentiated root--blocker edge vanishes,
as in the lower mixed-root cofactor-frame theorem.  Let `Q` be the named fixed
nonblocker endpoints available to those roots, `|Q|=q`, and let `W` be the
tensor product of the blocker modes left free.

Every surviving partial companion matching uses a set `A subset Q` of
root--endpoint partners.  The remaining `t-|A|` roots pair internally, so

```text
mathcal A_(t,q)={A subset Q: |A|<=t and |A|=t mod 2}.  (3)
```

Grouping matchings by their physically named endpoint set gives the exact
tensor identity

```text
J_I=sum_(A in mathcal A_(t,q)) G_A tensor C_(I union A), (4)
```

where

```text
G_A in U_I^*,       U_I=tensor_(i in I) S_i,           (5)
```

is the aggregate root companion form and `C_(I union A) in W` is the single
complementary hafnian tensor after deleting `I union A`.

Introduce the deletion-label space

```text
L_I=K^{mathcal A_(t,q)},
Gamma_I:L_I -> U_I^*,       e_A |-> G_A.               (6)
```

Unlike an unnamed cofactor span, the basis vector `e_A` remembers the actual
endpoint deletion set.

### Theorem 1 (individual label criterion)

The value of `C_(I union A)` is determined by `J_I` and the known companion
forms if and only if there is a tangent tensor `u_A in U_I` such that

```text
G_B(u_A)=delta_(A,B)       for every B in mathcal A_(t,q). (7)
```

Equivalently,

```text
e_A^* in im(Gamma_I^*)
<=> every k in ker(Gamma_I) has k_A=0.                 (8)
```

All deletion labels are simultaneously determined if and only if `Gamma_I`
is injective.

### Proof

If (7) holds, contraction of (4) by `u_A` on its root tangent factor gives
exactly `C_(I union A)`.  Conversely, if some `k in ker(Gamma_I)` has
`k_A!=0`, then for any `w in W`

```text
C'_(I union B)=C_(I union B)+k_B w                     (9)
```

gives the same right side in (4), because

```text
sum_B G_B tensor k_B w=Gamma_I(k) tensor w=0.          (10)
```

Choosing `w!=0` changes the named `A` value.  This proves both directions.
Applying the criterion to every basis coordinate proves the final statement.

The full ambiguity fiber in (9) is exactly (1), since (4) applies
`Gamma_I tensor id_W` to the cofactor array.  Thus the obstruction persists
unchanged at arbitrary blocker surplus: enlarging `W` enlarges rather than
removes the invisible translation space.

## 2. The cofactor-span gauge

If the named companion columns themselves are forgotten and only a rank-`d`
factorization of `J_I` is retained, the factorization has the usual gauge

```text
Gamma -> Gamma S,
C     -> C S^(-T),                  S in GL(L_I),       (11)
```

which leaves the contracted tensor unchanged.  Endpoint-count grading can
reduce this to the product of general linear groups on the allowed
`|A|`-sectors, but it does not select the deletion basis inside a sector.

Equation (11) is why a statement such as

```text
span{C_(I union A):G_A!=0} contains span{D_0,D_1}     (12)
```

does not name either `A` carrying `D_0` or `A` carrying `D_1`.  The labeled
nested recurrence

```text
c_T=sum_s A_ps c_(T union {p,s})                       (13)
```

is not invariant under an arbitrary change of deletion-frame basis.  It may
be imposed on values recovered by (7), but not on an unspecified frame
satisfying only (12).

This is a logical no-go for deductions from the jet tensor alone.  The
perturbed arrays in (9) are not asserted to be simultaneous principal
hafnians of a second graph; principal-hafnian realizability is precisely the
extra nonlinear structure that the compound-open tomography theorem tests.

## 3. A legal simultaneous even-deletion chart

The selector requirement is not vacuous.  Let `q` be even, take `q` varied
roots `r_1,...,r_q`, and take `q` named endpoints `v_1,...,v_q`.  At root
`i`, choose tangent covectors `alpha_i,beta_i` forming a basis of `S_i^*`.
Choose lifts annihilating the fixed root vector, and choose endpoint
covectors `ell_i` with `ell_i(z_i)=1`.

Use the following legal symmetric companion blocks:

```text
r_i--r_j:  alpha_i tensor alpha_j,       i<j,
r_i--v_i:  beta_i tensor ell_i,
all other root--endpoint companion blocks: 0.          (14)
```

Reverse orientations carry transposes.  Every block in (14) vanishes when a
root is fixed, so it is compatible with pairwise-zero roots.  Projectively
constant root--blocker rows may be added independently; their restrictions
to `S_i` vanish and do not alter the chart.

Let `y_b=tensor_i y_(i,b_i)` be the tangent basis dual to
`alpha_i,beta_i`, with `b in {0,1}^q`.  Fix an even endpoint set `A`.  If
`v_i in A`, that endpoint has only neighbour `r_i`, forcing `b_i=1`.  If
`b_i=1` but `v_i notin A`, root `r_i` has no nonzero available edge.  Hence
the coefficient can be nonzero only when

```text
A={v_i:b_i=1}.                                         (15)
```

When (15) holds, the roots with `b_i=1` use their private endpoints.  The
remaining `q-|A|` roots form a complete unit-weight graph through the first
line of (14).  Since both `q` and `|A|` are even, their number is even, and

```text
G_A(y_b)=(q-|A|-1)!!,                                  (16)
```

with `(-1)!!=1`.  This proves (2).  Ordering the even subsets and the
even-weight tangent basis by (15) makes `Gamma` diagonal.  Therefore

```text
C_(I union A)=G_A(y_A)^(-1) J_I(y_A)                  (17)
```

is a legal, individually named cofactor value for every even `A`.

This construction is arbitrary-order and symbolic.  The double factorial
is the hafnian of a complete even unit matrix, so it is nonzero in
characteristic zero.  No individual matching needs to be listed.

## 4. Capacity boundary at `q=4`, `q=6`, and `P_5`--`P_7`

A fixed `t`-root jet can contain only endpoint deletions satisfying (3), and
its coefficient-form space has dimension `2^t`.  Consequently a family of
named classes can be simultaneously selected only if it is accessible by
parity and cardinality and has at most `2^t` members.

For the complete even tower of an even `q`, all `2^(q-1)` even subsets are
needed.  The top class `c_Q=1` is normalized in relative response, but at
`t=q-2` the other accessible even classes already number

```text
2^(q-1)-1 > 2^(q-2).                                  (18)
```

At `t=q-1` the jet has odd parity and sees only odd endpoint sets.  Hence the
first possible single-jet order for the entire even tower is `t=q`, and
Section 3 attains it exactly.

The first two cases are

```text
q=4:  eight even classes; first complete chart at four roots;
q=6:  thirty-two even classes; first complete chart at six roots.          (19)
```

In the standard balanced cell `r+q=m`, the relevant low permanent orders are

```text
cell       roots r     consequence for one common-core lower jet
P_5,q=4       1        no lower mixed even chart;
P_6,q=4       2        at most 4 selectors for 7 non-top even classes;
P_7,q=4       3        each even jet still has order at most 2;
P_6,q=6       0        no root jet;
P_7,q=6       1        only odd singleton endpoint deletions;
P_5,q=6       -        not a balanced cell.                         (20)
```

Thus the actual lower jets in these cells do not automatically furnish the
complete labeled input required to compare every recovered cofactor with one
GHZ jet tower.  This does **not** rule out an individual selector (7).  Nor
does it rule out stacking several maps

```text
Gamma_stack:L -> direct_sum_j U_(I_j)^*.              (21)
```

Such a stack labels all classes exactly when `Gamma_stack` is injective.
But the graph cofactors in its summands are `C_(I_j union A)` with different
root deletion sets.  They are not one common residual array `c_A` until a
separate contraction or synchronization theorem proves that identification.

This label issue is now the front gate to the nonlinear result in
`PRINCIPAL_FOUR_HAFNIAN_GENERIC_EDGE_TOMOGRAPHY_AND_P7_SINGULAR_FIBRE_BOUNDARY.md`.
That theorem can recover the nine-nonroot edge graph generically from its
126 principal four-hafnians, but only after those depth-five cofactors are
exposed with their physical deletion labels.  An unnamed 126-dimensional
span does not define the principal deck and is still subject to (11).

For arbitrary blocker surplus the same statements hold with `W` replaced by
the larger free blocker tensor space.  Neither the selector ranks nor the
sharp chart depend on `dim W`.

## 5. Cross-depth multiplication collapses the gauge conditionally

There is a precise way that additional cross-depth structure could repair the
label ambiguity.  Let

```text
Z_q=K[x_1,...,x_q]/(x_1^2,...,x_q^2),                 (22)
```

the graded square-free, or zeon, deletion algebra.  Its basis monomial `x_T`
records the named deletion set `T`, and multiplication records disjoint
union.

### Theorem 2 (square-free gauge rigidity)

Every graded algebra automorphism of `Z_q` in characteristic zero is
monomial on degree one:

```text
x_i |-> lambda_i x_(sigma(i)),                         (23)
```

where `sigma` is a permutation and every `lambda_i` is nonzero.  Consequently

```text
x_T |-> (product_(i in T) lambda_i) x_(sigma(T)).      (24)
```

If the top monomial is normalized, then `product_i lambda_i=1`.  If the
degree-one residual ports are already named, the permutation is removed; if
their scales are calibrated, the remaining diagonal gauge is removed too.

### Proof

Write the degree-one image of a generator as

```text
phi(x_i)=sum_j m_(j,i) x_j.
```

Because `phi(x_i)^2=0`,

```text
0=2 sum_(j<k) m_(j,i)m_(k,i) x_j x_k.                 (25)
```

The square-free degree-two monomials are independent and `2!=0`, so each
column of `M` has at most one nonzero entry.  Invertibility gives exactly one
nonzero entry in every row and column, proving (23).  Multiplicativity gives
(24), and the top normalization gives the product constraint.

This theorem reduces the unrestricted `GL(L)` ambiguity only when the
observations expose the multiplication in (22), including the degree-one
generators and their products.  An even cofactor span by itself is not the
full algebra.  The current lower mixed-root frame theorem supplies vector
spaces and inclusions such as (12), not the cross-depth products.  The formal
no-cube model in the root `m=7` boundary theorem shows this missing
partition-closed structure cannot be inferred from the present frames.

Thus square-free rigidity identifies an exact future route, not a completed
transfer: construct legally synchronized odd and even deletion charts with
observable multiplication, then use (23)--(24) to reduce their gauge before
testing the division-free nested stresses.

## 6. Scope wall

Proved:

- the necessary and sufficient individual deletion-label selector criterion;
- the exact invisible translation space `ker(Gamma_I) tensor W`;
- the full `GL` cofactor-frame gauge when deletion incidence is forgotten;
- a legal arbitrary-order symmetric chart labeling every even deletion class;
- sharp `q=4` and `q=6` determinant formulas;
- the single-common-core capacity boundary for the balanced `P_5`--`P_7`
  cells;
- arbitrary-surplus stability of the observability and ambiguity statements;
- monomial rigidity of the full square-free deletion algebra.

Not proved:

- that a hypothetical Krenn--Gu witness lies on any selector chart;
- an individual selector forced in every `P_5`, `P_6`, or `P_7` witness;
- identification of cofactors with different root-deletion cores in (21);
- exposure of square-free multiplication by the actual lower jets;
- calibration of the residual-port permutation and scaling gauges;
- a GHZ-labeled cofactor violating a nested stress or residual cumulant;
- unrestricted `P_5`, `P_6`, or `P_7` nonrestriction;
- the global Krenn--Gu conjecture.

```text
individual deletion label from one jet:      EXACTLY THE SELECTOR CRITERION;
cofactor span alone:                         LABEL-AMBIGUOUS;
ambiguity group at arbitrary surplus:        ker(Gamma) tensor W;
full even q=4 chart:                         CONSTRUCTED AT FOUR ROOTS;
full even q=6 chart:                         CONSTRUCTED AT SIX ROOTS;
full common-core chart in balanced P_5-P_7:  NOT SUPPLIED BY ROOT CAPACITY;
cross-depth square-free multiplication:      WOULD REDUCE GAUGE TO MONOMIAL;
actual exposure of that multiplication:      UNKNOWN;
global Krenn--Gu:                            UNRESOLVED.                 (26)
```

## Replay

```powershell
uv run --with sympy python verify_lower_mixed_root_jet_deletion_label_tomography_and_squarefree_gauge.py
python audit_lower_mixed_root_jet_deletion_label_tomography_and_squarefree_gauge.py
python -m py_compile verify_lower_mixed_root_jet_deletion_label_tomography_and_squarefree_gauge.py audit_lower_mixed_root_jet_deletion_label_tomography_and_squarefree_gauge.py
uv run --with ruff ruff check verify_lower_mixed_root_jet_deletion_label_tomography_and_squarefree_gauge.py audit_lower_mixed_root_jet_deletion_label_tomography_and_squarefree_gauge.py
```

The primary replay constructs the exact legal coefficient matrices at `q=4`
and `q=6`, checks the diagonal double-factorial formula and determinants,
verifies the kernel-translation ambiguity, and audits square-free monomial
gauge rigidity.  The independent standard-library audit uses a separate
matching recurrence, rational row reduction, and direct square-free
multiplication.  These are fixed small audits of the formulas; the selector,
complete-graph hafnian, and square-zero arguments prove arbitrary order
without enumerating graph supports, blocker words, or parameter families.
