# Residual-depth observability staircase and all-depth kernel theorem

## Status

**Exact characteristic-zero root-budget theorem and sharp scalar-response
no-go.**  Retaining every principal residual subset does not repair the P7
observability problem.  If the original cell has an even residual set `Q` of
size `q` and `7-q` probe roots, a root-saturated principal-cofactor term that
leaves residual subset `T subset Q` and blocker-port set `S` must satisfy

```text
|S|+|T|>=2q.                                            (1)
```

Thus the legal deletion budget supplies an **upper staircase** in residual/
port bidegree.  Residual-relative inversion, the loop-hafnian cumulants, the
two-residual discriminant, and the zeon-apolar catalecticants instead require
proper subset faces below the observed coefficient.  Their natural domain is
a downward-closed deletion chart.  The two shapes do not agree.

This mismatch is sharp inside the honest scalar matching-response variety.

1. At `q=2`, a one-parameter graph family has identical values at **every**
   root-budget-eligible coefficient of all four residual depths
   `M,Y_0,Y_1,Z`, while its hidden direct pair, singleton residual row,
   corrected quadratic response, and degree-two discriminant all vary.
2. Even after adjoining the four standard marked-star observations, the
   torus-zero pair already in the repository has identical complete
   root-budget layers and marked stars but different direct pair families.
3. For every even `q>=4`, another one-parameter graph family has fixed
   residual matrix, fixed direct graph, fixed residual constants, and
   identical values at **all** budget-eligible residual depths, while a
   quadratic common-cofactor Gram entry and the corresponding zeon
   catalecticant entry vary.

Consequently no selector or postprocessing rule confined to the current
root-saturated principal-cofactor layers can manufacture the synchronized
depths required by the new discriminant or catalecticant theorems.  A new
mixed-root identity, herald/vacuum gadget, or target-specific equation must
cross below the staircase.

The controls are physical scalar response graphs, not full mixed-GHZ P7
realizations.  Hence they prove the strongest universal observability no-go
for the present mechanism, not a P7 counterexample.  Whether the complete
GHZ/root coefficient system forces an additional cross-depth observation
remains **UNKNOWN**, and Krenn--Gu remains **UNRESOLVED**.

No graph family, support family, colour word, matching family, or parameter
set is enumerated.

## 1. The bidegree root budget

Let

```text
P: probe roots,       |P|=r=7-q,
Q: residual vertices, |Q|=q,
B: blocker ports,      |B|=7.                           (2)
```

For `T subset Q` and `S subset B`, write

```text
Z_(T,S)=haf G[T union S].                               (3)
```

Thus `Z_(empty,S)=m_S`, while `Z_(Q,S)=z_S`.  A nonzero
response has the parity condition `|T|+|S|` even.

Expand a legal coefficient along all probe roots.  To leave precisely
`T union S` in the complementary principal cofactor, the root shore must
remove every vertex of

```text
(Q minus T) union (B minus S).                          (4)
```

Every removed nonroot is the distinct endpoint of a root--nonroot edge.
Root--root edges consume two roots and remove no nonroot.

### Theorem 1 (residual-depth staircase)

Any response coefficient directly isolated by the root-saturated
principal-cofactor mechanism must satisfy

```text
(q-|T|)+(7-|S|)<=7-q,
```

equivalently (1).

Proof.  The left side counts the nonroots in (4).  At most `r=7-q` distinct
nonroots can be paired to the roots.  Rearrangement gives (1).  Root--root
companions only reduce the available root--nonroot edges, so they cannot
improve the bound.

For the active `q=2` cell, the four residual depths therefore begin at

```text
M=Z_empty:       even port degree 4,
Y_0,Y_1:         odd  port degree 3,
Z=Z_{01}:        even port degree 2.                    (5)
```

In particular, the direct pairs `m_uv` and the one-residual singleton rows
`y_(i,u)` lie strictly below the staircase.

For `q=4`, the successive minimum port degrees for residual orders
`0,1,2,3,4` are `8,7,6,5,4`; for `q=6` they are
`12,11,10,9,8,7,6`.  Port parity may raise an odd threshold by one, but never
lowers it.

Eligibility remains only necessary.  A shore and a private companion
selector are still required at every eligible bidegree.

## 2. Upper filters versus deletion ideals

For fixed residual depth `T`, the eligible port subsets form the upper rank
filter

```text
F_T={S subset B: |S|>=2q-|T|}.                          (6)
```

By contrast, finite square-zero division

```text
Phi_T=M^(-1)Z_T                                        (7)
```

uses the recursion

```text
phi_(T,S)
 =z_(T,S)-sum_(U proper_subset S) phi_(T,U)m_(S minus U). (8)
```

It requires proper subset faces.  The residual-depth logarithm uses still
more residual subsets, and a square-free catalecticant concatenates several
of these relative coefficients.

### Proposition 2 (filter/ideal mismatch)

If `2q-|T|>0`, the budget family (6) is not a downward-closed domain for
(8).  In particular, for `q=2` no positive even discriminant coefficient can
be expanded from budget-eligible tower data alone: the coefficient formula

```text
D_S=sum_(U subset S)m_U z_(S minus U)
    -sum_(U subset S)y_(0,U)y_(1,S minus U)              (9)
```

contains the below-budget pair layer `m_2` and singleton layers `y_(i,1)`.

Proof.  Any eligible nonempty `S` of size at least the positive threshold
contains proper subsets below that threshold.  Equation (8) explicitly uses
them.  In (9), take an edge of any matching of the even set `S`: its
two-subset supplies an `m_2` term.  Splitting off one vertex supplies the
`y_(0,1)y_(1,|S|-1)` and reversed terms.  For `q=2`, degrees two and one are
below (5).

The proposition is a statement about the domain of the convolution, not a
claim that target equations can never reconstruct the missing faces.  The
physical fibers below prove that physical matching recursion alone does not.

## 3. A nonzero-`h` all-depth kernel at `q=2`

Use seven ports but activate only `u,v`.  For a parameter `t`, install

```text
B_uv=t,
A_(q_0,q_1)=1,
R_(q_0,u)=1,
R_(q_1,v)=-t,                                           (10)
```

and set every other edge to zero.  Put `X=x_u x_v` in the square-zero port
algebra.  Then

```text
M_t=1+tX,
Y_(0,t)=x_u,
Y_(1,t)=-t x_v,
Z_t=M_t(1-tX)=1.                                       (11)
```

Every positive-degree coefficient in `M_t` has degree two, every coefficient
in `Y_(i,t)` has degree one, and `Z_t` has no positive-degree coefficient.
Comparing with (5) proves that **every** root-budget-eligible coefficient of
all four depths is independent of `t` (indeed zero).  The constants
`M_empty=Z_empty=1` and the singleton-depth constants zero are fixed as well.

Nevertheless

```text
m_uv=t,
y_(1,v)=-t,
Phi_(01,t)=Z_t/M_t=1-tX,
k_uv=[X]Phi_(01,t)=-t.                                  (12)
```

The division-free discriminant is exact:

```text
M_t Z_t-Y_(0,t)Y_(1,t)
 =1+2tX=M_t^2,                                         (13)
```

so its degree-two coefficient is

```text
D_uv=2t=2h m_uv.                                       (14)
```

### Theorem 3 (all-depth observation kernel at `q=2`)

The map from honest two-residual response graphs to the complete set of
root-budget-eligible coefficients at every principal residual depth has a
nonconstant affine-line fiber, even with `h=1` and all residual constants
fixed.  Along that fiber the corrected quadratic channel and the first
discriminant coefficient vary.

Hence adding the legally **eligible** odd `Y_i` layers to the previously
studied `M,Z` layers does not make the discriminant observable.  The missing
singleton `Y_i` faces, rather than the higher odd faces, are essential.

The standard marked-star sum sees `B_uv=t`; thus this particular family is
not a countermodel after granting arbitrary extra marked-star observations.
The next control isolates that separate issue.

## 4. Marked stars still do not close the torus-zero branch

On four active ports ordered by
`(12,13,14,23,24,34)`, take

```text
B^(0)=(-1,1,0,0,1,-1),
B^(1)=(-1,0,1,1,0,-1).                                 (15)
```

Both lie in the kernel of the four marked-star incidence rows and satisfy

```text
m_1234=2.                                               (16)
```

Adjoin three isolated ports.  Set the residual edge and every residual--port
incidence to zero.  Then for both graphs

```text
Y_0=Y_1=Z=0,                                           (17)
```

all eligible direct moments agree (`m_4` is nonzero only on `1234` and equals
two; `m_6=0`), and all marked-star observations agree and equal zero.

### Proposition 4 (marked-star all-depth kernel at `h=0`)

The four marked stars, both top coefficients, and every root-budget-eligible
coefficient at all four residual depths do not determine the direct pair
family on the torus-zero branch.

This proposition does not settle the stronger chart with `h!=0`, marked
stars, and legally selected `Y_3,Y_5` simultaneously.  No theorem currently
forces that joint chart.

## 5. Higher residual order hides even the common Gram entry

Let `q>=4` be even.  Label residuals `0,...,q-1`.  Put a unit perfect
matching in the residual graph:

```text
A_01=A_23=...=A_(q-2,q-1)=1,                           (18)
```

with all other residual edges zero.  Set the direct port graph to zero and
activate only two residual--port incidences

```text
R_(0,u)=1,                  R_(1,v)=t.                 (19)
```

All principal residual constants are fixed by `A`.  Every port-dependent
coefficient at every residual subset has degree at most two, because only
`u,v` have incidence edges.  But Theorem 1 requires

```text
|S|>=2q-|T|>=q>=4                                      (20)
```

for every `T subset Q`.  Therefore every budget-eligible positive-degree
coefficient at every residual depth is zero and independent of `t`.

At the full residual depth, the unmatched residuals `2,...,q-1` use the
fixed perfect matching, while `0,1` may either match each other or use the two
ports.  Hence

```text
Phi_Q=Z_Q=1+t x_u x_v.                                 (21)
```

Thus

```text
[x_u x_v]Phi_Q=t                                       (22)
```

is a varying common-cofactor Gram entry.  It is also an entry of the
one-leg zeon-apolar catalecticant, while every direct marked-star observation
is fixed because `B=0`.

### Theorem 5 (higher-residual all-depth kernel)

For every even `q>=4`, the complete root-budget-eligible principal residual
tower has an affine-line physical response fiber on which the quadratic
relative response, common Gram layer, and a zeon catalecticant entry vary.

In the P7 splits this applies to `q=4` and `q=6`.  Therefore neither exposing
all eligible residual subsets nor adjoining direct marked stars can form a
nontrivial relative catalecticant without a new below-staircase observation.

## 6. Exact consequence for legal selectors

Suppose a fixed root shore and legal companion probes isolate any collection
of principal response coefficients satisfying (1), with arbitrary common
nonzero shore normalizations.  The families above may be placed behind the
same fixed shore data.  Every isolated cofactor value is identical along the
relevant parameter fiber, so every linear selector and every polynomial
postprocessing of those values is identical as well.

The invisible directions are:

```text
q=2:   direct pair + one-residual singleton + corrected Phi_2;
q>=4:  corrected Phi_2/common Gram + zeon Cat_1 entry.  (23)
```

This refutes the following hoped-for implication:

```text
all root-budget-eligible residual depths
    => partition-closed relative response chart.        (24)
```

It does **not** refute a selector using a new mixed coefficient outside the
principal-cofactor mechanism.  In particular, a GHZ-specific linear
dependence could couple an eligible top coefficient to a below-budget face,
and a herald or vacuum simulator could change the deletion count.  Those are
precisely the remaining routes.

## Scope wall

```text
general residual-depth budget |S|+|T|>=2q:             PROVED;
budget staircase is not convolution/down-set closed:  PROVED;
q=2 all-depth eligible observation map has A1 fiber:   PROVED;
q=2 hidden discriminant/common channel varies:         PROVED;
q=2 stars + all depths fail at h=0:                    PROVED;
even q>=4 all-depth eligible map has A1 fiber:          PROVED;
q>=4 hidden common-Gram/catalecticant entry varies:     PROVED;
budget layers => partition-closed relative chart:       FALSE;
h!=0 stars + synchronized odd-depth joint selector:     UNKNOWN;
new GHZ-specific cross-staircase identity:              UNKNOWN;
legal herald/vacuum/deletion simulator:                 UNKNOWN;
full target-compatible physical P7 boundary:            UNKNOWN;
unrestricted P5/P6/P7 nonrestriction:                  UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_residual_depth_observability_staircase_and_all_depth_kernel.py
python audit_residual_depth_observability_staircase_and_all_depth_kernel.py
python -m py_compile verify_residual_depth_observability_staircase_and_all_depth_kernel.py audit_residual_depth_observability_staircase_and_all_depth_kernel.py
uv run --with ruff ruff check verify_residual_depth_observability_staircase_and_all_depth_kernel.py audit_residual_depth_observability_staircase_and_all_depth_kernel.py
```

The primary replay checks the symbolic `q=2` residual tower and discriminant,
the marked-star kernel, and the complete parameter-dependence/eligibility
ledger at `q=4,6`.  The independent no-import audit compares two rational
parameters using a separately written square-zero matching product and exact
four-hafnian/star calculations.  Neither replay searches graphs, supports,
colour words, matchings, selectors, or parameters.
