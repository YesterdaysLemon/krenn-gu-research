# Hafnian jet lines split into projective reconstruction and one affine amplitude

## Status

**Exact arbitrary-even-order characteristic-zero theorem, P7 specialization,
and sharp GHZ boundary.**  Let a common scalar line of candidate hafnian jets
be

```text
(h,c,D)=t(h_0,c_0,D_0),              t!=0,             (1)
```

on `q=2m` named residual vertices.  On `det D_0!=0`, the graph reconstructed
from the first two cofactor decks is independent of `t`.  Every nonlinear
Hessian-deck equation becomes affine-linear in `t` after one common
homogeneous factor is removed, while the scalar Euler stress is independent
of `t`.  Consequently a nonzero radial jet line meets the physical hafnian
jet image in at most one point on the Hessian open.

For P7, apply this theorem to each of the nine eight-vertex nonroot shores.
Hessian determinants, scalar stresses, and overlap descent are projective
tests on the target-incidence line.  The four-deck realization equations
must all select one common nonzero target amplitude.  A legal local
`GL(3)^5` change that diagonalizes a torus-concise rank-three tensor leaves
the named cofactor line unchanged, and therefore cannot change any of these
outcomes.

Two exact controls make the remaining boundary sharp.

1. The all-one nine-vertex graph has

   ```text
   h_4=3,             h_6=15,             h_8=105,    (2)
   ```

   and lies in the common nine-shore Hessian open.  An injective **ambient**
   sensor can send this physical deck to the full diagonal GHZ tensor with a
   one-dimensional target intersection.  Thus tensor rank, sensor
   injectivity, and target incidence alone cannot force Hessian singularity
   or failure of integrability.  This sensor is not asserted to have legal
   permanental companion form.
2. For the committed explicit **legal** rank-219 sensor, the same all-one
   physical deck maps to a tensor whose `(roots 0,1)|(roots 2,3,4)`
   flattening has rank nine.  A named `9 x 9` integer minor is

   ```text
   -18494220325114867735328060700 != 0.                (3)
   ```

   Hence legal full-sensor observability plus the common physical Hessian
   open does not imply border-GHZ incidence.

Neither control is a Krenn--Gu witness.  It remains unknown whether a legal
P7 target-incidence line meets the common Hessian-open physical deck image.
No graph, support, tensor decomposition, parameter family, or finite field is
searched.

The complete open-jet representability theorem used below is proved in
[`RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md`](RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md).
The legal P7 sensor and its named companion blocks are fixed in
[`P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md`](P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md).

## 1. Arbitrary-order radial homogeneity

Let `Q` have order `q=2m>=4`, let

```text
E=binom(Q,2),                    N=|E|=binom(q,2),     (4)
```

and let `(h_0,c_0,D_0)` be candidate scalar, two-deletion, and
four-deletion data.  Assume that `D_0` has the hafnian-Hessian linear shell:
it is symmetric, vanishes on intersecting edge pairs, and assigns the same
entry to the three pairings of each four-set.  Put

```text
delta_0=det D_0,
b_0=(m-1) adj(D_0)c_0.                                (5)
```

For the point `(h_t,c_t,D_t)=t(h_0,c_0,D_0)`, define `delta_t,b_t` in the
same way.  Direct homogeneity gives

```text
D_t=tD_0,                 c_t=tc_0,       h_t=th_0,
delta_t=t^N delta_0,
adj(D_t)=t^(N-1) adj(D_0),
b_t=t^N b_0.                                      (6)
```

### Theorem 1 (projective-affine separation on a hafnian jet line)

Assume `delta_0!=0`.  Then:

1. the only graph candidate reconstructed from any nonzero point of the
   line is the scale-independent edge vector

   ```text
   a=(m-1)D_0^(-1)c_0=b_0/delta_0;                    (7)
   ```

2. for every disjoint pair of edges `e,f`, the determinant-cleared
   Hessian-deck equation at `t(h_0,c_0,D_0)` is equivalent to

   ```text
   t delta_0^(m-2) (D_0)_(e,f)
      =haf(b_0[Q minus (e union f)]);                  (8)
   ```

3. the scalar Euler stress at that point is equivalent to the projective
   equation

   ```text
   m delta_0 h_0
      =(m-1)c_0^T adj(D_0)c_0;                        (9)
   ```

4. the line contains at most one nonzero physical hafnian jet.

Subject to the linear shell, a nonzero point `t(h_0,c_0,D_0)` is a physical
jet if and only if (9) holds and the same `t` satisfies every equation (8).

### Proof

Equation (6) proves (7).  The complete open-jet theorem requires

```text
delta_t^(m-2) (D_t)_(e,f)
 =haf(b_t[Q minus (e union f)]).                      (10)
```

The left side of (10) is

```text
t^(N(m-2)+1) delta_0^(m-2)(D_0)_(e,f),               (11)
```

while the order-`q-4` hafnian on the right has degree `m-2` in `b_t` and is

```text
t^(N(m-2)) haf(b_0[Q minus (e union f)]).             (12)
```

Dividing the common nonzero factor proves (8).  In the scalar stress, both
sides acquire exactly `t^(N+1)`, proving (9).

Since `D_0` is invertible, at least one disjoint entry
`(D_0)_(e,f)` is nonzero.  Its equation (8) has a nonzero coefficient of
`t`, so it determines at most one amplitude.  The necessary-and-sufficient
statement is exactly the open-jet integrability theorem after the common
factors have been removed.  This also proves uniqueness.

The result includes `q=4`: then `m-2=0`, the right side of (8) is the empty
hafnian `1`, and the normalization of the otherwise Kneser-shaped Hessian is
still affine rather than projective.

## 2. P7 line equations and nine-shore descent

Let `N_9={0,...,8}` be the nine nonroots and let a target-incidence line be
represented by

```text
w=(w_I: |I| in {4,6,8}),              C=tw.           (13)
```

For `p in N_9`, put `U_p=N_9 minus {p}`.  Define on the 28 edges of `U_p`

```text
c^(p)_e(w)=w_(U_p minus e),
D^(p)_(e,f)(w)=w_(U_p minus (e union f))   if e,f disjoint,
                0                          otherwise,
delta_p(w)=det D^(p)(w),
b^(p)(w)=3 adj(D^(p)(w))c^(p)(w),
a^(p)(w)=b^(p)(w)/delta_p(w).              (14)
```

Here `m=4` and `N=28`.  Under `w -> tw`, the exact exponents are

```text
D^(p) -> tD^(p),             c^(p) -> tc^(p),
delta_p -> t^28 delta_p,
b^(p) -> t^28 b^(p),         a^(p) -> a^(p).          (15)
```

Before cancellation, a nonlinear deck equation has `t^57` on its left and
`t^56` on its right.  After cancellation it is

```text
t delta_p(w)^2 D^(p)_(e,f)(w)
 =haf(b^(p)(w)[U_p minus (e union f)]).               (16)
```

Equivalently, if the four-set remaining after the deletion is `I`, then

```text
t w_I=haf(a^(p)(w)[I]).                               (17)
```

The scalar stress is the projective equation

```text
4 delta_p(w) w_(U_p)
 =3 c^(p)(w)^T adj(D^(p)(w))c^(p)(w).                (18)
```

### Theorem 2 (radial P7 shallow-Hessian descent)

On the common open

```text
product_(p in N_9) delta_p(w) !=0,                    (19)
```

the nonzero point `tw` is the complete `H_4/H_6/H_8` principal deck of one
nine-vertex graph if and only if:

1. every projective scalar stress (18) holds;
2. the graphs (14) agree on all seven-vertex overlaps,

   ```text
   a^(p)|_(U_p intersect U_q)=a^(q)|_(U_p intersect U_q); (20)
   ```

3. one common nonzero `t` satisfies every local equation (16), equivalently
   every equation (17).

There is at most one such nonzero `t`.

### Proof

Theorem 1 applied to each shore proves that (18) and (16) are precisely the
complete local open-jet equations, including the `H_8` scalar.  If the
supplied deck is physical, all recovered shore graphs are restrictions of
the same graph and (20) holds.

Conversely, (20) glues the nine rationally reconstructed graphs to one named
graph `A`.  The common amplitude in (17) makes its complete four-deck equal
to `tw`.  The Hessian Euler identity then makes the supplied six-deck equal
to the genuine six-deck on every shore, and (18) makes each supplied
eight-hafnian genuine.  Every four- and six-set lies in an eight-shore, and
the nine eight-sets are exactly the `U_p`, so the entire tower is physical.
Uniqueness follows from Theorem 1 on any shore.

Thus the exact target-line test separates into:

```text
projective:  nine Hessian opens, nine scalar stresses, overlap descent;
affine:      all four-deck equations select one common target amplitude. (21)
```

No rescaling of a failed projective condition can repair it.  If all
projective conditions pass, the radial target line still contains at most
one physical point.

## 3. What legal GHZ diagonalization preserves

Let `Gamma:K^219 -> (K^3)^(tensor 5)` be a legal full-rank companion map.
For local root changes `g=(g_1,...,g_5)`, legal covariance is

```text
Gamma'=(tensor_i g_i)Gamma.                            (22)
```

If `Gamma(tw)=tau`, then

```text
Gamma'(tw)=(tensor_i g_i)tau.                         (23)
```

The named vector `tw` has not changed.  In particular, if `tau` is
torus-concise of rank three, a legal local basis change can make the right
side diagonal without changing any `delta_p`, reconstructed `a^(p)`, scalar
stress, overlap equation, or affine amplitude equation above.

### Corollary 3 (GHZ normalization cannot move the cofactor line)

For a fixed legal sensor, local diagonalization of a torus-concise tensor
cannot force or remove Hessian singularity and cannot repair or destroy
hafnian-jet integrability.  Those properties belong to the preimage line in
the named companion basis, not to the chosen root coordinate bases.

This statement does not allow an arbitrary `GL(219)` change among companion
labels.  Such a change would mix deletion sizes and destroy the principal
hafnian meanings used in (14).

Consequently the exact unresolved containment is

```text
Gamma^(-1)(torus-concise sigma_3)
 intersect {common Hessian open}
 intersect {projective descent conditions}
 intersect {one common nonzero affine amplitude}.     (24)
```

The mandatory dimension-eight intersection with the border-rank-three
secant closure does not decide (24): it may be contained in the nonconcise
secant boundary, in the Hessian discriminants, or outside the physical deck
image.

## 4. An exact ambient GHZ-compatible Hessian-open control

Let `A_1` be the all-one graph on nine vertices.  On every even subset,

```text
haf A_1[I]=(|I|-1)!!.                                 (25)
```

This gives (2).  On each eight-shore,

```text
D=3 K_8,
spec(K_8)={15 (mult 1), -5 (mult 7), 1 (mult 20)},
det D=3^28 * 15 * (-5)^7 !=0.                         (26)
```

Moreover `c=15*1`, `D*1=45*1`, and therefore

```text
3D^(-1)c=1.                                           (27)
```

All nine shore reconstructions return `A_1`, so every local equation and
overlap condition above holds.

Let `U` be the 219-dimensional named deck space, let `w_1` be this all-one
deck, and put

```text
tau_0=e_0^(tensor 5)+e_1^(tensor 5)+e_2^(tensor 5).   (28)
```

Choose decompositions

```text
U=K w_1 direct-sum U',
Delta=K tau_0 direct-sum Delta',
T=Delta direct-sum H,                    dim H=240.   (29)
```

Since `dim U'=218<=240`, choose an injection `j:U'->H` and define

```text
Gamma_amb(w_1)=tau_0,           Gamma_amb|U'=j.       (30)
```

Then `Gamma_amb` is injective and

```text
im Gamma_amb intersect Delta=K tau_0.                 (31)
```

This is an exact full-support GHZ incidence line whose unique cofactor point
is a physical common-Hessian-open deck.  It proves that no argument using
only injectivity, dimensions, diagonal target incidence, tensor rank three,
or the radial-line structure can force `det D=0` or violate (16)--(20).

The construction is deliberately **ambient**.  Nothing proves that
`Gamma_amb` is generated by root--root and root--nonroot matching companions,
or that it obeys the legal blocker/nonblocker contractions.  It is not a P7
witness.

## 5. A fixed legal sensor sends the same control to border rank at least nine

Now take exactly the legal integer companion blocks in
`P7_FULL_MIXED_ROOT_219_LABEL_SENSOR_AND_PINNED_STAR_GATING_BOUNDARY.md` and
let `Gamma_leg` be their rank-219 sensor.  Form

```text
tau_leg=Gamma_leg(w_1).                               (32)
```

Flatten `tau_leg` with roots `0,1` as the nine row coordinates, ordered

```text
00,01,02,10,11,12,20,21,22,                           (33)
```

and roots `2,3,4` as the 27 column coordinates.  Select the first nine
columns

```text
000,001,002,010,011,012,020,021,022.                  (34)
```

Direct integer evaluation of the matching formulas gives the determinant
(3).  Hence this flattening has rank nine.  Matrix flattening rank is a
lower bound for tensor border rank, so

```text
border-rank(tau_leg)>=9.                              (35)
```

Local `GL(3)^5` changes preserve flattening ranks.  Therefore no legal local
basis change of this fixed sensor/all-one-deck point can turn it into a
three-term diagonal GHZ tensor.

This is the complementary sharp control: the explicit legal sensor open and
the common physical Hessian open meet exactly, but their displayed meeting
point is far from the border-GHZ variety.  It does not say that every other
physical deck for this sensor, or every other legal sensor, has border rank
greater than three.

## 6. Exact frontier

```text
arbitrary-order radial reconstruction is projective:       PROVED;
nonlinear Hessian-deck equations on a line:                 AFFINE IN t;
scalar Euler stress on a line:                              PROJECTIVE;
nonzero physical points per Hessian-open radial line:       AT MOST ONE;
P7 nine-shore projective/affine descent split:              PROVED;
legal local GHZ diagonalization changes named deck line:    FALSE;
ambient GHZ line with physical all-one Hessian-open deck:   CONSTRUCTED;
ambient control is a legal matching companion sensor:       NOT CLAIMED;
committed legal sensor at all-one physical deck:            BORDER RANK >=9;
committed legal sensor has another physical GHZ point:      UNKNOWN;
legal GHZ incidence forces a Hessian discriminant:          UNKNOWN;
legal GHZ incidence violates jet/descent equations:         UNKNOWN;
legal target-incidence line meets common physical open:     UNKNOWN;
P7 nonrestriction and global Krenn--Gu:                     UNRESOLVED. (36)
```

## Replay

```powershell
uv run --with sympy python verify_arbitrary_hafnian_jet_line_projective_affine_separation_and_p7_ghz_boundary.py
python audit_arbitrary_hafnian_jet_line_projective_affine_separation_and_p7_ghz_boundary.py
python -m py_compile verify_arbitrary_hafnian_jet_line_projective_affine_separation_and_p7_ghz_boundary.py audit_arbitrary_hafnian_jet_line_projective_affine_separation_and_p7_ghz_boundary.py
uv run --with ruff ruff check verify_arbitrary_hafnian_jet_line_projective_affine_separation_and_p7_ghz_boundary.py audit_arbitrary_hafnian_jet_line_projective_affine_separation_and_p7_ghz_boundary.py
```

The primary verifier checks the arbitrary exponent ledger, the exact Kneser
determinant and reconstruction on all-one P7 shores, and the named legal
flattening minor using the committed matching operator.  The independent
no-import audit rebuilds the same legal tensor by a separate full-graph
hafnian recurrence, uses an independent Bareiss determinant, and checks the
same integer certificate.  Neither replay searches over graphs, supports,
decompositions, parameters, or finite fields.
