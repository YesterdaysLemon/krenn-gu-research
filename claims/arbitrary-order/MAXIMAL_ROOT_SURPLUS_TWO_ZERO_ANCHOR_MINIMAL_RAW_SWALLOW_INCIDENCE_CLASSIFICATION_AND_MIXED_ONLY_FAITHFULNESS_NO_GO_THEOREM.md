# Maximum-root surplus-two zero-anchor minimal raw-swallow incidence classification and mixed-only faithfulness no-go

## Status and scope

**Exact characteristic-zero arbitrary-root fibre exclusion, incidence-channel
classification, and four-port physical no-go theorem.**  Retain the zero-anchor
promoted chart of `GLS36`.  Here **full swallow** means
`q,r_0,r_1,r_2 in B_Q^anc`.  If the complete raw nuisance fully swallows these
four tensors and has its smallest possible rank three, then it is the
three-dimensional diagonal space.  The branch on which both residual shore
spaces have rank two is empty: the swallowed root deck pins both shores to one
two-colour plane, and every incidence generator is then supported on that
plane, whose diagonal part has dimension only two.

Equivalently, pointwise at every eligible promoted root order `r>=3` and every
divisor/rank fibre,

```text
full swallow + both residual shore ranks two
  => rank B_Q^anc >=4;

full swallow + rank B_Q^anc=3
  => at least one residual shore rank is at most one.       (1)
```

No incidence minor is selected and no response, deck, or residual parameter
is divided out.  This is a genuine exclusion of one complete nuisance-rank /
shore-rank fibre.  It is not a source-cover theorem and does not exclude the
remaining shore-rank-drop fibres or any full-swallow fibre of rank at least
four.

An independently reconstructed physical control also shows that the mixed
part of the `GLS36` labelwise-lift condition can be vacuous even when `q` is
literally swallowed and the local residual-absent output anchor is nonzero.
The control is not full-swallow, is not pure-normalized, and fails a pure-port
slice of the complete target.  Thus this mixed-only premise is insufficient:
a future exclusion must use at least one additional full-witness gate absent
from the control.  In the intended full-swallow route, the pure/full-swallow
and pure-port package supplies such missing information.

This is `GLS37`.  The maximum-root surplus-two supply-and-target-attachment
node and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Dependencies, provenance, and an interface correction

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the promoted root-companion grading and two-root/two-label bijection;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for the raw anchor module, full-swallow dichotomy, and physical control; and
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the incidence map and fixed-residual labelwise lift.

No external literature claim is used.  The new content is the minimal-rank
two-shore exclusion, the exact two-channel description used in its audit, and
the mixed-only labelwise-faithfulness no-go.

This tranche also corrects one explanation in the first merged version of
`GLS36`.  Under the owning `GLS8` grading, `G_D^A` for `|D|=2` is the sum of
the two root-to-`D` bijections.  It does **not** include an internal matching
`omega W_D`; that matching belongs to a different grade in the physical
four-vertex perfect-matching expansion.  Therefore edges internal to
`Bhat` never occur in the coefficient companion `G_D^A`.  On `omega=0`, the
published `GLS36` formulas for `sigma_Q`, the equality
`B_Q^anc=im sigma_Q`, and every finite rank computation remain unchanged.
The corrected proof below uses the owning companion definition directly and
does not infer a nonzero-`omega` statement from the mistyped expansion.

## 1. Correct incidence presentation

Retain the notation

```text
A={a_0,a_1},                   Q={q_0,q_1},
Bhat=Q disjoint-union Uhat,    omega=W_(a_0,a_1)=0,
E_A^*=V_(a_0)^* tensor V_(a_1)^*.                    (2)
```

At fixed residual vectors put

```text
a_s=xi_0^s=W_(a_0,q_s)(-,z_(q_s)),
b_s=xi_1^s=W_(a_1,q_s)(-,z_(q_s)),                   (3)

X_u(x)=W_(a_0,u)(-,x),
Y_u(x)=W_(a_1,u)(-,x).                               (4)
```

For `D={q_s,u}`, the owning grade-zero root companion evaluated at the
residual is

```text
a_s tensor Y_u(x)+X_u(x) tensor b_s.                 (5)
```

For `D={u,v}`, its coefficient slices are

```text
X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x).           (6)
```

These are precisely the component maps of `sigma_Q`.  Before the zero-anchor
specialization, the raw anchor module has the separate top summand
`K omega`; the pair companions (5)--(6) themselves contain no internal
`Bhat` edge.  Hence on (2)

```text
B=B_Q^anc=im sigma_Q.                                 (7)
```

This proves the corrected `GLS36` incidence presentation directly from
`GLS8`.

## 2. Minimal full-swallow rank excludes two rank-two shores

Let `e_(i,c)^*`, `c=0,1,2`, be the colour basis at probe `a_i`, and put

```text
r_c=e_(0,c)^* tensor e_(1,c)^*,
Delta=span{r_0,r_1,r_2},
S_0=span{a_0,a_1} subset V_(a_0)^*,
S_1=span{b_0,b_1} subset V_(a_1)^*.                  (8)
```

Here the subscripts on `a_s,b_s` label residual vertices, while the first
subscript on `e_(i,c)^*` labels the probe shore.

### Theorem 1 (minimal-rank two-shore fibre is empty)

Assume pointwise that

```text
r_0,r_1,r_2,q in B,       dim B=3,
dim S_0=dim S_1=2,                                 (9)
```

where

```text
q=a_0 tensor b_1+a_1 tensor b_0.                    (10)
```

Then (9) is impossible.

#### Proof

The three `r_c` are independent, so full swallow and `dim B=3` give

```text
B=Delta.                                             (11)
```

Matricize (10) from the second shore to the first.  If `A` and `C` are the
three-by-two matrices with columns `(a_0,a_1)` and `(b_0,b_1)`, then

```text
q=A J C^T,                 J=[[0,1],[1,0]].           (12)
```

Both shore matrices have rank two and `J` is invertible, so `q` has rank two,
its column space is `S_0`, and its row space is `S_1`.  By (11), `q` is
diagonal.  Therefore exactly two diagonal coefficients of `q` are nonzero.
For their colour set `P={c,d}`,

```text
S_0=span{e_(0,c)^*,e_(0,d)^*},
S_1=span{e_(1,c)^*,e_(1,d)^*}.                       (13)
```

Let `k` be the missing colour.  For arbitrary `u in Uhat` and `x in V_u`,
the two one-residual columns (5) belong to `B=Delta`.  In the matrix entry
`(i,k)`, `i in P`, equation (5) reads

```text
a_s(i) Y_u(x)(k)=0                                   (14)
```

because every `b_s(k)` is zero.  Since the `a_s` span the two-colour plane,
(14), for `s=0,1`, forces `Y_u(x)(k)=0`.  Applying the same argument to the
entry `(k,j)`, `j in P`, forces `X_u(x)(k)=0`.  Thus every port-incidence
slice belongs to the corresponding two-colour shore plane.

It follows from (5)--(6) that every column of `sigma_Q` is supported in

```text
span{e_(0,c)^*,e_(0,d)^*}
 tensor span{e_(1,c)^*,e_(1,d)^*}.                   (15)
```

Every such column also belongs to `B=Delta` by (7) and (11).  The
intersection of (15) with `Delta` is only

```text
span{r_c,r_d},                                       (16)
```

so `rank sigma_Q<=2`.  This contradicts (7) and `dim B=3`.  No minor,
response, or parameter has been divided out. `square`

### Corollary 1.1 (all-eligible-root pointwise rank alternative)

On every zero-anchor full-swallow point,

```text
dim S_0=dim S_1=2  => dim B_Q^anc>=4,                (17)

dim B_Q^anc=3      => min(dim S_0,dim S_1)<=1.       (18)
```

This includes every residual, incidence-rank, nuisance-rank, and divisor
fibre at every promoted root order `r>=3`.  It does not say that either
remaining alternative is empty.

### Lemma 1.2 (two one-residual channels)

In the intermediate situation (11)--(13), before the final image-rank
contradiction, define the allowed one-residual port space

```text
K_P={(x,y):a_s tensor y+x tensor b_s in Delta for s=0,1}. (19)
```

Every `(x,y)` lies in the two shore planes of (13).  The remaining
off-diagonal equations split as

```text
[ (a_0(c),a_1(c))^T  (b_0(d),b_1(d))^T ] (y(d),x(c))^T=0,

[ (a_0(d),a_1(d))^T  (b_0(c),b_1(c))^T ] (y(c),x(d))^T=0. (20)
```

Each two-by-two kernel has dimension at most one, and every nonzero kernel
vector has both entries nonzero.  Thus `dim K_P` can be zero, one, or two and
is the direct sum of at most two cross-colour channels.  If the pair labels
between distinct ports must also lie in `Delta`, the same nonzero channel
cannot occur at two ports: its self-pair has a nonzero off-diagonal
coefficient `2x(c)y(d)` or `2x(d)y(c)` in characteristic zero.  Hence at most
two ports can have nonzero `(X_u,Y_u)` incidence.  The focused checks exhibit
exact shore charts of all three local channel dimensions.  The sharper
contradiction in Theorem 1 uses the complete image equality and supersedes
this port count for the full-swallow rank-three fibre.

## 3. Mixed-only labelwise faithfulness is insufficient

Retain the exact four-port graph from `GLS35`, with vertex order

```text
(a_0,a_1,q_0,q_1,u_0,u_1,u_2,u_3).                  (21)
```

Its residual incidences give

```text
q=r_1+r_2,       p=2,                                (22)
```

and every port has the two incidence matrices

```text
W_0=
 [[ 0, 1,-1],
  [ 1, 0, 0],
  [-1, 0, 1]],

W_1=
 [[ 1, 1,-1],
  [ 0,-1, 2],
  [-1, 0, 0]].                                      (23)
```

The only port--port edges are

```text
W_(u_0,u_1)=e_0 e_0^T,
W_(u_2,u_3)=(1/2)e_0 e_0^T,                          (24)
```

and every residual--residual and residual--port edge is zero.

### Theorem 2 (exact mixed-only faithfulness no-go)

For (21)--(24),

```text
rank B=rank[B|q]=8,
rank[B|r_c]=9                  for c=0,1,2.           (25)
```

Thus `q` is swallowed but none of the three pure probes is swallowed.  Every
non-`Q` complementary deck in the `GLS36` map `rho_Q` is zero: deleting a
one-residual label leaves the other residual isolated, and deleting a
two-port label leaves both residuals isolated.  Meanwhile

```text
H_Uhat=(1/2)(e_0^*)^(tensor4),
p H_Uhat(e_0,e_0,e_0,e_0)=1.                         (26)
```

Consequently, for **every** certificate `v` with `sigma_Q(v)=q` and every
mixed port test `z in Z_mix`,

```text
rho_Q(z)+H_Uhat(z)v=0 in ker sigma_Q.                 (27)
```

So the complete mixed-port labelwise-lift condition of `GLS36` holds while
the local residual-absent output anchor is nonzero.

The full physical state is nevertheless exactly

```text
(1/2)|11000000>+(1/2)|22000000>.                     (28)
```

After contracting `q_0,q_1` by `(1,1,1)`, the only port word is `0000` and
its probe coefficient is `q/2`, of rank two.  All `78` mixed port words have
zero coefficient.  Thus (27) omits the displayed pure-port failure.  The
actual graph has pure full-state coefficients `(0,0,0)`; if one instead
compares the local interface with the declared normalized diagonal weights
`(1,1,1)` from `GLS35`, the three pure-port defect ranks are `(3,1,1)`.

#### Proof

Exact coefficient slicing of (23) gives the ranks (25), including all `78`
raw columns.  The isolation claim follows immediately from the undeclared
zero edges.  The port deck has the single matching in (24), proving (26).
Since `Z_mix` kills every pure port tensor, (26) gives `H_Uhat(z)=0`; isolation
gives `rho_Q(z)=0`, proving (27) independently of `v`.  Exact expansion of
the `105` perfect matchings on eight vertices gives (28) and the contracted
support statement. `square`

This control does not satisfy the full-swallow premise of Theorem 1, the
complete pure target, maximum-root maximality, or blocker saturation.  It is
not a witness and not a counterexample.  It proves only that

```text
q-swallow + nonzero local H_Uhat + mixed-port lift
```

does not by itself replace the full-swallow and pure-port target package.

## 4. Frontier and unresolved remainder

```text
correct promoted incidence companion typing:                    PROVED;
full-swallow rank 3 with both shore ranks 2:                     EXCLUDED;
rank-3 full swallow with a shore rank at most 1:                 OPEN;
full swallow with nuisance rank at least 4:                     OPEN;
mixed-only faithfulness from q-swallow/local output survival:    FALSE;
complete pure/full-swallow deck-coupled contradiction:          UNKNOWN;
raw escape supplies an original legal target package:           FALSE;
arbitrary-root source cover and strategic-node closure:         UNKNOWN;
global Krenn--Gu conjecture:                                    UNRESOLVED.
```

The smallest remaining zero-anchor obligation is now the union of two
pointwise branches:

1. full swallow with `rank B=3` and at least one residual shore of rank at
   most one; and
2. full swallow with `rank B>=4`.

Either branch must be contradicted by the same graph's complete pure and
mixed GHZ equations, or be transported through a named downstream theorem
with every selector, response/activity, synchronization, nuisance-survival,
anchor, exceptional-fibre, and arbitrary-root source gate proved.  The
q-swallowed control shows that a proof using only the mixed subspace of one
fixed contraction cannot suffice.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_minimal_raw_swallow_incidence_classification_and_mixed_only_faithfulness_nogo.py
```

The primary uses exact SymPy matrices, the existing GLS35 construction, and
direct perfect-matching coefficients.  The audit imports no project module
and no third-party package; it uses standard-library `Fraction` elimination,
`496` independently reconstructed exact shore charts, sparse matching-state
expansion, and an independently rebuilt graph.  These scripts audit the
finite and coordinate leaves.  The arbitrary-root fibre exclusion is the
symbolic proof of Theorem 1.
