# Characteristic-two contraction lift obstruction

## Status and purpose

This is a proved algebraic scope boundary for a tempting global modular
route.  A source-inspected external Lean project states an integer-weight
obstruction obtained by reduction to `ZMod 2` and characteristic-two
contraction.  This repository has not replayed its build or completed the
definition-correspondence audit, so the external theorem remains a candidate
formal counterpart here.  Even accepting its own reported scope, its proof
does not automatically extend to arbitrary algebraic or complex weights.

The results below identify three independent missing bridges:

1. an algebraic point need not have good reduction at a place above `2`;
2. even a `2`-integral algebraic point generally reduces to a finite extension
   of `F_2`, while the checked base theorem is specific to `F_2`; and
3. the rank-two update cancellation is isolated to characteristic two and has
   no nonzero analogue in infinitely many odd characteristics.

This note preserves a useful failed route.  It proves neither the global
Krenn--Gu conjecture nor the existence of a counterexample in its range.

## Pinned external provenance and exact scope

The source inspected is

```text
KitaKen1/monochromatic-quantum-graphs-lean
commit d3ed1892ef181f5f5f5d61d9b5817f05b53a6675.
```

This is the same commit recorded in the repository's
[`formalization interface`](../../docs/formalization-interface.md).  Read-only
source inspection, not a fresh Lean build, found the following interfaces:

- [`Conclusion.lean`](https://github.com/KitaKen1/monochromatic-quantum-graphs-lean/blob/d3ed1892ef181f5f5f5d61d9b5817f05b53a6675/lean/QuantumLean/Conclusion.lean), which states the even-`N>=6`, three-colour
  `ZMod 2` exclusion;
- [`ColorRestriction.lean`](https://github.com/KitaKen1/monochromatic-quantum-graphs-lean/blob/d3ed1892ef181f5f5f5d61d9b5817f05b53a6675/lean/QuantumLean/ColorRestriction.lean), which restricts an external `D>=3` equation
  system to three colours;
- [`ParityBridge.lean`](https://github.com/KitaKen1/monochromatic-quantum-graphs-lean/blob/d3ed1892ef181f5f5f5d61d9b5817f05b53a6675/lean/QuantumLean/ParityBridge.lean), which transports that equation system along
  a unital semiring homomorphism;
- [`RankTwo.lean`](https://github.com/KitaKen1/monochromatic-quantum-graphs-lean/blob/d3ed1892ef181f5f5f5d61d9b5817f05b53a6675/lean/QuantumLean/RankTwo.lean), whose four-vertex rank-two cancellation uses
  `2=0`;
- [`SixVertex.lean`](https://github.com/KitaKen1/monochromatic-quantum-graphs-lean/blob/d3ed1892ef181f5f5f5d61d9b5817f05b53a6675/lean/QuantumLean/SixVertex.lean), which contains the `ZMod 2` unit-matching step;
  and
- [`IntegerConclusion.lean`](https://github.com/KitaKen1/monochromatic-quantum-graphs-lean/blob/d3ed1892ef181f5f5f5d61d9b5817f05b53a6675/lean/QuantumLean/IntegerConclusion.lean), which assembles the reported integer theorem.

Within the external definitions, the resulting source-level transfer statement
is conditional:

> For even `N>=6` and `D>=3`, if the weights lie in a commutative semiring `R`
> with a unital homomorphism `R -> F_2`, then reduction preserves the external
> normalized equation system and its `F_2` theorem excludes those weights.

Subject to the still-pending correspondence audit, this includes integer
weights and weights integral in a local model whose residue field is exactly
`F_2`.  It does not directly include `Q`, `Qbar`, or `C`; no unital map from a
characteristic-zero field to `F_2` exists.

## Why ordinary good reduction is insufficient

A complex point of the integer equation scheme would yield an algebraic point
and reductions away from finitely many primes after spreading out.  The prime
`2` can be among the excluded denominator primes.  The affine equation

```text
2x=1
```

is the elementary model: its generic fibre is nonempty and its fibre at `2`
is empty.  Projective closure merely moves the point to infinity, where the
normalized target coefficient is no longer one.

Diagonal target-preserving vertex-colour gauges do not automatically repair
this.  Such a gauge has scalars `t_(i,c)` satisfying

```text
product_i t_(i,c)=1                                   (1)
```

for each target colour.  Hence every pure-colour perfect-matching monomial is
gauge invariant.

There is an exact same-equation-family counterexample to automatic
`2`-integralization at `n=4,d=2`.  Set all entries to zero except

```text
W_01[0,0]=1,       W_23[0,0]=1/2,
W_02[0,0]=1,       W_13[0,0]=1/2,
W_03[1,1]=1,       W_12[1,1]=1.                       (2)
```

The two colour-zero matching monomials sum to `1/2+1/2=1`, the sole
colour-one monomial is one, and every mixed coefficient is zero.  Thus (2)
gives exactly `Delta_2`.  Both colour-zero monomials have `2`-adic valuation
`-1`, invariant under (1).  If every active entry became integral, their
products would have nonnegative valuation, a contradiction.

The example is outside the conjectural range `n>=6,d>=3`; it refutes only an
automatic diagonal-gauge integralization lemma.  A special theorem using the
additional three-colour, six-or-more-vertex equations would be genuinely new.

## The residue-extension gap is also real

Even if an algebraic model is integral at a place over `2`, its residue field
is generally `F_(2^f)`, not `F_2`.  The checked six-vertex base cannot simply
be scalar-extended.

Let `F_4=F_2(alpha)` with

```text
alpha^2+alpha+1=0.
```

On a scalar six-vertex graph set

```text
A_01=alpha,   A_23=A_45=1,
A_02=alpha^2, A_13=1,
```

and all other edges to zero.  Its only nonzero perfect-matching terms are
`alpha` and `alpha^2`, so

```text
haf(A)=alpha+alpha^2=1.                               (3)
```

No contributing matching has every edge weight equal to one.  Thus the
external `F_2` step "matching sum one exposes a unit matching" is false over
`F_4`.  Its later endpoint-marginal count is field-specific as well: the
affine plane

```text
{(x,y,z) in F_q^3 : x+y+z=1}
```

has `q^2` points, four over `F_2` but sixteen over `F_4`.

The example (3) is an aggregate matching-sum counterexample, not a Krenn--Gu
witness.

## Universal pairwise-update classification

The characteristic dependence can be isolated exactly.  Let `V` be a
finite-dimensional vector space over a field `k`, let `B:V x V -> k` be a
symmetric bilinear form, and define the four-point matching form

```text
H_B(x1,x2,x3,x4)
 = B(x1,x2)B(x3,x4)
 + B(x1,x3)B(x2,x4)
 + B(x1,x4)B(x2,x3).                                 (4)
```

Then `H_B` vanishes identically exactly in the following cases:

```text
char(k)=2:       B is alternating and rank(B)<=2;
char(k)=3:       rank(B)<=1;
char(k)!=2,3:    B=0.                                 (5)
```

### Proof

Put `q(x)=B(x,x)`.  Substituting the same vector four times in (4) gives

```text
H_B(x,x,x,x)=3q(x)^2.                                (6)
```

Outside characteristic three, (6) gives `q=0`.  Outside characteristic two,
polarization then gives `B=0`, proving the last line of (5).

Here rank means the rank of the induced map `V -> V*`.  In characteristic
two, choose `y,z` with `B(y,z)!=0` unless `B=0`.  The
specialization

```text
H_B(x,x,y,z)=q(x)B(y,z)
```

shows that `B` is alternating.  For an alternating form, (4) is its
four-by-four Pfaffian because signs coincide in characteristic two.  If its
rank were at least four, symplectic Gram--Schmidt would give a nondegenerate
four-dimensional restriction and hence a nonzero four-by-four Pfaffian.
Conversely rank at most two makes every such Pfaffian vanish.  Thus all these
Pfaffians vanish exactly when `rank(B)<=2`.

In characteristic three, if `q` vanishes identically then polarization gives
`B=0`.  Otherwise choose `x` with `q(x)!=0`.  From

```text
0=H_B(x,x,y,z)=q(x)B(y,z)+2B(x,y)B(x,z)
```

and `2=-1` one obtains

```text
B(y,z)=B(x,y)B(x,z)/q(x),
```

so `B` has rank at most one.  Conversely a rank-one symmetric form makes (4)
three copies of the same product, which vanishes in characteristic three.
The alternating rank-at-most-two converse in characteristic two follows from
the same Pfaffian description.

For the external update

```text
B(u,v)=P(u)Q(v)+P(v)Q(u),
```

characteristic two makes `B` alternating of rank at most two.  Formula (5)
shows that the same nonzero rank-two, pairwise-weight update cannot work in
infinitely many odd characteristics; characteristic three retains only a
rank-one degeneration.  This does not exclude a fundamentally different
odd-characteristic or characteristic-zero contraction.

## Focused checks

```text
uv run --with sympy python claims/arbitrary-order/verify_characteristic_two_contraction_lift_obstruction.py
python claims/arbitrary-order/audit_characteristic_two_contraction_lift_obstruction.py
```

The first script verifies (2), (3), and the polynomial specializations in
(4)--(6).  The independent script uses a separate finite-field
implementation and small direct bilinear-form tables.  Neither computation is
the proof of the arbitrary-field classification.

## Boundary

```text
external source theorem:                        REPORTED BY PINNED PROJECT;
local Lean build replay:                        NOT RUN;
formal statement correspondence:               PENDING AUDIT;
good reduction at 2 from char-0 solvability alone: FALSE IN GENERAL;
automatic diagonal target-preserving 2-integral gauge: REFUTED IN THE EQUATION FAMILY;
specific F_2 unit-matching step over F_4:        REFUTED;
same rank-two update at infinitely many primes: NO;
special n>=6,d>=3 integralization theorem:      UNKNOWN;
six-vertex exclusion over Fbar_2:                UNKNOWN;
different odd-prime modular mechanism:          UNKNOWN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```
