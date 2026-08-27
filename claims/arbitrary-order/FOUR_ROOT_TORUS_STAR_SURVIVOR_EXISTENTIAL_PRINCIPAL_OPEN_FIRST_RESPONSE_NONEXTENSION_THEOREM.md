# Four-root torus-star survivor: existential principal-open first-response nonextension

## Status

**Exact existential survivor-open nonextension (`GLD80`).**  Work over
`K=Q(i)` and then over its algebraic closure in `C`.  Retain the complete
canonical `GLD70` fully-supported, nonisotropic rank-two maximal torus-star
interface, the scale-fixed equal-leaf survivor chart of `GLD75`--`GLD76`, the
complete `35`-dimensional raw coefficient fibre, and the legal `q_0` first
response.

There is a principal Zariski neighborhood of the exact `GLD72` Gaussian
survivor on which every raw coefficient preimage fails the legal first-response
condition.  This is the first survivor-locus, rather than single-tensor,
extension of `GLD74`.

The principal open is **existential**: the proof produces an element `delta`
of the survivor coordinate ring with `delta(F_0)!=0`, but does not expand that
polynomial.  Computing an explicit base-only exceptional divisor remains a
named elimination obligation.  The theorem is local to the certified
scale-fixed fixed-star component.  It does not cover another survivor
component or frame gauge, another source presentation, root, or interface;
certify maximum root order or exclude a fifth root; produce a graph witness;
or resolve Krenn--Gu.  The global conjecture remains **UNRESOLVED**.

This version also repairs an ambiguity in the original `GLD78` wording.  The
moving `65 x 3` necessary system is formed only **after** conjugating each
frame to literal `Delta_4` and transporting the complete nuisance and legal
response interface.  The fixed-coordinate `68 x 4` system of `GLD76` remains
the exact universal legal-lift incidence; no three-column condition is asserted
in untransformed moving coordinates.

## 1. Algebraic survivor base and complete frame transport

Let `X_sf` be the affine scale-fixed equal-leaf frame scheme of `GLD76`.  It
has fifteen shifted frame coordinates, the ten exact `GLD75` generators, and
the scale equation `x_8=0`.  Its Gaussian point is `F_0`, and its Jacobian has
rank eleven there.

Equality of the full and equal-leaf survivor germs in `GLD75` gives an affine
principal neighborhood of `F_0` on which the two schemes agree.  Shrink it so
that the following named factors are units:

```text
Omega = frame-gauge factors times product_u det(F_u),
theta = the selected rank-44 nuisance pivot,
gamma = the selected rank-13 transformed mixed-response pivot,
beta  = the selected rank-8 invariant-kernel pivot.     (1)
```

The fixed interface support and nonisotropic factors are also retained.  Write

```text
B=Spec A subset X_sf,                    F_0 in B.      (2)
```

For the frame tuple `F=(F_(0),F_(1),F_(2),F_(3))` put

```text
U_F=F_(0)^(-1) tensor F_(1)^(-1) tensor F_(2)^(-1) tensor F_(3)^(-1). (3)
```

Let `P'_u=P_u F_u^(-T)` be the transformed port planes, let `b_F` and
`D'_F` be the complete nuisance and legal-response maps rebuilt from those
ports, and let `S_F` be the induced raw-coordinate change: it is the identity
on the `Q` coordinate, `F_u^(-1)` on each residual label at port `u`, and the
corresponding Kronecker product on every port-pair label.  Let
`J_F=diag(J_F^const,I_4)` be the invertible `17 x 17` response-domain change,
where `J_F^const` is induced on the thirteen constant columns and the four
root directions are unchanged.  Direct multilinearity of every matching
cofactor gives

```text
U_F b = b_F S_F,
U_F D_q0(alpha) = D'_F(S_F alpha) J_F,
U_F R(F) = [e_0000 e_1111 e_2222].                     (4)
```

More explicitly, `U_F C=C'_F J_F^const` on the first thirteen columns and
`U_F H_r=H'_(r,F)S_F` on every root-response operator.  These are identities
of the actual graph/interface response maps, not merely of abstract GHZ
tensors.  The matrices `U_F`, `S_F`, and `J_F` are invertible on `D(Omega)`.
Hence a raw preimage and legal lift in the original fixed interface exist
exactly when their transported counterparts exist.

On `D(theta)` use the same pivot choices that specialize to `GLD74` to write

```text
b_F beta=Delta_4,
beta(F,t)=beta_0(F)+K_F t,                t in A^35.    (5)
```

Thus `K_F` is a regular frame of the moving kernel bundle, not a silently
fixed kernel of the conjugated map.  At `F_0`, (5) is exactly the `GLD74`
affine solve and quotient coordinate system.

## 2. Moving literal-Delta rank-one necessity

Let `C'_F` be the thirteen `Q`/eta-residual columns of `D'_F`, let `pi_mix`
retain the 78 non-diagonal literal-Delta words, and quotient
`pi_mix C'_F` by the fixed pivot selected in (1).  On `D(gamma)` this gives a
regular map

```text
q_F: A^78 -> A^65.                                      (6)
```

For the four root-response columns define

```text
Z_r(F,t)=q_F pi_mix H'_(r,F)(beta(F,t))
        =A_r(F)+K_(r,F)t,                  r=0,1,2,3.   (7)
```

All matrices in (6)--(7) are regular on `B`; inverses occur only through the
named units in (1).

### Lemma 2.1 (transported matching-partition identity)

For every `beta` satisfying `b_F beta=Delta_4`,

```text
Z_0+Z_1+Z_2-Z_3=0.                                    (8)
```

#### Proof

Partition the perfect matchings contributing to `b_F beta` by the neighbor
of `q_0`.  The classes in which that neighbor is `q_1` or one of the four
ports are the `Q` and twelve eta-residual columns with coefficient vector
`lambda(beta)=(beta_Q,beta_(eta,u,c))`.  The four classes in which it is root
`r` are `xi_r H'_(r,F)(beta)`, where `xi=(1,1,1,-1)`.  Therefore the exact
identity is

```text
b_F beta - sum_r xi_r H'_(r,F)(beta)=C'_F lambda(beta). (9)
```

The mixed projection of `b_F beta=Delta_4` vanishes.  Apply `q_F pi_mix` to
(9) to obtain (8).  This partition uses every matching exactly once and is
independent of the numerical port entries.  `square`

### Lemma 2.2 (moving rank-one necessity)

If a raw preimage `alpha` of `T(F)` has a legal first-response lift, then

```text
rank[Z_0(F,t) Z_1(F,t) Z_2(F,t)] <= 1.                 (10)
```

#### Proof

Transport the inclusion by (4).  Its target becomes the three-dimensional
literal diagonal space.  Both `C'_F` and `pi_mix C'_F` have rank thirteen on
`B`.  Lemma 2.1 eliminates the fourth root column after the mixed quotient,
so

```text
rank(pi_mix D'_F)=13+rank[Z_0 Z_1 Z_2].                (11)
```

The complete response map still has a 17-dimensional domain.  Consequently

```text
dim(im D'_F intersect Diag)
 <=17-(13+rank[Z_0 Z_1 Z_2])
 =4-rank[Z_0 Z_1 Z_2].                                (12)
```

Containing the three-dimensional target forces (10).  This is the `GLD74`
dimension argument in a moving, fully transported literal-Delta interface.
It does not replace the fixed-coordinate `68 x 4` equivalence of `GLD76`.
`square`

## 3. Intrinsic saturated projective incidence

Homogenize (7) in one projective raw coordinate:

```text
mathcal Z_r(F;t,s)=s A_r(F)+K_(r,F)t,
                                      [t:s] in P^35.   (13)
```

Define

```text
Ybar=V(I_2[mathcal Z_0 mathcal Z_1 mathcal Z_2])
     subset B times P^35,                              (14)
```

where `I_2` is the ideal of all `2 x 2` minors.  This intrinsic formulation
retains every proportionality chart and rank drop.  Its projection to `B` is
projective.

The finite raw-fibre incidence is

```text
Y_aff=Ybar intersect D_+(s).                           (15)
```

Let

```text
C=closure_(Ybar)(Y_aff)_red.                           (16)
```

Before reduction its homogeneous ideal is `(I_2:s^infinity)`.  Thus `C` is
the strict closure of finite raw preimages, not all of the possibly larger
projective boundary.  It is closed in `Ybar`, so `C->B` is proper.  Flat
field extension commutes with localization, contraction, and this saturation;
the same strict-closure description holds after base change.

## 4. Algebraic trait lemma

### Lemma 4.1 (finite-type DVR selection)

Let `k` be algebraically closed, `V` a finite-type `k`-scheme, `U` a
locally constructible subset, and `x` a closed point of `closure(U)\U`.
There is a morphism

```text
Spec R -> V,                                           (17)
```

where `R` is a DVR, the closed point maps to `x`, and the generic point maps
to `U`.

#### Proof

Choose an irreducible locally closed piece `W` of `U` whose closure contains
`x`, and replace `V` by the integral closed subscheme `Z=closure(W)_red`.
On an affine neighborhood of `x`, `W` contains a dense principal open
`D(f)` with `f!=0`.  In the local domain at `x`, prime avoidance and a
maximal chain of primes avoiding `f` produce a height `dim(Z)-1` prime; its
closure is an integral one-dimensional subscheme through `x` and is not
contained in `V(f)`.  Normalize that curve and choose a point above `x`.
The local ring at that point is a one-dimensional normal noetherian local
domain, hence a DVR, and its generic point lies in `W subset U`.  `square`

The lemma is applied only after base change to the algebraic closure.  It is
an algebraic specialization statement, not an appeal to numerical or
analytic curve sampling.

## 5. The Gaussian fibre and its three entrances

Base-change to `k=Kbar`.  At `F_0`, the transported construction is exactly
the `GLD74` literal-Delta system.  The predecessors give:

1. `GLD74` proves `(Y_aff)_(F_0)=empty` by exact unit identities.

2. `GLD79` proves that the reduced boundary fibre of `Ybar` consists of
   exactly the three reduced `GLD77` sign points `p_-`, `p_+`, and `p_x`,
   with first-column slopes

   ```text
   (-1,1), (1,-1), (-1,-1).                            (18)
   ```

   It also proves that the homogeneous map `K_(0,F_0)` is injective, so its
   output is nonzero at every projective boundary point.

3. Because the leaf frames are equal, the transported nuisance map, complete
   legal response, kernel bundle, and quotient are leaf-`S_3` equivariant.
   Reynolds-average the affine section `beta_0(F)` and use the regular
   invariant kernel frame selected by `beta` in (1).  For each point in (18),
   the `GLD78` formula defines a regular augmented `9 x 9` determinant

   ```text
   delta_j(F,a,b)=det([Phi_(F,a,b)|_triv | w_(F,a,b)]_(J_j)). (19)
   ```

   Its exact value at `(F_0,p_j)` is the corresponding nonzero `GLD78`
   value.  This is the corrected moving literal-Delta continuation of the
   base certificate; it is not a fixed-coordinate three-column assertion.

## 6. Survivor-open theorem

### Theorem 6.1 (existential principal-open nonextension)

There is an element `delta in A` such that

```text
delta(F_0)!=0                                           (20)
```

and, for every geometric point `F in D(delta)`, every raw coefficient
preimage of `T(F)` fails the legal `q_0` first-response condition required by
a shared ten-mode GHZ graph.

#### Proof

Suppose `C_(F_0)` contained a closed point `x`.  By the affine `GLD74`
exclusion it has `s(x)=0`; by `GLD79` it is one of the three points `p_j`.
Lemma 4.1 supplies a DVR trait in `C` whose closed point is `p_j` and whose
generic point lies in `Y_aff`.

Choose a projective raw coordinate nonzero at `p_j` and an output row `rho`
with `(K_(0,F_0)t)_rho(p_j)!=0`.  Both remain units in the DVR.  The correct
regular proportionality slopes along the whole trait are

```text
a=(mathcal Z_1)_rho/(mathcal Z_0)_rho,
b=(mathcal Z_2)_rho/(mathcal Z_0)_rho.                 (21)
```

They specialize to (18).  The minors in (14) imply the complete first-column
proportionality equations with these slopes.  Hence the determinant (19) has
nonzero residue and is a DVR unit.  Reynolds projection of the complete raw
equation then gives the `GLD78` invariant `8+1` column system; invertibility
of (19) forces its homogenizing coefficient `s` to vanish in the DVR.  This
contradicts the generic point's membership in `D_+(s)`.  Therefore

```text
C_(F_0)=empty.                                         (22)
```

The proper image `E=pi(C)` is closed in `B` and misses `F_0`.  Since
`B=Spec A`, its ideal contains an element `delta` outside the maximal ideal
of `F_0`; then `E subset V(delta)` and (20) holds.  Thus `Y_aff` is empty over
`D(delta)`.  Lemma 2.2 says every legal first-response lift would produce a
point of `Y_aff`, so none exists there.  `square`

## 7. Exact residual obligation, verification, and hostile controls

The exceptional set is contained in the proper closed image

```text
E=pi(closure(Ybar intersect D_+(s))) subset B.          (23)
```

The next exact computational obligation is to eliminate `[t:s]` from

```text
(I_2[mathcal Z_0 mathcal Z_1 mathcal Z_2]:s^infinity)  (24)
```

and exhibit a base polynomial nonzero at `F_0`, or give a finite exact
base-divisor cover.  The divisor may not be discarded or called empty.

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_survivor_existential_principal_open_first_response_nonextension.py
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_universal_module_reduction.py
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py
```

The primary replays the exact `GLD74`, `GLD78`, and `GLD79` computational
premises.  The universal verifier separately checks the actual nuisance,
complete response, raw-coordinate, and target intertwiners at the Gaussian
specialization.  Regular frame transport, the matching partition, rank
argument, saturation, DVR selection, and proper-image step are the
mathematical bridge proved above; they are not reported as CAS elimination.
The no-import audit does not independently replay the `GLD79` standard-block
determinant cover, and that limit remains explicit.

Hostile controls:

- `GLD72` is the centre of the excluded open, not contradicted as a concise
  GHZ survivor;
- the `GLD70` epsilon generator is never used as a GHZ-membership test;
- the moving construction transports the actual interface and specializes
  exactly to the `GLD74` `65 x 3` quotient;
- the fixed-coordinate legal incidence remains the full `GLD76` `68 x 4`
  lift system; the smaller moving system is used only after literal-Delta
  conjugation and only as a necessary condition;
- the kernel frame, quotient, invariant section, and obstruction determinants
  all move, with `Omega`, `theta`, `gamma`, and `beta` named as units;
- the intrinsic minors retain every proportionality chart and rank drop;
- the strict closure is saturated by `s`, and the trait slopes use the full
  homogenized columns, not merely their boundary terms;
- every characteristic-zero field extension and DVR trait is covered;
- frame nonuniqueness is handled inside the certified gauge and by the exact
  intertwiners (4);
- no fixed-star local theorem is promoted to another component, a source
  theorem, graph witness, counterexample, or global resolution.
