# A four-root P6 chart labels the complete four-hafnian deck

## Status

**Exact characteristic-zero sensor theorem, relative finite tomography, and
target-incidence boundary.**  In the two-residual `P_6` cell there are four
probe roots and eight named nonroots.  If every root--root block is zero, the
complete root tensor contains only the depth-four companion sector and hence
only the

```text
binom(8,4)=70                                           (1)
```

principal four-hafnian labels.  This note gives a legal fixed integer chart
on which those 70 companion columns have rank 70 in the `3^4=81` root tensor.
Thus every named four-hafnian is individually selectable on a nonempty open
set.  Combined with the full-rank Jacobian of the principal four-hafnian map,
the known companion blocks and full root tensor recover all 28 nonroot edges
up to finitely many algebraic branches on a nonempty product open.

The displayed chart is deliberately not promoted to a GHZ witness.  Adding
the three pure diagonal target columns raises its rank from 70 to 73, so its
sensor image meets the diagonal target space only at zero.  A target-compatible
full sensor must lie on a proper Schubert incidence locus.  In the ambient
Grassmannian of 70-planes in 81-space that locus has codimension nine; its
pullback to the legal companion family is not proved transverse or even
nonempty.

This construction is symbolic.  The proof uses one named 70-by-70 integer
minor and one named 73-by-73 augmented minor.  Their nonzero modular residues
are exact certificates that the corresponding integer determinants are
nonzero.  The replays construct only this fixed `81 x 70` operator; no
candidate supports, graphs, or parameter families are enumerated or sampled.

## 1. The four-root expansion with zero root--root blocks

Let `R={0,1,2,3}` be the roots and `N={0,...,7}` the nonroots.  After fixing
one vector at each nonroot, write

```text
h_(i,u) in V_i^*,             dim V_i=3,               (2)
```

for the root factor of the edge `i--u`, and let `L_ij` be the root--root
bilinear form.  For a four-set `D subset N`, define

```text
G_D=sum_(f:R -> D bijective) tensor_(i in R) h_(i,f(i)). (3)
```

The general root-matching partition has deletion depths four, two, and zero.
Set

```text
L_ij=0                    for every root pair.          (4)
```

Every term with one or two root--root edges then vanishes.  What remains is
the exact tensor identity

```text
T_R=sum_(D subset N, |D|=4) G_D H_(N minus D),          (5)
```

where `H_S` is the principal hafnian of the nonroot graph on the four-set
`S`.  Hence the companion synthesis map is

```text
Gamma_4:K^70 -> tensor_(i in R) V_i^*,
e_D |-> G_D.                                             (6)
```

All 70 named four-hafnians are observable relative to the known companions
exactly when `Gamma_4` is injective.

## 2. A legal integer companion chart

Put

```text
x_i=(1,1,1),                 w_i in {1,2,4,8},          (7)
```

using `w_i=2^i`.  Name the nonroots

```text
b_0,...,b_5,q_0,q_1.                                   (8)
```

For blocker `b_u`, set `t=u+1` and use

```text
h_(i,b_u)=e_0+t^(w_i)e_1+t^(2w_i)e_2.                  (9)
```

For `q_s`, set `t=7+s` and use

```text
h_(i,q_s)=e_0+t^(w_i)e_1-(1+t^(w_i))e_2.              (10)
```

Then

```text
h_(i,b_u)(x_i)=1+t^(w_i)+t^(2w_i) != 0,
h_(i,q_s)(x_i)=0.                                     (11)
```

Thus all six blockers are active and both `q_0,q_1` are genuine residual
nonblockers.  As usual, realize a root--nonroot edge by

```text
B_(i,u)=h_(i,u) tensor ell_u,       ell_u(z_u)=1,      (12)
```

and use its transpose in the reverse orientation.  Together with (4), these
are legal symmetric loopless graph blocks over the integers.  The nonroot
graph is an independent parameter family.

## 3. The named rank-70 certificate

Order the columns by the four-subsets of `{0,...,7}` in lexicographic order.
Order the 81 tensor rows by the ternary words

```text
0000,0001,...,2222.                                    (13)
```

Let `M` be the resulting integer `81 x 70` matrix.  With zero-based row
indices, take

```text
R_70={0,...,53,55,56,58,59,61,62,64,65,66,67,
      68,69,70,71,76,77}.                              (14)
```

The named square submatrix `M[R_70,*]` satisfies

```text
det M[R_70,*] mod 1,000,003 = 636,419 != 0,
det M[R_70,*] mod 1,000,033 = 549,813 != 0.            (15)
```

Either residue proves that this particular integer determinant is nonzero.
Therefore `Gamma_4` has rank 70 over `Q`, and hence over every
characteristic-zero field.  Since the determinant is polynomial in the
legal companion entries, the same rank holds on a nonempty Zariski-open
subset of the legal family (4), (11).

### Theorem 1 (complete P6 four-hafnian sensor)

There is a legal four-root, six-blocker, two-residual `P_6` companion chart
with zero root--root blocks on which all 70 named principal four-hafnian
cofactors have simultaneous individual linear selectors in the full root
tensor.

This is stronger than the earlier capacity inequality `70<=81`: it attains
the required rank while preserving the blocker/residual contractions.

## 4. The diagonal target-incidence boundary

Let

```text
Delta=span{e_0^(tensor 4),e_1^(tensor 4),e_2^(tensor 4)}. (16)
```

Append those three columns to `M`.  The pure words have row indices `0,40,80`.
For

```text
R_73={0,...,53,55,56,57,58,59,61,62,64,65,66,67,
      68,69,70,71,76,77,79,80},                        (17)
```

the corresponding augmented minor satisfies

```text
det [M|Delta][R_73,*] mod 1,000,003 = 420,326 != 0,
det [M|Delta][R_73,*] mod 1,000,033 = 680,957 != 0.    (18)
```

Consequently

```text
rank[M|Delta]=73,
im(Gamma_4) intersect Delta={0}                        (19)
```

at the displayed chart and throughout a nonempty open neighborhood.

For an arbitrary injective `Gamma_4`, let

```text
q:K^81 -> K^81/im(Gamma_4),          dim coker=11,
E:K^3 -> Delta subset K^81.                            (20)
```

Then a nonzero diagonal target lies in the sensor image exactly when

```text
rank(q E)<=2.                                          (21)
```

Equivalently, the 70-plane `im(Gamma_4)` meets the fixed 3-plane `Delta`.
In `Gr(70,81)` this is the special Schubert variety of codimension

```text
81-70-3+1=9.                                           (22)
```

Equation (18) proves that this incidence condition is proper after pullback
to the legal companion family.  It does **not** prove that the pullback has
codimension nine, is transverse, or contains a GHZ-compatible physical
point.

## 5. Relative finite edge tomography

Let `A` be the symmetric zero-diagonal matrix of the eight-nonroot graph and
consider

```text
F_4(A)=(H_S(A))_(|S|=4) in K^70.                       (23)
```

At the all-one graph, the derivative of `H_S` with respect to edge `a_ij`
is one exactly when `{i,j} subset S`.  Thus

```text
dF_4=W_(2,4)(8),                                       (24)
```

the 4-subset versus edge inclusion matrix.  Its 70 rows have rank 28 over
characteristic zero; the proof can be given directly by the usual subset-sum
kernel argument, and both replays check it independently.  Therefore the
four-hafnian morphism has image dimension 28 and is generically finite onto
its image.

The sensor determinant and the Jacobian determinant depend on independent
parameter families.  Their principal opens have nonempty product
intersection: take the companion chart (7)--(10) and the all-one nonroot
graph.

### Corollary 2 (relative finite P6 local-to-global tomography)

Fix, or retain as known base data, companion blocks in the sensor open set.
On a nonempty product open, the full four-root tensor recovers all 70 named
four-hafnians linearly, and those labels recover all 28 nonroot edges up to
finitely many algebraic branches.

This is not rational uniqueness.  In particular `A` and `-A` have the same
four-hafnian deck.  It also does not recover unknown companion parameters
from the tensor alone.

Nor is the first-deck Jacobian open forced by edge nonvanishing.  The exact
`Q(omega)` control in
`PINNED_H4_STAR_TORUS_CIRCUIT_GIRTH_AND_P6_CUBIC_ESCAPE.md` has all 21 shore
edges nonzero but a rank-six pinned matrix with a two-column kernel and
nonzero four- and six-deck entries.

## 6. The P5/P6/P7 shallow-sensor staircase

For the two-residual cells, the top deletion sector has the following exact
size.

| cell | roots | nonroots | top `H_4` labels | root channels | conclusion |
|---|---:|---:|---:|---:|---|
| `P_5` | 3 | 7 | 35 | 27 | complete linear deck impossible; compressed physical map generically finite |
| `P_6` | 4 | 8 | 70 | 81 | attained on the chart above |
| `P_7` | 5 | 9 | 126 | 243 | contained in the attained full 219-label sensor |

Thus `P_6` is the first balanced cell where the complete top deck fits and
is now legally realized.  The remaining obstruction is not raw capacity but
diagonal target incidence followed by physical hafnian integrability.
The nonlinear `P_5` refinement is proved in
`P5_COMPRESSED_H4_PHYSICAL_TOMOGRAPHY_AND_TARGET_TANGENT_BOUNDARY.md`.

## 7. Scope wall

```text
four-root deletion depths with L_ij=0:               ONLY DEPTH FOUR;
legal six-blocker/two-residual chart:                CONSTRUCTED;
complete 70-column P6 H4 sensor:                     INJECTIVE;
nonempty legal full-sensor open set:                 PROVED;
relative recovery of all 70 named H4 labels:         LINEAR UNIQUE;
relative recovery of 28 nonroot edges:               GENERICALLY FINITE;
global or rational edge recovery from H4:            FALSE/NOT CLAIMED;
explicit sensor meets nonzero diagonal target:       FALSE;
ambient full-sensor target incidence codimension:    NINE;
legal incidence pullback nonempty/transverse:        UNKNOWN;
GHZ fibre meets the sensor and H4-Jacobian opens:     UNKNOWN;
P5 complete top-deck sensor:                         DIMENSIONALLY IMPOSSIBLE;
P6 obstruction:                                      UNKNOWN;
global Krenn--Gu:                                    UNRESOLVED.        (25)
```

## Replay

```powershell
uv run --with sympy python claims/p6/verify_p6_four_root_full_h4_sensor_and_target_incidence_boundary.py
python claims/p6/audit_p6_four_root_full_h4_sensor_and_target_incidence_boundary.py
python -m py_compile claims/p6/verify_p6_four_root_full_h4_sensor_and_target_incidence_boundary.py claims/p6/audit_p6_four_root_full_h4_sensor_and_target_incidence_boundary.py
uv run --with ruff ruff check claims/p6/verify_p6_four_root_full_h4_sensor_and_target_incidence_boundary.py claims/p6/audit_p6_four_root_full_h4_sensor_and_target_incidence_boundary.py
```

The primary replay builds every companion column by a recursive permanent,
checks (15) and (18), and computes the exact inclusion rank (24).  The
independent standard-library audit rebuilds the columns by Ryser's formula,
uses the second prime in (15), (18), and checks (24) by rational elimination.
Neither replay imports the other or searches any graph, support, word, or
parameter family.
