# Four-residual even Wick tower and the P6 synchronization interface

## Status

**Exact characteristic-zero necessary-and-sufficient theorem for the complete
even residual tower on four named residual vertices.**  The full residual
loop-hafnian theorem uses all residual depths, including the four singleton
and four triple responses.  The parity-compatible `P_6` selector naturally
points instead to the empty response, the six pair responses, and the full
four-residual response.  The odd depths can be eliminated exactly.

After division by the common residual-absent moment `M`, every pair response
has the form

```text
F_ij=a_ij+L_i L_j,                                    (1)
```

where the six `a_ij` are the residual edges and the four `L_i` are the same
port-linear forms in every pair.  Put `P_ij=F_ij-a_ij`.  Then

```text
P_12 P_34=P_13 P_24=P_14 P_23,                        (2)
```

and the full normalized response is forced by

```text
F_1234=haf(a)+sum_(ij) a_ij P_(Q minus {i,j})+P_12 P_34. (3)
```

Conversely, (1) for four common linear forms, together with (3), reconstructs
one graph producing the entire displayed even tower.  Thus this is a
complete representability criterion, not only a necessary rank bound.

There is a division-free form.  If

```text
N_ij=Z_ij-a_ij M,                                     (4)
```

then (2) holds with `P` replaced by `N`, and

```text
M Z_1234
 =haf(a) M^2+M sum_(ij) a_ij N_(Q minus {i,j})+N_12 N_34. (5)
```

Equations (2) and (5) alone are not sufficient: the six pair forms must have
the **common four-row factorization** (1).  A fixed five-port pentad control
passes (2) and (5) trivially but cannot factor even one of its pair forms.

This theorem gives an exact new obstruction interface for the clean `P_6`
four-residual selector.  It does not claim that an ordinary Krenn--Gu target
coefficient exposes the complete optional-port response polynomials needed
to multiply the terms in (2) and (5).  Current root polarization labels the
six residual pair deletions, but a fixed blocker-present tensor coefficient
does not automatically supply all blocker-subset companions occurring in a
square-free product.  Legal synchronized exposure remains **UNKNOWN**.

No graph, support, colour word, parameter set, finite field, or numerical
point is searched.  The proof is an identity in a square-free algebra over
an arbitrary characteristic-zero field.

## 1. Response algebra

Let `K` be a characteristic-zero field, let `U` be a finite set of scalar
ports, and put

```text
A_U=K[x_u:u in U]/(x_u^2:u in U).                     (6)
```

Let `Q={1,2,3,4}` be four named residual vertices.  Write

```text
Q_B=sum_(u<v) B_uv x_u x_v,
L_i=sum_u R_iu x_u,
Q_A=sum_(i<j) a_ij y_i y_j.                           (7)
```

In the square-free algebra on both the `x` and `y` variables, the matching
response is

```text
E(x,y)=exp(Q_B+sum_i y_i L_i+Q_A).                    (8)
```

For `S subset Q`, let

```text
Z_S=[y_S]E,                 M=Z_empty=exp(Q_B),
F_S=M^(-1)Z_S.                                      (9)
```

The inverse exists because the constant coefficient of `M` is one.  All
exponentials and inverses are finite in the nilpotent square-free ideal.

The data retained in the **even tower** are

```text
M,        (Z_ij)_(1<=i<j<=4),        Z_1234.          (10)
```

No singleton or triple residual response is assumed observable.

## 2. Pair curvature and common-row compatibility

### Proposition 1 (normalized pair form)

For every residual pair,

```text
F_ij=a_ij+L_i L_j.                                   (11)
```

In particular, `a_ij` is the constant coefficient of `F_ij`, while

```text
P_ij=F_ij-a_ij=L_i L_j                               (12)
```

is homogeneous of port degree two.

### Proof

After removing `M`, extract `y_i y_j` from

```text
exp(Q_A+sum_r y_r L_r).
```

The two residual vertices are either paired by their residual edge, giving
`a_ij`, or each uses one residual--port incidence, giving `L_iL_j`.  These
are the only possibilities.

### Corollary 2 (even tetrads)

The three complementary products agree as in (2).

### Proof

Each product is the same element

```text
L_1 L_2 L_3 L_4
```

of `A_U`.  The equality is valid on coordinate boundaries and requires no
division or chosen nonzero port.

The word **common** in (12) is essential.  Checking each `P_ij` against an
unrelated two-factor model loses the synchronization among the four rows.
The six forms together lie in the image of the invented square-free map

```text
(L_1,L_2,L_3,L_4) |-> (L_i L_j)_(i<j).               (13)
```

Call this image the **four-row even Wick variety**.  It is a block-valued
analogue of a one-factor/two-row moment parametrization; the quotient
`x_u^2=0` hides the diagonal coefficients and makes the existing factor-
analysis pentads part of its individual-pair ideal.

## 3. The full four-residual law

Put

```text
h=haf(a)=a_12 a_34+a_13 a_24+a_14 a_23.              (14)
```

### Theorem 3 (even Wick top identity)

The normalized full response obeys (3), where the sum ranges over all six
residual edges and `P_(Q minus {i,j})` is the complementary pair form.

Equivalently,

```text
F_12 F_34+F_13 F_24+F_14 F_23-F_1234
 =2 P_12 P_34.                                       (15)
```

### Proof

Extract `y_1y_2y_3y_4` after division by `M`.  There are three disjoint
types of partial residual matching.

1. Two residual edges contribute `h`.
2. One residual edge `{i,j}` and two residual--port incidences at the
   complementary vertices contribute `a_ij L_kL_l=a_ijP_kl`.
3. Four residual--port incidences contribute `L_1L_2L_3L_4=P_12P_34`.

Their sum is (3).  Expanding the three products in the left side of (15)
counts the first two types once and the four-linear term three times.
Subtracting (3) leaves twice that term.

Equation (15) is an even-depth curvature law.  It is not the assertion that
the ordinary fourth cumulant vanishes: the hidden singleton forms survive
through the decomposable right side.

### Corollary 4 (division-free tower equations)

With (4),

```text
N_12N_34=N_13N_24=N_14N_23,                          (16)
```

and the top response satisfies (5).

### Proof

Equations (9), (11), and (12) give

```text
N_ij=M P_ij.                                         (17)
```

Multiply (2) by `M^2`.  Multiplying (3) by `M^2`, then using
`M F_1234=Z_1234` and (17), gives (5).

## 4. Complete even-tower criterion

### Theorem 5 (necessary and sufficient representability)

A family (10) is the complete even residual response tower of a loopless
port/four-residual graph if and only if all of the following hold.

1. `M` has constant coefficient one and `log M` is a port quadratic.
2. For every pair, `F_ij=M^(-1)Z_ij` has only port degrees zero and two.
3. Writing `a_ij=[1]F_ij` and `P_ij=F_ij-a_ij`, there are four port-linear
   forms `L_i` satisfying all six common equations `P_ij=L_iL_j`.
4. The normalized top response satisfies (3).

### Proof

Necessity is Proposition 1 and Theorem 3.

Conversely, condition 1 reconstructs the port--port weights as the
coefficients of `log M`.  Condition 3 reconstructs one residual--port row
from each `L_i`, and the constants in condition 3 reconstruct the six
residual edges.  Let `E` be the matching exponential (8) of this graph.
Proposition 1 says its six pair responses are exactly the proposed
`Z_ij=M(a_ij+P_ij)`.  Theorem 3 and condition 4 say its full response is the
proposed `Z_1234`.  Its empty response is `M` by construction.  Hence it
realizes the entire family (10).

There can therefore be no stronger scalar obstruction using only the
complete even tower: once conditions 1--4 hold, a graph has been explicitly
reconstructed.

## 5. Why the displayed polynomial shell is not sufficient

The complementary-product equations (16) and the top law (5) do not replace
the common-row factorization in Theorem 5.

Take five ports and set `M=1`, every `a_ij=0`, every `P_ij=0` except
`P_12`.  Give `P_12` the off-diagonal coefficient pattern

```text
k_01=k_02=k_13=k_24=k_34=1,
all other k_uv=0.                                    (18)
```

This is the named five-cycle monomial of the factor-analysis pentad.  Its
pentad is exactly one, so no two linear forms have product `P_12` in the
square-free port algebra.  Nevertheless every complementary product in
(2) is zero, and choosing `F_1234=0` satisfies (3).  Thus the visible
quartic equations pass while representability fails.

This control also explains how the one-depth pentad and the cross-depth even
Wick law cooperate:

- the pentad tests an individual pair form;
- the common-row equations synchronize all six pair forms;
- the top law synchronizes the pair layer with the full residual layer.

None subsumes the other two.

## 6. P6 interface and observability boundary

The legal four-root selector has exactly the right residual parity.  On a
clean four-residual window it can, conditionally, invert a `2 x 3`
permanental fan and label all six pair-deletion tensors.  A compatible
four-root permanent also labels the unique four-deletion tensor.  The
original undeleted coefficient supplies the top residual response.

If those tensors are supplied as complete response polynomials over one
common optional-port set, Theorem 5 gives a complete physical
integrability test before the target Segre equations are imposed:

```text
clean P6 deck
 -> normalize by the four-deletion response M
 -> test six common products P_ij=L_iL_j
 -> test the even top law (3)
 -> intersect with the three target Segre pullbacks.                (19)
```

The current Krenn--Gu coefficient does not automatically provide the first
arrow at full port depth.  Products such as `N_12N_34` use every partition
of a port subset between two response factors.  A tensor coefficient with
all blockers present supplies only one total subset, not the lower blocker
subsets in that convolution.  Ordinary local polarizations change vertex
vectors but do not delete vertices.  This is the same herald/vacuum
boundary proved in the existing deletion-filtration notes.

Therefore (19) is an exact conditional route, not a P6 exclusion.  The next
legal selector must expose one synchronized blocker-deletion convolution,
or derive its value from the GHZ target by a new identity.  Repeating the
pair-deck fan alone cannot do so.

## 7. Literature translation

The exponential of a linear plus quadratic form is the classical Gaussian
moment-generating shape, and treating its moments as one algebraic image is
standard in algebraic statistics; see Amendola, Faugere, and Sturmfels,
[*Moment Varieties of Gaussian Mixtures*](https://arxiv.org/abs/1510.04654).
Loop hafnians as moment functions and the parallel use of cumulants appear
in Cardin and Quesada,
[*Photon-number moments and cumulants of Gaussian states*](https://arxiv.org/abs/2212.06067).
The individual five-port obstruction is the factor-analysis pentad of
Drton, Sturmfels, and Sullivant,
[*Algebraic Factor Analysis: Tetrads, Pentads and Beyond*](https://arxiv.org/abs/math/0509390).

The square-free optional-port algebra, the elimination of all odd residual
depths, the common four-row factorization criterion, the division-free law
(5), and its P6 legality interface are the problem-specific content proved
here.  No cited source implies them.

## Scope wall

```text
four-residual normalized pair law F_ij=a_ij+L_iL_j: PROVED;
odd residual depths needed for pair factorization:   NO;
three complementary even products equal:            PROVED;
normalized full-response identity:                   PROVED;
division-free equations (5) and (16):                PROVED;
complete even-tower representability iff:            PROVED;
quartic equations alone imply common factorization:  FALSE;
five-port pentad/common-row/top laws are redundant:   FALSE;
clean P6 six-face labels, conditional:                AVAILABLE;
clean P6 complete optional-port convolutions:         UNKNOWN;
GHZ forces a violation of the even Wick criterion:    UNKNOWN;
physical P6 Segre/even-Wick intersection empty:       UNKNOWN;
unrestricted P5, P6, or P7 nonrestriction:            UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.       (20)
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_four_residual_even_wick_tower_and_p6_synchronization.py
python claims/arbitrary-order/audit_four_residual_even_wick_tower_and_p6_synchronization.py
python -m py_compile claims/arbitrary-order/verify_four_residual_even_wick_tower_and_p6_synchronization.py claims/arbitrary-order/audit_four_residual_even_wick_tower_and_p6_synchronization.py
uvx ruff check claims/arbitrary-order/verify_four_residual_even_wick_tower_and_p6_synchronization.py claims/arbitrary-order/audit_four_residual_even_wick_tower_and_p6_synchronization.py
```

The primary replay works symbolically with four generic incidence rows and
a nontrivial six-port moment, verifies normalization, all complementary
products, (5), (15), and the pentad sharpness control.  The independent
no-import audit constructs a fixed ten-vertex matching response by a separate
hafnian recurrence, verifies every even deck identity, and detects a named
one-coefficient perturbation of the top response.  These are fixed small
algebra audits; the written coefficient proof establishes arbitrary port
number without enumerating graphs or supports.

## Dependencies

- [`RESIDUAL_DEPTH_LOOP_HAFNIAN_CUMULANT_AND_TWO_PORT_DISCRIMINANT_THEOREM.md`](RESIDUAL_DEPTH_LOOP_HAFNIAN_CUMULANT_AND_TWO_PORT_DISCRIMINANT_THEOREM.md)
- [`RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md`](RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md)
- [`P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md`](../p6/P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md)
- [`RESIDUAL_TWO_PORT_FACTOR_ANALYSIS_IDEAL_AND_FIVE_PORT_PENTAD_THEOREM.md`](RESIDUAL_TWO_PORT_FACTOR_ANALYSIS_IDEAL_AND_FIVE_PORT_PENTAD_THEOREM.md)
- [`MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md`](MIXED_ROOT_DELETION_FILTRATION_AND_HERALD_FREE_PAIR_NO_GO.md)
