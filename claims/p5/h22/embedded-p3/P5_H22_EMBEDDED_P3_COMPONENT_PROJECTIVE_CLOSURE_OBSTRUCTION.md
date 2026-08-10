# Refuted overstrong projective-closure argument for embedded-`P_3` weighted `H22`

## Status and scope

**REFUTED as a full closure proof; target remains UNKNOWN.**  The exact
homogeneous normal-base transport below is valid, but it does not extend the
weighted-`H22` obstruction on the normalized affine chart of the ninth,
embedded-`P_3` pure-`P_4` component to the full projective closure.

Every projective normal point with nonzero pure `P_4` restriction is carried
into the affine sign chart `C'=1,B'!=0`.  However, the free mode-zero plane has
its own normalization/pivot boundary, which this transport does not cover.
The three remaining projective normal coordinate points do have zero pure
restriction and cannot be the required pure root contraction.

The proof is characteristic zero and intrinsic.  It does not classify all
pure-`P_4` components, close weighted `H22` on other components, prove the
arbitrary-order reduction, or resolve the global Krenn--Gu conjecture.

## Homogeneous sign rectangle

The last three planes lie in a source hyperplane.  In its three coordinates,
their projective normals form an oriented face of a sign rectangle:

```text
n1=(C, A, B),
n2=(C,-A,-B),
n3=(C,-A, B),              [C:A:B] in P^2.          (1)
```

The other five oriented faces are obtained by permuting the three tensor
modes and changing source-coordinate signs.  On the chart `C!=0`, bases

```text
(-A,C,0), (-B,0,C);
( A,C,0), ( B,0,C);
( A,C,0), (-B,0,C)                                  (2)
```

give exactly two nonzero restricted-`P_3` coefficients:

```text
T100=2 A C^2,              T101=-2 B C^2.           (3)
```

After `C=1`, this is the normalized embedded-`P_3` family used by the three
existing weighted-`H22` obstruction theorems.

## Support-one points are inadmissible

If exactly one of `C,A,B` is nonzero, the three normals in (1) define one
common coordinate plane.  The squarefree `P_3` permanent vanishes identically
on the triple product of that plane.  Since the suspension identity is

```text
P_4(z,-,-,-)=z0 P_3(-,-,-),                         (4)
```

the pure `P_4` restriction is zero.  A root contraction producing a nonzero
`Delta_3` tensor cannot lie at one of these three coordinate points.

## Every nonzero point enters the closed chart

At every remaining projective point, at least two of `C,A,B` are nonzero.
Choose two.  A permutation of the three hyperplane coordinates sends the
first to a new common-coordinate slot `C'` and the second to the sign slot
`B'`; rescale to obtain

```text
C'=1,                     B'!=0.                    (5)
```

Signed coordinate changes and a permutation of the last three tensor modes
restore the oriented face (1).  The free fourth plane remains arbitrary.

The weighted-`H22` signature is invariant under this transport.  The two
weighted source mergers form a perfect matching of the four source
coordinates, represented by `01|23`.  Source permutations act transitively
on the three perfect matchings

```text
01|23,                    02|13,                    03|12.            (6)
```

Relabeling the two merge directions and their homogeneous weights therefore
returns the transported problem to the standard `D01,D23` normalization.
Tensor-mode permutations merely relabel markings.  Coordinate signs and
nonzero scalings preserve the permanent and all relevant local ranks up to
nonzero factors.

The normalized weighted-`H22` chart with `B'!=0` is already
closed by the union of:

- `P5_H22_EMBEDDED_P3_COMPONENT_GENERIC_OBSTRUCTION.md`;
- `P5_H22_EMBEDDED_P3_COMPONENT_RANK_TWO_LINE_BOUNDARY_OBSTRUCTION.md`;
- `P5_H22_EMBEDDED_P3_COMPONENT_RANK_ONE_COLLAPSE_OBSTRUCTION.md`.

Those three theorems explicitly retain an omitted normalization/projective
boundary of the free mode-zero plane.  The analogous complete `H31` closure
requires the additional
`P5_H31_EMBEDDED_P3_COMPONENT_R_ZERO_BOUNDARY_OBSTRUCTION.md`; no weighted
`H22` analogue has been proved here.  Equations (1)--(6) cover the projective
normal base but do not prove that this independent plane boundary enters the
closed normalized chart.  The claimed full projective weighted-`H22` closure
therefore does not follow.

## Relevance to the component-twenty `p+q` wall

The verified `p+q=0` diagonal-DVR arc classification sends its negative
equal-weight and `y<-r` infinity strata into the embedded-`P_3` closure.
The calculation does not supply the projective weighted-`H22` dependency for
all those lower-pair strata.  Their intersection with the omitted free-plane
normalization boundary remains an explicit target.  The displayed
`B_full/B_drop` charts and the direct `a=0,-1` component-fifteen special
fibres have separate certificates.

## Replay and evidence boundary

```text
uv run --with sympy python claims/p5/h22/embedded-p3/verify_p5_h22_embedded_p3_component_projective_closure.py
```

The primary reconstructs (3), proves the three support-one restrictions are
zero, exhausts the four nonzero projective-normal support masks by exact chart
transport, and checks the source-permutation orbit (6).  Those subclaims are
retained.  Its dependency audit records that they are insufficient for full
closure.  No finite-field calculation is used as proof.
