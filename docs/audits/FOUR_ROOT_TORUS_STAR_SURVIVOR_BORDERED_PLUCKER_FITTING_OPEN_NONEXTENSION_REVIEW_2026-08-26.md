# Review: survivor bordered-Pluecker Fitting-open nonextension

Date: 2026-08-26

## Verdict

Accept `GLD83` as an **exact denominator-free principal-open theorem and
intrinsic full quadratic Fitting-open reduction** on the globally defined
scale-fixed equal-leaf survivor subincidence

```text
B=Spec Q(i)[x_0,...,x_14]/(g_0,...,g_9,x_8)
```

in the displayed frame gauge.  Unlike the smaller `GLD80` neighborhood,
this base does not invert the selected quotient pivot `gamma_num`.

The selected bordered determinant gives

```text
Delta_83=Omega det(M_Pl),
```

with `Delta_83(F_0)!=0`, and every raw coefficient preimage fails the
complete legal first-response condition on `D(Delta_83)`.  The complete
exterior-coordinate family gives the larger exact finite union
`D(Omega I_Pl)`, where

```text
I_Pl=I_45(A_Pl)=Fitt_0(coker A_Pl).
```

This removes `gamma_num` and the single selected quadratic determinant as
intrinsic residual branches.  It does not prove that `V(I_Pl)` contains a
response, classify survivor components, cover other gauges or physical
source branches, or resolve Krenn--Gu.  The global status remains
**UNRESOLVED**.

## Exact construction audited

Let `C_F` be the transported `78 x 13` mixed constant block and let
`w_0,w_1,w_2` be the first three transported mixed response columns, linear
in the nine homogeneous invariant-raw coordinates `y`.  For every response
pair and ordered fifteen-row set define

```text
P_(S;c,d)=det [C_F | w_c | w_d]_S.
```

These homogeneous quadrics are necessary for a legal response without a
constant-block pivot.  If `rank C_F<13`, they all vanish identically.  If
`rank C_F=13`, they are the denominator-free exterior coordinates of the
ordinary quotient proportionality equations.  The independent response-
domain count gives the same rank-at-most-fourteen condition and retains
response-rank drops.

Using the thirteen Gaussian pivot rows and the forty-five `GLD82`
descriptors produces a `45 x 45` coefficient matrix `M_Pl`.  Exact bordered
Schur expansion gives the ambient polynomial identity

```text
M_ff=gamma_num M_Pl,
det(M_ff)=gamma_num^45 det(M_Pl).
```

Consequently

```text
Delta_82=gamma_num^46 Delta_83.
```

The identity holds before imposing survivor equations and therefore remains
valid in `O(B)` without localizing at `gamma_num`.  Nonvanishing of
`det(M_Pl)` itself forces `rank C_F=13`, so the `GLD82` Reynolds reduction is
legal on the selected open rather than assumed there.

For the full reduction, put `E=O_B^78` and `Y=O_B^9`.  The three elements

```text
(wedge^13 C_F) wedge w_c wedge w_d
    in wedge^15 E tensor Sym^2(Y^*)
```

define a coefficient map

```text
A_Pl: (wedge^15 E)^* tensor O_B^3 -> Sym^2(Y^*).
```

It is a `45 x N` matrix with

```text
N=3 binomial(78,15)=13103742929259840.
```

Its maximal-minor open is a finite union even though explicitly
materializing every column is impractical.  Changes of the mixed basis,
constant-block basis, or invariant homogeneous raw basis act by invertible
source or target operations.  The displayed wedges and ordered coordinate
minors may change by units, while the Fitting-open and its vanishing locus do
not.

## Gaussian specialization

At the exact `GLD72` survivor,

```text
d=24-24i,
gamma_num=-692533995824480256(1+i),
M_Pl=d^2 gamma_num M_0,
det(M_Pl)=d^90 gamma_num^45 det(M_0) != 0.
```

Here `M_0` is the independently audited normalized `GLD74` matrix.  The
primary verifier reconstructs `C_F`, the three response maps, the exact
Schur quotient, and all `2,025` coefficients of the forty-five selected
bordered quadrics at this specialization.  They agree entry-for-entry with
the pinned prediction.  The inherited certificate SHA-256 is
`4cdaf08a5f5dc40abc845d4dc1e6046ce3b259b2c751dfd3ec2955e5b94e65e0` and
the `GLD74` quotient fingerprint is
`17c10d8e04a4e29b073914919beb0a99ff77735be12cc16f095e07ef7549452e`.

## Hostile-review history and repairs

Three bounded hostile reviews attacked the Fitting orientation and size,
rank-drop semantics, source-interface scope, quotient decharting, basis
dependence, and evidence boundary.

The first Fitting review rejected the draft as merge-ready because the base
was described through the `GLD80` neighborhood, where `gamma_num` had
already been inverted.  That would have made the advertised gamma-free
coverage vacuous.  The final theorem instead defines `B=X_sf` globally and
keeps `Omega` explicit.  The physical corollary was narrowed to the named
`GLD81` source branch whose induced normalized equal-leaf frame actually lies
in `B intersect D(Delta_83)`, and every full-open statement retains the
factor `Omega`.

The source review found the written bordered and rank-drop argument sound,
but identified a priority-one evidence gap: the initial verifier replayed
only scaling and toy bordered identities.  The final primary verifier now
reconstructs the physical moving interface at `GLD72` and checks all selected
coefficients directly.  The geometric review requested an explicit base,
ambient location for the polynomial identity, target-response normalization,
and precise meaning of "intrinsic"; all four were added.

No hostile reviewer found a priority-zero mathematical defect.  The accepted
package preserves the distinction between the exact written universal
reduction and its exact Gaussian computational replay.

## Evidence and independence

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_survivor_bordered_plucker_fitting_open_nonextension.py
python -I claims/arbitrary-order/audit_four_root_torus_star_survivor_bordered_plucker_fitting_open_nonextension.py
```

The primary verifier imports the established moving-response builder and
reconstructs the selected `45 x 45` bordered matrix at `GLD72`.  The no-import
audit instead uses only the standard library: it independently parses
`Q(i)`, recomputes the normalized determinant, checks the exponent and
dimension arithmetic, and tests nonsingular-pivot, singular-pivot, and
constant-rank-drop bordered identities together with scope fences.

Neither program materializes the roughly `10^16` columns of `A_Pl`, and the
selected circuit is not symbolically expanded over the whole survivor base.
The universal block-determinant identity and geometric-point Fitting argument
are proved in the theorem document; specialization is not substituted for
them.

## Hostile controls and residual

- `GLD72` remains an exact concise GHZ tensor in the nuisance space; the new
  theorem excludes only its legal first response and an explicit open around
  it.
- No epsilon or `Q`-generator criterion is used to infer GHZ membership.
- Reynolds averaging is applied only after the bordered open itself forces
  `rank C_F=13`; all raw preimages are retained before that proved reduction.
- Constant-block rank drops, zero response columns, response-rank drops, and
  the projective boundary `s=0` remain in the equations.
- Frame nonuniqueness is controlled only in the declared equal-leaf gauge.
- `D(Omega I_Pl)` is a sufficient finite Fitting-open exclusion, not an
  exhaustive survivor theorem.

The fixed-chart residual is now the intrinsic closed locus

```text
V(I_Pl) intersect D(Omega).
```

The next high-value parent move is an exact finite survivor/component cover
of that locus, beginning with center-rank determinantal charts, or a stronger
projective certificate that excludes additional points of `V(I_Pl)`.  Other
gauges, components, source branches, rank/support boundaries, triangles,
other root profiles, and the global conjecture remain separate obligations.
