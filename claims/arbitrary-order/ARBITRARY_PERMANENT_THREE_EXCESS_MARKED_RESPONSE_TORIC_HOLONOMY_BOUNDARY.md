# Marked response holonomy and the alternating-separator boundary

## Status

**Exact characteristic-zero response identity, exact alternating-path
separator theorem, exact tight support-side countermodel, and an exact
one-channel exception.**  The exterior matrix needed by the bare-theta
factor-`2` obstruction is precisely the degree-one zeon boundary response

```text
Omega=Y C_per(W) Z.                                 (1)
```

Neither matching delta-matroid exchange nor the permanental compound tower
forces a `2 x 2` minor of `Omega` to vanish.  More strongly, there is an
exact `m=5`, `3m+3`-cell graph with a mandatory tricolour cover, local rank
three, three pure backbones, connected matching-covered support, a conformal
bare theta, and an aligned three-term cancellation, but with a marked
exterior block of determinant one.

This graph is **not** a restriction `P_5 -> Delta_3`: the previously proved
`(0,2,2;1)` quotient obstruction detects a nonzero projected residue.  Thus
it proves that the support, colour, alignment, and matching structure alone
do not supply the cross-ratio; it does not refute any restriction theorem.

There is a positive replacement.  Relative to a unique empty exterior
matching, `Omega` is a weighted alternating-path matrix.  Its `2 x 2` minors
are signed sums of pairs of vertex-disjoint alternating paths.  Hence a
single alternating separator forces rank one.  When the exterior has one
mode-source pair, this separator is automatic and `Omega` is an outer
product.  This covers the exterior response algebra at `m=4`, but the
separate legal target-marking problem remains open.

The global Krenn--Gu conjecture remains unresolved.

## Identification with the zeon jet

Use the boundary block notation

```text
          P   Q
       +---------+
 A     | X   Y   |
 R     | Z   W   |.                                (2)
       +---------+
```

For core terminals `a_i,p_j`, the aggregate elementary exterior response is

```text
Omega_ij
 =sum_(q in Q,r in R)
    Y_iq Z_rj per(W_(delete r,delete q))
 =(Y C_per(W) Z)_ij.                               (3)
```

In the zeon boundary jet

```text
J_W(u,v)=per(W+(Z v)(u^T Y)),                      (4)
```

this is exactly

```text
[u_i v_j]J_W=Omega_ij.                             (5)
```

Equivalently, in the permanental compound tower,

```text
Omega=R^(1)=P_1(Y) D_1(W) P_1(Z).                 (6)
```

For the bare theta, if `Q_ij` denotes its internal pair-deletion cofactor,
the marked global sector response is the Hadamard product

```text
mathcal_R_ij=Q_ij Omega_ij.                        (7)
```

These are exact identities for one marked sector.  They do not assert that
the complete unmarked restriction tensor splits degree by degree.

## Why the compound tower does not give the cross-ratio

Over a field, (6) gives only

```text
rank(Omega)<=min(rank(Y),rank(C_per(W)),rank(Z)).   (8)
```

Each factor may have rank at least two.  Moreover the next zeon layer
`R^(2)` is a **permanental** compound response:

```text
R^(2)=P_2(Y) D_2(W) P_2(Z).                        (9)
```

It is not the ordinary exterior square `wedge^2 Omega`.  Consequently a
nonzero degree-two boundary response neither equals nor forces a `2 x 2`
minor of `Omega`.

The matching delta-matroid controls only which coefficients in (4) have
feasible support.  It carries no equality between specialized complex
weights of different elementary sectors.

## Exact abstract two-channel counterfamily

Take two exterior modes and sources and put

```text
W=I_2,             Y=I_2,
Z=[1 s]
  [t 1],           s,t!=0,       s t notin {1,-1}. (10)
```

Since `C_per(I_2)=I_2`, equation (1) gives

```text
Omega=[1 s]
      [t 1],
det(Omega)=1-s t!=0.                               (11)
```

Every elementary response is nonzero.  The size-two boundary response is

```text
R^((2))_(12,12)=per(Z)=1+s t!=0.                  (12)
```

The complete two-port zeon jet is therefore

```text
J_W=1+sum_(i,j=1)^2 Omega_ij u_i v_j
       +2(1+s t)u_1u_2v_1v_2.                     (13)
```

Its feasible terminal family is the empty set, all four balanced elementary
pairs `{a_i,p_j}`, and the full four-terminal set.  This is an even matching
delta-matroid.  Thus support exchange, nonvanishing of every response layer,
and the exact zeon factorial are all compatible with a nonzero toric minor.

This first family is a boundary-response gadget, not a tight coloured
support or a `P_m -> Delta_3` restriction.  The next construction upgrades
the no-go to all presently isolated **support-side** hypotheses.

## Exact tight support-side countermodel at `m=5`

Let the modes be

```text
A={a_0,a_1,a_2},       R={r_1,r_2},
```

and the sources be

```text
P={p_0,p_1,p_2},       Q={q_1,q_2}.
```

Write `e_0,e_1,e_2` for the coordinate covectors and put

```text
L_0=e_0+e_1+e_2,
L_1=e_0+2e_1+e_2,
L_2=e_0+e_1-2e_2.                                 (14)
```

The seven-cell core is the bare theta

```text
X_Theta=[ L_0  L_1  L_2 ]
        [ e_0  e_0   0  ]
        [ e_1   0   e_1 ].                         (15)
```

Add the eleven exterior cells

```text
A--Q:
 a_1q_1:e_1,   a_1q_2:e_2,
 a_2q_1:e_2,   a_2q_2:2e_0;

R--Q:
 r_1q_1:e_0,   r_2q_2:e_1;

R--P:
 r_1p_0:e_2,   r_1p_1:e_1,   r_1p_2:e_2,
 r_2p_1:e_2,   r_2p_2:e_0.                         (16)
```

There are exactly `18=3m+3` physical cells.  The mode degrees are
`(3,4,4,4,3)` and the source degrees are `(4,4,4,3,3)`.  At every source,
the coordinate cells in (15)--(16) contain one mandatory cell of each
colour.  Every mode has colour rank three; for `a_0` this follows from

```text
det[L_0 L_1 L_2]=-3!=0,                            (17)
```

and it is immediate from the coordinate cells at the other modes.

Three pure backbones are

```text
M_0={r_1q_1,a_2q_2,a_0p_0,a_1p_1,r_2p_2},
M_1={a_1q_1,r_2q_2,a_0p_0,a_2p_2,r_1p_1},
M_2={a_2q_1,a_1q_2,a_0p_0,r_1p_2,r_2p_1}.         (18)
```

Their full pure-word coefficients are respectively `4,2,-1`, so none is
cancelled.  The matching

```text
F={a_0p_0,a_1p_1,a_2p_2,r_1q_1,r_2q_2}           (19)
```

lies in `M_0 union M_1 union M_2` and carries the mixed labels
`(2,0,1,0,1)` at `(a_0,a_1,a_2,r_1,r_2)`.  At that word every exterior cut
cell is ineligible, and the only three physical terms are the three theta
matchings with values

```text
L_0[2], L_1[2], L_2[2] = 1,1,-2.
```

Hence the aligned mixed coefficient is exactly zero.

The core is conformal because its complement has the perfect matching
`{r_1q_1,r_2q_2}`.  The whole support is connected and matching-covered
without listing its perfect matchings.  Contract (19), and orient a non-`F`
cell from its mode to the mode whose `F`-edge meets its source.  The arcs are

```text
a_0 -> {a_1,a_2},
a_1 -> {a_0,r_1,r_2},
a_2 -> {a_0,r_1,r_2},
r_1 -> {a_0,a_1,a_2},
r_2 -> {a_1,a_2}.                                  (20)
```

This digraph is strongly connected.  Every non-`F` cell therefore lies on
an `F`-alternating cycle, and toggling that cycle gives a perfect matching
containing the cell.  The cells of `F` already lie in a perfect matching.

The core-to-exterior cut has colours `{0,1,2,2}`, while the exterior-to-core
cut has colours `{0,1,2,2,2}`.  The surplus is the colour-`2` token at the
unique degree-four exterior mode, exactly the `(0,2,2;1)` generalized cut
ledger.

Now take a scalar marked specialization on entrance rows `{a_1,a_2}` and
exit columns `{p_0,p_2}`, transverse to the aligned coordinate word.  Use
one common direction at each exposed mode:

```text
h_(a_1)=e_1+e_2,             h_(a_2)=e_0+e_2,
h_(r_1)=e_0+e_2,             h_(r_2)=e_0+e_1.
```

This single multilinear evaluation simultaneously produces the displayed
`Y,W,Z`; no split base/tangent convention is being used.  It is an exact
scalar specialization of the marked exterior response, but is **not**
claimed to be the still-missing target-compatible marking.  The exit
columns `{p_0,p_2}` are the cofactor block in the zero-defect signless
relation anchored by the core cell `a_0p_1`.  At the aligned coordinate word
itself the cut matrices are zero; equation (21) is deliberately transverse.
Equations (15)--(16) give

```text
Y=[1 1],        Z=[1 1],        W=I_2,
  [1 2]          [0 1]

Omega=Y Z=[1 2],             det(Omega)=1.         (21)
          [1 3]
```

Thus even the complete support-side package does not force exterior toric
holonomy.

There is no contradiction with the earlier `(0,2,2;1)` exclusion.  Quotient
the three core rows by

```text
B_0=0,       B_1=span(e_1,e_2),
B_2=span(e_0,e_2).                                 (22)
```

The projected target is zero, but the theta leaves

```text
(L_0+L_1+L_2) tensor e_0 tensor e_1
 =(3e_0+4e_1) tensor e_0 tensor e_1 !=0.           (23)
```

The unique empty complement multiplies (23) by a nonzero scalar.  This is
an exact certificate that the countermodel fails `P_5 -> Delta_3`.

## Invented theory: alternating-path transmission

Assume the eligible `R--Q` graph has a unique perfect matching `F_R`, with
weight `w(F_R)`.  Contract its matched edges.  Orient every remaining
eligible `R--Q` edge in the alternating direction, every `A--Q` edge into
the contracted network, and every `R--P` edge out toward `P`.  Call the
resulting directed network `D_F`.

A directed interior cycle would lift to an `F_R`-alternating cycle and
produce a second empty matching.  Hence `D_F` is acyclic.  Symmetric
difference with `F_R` gives a weight-preserving bijection between an
`(a_i,p_j)` pair-sector matching and a directed path `a_i -> p_j`.  With the
usual alternating edge-gain convention,

```text
Omega_ij=w(F_R) sum_(pi:a_i -> p_j) gain(pi).       (24)
```

The Lindstrom--Gessel--Viennot path-minor identity therefore gives

```text
det Omega_(I,J)
 =w(F_R)^2 sum_(vertex-disjoint path pairs)
    sign(sigma) gain(pi_1) gain(pi_2).              (25)
```

This proves the **alternating-separator theorem**:

> If no two vertex-disjoint `F_R`-alternating paths join the selected two
> entrance ports to the selected two exit ports, then the corresponding
> `2 x 2` minor of `Omega` is zero.

A particularly transparent sufficient condition is one contracted
`F_R`-edge through which every relevant alternating path passes.  Every path
then decomposes uniquely at that vertex, so

```text
Omega_ij=w(F_R) u_i v_j,                            (26)
```

and the entire selected response has rank at most one.  By directed Menger
theory, the support-side problem is now an alternating vertex-connectivity
problem: force connectivity at most one across the marked port block.

If localization removes all nonmatching interior `R--Q` cells, `D_F` has
depth one.  Write the matched-edge weights as `f_k`, the entrance matrix as
`V`, and the exit matrix as `U`.  Then

```text
Omega=w(F_R) V diag(f_k^(-1)) U.                   (27)
```

Cauchy--Binet makes the obstruction completely local:

```text
det Omega_(I,J)
 =w(F_R)^2 sum_(k<l)
   det V_(I,{k,l}) det U_({k,l},J)/(f_k f_l).       (28)
```

Thus it suffices to prove, for every channel pair, that the entrance minor
or the exit minor vanishes.  The tight countermodel (14)--(23) shows that
the present colour and degree ledgers do not do this by themselves.

## Exact one-channel exception

If the exterior has one mode and one source, then `W=[w]` and

```text
C_per(W)=[1],             Omega=Y Z.               (29)
```

Thus `rank(Omega)<=1`, and every marked `2 x 2` block obeys

```text
Omega_11 Omega_22=Omega_12 Omega_21.               (30)
```

For the Krenn--Gu port decomposition, one exterior pair means `m=4`.
Therefore the exterior half of the bare-theta sign-clash obstruction is
automatic at order four.  What is still missing is a legal coefficient or
marked-sector operator proving that the corresponding target block satisfies
the alternating Segre equation.  Equation (30) alone is not an exclusion.

More generally, (30) follows on a chosen block whenever one relevant factor
in (1) has rank at most one.  The alternating-separator theorem supplies the
graph-theoretic version of this **single-channel cofactor separator**.

## Literature boundary

The directed-network translation is the classical acyclic
Lindstrom--Gessel--Viennot mechanism.  Talaska's
[*Determinants of weighted path matrices*](https://arxiv.org/abs/1202.3128)
extends the path-minor formula beyond acyclic networks; uniqueness of the
empty matching keeps the present application in the elementary acyclic
case.

Planarity does not imply (30).  Postnikov's
[*Total positivity, Grassmannians, and
networks*](https://arxiv.org/abs/math/0609764) uses planar boundary
measurements precisely to parametrize Grassmannian cells with nontrivial
minors.  Planarity organizes the signs and boundary order; it does not
remove two-channel transmission.

The dimer and matchgate translations point to the same missing datum.
Kenyon's [*Lectures on Dimers*](https://arxiv.org/abs/0910.3129) relates
dimer correlations to inverse Kasteleyn entries.  Boundary monomer
partition functions obey Pfaffian rather than rank-one relations under the
hypotheses of Giuliani--Jauslin--Lieb,
[*A Pfaffian formula for monomer-dimer partition
functions*](https://arxiv.org/abs/1510.05027).  Cai--Gorenstein's
[*Matchgates Revisited*](https://arxiv.org/abs/1303.6729) characterizes
matchgate signatures by matchgate identities.  In each language, a
four-terminal or two-path sector is an additional term; its separate
vanishing, not membership in the ambient theory, is what collapses the
response to rank one.

The correct next target is therefore not ambient planarity or another
support exchange axiom.  It is one of:

1. force an alternating articulation for one cofacial theta block from the
   **full restriction equations**;
2. prove cancellation of the Cauchy--Binet channel-pair sum (28); or
3. construct the legal target marking and use its additional equations to
   eliminate every full-rank response.

## Scope wall

```text
Omega equals degree-one zeon response:                    PROVED;
Omega=Y C_per(W) Z compound factorization:                PROVED;
delta-matroid exchange forces det(Omega)=0:                FALSE;
nonzero higher response forces det(Omega)=0:               FALSE;
exact abstract two-channel full-rank family:               CONSTRUCTED;
tight aligned support structure forces det(Omega)=0:       FALSE;
exact m=5 tight support-side countermodel:                  CONSTRUCTED;
countermodel is a P_5 -> Delta_3 restriction:              FALSE;
unique complement gives alternating-path response:         PROVED;
alternating articulation implies rank-one response:         PROVED;
one exterior channel / m=4 exterior cross-ratio:           PROVED;
full restriction forces an alternating separator:          UNKNOWN;
legal target marked Segre selector:                        UNKNOWN;
bare-theta exclusion:                                     UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_arbitrary_permanent_three_excess_marked_response_toric_holonomy_boundary.py
python audit_arbitrary_permanent_three_excess_marked_response_toric_holonomy_boundary.py
```

The primary verifier reconstructs `C_per(W)`, the abstract response family,
the exact tight graph ledger, pure backbones, aligned cancellation,
alternating-cycle certificate, full-rank marked block, nonzero quotient
residue, and the one-channel outer-product identity.  The independent
no-import audit rebuilds the physical graph and checks the same decisive
incidences without importing the primary verifier.  No tuple search,
physical-support census, word census, or perfect-matching family is
enumerated.
