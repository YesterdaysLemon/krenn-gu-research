# Four-root torus-star equal-leaf H4 Q6 H2 degree-drop six-minor offset exclusion (GLD99)

## Status and exact scope

**Proved exact scoped characteristic-zero theorem (`GLD99`).**  In the
normalized scale-fixed equal-leaf H4 chart, impose

```text
H2 = 2p^2-2p+1 = 0,
Q6 = 0,
```

retain `a,B,C` as formal coordinates before imposing the rank-minor
equations, and use the GLD88 offset coordinates

```text
b = b88(p,q,a)+B,
c = c88(p,q,a)+C.
```

On the declared denominator-safe chart this is an affine bijection between
the original `(b,c)` coordinates and the offsets `(B,C)`.

On the denominator-safe open `D(Delta)`, every geometric point at which the
full GLD71 `37 x 9` syndrome has rank at most six has `B=C=0`.  Consequently,
after the GLD75/GLD86 incidence bridge and the exact GLD95 direct-H2 endpoint,
the corresponding rank-at-most-six incidence is empty on
`D(Omega Delta)`.

This is a theorem about the `H2=0` degree-drop fibre in one normalized
F88-offset chart.  It uses no `R31`, `E31`, or `g0` localization.  It does not
prove that arbitrary H4/Q6 points enter this chart, compute the GLD83
pulled-back Fitting ideal, cover `Delta=0`, or address other gauges,
components, source branches, roots, or orders.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

The primary exact verifier is
`claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py`.
It reconstructs the canonical GLD71 syndrome and GLD88 family, verifies the
degree-drop and every localization gate, and constructs exact polynomial
multiplier identities for `B` and `C`.  A separate self-contained audit uses
copied immutable sparse supports, direct syndrome accumulation, and local
sparse subset determinant accumulation, with fraction-free exact
specialization controls.

## 1. The true H2/Q6 fibre

Use the GLD96 scale-fixed H4 leaf

```text
G = [1  1       1      ]
    [p  q       s      ],
    [a  1+b     1+c    ],

s = (p+q-pq)/(p+q-1).
```

Put

```text
d0 = p+q-1,
P  = p^2-p+1,
L1 = p^2+2pq-2p-q,
L2 = 2pq-p+q^2-2q,
e  = 2pq^2-2pq-p-q^2-2q+2,
Delta = (p-q)d0 P L1 L2 e.
```

Exact division in `Q[p,q]` gives

```text
Q6 = d0*K/4 modulo H2,

K = -4p q^2+4p q-6p+2q^2-4q+4.
```

Over `Q(i)`, the two roots of `H2` are

```text
p+ = (1+i)/2,
p- = (1-i)/2.
```

On the plus branch,

```text
Q6(p+,q) = (-i/2) d0,+ Q+(q),

d0,+ = q-1/2+i/2,
Q+(q) = q^2-(1+i)q+(3+i)/2.
```

Put `Q-:=conjugate(Q+)`; the minus branch is the coefficientwise complex
conjugate.  The discriminant
of `Q+` is `-6`, so `Q+` is irreducible over `Q(i)`.

The factor `d0` is already excluded by `D(Delta)`.  There is no further
hidden chart collision on the quadratic branch: with resultants taken in
`q` against monic `Q+`, exact arithmetic gives

| factor `u` | `d0` | `p-q` | `P` | `L1` | `L2` | `e` |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `Res_q(Q+,u(p+,q))` | `1/2` | `3/2` | `1/4` | `3/4` | `3` | `8` |

Thus every displayed F88 denominator and every factor of `Delta/d0` is a
unit in

```text
A+ = Q(i)[q]/(Q+).
```

Equivalently, the product resultant is
`Res_q(Q+,Delta/d0)=27/4`.

The conjugate resultants give the identical conclusion on `p-`.  After the
faithfully flat scalar extension from `Q` to `Q(i)`, the squarefree polynomial
`H2` splits and the Chinese remainder theorem separates the two conjugate
`p` branches.  On `D(Delta)`, each branch retains only its quadratic `Q+` or
`Q-` component; the discarded `d0=0` component is not silently retained.

## 2. Six raw rank-seven minors

Let `M(G)` be the complete GLD71 syndrome.  Use the four raw bordered
seven-minors already selected by GLD96:

```text
T0 = det M[(0,1,2,17,25,31,28), (0,1,3,4,6,7,8)],
T1 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,2)],
T2 = det M[(0,1,2,17,25,31,32), (0,1,3,4,6,7,5)],
T3 = det M[(0,1,2,17,25,31,33), (0,1,3,4,6,7,8)],
```

and the two direct GLD97 detectors

```text
D0 = det M[(1,17,28,0,25,31,32), (0,1,2,3,4,5,6)],
D2 = det M[(1,17,28,0,31,32,3), (0,1,2,3,4,5,6)].
```

These are raw seven-by-seven determinants.  A full syndrome rank bound of
six makes all six vanish, regardless of the value of the old six-by-six
`R31` determinant.  Conversely, no equivalence between these six equations
and the full rank condition is claimed or needed.

Substitute `p=p+` and `b=b88+B,c=c88+C`.  Reduce every q-coefficient modulo
`Q+` only after checking that the corresponding raw denominator is coprime
to `Q+`.  Clearing a denominator that is already a unit on `D(Delta)` gives
six polynomial representatives

```text
F_T0,F_T1,F_T2,F_T3,F_D0,F_D2 in A+[a,B,C].
```

The four bordered representatives `F_T0,...,F_T3` are affine in `C`.  The
direct representatives `F_D0,F_D2` retain genuine `C^2` terms, so an
affine-in-`C` ansatz would lose part of their support.  All six have total
`(B,C)` degree three, and the multiplier construction below includes their
complete support without an affine-in-`C` truncation.

At `B=C=0`, the GLD88 common block-kernel vector annihilates all three
syndrome blocks.  The primary checks all `3*37=111` entries exactly.  Hence

```text
F_j(0,0)=0
```

for all six representatives, and the generated ideal is contained in
`(B,C)`.  The primary also checks these six constant terms directly after
quotient reduction, rather than inferring their vanishing only from the
kernel identities.

## 3. Exact all-a multiplier certificate

The reverse containment is proved without treating `a` as a rational-function
coefficient and without deleting any exceptional `a` value.  For each target
`X` in `{B,C}` and each of the six representatives, use the multiplier ansatz

```text
U_j,X = sum lambda(j,r,s,t,u) B^r C^s q^t a^u,

r+s <= 1,   0 <= t <= 1,   0 <= u <= 3.
```

There are

```text
6 * 3 * 2 * 4 = 144
```

Gaussian-rational unknown coefficients.  Expanding

```text
sum_j U_j,X F_j - X
```

in `B,C,a` and the `A+` basis `(1,q)` gives one exact coefficient matrix with
`158` rows and `144` columns.  Its exact rank over `Q(i)` is `140`.  Appending
the coefficient vector for either `B` or `C` leaves the rank `140`.  Choosing
the four free multiplier coefficients canonically and substituting the two
solutions back gives the exact identities

```text
sum_j U_j,B F_j = B  in A+[a,B,C],
sum_j U_j,C F_j = C  in A+[a,B,C].
```

The primary verifier pins the input matrix and the canonical solution data,
then replays both identities coefficientwise.  The independent audit rebuilds
the same two identities from copied supports and a separate determinant and
linear-algebra path.  Because `a` was a polynomial variable in the coefficient
matching, this is not a generic-in-`a` rank calculation or an interpolation
claim.

Together with the zero constant terms, the identities prove

```text
(F_T0,F_T1,F_T2,F_T3,F_D0,F_D2) = (B,C)
```

in `A+[a,B,C]`.  Coefficientwise conjugation proves the same equality in

```text
A- = Q(i)[q]/(Q-)
```

on the `p-` branch.  The Chinese-remainder decomposition over `Q(i)` covers
both factors of `H2`; faithful-flat descent gives the corresponding ideal
containment in the localized `H2,Q6,D(Delta)` quotient over `Q`.
Equivalently, for the geometric conclusion used here, every complex point
lies on one of the
two conjugate branches and is covered by the appropriate identity.

## 4. Rank implication and downstream exclusion

Assume a normalized H4 point lies on `H2=Q6=0` and `D(Delta)`, and the full
syndrome has rank at most six.  Every displayed seven-minor vanishes.  On its
appropriate `p+` or `p-` branch, the exact ideal equality forces `B=C=0`.
Thus the point lies on the written GLD88 family `F88`.

Separately, GLD95 directly specialized its finite-common-minor calculation on `H2`,
rather than using the invalid generic Q6 division with denominator `H2^47`.
It proved

```text
gcd_q(Q6, Res_a(F28,F31)) = d0
```

on that fibre.  This is the committed GLD95 H2-specialized `F28,F31`
statement, not a generic identity and not a consequence of the six offset
minors.  Since `d0` is excluded by `D(Delta)`, that separate theorem makes the
F88 endpoint empty there.  The exact GLD75/GLD86 bridge supplies the upstream incidence-to-
syndrome implication, and `D(Omega)` retains the physical frame, leaf, and
center determinant gates.  Consequently

```text
B_incidence intersect V(I_7(A)) intersect H4
  intersect V(H2,Q6) intersect D(Omega Delta) = empty
```

in this normalized offset chart.

## 5. Evidence boundaries and retained frontier

The theorem proves one local implication and its downstream exclusion.  It
does not claim:

- that the six selected minors characterize full syndrome rank at most six;
- that points outside the normalized F88-offset chart enter this coordinate
  system;
- any conclusion on `Delta=0` or a different scale/gauge chart;
- closure of the separate `E31=0` or `g0=0` generic-resultant strata;
- computation or emptiness of the GLD83 pulled-back Fitting ideal;
- coverage of other equal-leaf ranks, components, source branches, profiles,
  roots, or orders; or
- a global Krenn--Gu proof or counterexample.

The proof removes `H2=0` only as an independent exceptional factor in the
declared normalized GLD96/F88-offset subroute on `D(Delta)`.  It does not
remove H2 from unrelated GLD96 obligations, charts, or branches.  The
remaining exceptions in the complementary generic-resultant route are
`E31=0`, `g0=0`, and the declared chart boundary `Delta=0`.  Arbitrary H4
Q6 points outside this chart, the Fitting pullback, and the other global proof
obligations remain open.  The global conjecture remains **UNRESOLVED**.

## 6. Replay

Run the canonical-builder primary and the self-contained audit under bounded
containment:

```powershell
python tools/research/run_bounded.py --run-id gld99-h2-primary --timeout-seconds 600 --memory-mb 12288 -- python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py

python tools/research/run_bounded.py --run-id gld99-h2-audit --timeout-seconds 600 --memory-mb 12288 -- python claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_h4_q6_h2_degree_drop_six_minor_offset_exclusion.py
```

Both replays use exact characteristic-zero arithmetic.  Solver output or a
timeout is not a proof; the claimed status requires both scripts to complete
their pinned identities and the dedicated hostile review to accept the exact
scope above.
