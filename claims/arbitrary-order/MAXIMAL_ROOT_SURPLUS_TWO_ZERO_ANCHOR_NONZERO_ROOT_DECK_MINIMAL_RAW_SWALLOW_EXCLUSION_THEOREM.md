# Maximum-root surplus-two zero-anchor nonzero-root-companion minimal raw-swallow exclusion

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise fibre exclusion.**
Continue the zero-anchor raw-incidence branch of `GLS37`.  If the raw nuisance
fully swallows

```text
q,r_0,r_1,r_2
```

and the root-companion coefficient `q` is nonzero, then the nuisance cannot
have its minimum possible rank three.  Equivalently, at every eligible promoted root order
`r>=3` and on every residual, shore-rank, nuisance-rank, incidence-rank, and
divisor fibre,

```text
omega=0,
q!=0,
q,r_0,r_1,r_2 in B_Q^anc
  => rank B_Q^anc>=4.                                 (1)
```

The new low-shore argument proves that a hypothetical rank-three point would
have both residual shore ranks two.  `GLS37` excludes exactly that remaining
two-shore fibre.  No response, complementary deck, minor, or parameter is
divided out.

Here `q=G_Q^A(z_Q)` is the raw root-companion coefficient of the physical
residual-absent deck `H_Uhat`; it is not that physical deck itself.  On the
complete-target non-silent branch of `GLS35`, `p!=0`, hence `q!=0`.
Therefore its full-swallow alternative now begins at nuisance rank four.
This does not exclude ranks four through nine or rank-three full swallow with
`q=0`; those open fibres include `p=0` and diagonal-silent cases.  It also
does not exclude raw escape, any nonzero-anchor branch, or any downstream
attachment gate.  It is not a source-cover or strategic-node closure theorem.

This is `GLS38`.  The maximum-root surplus-two supply-and-target-attachment
node and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the grade-zero two-root/two-label companion;
- [`GLS35`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_RAW_ROOT_DECK_QUOTIENT_AND_OUTPUT_COEFFICIENT_SEPARATION_NO_GO_THEOREM.md)
  for the complete-target non-silent escape/full-swallow dichotomy and the
  implication `p!=0 => q!=0`;
- [`GLS36`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_INCIDENCE_IMAGE_COMMON_ROW_SILENCE_AND_LABELWISE_LIFT_SHARPNESS_THEOREM.md)
  for the pointwise zero-anchor equality `B_Q^anc=im sigma_Q`; and
- [`GLS37`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_MINIMAL_RAW_SWALLOW_INCIDENCE_CLASSIFICATION_AND_MIXED_ONLY_FAITHFULNESS_NO_GO_THEOREM.md)
  for exclusion of the rank-three fibre with both residual shore ranks two.

No external literature claim is used.  The new content is the complete
rank-one-shore exclusion and its integration with `GLS37` into (1).

## 1. Setting

Retain the corrected zero-anchor incidence notation

```text
a_s=xi_0^s in V_(a_0)^*,
b_s=xi_1^s in V_(a_1)^*,

X_u(x)=W_(a_0,u)(-,x),
Y_u(x)=W_(a_1,u)(-,x),                               (2)

q=a_0 tensor b_1+a_1 tensor b_0,

S_0=span{a_0,a_1},       S_1=span{b_0,b_1},
d_i=dim S_i.                                         (3)
```

The incidence map has one-residual components

```text
sigma_(s,u)(x)=a_s tensor Y_u(x)+X_u(x) tensor b_s   (4)
```

and promoted-pair components

```text
sigma_(u,v)(x tensor y)
 =X_u(x) tensor Y_v(y)+X_v(y) tensor Y_u(x).         (5)
```

At `omega=0`, the corrected `GLS36` presentation is

```text
B=B_Q^anc=im sigma_Q.                                (6)
```

Put

```text
r_c=e_(0,c)^* tensor e_(1,c)^*,
Delta=span{r_0,r_1,r_2}.                             (7)
```

## 2. A low residual shore collapses the incidence image

### Lemma 1 (rank-one left shore forces one diagonal row)

Assume

```text
B=Delta,          q!=0,          q in Delta,
d_0<=1.                                               (8)
```

Then every column of `sigma_Q` lies in one common line `K r_c`.  In
particular, (6) and (8) cannot hold simultaneously.

#### Proof

Since `q!=0`, equation (3) rules out `d_0=0`.  Thus `d_0=1`; write

```text
a_s=lambda_s a.
```

Equation (3) gives

```text
q=a tensor d,
d=lambda_0 b_1+lambda_1 b_0.                         (9)
```

This is a nonzero rank-one diagonal tensor.  Hence for one colour `c`,

```text
a in K e_(0,c)^*,       0!=d in K e_(1,c)^*.         (10)
```

Fix an arbitrary port `u` and slice `z in V_u`, and abbreviate

```text
x=X_u(z),          y=Y_u(z).                         (11)
```

Each of the two columns (4) belongs to `B=Delta`.  Suppose some coordinate
`x(i)` is nonzero for `i!=c`.  In row `i`, the first term of (4) is zero by
(10).  Every off-diagonal `(i,j)` entry, `j!=i`, is therefore

```text
x(i)b_s(j)=0.
```

Thus both `b_s` are supported on the single coordinate `i`.  Equation (9)
then puts `d` in `K e_(1,i)^*`, contrary to the nonzero statement (10).
Therefore

```text
X_u(V_u) subset K e_(0,c)^*                         (12)
```

for every promoted port, including every incidence-rank-drop fibre.

Every one-residual column (4) is now supported in probe row `c`; since it is
also diagonal, it belongs to `K r_c`.  Every promoted-pair column (5) is
again supported in row `c` by (12), and its membership in `B=Delta` puts it
in the same line.  These are all columns of `sigma_Q`, so

```text
im sigma_Q subset K r_c.                             (13)
```

This contradicts (6) and `B=Delta`, which has dimension three.  No nonzero
coordinate was normalized or divided out: the argument assumes a coordinate
is nonzero only to show that assumption is impossible. `square`

### Lemma 1.1 (rank-one right shore)

Under (8) with `d_1<=1` in place of `d_0<=1`, the same conclusion holds.

#### Proof

Exchange the two probe shores and transpose every tensor in Lemma 1.  The
argument forces every `Y_u(V_u)` onto one coordinate axis, so all columns lie
in one common diagonal line. `square`

## 3. Complete minimal-rank exclusion

### Theorem 2 (nonzero root companion excludes rank-three full swallow)

Assume pointwise that

```text
omega=0,
q!=0,
q,r_0,r_1,r_2 in B_Q^anc,
rank B_Q^anc=3.                                      (14)
```

Then (14) is impossible.

#### Proof

The three pure tensors are independent, so (14) and full swallow give

```text
B_Q^anc=Delta.                                       (15)
```

Because `q!=0`, neither residual shore is zero; hence

```text
(d_0,d_1) in {(1,1),(1,2),(2,1),(2,2)}.             (16)
```

Lemmas 1 and 1.1 exclude the first three profiles.  `GLS37` Theorem 1
excludes `(2,2)`.  This exhausts (16). `square`

### Corollary 2.1 (GLS35 non-silent full swallow starts at rank four)

On the complete-target zero-anchor non-silent branch of `GLS35`,

```text
p=epsilon_A(q)!=0.                                   (17)
```

Thus `q!=0`.  If the raw escape alternative fails, `GLS35` gives full
swallow, and Theorem 2 yields

```text
rank B_Q^anc>=4.                                     (18)
```

This is pointwise at every residual contraction and includes all shore,
incidence, nuisance, response, and divisor rank drops inside the declared
non-silent gate.  It does not assert that the rank-at-least-four branch is
empty.

## 4. Frontier and unresolved remainder

```text
rank-3 full swallow with nonzero q:                         EXCLUDED;
rank-3 full swallow on the GLS35 non-silent branch:         EXCLUDED;
rank-3 full swallow with q=0:                               OPEN;
full swallow with rank B_Q^anc in {4,...,9}:                OPEN,
  including p=0 and diagonal-silent fibres;
raw escape supplies an original legal target package:       FALSE;
nonzero-anchor marginal/double-transverse branches:          OPEN;
arbitrary-root source cover and strategic-node closure:      UNKNOWN;
global Krenn--Gu conjecture:                                 UNRESOLVED.
```

The smallest continuation of this exact zero-anchor non-silent branch is now
to exclude or legally attach full-swallow fibres with
`rank B_Q^anc>=4`, using the complete pure-port and mixed equations on the
same graph.  The `GLS36` common-row no-go and `GLS37` mixed-only control still
apply: rank data alone do not provide an original GLS22/23 or GLD target,
and a mixed-only fixed contraction is insufficient.  Any downstream entry
must separately prove selector survival, response/activity,
synchronization, complete labelled nuisance survival, the declared anchor,
and arbitrary-root source coverage.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_nonzero_root_deck_minimal_raw_swallow_exclusion.py
```

The primary uses SymPy nullspaces on bounded exact rational representatives:
`648` left-shore and `648` right-shore charts, sampling each of the rank
profiles `(1,1)`, `(1,2)`, and `(2,1)`.  These finite coefficient grids are
not an exhaustive parameter-space cover.  The audit imports no project module
and no third-party package; instead of regenerating the coefficient charts,
it exhausts the independent colour-support and missing-row contradiction
census, its transpose, the incidence-column support collapse, and the four
positive discrete shore-rank profiles.  Both implementations verify that a low-shore
`X` or `Y` slice is forced onto the root-companion coordinate axis, every
diagonal incidence column then lies in one line, and that line cannot span
`Delta`.  The arbitrary-parameter and arbitrary-root statement is the
symbolic proof above; the `(2,2)` dependency is the already independently
audited `GLS37` theorem.
