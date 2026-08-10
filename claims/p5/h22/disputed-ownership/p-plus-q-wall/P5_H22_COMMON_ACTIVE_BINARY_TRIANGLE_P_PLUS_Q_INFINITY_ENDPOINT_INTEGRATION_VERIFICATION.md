# Independent verification of the off-wall endpoint integration step

## Verdict and exact scope

**VERIFIED.**  On both off-wall `gamma=0` marking axes, every common genuine
finite-`D01` / finite-`D23` extension is forced to have `D23` slope `r=0`.
It therefore lies in the already independently verified `r=0` compatibility
obstruction.

This report verifies only that finite-slope integration.  It does not silently
claim the projective infinity branches: those are cited separately from the
independent endpoint audit, whose overall verdict was `REFUTED` for an
unrelated rank-exactness sentence but which explicitly verified both infinity
subclaims used here.

## Fresh direct reconstruction

Starting from

```text
e=(1,0,0,0), w=(0,1,1,1), u=(0,1,-1,0),
v1=(0,1,1,0), v2=(0,0,0,1),

alpha=(e,e,-u,2v2-v1), beta=(w,w,e,v1),
```

the verifier rebuilds all fourteen mixed permanent rows over characteristic
zero.  It imports neither the endpoint derivation nor any compatibility
derivation or helper.

At `h=(T,0,0,0)`, finite `D01` slope `s` has the complete rank-seven kernel

```text
k0=(-1,-1,0,-2T;2T,T,1,0),
det witness=-16s^6.
```

At `h=(0,T,0,0)`, the direct rebuild gives

```text
k1=(-1,-1,0,-2T;T,2T,1,0)
```

with the same witness.  At `s=0`, the mixed rank drops to one but the complete
seven-dimensional kernel is killed by `A01`; there is no hidden genuine
branch.

## Arbitrary finite `D23` slope on the shared line

Let `M23(r)` be the finite-`D23` mixed matrix built at the same marking and
with the same extension coordinates.  Direct multiplication gives on both
axes

```text
M23(r) ki=(0,...,0,-12Tr),
```

where row 13 is the sole possibly nonzero entry.  Since the coefficient is a
nonzero characteristic-zero scalar,

```text
M23(r)ki=0 iff T*r=0.
```

For the shared projective vector `z=Cki`, the four diagonals are

```text
A01=-4Cs,          B01=4C(Ts+1),
A23= 4C,           B23=4CT(2r+1).
```

Thus common genuineness requires

```text
C*s*(Ts+1)!=0,
T*(2r+1)!=0,
T*r=0.
```

The second condition forces `T!=0`; compatibility then forces `r=0`, after
which `2r+1=1`.  Equivalently, every common genuine finite-finite extension
satisfies

```text
r=0, C*s*T*(Ts+1)!=0.
```

No division by `T`, `r`, or `2r+1` is used to obtain the result.

## Boundary attack

- `T=0`: the two marking axes coincide, `M23(r)ki=0` for every `r`, but
  `B23=0` on the complete shared line.  The origin is nongenuine.
- `r=-1/2`: if `T!=0` the mixed compatibility row is nonzero; if `T=0`,
  `B23=0`.  No diagonal-zero slope escapes.
- `s=0`: `A01` vanishes on the complete direct rank-one mixed fibre.
- `Ts+1=0`: `B01` vanishes on the complete rank-seven `D01` line.
- `C=0`: the shared extension is zero and cannot meet the normalized binary
  incidence.

These direct branches verify that common genuineness really forces
`C*s*T*(Ts+1)!=0` and `r=0`, including the axis intersection.

## Reduction to the verified compatibility theorem

Substitution `r=0` recovers exactly the shared line, four diagonals, and open
condition audited in
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_COMPATIBILITY_OBSTRUCTION_VERIFICATION.md`.
That independent verifier proved both the transverse mode-two rank-four minor
and the stacked two-contraction rank-five minor.  Consequently every common
off-wall finite-finite survivor is excluded by that already `VERIFIED`
bounded theorem.

## Projective infinity branches: cited boundary only

The independent audit
`P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_INFINITY_ENDPOINT_INDEPENDENT_VERIFICATION.md`
explicitly verified that, for the off-wall face,

- `D01` infinity has a complete rank-six kernel with a genuine-locus
  rank-four mode-two minor; and
- `D23` infinity has unit projected ideal.

That audit’s overall label is `REFUTED` because it found an unrelated exact
rank-two subfamily at finite `D23,r=1/2`; the infinity statements themselves
are explicitly listed as verified and are the only facts cited here.  This
integration verifier does not recompute or broaden them.

## Evidence boundary and replay

- Exact characteristic-zero algebra only.
- No finite fields, parameter grids, or broad minor scans.
- No failed branch or timeout.
- No on-wall, non-diagonal, arbitrary-order, component-exhaustiveness, or
  global Krenn--Gu claim.

Replay the full machine-readable verifier report with

```text
uv run --with sympy python \
  claims/p5/h22/disputed-ownership/p-plus-q-wall/audit_p5_h22_common_active_binary_triangle_p_plus_q_infinity_endpoint_integration_verifier.py
```
