# Two-sided cycle faces and binary low-order cuts are compatible

## Status and parent implication

**Proved exact mechanism no-go over algebraic complex numbers.** In the
[common-star construction](PROTECTED_SCAFFOLD_COMMON_STAR_COMPONENT_TARGET_OBSTRUCTION.md),
there exists a legal nine-component array with an internal induced directed
three-cycle satisfying both localized cycle-face systems and every binary
singleton and same-color double-component target for one color pair. A
specified three-component cut still has a nonzero source.

This refutes the proposed implication that the two opposite cycle faces
from [PSCL](PROTECTED_SCAFFOLD_FULL_BINARY_CYCLE_LOCALIZATION.md), together
with this binary low-order subsystem, are already inconsistent. It does
not supply the third-color singleton or distinct-color double-component
equations. It does not refute the sharper three-color subsystem, the full
binary parent FB, CSQ4, or Krenn--Gu. The global status is **UNRESOLVED**.

The result has an exact primary replay and an independent physical-vertex
audit, reviewed by a separate agent in the same session. There is no Lean
formalization or separate-human refereeing. The
[parent attempt](../../docs/strategy/full-binary-parent-attempt-2026-09-20.md)
states the full quantifiers, CSQ4 supply, and common-star consumer. This is
an obstruction to a named synthesis step in that attempt, not a new case
census.

## Parameters exist and all denominators are nonzero

Choose any complex root s of

```
H(s)=3s^2+3s+1=0.
```

Then choose any root r of

```
P_s(r)=(3s+1)r^4+12(s+1)r^3-6(3s+1)r^2+12(s+1)r+3s+1=0,
```

and any root t of

```
E_(s,r)(t)=-2r(r+1)(3s+1)t^2
 +(3r^2s+3r^2-6rs-10r+3s+3)t+6(r+1)(2s+1)=0.           (1)
```

The linear factors s, 1+s, 2+3s, 3s+1 and 2s+1 are all coprime to H.
In particular P has degree four and nonzero constant coefficient. Its norm
from Q(s) is

```
N(r)=P_s(r) P_(-1-s)(r)=r^8+36r^6+134r^4+36r^2+1.       (2)
```

This polynomial is coprime to r(r+1)(r^2-1)(r^2+1). Every chosen r is
therefore nonzero and different from -1, and r^2+1 is nonzero. Both the
leading and constant coefficients of E are nonzero, so t exists and is
nonzero. This triangular construction proves existence without relying
on a numerical root or an ideal-membership check alone. Irreducibility
of P or E, distinct roots, and a choice of complex embedding are unnecessary.

## Actual shared-factor array

Index the components by

```
C={0,1,2}, I={3,4}, O={5,6}, D={7,8}.
q=-1-s, w=s/2, delta=-1-3w.
```

Every gadget has endpoint label (0,1) in its displayed orientation. Specify
the product matrix Q=A Hadamard B by

| Oriented support | Product |
| --- | --- |
| 0->1, 1->2, 2->0 | q |
| I->C and C->O, all pairs | w |
| I->O, all pairs | delta/2 |
| O->D and D->I, all pairs | -1/2 |

Put A=1 on every supported entry except

```
A[I,O]=t [[r,1],[1,r]],
```

and put B_uv=Q_uv/A_uv there and on every other supported entry. Set both
matrices to zero elsewhere. There are exactly 27 arcs, no loops, no opposite
arcs, and at most one label per component pair. The preceding nonvanishing
argument applies to q,w,delta,t and rt, so both actual factors on every
gadget are nonzero and A,B have exactly the same support.

Give each component its protected unit K4 matchings. A supported entry
provides the color-(0,1) edge between its two centers with weight A_uv,
and between its selected leaves with weight B_uv. All other crossing
entries vanish. This is a literal array on 36 physical vertices, with
no independent cofactor variables.

For arbitrary row and column sets define the actual source

```
Z(W,T)=sum_(J subset W, K subset T, |J|=|K|)
                         per(A[J,K]) per(B[J,K]).            (3)
```

Its empty term is one. The physical binary word with color 0 on S and
color 1 elsewhere has F(S)=Z(S,S^c), by the PSCS matching expansion.

## The simultaneous constraints

Every row and column of Q sums to -1. For cycle rows the sum is q+2w;
for I rows it is 3w+delta; for O and D rows it is -1. The column sums
have the same three forms. Hence all singleton cuts and their complements
vanish: F({u})=F(V\{u})=0.

For every T subset C with m=|T|,

```
Z(I,T)=Z(T,O)=1+m s+binom(m,2)s^2.
```

For m<3 this is (1+s)^m=(-q)^m; for m=3 it is H(s)=0. These are exactly
the two localized exterior cycle systems. Both live in the same A,B.
The closing blocks provide the exterior singleton constraints without
entering these contractions. Applying PSCL's matching-row deletion in
each orientation also gives both full binary faces: the exterior is held
all 0 for one face and all 1 for the other. In each face only its constant
cycle word has amplitude one; all seven other words have amplitude zero.

For the two-row cuts, after imposing only H(s)=0, direct expansion of
(3) gives the following exhaustive table. The first row index is in the
first named group and the second in the second group.

| Pair type | Number of cuts | F(pair) |
| --- | --- | --- |
| C,C | 3 | 0 |
| C,I | 6 | E_(s,r)(t)/(24rt) |
| C,O | 6 | 0 |
| C,D | 6 | 0 |
| I,I | 1 | P_s(r)/(16r^2) |
| I,O | 4 | 0 |
| I,D | 4 | 0 |
| O,O | 1 | 0 |
| O,D | 4 | 0 |
| D,D | 1 | 0 |

For the transposed array, exchange I and O in this table. Since
F_A,B(V\S)=F_(A^T,B^T)(S), this also accounts for every seven-element
cut. The table follows either by expanding the two permanents or the
shared-neighbor identity in PSCS. The primary program checks each of its
72 actual instances modulo H alone, before imposing P or E. Thus (1)
annihilates all 36 two-row and 36 two-column cuts. Together with the 18
singleton orientations, all 90 cuts of sizes 1,2,7,8 vanish.

This is a finite exhaustive cover of the asserted binary subsystem.
It is not a cover of all binary words or of the three-color S2 system.

## The remaining full-source failure is exact

Keep S={0,1,3} at color 0 and its complement at color 1. Expansion of
the same source and reduction by H,P,E gives

```
F({0,1,3})=(r^2+1)/(12r) != 0.                            (4)
```

The norm coprimality in (2) proves nonvanishing for every admitted parameter
choice. This word is `001011111`. The independent physical recursion has
49 supported perfect matchings for it and agrees with (3) identically
before specialization. Therefore the control fails the full binary target.
Moreover there are no color-2 gadgets at all, so changing one component
to color 2 in a color-0 background has source one. The missing third-color
antecedent is explicit, not an untested implicit promise.

## Evidence and sharper residual

The [primary replay](verify_common_star_two_sided_cycle_control.py) checks
support, existence/nonvanishing identities, both localized systems, the
unspecialized table, all 90 cuts, and the failed full source. It uses exact
Groebner reduction. The
[independent audit](audit_common_star_two_sided_cycle_control.py) imports no
primary module, uses successive univariate remainders in t,r,s instead of
a Groebner basis, and reconstructs the literal 36-vertex protected graph.
For all 90 asserted cuts and the exhibited failure, physical matching
recursion and a separately computed permanent expansion agree before
parameter specialization. The independent arithmetic still uses SymPy;
it is not a fully separate computer-algebra implementation.

The [review](../../docs/audits/COMMON_STAR_TWO_SIDED_CYCLE_REVIEW_2026-09-20.md)
pins the accepted files, checks the finite case cover and equation scopes,
and records the physical bridge. Regression controls deliberately preserve
Q while changing A,B, and reject discarding the unequal center/leaf
matchings. No numerical or modular evidence is used as a proof premise.

Adding the opposite cycle face and every binary first/second-order cut
does not close the PSCL residual. A closure must use further cuts that
change exterior components, or the missing coupling to the third color,
or an equivalent additional condition. In particular, it must explain
why the load-bearing source in (4) cannot be made zero while retaining
the full parent antecedent. Neither this control nor PSCL proves that
general incompatibility. FB, CSQ4 and arbitrary-witness coverage remain open.
