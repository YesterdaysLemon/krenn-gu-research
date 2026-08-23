# Maximum-root surplus-two zero-anchor full-swallow pure-core/excess-response dichotomy and all-rank intersection theorem

## Status and scope

**Exact characteristic-zero arbitrary-root pointwise reduction.**  Fix one
`GLS8`-eligible `(Q,A)` chart, one fully supported residual contraction, and
the zero-anchor full-swallow branch of `GLS35`--`GLS40`.  Work on the `GLS22`
transverse localization

```text
p=epsilon_A(q)!=0.
```

For every promoted pair target, `GLS40` confines the desired tensor, its
complete transverse nuisance, and all three pure target columns to a cylinder
of dimension `9(k-1)`, where `k=dim B_Q^anc`.  This theorem gives that
cylinder a canonical pure-core subspace and associated excess quotient:

- the projected pure core, of dimension `27` when `q notin Delta` and `18`
  when `q in Delta`; and
- the excess quotient, canonically dual to the `GLS40` excess-syzygy space in
  the root factor.

Projecting the complete target identity to the excess quotient proves a sharp
response dichotomy.  A surviving desired excess class forces the physical
response to be zero.  If the response is nonzero, the desired class is
represented in the pure core.  In particular, a nuisance-killing selector
which vanishes on the pure core is necessarily a zero-response selector.

Consequently the useful-row rank-rise test is pointwise exactly the rank rise
of the three pure columns modulo the **intersection** of the complete nuisance
with the `18`- or `27`-row pure core.  This is independent of `k`, but the
intersection must be computed on every rank/divisor fibre.  A generic
projection or a chosen complementary minor is not pointwise sufficient.

This is `GLS41`.  It does not force a pure-core class to survive, supply a
nonzero response, synchronize targets, prove selected-response activity,
provide nuisance survival or a named downstream receiver, cover `p=0`, attach
raw escape, or close the strategic node.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

## Dependencies and provenance

The owning interfaces are:

- [`GLS5`](MAXIMAL_ROOT_SURPLUS_TWO_POINTWISE_SELECTOR_FAILURE_AND_DECOMPOSABLE_RETRACTION_BOUNDARY_THEOREM.md)
  for the pointwise response-gated radical--Fitting criterion;
- [`GLS8`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TWO_PROBE_ONE_TARGET_ATTACHMENT_AND_POINTWISE_FAILURE_REDUCTION_THEOREM.md)
  for the promoted target family and legal one-row interface;
- [`GLS22`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_ALL_PORT_TRANSVERSE_QUOTIENT_AND_PROJECTIVE_SYNCHRONIZATION_FAILURE_THEOREM.md)
  for `P_Q`, the complete transverse target identity, and the equivalence
  between a useful legal selector and transverse pure rank one;
- [`GLS23`](MAXIMAL_ROOT_SURPLUS_TWO_PROMOTED_TRANSVERSE_COMPLETE_NUISANCE_DECOMPOSITION_AND_TOP_ANCHOR_DICHOTOMY_THEOREM.md)
  for the complete labelled transverse nuisance; and
- [`GLS40`](MAXIMAL_ROOT_SURPLUS_TWO_ZERO_ANCHOR_FULL_SWALLOW_AGGREGATE_DECK_EXCESS_SYZYGY_AND_TRANSVERSE_CYLINDER_THEOREM.md)
  for the full-swallow rank strata, the excess module, and the exact target
  cylinder.

No external literature claim is used.  The new content is the canonical
pure-core/excess quotient, its exact sequence, the excess-response
dichotomy, and the all-rank nuisance-intersection criterion.

## 1. Root-factor pure core and excess quotient

Retain the `GLS40` notation

```text
E=E_A^*,
B=B_Q^anc=im sigma_Q,                 k=dim B,
Delta=span{r_0,r_1,r_2},
S=Delta+Kq,
P_Q=p id_E-q tensor epsilon_A,
C_Q=P_Q(B)=N_empty^tr.                              (1)
```

Put

```text
R_Q=P_Q(Delta) subset C_Q.                          (2)
```

### Theorem 1 (canonical pure-core/excess identification)

The map `P_Q` induces a canonical isomorphism

```text
B/S  ->  C_Q/R_Q.                                   (3)
```

Hence

```text
q notin Delta:
  dim R_Q=3,       dim C_Q/R_Q=k-4;

q in Delta:
  dim R_Q=2,       dim C_Q/R_Q=k-3.                 (4)
```

Under the `GLS40` identification

```text
E_Q^exc=sigma_Q^*(Ann(S)) isomorphic to (B/S)^*,    (5)
```

the root excess quotient `C_Q/R_Q` is canonically dual to the excess-syzygy
module.  No complement to `S` in `B` is chosen.

#### Proof

On `D(p)`, `ker P_Q=Kq`.  Since `q in B`, the restriction `P_Q:B->C_Q` is
surjective with kernel `Kq`.  The preimage of `R_Q=P_Q(Delta)` is exactly

```text
Delta+Kq=S:
```

indeed, `P_Q(b)=P_Q(d)` for `b in B,d in Delta` if and only if
`b-d in Kq`.  The first isomorphism theorem gives (3).

If `q notin Delta`, `P_Q` is injective on `Delta`; if `q in Delta`, its
kernel there is `Kq`.  Together with `dim C_Q=k-1`, this proves (4).  Formula
(5) is the `GLS40` pullback description, and dualizing (3) proves the final
statement. `square`

## 2. Cylinder exact sequence and response dichotomy

Fix a promoted pair target `C subset Uhat`, `|C|=2`, and put

```text
L_C^cyl=C_Q tensor V_C^*,
R_C^pure=R_Q tensor V_C^*,
N_C=N_C^tr subset L_C^cyl.                           (6)
```

The containment in (6) is `GLS40`; `N_C` is still the **complete labelled**
transverse nuisance, not a smaller replacement.  Let

```text
pi_C:L_C^cyl -> (C_Q/R_Q) tensor V_C^*               (7)
```

be the quotient map.

### Theorem 2 (exact core/excess sequence)

There is a canonical short exact sequence

```text
0 -> R_C^pure/(N_C intersect R_C^pure)
  -> L_C^cyl/N_C
  -> ((C_Q/R_Q) tensor V_C^*)/pi_C(N_C)
  -> 0.                                               (8)
```

All three transverse pure columns `d_(C,c)^tr` lie in `R_C^pure`.  Projecting
the complete `GLS22` target identity through the right map in (8) gives

```text
[pi_C(t_C)] tensor P_(S_C)(H;z_Q)=0                  (9)
```

in

```text
(((C_Q/R_Q) tensor V_C^*)/pi_C(N_C)) tensor W_(S_C).
```

Consequently, pointwise:

1. if the desired excess class `[pi_C(t_C)]` is nonzero, then the physical
   response `P_(S_C)(H;z_Q)` is zero;
2. if the response is nonzero, then `[t_C] in L_C^cyl/N_C` lies in the image
   of the pure-core term on the left of (8); and
3. if `mu in (L_C^cyl)^*` satisfies

   ```text
   mu(N_C)=mu(R_C^pure)=0,              mu(t_C)!=0,    (9a)
   ```

   then, after rescaling on `t_C` and extending linearly from the cylinder to
   `K_C^tr`, it gives a legal full transverse selector whose physical
   response is zero.

#### Proof

For any vector space `L`, subspace `R`, and subspace `N`, the quotient map
`L/N -> (L/R)/pi(N)` is surjective.  Its kernel is `(R+N)/N`, canonically
isomorphic to `R/(N intersect R)`.  Apply this with the three spaces in (6)
to obtain (8).

`GLS40` puts each pure column in `R_C^pure`.  The complete transverse target
identity of `GLS22` is

```text
sum_c alpha_c[d_(C,c)^tr] tensor w_(S_C,c)
  =[t_C] tensor P_(S_C)(H;z_Q)                       (10)
```

in `L_C^cyl/N_C`; every term lies in the cylinder.  The left side maps to
zero under (8), proving (9).  A pure tensor over a field is zero if and only
if one factor is zero, proving statements 1 and 2.  The functional in
statement 3 factors through the right quotient and makes its desired class
nonzero.  Because `N_C subset L_C^cyl`, any linear extension to `K_C^tr`
still kills the complete nuisance; rescaling by its nonzero value on `t_C`
gives the `GLS22` normalization.  Statement 1 then makes its response zero.
`square`

This theorem does not say that a nonzero response is forced.  It says that
the high-rank excess quotient cannot be the source of a **useful** nonzero
response.

## 3. Exact all-rank pure-core intersection criterion

Write

```text
D_C^tr=[d_(C,0)^tr|d_(C,1)^tr|d_(C,2)^tr].           (11)
```

### Theorem 3 (usefulness is exactly a core-intersection rank rise)

At every point of every nuisance-rank and divisor fibre,

```text
rank[N_C|D_C^tr]>rank N_C
iff
rank[(N_C intersect R_C^pure)|D_C^tr]
  >rank(N_C intersect R_C^pure).                     (12)
```

Thus the `GLS5/GLS22` useful-row test on the complete target is pointwise an
exact quotient problem in

```text
R_C^pure/(N_C intersect R_C^pure),                   (13)
```

whose ambient dimensions are

```text
27  if q notin Delta,
18  if q in Delta.                                   (14)
```

These dimensions do not depend on `k in {4,...,9}`.

#### Proof

All columns of `D_C^tr` lie in `R_C^pure`.  The left injection in (8) shows
that their span modulo `N_C` is canonically their span modulo
`N_C intersect R_C^pure`.  Its dimension is the rank increment on either
side of (12).  Since `dim V_C^*=9`, equations (4) and (6) give (14).
`square`

### All-fibre implementation without a chosen minor

Use the fixed-domain canonical pure map

```text
A_C=(P_Q|Delta) tensor id_(V_C^*):
    Delta tensor V_C^* -> K_C^tr.                     (15)
```

Its domain has dimension `27`; its image is `R_C^pure`, with rank `27` or
`18` on the two strata.  At one point, let `B_C:K^m->K_C^tr` present `N_C`
and define the exact fibre product

```text
K_C^fib=ker[B_C|-A_C]
  subset K^m direct-sum (Delta tensor V_C^*).         (16)
```

Then

```text
A_C(pr_r K_C^fib)=N_C intersect R_C^pure.            (17)
```

Equations (16)--(17), followed by (12), are an exact finite criterion on that
point.  The canonical map (15) is allowed to drop from rank `27` to rank `18`;
no image basis or minor is chosen.  Over a parameter family the kernel, its
projection, and the nuisance rank can all jump.  A pointwise theorem must
therefore retain the complete kernel/module or its saturated Fitting encoding
on every fibre; it may not choose one generic kernel basis or one denominator.

## 4. Sharp projection/intersection boundary

The excess projection does not determine the pure-core intersection.  Over
`K[t]`, let

```text
L=K e_0 direct-sum K e_1,
R=K e_0,
N_t=span{e_1,t e_0},
D=e_0.                                                (18)
```

The projection of `N_t` to `L/R` is `K[e_1]` for every `t`.  Nevertheless,

```text
t!=0: N_t intersect R=R,    D is swallowed;
t=0:  N_t intersect R=0,    D survives.              (19)
```

Thus even a constant full excess projection does not control pointwise
pure-core survival.  This is an abstract exact module boundary, not a graph
or witness.

The `GLS40` rank-six labelled control exhibits the complementary response
boundary: its excess rows are nonzero on labelled incidence, while every
label detected by those rows has zero assigned deck.  It satisfies the fixed
residual aggregate equation but is not proved physical.  Together, (18)--(19)
and that inherited control rule out replacing the intersection in (12) by a
generic excess projection or by excess activity alone.

## 5. Frontier and unresolved remainder

```text
canonical B/S to C_Q/R_Q identification:                 PROVED;
18/27-row pure-core dimensions:                           PROVED;
core/excess quotient exact sequence:                      PROVED;
surviving excess desired class forces zero response:      PROVED;
useful-row test equals pure-core intersection rank rise:  PROVED;
all rank/divisor fibres retained by fibre product:         PROVED;
some pure-core class survives on every source point:       OPEN;
response / synchronization / activity / nuisance gates:   OPEN;
named downstream receiver and arbitrary-r attachment:      OPEN;
silent p=0 source cover and raw escape attachment:         OPEN;
strategic-node closure:                                    OPEN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The smallest remaining load-bearing obligation on `D(p)` is no longer an
arbitrary `27,...,72`-row selector search.  For every eligible source point,
one must force

```text
im D_C^tr not subset N_C^tr intersect R_C^pure        (20)
```

for one promoted pair `C` at one common contraction retaining the owning
`H_Q(z_Q)p(z_Q)!=0` source gate, or contradict the simultaneous validity of
these containments using the complete same-graph pure/mixed equations.  The
rank rise already supplies that chosen row's complete-nuisance selector; it
must still be synchronized with the required responses, have declared
activity and every additional/common downstream nuisance gate, and enter a
named downstream theorem.  The zero-anchor top target remains dead, and
`p=0` remains outside this reduction.

## Verification boundary

Run the focused exact primary verifier:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py
```

Run the genuinely independent no-import audit:

```text
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_full_swallow_pure_core_excess_response_dichotomy_and_all_rank_intersection.py
```

The primary uses SymPy to replay both root-factor strata, the induced quotient
ranks, exact-sequence dimensions, core/ambient pure-rank equivalence, and the
jumping family (18).  The audit imports no project module or third-party
package; it uses independent `Fraction` elimination and a different family of
small exact cylinder/intersection fixtures.  The arbitrary-root and all-fibre
statements are the written linear-algebra proofs above, not a finite search.
