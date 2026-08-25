# Four-root torus-star Gaussian GHZ survivor and determinant-safe route refutation

## Status

**Exact complex counterexample to the fixed torus-star GHZ-exclusion route.**
This result is a successor to `GLD70` and `GLD71`.  It proves that the fixed
`44`-dimensional torus-star nuisance space `N_star` contains a concise
three-colour GHZ tensor.  Consequently,

```text
N_star intersect GHZ_3 = empty
```

and the determinant-safe three-word implication proposed in `GLD71` are
**false over C**.

This is not a counterexample to the Krenn--Gu conjecture.  Membership in the
contracted nuisance space is a necessary linear compatibility condition, not
a proof that the nuisance coefficients come from one legal graph, shared
decks, responses, and source attachments.  The tensor below is not the
three-cell weighted coordinate diagonal.  Graph/source integrability remains
open, and the global conjecture remains **UNRESOLVED**.

The fixed space is the one constructed in the
[`GLD70` complete-Q-layer theorem](FOUR_ROOT_COMPLETE_Q_LAYER_SECANT_BOUNDARY_TRAP_AND_TORUS_STAR_COMPRESSION_THEOREM.md),
and the syndrome conventions are those of the
[`GLD71` punctured-syndrome theorem](FOUR_ROOT_TORUS_STAR_PUNCTURED_SYNDROME_AND_EISENSTEIN_NORM_GATE_THEOREM.md).

## 1. The exact Gaussian point

Put

```text
G = [1  1    1  ]        A = [-2-2i  -1+2i   3]
    [0  0   1+i ]            [ 0     -3+3i   0]
    [0  1    1  ]            [ 0     -1+2i   1].            (1)
```

Let the three leaf frames all equal `G`, and define

```text
T_(r i j k) = sum_(c=0)^2 A_(r c) G_(i c) G_(j c) G_(k c). (2)
```

Thus (2) is an honest sum of three decomposable four-qutrit tensors.

### Theorem 1.1 (exact fixed-star GHZ survivor)

For the matrices in (1):

```text
det A = 12,
det G = -1-i,
T in N_star,
rank_(u|rest)(T) = 3              for all four modes u,
rank_(uv|rest)(T) = 3             for all three balanced cuts,
epsilon(T) = 144-144i != 0.                              (3)
```

Equivalently, for the full `37 x 9` `GLD71` syndrome matrix,

```text
rank M(G,G,G) = 7,
M(G,G,G) vec(A) = 0,                                  (4)
```

where `vec(A)` is root-major.  In particular, `T` is a concise GHZ tensor
in `N_star`.

#### Proof

The `GLD70` permanent definitions reconstruct the `79` raw nuisance columns
with total rank `44`.  Exact Gaussian-rational elimination expresses the
81-coordinate tensor (2) in a pinned `44`-column basis of that space; adjoining
`T` leaves the rank equal to `44`.  Independently, the punctured annihilator
has dimension `37`, and direct evaluation gives (4).

The two determinants in (3) follow immediately from (1).  Since every local
frame in the displayed decomposition is invertible, the four one-mode and
three balanced flattenings have rank three.  Direct replay of the full cubic
epsilon contraction agrees with the frame formula

```text
epsilon(T) = 6 det(A) det(G)^3 = 144-144i.              (5)
```

This is nonzero, so the `GLD70` epsilon-open-orbit theorem identifies `T` as
a concise GHZ point.  All equalities are replayed exactly by the primary
verifier and by a no-repository-import audit.  `square`

## 2. What is refuted and what survives

Theorem 1.1 refutes both of the following fixed-space targets:

```text
N_star intersect GHZ_3 = empty,                         (6)

det B det C det D != 0 and M(B,C,D) vec(A) = 0
    imply det A = 0.                                    (7)
```

Indeed, take `B=C=D=G` in (7).  The same tensor has every balanced rank equal
to three and nonzero epsilon, so it also refutes the stronger balanced-minor
shortcut proposed in `GLD70`.

The following proved statements remain intact:

- the `GLD70` `79`-column construction, rank-`44` torus-star compression,
  epsilon open-orbit theorem, and one-way graph-level reduction;
- the `GLD71` rank-`21` pair erasure, rank-`23` punctured nuisance code,
  `37`-dimensional syndrome, one-word rank dichotomy, root-slice checks, and
  Eisenstein-norm identities.

Only the attempted three-word exclusion and the fixed-space route built on
it are refuted.

## 3. Conceptual origin and the new bridge

The leaf columns in (1) are

```text
g_0=(1,0,0),   g_1=(1,0,1),   g_2=(1,1+i,1).           (8)
```

The first two lie on the exceptional vertical fibre of the diagonal
one-word syndrome map.  Their six syndrome columns have rank five.  Adding
the third word usually raises the rank to eight, but on the Gaussian divisor

```text
(z-1)^2+1=0                                                   (9)
```

it raises the rank only to seven.  The resulting two-dimensional centre
kernel is not contained in the determinant hypersurface; (1) selects one
invertible centre from it.

This changes the useful parent language.  The remaining problem is not to
separate the whole fixed linear nuisance space from the GHZ orbit: that is
impossible.  It is to compare the GHZ-survivor locus with the nonlinear image
of **source-integrable nuisance coefficients**.  A proof must show that every
such survivor violates a shared-deck, incidence, response, or attachment
condition; a refutation would have to lift one survivor through all of those
conditions to an actual graph witness.

The concrete point (1) is therefore a high-value test object for every
proposed universal source-to-target bridge.  Any bridge that accepts it using
only `N_star` membership is too weak.

## 4. Explicit scope boundary

The tensor (2) has `61` nonzero coordinates in the displayed basis, whereas
the weighted target diagonal has only three.  Although invertible local
changes send any concise GHZ tensor to a diagonal, those changes also move
the fixed nuisance space and do not provide legal graph data.  No port maps,
shared deck tensors, graph edge weights, response polynomials, or source
attachments are constructed here.

Therefore this package proves:

```text
fixed-star determinant-safe route: REFUTED,
fixed-star GHZ exclusion:          REFUTED,
graph/source integrability:        OPEN,
global Krenn-Gu conjecture:        UNRESOLVED.            (10)
```

## 5. Verification

Run the primary exact verifier:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py
```

Run the independent no-repository-import audit:

```powershell
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_ghz_survivor_and_determinant_safe_route_refutation.py
```

The two implementations separately reconstruct the permanent nuisance map
and check the original `81` coordinates.  The syndrome calculation is a
second membership interface, not the sole evidence for (3).

## 6. Frontier delta

Relative to `GLD70`--`GLD71`:

- the fixed `N_star` exclusion and determinant-safe saturation are closed by
  exact refutation, not proof;
- the balanced-minor and full fixed-space separator routes are withdrawn;
- the Gaussian point (1) becomes a mandatory hostile control for future
  bridges;
- the live successor obligation is source/graph integrability of the
  fixed-star GHZ-survivor locus, with the concrete point tested first;
- residual-coordinate boundary, triangle, lower-rank, other-root, and global
  coverage remain open and unchanged.

The global Krenn--Gu conjecture remains **UNRESOLVED**.
