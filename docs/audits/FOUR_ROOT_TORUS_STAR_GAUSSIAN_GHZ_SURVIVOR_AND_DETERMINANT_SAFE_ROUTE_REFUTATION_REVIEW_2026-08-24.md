# Hostile review: four-root torus-star Gaussian GHZ survivor

Date: 2026-08-24

## Verdict

**Accept as an exact counterexample to the fixed-star GHZ exclusion and the
determinant-safe three-word route.**  The displayed Gaussian-rational tensor
lies in the original `GLD70` rank-`44` nuisance space and is an honest concise
three-colour GHZ tensor.  The result therefore changes the live mathematical
frontier: the strong fixed-space separator and its proposed saturation are
refuted, not merely unproved.

It does not construct one legal graph, shared deck family, response system,
source attachment, or the required three-cell weighted coordinate diagonal.
The `GLD70` graph implication is one-way.  This is not a counterexample to the
Krenn--Gu conjecture, whose global status remains **UNRESOLVED**.

Reviewed artifacts:

- [`FOUR_ROOT_TORUS_STAR_GAUSSIAN_GHZ_SURVIVOR_AND_DETERMINANT_SAFE_ROUTE_REFUTATION_THEOREM.md`](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_GAUSSIAN_GHZ_SURVIVOR_AND_DETERMINANT_SAFE_ROUTE_REFUTATION_THEOREM.md);
- [`verify_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py`](../../claims/arbitrary-order/verify_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py);
- [`audit_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py`](../../claims/arbitrary-order/audit_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py);
- the owning [`GLD70` fixed-space reduction](../../claims/arbitrary-order/FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md);
- the [`GLD71` syndrome interface](../../claims/arbitrary-order/FOUR_ROOT_TORUS_STAR_PUNCTURED_SYNDROME_AND_EISENSTEIN_NORM_GATE_THEOREM.md).

## 1. Exact claim under review

With

```text
G = [1  1    1  ]        A = [-2-2i  -1+2i   3]
    [0  0   1+i ]            [ 0     -3+3i   0]
    [0  1    1  ]            [ 0     -1+2i   1],
```

define

```text
T_(r i j k) = sum_(c=0)^2 A_(r c) G_(i c) G_(j c) G_(k c).
```

The reviewed assertion is the conjunction

```text
T in N_star,
det(G)=-1-i,                 det(A)=12,
all four one-mode ranks = 3,
all three balanced ranks = 3,
epsilon(T)=144-144i.
```

These facts imply that `T` is in the concise GHZ orbit and refute

```text
N_star intersect GHZ_3 = empty
```

as well as the `GLD71` implication that an invertible three-leaf frame in the
full syndrome kernel must have singular centre.

## 2. Original-space membership audit

The primary verifier loads the owning permanent construction, rebuilds all
`1+24+54=79` nuisance columns, and checks exact rank `44`.  It uses the pinned
`44` pivot columns to solve for the concrete `81`-coordinate tensor.  The
solution has `37` nonzero coefficients, replays every coordinate exactly, and
leaves the augmented rank equal to `44`.

This direct check is load-bearing.  A zero syndrome alone could be misleading
if the annihilator, puncture, coordinate order, or kernel identification were
wrong.  Here membership is independently checked before the syndrome
interpretation is used.

The standalone audit imports no repository module and uses only exact
standard-library `Fraction` arithmetic in a separately implemented
Gaussian-rational field.  It rebuilds the permanent through a reversed label
and index traversal, reconstructs all `79` columns, obtains rank `44`, and
again obtains augmented rank `44` for the same original `81` coordinates.
It then derives a fresh left nullspace of dimension `37` and checks every
relation against every nuisance column and against `T`.

Thus the result is not an artifact of importing the primary basis, pivots, or
syndrome rows.

## 3. Syndrome and convention audit

Both implementations use root-major vectorization for the `3 x 3` centre
frame.  The primary verifier evaluates the committed `GLD71` relations; the
standalone audit derives its own annihilator from the independently rebuilt
map.  Both obtain

```text
rank M(G,G,G)=7,           nullity=2,
M(G,G,G) vec(A)=0
```

exactly.  Agreement with the direct original-space membership check audits
the puncturing, root/leaf mode order, and centre-vector convention.

## 4. GHZ and invariant audit

The determinant calculations are exact in `Q(i)`.  Because `A` and all three
copies of `G` are invertible, the displayed three-term decomposition has a
basis of local vectors in every mode.  Both implementations nevertheless
compute all four one-mode and all three balanced flattening ranks directly
and obtain `(3,3,3,3)` and `(3,3,3)`.

The primary verifier evaluates the owning full epsilon contraction and the
frame identity.  The standalone audit separately evaluates the full
permutation contraction.  Both give

```text
epsilon(T)=6 det(A) det(G)^3=144-144i != 0.
```

The tensor has exactly `61` nonzero coordinates in the fixed displayed basis.
It is therefore not the three-cell coordinate diagonal being sought at graph
level, even though it is locally equivalent to a diagonal as every concise
GHZ tensor is.

## 5. Hostile attacks and rejected strengthenings

### 5.1 The survivor is only a syndrome false positive

Rejected.  Two independent original-space rank checks give `44/44` before any
syndrome conclusion is drawn.

### 5.2 Balanced rank three is being mistaken for third-secant membership

Rejected.  The displayed formula for `T` is already an explicit sum of three
decomposable tensors.  Invertible local frames prove concision.  The balanced
ranks and epsilon are consistency checks, not the sole secant test.

### 5.3 The calculation is merely numerical or modular

Rejected.  Every entry and elimination step is exact over `Q(i)`.  No floating
point, tolerance, finite-field lift, or external solver output is used in the
accepted claim.

### 5.4 The Gaussian divisor is a complete classification

Rejected as an unsupported strengthening.  The equation
`(z-1)^2+1=0` explains how this point arose from one symmetric vertical
three-word chart.  This package does not claim an exhaustive classification
of the full rank-drop or GHZ-survivor locus.

### 5.5 A nuisance-space survivor is a graph counterexample

Rejected.  `N_star` records a contracted necessary compatibility space.  Its
raw coefficients need not be simultaneously realizable by one legal graph or
one shared source/deck system.  Invertible local changes that diagonalize `T`
also move `N_star` and do not supply graph data.  No reverse integrability
theorem exists here.

## 6. Independence and reproducibility boundary

The primary route deliberately reuses the owning `GLD70`/`GLD71`
implementations, ensuring that the point is checked against the live
definitions.  The no-import route independently implements the Gaussian
field, permanent map, elimination, annihilator, syndrome, flattenings, and
epsilon contraction.  Their shared mathematical specification is unavoidable;
their code, arithmetic representation, basis derivation, and traversal are
separate.

The accepted replay is:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py
```

The required outputs include nuisance/augmented ranks `44/44`, annihilator
dimension `37`, syndrome rank `7`, the two nonzero determinants, local ranks
`(3,3,3,3)`, balanced ranks `(3,3,3)`, epsilon `144-144i`, and support size
`61`.

## 7. Accepted frontier delta

The fixed-space part of the torus-star programme now has a negative answer:

1. the `GLD70` complete map and fixed rank-`44` compression remain proved;
2. the `GLD71` puncture, one-word theorem, and low-degree gates remain proved;
3. fixed-star GHZ exclusion, balanced-minor separation, and determinant-safe
   saturation are refuted by the exact point above;
4. the live universal bridge is the nonlinear comparison between this
   survivor locus and source-integrable nuisance coefficients;
5. residual-boundary, triangle, lower-rank, smaller-survivor, other-root, and
   graph-global coverage remain separate.

The concrete Gaussian point is now a mandatory hostile control for any
proposed source-to-target bridge.  This is a substantial route correction,
not global closure.
