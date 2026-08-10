# Shallow hafnian Hessians give a two-deck P7 inverse

## Status

**Exact arbitrary-order characteristic-zero identity, rational P7 inverse,
and legal observability boundary.**  For a symmetric hollow graph on an even
vertex set `V`, put the principal two-deletion hafnians in a vector `c` and
the principal four-deletion hafnians in the edge-indexed Hessian `D`.  Then

```text
D a=(m-1)c,                         |V|=2m.             (1)
```

The Hessian is invertible on a nonempty Zariski-open set.  At the all-one
graph it is a nonzero scalar multiple of the adjacency matrix of the Kneser
graph `KG(2m,2)`, whose three eigenvalues are all nonzero in characteristic
zero.  Thus the two shallow deletion decks reconstruct every edge rationally
on `det D!=0`.

This identity aligns exactly with the established legal `P_7` mixed-root
sensor.  On any fixed eight-nonroot shore, the depth-five `H_4` labels form
`D`, while the depth-three `H_6` labels form `c`; hence one Hessian inversion
recovers all 28 shore edges.  One additional eight-by-eight partner system
using `H_4` sets through the omitted vertex recovers its star, and therefore
all 36 edges of the nine-nonroot graph.  On this open chart, once all supplied
`H_4` values are verified against the reconstructed graph, the 28 `H_6`
values contained in the chosen shore are automatic from (1).  A full-tower
test needs only the remaining 56 `H_6` checks and the nine `H_8` checks.

The alignment is sharp for the present sensors.  A projected Hessian identity
cannot reconstruct the 28 shore edges from fewer than 28 independent linear
combinations of `c`.  The established `P_6` chart exposes only `H_4`, and a
single four-root tensor cannot linearly select all 70 `H_4` and 28 `H_6`
labels because `98>3^4`.  `P_5` has no eight-shore; on a six-shore its
Hessian would require unexposed `H_2` edge labels.  Nonlinear compression or
additional synchronized jets could evade those linear boundaries and remain
unknown.

No search over graphs, supports, blockers, colour words, or coefficient
families is used.  The theorem is not a GHZ realization or obstruction.  A
hypothetical witness is not known to meet the simultaneous legal sensor,
Hessian, and star opens.  `P_7` and global Krenn--Gu remain
**UNKNOWN/UNRESOLVED**.

The arbitrary-order identity, Kneser etaleness, scalar Euler stress, and the
complete determinant-cleared representability criterion for a candidate
`(h,c,D)` jet are proved in
[`RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md`](../arbitrary-order/RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md).
Sections 1--2 below restate the identity and its projected rank consequence
only to make the legal P7 transfer self-contained.  The new content here is
the alignment with the existing P7 sensor, the one-shore/star inverse, and
the nine-shore descent theorem.

## 1. The shallow Hessian identity

Let `K` have characteristic zero, let `V` have order `2m`, `m>=2`, and let

```text
A=(a_ij)_(i,j in V),             a_ii=0,
h_S=haf A[S],                    h_empty=1.             (2)
```

Index vectors and matrices by the edge set `E=binom(V,2)`.  Define

```text
c_e=h_(V minus e),

D_(e,f)=h_(V minus (e union f))   if e intersect f=empty,
          0                        otherwise.           (3)
```

Thus `c` is the gradient of `h_V` and `D` is its edge Hessian:

```text
c_e=partial h_V/partial a_e,
D_(e,f)=partial^2 h_V/(partial a_e partial a_f).       (4)
```

### Theorem 1 (two-deck Hessian inversion)

For every `A`,

```text
D(A)a=(m-1)c(A).                                      (5)
```

On the principal open `det D(A)!=0`,

```text
a=(m-1)D(A)^(-1)c(A).                                 (6)
```

Consequently the principal two- and four-deletion hafnian arrays determine
the full named edge graph uniquely and rationally on a nonempty open set.

### Proof

Fix an edge `e`.  The polynomial `c_e=h_(V minus e)` is homogeneous of edge
degree `m-1`.  Its derivative with respect to `a_f` is zero when `e` and `f`
meet and otherwise is `h_(V minus (e union f))`.  Euler's homogeneous
identity therefore gives

```text
sum_(f in E) D_(e,f)a_f=(m-1)c_e.                     (7)
```

This is (5) row by row.  Inverting `D` gives (6).

It remains to show that the determinant open is nonempty.  At the all-one
graph `J`, every four-deletion cofactor equals

```text
alpha=(2m-5)!!,                                       (8)
```

so

```text
D(J)=alpha K_(2m),                                    (9)
```

where `K_n` is the edge-disjointness matrix, equivalently the adjacency
matrix of `KG(n,2)`.  If `B` is the vertex-edge incidence matrix and
`mathbf J` the all-one edge matrix, then

```text
K_n=mathbf J-B^T B+I.                                (10)
```

The edge space splits into the constant line, the `(n-1)`-dimensional
standard vertex-incidence space, and `ker B`.  Equation (10) acts on them by

```text
binom(n-2,2),              -(n-3),              1,   (11)
```

with multiplicities `1,n-1,binom(n,2)-n`.  All are nonzero for `n=2m>=4`.
Hence

```text
det D(J)
 =alpha^binom(n,2) binom(n-2,2) (-(n-3))^(n-1) !=0.  (12)
```

This proves nonemptiness over characteristic zero.  It also gives a second
open certificate, at a dense graph, independent of the matching-point
certificate for the cofactor-gradient map.

## 2. A sharp projected-data boundary

Suppose `D` is known and invertible, but only a linear projection

```text
y=P c                                                   (13)
```

of the two-deletion vector is exposed.  The projected form of (5) is

```text
P D a=(m-1)y.                                         (14)
```

### Proposition 2 (no reduction of the cofactor rank)

Within the linear Hessian inversion (14), `a` is uniquely determined if and
only if `P` has full column rank `binom(2m,2)`.

Indeed, multiplication by invertible `D` does not change rank:

```text
rank(PD)=rank P.                                      (15)
```

For an eight-shore this lower bound is 28.  It does not claim that a
different nonlinear use of the physical hafnian variety needs 28 readings;
it says precisely that projecting (5) cannot reduce the required cofactor
rank.

## 3. The one-shore P7 inverse

Let the nine named nonroots be

```text
N=U disjoint union {p},                  |U|=8.        (16)
```

Assume supplied named candidate decks

```text
(h_S)_(|S|=4,6,8).                                    (17)
```

On `U`, form

```text
c_e=h_(U minus e),
D_(e,f)=h_(U minus (e union f)) if e intersect f=empty,
          0                       otherwise.           (18)
```

These use exactly the 28 six-set labels contained in `U` and the 70 four-set
labels contained in `U`.  On `det D!=0`, put

```text
a_U=3D^(-1)c.                                         (19)
```

For the omitted star, index rows by triples `T subset U` and columns by
vertices `u in U`, and define

```text
S_U(A_U)[T,u]=a_(T minus {u})   if u in T,
                0               otherwise,            (20)
```

where `a_(T minus {u})` is the single edge on the remaining pair.  Expansion
by the partner of `p` gives

```text
S_U(A_U)(a_pu)_(u in U)=(h_({p} union T))_(|T|=3).    (21)
```

Use the eight cyclic triples

```text
T_i={i,i+1,i+2} mod 8,                  i=0,...,7.    (22)
```

At the all-one graph their selected matrix is the circulant incidence matrix
with first row `(1,1,1,0,0,0,0,0)` and determinant `3`.  Therefore its
determinant `sigma(A_U)` is not the zero polynomial.  On

`det D sigma!=0`, (19) followed by the selected rows of (21) recovers every
one of the 36 edges rationally.  At the all-one graph,

```text
det D=3^28 * 15 * (-5)^7 !=0,       sigma=3,          (23)
```

so the two opens meet.

### Theorem 3 (reduced P7 tower criterion)

On `det D sigma!=0`, reconstruct `A` by (19)--(21).  The supplied tower (17)
is the principal `H_4/H_6/H_8` tower of one graph if and only if:

1. `h_S=haf A[S]` for every one of the 126 four-sets `S`;
2. `h_S=haf A[S]` for the 56 six-sets `S` containing `p`;
3. `h_S=haf A[S]` for all nine eight-sets `S`.

No separate test is required for the 28 six-sets contained in `U`.

### Proof

Necessity is immediate.  Conversely, condition 1 makes the supplied matrix
`D` the actual four-deletion Hessian of the reconstructed `A[U]`.  Theorem 1
applied to `A[U]` gives

```text
D a_U=3 c_actual.                                     (24)
```

But reconstruction (19) gives `D a_U=3 c_supplied`.
Invertibility of `D` therefore forces

```text
c_supplied=c_actual.                                  (25)
```

Every six-set contained in `U` is `U minus e` for a unique edge `e`, so (25)
proves all 28 omitted six-set equations.  Conditions 2 and 3 prove the
remaining upper-deck values.  Hence the entire supplied tower is physical.

This replaces the eight oriented star inversions of the existing P7
criterion by one Hessian inversion and one star inversion, and reduces the
explicit upper partner checks from 84 to 56.  It does not assert lower
polynomial degree: `det D` has degree 28 in the four-deck entries.

If target incidence supplies a common Cramer numerator vector `v` and sensor
denominator `beta`, form `Dhat,chat` from the corresponding `v_4,v_6` entries.
Then

```text
a_U=3 Dhat^(-1) chat                                  (26)
```

because `Dhat=beta D` and `chat=beta c`; the common scale cancels.  The
physical checks are `v_S=beta haf A[S]`, and can be determinant-cleared.
Thus the inverse is compatible with the projective target-incidence line,
but it does not prove that such a line meets the open chart.  The sibling
arbitrary-order theorem gives the complete determinant-cleared `(h,c,D)`
equations, including the scalar stress, for each eight-shore; the present
criterion explains how those local systems recover and glue the full P7
nonroot graph.

## 4. Nine-shore shallow-Hessian descent

There is a coordinate-free alternative that uses all nine eight-shores and
needs no distinguished omitted-star solve.  For every `p in N`, put

```text
U_p=N minus {p},
c^(p)_e=h_(U_p minus e),
D^(p)_(e,f)=h_(U_p minus (e union f))                 (27)
```

for disjoint edges, with zero otherwise.  Write

```text
delta_p=det D^(p),
a^(p)=3(D^(p))^(-1)c^(p).                             (28)
```

Call the shore `p` locally physical when

```text
h_S=haf a^(p)[S]                  for every |S|=4 in U_p,
h_(U_p)=haf a^(p).                                    (29)
```

The local six-deck equations are deliberately absent: Theorem 1 makes them
automatic from the first line of (29) and `delta_p!=0`.

### Theorem 4 (shallow-Hessian descent)

On the common open `product_p delta_p!=0`, the supplied nine-vertex
`H_4/H_6/H_8` tower is physical if and only if:

1. every shore is locally physical in the sense of (29); and
2. the reconstructed graphs agree on every overlap:

   ```text
   a^(p)|_(U_p intersect U_q)=a^(q)|_(U_p intersect U_q). (30)
   ```

### Proof

If one global graph supplies the tower, Theorem 1 says that (28) recovers its
restriction to every shore.  Conditions (29)--(30) follow.

Conversely, (30) glues the local edge weights to one named graph `A` on `N`:
every edge lies in several eight-shores and receives the same value on their
overlaps.  Every four-set and every six-set is contained in an eight-shore.
The first line of (29) gives its four-hafnian, while Theorem 1 gives all
six-hafnians on that shore.  Finally, each eight-set is exactly one `U_p`, so
the second line of (29) gives all nine eight-hafnians.  Thus the entire tower
is the principal deck of `A`.

This is a finite affine descent theorem: the local inverse is the Hessian
chart, the overlap equalities are its cocycle conditions, and physical deck
realizability is local on the nine-shore cover once all `delta_p` are units.
It eliminates all 84 explicit `H_6` partner checks, replacing them by local
`H_4` realization and rational overlap agreement.  It is not claimed to be
a smaller polynomial system after denominators are cleared, and it says
nothing about the complement of the common determinant open.

## 5. Interface with the legal P5/P6/P7 sensors

The full five-root P7 expansion has deletion depths five, three, and one.
On nine nonroots these are exactly the named `H_4,H_6,H_8` decks.  The
established rank-219 companion chart therefore supplies every entry used in
(18) and (21) with its physical deletion label.  This is stronger than the
root-budget eligibility count and avoids the deletion-cube ambiguity: (5) is
an identity of one absolute principal deck, not an identification of hidden
direct and residual relative-response faces.

The lower cells do not presently align:

- `P_5` has seven nonroots.  On a six-shore the same construction would use
  `H_4` as `c` but the Hessian entries would be `H_2`, namely the unknown
  edges themselves.  Three-root deletion depths do not expose that edge
  deck, and there is no eight-shore.
- The established `P_6` full sensor sets all root-root blocks to zero and
  exposes the 70 `H_4` labels only.  An eight-shore Hessian additionally
  needs all 28 `H_6` labels.  Even allowing root-root blocks, simultaneous
  *individual linear selection* of all raw entries is impossible from one
  four-root tensor, because `70+28=98>81`.  A projected use still needs 28
  independent `H_6` combinations by Proposition 2.  Nonlinear physical
  compression or a synchronized stack of jets is not excluded.
- `P_7` has 243 root channels and an established legal chart selecting all
  219 shallow labels.  It is the first current cell where the complete
  Hessian data and the omitted-star data are simultaneously legal.

The arbitrary-residual tomography theorem reconstructs every depth on a
square permanental-compound chart.  The present theorem is different: it
uses only two adjacent shallow hafnian decks, but needs an even shore and an
invertible edge Hessian.  Once the graph is reconstructed, all deeper nested
cofactor and cumulant equations become predicted checks rather than input to
the inverse.

## Scope wall

Proved:

- the arbitrary-order identity `D a=(m-1)c`;
- the exact Kneser-spectrum certificate that `det D` is a nonempty open;
- rational edge recovery from the two shallow deletion decks;
- the full-rank lower bound for every projected version of this inversion;
- a P7 inverse using one eight-shore Hessian and one omitted-star system;
- automatic recovery of the 28 shore-contained `H_6` values after `H_4`
  realization;
- a necessary-and-sufficient open-chart tower test with only 56 explicit
  `H_6` checks;
- nine-shore Hessian descent with overlap gluing and no explicit `H_6`
  partner checks;
- exact compatibility with the established labeled P7 sensor;
- the current P5/P6 raw-label boundaries.

Not proved:

- that a hypothetical GHZ witness lies in the full P7 sensor open;
- that target incidence meets `det D sigma!=0`;
- that GHZ forces any reconstructed `H_4` equation;
- control of `det D=0` or `sigma=0` singular fibres;
- a nonlinear or multi-jet P6 realization of the projected identity;
- a P5, P6, or P7 restriction obstruction;
- the Krenn--Gu conjecture.

```text
arbitrary-order shallow Hessian identity:           EXACT;
two-deck edge inverse on det D:                      RATIONAL;
minimum projected C-rank on an eight-shore:         28;
P5 legal C/D alignment:                             ABSENT IN CURRENT JETS;
P6 complete raw C/D linear selection:               IMPOSSIBLE IN ONE JET;
P7 legal C/D alignment:                             PRESENT ON SENSOR OPEN;
P7 GHZ fibre meets Hessian/star open:                UNKNOWN;
P7/global Krenn--Gu:                                 UNRESOLVED.          (31)
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_shallow_hafnian_hessian_two_deck_inversion_and_p7_legal_sensor_interface.py
python claims/p7/audit_shallow_hafnian_hessian_two_deck_inversion_and_p7_legal_sensor_interface.py
python -m py_compile verify_shallow_hafnian_hessian_two_deck_inversion_and_p7_legal_sensor_interface.py audit_shallow_hafnian_hessian_two_deck_inversion_and_p7_legal_sensor_interface.py
uv run --with ruff ruff check verify_shallow_hafnian_hessian_two_deck_inversion_and_p7_legal_sensor_interface.py audit_shallow_hafnian_hessian_two_deck_inversion_and_p7_legal_sensor_interface.py
```

The primary replay verifies (5) symbolically on eight vertices, checks the
exact all-one Kneser determinant and cyclic-star determinant, reconstructs
the all-one nine-vertex graph, and audits the automatic `H_6` implication.
The independent no-import audit uses a separate integer hafnian recurrence,
Bareiss determinants, and rational elimination on a fixed nonconstant graph.
These are bounded exact audits of the displayed identities, not searches or
finite-field experiments.
