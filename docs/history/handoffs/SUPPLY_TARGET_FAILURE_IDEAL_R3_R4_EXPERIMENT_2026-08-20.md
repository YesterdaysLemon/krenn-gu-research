# Supply/target failure ideal at r=3 and r=4: exact formulation audit

Date: 2026-08-20
Branch: `codex/kg-supply-target-node-20260820`
Base: `origin/main` at `a16315f145324b503c3ec0ccd017ee7562f9626d`
Status: **model-equivalence obstruction; no failure locus was solved**
Global Krenn--Gu status: **UNRESOLVED**

## 1. Outcome

There is no honest single "universal selector-failure ideal" yet available to
run at either `r=3` or `r=4`.  The complete physical GHZ system and the GLS2
sensor can be encoded exactly, but the proposed bridge combines three
different quantifiers:

1. maximum-root maximality is the nonexistence of a torus common zero for
   every `(r+1)`-vertex set;
2. GLS2 observability is rank over the outside function field `K(z_B)`;
3. legal target attachment asks for the existence of a fully supported
   residual contraction, including exceptional contraction fibres.

A scalar kernel at one contraction does not encode item 2.  Generic quotient
membership over `K(z_Q)` does not encode failure at every contraction in item
3.  Exact one-parameter examples below prove both inequivalences.  Moreover,
the existing GLD target-attachment interface starts at four roots, so applying
the same formal quotient at `r=3` would require a new theorem identifying its
output with a legal downstream package.

Consequently this lane stopped at its required equivalence gate.  It did not
run a misleading Groebner basis on the two support-preserving controls from
checkpoint `39933ee8`, did not infer a locus dimension, and did not classify
support masks.  The exact script
[`supply_target_failure_ideal_probe.py`](../../../tools/explore/supply_target_failure_ideal_probe.py)
pins the complete physical coefficient formula, audits every `r=3` word, and
records the exact `r=3,4` system sizes and quantifier counterexamples.

## 2. The complete physical polynomial system

Work first over `C`, the field of the owning maximum-root theorem.  Label the
chosen root set

```text
R={0,...,r-1},                    |B|=r+2,
Omega=R disjoint-union B,         |Omega|=2r+2.
```

For each unordered edge `{u,v}` and endpoint colours `a,b in {0,1,2}`, let
`w_(uv;ab)` be the corresponding entry of the physical bilinear block.  The
opposite orientation is its transpose; there are exactly

```text
9 binom(2r+2,2)
```

independent graph entries.  For every colour word
`alpha in {0,1,2}^Omega`, define

```text
C_alpha(W)
 =sum_(M perfect matching of Omega)
    product_({u,v} in M) w_(uv;alpha_u alpha_v).       (1)
```

The complete normalized ternary GHZ equations are

```text
C_alpha(W)=1   if alpha is constant,
C_alpha(W)=0   otherwise.                             (2)
```

Equation (1) is not a shell or a sample.  It contains every perfect matching
and (2) ranges over all `3^(2r+2)` words.

### Equivalence to the physical tensor equality

On the basis covector indexed by `alpha`, a matching contributes the product
of exactly the endpoint entries displayed in (1).  Summing over physical
perfect matchings is therefore the coefficient of the graph tensor.  The
normalized GHZ tensor has coefficient one exactly on the three constant
words and zero elsewhere.  Thus (2) is coefficientwise equivalent to the
original tensor equality.  No root contraction, support specialization, or
Hamming truncation enters this equivalence.

### The chosen torus root

Introduce root coordinates `x_(i,c)` and impose

```text
sum_(a,b) w_(ij;ab) x_(i,a) x_(j,b)=0
       for all {i,j} subset R,                        (3)
tau_x product_(i,c) x_(i,c)-1=0.                     (4)
```

The Rabinowitsch equation (4) is an exact characteristic-zero encoding of
full support.  It does not divide by a coordinate.

For an `(r+1)`-set `A subset Omega`, use fresh variables `y_(v,c)` and put

```text
I_A(W)=< B_uv(y_u,y_v) : {u,v} subset A >.
```

At a fixed complex graph, `A` contains no torus-root configuration exactly
when

```text
I_A(W) : (product_(v in A,c) y_(v,c))^infinity = (1). (5)
```

This is the Laurent Nullstellensatz.  The selected root has maximum
cardinality `r` exactly when (3)--(4) hold and (5) holds for every
`binom(2r+2,r+1)` set `A`.  Blocker quotas, corank at most six, local
concision, pure normalization, and Hamming-one equations are consequences or
necessary controls; they are not equivalent replacements for (5).

Parametric unit-ideal membership in (5) is not itself a list of equations in
the graph entries.  To turn it into one existential polynomial incidence
scheme requires either quantified elimination or explicit Laurent
Nullstellensatz certificates with a proved degree bound.  No such compact
bound/interface is currently supplied by the owning theorem package.

## 3. The exact GLS2 function-field sensor

Let `z_u=(z_(u,0),z_(u,1),z_(u,2))` be generic outside vectors.  For each
nonempty even `I subset B`, matching partition at the roots gives the
companion column

```text
G_(B-I)(W;z_(B-I)) in C(z_B)^(3^r).                  (6)
```

Ordering all such labels gives the GLS2 matrix

```text
M(W;z_B): C(z_B)^(2^(r+1)-1) -> C(z_B)^(3^r).        (7)
```

The column for a label of order `|I|=2+2p` is the sum over a `p`-edge
partial matching of the roots and a bijection from the other `r-2p` roots to
`B-I`.  Multiplying that column by the physical hafnian `H_I` and summing all
labels partitions every matching of the full graph exactly once.  Every term
has graph degree

```text
(r-p)+(1+p)=r+1=(2r+2)/2,                             (8)
```

so the companion identity reconstructs precisely (1), not an additional
surrogate equation.

Let `P_2` be the pair labels.  The failure of collective pair observability
is exactly

```text
there exists v in ker_(C(z_B)) M
with pi_(P_2)(v) != 0.                               (9)
```

For a residual pair `Q`, split the labels as in GLS2 into `C_Q` (meeting `Q`
in zero or two vertices) and `N_Q` (meeting it once).  Fixed-`Q`
observability fails exactly when

```text
there exists v_Q in ker_(C(z_B)) M
with pi_(C_Q)(v_Q) != 0.                             (10)
```

Over a field, projected nonzero can be normalized without choosing a chart:

```text
pi(v) != 0  iff  there exists a with a dot pi(v)=1.  (11)
```

However, in (9)--(10), both `a` and `v` live over `C(z_B)`.  Replacing them by
constant scalar variables tests only constant syzygies.  Clearing
denominators gives polynomial syzygies, but an incidence encoder must prove a
degree bound or instead impose coefficientwise determinantal identities.
Neither may be silently omitted.

### Exact counterexample to a constant kernel witness

Over `Q(t)`, the matrix

```text
[ 1  t ]                                              (12)
```

has the nonzero kernel vector `(-t,1)`.  A constant vector `(a,b)` in its
kernel would satisfy `a+tb=0`, so coefficient comparison gives `a=b=0`.
Thus a one-contraction or constant-vector kernel ideal can declare an
observable matrix even though its function-field sensor is not injective.

### Exact coefficientwise determinantal repair

The GLS2 part can nevertheless be made into a finite constructible condition
without guessing a syzygy degree.  Write

```text
M=[H P],
```

where `P` is the desired column block and `H` is its nuisance complement.
If `P` has `p` columns, failure of injectivity modulo `H` is the union over
`k=0,...,number_of_columns(H)` of the branches

```text
rank_(C(z_B)) H = k,
rank_(C(z_B)) [H P] <= k+p-1.                        (12a)
```

On branch `k`, impose coefficientwise vanishing in `z_B` of every
`(k+1)`-minor of `H` and every `(k+p)`-minor of `[H P]`, and saturate by the
coefficient vector of at least one `k`-minor of `H`.  A polynomial minor is
zero in `C(z_B)` exactly when every one of its finitely many coefficients is
zero.  Nonzero of at least one coefficient can be encoded without choosing a
chart by a dual normalization as in (11).

For collective pair failure, `(H,P)` is `(higher columns, pair columns)`, so
there are six rank branches at `r=3` and seventeen at `r=4`.  For fixed-`Q`
failure, `(H,P)=(N_Q,C_Q)`, giving nine branches for each of the ten `r=3`
pairs and seventeen branches for each of the fifteen `r=4` pairs.  This is an
exact determinantal localization of the sensor failures.  It is not one
prime ideal, and taking a single minor chart would omit divisor branches.

## 4. Fixed-Q legal selectors and the opposite quantifier

At four roots, fix a residual pair `Q`, a fully supported contraction `z_Q`,
and `U=B-Q`, so `|U|=4`.  For each

```text
S in binom(U,2) union {U},
```

GLD5 defines the complete constant map `Gamma_Q`, desired coefficient `g_S`,
and full nuisance slice space `N_S`.  If a matrix `A_S(W;z_Q)` lists a
spanning family for `N_S`, selector failure at this fixed contraction is
exactly the existential polynomial condition

```text
there exists c_S such that A_S(W;z_Q)c_S=g_S(W;z_Q). (13)
```

This avoids minors and divisions.  It also shows why the residual
contraction cannot be suppressed.  The useful-pair output may choose a
contraction, so failure of every selector has the form

```text
for every z_Q in (C^*)^6 and every S,
    g_S(W;z_Q) belongs to N_S(W;z_Q),                 (14)
```

before the additional response, synchronization, augmented-weight,
alignment, and target-pure-anchor gates are imposed.  Formula (14) has the
opposite contraction quantifier from a generic function-field calculation.

### Exact counterexample to generic-to-pointwise failure

Let `s` be a torus coordinate and put `t=s-1`.  Thus `t=0` is the allowed
fully supported contraction `s=1`, not a forbidden coordinate hyperplane.
Let

```text
N(t)=span{t e_1},                   g=e_1.             (15)
```

Over `Q(t)`, `g=(1/t)(t e_1)`, so the generic selector fails.  At `t=0`, the
nuisance space is zero and `g` survives.  Hence generic quotient membership
does not exclude an exceptional legal selector.  Conversely, membership at
one selected contraction says nothing about the other contractions.

This toy identity is precisely the rank-specialization direction already
visible in GLD13: exceptional nuisance-rank-drop fibres cannot be inferred
from the generic branch.

There is an exact rank-stratified pointwise formulation.  On the
stratum `rank A_S=k`, selector survival is

```text
all (k+1)-minors of A_S vanish,
some k-minor of A_S is nonzero,
some (k+1)-minor of [A_S | g_S] is nonzero.           (15a)
```

Torus nonzero and both "some minor" clauses can be encoded by auxiliary dual
normalizations.  Failure for every contraction means that, for every `k`,
the exact incidence ideal for (15a) has empty torus fibre.  Equivalently its
appropriate saturated ideal is the unit ideal after specializing the graph.
This uses 730 possible nuisance ranks for each `r=4` pair target and 82 for
each all-port target before any structural compression.  It is a valid
quantified determinantal formulation, but converting the parametric
fibrewise unit-ideal assertions into a graph ideal is the missing elimination
invariant.  Blindly decomposing these ranks would violate the programme stop
rule.

### The compact missing invariant: radical Fitting-rank profile

The rank strata admit a support-free compression.  Let `K` be algebraically
closed, let

```text
Lambda=K[z_1,z_1^(-1),...,z_m,z_m^(-1)]
```

be the Laurent coordinate ring of the fully supported contraction torus,
let `A` be any `d x e` nuisance matrix over `Lambda`, and let `g` be a desired
column.  Write `I_j(A)` for the ideal of `j x j` minors, with the usual
conventions.

**Proposition (pointwise selector failure criterion).**  The following are
equivalent:

1. `g(z)` lies in the column span of `A(z)` for every torus point
   `z in (K^*)^m`;
2. `rank[A(z)|g(z)]=rank A(z)` at every torus point;
3. for every `j=1,...,d`,

   ```text
   radical I_j(A)=radical I_j([A|g]) in Lambda.       (15b)
   ```

**Proof.**  Items 1 and 2 are ordinary field linear algebra in every fibre.
At a point `z`, `rank A(z)<j` exactly when every `j`-minor of `A` vanishes
there.  Since the columns of `A` occur in `[A|g]`, one always has
`I_j(A) subset I_j([A|g])`.  The two matrices have the same rank at every
point exactly when their `j`-minor zero sets agree for every `j`.  The Laurent
Nullstellensatz identifies equality of those zero sets with equality of the
radicals in (15b).  QED.

This is the quantifier-compatible invariant missing from a generic quotient
calculation.  It handles all exceptional rank drops at once and uses no
minor division.  It is also strictly weaker than global polynomial module
membership.  For example, over `K[s,s^(-1)]`, take

```text
A=[(s-1)^2],                    g=s-1.                (15c)
```

At `s!=1`, the single nuisance column spans the fibre; at `s=1`, both `A`
and `g` evaluate to zero.  Hence the selector fails pointwise everywhere,
and both first-minor ideals have radical `(s-1)`.  Nevertheless
`s-1` is not a polynomial multiple of `(s-1)^2`.  Thus imposing
`g=A c` over the Laurent polynomial ring would omit genuine pointwise
failure, while imposing it only over the fraction field would admit the
false generic-to-pointwise inference in (15).

For the actual GLD5 data, apply (15b) to the full nuisance-slice matrix
`A_S(W;z_Q)` and desired column `g_S(W;z_Q)` for every `Q,S`.  This produces a
compact exact definition of simultaneous raw selector failure at a fixed
physical graph.  What remains is to derive a usable graph-coefficient
consequence of these radical equalities and to incorporate the additional
response/alignment/anchor gates; the present experiment does not perform
that elimination.

At `r=3`, one can formally repeat the tensor quotient construction with
three ports, but GLD5, GLD7, and the four-root detector do not assert that
this formal quotient is a legal entry to their attachment machinery.
Calling it the required target selector would therefore change the theorem
interface.  The `r=3` experiment can discover algebra, but it cannot encode
the existing downstream legality condition until a uniform arbitrary-`r`
target package is stated and proved.

## 5. Exact size ledger

The probe obtains the following counts without support specialization.

| Quantity | `r=3` | `r=4` |
|---|---:|---:|
| vertices `2r+2` | 8 | 10 |
| graph block entries | 252 | 405 |
| root-vector coordinates | 9 | 12 |
| root-pair equations (3) | 3 | 6 |
| maximum-root Laurent tests (5) | 70 | 252 |
| complete GHZ equations | 6,561 | 59,049 |
| mixed GHZ zero equations | 6,558 | 59,046 |
| perfect matchings per coefficient | 105 | 945 |
| expanded GHZ monomial occurrences | 688,905 | 55,801,305 |
| GLS2 rows over `C(z_B)` | 27 | 81 |
| pair / higher / total GLS2 columns | 10 / 5 / 15 | 15 / 16 / 31 |
| pair-failure nuisance-rank branches | 6 | 17 |
| `C_Q` / `N_Q` columns | 7 / 8 | 15 / 16 |
| fixed-`Q` failure rank branches per `Q` | 9 | 17 |
| residual-pair choices | 10 | 15 |
| expanded companion monomial occurrences | 44,955 | 2,493,423 |
| full tensor deck-module dimension | 495 | 2,079 |
| fixed-`Q` open target dimension | 729 | 6,561 |
| pair-selector ambient rows / rank branches | 81 / 82 | 729 / 730 |
| pair-target nuisance generators | 4,455 | 18,711 |
| all-port selector ambient rows / rank branches | 27 / 28 | 81 / 82 |
| all-port nuisance generators | 13,365 | 168,399 |
| naive auxiliaries for all `Q,S` memberships | 267,300 | 4,209,975 |

The last line merely counts one coefficient per displayed nuisance generator
in (13); it is not a claim that all generators are independent or that (14)
has been eliminated.

The complete lazy coefficient specifications have SHA-256 identifiers

```text
r=3: 5d232f5f0df7a774f60729ed7670057470ffa08dfd35c95d009e83e2c61e0598
r=4: c0a57c287b19b162a83457a2d2e7b770d6fc1ae37e888a4c1aa30d821f15b96f
```

Each hash includes the canonical full matching list and every ternary
word/RHS pair.  The coefficient formula is the uniform equation (1), so the
lazy representation retains all mixed equations without storing 55.8
million repeated monomial records.

## 6. Focused exact run

Run from repository root:

```powershell
python tools/explore/supply_target_failure_ideal_probe.py
```

Result on 2026-08-20:

```text
status: equivalence_gate_stops_before_locus_elimination
r=3 coefficient audit: all 6561 words agree between explicit matching
    enumeration and an independent bit-mask recurrence over Z
r=4 coefficient audit: 9 exact pure/mixed stress words agree
function-field kernel example: [1,t](-t,1)^T=0
generic selector membership: e1=(1/(s-1))((s-1)e1), with survival at
    the torus point s=1
radical profile: A=[(s-1)^2], g=s-1 is pointwise failure without
    polynomial module membership
locus classification: not determined
global conjecture: UNRESOLVED
```

The written matching partition proves the complete `r=4` encoder; the nine
stress words are a bounded implementation replay, not an exhaustive
computation or a proof substitute.

## 7. Missing invariant and handoff

The smallest honest next object is not a larger support atlas.  It is a
**quantifier-compatible failure module** with all of the following:

1. a coefficientwise determinantal or bounded-syzygy representation of the
   GLS2 `C(z_B)` kernel, including pair and every `C_Q` projection;
2. a graph-coefficient consequence of the denominator-free radical
   Fitting-rank equalities (15b), or a stronger physical property which turns
   them into an ordinary module identity;
3. a uniform target-package functor (or separate proved `r=3` and `r=4`
   interfaces) which includes response nonvanishing, synchronization,
   augmented detector weight, `l-kappa p in ker U`, and the target-pure
   anchor rather than raw selector survival alone;
4. either compact Laurent Nullstellensatz certificates for maximum-root
   maximality or a proved statement that the already derived source
   consequences suffice for this particular module identity.

Only after those equivalences are supplied is it meaningful to ask whether
the exact `r=3` or `r=4` failure locus is empty, nonempty, or
positive-dimensional.  Any ideal formed now by substituting scalar kernel
witnesses, generic selector membership, blocker quotas, or the two
support-preserving controls would solve a different problem.

No exact physical point was produced, so there is no counterexample
escalation.  Nothing here proves an arbitrary-`r` theorem or changes the live
frontier.
