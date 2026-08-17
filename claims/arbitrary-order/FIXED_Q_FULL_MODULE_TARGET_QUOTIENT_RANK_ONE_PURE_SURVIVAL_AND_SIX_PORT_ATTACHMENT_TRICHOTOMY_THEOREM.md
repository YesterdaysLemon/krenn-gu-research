# Fixed-Q full-module target quotient rank one, pure survival, and six-port attachment trichotomy

## Status

**Exact characteristic-zero witness-target incidence theorem.**  Fix the
four-root, residual-pair, four-port module of the
[`constant target-module selector theorem`](FOUR_ROOT_CONSTANT_TARGET_MODULE_SELECTOR_QUOTIENT_AND_MAXIMUM_ROOT_SHARPNESS_THEOREM.md),
including all `2079` nonempty even deck coordinates.  For any pair of open
ports `S`, or for all four ports, quotient the fixed-`Q` witness equation by
the complete nuisance coefficient-slice space `N_S`.

The quotient of the pure GHZ target has tensor rank at most one.  More
precisely, if `d_(S,c)` is the pure colour-`c` root/complement-port word and
`C_Q` is the active contracted-colour set, then

```text
dim span{[d_(S,c)]:c in C_Q} <= 1.                   (1)
```

This has two exact consequences.

1. If two pure classes are independent modulo `N_S`, the chart cannot satisfy
   the full fixed-`Q` hypothetical-witness equation.
2. If any pure class survives, the desired class `[g_S]` survives, so the
   legal constant open-port selector exists.  If the physical tensor selected
   by `P_S` is nonzero, this condition is also necessary: attachment holds
   exactly when at least one pure target class survives nuisance.

Thus the bad quotient locus from the preceding theorem is sharpened on the
actual target equation.  It is contained in the locus where every active
pure GHZ word is swallowed by nuisance, and on `P_S(H)!=0` it equals that
locus.

The same proof applies to six roots, a residual pair, and six ports.  It
gives an exact trichotomy for each of the fifteen pair rows, fifteen
four-port rows, and the six-port row used by `GLD6`: pure quotient rank at
least two excludes target incidence; rank one legally attaches that row; and
rank zero is the swallowed-pure branch.  This is a conditional attachment
criterion, not a proof that all thirty-one ranks equal one.

The theorem does not prove that a pure class survives for every hypothetical
witness and does not produce a coefficient-pure mixed syzygy or a weighted
permanent restriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

## 1. Fixed module and witness equation

Work over a characteristic-zero field `K`.  Let

```text
R={1,2,3,4},       Q={q0,q1},       U={u1,u2,u3,u4}. (2)
```

Every local space has dimension three.  Fix nonzero residual vectors `z_q`
at the two residual modes, leave the roots and ports open, and retain the
full fixed-`Q` companion map

```text
Gamma_Q:E -> F,
E=direct-sum_(empty!=I subset Q union U, |I| even)
     tensor_(i in I)V_i^*,
F=(tensor_(r in R)V_r^*) tensor (tensor_(u in U)V_u^*).
                                                               (3)
```

Here `dim E=2079` and `dim F=6561`.  Let `H in E` denote the complete named
deck array of one fixed graph after the residual contraction.  A hypothetical
witness satisfies

```text
Gamma_Q(H)=J_Q,                                      (4)
```

where `J_Q` is the correspondingly contracted pure GHZ target.

Fix

```text
S in binom(U,2) union {U},
L_S^*=(tensor_(r in R)V_r^*) tensor
      (tensor_(u in U-S)V_u^*),
W_S=tensor_(u in S)V_u^*.                            (5)
```

Thus `F=L_S^* tensor W_S`.  In the notation of the preceding theorem,

```text
Gamma_Q=g_S tensor P_S+Theta_S,                      (6)
N_S=span{(id tensor eta)Theta_S(x):x in E, eta in W_S^*}
       subset L_S^*.                                 (7)
```

The desired constant module selector exists exactly when

```text
[g_S]!=0 in L_S^*/N_S.                               (8)
```

No target value is used in this criterion.

Choose the pure GHZ dual bases `e_(v,c)^*`, `c=0,1,2`.  Put

```text
d_(S,c)=
  (tensor_(r in R)e_(r,c)^*) tensor
  (tensor_(u in U-S)e_(u,c)^*) in L_S^*,             (9)
w_(S,c)=tensor_(u in S)e_(u,c)^* in W_S.            (10)
```

The residual contraction contributes

```text
alpha_c=e_(q0,c)^*(z_q0)e_(q1,c)^*(z_q1).            (11)
```

Let

```text
C_Q={c in {0,1,2}:alpha_c!=0}.                       (11a)
```

For fully supported residual contractions, `C_Q={0,1,2}`.  Keeping the
active-colour set makes the statement exact even when a contracted residual
coordinate vanishes.  Therefore

```text
J_Q=sum_(c in C_Q) alpha_c d_(S,c) tensor w_(S,c).   (12)
```

The active tensors `w_(S,c)` are linearly independent.

## 2. Exact quotient identity

Let

```text
pi_S:L_S^* -> overline L_S=L_S^*/N_S                (13)
```

be the quotient map.

### Theorem 1 (rank-one target quotient)

As an identity on the complete labelled deck module,

```text
(pi_S tensor id_(W_S))Gamma_Q=[g_S] tensor P_S.      (13a)
```

Every fixed-`Q` hypothetical-witness equation (4) consequently satisfies

```text
sum_(c in C_Q) alpha_c [d_(S,c)] tensor w_(S,c)
   =[g_S] tensor P_S(H)                              (14)
```

in `overline L_S tensor W_S`.  Consequently

```text
rank overline(J_Q)
 =dim span{[d_(S,c)]:c in C_Q}
 <=1.                                                (15)
```

### Proof

Every coefficient slice of `Theta_S(x)` belongs to `N_S` by (7), for every
`x in E`.  Thus `Theta_S(E) subset N_S tensor W_S`, and quotienting (6)
proves the operator identity (13a).  Apply it to `H` and insert (12) to obtain
(14).  Its right side is one decomposable tensor and therefore has tensor
rank at most one.

In the independent active basis `w_(S,c)`, the column space of the left side
is the span of the vectors `alpha_c[d_(S,c)]`, `c in C_Q`.  These `alpha_c`
are nonzero, so its rank is exactly the dimension in (15).
`square`

### Corollary 1.1 (pure quotient obstruction)

If

```text
dim span{[d_(S,c)]:c in C_Q} >=2,                    (16)
```

then the named graph data cannot satisfy the full fixed-`Q` target equation.
Equivalently, any nonzero `2 x 2` quotient minor of the active pure classes is
an exact target-incidence obstruction.

This is not an ambient graph-space rank test.  It is obtained after imposing
the actual target equation, while retaining every nuisance label in `N_S`.

## 3. Pure survival forces legal attachment

### Theorem 2 (pure-survival attachment)

For a hypothetical-witness chart, if

```text
[d_(S,c)]!=0                                         (17)
```

for at least one active colour `c in C_Q`, then

```text
[g_S]!=0,                 P_S(H)!=0.                 (18)
```

Hence the exact constant selector `lambda_S` from the preceding theorem
exists.  It is constant in the open `S` coordinates, may depend on the fixed
graph and `Gamma_Q`, annihilates every nuisance coefficient slice, and
outputs the named physical tensor `P_S(H)` with exact normalization.

If `P_S(H)!=0`, then the converse also holds:

```text
[g_S]!=0
  iff some [d_(S,c)]!=0.                             (19)
```

In particular, on `P_S(H)!=0`, all active pure classes lie in `N_S` exactly
when the desired constant module selector fails.

### Proof

If one pure class survives, the left side of (14) is nonzero because the
`w_(S,c)` are independent and `alpha_c!=0`.  A decomposable tensor is nonzero
only when both factors are nonzero, proving (18).  Criterion (8) then gives
the selector before its realized diagonal value is inspected.

Now assume `P_S(H)!=0`.  If `[g_S]!=0`, the right side of (14) is nonzero,
so at least one pure class survives.  The reverse implication was just
proved.  If all pure classes vanish, (14) becomes
`[g_S] tensor P_S(H)=0`; the nonzero second factor forces `[g_S]=0`.
`square`

If `P_S(H)=0`, equation (14) forces all active pure classes to vanish, but it
places no restriction on `[g_S]`.  Thus the nonzero-response qualification
in (19) cannot be dropped.

### Corollary 2.1 (simultaneous seven-target supply)

Suppose that, for each of the six pairs `S subset U` and for `S=U`, at least
one of its active pure classes survives its own nuisance space `N_S`.  Then all
seven legal selectors exist on the same fixed graph, residual pair `Q`, and
contractions.  They supply exactly the six physical `D_uv` tensors and the
four-port `T` required by `GLD3`.

The selectors are allowed to be different functionals because their output
spaces differ.  Their physical graph, `Q`, contractions, and normalizations
are not allowed to vary.

## 4. What the rank-one line does and does not provide

When the span in (15) is one-dimensional and nonzero, the target quotient is
one pure line and attachment follows.  This is not a coefficient-pure left
syzygy.  A normalizing functional on `[g_S]` may have nonzero values on more
than one `d_(S,c)`, and (12) may therefore retain several diagonal colours.
Nothing in the rank-one identity isolates one mixed coefficient.

An exact two-dimensional control makes the distinction sharp.  Take

```text
L^*=K^2,       N=span{e_1-e_2},       g=e_1.         (19a)
```

Then `[e_1]=[e_2]!=0`, so the pure quotient has rank one and `[g]!=0`.
However,

```text
N^perp=span{(1,1)}.                                  (19b)
```

Every normalized selector is dense in the two displayed coordinates; neither
coordinate functional kills `N`.  Rank-one pure survival therefore supplies
attachment, not coefficient purity.  Likewise, rank at least two supplies a
`2 x 2` quotient-minor obstruction, not one displayed mixed coefficient.

The exact branch split for each `S` is

```text
pure quotient rank >=2
  -> target-incidence contradiction;

pure quotient rank =1
  -> legal constant target attachment;

pure quotient rank =0 and P_S(H)!=0
  -> [g_S]=0 and exact module-selector failure;

pure quotient rank =0 and P_S(H)=0
  -> [g_S] remains undecided by the target equation. (20)
```

The last two branches are the precise swallowed-pure residue.  An arbitrary
deck kernel is not introduced, and no physical graph fibre is claimed.

## 5. Conditional six-root, six-port attachment trichotomy

Take now

```text
|R|=6,              |Q|=2,              |U|=6,       (21)
```

and retain the analogous full companion module for every

```text
S subset U,                 |S| in {2,4,6}.           (22)
```

The proof of Theorems 1 and 2 uses only the decomposition
`Gamma_Q=g_S tensor P_S+Theta_S`, the complete nuisance-slice definition,
and the pure GHZ target.  It therefore applies verbatim.  For each of the
thirty-one sets in (22), let

```text
q_S=dim span{[d_(S,c)]:c in C_Q}.                     (23)
```

Then

```text
q_S>=2  -> exact target-incidence contradiction;
q_S=1   -> legal constant attachment of P_S(H);
q_S=0   -> [g_S] tensor P_S(H)=0.                     (24)
```

If `P_S(H)!=0`, the last alternative is exactly `[g_S]=0`.  Consequently,
if all fifteen pair classes, all fifteen four-port classes, and the six-port
class have rank one, the corresponding legal same-`Q` selectors attach all
`z_2`, `z_4`, and `z_6` rows assumed by `GLD6`.  This implication uses one
graph, one `Q`, one deck, and the full equations; it does not force any of the
thirty-one rank-one conditions.

The exact module sizes are

```text
dim E_full=sum_(k=2,4,6,8) binom(8,k)3^k=32895;
dim E_after fixed-Q evaluation=8191;

|S|        dim L_S        dim Hom(E_effective,W_S)
 2           59049                    73719
 4            6561                   663471
 6             729                  5971239.          (25)
```

These counts retain every effective nuisance label.  They show that (24) is
a finite exact module question; they do not decide it on the witness locus.

## 6. Frontier and UNKNOWN remainder

```text
quotient witness identity (14):                         PROVED;
pure quotient rank at most one:                         PROVED;
rank at least two excludes target incidence:            PROVED;
one surviving pure class forces attachment:             PROVED;
attachment iff pure survival when P_S(H)!=0:             PROVED;
same trichotomy for all 31 six-port rows:                 PROVED;
all seven pure-survival conditions on every witness:    UNKNOWN;
swallowed-pure branch excluded by full mixed equations: UNKNOWN;
coefficient-pure mixed left syzygy from rank one:        UNKNOWN;
all 31 six-port quotient ranks equal one:                UNKNOWN;
six-port z_2/z_4/z_6 constant attachment in witnesses:   UNKNOWN;
GLD3 three-colour activity:                              UNKNOWN;
weighted permanent attachment:                          UNKNOWN;
global Krenn--Gu conjecture:                             UNRESOLVED.
```

The breadth is one complete fixed-`Q` chart, with four-port and six-port
specializations.  The depth is the full surplus-two companion module, not a
selected deck slice.  The reconstructed data on the good branch are the
physical pair/four-port tensors in `GLD5`, or conditionally all thirty-one
rows in `GLD6`.  There is no overlap transition.  The ambiguity object is
the zero pure-target quotient, not a graph fibre.  The target implication is
exact attachment or exact target nonincidence; the permanent implication is
none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_full_module_target_quotient_rank_one_pure_survival_and_six_port_attachment_trichotomy.py
python -I claims/arbitrary-order/audit_fixed_q_full_module_target_quotient_rank_one_pure_survival_and_six_port_attachment_trichotomy.py
```

The primary verifier replays the quotient tensor-rank lemma in exact rational
arithmetic for canonical pure-class ranks zero through three, checks the
nonzero column scalings, and exercises every branch in (20).  The independent
no-import audit uses exterior `2 x 2` minors and direct decomposable-tensor
tests instead of importing the primary construction.  These scripts are
focused replays of the finite linear algebra; the proof is the quotient
argument above.
