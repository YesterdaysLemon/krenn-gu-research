# Fixed-Q joint M/Z module quotient, paired attachment, and rank-one fibre boundary

## Status

**Exact characteristic-zero joint module-selector theorem and conditional
paired-response detector.**  At surplus two, the residual-absent tensor

```text
M_S=H_S
```

and the residual-present tensor

```text
Z_S=H_(Q union S)(z_Q)
```

are two distinct labelled summands of the same full fixed-`Q` companion
equation.  Removing exactly those two summands and quotienting by coefficient
slices of every other label gives a finite noncircular criterion for all
constant-open-port combinations `aM_S+bZ_S`.

Two independent desired classes give separate exact `M_S` and `Z_S`
selectors.  On a hypothetical witness, pure quotient rank two forces this
paired attachment and tensor independence of the realized responses.  Pure
rank one is genuinely ambiguous: it may coexist either with paired selectors
and dependent responses, or with only one attachable combination and
independent responses.  Pure rank zero may coexist with operator attachment
when both outputs vanish, or with a nonzero `M`-active combination whose
realized value cancels as `M+aZ=0`.

On the six-root/six-port branch, joint rank two for the fifteen pair and
fifteen four-port targets legally attaches all corresponding `M_2,Z_2,M_4,Z_4`
tensors.  The attached residual-absent tensors are target-diagonal, so the
paired-response theorem `GLD14` gives an exact one-row mixed `M_4` detector
whenever two disjoint direct edges of different colours are active.  If no
detector fires, the differently coloured direct-edge supports are pairwise
cross-intersecting.

None of these rank-two conditions is proved universal on the witness locus.
The theorem does not turn a rank-one mixed combination into separate tensors,
does not integrate a formal deck fibre into a graph fibre, and has no
permanent implication.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

The owning one-target quotient is
[`GLD7`](FIXED_Q_FULL_MODULE_TARGET_QUOTIENT_RANK_ONE_PURE_SURVIVAL_AND_SIX_PORT_ATTACHMENT_TRICHOTOMY_THEOREM.md),
and the paired response boundary is
[`GLD14`](PAIRED_M2_AFFINE_INCIDENCE_ONE_COLOUR_KERNEL_AND_ALL_DEPTH_MIXED_SHAPE_THEOREM.md).

## 1. The two labelled response projections

Work over a characteristic-zero field `K`.  Fix one graph, one residual pair,
and one residual contraction:

```text
R={1,2,3,4},       B=Q disjoint-union U,
|Q|=2,             |U|=4.                              (1)
```

Every local space is ternary.  Retain the complete fixed-`Q` companion map

```text
Gamma_Q:E -> F,

E=direct-sum_(empty!=I subset B, |I| even)
     tensor_(i in I)V_i^*,
F=(tensor_(r in R)V_r^*) tensor (tensor_(u in U)V_u^*).
                                                               (2)
```

Thus `dim E=2079` and `dim F=6561`.  The residual contraction is inserted
only after every labelled summand in `E` has been retained.

Fix a nonempty even

```text
S subset U,          S in binom(U,2) union {U},
C=U-S.                                                   (3)
```

Put

```text
L_S^*=(tensor_(r in R)V_r^*) tensor (tensor_(u in C)V_u^*),
W_S=tensor_(u in S)V_u^*,              F=L_S^* tensor W_S.
                                                               (4)
```

The universal companion expansion has coefficient `G_(B-I)` on the deck
label `H_I`.  Therefore define

```text
P_S^M:E -> W_S,       supported on I=S,
P_S^Z:E -> W_S,       supported on I=Q union S,

g_S^M=G_(Q union C)(z_Q) in L_S^*,
g_S^Z=G_C in L_S^*.                                  (5)
```

On the `I=S` summand, `P_S^M` is the identity.  On `I=Q union S`, `P_S^Z`
evaluates the `Q` slots at the same fixed `z_Q`.  These are distinct direct
summands, and

```text
P_S^M(H)=M_S,             P_S^Z(H)=Z_S.               (6)
```

For a pair `S={u,v}`, `M_S=B_uv` and `Z_S=z_uv`.  For `S=U`, they are the
residual-absent four-port matching tensor and the residual-present tensor
`T`, respectively.

## 2. The complete joint nuisance quotient

Remove both desired blocks:

```text
Theta_S^(MZ)=Gamma_Q
 -g_S^M tensor P_S^M-g_S^Z tensor P_S^Z.              (7)
```

Define the complete joint nuisance space

```text
N_S^(MZ)=span{
 (id_(L_S^*) tensor eta)Theta_S^(MZ)(x):
 x in E, eta in W_S^*
} subset L_S^*.                                       (8)
```

Every coefficient of every label other than `I=S` and `I=Q union S` occurs
in (8).  No fixed-`z_Q` graph slice or selected nuisance ledger replaces this
full definition.

Write

```text
pi_S:L_S^* -> overline L_S=L_S^*/N_S^(MZ),
bar g_M=pi_S(g_S^M),             bar g_Z=pi_S(g_S^Z),
k_S=dim span{bar g_M,bar g_Z}.                         (9)
```

For `lambda in L_S=(L_S^*)^*`, define its desired coefficient row

```text
c_S(lambda)=(lambda(g_S^M),lambda(g_S^Z)) in K^2.     (10)
```

### Theorem 1 (joint constant-module selector criterion)

Let

```text
C_S={c_S(lambda):lambda in (N_S^(MZ))^perp} subset K^2.
                                                               (11)
```

Then:

1. `dim C_S=k_S`;
2. for `(a,b) in K^2`, the exact operator identity

   ```text
   (lambda tensor id_(W_S))Gamma_Q
     =aP_S^M+bP_S^Z                                  (12)
   ```

   holds for some constant `lambda` exactly when `(a,b) in C_S`;
3. separate normalized selectors for `P_S^M` and `P_S^Z` exist exactly when

   ```text
   k_S=2,
   ```

   equivalently

   ```text
   rank[N_S^(MZ)|g_S^M|g_S^Z]=rank N_S^(MZ)+2;        (13)
   ```

4. if `k_S=1` and `bar g_M=a bar g`, `bar g_Z=b bar g` with `bar g!=0`,
   exactly the line `K(aP_S^M+bP_S^Z)` is attachable;
5. if `k_S=0`, no nonzero combination of the two desired projections is
   attachable.

The selectors may depend on the fixed graph, `Gamma_Q`, `Q`, and `z_Q`.
They are constant in the open `S` variables, satisfy the cross-normalizations
on both desired labels, and are chosen before inspecting the realized tensors
`M_S,Z_S`.

### Proof

For `lambda in (N_S^(MZ))^perp`, every coefficient slice of
`(lambda tensor id)Theta_S^(MZ)` vanishes, so (7) gives

```text
(lambda tensor id)Gamma_Q
 =lambda(g_S^M)P_S^M+lambda(g_S^Z)P_S^Z.              (14)
```

Conversely, the independence of the two labelled deck summands makes the
coefficients in (14) exact, and forces `lambda` to annihilate every slice in
(8).  The evaluation map from `(overline L_S)^*` to `K^2` is the transpose of

```text
K^2 -> overline L_S,       (u,v) |-> u bar g_M+v bar g_Z.
                                                               (15)
```

Its image is `C_S` and its rank is `k_S`.  If the two quotient classes are
independent, choose their dual basis to obtain coefficient rows `(1,0)` and
`(0,1)`.  If their span has dimension one or zero, (15) gives exactly the
remaining assertions.  `square`

### Comparison with the individual one-target quotients

If `M` is targeted alone, the `Z` block is nuisance; if `Z` is targeted alone,
the `M` block is nuisance.  The joint remainder is zero on both desired
labelled summands, while `P_S^M` and `P_S^Z` have disjoint direct-summand
support and are each surjective onto `W_S`.  Restricting the nuisance input
to `I=Q union S` therefore isolates every scalar multiple of `g_S^Z`, and
restricting it to `I=S` isolates every scalar multiple of `g_S^M`; every
other label contributes exactly the joint nuisance.  Hence the one-target
nuisance spaces are exactly

```text
N_S^M=N_S^(MZ)+K g_S^Z,
N_S^Z=N_S^(MZ)+K g_S^M.                               (16)
```

Consequently an individual `M` selector exists exactly when
`bar g_M notin K bar g_Z`, and an individual `Z` selector exists exactly when
`bar g_Z notin K bar g_M`.  In a rank-one joint quotient, an axis line gives
one individual selector, while an oblique line gives only a mixed combination
and neither individual tensor.  Thus the joint quotient cannot be replaced by
either one-target nuisance quotient.

### Exact finite sizes

For a pair `S`,

```text
dim L_S=729,       dim W_S=9,
raw slice count <=2079*9=18711,
effective fixed-z_Q slice count <=511*9=4599.          (17)
```

For `S=U`,

```text
dim L_U=81,        dim W_U=81,
raw slice count <=2079*81=168399,
effective fixed-z_Q slice count <=511*81=41391.        (18)
```

Two separate selectors for all seven targets use

```text
2(6*729+81)=8910                                  (19)
```

scalar functional coordinates.  These are exact finite matrix sizes, not
rank claims.

## 3. The full witness equation and the three ranks

Let `H in E` be the complete deck array of one hypothetical witness:

```text
Gamma_Q(H)=J_Q.                                        (20)
```

For active residual colours `c in C_Q`, put

```text
d_(S,c)=
 (tensor_(r in R)e_(r,c)^*) tensor
 (tensor_(u in C)e_(u,c)^*) in L_S^*,
w_(S,c)=tensor_(u in S)e_(u,c)^* in W_S,
alpha_c=product_(q in Q)e_(q,c)^*(z_q)!=0.             (21)
```

The `w_(S,c)` are independent and

```text
J_Q=sum_(c in C_Q) alpha_c d_(S,c) tensor w_(S,c).
                                                               (22)
```

Quotienting (7) gives the operator identity

```text
(pi_S tensor id)Gamma_Q
 =bar g_M tensor P_S^M+bar g_Z tensor P_S^Z,           (23)
```

and applying it to (20) gives

```text
sum_(c in C_Q) alpha_c[d_(S,c)] tensor w_(S,c)
 =bar g_M tensor M_S+bar g_Z tensor Z_S.               (24)
```

Define the three distinct ranks

```text
q_S=dim span{[d_(S,c)]:c in C_Q},
k_S=dim span{bar g_M,bar g_Z},
r_S=dim span{M_S,Z_S}.                                 (25)
```

Here `q_S` is the pure target quotient rank, `k_S` is the module-selector
rank, and `r_S` is the whole-tensor response rank.

### Theorem 2 (paired target-rank trichotomy)

Every hypothetical-witness chart satisfies

```text
q_S<=min(k_S,r_S)<=2,                                  (26)
```

and more precisely:

1. `q_S=2` if and only if `k_S=r_S=2`.  In particular, pure rank two forces
   separate legal `M_S,Z_S` attachment and response independence;
2. if `k_S=2`, then `q_S=r_S`.  Thus the two operator selectors still exist
   when `q_S=1` and the responses are dependent, or when `q_S=0` and both
   responses vanish;
3. if `r_S=2`, then `q_S=k_S`.  Under tensor-independent responses, pure
   rank two is equivalent to paired attachment;
4. if `k_S=1`, write `bar g_M=a bar g`, `bar g_Z=b bar g`.  Then

   ```text
   q_S=1 iff aM_S+bZ_S!=0,
   q_S=0 iff aM_S+bZ_S=0;                              (27)
   ```

   only this one combination is attached;
5. if `k_S=0`, then `q_S=0` for arbitrary response rank `r_S`;
6. `q_S>=3` is an exact target-incidence obstruction.

Therefore pure rank one and pure rank zero do not decide paired attachment.
In particular, response nonvanishing is not response independence, and zero
response does not refute an operator selector.

### Proof

Represent the right side of (24) as the product of a two-column desired-class
map and a two-row response map.  Its rank is at most both `k_S` and `r_S`.
The left side has rank exactly `q_S`, because the active `w_(S,c)` are
independent and every `alpha_c` is nonzero.  If the desired-class map and the
two-row response map both have rank two, their product has rank two.
Conversely a rank-two product forces both factors to have rank two.  If the
desired-class map has rank two, it is
injective and preserves the response-map rank; if the response map has rank
two, it is surjective onto the two coefficient coordinates and preserves the
desired-class rank.  This proves assertions 1--3.

For `k_S=1`, substitute the displayed expressions for `bar g_M,bar g_Z` in
(24).  Its right side is the simple tensor

```text
bar g tensor (aM_S+bZ_S),                              (28)
```

which has rank one exactly when its second factor is nonzero.  The zero-rank
and `k_S=0` claims follow, and (26) excludes rank at least three.  `square`

### Corollary 2.1 (separate target-diagonal tensors)

If `k_S=2`, choose the normalized selectors from Theorem 1 and apply them to
the pure target (22).  Then

```text
M_S=sum_c alpha_c lambda_M(d_(S,c))w_(S,c),
Z_S=sum_c alpha_c lambda_Z(d_(S,c))w_(S,c).            (29)
```

Both tensors are separately target-diagonal, even in the response-dependent
`q_S=1` and zero-response `q_S=0` branches.  If `k_S=1`, only the attached
combination in (27) has such a target formula; it must not be promoted to
separate `M` and `Z` attachment.

## 4. Rank-one M-active combinations on a fixed Z fibre

The rank-one branch can still carry exact direct-layer information.

### Corollary 2.2 (M-active joint row criterion)

The following are equivalent:

1. `bar g_M!=0` in the joint quotient;
2. `C_S` contains a coefficient row `(1,a)` for some `a in K`;
3. there is an exact constant selector for

   ```text
   P_S^M+aP_S^Z.                                      (30)
   ```

For a fixed `Gamma_Q` and any affine family of formal deck arrays on which
`P_S^Z` is constant, (30) varies exactly with `P_S^M`.  Thus it cuts a fixed
`Z_S` fibre by the same linear equations as the direct tensor, even though it
need not attach `M_S` separately.

If (30) holds for every pair in one six-port union, equality of all fifteen
selected combined tensors and of the complete `Z` data forces equality of
the entire direct pair array `B=M_2`.  This is a fixed-module deck-fibre
statement.  It is not a physical graph fibre unless the affine family is
separately integrated while keeping the same `Gamma_Q`.

### Proof

If `bar g_M!=0`, choose a dual functional nonzero on it and normalize its
first desired coefficient to one; Theorem 1 gives (30).  The reverse
implication is immediate from (14).  On a fixed `Z_S` fibre, the difference
of two outputs of (30) is the difference of their `M_S` tensors.  For pair
sets, those tensors are precisely the complete direct blocks.  `square`

### Corollary 2.3 (exact pair-block cover of a full-Z fibre)

Fix one finite port union `V` with `n=|V|`, one physical `q=2`, `h=0` pair
channel `K`, and
the full tensor Wick kernel

```text
L=ker(mu_K:A_2 -> A_4).
```

For a pair set `D`, let `rho_D` restrict a direct-layer perturbation to its
complete ternary pair block, and for a family `C` put

```text
rho_C=direct-sum_(D in C)rho_D,
kappa(L)=min{|C|:rho_C|_L is injective}.              (31)
```

If `d=dim L` and every local space is ternary, then

```text
ceil(d/9) <= kappa(L) <= min(d,binom(n,2)).            (32)
```

On one fixed compatible full-`Z` fibre, available `M`-active joint rows on
a pair family `A` leave exactly the ambiguity

```text
L intersect intersection_(D in A)ker rho_D.           (33)
```

In particular, if `q_D=2` for every `D` in a pair-block cover `C`, the
separate attached `M_D,Z_D` tensors eliminate the full-`Z` affine fibre.
The same conclusion follows from `M+a_DZ` rows on `C` only after the full
`Z` fibre has independently been fixed.  Such mixed rows alone neither
reconstruct `M` nor transfer target diagonality.  Once the cover identifies
`B`, the Wick formulas reconstruct every `M` and `Z` depth on every principal
subwindow of this named union; this is still downstream of legal attachment.

The bounds in (32) are sharp enough to expose two exact physical controls.
For the ternary one-pure-colour complete-bipartite `K_(3,3)` channel of
`GLD14`, `dim L=16` and

```text
kappa(L)=4,
C={12,13,45,46}                                      (34)
```

after numbering the two shores `{1,2,3}` and `{4,5,6}`.  The kernel splits
as two eight-dimensional shore spaces.  One internal-edge block has rank
five on its shore, while two internal-edge blocks inject that shore; hence
two blocks per shore are necessary and sufficient.

For the full ternary one-pure-colour seven-port `K_(5,2)` channel,

```text
dim L=24,            kappa(L)=6.                      (35)
```

Here the two-vertex shore is called the centre shore.  The kernel is the
direct sum of five three-dimensional leaf bundles, each supported on the
two edges from one leaf to the centres, and the complete nine-dimensional
centre-centre pair block.  Injectivity therefore requires the centre-centre
block and at least one leaf-centre block for each leaf, and those six blocks
are sufficient.  This is a full tensor statement, not merely the scalar
`K_(5,2)` nullity ledger.

### Proof

The complete collection of pair restrictions is the identity on `A_2`, so
some pair family injects `L`.  Each ternary pair block has dimension nine,
giving the lower bound.  Greedily add a pair block that increases the rank
of the current restriction; at most `d` additions are needed, giving the
upper bound.  Formula (33) is exactly the kernel of the collected fixed
linear observations on the GLD12 fibre `B_0+L`.  The two displayed controls
follow from the one-pure-colour decomposition of `GLD14`.  For `K_(5,2)`,
write `Q_G=L_A L_C` with `|A|=5` and `|C|=2`.  The scalar `N=empty` block has
nullity six.  On `A_2(A)`, multiplication `A_2(5)->A_3(5)` becomes the
`KG(5,2)` disjointness matrix after complementing, with nonzero eigenvalues
`3,-2,1`; the block is injective.  The
`A_1(A) tensor A_1(C)` block has the five-dimensional centre-difference
kernel, and `A_2(C)` is killed.  If one deletes a leaf, the only degree-one
kernel is the span of `x_(c1)-x_(c2)`; if one deletes a centre, it is the span
of the remaining centre coordinate.  Hence `h_p=1` for all seven vertices.
The unique two-vertex cover is the centre pair.  Thus the GLD14 ledger

```text
s=6,       h_p=1 for all seven p,       c_2=1
```

gives `6+2*7+4=24`.  Regrouping its basis gives the five three-dimensional
leaf bundles and the nine-dimensional centre block above.  Their disjoint
supports force the lower bound, and the listed six restrictions separate
them.  The analogous two-shore decomposition proves (34).  `square`

## 5. Six-port paired attachment and bounded mixed detectors

Take now six roots and six ports at surplus two:

```text
|R|=6,       |Q|=2,       |U|=6.                      (36)
```

The same proof applies for every `S subset U` of size `2`, `4`, or `6`.
Both labels `I=S` and `I=Q union S` are nonempty even deck summands.  The
complete effective deck dimension after fixed-`Q` evaluation is `8191`; the
spaces `L_S` have dimensions `59049`, `6561`, and `729`, respectively.

### Corollary 2.4 (conditional thirty-one-target paired supply)

If `q_S=2` for all fifteen pair sets, all fifteen four-port sets, and the
six-port set at one fixed graph, `Q`, and contraction, then Theorem 2 supplies
separate legal selectors for all thirty-one `M_S` tensors and all thirty-one
`Z_S` tensors.  The functionals may vary with `S`; the graph, `Q`, contraction,
and normalization may not.

For the paired-response detector only the thirty pair/four sets are needed.
On a hypothetical witness, if `k_S=2` for those thirty sets, (29) makes every
direct pair tensor `B_e` and every residual-absent four-port tensor `M_F`
target-diagonal.  Hence for every pair of disjoint edges `e,f` and different
colours `c!=d`,

```text
B_e(c,c)B_f(d,d)=0.                                  (37)
```

If the product in (37) is nonzero, its four-set `F=e union f` has the single
coefficient-pure mixed tensor entry

```text
M_F(c,c,d,d)=B_e(c,c)B_f(d,d)!=0,                    (38)
```

contradicting the legally attached pure GHZ target.  Thus (38) is a bounded
one-row mixed detector.  If no detector fires, the active edge families of
different colours are pairwise cross-intersecting, exactly as in `GLD14`.

This does not force any `q_S=2` or `k_S=2`, any disjoint colour activity, or
any permanent restriction.

### Corollary 2.5 (three-target localized coefficient-pure detector)

Let `F={1,2,3,4}` and suppose

```text
B_12(c,c)B_34(d,d)!=0,             c!=d.             (39)
```

It is enough to have `q_F=2`, together with `q_D=2` for one pair

```text
D in {13,24}
```

and `q_E=2` for one pair

```text
E in {14,23}.                                           (40)
```

Indeed, the pair selectors make one factor in each nuisance product zero,
while the four-port selector makes the mixed target row zero:

```text
0=M_F(c,c,d,d)
 =B_12(c,c)B_34(d,d)
  +B_13(c,d)B_24(c,d)
  +B_14(c,d)B_23(c,d).                                (41)
```

This contradicts (39).  Thus three joint rank-two targets suffice for this
localized detector.  If the two active factors in (39) must themselves be
legally read rather than supplied as an external activity hypothesis, add
the pair targets `12` and `34`, for five targets total.

Two cross-pair targets are minimal only for this robust coefficientwise
nuisance-killing scheme.  With just the selected pair `13`, take

```text
B_12(0,0)=B_34(1,1)=B_13(0,0)=B_24(0,0)=1,
B_14(0,1)=1,                 B_23(0,1)=-1,             (42)
```

and all other coefficients zero.  Then `M_13` is nonzero diagonal and
`M_F` is the nonzero pure `0000` row, but the remaining `14|23` term cancels
the desired mixed `12|34` product.  Independent diagonal abstract `Z_13`
and `Z_F` tensors can make both response pairs independent.  This is a
response-algebra sharpness control, not an integrated hypothetical-witness
or graph control, and it proves no minimality against arbitrary linear
combinations or additional equations.

### Corollary 2.6 (maximal-rank common-contraction synchronization)

Let the fully supported residual contraction vary on one irreducible torus,
with one fixed graph and `Q`.  For any finite target family, suppose each
target has a contraction at which its complete joint nuisance matrix has
maximal rank and adjoining `g_S^M,g_S^Z` raises that rank by two.  Nonzero
nuisance and augmented minors define nonempty principal opens.  Their finite
intersection supplies one common contraction with `k_S=2` for every target.

If each starting point is a hypothetical-witness point with `q_S=2`, include
one nonzero `2 x 2` response minor for each target in the principal-open
product.  The common contraction then retains `q_S=2` and the separate paired
attachments.  The maximal-rank and response-minor hypotheses are inputs, not
conclusions.

### Arbitrary-root breadth ledger

For `n` roots, `n` open ports, and one residual pair, the complete nonempty
even surplus-two deck has dimension

```text
dim E_n=(4^(n+2)+(-2)^(n+2))/2-1,                    (43)
```

and the joint quotient for an even target `S` has

```text
dim L_S=3^(2n-|S|).                                  (44)
```

Thus the seven-root/seven-port extension has

```text
dim E_7=130815,
dim L_S=531441,59049,6561       for |S|=2,4,6.        (45)
```

These are exact module sizes, not rank or attachment claims.  In particular,
the six-root theorem does not itself attach the thirty-five four-port rows
required on a seven-port union.

## 6. Sharpness controls and exact remainder

The rank-one ambiguity is not cosmetic.  The following exact finite module
controls realize every branch; they are not asserted to be graphs or
witnesses.

```text
k=2, r=2, q=2:  bar g_M=e1, bar g_Z=e2, M=f1, Z=f2;
k=2, r=1, q=1:  bar g_M=e1, bar g_Z=e2, M=Z=f1;
k=2, r=0, q=0:  bar g_M=e1, bar g_Z=e2, M=Z=0;
k=1, r=2, q=1:  bar g_M=bar g_Z=g, M=f1, Z=f2;
k=1, r=1, q=0:  bar g_M=bar g_Z=g, M=f, Z=-f;
k=0, r=2, q=0:  bar g_M=bar g_Z=0, M=f1, Z=f2.       (46)
```

A rank-three pure tensor is an exact target-incidence control.  The
zero-root-edge maximum-root/triple-blocker physical control of `GLD11` has
the sharper exact ranks

```text
k_S=1 for all six pairs,             k_U=0.           (47)
```

Indeed, every `g_S^Z=G_(U-S)` vanishes because a residual-present pair needs
one root-root edge, while both `g_U^M=G_Q` and `g_U^Z=G_empty` need root-root
edges and vanish.  For five pairs, the following single `L_S` coordinates
occur in `g_S^M` with coefficient one and in no joint nuisance slice (root
word first, then complement-port word):

```text
S=01: 2021;22,   S=02: 0112;21,   S=03: 0001;00,
S=13: 1001;10,   S=23: 1212;12.                       (48)
```

For `S=12`, the separator is

```text
delta_(0020;02)-delta_(0110;01)+delta_(1210;10).      (49)
```

On the desired `G_(Q union (U-S))` column its coordinate triple is
`(1,1,1)`.  Among the other fourteen four-element companion sets, only two
meet these coordinates, with triples `(0,1,1)` and `(1,1,0)`, both killed by
`(1,-1,1)`.  Thus all six `M` classes survive while every `Z` class vanishes.
All physical `M,Z` response values in this control are nonzero.  Consequently
the graph-side maximum-root, blocker, concision, pure-normalization,
Hamming-one, and nonzero-response data do not force paired attachment.  Its
displayed mixed coefficient excludes it from the witness locus.

```text
joint desired coefficient space C_S:                       PROVED;
k_S=2 iff separate constant M/Z selectors:                 PROVED;
one-target nuisance comparison (16):                       PROVED;
witness pure quotient rank q_S<=2:                         PROVED;
q_S=2 forces paired attachment and response independence: PROVED;
rank-one M-active fixed-module Z-fibre criterion:           PROVED;
exact pair-block cover criterion and kappa bounds:          PROVED;
ternary K_(3,3) kappa=4 and K_(5,2) kappa=6:               PROVED;
conditional six-port M4 coefficient-pure detector:         PROVED;
localized three-target coefficientwise detector:           PROVED;
GLD11 physical graph-side ranks six k=1 and one k=0:       PROVED;
maximum-root/triple-blocker data force paired attachment:   FALSE;
any/all q_S=2 or k_S=2 forced on every witness:             UNKNOWN;
rank-one residual excluded on the witness locus:            UNKNOWN;
physical integration of the formal fixed-module fibre:      UNKNOWN;
legal joint rows on a pair-block cover forced:               UNKNOWN;
GLD3 disjoint three-colour activity:                         UNKNOWN;
weighted permanent implication:                             UNKNOWN;
global Krenn--Gu conjecture:                                 UNRESOLVED.
```

The breadth is one fixed-`Q` chart, simultaneously applicable to the six
pairs and four-port set, and conditionally to all thirty-one even targets on
one six-port union.  The depth is the complete nonempty even surplus-two deck.
The reconstructed objects on `k_S=2` are both physical response tensors for
the named `S`.  On rank one, the ambiguity object is the missing coefficient
line in `K^2/C_S`; it is not a graph fibre.  There is no transition gauge.  The
target implication is exact paired attachment or the displayed mixed `M_4`
coefficient under the stated family hypotheses.  The permanent implication
is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_fixed_q_joint_mz_module_quotient_paired_attachment.py
python -I claims/arbitrary-order/audit_fixed_q_joint_mz_module_quotient_paired_attachment.py
```

The primary verifier uses exact rational matrices to replay the six canonical
rank controls, the accessible coefficient spaces, dual selectors, tensor-rank
branches, the rank-three obstruction, the dimension ledgers, the complete
six-pair GLD11 joint-nuisance separator ledger, the sixteen- and
twenty-four-dimensional `K_(3,3)`/`K_(5,2)` block covers, and the localized
detector control.  The independent audit uses standard-library `Fraction`, a
recursive companion generator, sparse tensor multiplication, wedge tests, and
a separately implemented elimination route.  It independently replays the
GLD11 slice counts `202,202,199,174,193,193` and both block covers.  These
bounded checks audit the finite controls.  The full all-nuisance quotient,
tensor-rank, Kneser/deleted-vertex decomposition, fixed-fibre, and six-port
detector proofs are load-bearing.
