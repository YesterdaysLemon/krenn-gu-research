# Independent verification of component twenty's intrinsic-wall exceptional fibres

```yaml
role: verifier
date_utc: 2026-08-01T14:10:40Z
git_commit: 00c3574f854e1f86cb8ec2304645204479c3f75e
claim_label: VERIFIED
scope: compactified Segre-direction H31/H22 incidence over the zero restrictions (p,q)=(0,1),(-1,0), plus structural audits of the straight fixed-source zero edge and exact s=0 diagonal-DVR arcs at (-1/2,1/2)
inputs:
  COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_CANDIDATE.md: 000aea9a03665448b68fe266e741af825cc2221e03e6f3c0e015aa9a3cb2517c
  derive_component20_intrinsic_wall_exceptional_fibres_candidate.py: 0bc5ecdefc923410cd8baf58a8e9e76ab86dcb1c3513beb16055cbf989d52470
  component20_intrinsic_wall_exceptional_fibres_certificate.json: df770981af8b350cf6a68cb1ae104fd10c65ac31fbe453f91d07c4c843f5c8b3
  P4_COMPONENT20_INTRINSIC_EXCEPTIONAL_BASE_GEOMETRY_PROOF_B.md: 68a837465d0c82621a6ed0a0d3aaf9dda3086a206bcd3d6a0e5a84d2e4b40cc0
  derive_p4_component20_intrinsic_exceptional_base_geometry_proof_b.py: cd1f0552775f3f6c24e92e4068a65372e47f059e664a8f0c6ca27607066bd004
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_COMPONENT.md: dcaae5365f5e2072e798c2ee52dea47c0d5c48f073ed7553ae5f758e9830f0b2
  P4_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY.md: 667611de1e8bd08dd8c1a5b3b3c431ab57df523f834828c4258d881833b9ee82
  P5_H22_COMMON_ACTIVE_BINARY_TRIANGLE_P_PLUS_Q_BOUNDARY_OBSTRUCTION.md: 52168b35b43c40c483919c8fa1dd37e7c147cae5f331320d8656bf6a1ed309a9
  P4_SUPPORT_ONE_SECANT_BOUNDARY_INCLUSION.md: eb5a8fb528a9c367ec059a06a5630cbcb533be5c49a4ecd1ee8148cac6644b32
method: no-import plane and permanent reconstruction, transverse graph calculation, exact polynomial-rho/lambda elimination with inverse saturation, half-centre pair and arc audit, and exact real-linear valuation-cone verification
command: uv run --with sympy --with z3-solver python claims/p4/disputed-ownership/component20-intrinsic-boundary/exceptional-fibres/audit_component20_intrinsic_wall_exceptional_fibres_candidate.py
outputs:
  audit_component20_intrinsic_wall_exceptional_fibres_candidate.py: ffc3bb2176756487c7e889a4487f0b68564868e0f0ff748cbb0d8de75b112329
  COMPONENT20_INTRINSIC_WALL_EXCEPTIONAL_FIBRES_VERIFICATION.md: hash reported by replay
limitations: the P1 fibres are compactified tensor-direction fibres over zero restrictions, not ordinary nonzero-P4 fibres; the half-point audit covers the straight fixed-source zero edge and exact s=0 diagonal-DVR arcs only; mixed or non-diagonal source arcs, complete p=0,-1 source-torus atlases, component-parameter infinity, arbitrary GL4 degenerations, component exhaustiveness, arbitrary-order reduction, prize graph, and the global Krenn-Gu conjecture remain outside scope
```

## Verdict

**VERIFIED in the stated compactified scope.**  The candidate implementation
was not imported.  The planes, permanents, graph closure, incidence matrices,
elimination ideals, half-centre geometry, and component-fifteen arc were
reconstructed first; the candidate and proof-B artifacts were compared and
replayed only afterward.

The tuples over `(p,q)=(0,1),(-1,0)` have identically zero restricted
tensors and pair profile `(3,3,3,3,3,3)`.  They are not ordinary nonzero
`P4` fibres.

## Exceptional direction lines

Put `s=p-q+1` and `t=q(q-1)`.  The base ideal `(s,t)` has exactly the two
stated points.  Its Jacobian determinants there are `1,-1`, so both are
simple transverse complete intersections.  For the coefficient direction

```text
[a:b]=[s:-t],
```

the graph closure is the hypersurface `s*b+t*a=0`; its fibre over either
base point is exactly `P1_[a:b]`.  The correct mode-zero kernel line is

```text
alpha0=b*r0-a*r1.
```

The verifier covers `[1:rho]` by `alpha0=rho*r0-r1,beta0=r0`, retaining
`rho` polynomially over `Q`, and covers `[0:1]` directly with
`alpha0=r0,beta0=r1`.  This is an exceptional fibre of the compactified
tensor-direction graph over a zero restriction; it does not make the base
tuple a nonzero `P4` fibre.

## Exact incidence results

All eliminations are characteristic zero and use explicit inverse equations
for the required nonzero diagonals.

- Marked `H31`: all `16/16` deletion projections are `<1>`.
- Complete shared weighted `H22`: all `16/16` projections are `<1>`.
- Individual weighted-binary projections: `14/16` are `<1>` and exactly two
  finite-Segre, finite-weight `D01` closures survive:

```text
(p,q)=(0,1):
<h3,h0,
 rho*h1*h2*lambda+rho*h1*lambda+rho*h1+rho*h2-h1*lambda-h1>

(p,q)=(-1,0):
<h3,h0,
 rho*h1*h2*lambda-rho*h2*lambda-rho*h1-rho*h2-h2*lambda-h2>.
```

The shared same-extension calculation kills both individual closures.  The
finite weight chart retains `lambda` polynomially and therefore includes
`lambda=0`; `[1:0]` is checked directly.  Both all-alpha orientations are
checked.  There is no missing normalization, saturation, Segre endpoint, or
homogeneous-weight endpoint in this compactified incidence statement.

## Half-centre and component-fifteen audits

The two walls meet at `(p,q)=(-1/2,1/2)`.  The straight fixed-source limit is

```text
U0=<e,A-B>,
U1=<e,C+(A-B)/2>,
U2=<e,C-(A-B)/2>,
U3=<e,A+B>.
```

Its full tensor is zero and its pair profile is `(3,3,2,3,3,3)`.  It is the
`k=infinity` limit of `U0=<A-B,C-k e>`, whose Pluecker vector is
`(k,-k,0,0,1,-1)`.  Thus it is a zero-tensor edge, not a missing genuine
half-centre wall stratum and not a new `H31/H22` claim.

The candidate's separate component-fifteen placement is also **VERIFIED**.
The reconstructed `tau!=0` arc has sole coefficient `T1100=-2*tau`, pair
profile `(3,4,2,4,3,4)`, and exact rank-two pair `03` with kernel

```text
<e tensor e, (A-B) tensor (A+B)>.
```

All four Pluecker limits equal the zero-edge planes.  The punctured arc is a
nonzero pure restriction with an exact rank-two pair containing a
support-one Segre-kernel point, precisely the hypotheses of the verified
support-one secant theorem; hence it lies in the component-fifteen closure.

## Proof-B geometry and boundary

The proof-B discovery label remains `DERIVED`, while its scoped geometry is
now independently **VERIFIED**.  Exact real linear arithmetic proves for
`s=0` diagonal-DVR arcs that

```text
E=0 iff x1=x2=y, -d<=y<=0, x0>=d.
```

Direct leading-plane reconstruction gives the same four embedded-`P3`
negative-`y` flags and the finite-`k`/`k=0` `y=0` charts already present in
the diagonal wall atlas.  Proof-B makes no `H31/H22` claim, and this audit
does not promote its result to non-diagonal or arbitrary source arcs.

Neither this report nor the candidate resolves component exhaustiveness,
arbitrary-order local-to-global reduction, a prize graph, or the global
Krenn--Gu conjecture.
