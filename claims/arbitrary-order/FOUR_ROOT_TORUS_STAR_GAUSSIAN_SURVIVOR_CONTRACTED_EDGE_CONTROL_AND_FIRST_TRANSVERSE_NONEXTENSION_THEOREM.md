# Four-root torus-star Gaussian survivor: contracted edge control and first-transverse nonextension

## Status

**Exact single-fibre contracted-edge realization and pointwise first-transverse
nonextension theorem.**  This is a successor to the `GLD72` Gaussian survivor.
After the four open-port bases are changed so that the survivor becomes the
literal three-colour diagonal `Delta_4`, one pinned preimage under the complete
`79`-column torus-star map is realized by the contraction of one ten-vertex
edge array.  Thus that preimage passes the complete grade-zero boundary-edge
control; it is not merely a formal vector in the rank-`44` nuisance space.

The same effective edge data cannot be completed to a ten-vertex GHZ graph.
At each of the six contracted vertices, the complete first-transverse response
has only the line `C Delta_4` in the three-dimensional diagonal four-port
space.  A GHZ extension would require all three diagonal directions.

This excludes **one pinned raw-coefficient preimage**, including every choice
of the unused rows of its edge matrices.  It does not exclude the other points
of the `35`-dimensional affine preimage of `Delta_4`, certify that the displayed
four roots form a maximum root, exclude a fifth root, or produce a graph
witness.  It is not a counterexample to Krenn--Gu.  The global conjecture
remains **UNRESOLVED**.

**Successor notice (2026-08-24).**  `GLD74` discharges the parent obligation
left here: one exact `q_0` quotient and a complete projective rank-one cover
exclude every point of the full `35`-dimensional raw fibre at first response.
That successor remains fixed-model only; whole-locus, source-presentation,
maximum-root, fifth-root, and global obligations stay open.

The fixed space and raw coefficient order are those of the
[`GLD70` complete-Q-layer theorem](FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md),
and the exact survivor is the point in the
[`GLD72` route-refutation theorem](FOUR_ROOT_TORUS_STAR_GAUSSIAN_GHZ_SURVIVOR_AND_DETERMINANT_SAFE_ROUTE_REFUTATION_THEOREM.md).

## 1. Equivariant pullback to the literal diagonal

Let

```text
G = [1  1    1  ]        A = [-2-2i  -1+2i   3]
    [0  0   1+i ]            [ 0     -3+3i   0]
    [0  1    1  ]            [ 0     -1+2i   1],

F_0=A,                       F_1=F_2=F_3=G,
S_u=F_u^(-1).                                             (1)
```

The `GLD72` tensor is

```text
T=(F_0 tensor F_1 tensor F_2 tensor F_3) Delta_4,
Delta_4=sum_(c=0)^2 e_c tensor e_c tensor e_c tensor e_c. (2)
```

Write the canonical torus-star port map at mode `u` as a `4 x 3` matrix
`P_u`, with the local coordinate indexing its columns.  Put

```text
P'_u=P_u F_u^(-T).                                      (3)
```

Then each `P'_u` still has rank three and spans the same root-side port plane
as `P_u`.  The tensor and port transformations use the same convention:

```text
(S_0 tensor S_1 tensor S_2 tensor S_3)T=Delta_4.         (4)
```

For a raw coefficient vector

```text
alpha=(q, (h_(rho,u)), (H_(uv))),
rho in {xi,eta},       h_(rho,u) in C^3,
H_(uv) in Mat_(3 x 3)(C),                                (5)
```

the corresponding coefficient transformation is

```text
q'=q,
h'_(rho,u)=S_u h_(rho,u),
H'_(uv)=S_u H_(uv) S_v^T.                               (6)
```

Equations (3) and (6) transform each of the `1+24+54=79` raw columns
covariantly.  In particular, let `alpha_*` be obtained by solving the original
`GLD72` tensor in the committed `GLD70` pivot basis, setting all nonpivot raw
coefficients to zero, and then applying (6).

### Theorem 1.1 (exact pinned diagonal preimage)

For the transformed complete map `b'` determined by `P'_u`,

```text
b'(alpha_*)=Delta_4.                                    (7)
```

The original pinned vector has `37` nonzero entries.  The transformed vector
has `52` nonzero entries, split as

```text
Q / residual-port / port-pair = 1 / 24 / 27.            (8)
```

Using numerator/denominator pairs for the real and imaginary parts of all
`79` entries in raw-label order, separated by newlines, its canonical SHA-256
is

```text
4d227cac41d64bef66d062ffb6a052a12aa11e9c648ddbb59d8c27040c357f0a. (9)
```

#### Proof

The original pinned solve replays `T` in all `81` coordinates.  Applying the
four inverse frame maps gives (4).  Direct substitution of (3) and (6) into
the permanent definition of every raw column gives (7).  The counts and hash
in (8)--(9) are then exact Gaussian-rational arithmetic.  The primary checker
and the independent no-import audit replay the complete calculation.
`square`

## 2. One physical contracted-edge fibre

Use ten labelled vertices

```text
C={r_0,r_1,r_2,r_3,q_0,q_1},       U={u_0,u_1,u_2,u_3}. (10)
```

The vertices in `C` are contracted at the fully supported vector
`x=(1,1,1)`.  The vertices in `U` remain open.  Let

```text
xi=(1,1,1,-1),                    eta=(1,1,1,1)          (11)
```

be the canonical residual vectors.  Define the effective edge evaluations by

```text
E_(r_i,r_j)=0,
E_(r_i,q_0)=xi_i,                 E_(r_i,q_1)=eta_i,
E_(r_i,u_a)(c)=P'_a[i,c],
E_(q_0,q_1)=q',
E_(q_0,u_a)(c)=h'_(eta,a)[c],
E_(q_1,u_a)(c)=h'_(xi,a)[c],
E_(u_a,u_b)(c,d)=H'_(ab)[c,d].                         (12)
```

The `xi/eta` interchange in the two residual-port lines is essential.  When
`q_0` is paired directly to a port, `q_1` remains in the complementary
permanent and contributes `eta`; the other line is analogous.

### Theorem 2.1 (complete grade-zero contracted-edge control)

The perfect-matching tensor of (12), after contracting the six vertices in
`C` at `x`, is exactly

```text
Delta_4.                                                (13)
```

Every effective value in (12) is realized by an independent `3 x 3` graph
edge matrix.  Thus (13) is one honest ten-vertex boundary-edge contraction,
not only a nuisance-space membership statement.

#### Proof

There are

```text
9!!=945                                                 (14)
```

perfect matchings of ten labelled vertices.  Enumerating all of them with
(12) gives coefficient one at `0000`, `1111`, and `2222`, and zero at the
other `78` port words.  This is also a direct graph interpretation of (7):
because every surviving matching contains exactly one edge among the raw
`Q`, residual-port, and port-pair labels, the contracted tensor is linear in
the `79` entries of `alpha_*`.

For realizability, evaluation of an arbitrary edge matrix against
`x=(1,1,1)` is onto the required scalar or three-vector row space.  Distinct
labels use distinct edges, so these choices impose no cross-edge relation.
For example, putting the desired row in colour row zero and setting colour
rows one and two to zero realizes every contracted-to-open covector; a single
`(0,0)` entry realizes a contracted-to-contracted scalar.  `square`

This last row-zero construction is deliberately not a global witness.  At
the global all-colour-one word every matching has a zero incident edge, so
its coefficient is `0`, whereas the GHZ coefficient would be `1`.

## 3. The complete first-transverse response

Fix `v in C`.  Remove `v` and one of its nine neighbours from a matching and
evaluate the remaining four-edge matching on the other five contracted
vectors.  The possible replacement row at `v` has one scalar for each other
contracted vertex and one three-vector for each open port.  This defines

```text
D_v : C^17 -> (C^3)^(tensor 4),
C^17 = C^5 direct-sum (C^3 direct-sum C^3 direct-sum C^3 direct-sum C^3).
                                                               (15)
```

Let `Diag` be the three-dimensional coordinate-diagonal subspace and let
`pi_mix` retain the `78` non-diagonal port coordinates.

The domain in (15) is complete.  For a direction `y` independent of the base
vector `x`, an incident `3 x 3` edge matrix with its `x`-evaluation fixed can
give an arbitrary `y`-evaluation.  The nine incident edges are independent.
Thus every first derivative of every edge-matrix lift of (12) lies in
`Im D_v`, and no legal first-row direction has been omitted.

### Theorem 3.1 (pointwise first-transverse nonextension)

For all six contracted vertices, exact elimination over `Q(i)` gives

```text
v                         rank D_v   rank(pi_mix D_v)   difference
r_0,r_1,r_2,r_3,q_0,q_1      17             16              1.     (16)
```

Consequently,

```text
Im D_v intersect Diag = C Delta_4                  for every v in C. (17)
```

No completion of the unused edge-matrix rows in (12) can make the resulting
ten-vertex graph tensor equal the literal ten-mode GHZ tensor.

#### Proof

The rank difference in (16) is the dimension of the kernel of `pi_mix`
restricted to `Im D_v`, hence the dimension of `Im D_v intersect Diag`.
The base incident row belongs to the domain of (15), and its exact replay is
the contraction (13).  Therefore the one-dimensional intersection contains
`Delta_4` and is exactly the line in (17).

Suppose an edge-matrix completion gave the ten-mode GHZ identity.  Contract
the other five vertices of `C` at `x=(1,1,1)` and replace the vector at `v`
by an arbitrary `y=(y_0,y_1,y_2)`.  The target slice would be

```text
y_0 e_0^(tensor 4)+y_1 e_1^(tensor 4)+y_2 e_2^(tensor 4), (18)
```

whose image as `y` varies is all of `Diag`.  The graph-side slice is a first
row replacement and therefore lies in `Im D_v`.  Equation (17) makes the
three-dimensional image in (18) impossible.  This contradiction works at
each of the six vertices.  `square`

## 4. Exact scope boundary

Let

```text
F=(b')^(-1)(Delta_4).                                  (19)
```

Since `b'` has rank `44`, `F` is an affine `35`-space inside `C^79`.
Theorems 2.1 and 3.1 concern the single pinned point `alpha_* in F`.  Changing
`alpha_*` within `F` changes the complementary matching cofactors and hence
the maps `D_v`.  The rank calculation at `alpha_*` is not fibre-invariant by
assertion, and no such invariance is assumed.

Therefore this package proves:

```text
one GLD72 raw preimage has exact contracted-edge control:       YES,
that entire edge-evaluation fibre has a first-jet GHZ lift:      NO,
every raw preimage of the GLD72 tensor is nonextendable:         OPEN,
the four displayed roots are certified maximum / no fifth root: NO,
a legal graph witness or Krenn--Gu counterexample is constructed: NO,
global Krenn--Gu conjecture:                                    UNRESOLVED.
                                                               (20)
```

The parent obligation left by this theorem is finite and falsifiable.  On
`F`, form the polynomial response maps `D_v(alpha)`.  A global lift requires

```text
rank D_v(alpha)-rank(pi_mix D_v(alpha)) >= 3          for every v in C. (21)
```

`GLD74` closes this obligation more sharply than the provisional six-vertex
saturation: at `q_0`, quotienting the thirteen fixed columns reduces the
necessary condition to one `65 x 3` affine matrix of rank at most one.  A
complete three-chart projective cover proves that locus empty on all of `F`,
including response-rank drops.  The remaining parent problem is therefore
globalization across the survivor locus or proof that every relevant source
presentation is forced through this effective interface; another raw point
of this same fibre is no longer an open target.

## 5. Verification

Run the primary exact verifier:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py
```

Run the independent no-repository-import audit:

```powershell
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_contracted_edge_control_and_first_transverse_nonextension.py
```

Both routes reconstruct the frames, transformed raw presentation, physical
edge convention, all `945` perfect matchings, and the six exact response-rank
triples.  The independent route uses a separately implemented Gaussian field,
matching recurrence, elimination, and traversal.

## 6. Frontier delta

Relative to `GLD72`:

- fixed-space membership has been upgraded to exact grade-zero boundary-edge
  control for one pinned raw preimage;
- the same preimage, including every lift of its unused matrix rows, is
  excluded from the full GHZ graph locus by a complete first-transverse test;
- the relevant remaining object is the entire affine `35`-dimensional raw
  preimage, not another representative selected by a linear solve;
- maximum-root certification, higher root orders, non-star atlases, and global
  coverage remain open and unchanged.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
