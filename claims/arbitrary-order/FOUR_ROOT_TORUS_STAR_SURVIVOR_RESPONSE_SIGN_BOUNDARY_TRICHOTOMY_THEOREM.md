# Four-root torus-star survivor response: sign-boundary trichotomy

## Status

**Exact fixed-fibre projective-boundary classification inside the leaf-sign
block (`GLD77`).**  Work over `Q(i)` and extend scalars to `C`.  Retain the
complete canonical `GLD70` fully-supported, nonisotropic rank-two torus-star
interface, the exact `GLD72` Gaussian survivor, the full `35`-dimensional raw
coefficient fibre, and the `GLD74` mixed first-response quotient.

This theorem classifies the rank-one boundary on the entire
three-dimensional leaf-sign isotypic block of that raw fibre.  It does **not**
classify boundary points in the eight-dimensional trivial block or the
24-dimensional standard block, construct a finite raw lift, exclude a
survivor neighbourhood, prove a source graph, or resolve Krenn--Gu.  The
global conjecture remains **UNRESOLVED**.

**Successor notice.**  `GLD78` retains all survivor and slope directions,
checks the corrected first strict jet at all three points, and proves an
all-order invariant-sector exclusion on one explicit principal open around
each sign-boundary chart.  Boundary directions with trivial or standard raw
components remain open.

## 1. Fixed-fibre homogeneous response

Write the exact `GLD74` mixed quotient as

```text
Z(t)=Z_const + K_0 t, Z_const + K_1 t, Z_const + K_2 t,
```

where each `K_j` is `65 x 35` and `t` uses the fixed ascending coordinate
order `t_0,...,t_34`.  On the projective boundary of the raw fibre only the
homogeneous matrix

```text
Z_infinity(t)=[K_0 t | K_1 t | K_2 t]                 (1)
```

remains.  The `GLD76` leaf-`S_3` action splits the raw kernel as

```text
8 trivial + 3 sign + 12 standard copies.              (2)
```

The sign-isotypic summand therefore has vector-space dimension three.  The
primary verifier constructs it with the central idempotent

```text
P_sign=(1/6) sum_(sigma in S_3) sign(sigma) P_raw(sigma). (3)
```

No invariant-fibre assumption is made: (3) selects one exact direct summand
of the complete 35-dimensional fibre only.

## 2. Exact three-by-three compression

Choose sign coordinates `(u,v,w)` in the sparse basis recorded by the
verifier.  The image of (1) spans a three-dimensional sign block in the
`GLD74` quotient.  In an exact output basis, (1) is the following `3 x 3`
matrix of linear forms:

```text
W(u,v,w) = [ u   i*u+(1+i)*v       -u ]
           [ v   (1-i)*u-i*v       -v ]               (4)
           [ w       -w             w ]
```

The remaining 62 quotient coordinates are recovered by the verified
injective output-basis matrix, so

```text
rank Z_infinity(t) = rank W(u,v,w)                    (5)
```

for every sign vector `t`.

### Theorem 2.1 (sign-plane boundary trichotomy)

The homogeneous ideal of the rank-at-most-one locus of (4) is

```text
I_sign=((u+v)(u-i*v), u*w, v*w).                      (6)
```

Its projective zero scheme over `Q(i)` (and hence over `C`) is the reduced
union of exactly three points:

```text
[0:0:1],       [i:1:0],       [1:-1:0].               (7)
```

#### Proof

The nine two-by-two minors of (4) have seven nonzero values.  Exact Groebner
reduction over `Q(i)` gives (6), and conversely three of the minors are units
times the three displayed generators, so no equation was lost.

If `w != 0`, the last two generators force `u=v=0`, giving `[0:0:1]`.
If `w=0`, the first generator splits into the two distinct linear factors
`u+v` and `u-i*v`, giving `[1:-1:0]` and `[i:1:0]`.  The three corresponding
homogeneous maximal ideals are distinct and occur with multiplicity one;
the projective scheme is reduced.  `square`

## 3. Raw-coordinate witnesses

In the fixed `GLD74` fibre coordinates, representatives of (7) are

```text
v_- = -e_13+e_15+e_22-e_24-e_31+e_33,

v_+ = -i*e_9-e_10+i*e_11+e_14+i*e_18+e_19-i*e_20
      -e_23-i*e_27-e_28+i*e_29+e_32,

v_x = e_9-e_10-e_11+e_14-e_18+e_19+e_20
      -e_23+e_27-e_28-e_29+e_32.                      (8)
```

They have exact response-column ratios

```text
v_- : (1,-1, 1),
v_+ : (1, 1,-1),
v_x : (1,-1,-1).                                      (9)
```

For every point, the appropriate `130 x 35` proportionality matrix has rank
`34`; the displayed vector spans its one-dimensional kernel.  The induced
79-coordinate raw direction lies in `ker b` and transforms by the sign
character under every leaf permutation.

The first two points are the `GLD76` witnesses.  The third is new.  All three
are points at infinity in the homogenized **necessary mixed rank-one
condition**.  None is a finite raw coefficient preimage or a solution of the
full universal affine response incidence.

## 4. Proof-topology consequence and residual obligations

Within the sign plane, the projective boundary is no longer an unspecified
escape set: it is the exhaustive finite cover (7).  A strict-transform
calculation restricted to this block therefore has exactly three exceptional
charts to test.

This does not exhaust the full projective boundary in `P^34`; additional
points may have trivial or standard raw components.  Nor does tangent or
first-jet failure at a point exclude arcs whose homogenizing coordinate
starts in higher order.  The named residual parent obligations are:

1. test the strict transform at all three points in (7), retaining the four
   scale-fixed `GLD75` survivor directions and the moving fixed response
   quotient;
2. classify or finitely cover rank-one boundary points outside the sign
   plane;
3. only after all boundary branches are controlled, resume a principal-open
   certificate lift or comprehensive Groebner cover of the affine incidence.

## 5. Verification and hostile controls

Run:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_survivor_response_sign_boundary_trichotomy.py
python -I claims/arbitrary-order/audit_four_root_torus_star_gaussian_survivor_full_coefficient_fibre_first_response_nonextension.py
```

The primary verifier reconstructs the `65 x 3 x 35` homogeneous response,
the raw-kernel sign projector, the compressed matrix (4), the ideal (6), all
three sparse points, their rank-`34` proportionality systems, and their actual
raw sign covariance.  The independent standard-library audit rebuilds the
literal-Delta permanent map, reverses the fibre-variable order, reconstructs
the sign basis without importing a project module, checks (4), and replays
the three witnesses.

The hostile controls are preserved:

- `GLD72` remains an exact concise GHZ tensor in the fixed nuisance space;
- the `GLD70` epsilon generator is not used as a GHZ-membership criterion;
- the `GLD74` affine exclusion and exact quotient fingerprint are replayed;
- all statements are in the fixed literal-Delta fibre, so no unique-frame
  assertion is made;
- no response minor or projective coordinate is divided by silently;
- the cover (7) is exhaustive only inside the sign plane;
- projective boundary directions are not promoted to finite lifts, graph
  witnesses, or counterexamples;
- no local fixed-star statement is promoted to the global conjecture.
