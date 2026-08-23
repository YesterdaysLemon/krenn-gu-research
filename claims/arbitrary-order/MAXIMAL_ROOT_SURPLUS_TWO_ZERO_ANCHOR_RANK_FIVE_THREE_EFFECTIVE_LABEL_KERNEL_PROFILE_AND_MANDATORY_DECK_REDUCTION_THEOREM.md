# Maximum-root surplus-two zero-anchor rank-five three-effective-label kernel-profile and mandatory-deck reduction

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS50`, a pointwise characteristic-zero reduction of
the remaining exactly-three-effective-label part of the zero-anchor,
rank-five, fully swallowed fixed-residual target locus.  `GLS49` already
excludes the support consisting of both residual labels and one promoted
port.  The two other support types obey the following exact restrictions.

1.  With one residual label and two promoted ports, the evaluated
    complementary deck of the port pair is nonzero.  Each port joint kernel
    has dimension at most one, but they cannot both be nonzero.  The only
    surviving effective-dimension profiles are therefore
    `(1,2,3)` and `(1,3,3)`, up to exchanging the ports.
2.  With three promoted ports, the three evaluated complementary deck
    covectors are nonzero coordinate lines in a permutation of the three
    colours.  Every joint kernel has dimension at most one and at least one
    port joint map is injective.  The only surviving profiles are
    `(2,2,3)`, `(2,3,3)`, and `(3,3,3)`, up to permutation.

The proof contracts only inactive promoted ports, at the all-ones vector, as
a consequence of the complete uncontracted physical target equation.  It
retains zero, proportional, and cancelling deck slices and every
incidence-rank, divisor, and residual fibre.  The mandatory deck scalar is an
evaluated complementary physical deck.  It is **not** thereby a named
downstream response, selector, or attachment gate.

The coordinate deck lines are a contracted target consequence, not the
joint-line synchronization, normalized selector, or physical response
required by a named downstream theorem.  The theorem does not prove
existence or exclusion of any surviving profile.
It does not force a silent source point into full swallow, treat four or more
effective labels, treat ranks six through nine, or supply response,
selector, synchronization, nuisance-survival, anchor, or source-coverage
hypotheses for a downstream receiver.

## Dependencies and provenance

This proof uses the following exact interfaces.

- `GLS21` gives the complete raw pair-labelled promoted decomposition and
  its complementary physical decks.
- `GLS36` gives the fixed-residual incidence map
  `B_Q^anc=im sigma_Q` and the complete target equation.
- `GLS39` adjoins the residual labels and identifies every nonzero raw root
  coefficient with one auxiliary pair map.
- `GLS48` supplies the pointwise three-effective-label floor.
- `GLS49` excludes the residual-pair-plus-one-port support and records
  `p=epsilon_A(q)`.

`GLS40` is frontier context for the rank-five cell but is not a proof step.
The proof below was derived independently through a direct kernel
restriction and through flattening-rank analysis.  The focused exact
verifier replays the coordinate and profile obstructions over the rationals;
the no-import audit uses a separate finite-field representation and direct
coefficient enumeration.

## 1. Common notation and inactive-port contraction

Retain

```text
A={a_0,a_1},                    Q={q_0,q_1},
T=Q disjoint-union Uhat,        |Uhat|=2r-2>=4,
E=V_(a_0)^* tensor V_(a_1)^*,  Delta=span{r_0,r_1,r_2}.
```

For every promoted port `t`, put

```text
X_t:V_t -> V_(a_0)^*,          Y_t:V_t -> V_(a_1)^*,
K_t=ker X_t intersect ker Y_t,
d_t=dim(V_t/K_t)=3-dim K_t.                         (1)
```

The auxiliary residual domains are one-dimensional as in `GLS39`.  The
effective support is

```text
Act={t in T:X_t!=0 or Y_t!=0}.                       (2)
```

Assume pointwise throughout that

```text
omega=0,
q,r_0,r_1,r_2 in B_Q^anc,
rank B_Q^anc=5,
|Act|=3,                                             (3)
```

and that the fixed residual target is fully supported.  Thus its three
residual-torus coefficients `alpha_c` are all nonzero.

Let `P=Act intersect Uhat` and `I=Uhat-P`.  In the complete target equation,
evaluate every port in `I` at

```text
1=e_0+e_1+e_2.                                      (4)
```

Every pure target word evaluates to one at those ports, so no `alpha_c`
vanishes.  A raw pair term with an inactive endpoint has zero root
coefficient by (2).  Every surviving complementary physical deck becomes a
form on the active ports outside its pair, or a scalar when none remain.
Hence (4) loses no source term relevant to the displayed support and makes no
genericity assumption.

In both support types treated below, at least one residual label is
ineffective.  Its two residual shore vectors vanish, so

```text
q=a_0 tensor b_1+a_1 tensor b_0=0,
p=epsilon_A(q)=0.                                   (5)
```

Thus these are precisely `p=0` successors; no physical response is being
divided out.

## 2. One residual label and two promoted ports

Suppose

```text
Act={q_s,u,v}.                                       (6)
```

Write `a=X_(q_s)(1)` and `b=Y_(q_s)(1)`, and define

```text
G_u(z)=a tensor Y_u(z)+X_u(z) tensor b,
G_v(w)=a tensor Y_v(w)+X_v(w) tensor b,
M_uv(z,w)=X_u(z) tensor Y_v(w)+X_v(w) tensor Y_u(z).
                                                               (7)
```

After (4), let

```text
lambda_v in V_v^*   be the deck accompanying G_u,
lambda_u in V_u^*   be the deck accompanying G_v,
gamma in K           be the deck accompanying M_uv.            (8)
```

The complete target consequence is exactly

```text
G_u(z)lambda_v(w)+G_v(w)lambda_u(z)+gamma M_uv(z,w)
 =sum_(c=0)^2 alpha_c z_c w_c r_c.                  (9)
```

No object in (8) is assumed nonzero.

### Lemma 1 (the port-pair deck scalar is nonzero)

At every point satisfying (3) and (6),

```text
gamma!=0.                                           (10)
```

#### Proof

Suppose `gamma=0`.  Take `z in ker lambda_u` and
`w in ker lambda_v`.  Equation (9) and independence of the `r_c` give

```text
z_c w_c=0
for every z in ker lambda_u, w in ker lambda_v, c=0,1,2.       (11)
```

For each `c`, (11) says that the simple bilinear form

```text
(e_c^* restricted to ker lambda_u)
 tensor
(e_c^* restricted to ker lambda_v)
```

is zero.  Hence one factor is zero.  If `lambda_u` is nonzero, its kernel is
contained in `ker e_c^*` only when `lambda_u` is proportional to `e_c^*`,
which can happen for at most one colour.  If `lambda_u=0`, it accounts for no
colour.  The same holds for `lambda_v`.  Two forms can therefore account for
at most two of the three coordinate kernels, contradicting (11). `square`

### Lemma 2 (joint-kernel restriction)

One has

```text
dim K_u<=1,                  dim K_v<=1.             (12)
```

If `K_u=Kz` is nonzero, then

```text
lambda_u(z)!=0,
lambda_u(z)G_v(w)=sum_c alpha_c z_c w_c r_c,         (13)
im G_v subset Delta.                                (14)
```

The transposed statements hold for `K_v` and `G_u`.

#### Proof

For `z in K_u`, both `G_u(z)` and `M_uv(z,w)` vanish.  Equation (9) becomes
(13).  If also `lambda_u(z)=0`, independence of the `r_c`, nonvanishing of
the `alpha_c`, and variation of `w` force every coordinate of `z` to vanish.
Thus `lambda_u` restricts injectively to `K_u`, proving `dim K_u<=1`.
For nonzero `z`, (13) is denominator-free and its right side lies in
`Delta`, proving (14).  Exchange `u` and `v` for the other assertions.
`square`

### Theorem 3 (one-residual profile reduction)

The profile `(1,2,2)` is impossible.  The only surviving profiles are

```text
(1,2,3), (1,3,3),                                   (15)
```

up to exchanging `u,v`.  In profile `(1,2,3)`, the residual--port tensor
opposite the deficient port is exactly diagonal in the denominator-free
sense (13).

#### Proof

The residual label has effective dimension one.  Lemma 2 makes each port
dimension two or three.  If both dimensions were two, both joint kernels
would be lines, and (14) and its transpose would put `im G_u` and `im G_v`
in `Delta`.  By Lemma 1, `gamma` is nonzero; equation (9) then puts
`im M_uv` in `Delta` as well.  Since `q=0`, `GLS36` and `GLS39` give

```text
B_Q^anc=im G_u+im G_v+im M_uv subset Delta,          (16)
```

contradicting `rank B_Q^anc=5`.  This removes `(1,2,2)` and proves (15).
`square`

## 3. Three promoted ports

Suppose instead

```text
Act={u,v,w} subset Uhat.                             (17)
```

Both residual labels are ineffective.  Put `M_st=mu_(s,t)` for the three
promoted pair maps.  After (4), let `lambda_t in V_t^*` be the evaluated deck
opposite `t`.  The exact target consequence is

```text
M_uv(z_u,z_v)lambda_w(z_w)
+M_uw(z_u,z_w)lambda_v(z_v)
+M_vw(z_v,z_w)lambda_u(z_u)
 =sum_(c=0)^2 alpha_c z_(u,c)z_(v,c)z_(w,c) r_c.    (18)
```

Again, every `lambda_t` may initially be zero.

### Lemma 4 (complete coordinate deck-line cover)

All three deck covectors are nonzero, and their projective lines are exactly
the three coordinate lines:

```text
{K lambda_u,K lambda_v,K lambda_w}
 ={K e_0^*,K e_1^*,K e_2^*}.                        (19)
```

#### Proof

Apply the coefficient functional selecting `r_c` and killing the other two
diagonal directions.  Quotient the `u`, `v`, and `w` covector factors by
`K lambda_u`, `K lambda_v`, and `K lambda_w`, respectively.  Every source
term in (18) vanishes in the resulting triple quotient.  Therefore

```text
(e_c^* mod K lambda_u)
 tensor (e_c^* mod K lambda_v)
 tensor (e_c^* mod K lambda_w)=0.                   (20)
```

A pure tensor over a field is zero only when one factor is zero.  Thus, for
each colour `c`, at least one of the three deck lines is `K e_c^*`.  A
nonzero line can equal at most one of the three distinct coordinate lines,
and a zero covector covers none.  Three deck slots must cover three colours,
so all are nonzero and give a permutation, proving (19). `square`

### Lemma 5 (three-port joint-kernel restriction)

For every `t in {u,v,w}`,

```text
dim K_t<=1.                                         (21)
```

If `K_u=Kk_u` is nonzero, then

```text
lambda_u(k_u)!=0,
lambda_u(k_u)M_vw(z_v,z_w)
 =sum_c alpha_c k_(u,c)z_(v,c)z_(w,c) r_c,          (22)
im M_vw subset Delta.                               (23)
```

The cyclic statements also hold.

#### Proof

Restrict (18) to `z_u in K_u`.  The two pair maps incident with `u` vanish,
leaving (22).  If `lambda_u(z_u)=0`, the right side vanishes for every
`z_v,z_w`, so `z_u=0`.  Thus `lambda_u` is injective on `K_u`, proving (21),
and (22) proves (23).  Cycle the labels. `square`

### Theorem 6 (three-port profile reduction)

At least one of the three joint port maps is injective.  The only surviving
effective-dimension profiles are

```text
(2,2,3), (2,3,3), (3,3,3),                          (24)
```

up to permutation.

#### Proof

Lemma 5 makes every effective dimension two or three.  If all three joint
kernels were lines, (23) and its cyclic mates would put all three pair-map
images in `Delta`.  Because `q=0`,

```text
B_Q^anc=im M_uv+im M_uw+im M_vw subset Delta,        (25)
```

contradicting rank five.  Hence at least one kernel is zero, giving exactly
(24). `square`

## 4. Exhaustive support cover and exact boundary

Under `|Act|=3`, the support contains zero, one, or two residual labels.

```text
two residuals plus one port:      excluded by GLS49;
one residual plus two ports:      profiles (1,2,3), (1,3,3);
three promoted ports:             coordinate deck-line permutation;
                                  profiles (2,2,3), (2,3,3), (3,3,3).
```

Together with `GLS48`, this is an exhaustive classification of the
exactly-three-effective-label rank-five full-swallow target cell.  It is not
an exhaustive classification of rank five itself: four or more labels remain
open, and existence of the five displayed profiles is not asserted.

The exact frontier after `GLS50` is

```text
zero-anchor rank-five target with <=2 labels:                 EXCLUDED;
zero-anchor rank-five target with residual pair + one port:   EXCLUDED;
one-residual/two-port exactly-three-label profiles:           TWO OPEN;
three-port exactly-three-label profiles:                      THREE OPEN;
zero-anchor rank-five with >=4 labels:                        OPEN;
ranks six through nine full swallow:                          OPEN;
silent source necessarily enters full swallow:               UNKNOWN;
raw escape supplies an original legal target package:        NOT SUPPLIED;
nonzero-anchor marginal/double-transverse branches:           OPEN;
selector/response/activity/synchronization/nuisance gates:    OPEN;
arbitrary-root strategic-node closure:                        UNKNOWN;
global Krenn--Gu conjecture:                                  UNRESOLVED.
```

The smallest continuation is a target-coupled classification or exclusion
of the five surviving profiles, preferably through the same kernel/deck
identities rather than a support atlas, together with a rank-independent
bridge for four-or-more labels and ranks six through nine.

## Verification boundary

The focused verifier checks the contracted target tensors, the two-form
coordinate-cover obstruction, exact injectivity and rank of the one- and
two-opposite-port target-slice maps, the profile logic, and the three-deck
coordinate cover.  It is an identity and case-cover replay, not the prose
proof.

The independent audit imports no project code and uses a different prime,
custom projective/kernel arithmetic, and direct coefficient tables.  It exhausts
zero and nonzero deck forms, all projective kernel lines, and the hostile
two-kernel/zero-third-deck branch.

Neither checker validates physical source coverage, a legal selector or
response, a named downstream receiver, or the global conjecture.
