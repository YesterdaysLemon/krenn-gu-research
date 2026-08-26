# Four-root torus-star survivor locus: symmetry and local-germ reduction

## Status

**Exact complex local survivor-germ theorem and parent-level route
correction.**  Let `N_star` be the fixed rank-`44` nuisance space of `GLD70`
on its fully supported, nonisotropic rank-two maximal torus-star interface,
and let `T_0` be the concise Gaussian GHZ tensor of `GLD72`.  At `T_0`, the
survivor scheme

```text
S_star = N_star intersect GHZ_3
```

is smooth of dimension `5`.  The identity component of the local-basis
stabilizer of `N_star` consists only of the four factor scalars and has a
one-dimensional orbit on tensors.  Hence the survivor germ has **four genuine
directions transverse to interface-preserving scaling**.  Symmetry transport
of the pointwise `GLD74` certificate therefore cannot prove the parent
survivor-locus proposition.

On an explicit frame gauge containing `T_0`, the full survivor germ equals
the germ in which the three leaf frames are equal.  A bidirectional exact
ideal certificate over `Q(i)`, followed by a rank-`10` Jacobian check, proves
this statement; it is not inferred from tangent equality alone.

This theorem does **not** prove first-response nonextension away from `T_0`,
produce a principal-open response certificate, cover every component of
`S_star`, integrate a source presentation, certify maximum root order, or
resolve Krenn--Gu.  `GLD74` still excludes the entire affine `35`-dimensional
raw fibre only over the single tensor `T_0`.  The global conjecture remains
**UNRESOLVED**.

The predecessor is the
[`GLD74` full coefficient-fibre theorem](FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_FULL_COEFFICIENT_FIBRE_FIRST_RESPONSE_NONEXTENSION_THEOREM.md).

## 1. Fixed interface and exact point

Use the canonical `GLD70` data

```text
xi=(1,1,1,-1),                 eta=(1,1,1,1),
h=1,
N_star=im(b),                  b:C^79 -> C^81,
rank b=44.                                                   (1)
```

All `1+24+54=79` columns of `b` are retained.  Exact left reduction gives a
`37 x 81` annihilator `W` with

```text
W b=0,                         rank W=37.                    (2)
```

The `GLD72` frames are

```text
G = [1  1    1  ]        A = [-2-2i  -1+2i   3]
    [0  0   1+i ]            [ 0     -3+3i   0]
    [0  1    1  ]            [ 0     -1+2i   1],             (3)
```

with `det G=-1-i` and `det A=12`.  Put

```text
T_0=(A tensor G tensor G tensor G) Delta_4.                  (4)
```

The verifier reconstructs (1)--(4) from the owning `GLD70--GLD72`
definitions and checks `W T_0=0`.  Thus this calculation retains the exact
hostile survivor; it never reasserts `N_star intersect GHZ_3=empty`.

## 2. Interface-preserving symmetry

Let

```text
G_N={ (M_0,M_1,M_2,M_3) in GL_3(C)^4 :
      (M_0 tensor M_1 tensor M_2 tensor M_3)N_star=N_star }. (5)
```

For each of the `36` matrix-unit infinitesimal local changes, apply it to an
exact `44`-column basis of `N_star` and reduce the result by `W`.  The resulting
linear system has rank `32`, so

```text
dim Lie(G_N)=4.                                             (6)
```

Its kernel is exactly the span of the four factor identity matrices.  Since
the four factor-scalar torus is contained in `G_N`, (6) proves

```text
(G_N)^0=(C^*)^4.                                           (7)
```

The induced orbit tangent at `T_0` is the single tensor-scaling line:

```text
dim T_(T_0)((G_N)^0 T_0)=1.                                (8)
```

The complete canonical interface also has the following checked discrete
symmetries:

- the six permutations of the three equal-sign root coordinates, with their
  induced changes in all four port bases;
- the six permutations of the three leaf ports and tensor modes.

Each preserves the complete `79`-column space.  The root permutations give
six projective tensor lines through the orbit of `T_0`; leaf permutations fix
`T_0` because its three leaf frames are equal.  This is a verified physical
subgroup, not a claim that the finite component group of `G_N` has been fully
classified.

The root-diagonal and residual rescalings used in `GLD70` to choose the
canonical representatives are presentation gauges.  Once (1) and all port
bases are fixed, any continuous gauge that acts on tensor coordinates and
preserves the complete interface lies in (5), so (6)--(7) leave no hidden
continuous direction beyond factor scalars.  Frame column rescalings whose
four colourwise products are one instead stabilize `Delta_4`; they are the
`9`-dimensional frame nonuniqueness treated below and do not enlarge a tensor
orbit.

## 3. Survivor tangent and frame gauge

The infinitesimal `GL_3^4` action on `T_0` has

```text
rank 27,                         kernel dimension 9.         (9)
```

Thus it is the tangent space to the concise GHZ orbit.  Imposing the `37`
linear equations from `W` gives

```text
dim( N_star intersect T_(T_0)GHZ_3 )=5.                    (10)
```

Combining (8) and (10), the quotient tangent has dimension four.  In
particular, the interface-preserving orbit cannot be open in the survivor
germ.

For an integrated calculation, use the principal frame open

```text
delta_gauge=product_(u=1)^3 product_(c=0)^2 (F_u)_(0,c) !=0. (11)
```

It contains (3).  The `9` colourwise column-rescaling stabilizers of
`Delta_4` uniquely normalize the first row of every leaf frame to
`(1,1,1)`, with the compensating factors absorbed in the centre frame.  The
resulting gauge has `27` variables: nine centre entries and the two lower
rows of each leaf frame.  Its `37` incidence equations are

```text
W T(F)=0.                                                   (12)
```

At (3), the Jacobian of (12) has rank `22`; its kernel therefore reproduces
the five-dimensional tangent (10).  No determinant or response minor is
divided out.  Frame invertibility and the fixed fully supported,
nonisotropic interface remain open conditions in a neighborhood of the
basepoint.

## 4. Bidirectional ideal certificate

Inside (12), impose equality of the three normalized leaf frames.  Write the
fifteen shifted variables in the order

```text
x0,...,x8      = centre-frame entries, row-major;
x9,...,x14     = common-leaf rows 1 and 2, row-major.       (13)
```

The `37` shifted incidence polynomials include eleven displayed zeros.  The
stored certificate gives ten polynomials `g_0,...,g_9` and sparse polynomial
matrices

```text
P: 37 x 10,                       27 nonzero terms,
Q: 10 x 37,                       63 nonzero terms,          (14)
```

such that, as exact identities over `Q(i)`,

```text
g = f P,                           f = g Q.                  (15)
```

Consequently the ten stored polynomials and all `37` equal-leaf incidence
polynomials generate the same ideal.  Their Jacobian has rank `10` at the
origin.  The equal-leaf incidence is therefore smooth of dimension

```text
15-10=5,                                                     (16)
```

with the implicit-function coordinates

```text
x6, x8, x12, x13, x14.                                     (17)
```

These are respectively two centre third-row shifts and the three common-leaf
third-row shifts.  Tensor scaling is one tangent combination among the five;
the other four quotient directions are not removed.

The canonical LF-serialized certificate is `15040` bytes and has SHA-256

```text
05a2540431023b7add3d3ae60189cac31ebd375609911cfdc66b8c4028346b57. (18)
```

### Theorem 4.1 (local survivor germ)

On the gauge open (11), the full survivor incidence germ at (3) is smooth of
dimension `5` and equals its equal-leaf subincidence germ.

#### Proof

Let `X` be the full gauge incidence (12), and let `Y` be its closed
equal-leaf subincidence.  Equation (16) proves that `Y` is smooth of local
dimension five.  Since `Y` is contained in `X`, the local dimension of `X`
is at least five.  The tangent calculation (10)--(12) bounds it above by
five.  Thus the embedding dimension and local dimension of `X` are both
five, so the local ring of `X` is regular and in particular a domain.  The
closed germ `Y` has the same local dimension, so its defining ideal in that
domain has height zero and is zero.  Hence `X` and `Y` have the same germ.
The gauge map has differential rank `27` by (9), so this also gives the
five-dimensional tensor survivor germ at `T_0`.  `square`

The use of (15), rather than tangent equality by itself, is load-bearing:
it proves that the five equal-leaf directions integrate and supplies the
smooth closed germ needed in the dimension argument.

## 5. Consequence for the parent response incidence

`GLD74` is the specialization of the desired universal response incidence at
the origin of (17).  Theorem 4.1 proves that a local universal calculation
cannot be compressed to the interface orbit.  After quotienting overall
tensor scaling, it must retain four survivor parameters, together with the
complete `35`-dimensional raw kernel in

```text
alpha(F,t)=alpha_0(F)+sum_(j=0)^34 t_j k_j.              (19)
```

The correct next exact object is therefore the denominator-free incidence

```text
b alpha=T(F),                 D_q0(alpha)L=R(F),          (20)
```

on the four-parameter local survivor germ, or an equivalent parametric
Fitting/quotient system.  Any leading coefficient used in a parametric
syzygy lift must be collected in an explicit exceptional polynomial
`delta`; `delta=0` remains a named branch.

An exploratory direct lift of the unchanged `GLD74` sparse multipliers along
an exact nonscalar survivor curve, and a separate rank-seven Schur-complement
expansion, did not finish within their bounded exact runs.  They provide no
positive or negative mathematical evidence and are not part of this theorem.
No isolated survivor point was promoted.

## 6. Verification and independence

Run the portable primary verifier:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py
```

Run the no-import independent audit in isolated mode:

```powershell
python -I claims/arbitrary-order/audit_four_root_torus_star_survivor_locus_symmetry_and_local_germ_reduction.py
```

Both routes independently construct the `79` permanent columns, the rank-44
nuisance space, the `37` annihilators, the stabilizer constraints, the GHZ
action, and the two incidence Jacobians.  The primary uses the owning
repository definitions and SymPy.  The audit imports neither repository code
nor third-party packages: it implements Gaussian-rational arithmetic,
permanents, elimination, sparse polynomial arithmetic, and certificate replay
directly.  Both verify (15) in both directions and obtain (18).

The optional producer
[`generate_four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.py`](generate_four_root_torus_star_survivor_locus_symmetry_and_local_germ_certificates.py)
uses Singular only to regenerate (14).  The durable proof is the explicit
certificate plus the portable replays, not a CAS status line.

## 7. Scope ledger and hostile controls

- **GLD72:** retained exactly; it is the basepoint of a smooth
  five-dimensional survivor germ.
- **GLD70 `Q` generator:** no epsilon-only inference is used.  Membership is
  imposed by all `37` exact annihilator equations.
- **GLD74:** its exact `65 x 3` quotient and three-chart full-raw-fibre
  exclusion remain the required specialization at `T_0`; nothing here
  weakens or globalizes it.
- **Frame nonuniqueness:** the continuous `9`-dimensional stabilizer is fixed
  on (11); the colour permutations are finite and do not alter the local
  dimension.
- **Divisors:** only the explicit gauge open (11) is used.  Its complement is
  not discarded from a global theorem because this theorem is local at a
  point where `delta_gauge=1`.  No response, determinant, support, or chart
  minor is inverted.
- **Interface covariance:** (5) preserves the full `79`-column nuisance
  space.  The result deliberately makes no covariance claim for the legal
  source-response map beyond `GLD74`.
- **Global scope:** no source attachment, maximum-root bridge, non-star
  profile, other root order, or global graph conclusion follows.

The accepted advance is an exact obstruction to symmetry compression and an
exact minimal local parameter reduction for the requested parent theorem.
It is not the parent response-nonextension theorem itself.
