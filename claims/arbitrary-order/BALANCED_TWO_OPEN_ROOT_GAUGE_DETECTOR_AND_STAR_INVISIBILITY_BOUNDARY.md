# Balanced two-open-root gauge detector and star-invisibility boundary

## Status

**Exact characteristic-zero matching theorem and sharp physical boundary.**
Start with the fixed-surplus root layer of
[`BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md`](BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md).
Opening two old roots gives five, not two, matching sectors.  In particular,
when the first root uses an affine absorption perturbation and the second
root meets a pinned old root, an additional surplus-`2q+2` companion term is
present.  The theorem below gives the complete two-open identity and the
full affine-gauge variation, including that essential term.

The resulting detector is conditional.  It succeeds if a no-companion
sector can be selected and its defect-row permanent is nonzero, or if the
row-replacement map is injective on the effective companion space.  Neither
condition is currently forced for every hypothetical witness.

The boundary is exact.  At tight surplus `q=0`, a one-mode `a` row produces
a physical star outside graph on which the affine absorption is an exact
kernel of the **entire graph tensor**.  A sign-reversing matching involution
proves this at arbitrary order.  The construction can be installed over any
nonzero tight `P_r` layer without changing that contracted layer, but it does
not construct the tight layer, satisfy the unspecialized GHZ identity, or
give a Krenn--Gu witness or counterexample.

The global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Fixed-surplus notation

Work over a characteristic-zero field.  Let

```text
Omega=R disjoint-union B,
|R|=r,                 |B|=r+2q.                     (1)
```

Fix fully supported root vectors `x_s`, `s in R`, satisfying

```text
W_st(x_s,x_t)=0                  for distinct s,t in R.   (2)
```

For `u in B`, write

```text
h_(s,u)=W_su(x_s,-) in L_u^*.                         (3)
```

For even `A subset R`, define the layer with the roots in `A` removed by

```text
Lambda_A
 =sum_(S subset B, |S|=2q+|A|)
    H_S tensor
    P_(r-|A|)(h_(s,u):s in R-A, u in B-S).            (4)
```

Here `H_S` is the physical perfect-matching tensor of the outside graph on
`S`, and the permanent in (4) sums all labelled bijections from the
remaining roots to `B-S`.  Thus `Lambda_empty` is the fixed-surplus layer,
`Lambda_{i,j}` has outside order `2q+2`, and
`Lambda_{i,j,s,t}` has outside order `2q+4`.

For a root `i` and a vector `y in L_i`, put

```text
k_(i,u)(y)=W_iu(y,-),
ell_(i,s)(y)=W_is(y,x_s).                              (5)
```

If `A` is even, disjoint from `i`, and `i in R-A`, let `L_i^A(k_i(y))`
denote (4) with the persistent row `i` replaced by the family `k_(i,u)(y)`.
Write `L_i=L_i^empty`.  Similarly, `L_ij(y,z)` replaces both rows `i,j` in
the original fixed-surplus layer.

## 2. The complete two-open-root equation

Fix distinct roots `i,j`.  Leave their local vectors `y in L_i` and
`z in L_j` open, while every other root remains fixed at `x_s`.

### Theorem 1 (five-sector two-open identity)

The graph tensor contracts exactly to

```text
T_ij(y,z)
 =L_ij(y,z)
  +W_ij(y,z) Lambda_{i,j}

  +sum_(s in R-{i,j})
     ell_(i,s)(y) L_j^{i,s}(z)

  +sum_(s in R-{i,j})
     ell_(j,s)(z) L_i^{j,s}(y)

  +sum_(s,t in R-{i,j}, s!=t)
     ell_(i,s)(y) ell_(j,t)(z) Lambda_{i,j,s,t}.       (6)
```

For a ternary GHZ witness, (6) equals

```text
sum_(c=0)^2
  y[c] z[c] product_(s in R-{i,j}) x_s[c]
  e_c^(star tensor B).                                (7)
```

### Proof

Restrict a perfect matching to the two open roots.

1. Both open roots meet distinct outside vertices.  Every pinned root also
   meets outside, because an edge between two pinned roots has value zero.
   This is `L_ij`.
2. The open roots meet one another.  Removing them leaves the layer
   `Lambda_{i,j}`.
3. Root `i` meets one pinned root `s`, while `j` meets outside.  Removing
   `i,s` leaves the row-replaced surplus-`2q+2` layer `L_j^{i,s}`.
4. Root `j` meets one pinned root `s`, while `i` meets outside.  This gives
   `L_i^{j,s}`.
5. The roots `i,j` meet two distinct pinned roots `s,t`.  Removing all four
   roots leaves `Lambda_{i,j,s,t}`.

The five cases are disjoint and exhaustive.  In the final sum, `(s,t)` is
ordered by which pinned root meets `i` and which meets `j`; there is no
factor `1/2`.  Every matching occurs once.  The permanents already count the
cross bijections, while `H_S` already counts the outside matchings, so no
additional binomial or factorial multiplicity occurs in (6).

## 3. Full variation of the affine absorption gauge

Assume that the entire outside graph has the physical two-row form

```text
W_uv=a_u tensor b_v+b_u tensor a_v,                   (8)
```

and that the second row is the fixed row of root `j`,

```text
b_u=h_(j,u).                                          (9)
```

Choose `eta_j in L_j^*` with `eta_j(x_j)=1`, and define the open `j` row
and its projective defect by

```text
g_u(z)=W_ju(z,-),
d_u(z)=g_u(z)-eta_j(z)b_u.                            (10)
```

Choose `0!=kappa_i in L_i^*` with `kappa_i(x_i)=0`.  Consider the physical
affine perturbation, with `tau` its formal direction parameter,

```text
delta W_iu=tau kappa_i tensor a_u,
delta W_ij=-tau(q+1) kappa_i tensor eta_j,             (11)
```

with transposed blocks in the reverse orientations.

### Theorem 2 (defect plus companion formula)

Put `m=r+2q`.  The complete variation of (6) is

```text
delta T_ij(y,z)
 =tau kappa_i(y) [ D_ij(z)+C_ij(z) ],                 (12)

D_ij(z)
 =(1/q!)
   P_m(H_(R-{i,j}), a repeated q+1,
       b repeated q, d(z)),                           (13)

C_ij(z)
 =sum_(s in R-{i,j}) ell_(j,s)(z) A_(i,j;s),         (14)

A_(i,j;s)
 =(1/(q+1)!)
   P_m(H_(R-{i,j,s}), a repeated q+2,
       b repeated q+1).                               (15)
```

The row counts in (13) and (15) are respectively

```text
(r-2)+(q+1)+q+1       =r+2q=m,
(r-3)+(q+2)+(q+1)     =r+2q=m.                        (16)
```

### Proof

First restrict to matchings in which both `i` and `j` meet outside.  A
`2q`-vertex outside hafnian in (8) is

```text
(1/q!) P_(2q)(a repeated q,b repeated q).             (17)
```

Using the perturbed `i` row adds one `a` row, while the open `j` row is
`g(z)`.  This gives

```text
(tau kappa_i(y)/q!)
P_m(H_(R-{i,j}),a^(q+1),b^q,g(z)).                    (18)
```

The `delta W_ij` term is

```text
-tau(q+1)kappa_i(y)eta_j(z) Lambda_{i,j}.             (19)
```

The outside order in `Lambda_{i,j}` is `2q+2`, so

```text
Lambda_{i,j}
 =(1/(q+1)!)
   P_m(H_(R-{i,j}),a^(q+1),b^(q+1)).                  (20)
```

Since `(q+1)/(q+1)!=1/q!`, subtracting (19) from (18) replaces the final
row `g(z)` by `d(z)`.  This is (13).

There is one further sector.  The perturbed `i`-outside edge may be used
while `j` meets a pinned root `s`.  Removing `j,s` leaves `r-2` persistent
rows, including the new `a` row at `i`, and an outside hafnian of order
`2q+2`.  Equation (17) with `q+1` in place of `q` gives exactly (14)--(15).
There is no compensating `delta W_ij` term in this sector because `j` is
already occupied by `s`.

No other term in (6) changes under (11).  This proves the full formula.

### Exact detector criteria

The two-open tensor detects (11) exactly when the linear map

```text
z |-> D_ij(z)+C_ij(z)                                 (21)
```

is nonzero.  Two useful sufficient hypotheses are:

1. a legal selector isolates the no-`j`-companion sector and the defect-row
   permanent (13) is nonzero;
2. on the projectively constant branch `d=0`, the map

   ```text
   (lambda_s)_s |-> sum_s lambda_s A_(i,j;s)          (22)
   ```

   is injective on the nonzero effective companion-coefficient space

   ```text
   E_j={(ell_(j,s)(z))_s:z in ker eta_j} != {0}.      (23)
   ```

For a hypothetical GHZ witness, Theorem 6 (the exact single-open-root
equation), equation (33), of
[`BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md`](BALANCED_FIXED_SURPLUS_TRUNCATION_FIBRE_NONOBSERVABILITY_AND_TRANSVERSE_ABSORPTION_THEOREM.md)
excludes `E_j={0}`: a nonzero vector in `ker eta_j` kills the projective
outside row and every root-companion coefficient, but not the injective
diagonal target map.  This is a witness-level observation, not part of the
unconditional detector criterion.  No current theorem proves the
injectivity in (22).  Projective constancy `d=0` by itself therefore does
not prove either detection or invisibility.

## 4. Clean higher strata

Fix a labelled partial matching `P` of `p` additional old-root pairs,
disjoint from `{i,j}`.  Keep `j` pinned at `x_j`, do not allow `j` to meet a
root in `P`, and isolate this matching stratum from every other companion
sector.

After removing the `2p` roots used by `P`, the half-surplus is `q+p`.  The
row-pointing argument of the fixed-surplus theorem gives

```text
L_i^P(a)=(q+p+1) Lambda_(i,j;P).                      (24)
```

The compensation in (11) removes only `(q+1)Lambda_(i,j;P)`.  Therefore

```text
delta T_P
 =tau p kappa_i times
   (coefficient of P) Lambda_(i,j;P).                 (25)
```

In characteristic zero, the first nonzero **isolated clean** stratum with
`p>=1` detects the gauge.  This does not say that `p=1` is the first global
detector.  Opening `j` introduces (13)--(15) already at `p=0`; allowing `j`
to meet another root introduces further sectors; and a physical support may
make every clean `p>=1` layer zero.

## 5. A star-supported exact tensor gauge at `q=0`

Now put `q=0`, so `|B|=|R|=r`.  Fix distinct roots `i,j` and one outside
vertex `u_0`.  Choose nonzero covectors `a_(u_0)`, `kappa_i`, and `eta_j`,
put

```text
a_u=0                         for u!=u_0,             (26)
```

and let `b_u` be arbitrary outside covectors.  Install the outside star

```text
W_(u_0,v)=a_(u_0) tensor b_v       for v!=u_0,
W_uv=0                             if u,v!=u_0,        (27)
```

and the projective root shore

```text
W_jv=eta_j tensor b_v.                                (28)
```

Consider

```text
delta W_(i,u_0)=tau kappa_i tensor a_(u_0),
delta W_ij=-tau kappa_i tensor eta_j.                 (29)
```

### Theorem 3 (star-invisibility involution)

The perturbation (29) preserves the complete graph tensor exactly, for
arbitrary values of all local vertex vectors and arbitrary values of every
other physical block.

### Proof

The tensor is affine in `tau`, because every perfect matching uses only one
edge incident with `i`.  Consider a matching in its `tau` coefficient.

If it uses `delta W_(i,u_0)`, then `u_0` is occupied.  No outside--outside
edge is available, because every such edge belongs to the star (27).  If `p>0`
remaining root--root edges were used, balance would require `p`
outside--outside edges, which is impossible.  Thus every remaining root
crosses outside.  In particular, `j` meets one vertex `v!=u_0` through
`W_jv`.

If the matching instead uses `delta W_ij`, balance requires one more
outside--outside edge than remaining root--root edges.  The star has matching
number one, so there are no further root--root edges and exactly one outside
edge, necessarily `u_0v` for some `v!=u_0`.

The replacement

```text
{i-u_0, j-v}  <->  {i-j, u_0-v}                      (30)
```

leaves every other edge unchanged.  The two products are

```text
+tau kappa_i a_(u_0) eta_j b_v,
-tau kappa_i eta_j a_(u_0) b_v.                      (31)
```

They are equal with opposite signs.  The replacement (30) is an involution without
fixed points, so every coefficient cancels.  This proves exact invariance of
the entire tensor, not merely invariance of zero-, one-, or two-open root
jets.

In the language of Theorem 2, (28) gives `d=0`, while every companion
permanent (15) contains two copies of `a`.  Both copies are supported only at
`u_0`, so injectivity of the permanent assignment fails and every
`A_(i,j;s)` is zero.  All clean higher layers also require at least two
outside star edges and vanish.

### Conditional tight-layer relevance

Suppose a nonzero tight layer is already given:

```text
P_r(H_1,...,H_r)=sum_(c=0)^2 X_c e_c^(star tensor B),
X_0 X_1 X_2!=0.                                       (32)
```

Laplace expansion along row `i` has at least one nonzero summand.  Choose
`u_0` at such a summand and choose `a_(u_0)` so that `L_i(a)!=0`.  Put
`b=h_j`, lift the `j` shore by (28) with `eta_j(x_j)=1`, and require
`kappa_i(x_i)=0`.  The outside graph is absent from the tight contraction,
so installing (27) and applying (29) leaves the fixed rows, pairwise root
zeros, and the tight restriction (32) unchanged.  The single-open absorption
is nontrivial, while Theorem 3 shows that no higher root jet detects it.

This is a conditional fibre statement.  It does **not** construct a tight
restriction (32), prove that the installed full graph equals GHZ, or assert
the existence of a hypothetical witness on the star stratum.  It is not a
Krenn--Gu counterexample.  It proves only that the fixed layer and matching
recursion do not universally remove this physical representation gauge.

For `q>=1`, the permanent Hall quotas force substantially more support in
the repeated `a` row.  The one-mode star construction is therefore not
claimed beyond `q=0`.

## 6. Exact boundary

```text
complete five-sector two-open identity:              PROVED;
defect-row plus old-root-companion variation:         PROVED;
no-companion defect selector criterion:               PROVED;
companion-space injectivity detector criterion:       PROVED;
clean pinned-j p-stratum residual factor p:           PROVED;
universal first-higher-stratum detector:              FALSE;
q=0 star affine gauge preserves full graph tensor:    PROVED;
existence of a tight layer on the star stratum:        NOT CLAIMED;
existence of a GHZ witness on the star stratum:        NOT CLAIMED;
unfactorized/higher-surplus witness exclusion:         UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.
```

## Focused check

Run from repository root:

```text
python claims/arbitrary-order/verify_balanced_two_open_root_gauge_detector_and_star_invisibility.py
python claims/arbitrary-order/audit_balanced_two_open_root_gauge_detector_and_star_invisibility.py
```

The primary checker groups direct perfect matchings into the five sectors
for small `q`, checks the repeated-row hafnian/permanent factorials, and
verifies the exact `r=5` star involution with formal monomial labels.  The
independent audit does not import the primary.  It uses a separate bitmask
matching partition, endpoint-word ledgers, and formal monomial expansion to
check the ordered pinned-root sectors, every companion term, the factorials,
and the star involution through separate small exact instances.  These
bounded checks audit conventions and multiplicities.  The arbitrary-order
proofs are the matching partition and the sign-reversing involution above.
