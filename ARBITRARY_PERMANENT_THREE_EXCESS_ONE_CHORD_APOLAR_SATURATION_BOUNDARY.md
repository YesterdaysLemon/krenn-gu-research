# Apolar saturation and backbone-alignment defect in the one-chord `2+1+0` profile

## Status

**Exact six-mode symbolic countermodel to a method, not to the conjecture.**
The aligned diagonal-`1+1+1` one-chord profile is excluded, but the same
termwise boundary quotient cannot be transferred formally to excess-mode
profile `2+1+0`.

There is an exact `m=6`, `21=3m+3` cell model with:

- the one-chord theta port and all three excess cells in the bare theta;
- mode/source degree ledgers `(3,4,5,3,3,3)` and `(4,4,4,3,3,3)`;
- local rank three at every input mode;
- a mandatory tricolour source cover and three pure perfect matchings;
- connected matching-covered support;
- a conformal exterior perfect matching with a unique selector word; and
- an exact zero mixed coefficient containing the three theta terms and the
  one-chord term.

Nevertheless one core boundary span is the entire three-dimensional input
space.  The tensor-product apolar quotient therefore annihilates both the
port tensor and every projected `Delta_3` direction.  The model misses the
global alignment condition by the smallest possible amount: every bare-
theta matching uses a cell outside the chosen pure-backbone union, but one
matching uses only one such cell.

Thus structural ledgers, one coefficient equation, conformality, and the
ordinary boundary quotient do not close the `2+1+0` branch.  A next proof
must force backbone-alignment defect zero or replace the ordinary quotient
with an operator that retains saturated boundary information.  No support
family or matching-tuple census is used.

## Two boundary invariants

For a core mode `a_i`, let

```text
B_i=span{covectors on cells from a_i to exterior sources}.
```

Define the **apolar survival profile**

```text
q(K)=(dim(V_0/B_0),dim(V_1/B_1),dim(V_2/B_2)).      (1)
```

If some coordinate of `q(K)` is zero, the product quotient
`pi_0 tensor pi_1 tensor pi_2` annihilates every three-port tensor.  This is
an exact certificate that the ordinary apolar-decoupling method has no
surviving core signal; it is not evidence that the original tensor vanishes.

Let `H=M_0 union M_1 union M_2` be a selected pure-backbone union and let
`PM(Theta)` be the three internal perfect matchings of the bare theta.
Define the **backbone-alignment defect**

```text
delta_H(Theta)=min_(T in PM(Theta)) |T-H|.           (2)
```

Even when the common exterior complement lies in `H`, `delta_H=0` is only a
necessary residual core condition for coefficient-induced alignment: the
cell labels must also induce one common backbone word.  The countermodel
below has `delta_H=1`, so it already fails on the first, setwise nonaligned
shell.

## The exact 21-cell model

Use modes

```text
a_0,a_1,a_2,r_0,r_1,r_2
```

and sources

```text
p_0,p_1,p_2,q_0,q_1,q_2.
```

All unmarked coordinate covectors have unit scalar weight.  Put the three
excess covectors on

```text
E_1=a_0p_1=e_0+e_1,
E_2=a_0p_2=-3e_0+e_2,
E_0=a_1p_0=e_1+e_2.                                (3)
```

The eight-cell one-chord core, missing `a_2p_1` and containing the added
chord `a_1p_2`, is

```text
a_0p_0:e_0,   a_0p_1:E_1,  a_0p_2:E_2,
a_1p_0:E_0,   a_1p_1:e_1,  a_1p_2:e_1,
a_2p_0:e_2,                    a_2p_2:e_2.          (4)
```

Add the four core-mode-to-exterior-source cells

```text
a_1q_0:e_0,
a_2q_1:e_0,   a_2q_0:e_1,   a_2q_2:e_2,            (5)
```

the four exterior-mode-to-core-source cells

```text
r_0p_0:e_1,   r_0p_1:e_2,
r_1p_1:e_0,   r_2p_2:e_0,                           (6)
```

and the five exterior cells

```text
r_0q_2:e_0,
r_1q_1:e_1,   r_1q_0:e_2,
r_2q_2:e_1,   r_2q_1:e_2.                           (7)
```

There are exactly

```text
8+4+4+5=21=3*6+3                                  (8)
```

cells.  The 18 coordinate cells form the mandatory source-colour cover;
the only cells outside it are (3).

The mode degrees are

```text
(3,4,5,3,3,3),                                     (9)
```

and the source degrees are

```text
(4,4,4,3,3,3).                                    (10)
```

At `a_0`, the forms `e_0,E_1,E_2` are independent.  At `a_1`, the forms
`e_0,e_1,E_0` are independent.  At `a_2` and every exterior mode, the three
coordinate forms occur.  Thus every local map has rank three.

## Pure backbones and matching-coveredness

The following are pure perfect matchings:

```text
M_0={a_0p_0,a_1q_0,a_2q_1,r_0q_2,r_1p_1,r_2p_2},
M_1={a_0p_1,a_1p_2,a_2q_0,r_0p_0,r_1q_1,r_2q_2},
M_2={a_0p_2,a_1p_0,a_2q_2,r_0p_1,r_1q_0,r_2q_1}.  (11)
```

Every used component in (11) is nonzero; in particular the `e_2` component
of `E_2` remains one despite its `-3e_0` component.

The support is matching-covered without enumerating its perfect matchings.
Contract the six edges of `M_0`.  Direct every other edge from its mode to
the contracted vertex owning its source.  The resulting six-vertex digraph
is strongly connected: every vertex reaches `a_0`, while `a_0` reaches
`r_1,r_2`, those reach `a_1,a_2,r_0`, and the displayed arcs close the
reverse routes.  Hence every nonmatching arc lies on a directed cycle.
Undoing the contraction turns that cycle into an `M_0`-alternating circuit,
so every physical edge belongs to a perfect matching.  The support is also
connected, and therefore matching-covered.

## Conformality and the exact mixed coefficient

The exterior graph has the perfect matching

```text
F={r_0q_2,r_1q_0,r_2q_1}.                          (12)
```

Its exterior word is `(0,2,2)`.  Each exterior mode has one cell of each
colour, so this word uniquely selects `F`.

At the core word

```text
(alpha_0,alpha_1,alpha_2)=(0,1,2),                 (13)
```

the four nonzero port permutation weights are exactly

```text
1, 1, -3, 1.                                       (14)
```

They are the three bare-theta matchings and the added-chord matching.  Their
sum is zero.  Since (12) is forced, the full six-mode coefficient at the
mixed word `(0,1,2,0,2,2)` is exactly zero, as required by `Delta_3` for
that one word.  This is a complete coefficient equation, not a selected
partial cancellation.  Other input words are not imposed, so the model is
not a full restriction.

## Exact apolar saturation

From (5),

```text
B_0=0,
B_1=span(e_0),
B_2=span(e_0,e_1,e_2)=V_2.                         (15)
```

Therefore

```text
q(K)=(3,2,0).                                      (16)
```

The tensor-product quotient kills every nonempty boundary sector, but it
also gives

```text
pi(T_K)=0,
pi(Delta_3)=0.                                     (17)
```

Thus no BER, flattening, or diagonal-direction contradiction survives this
ordinary quotient.  This is a zero-versus-zero method failure, not a
solution signature.

## Exact alignment defect

The three bare-theta matchings are

```text
T_0={a_0p_0,a_1p_1,a_2p_2},
T_1={a_0p_1,a_1p_0,a_2p_2},
T_2={a_0p_2,a_1p_1,a_2p_0}.                        (18)
```

For `H=M_0 union M_1 union M_2`, their defect sizes are respectively

```text
|T_0-H|=2,             |T_1-H|=1,             |T_2-H|=2. (19)
```

Hence `delta_H(Theta)=1`.  All theta edges are eligible at (13), and their
three matching monomials are nonzero, but no theta matching is itself the
distinguished mixed matching of the selected pure-backbone union.  This is
exactly the alignment hypothesis missing from the model.

## Proposed next object: the derived apolar boundary signature

The survival profile (16) shows what an ordinary quotient forgets.  A
possible replacement is to retain, at each port, the graded carrier

```text
D(B_i;V_i)=(V_i/B_i)
           direct-sum B_i[1]
           direct-sum Lambda^2(B_i)[2]
           direct-sum Lambda^3(B_i)[3].             (20)
```

rather than only its degree-zero quotient.  When `B_i=V_i`, the ordinary
piece vanishes but the top class `Lambda^3(B_i)[3]` does not.  Call the tensor
product of these carriers, together with a boundary-sector incidence
differential, the **derived apolar boundary signature**.

Equation (20) is a rigorous graded carrier, but a matching-compatible
differential and a target-rank obstruction have not yet been proved.  An
alternative route is to show directly that a hypothetical full restriction
forces `delta_H(Theta)=0`, using the exact coloured-extension criterion.
The countermodel proves that either route must use information absent from
the support/degree/conformality ledgers.

A later theorem constructs a different rigorous all-sector carrier: the
zeon boundary jet

```text
J_W(u,v)=per(W+(Zv)(u^T Y)).
```

Its degree-`k` squarefree coefficient is `k!` times the exact size-`k`
boundary response, so it retains the saturated top layer that (17) loses.
See `ARBITRARY_PERMANENT_THREE_EXCESS_ZEON_BOUNDARY_JET_THEOREM.md`.  This
packages every physical sector but still does not provide the missing
differential or target obstruction.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_one_chord_apolar_saturation_boundary.py
python audit_arbitrary_permanent_three_excess_one_chord_apolar_saturation_boundary.py
```

The primary verifier checks all 21 cells, source-colour cover, mode/source
degrees, local ranks, pure matchings, strong connectivity of the contracted
alternating digraph, conformality, the exact four-term zero, apolar profile,
and alignment defect.  The no-import audit independently checks the same
fixed symbolic witness.  Neither script searches support families or
matching tuples.

## Boundary

```text
21-cell structural model:                       EXACT;
one complete mixed coefficient:                 ZERO EXACTLY;
support connected and matching-covered:         YES;
conformal exterior selector:                    UNIQUE AND NONZERO;
apolar survival profile:                        (3,2,0);
backbone-alignment defect:                      1;
counterexample to ordinary quotient extension: YES;
coefficient-induced backbone alignment:         NO;
full P_6 -> Delta_3 restriction:                NOT CLAIMED;
derived apolar differential/obstruction:        NOT YET CONSTRUCTED;
all-sector zeon boundary carrier:                CONSTRUCTED LATER;
one-chord 2+1+0 global exclusion:               NOT PROVED;
global Krenn--Gu conjecture:                    UNRESOLVED.
```
