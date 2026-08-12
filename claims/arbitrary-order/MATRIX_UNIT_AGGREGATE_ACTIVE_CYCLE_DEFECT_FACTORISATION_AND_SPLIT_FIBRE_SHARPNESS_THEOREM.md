# Matrix-unit aggregate active-cycle defect factorisation and split-fibre sharpness

## Status

This theorem gives the exact arbitrary-order holonomy formula when one or
more fibres of an active matrix-unit transport cycle are aggregate rather
than binomial.

For each cycle word, normalize the sum of all extra compatible matching
monomials by the selected outgoing matching.  The resulting aggregate defect
`A_i` is gauge invariant, and the complete cycle equations give

```text
H=(-1)^m product_i (1+A_i).                         (1)
```

This recovers `H=(-1)^m` in the binomial case, but also exposes two exact
boundaries:

1. an aggregate fibre can be **split**: its extra nonzero terms cancel among
   themselves, so `A_i=0` and the known sign survives unchanged; and
2. without an additional equation coupling the defects, the aggregate cycle
   equations need not impose any polynomial on `H`.

The second boundary is physically sharp.  There is an exact one-parameter
family of complete nonzero eight-vertex matrix-unit tables with all three
endpoint labels present at every vertex, three complete active-cycle target
equations, two binomial fibres, and one five-term aggregate fibre, for which

```text
H=-2/(1+2t).                                        (2)
```

The image is Zariski dense in `C^*`, and the selected subsystem has
elimination ideal zero in `Q[H,H^(-1)]`.  At `t=1/2`, the three extra terms
are `1/2,-1,1/2`, giving an exact split aggregate with `H=-1`.

The family has zero pure target coefficients and is therefore not a
Krenn--Gu witness.  The theorem does not say that the complete target system
of a hypothetical witness leaves the defects free.  It proves that aggregate
cycle equations alone neither force the binomial sign nor contradict it;
effective cross-fibre, cross-multiplicity, pure, or deeper coupling is
load-bearing.  The `r=1` branch and the global Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. Imported active transport cycle

Work in the complete nonzero `r=1` matrix-unit branch over `C`.  Let

```text
chi_0 -> chi_1 -> ... -> chi_(m-1) -> chi_0,
m>=2,                                                (3)
```

be an active transport cycle from the imported phase-holonomy theorem.  At
step `i`, let

```text
F_i=E_i union P_i                                   (4)
```

be the selected nonzero outgoing matching inducing `chi_i`, and let

```text
G_i=B_i union P_i                                   (5)
```

be the selected nonzero diagonal matching inducing `chi_(i+1)`.  Thus the
incoming selected matching at `chi_i` is `G_(i-1)`.

The gauge-invariant cycle holonomy is

```text
H=product_i lambda(G_i)/lambda(F_i).                (6)
```

Every complete mixed target coefficient on the cycle is zero.

## 2. Complete aggregate defects

List every other compatible perfect matching at `chi_i` as

```text
X_(i,1),...,X_(i,k_i),                              (7)
```

where `k_i` may be zero.  The complete fibre equation is

```text
lambda(G_(i-1))+lambda(F_i)
 +sum_(a=1)^(k_i) lambda(X_(i,a))=0.                (8)
```

Define the normalized aggregate defect

```text
A_i=sum_a lambda(X_(i,a))/lambda(F_i).              (9)
```

When `k_i=0`, this is the empty sum `A_i=0`.  When `k_i>0`, every summand in
(9) is a nonzero Laurent monomial, but their sum may vanish.

### Theorem 1 (gauge-invariant aggregate-defect factorisation)

Every `A_i` is invariant under diagonal endpoint-coordinate gauge.  Moreover

```text
lambda(G_(i-1))/lambda(F_i)=-(1+A_i),               (10)
1+A_i!=0,                                           (11)
H=(-1)^m product_i (1+A_i).                         (12)
```

### Proof

The matchings `X_(i,a)` and `F_i` induce the same word `chi_i`.  Under a
diagonal endpoint scaling, all matching weights at that word acquire the
same nonzero character.  Their ratios and their sum `A_i` are therefore
gauge invariant.

Divide (8) by the nonzero monomial `lambda(F_i)`.  This gives (10).  Its left
side is nonzero, proving (11).  Multiplying (10) around the cycle yields

```text
product_i lambda(G_(i-1))/lambda(F_i)
 =(-1)^m product_i(1+A_i).                          (13)
```

Cyclic reindexing identifies the left side with (6), proving (12).  QED.

No aggregate sum is divided out.  The only denominators are selected
nonzero physical matching monomials.

### Corollary 2 (split and coupled aggregate fibres)

The following distinctions are exact.

```text
all A_i=0:
    H=(-1)^m, even if some k_i>0;

some A_i!=0:
    the holonomy defect is exactly product_i(1+A_i);

holonomy restriction beyond (12):
    requires an additional relation among the A_i.  (14)
```

In particular, combinatorial aggregate size does not imply a nonzero
aggregate defect.  Nor does one nonzero defect alone give a contradiction:
different factors can multiply to one or to another allowed nonzero value.

## 3. A complete physical aggregate-cycle family

Use vertices `0,...,7` and the three words

```text
chi_0=(0,0,0,0,1,1,1,1),
chi_1=(0,0,1,1,0,0,1,1),
chi_2=(0,1,0,1,0,1,0,1).                           (15)
```

Start with the established three-step transport data

```text
i   E_i       P_i       B_i
0   24|35     01|67     23|45
1   12|56     04|37     15|26
2   14|36     02|57     46|13.                      (16)
```

An edge in `E_i` receives its endpoint labels from `chi_i`; an edge in
`P_i` receives its equal labels from `chi_i`; and an edge in `B_i` receives
its equal labels from `chi_(i+1)`.  These 18 edges are distinct.

Give every displayed edge weight one except

```text
lambda_24=x=-(1+2t)/2,
lambda_12=lambda_14=-1,                             (17)
```

where

```text
t!=0,
1+2t!=0.                                           (18)
```

Add four edges compatible with `chi_0`:

```text
edge   endpoint labels   weight
03     (0,0)             1
16     (0,1)             1
25     (0,1)             1
47     (1,1)             t.                         (19)
```

Complete the remaining six physical pairs as follows:

```text
edge   endpoint labels   weight
05     (1,2)             1
06     (2,2)             1
07     (1,0)             1
17     (2,2)             1
27     (2,0)             1
34     (2,2)             1.                         (20)
```

Equations (16), (19), and (20) assign one nonzero matrix unit to every one
of the 28 physical pairs.  Every vertex sees all three endpoint labels
`0,1,2`, so the matrix-unit support is locally concise.  Each edge in (20)
disagrees with every cycle word at at least one endpoint and contributes to
none of the three cycle fibres.

### Theorem 3 (one aggregate and two binomial cycle fibres)

The complete compatible matching fibres of (15) are exactly

```text
chi_0:
  01|24|35|67     weight x       selected F_0,
  02|13|46|57     weight 1       incoming G_2,
  02|16|35|47     weight t,
  03|16|24|57     weight x,
  03|16|25|47     weight t;

chi_1:
  01|23|45|67     weight 1       incoming G_0,
  04|12|37|56     weight -1      selected F_1;

chi_2:
  02|14|36|57     weight -1      selected F_2,
  04|15|26|37     weight 1       incoming G_1.       (21)
```

All three complete fibre sums vanish.  The first is aggregate and the other
two are binomial.  The selected cycle holonomy is

```text
H=1/x=-2/(1+2t).                                   (22)
```

### Proof

There are only `105` perfect matchings on eight labelled vertices.  Exact
compatibility enumeration gives precisely (21).  The two binomial sums are
`1-1=0`.  The aggregate sum is

```text
1+x+t+x+t=1+2x+2t=0                                (23)
```

by (17).  All bridge-edge products equal one.  The three selected cross-core
products are `x,-1,-1`, so (6) gives (22).  QED.

The aggregate defect at `chi_0`, normalized by `F_0`, is

```text
A_0=(t+x+t)/x=(x+2t)/x,                            (24)
```

while `A_1=A_2=0`.  Direct substitution gives

```text
(-1)^3(1+A_0)=1/x=H,                               (25)
```

as required by Theorem 1.

### Split aggregate specialization

At `t=1/2`, one has `x=-1`.  The three extra terms in the aggregate fibre
are

```text
1/2,-1,1/2,                                        (26)
```

so `A_0=0` even though all three terms are nonzero.  The selected pair also
cancels, and `H=-1=(-1)^3`.  This is an exact split aggregate fibre.

### Nonsplit specialization

At `t=1`, one has `x=-3/2`.  The extra sum is `1/2`, the aggregate defect is
`A_0=-1/3`, and

```text
H=-2/3.                                             (27)
```

Thus the same complete label support and the same three transport words admit
both the binomial sign and a different holonomy value while preserving all
three complete cycle equations.

## 4. Exact holonomy elimination of the family

Before substituting (17), use independent Laurent variables `x,t,H` and the
two exact equations

```text
1+2x+2t=0,
Hx-1=0.                                             (28)
```

Let

```text
R=Q[x^(+-1),t^(+-1),H^(+-1),(1+2t)^(-1)]           (29)
```

and `I` be the ideal generated by (28).

### Theorem 4 (zero aggregate-cycle holonomy elimination)

One has

```text
I intersect Q[H,H^(-1)]=(0).                       (30)
```

### Proof

The quotient maps to `Q(t)` by

```text
x |-> -(1+2t)/2,
H |-> -2/(1+2t).                                   (31)
```

Both equations (28) vanish and every localized element maps to a nonzero
rational function on the stated open set.

The image of `H` is a nonconstant rational function of the transcendental
parameter `t`.  Therefore the induced homomorphism

```text
Q[H,H^(-1)] -> Q(t)                                (32)
```

is injective: a nonzero Laurent polynomial in `H` cannot vanish after
substitution of a transcendental rational function.  Hence no nonzero
Laurent polynomial in `H` lies in `I`, proving (30).  QED.

Equivalently, (22) takes every value in `C^*` except at most the single value
corresponding to the excluded divisor `t=0`; its image is Zariski dense.
This is an exact elimination statement, not numerical sampling.

## 5. Why the family is not a witness

For each constant word `c^8`, `c=0,1,2`, the table has no compatible perfect
matching.  Its three pure coefficients are therefore zero, whereas the GHZ
target requires them to be one.  Thus the family fails the target equations
before any global conclusion can be drawn.

The family proves only a method boundary inside complete nonzero, locally
concise matrix-unit support:

```text
complete physical pairs:                   YES;
all three local endpoint labels:            YES;
three complete active-cycle equations:      YES;
one aggregate cycle fibre:                  YES, five terms;
holonomy constrained by those equations:    NO, elimination ideal zero;
all pure target equations:                  FAIL;
complete GHZ target:                        FAIL;
Krenn--Gu counterexample:                   NO.       (33)
```

## 6. Consequence for the live `U7` edge

The aggregate active-cycle branch now has the exact normal form

```text
H=(-1)^m product_i(1+A_i),                          (34)
```

with gauge-invariant Laurent-sum defects.  This yields three rigorous
conclusions.

1. Aggregate combinatorics does not automatically destroy the binomial
   sign: a nonempty extra subfibre may cancel exactly.
2. Aggregate cycle equations alone do not produce a holonomy polynomial:
   the complete locally concise family (15)--(20) has zero elimination ideal
   in `H`.
3. A successful aggregate continuation must prove an additional equation
   that couples the defects, forces their product, or makes the full target
   ideal a unit.  Merely counting extra matchings or observing shared physical
   variables is insufficient.

This closes the route "an aggregate cycle fibre by itself constrains or
contradicts holonomy."  It does not close aggregate fibres after imposing
the complete target block.  The next load-bearing alternatives are effective
cross-multiplicity overlap, a forced low-rank quotient with every sheet
killed, or a mixed/deeper coupling to the pure structures.

## 7. Assumptions and boundary

```text
field for factorisation:                         C (indeed any field where selected monomials are nonzero);
physical branch:                                 complete nonzero r=1 matrix units;
cycle input:                                     imported active transport cycle;
complete fibre equations:                        every compatible matching included;
aggregate defects gauge invariant:               PROVED;
holonomy defect product:                          PROVED;
split aggregate compatible with sign holonomy:    PROVED;
complete locally concise sharpness table:         PROVED over Q(t);
selected cycle elimination in H:                  ZERO IDEAL;
pure target coefficients in sharpness table:      ZERO, so not a witness;
complete target constrains every defect product:  UNKNOWN;
effective cross-multiplicity overlap forced:       UNKNOWN;
aggregate active-cycle branch excluded:           UNKNOWN;
general r=1 branch excluded:                       UNKNOWN;
global Krenn--Gu conjecture:                       UNRESOLVED.
```

The excluded sharpness divisors are exactly `t=0` and `1+2t=0`; they ensure
that the new physical edge and selected edge `24` remain nonzero.  The
factorisation theorem itself introduces no division by an aggregate defect
or by `1+A_i`; equation (11) proves the latter is nonzero.

## 8. Evidence and replay

Run:

```powershell
python claims/arbitrary-order/verify_matrix_unit_aggregate_active_cycle_defect_factorisation_and_split_fibre_sharpness.py
python claims/arbitrary-order/audit_matrix_unit_aggregate_active_cycle_defect_factorisation_and_split_fibre_sharpness.py
python -m py_compile claims/arbitrary-order/verify_matrix_unit_aggregate_active_cycle_defect_factorisation_and_split_fibre_sharpness.py claims/arbitrary-order/audit_matrix_unit_aggregate_active_cycle_defect_factorisation_and_split_fibre_sharpness.py
python -m ruff check claims/arbitrary-order/verify_matrix_unit_aggregate_active_cycle_defect_factorisation_and_split_fibre_sharpness.py claims/arbitrary-order/audit_matrix_unit_aggregate_active_cycle_defect_factorisation_and_split_fibre_sharpness.py
```

The primary verifier uses exact SymPy rational functions and a recursive
matching-first census.  It checks all 28 physical pairs, local label
concision, the complete `5/2/2` cycle fibres, the defect product, split and
nonsplit specializations, absence of pure matchings, endpoint-character
circulation, and the small exact elimination ideal.

The independent no-import audit uses disjoint edge masks, exact `Fraction`
specializations, and a separate triangular polynomial-substitution argument.
It independently checks the complete matching census, the gauge-character
cancellation, the two defect regimes, and injectivity of the holonomy
parameter through bounded degree.  The arbitrary-order result is the written
complete-fibre division and telescoping proof; the physical sharpness and
elimination statements are exact finite algebra, not a global case census.
