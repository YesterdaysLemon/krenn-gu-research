# Four-root torus-star Gaussian survivor: full coefficient-fibre first-response nonextension

## Status

**Exact fixed-model full-coefficient-fibre first-response nonextension
theorem.**  This is the parent-theorem successor to `GLD73`.  In the literal
diagonal coordinates of that theorem, let

```text
b' : C^79 -> C^81,                 coefficients in Q(i),
F=(b')^(-1)(Delta_4) subset C^79.                      (1)
```

The map has rank `44`, so `F` is an affine `35`-space.  For **every** raw
coefficient vector in `F`, the complete legal-response span at the contracted
vertex `q_0` fails to contain the three-dimensional diagonal response required
by a ten-mode GHZ identity.  Thus the pinned obstruction of `GLD73` was not an
accident of its chosen linear solve: the entire raw fibre of the exact `GLD72`
tensor is excluded at first response in this fixed ten-vertex effective model.

This is not a source-integrability theorem for every presentation of the
`GLD72` point.  It keeps the canonical torus-star roots, transformed port
planes, ten effective vertices, and zero root-root grade-zero values fixed.
It does not exclude the rest of the fixed-star GHZ-survivor locus, certify
maximum root order four, exclude a fifth root, produce a graph witness, or
resolve Krenn--Gu.  The global conjecture remains **UNRESOLVED**.

The predecessor is the
[`GLD73` contracted-edge theorem](FOUR_ROOT_TORUS_STAR_GAUSSIAN_SURVIVOR_CONTRACTED_EDGE_CONTROL_AND_FIRST_TRANSVERSE_NONEXTENSION_THEOREM.md).

## 1. The full affine fibre

Use the exact Gaussian frames

```text
G = [1  1    1  ]        A = [-2-2i  -1+2i   3]
    [0  0   1+i ]            [ 0     -3+3i   0]
    [0  1    1  ]            [ 0     -1+2i   1]
```

and the transformed port maps `P'_u=P_u F_u^(-T)` from `GLD73`.  The complete
raw map has the ordered columns

```text
Q;  h_(xi,u,c);  h_(eta,u,c);  H_(uv,c,d),              (2)
```

with counts `1+12+12+54=79`.  Exact elimination over `Q(i)` gives

```text
rank b'=44,                  dim F=79-44=35.             (3)
```

Choose the pivot set produced by exact left-to-right elimination and write

```text
alpha(t)=alpha_0+sum_(j=0)^34 t_j k_j,    t in C^35,    (4)
```

where the `k_j` are the free-column kernel basis.  Both verifiers replay

```text
b' alpha_0=Delta_4,          b' k_j=0.                  (5)
```

No genericity restriction or sampled specialization is made in (4).

## 2. The complete response at q0

Keep the ten effective vertices

```text
r_0,r_1,r_2,r_3,q_0,q_1,u_0,u_1,u_2,u_3               (6)
```

and the `GLD73` convention

```text
xi=(1,1,1,-1),                 eta=(1,1,1,1),           (7)
q_0--u uses h_eta,             q_1--u uses h_xi.        (8)
```

At `q_0`, the edge to `q_1` contributes one scalar parameter and the four
edges to open ports contribute twelve coordinate parameters.  Their cofactor
columns are exactly

```text
C=(Q column, twelve eta-residual columns).              (9)
```

The four `q_0--r_j` edges contribute four further scalar parameters, with
cofactor columns `R_0(alpha),...,R_3(alpha)`.  Hence the complete legal-response
map is

```text
D_q0(alpha)=[C | R_0(alpha) R_1(alpha) R_2(alpha) R_3(alpha)]
             : Q(i)^17 -> Q(i)^81.                     (10)
```

The domain is complete for first row replacement: five contracted neighbours
give five scalar evaluations and four open neighbours give four arbitrary
three-vectors.  If base-edge constraints correlate or remove any of these
directions in a more restrictive physical lift, the actual response can only
shrink, so using the full space (10) is safe for an exclusion.

Let `pi_mix` retain the `78` non-diagonal four-port words.  Exact elimination
gives

```text
rank C=rank(pi_mix C)=13.                               (11)
```

Quotient `pi_mix R_j` by `im(pi_mix C)`.  A pivot-row complement identifies
the quotient with `Q(i)^65`; write the resulting columns as `Z_j(t)`.  Every
nonzero matching cofactor contains exactly one raw residual-port or port-pair
coefficient, so each `Z_j` is affine-linear in the `35` parameters of (4).
The residual vector (7) gives the exact matrix identity

```text
Z_0(t)+Z_1(t)+Z_2(t)-Z_3(t)=0              for all t.    (12)
```

Put `Z(t)=[Z_0(t) Z_1(t) Z_2(t)]`, a `65 x 3` matrix.

### Theorem 2.1 (rank-one necessity)

If the response (10) contains the three-dimensional diagonal target space,
then

```text
rank Z(t)<=1.                                            (13)
```

#### Proof

By (11) and the definition of the quotient,

```text
rank(pi_mix D_q0)=13+rank Z(t).                         (14)
```

The domain of `D_q0` has dimension `17`, so `rank D_q0<=17`.  The dimension
of the response tensors supported on the three diagonal words is therefore

```text
dim(im D_q0 intersect Diag)
 =rank D_q0-rank(pi_mix D_q0)
 <=17-(13+rank Z(t))
 =4-rank Z(t).                                          (15)
```

A ten-mode GHZ identity, after contracting the other five closed vertices at
`(1,1,1)` and replacing the row at `q_0` by arbitrary
`y=(y_0,y_1,y_2)`, produces all three tensors
`y_0 0000+y_1 1111+y_2 2222`.  Thus its diagonal response has dimension three.
Equation (15) then forces (13).  `square`

## 3. Exact projective rank-one exclusion

The condition `rank Z<=1` has the following exhaustive projective cover.

1. If `Z_0!=0`, there are scalars `a,b` with

   ```text
   a Z_0-Z_1=0,                  b Z_0-Z_2=0.            (16)
   ```

2. If `Z_0=0` and `Z_1!=0`, there is a scalar `b` with

   ```text
   Z_0=0,                        b Z_1-Z_2=0.            (17)
   ```

3. If `Z_0=Z_1=0`, the remaining direction is represented by

   ```text
   Z_0=Z_1=0.                                             (18)
   ```

Each of (16)--(17) consists of `130` affine polynomial equations.  Four are
identically zero in each chart, leaving `126` nonzero ideal generators.
Exact `liftstd` computation over

```text
Q(i)[t_0,...,t_34,a,b],             i^2+1=0             (19)
```

produces the following checked sparse identities:

```text
chart                         multiplier terms   maximum multiplier degree
Z_0!=0                              42                         1
Z_0=0, Z_1!=0                       35                         0. (20)
```

In both charts the stored multipliers sum against the original `130`
generators to exactly `1`.  The identity is already over `Q(i)`, so it remains
a unit identity after scalar extension to `C` and excludes complex parameter
values, not merely Gaussian-rational points.  For (18), the `130 x 35`
coefficient matrix and its augmented matrix have exact ranks

```text
35 and 36,                                                (21)
```

so the affine linear system is inconsistent.  Equations (16)--(18) are an
exhaustive cover, and therefore

```text
rank Z(t)>=2                         for every t in C^35. (22)
```

For provenance, serialize the real and imaginary numerator/denominator pairs
of the `65 x 3 x 36` affine coefficient array in row/column/parameter order.
Its SHA-256 is

```text
17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e. (23)
```

The canonical LF-serialized `2744`-byte sparse certificate has SHA-256

```text
7bb2dc47270a2c2e9b87c722aace298e63a6691a7979d86564425aac760a748f. (24)
```

### Theorem 3.1 (full raw-fibre first-response nonextension)

For every `alpha in F`,

```text
dim(im D_q0(alpha) intersect Diag)<=2.                   (25)
```

Consequently no point of the full `35`-dimensional raw coefficient fibre (1)
can be completed through this fixed effective-edge interface to a ten-mode
GHZ identity.

#### Proof

Equation (22) inserted into (15) gives (25).  The target response has
dimension three, so the same contraction-and-row-replacement argument as in
Theorem 2.1 excludes every point of (1).  `square`

## 4. Verification and independence

Run the portable primary replay:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py
```

Run the independent standard-library audit in isolated mode:

```powershell
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py
```

The primary reconstructs the live `GLD72`/`GLD73` map, performs one exact
Gaussian row reduction, derives the matching-cofactor map, and checks the
stored identities with SymPy polynomials over `Q(i)`.  The audit imports no
repository module or third-party package; it rebuilds the frames, permanent
map, affine quotient, and sparse identities with a separately implemented
Gaussian field and reversed polynomial variable order.

The optional generator requires Singular 4.x:

```powershell
python claims/arbitrary-order/generate_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension_certificates.py
```

It checks the `liftstd` identities inside Singular before writing the durable
certificate.  Singular is not required for either replay.

## 5. Exact scope boundary and frontier delta

This theorem proves:

```text
one pinned GLD72 preimage has contracted edge control:          YES (GLD73),
every raw preimage of that tensor fails q0 first response:      YES (GLD74),
the whole fixed-star GHZ-survivor locus is excluded:             NO,
every source/graph presentation of the GLD72 point is excluded: NO,
maximum root order four / no fifth root is certified:           NO,
a graph witness or Krenn--Gu counterexample is constructed:     NO,
global Krenn--Gu conjecture:                                    UNRESOLVED.
```

The next parent target is no longer another point of the same affine fibre.
Useful progress must either globalize the response obstruction across the
fixed-star GHZ-survivor locus, prove that every relevant source presentation
lands in this effective model, or route the universal maximal-root problem
through an equally complete non-star/interface cover.  Another isolated raw
preimage calculation would not advance this boundary.
