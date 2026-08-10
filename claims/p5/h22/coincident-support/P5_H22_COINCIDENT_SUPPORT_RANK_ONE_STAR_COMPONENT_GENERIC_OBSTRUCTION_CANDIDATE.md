# Candidate generic weighted-`H22` obstruction for component twenty-one

```yaml
role: construction
date_utc: 2026-08-01T12:49:29Z
git_commit: bb7fb22c44b8348d993b6ed655ac007120dc0099
claim_label: VERIFIED
discovery_claim_label: CANDIDATE
scope: generic weighted H22 fibre of component twenty-one, the coincident-support rank-one star
inputs:
  P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md: 1b535667beed409fe08d4fa9011f2fbc455d4d4c6a7d0c2aecc089a107cdc447
  P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md: 8516673bfb7bffd5aa0cba6f92cc54aeb534845d0c43bcd07e1bdfee77e02220
  P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md: da64a3ee55d5dfa361a70cb771196f76f93d13b3d61df358442a22e1e72de1a8
method: exact characteristic-zero Hall support, normalized mixed-incidence projection with beta-diagonal reduction, and an infinity row-module certificate
command: uv run --with sympy python claims/p5/h22/coincident-support/derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
outputs:
  derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py: hash reported by replay
  p5_h22_coincident_support_rank_one_star_component_generic_certificate.json: hash reported by replay
  P5_H22_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: hash reported by replay
limitations: verified after a fresh no-import replay; generic function-field theorem only; no special-parameter or projective component-boundary fibres, pure-P4 component exhaustiveness, arbitrary-order local-to-global reduction, prize graph, or global Krenn-Gu conclusion
```

## Frozen claim

**VERIFIED after a fresh independent no-import replay:** the generic
weighted-`H22` fibre of component twenty-one is empty.  The `D01` direction
loses its all-alpha binary diagonal by Hall deficiency.  In the opposite
direction, a finite all-alpha incidence remains, but its all-beta diagonal is
identically zero; at projective infinity the all-alpha row is already in the
mixed row module.

The proof works over `K=Q(p,q,kappa,ell)`, uses the original component normal
form, and makes no finite-field inference or parameter-grid search.

## Intrinsic pure basis

Use

```text
alpha0=q(A+pB)-p(C+qB),       beta0=A+pB,
alpha1=ell A+C,               beta1=A,
alpha2=C,                     beta2=B+kappa A,
alpha3=D,                     beta3=A+ell C.        (1)
```

Direct permanent expansion gives only

```text
T1111=4p.                                             (2)
```

Every affine marking is `betai -> betai+hi alphai`.

## `D01`: homogeneous Hall deficiency

The kernel rows `alpha0,alpha1,alpha2` are all supported on source
coordinates `{X0,X1}`.  For arbitrary `[rho:sigma]`, their images under

```text
D01(z,e)=(rho z0+sigma z1,z2,z3,e)                 (3)
```

are supported on only the merged target channel and the extension channel.
Three permanent rows cannot be matched injectively into two columns.  Thus

```text
A01=0                                               (4)
```

for every marking, extension, and homogeneous weight, including both
endpoints.  `D01` is never genuinely binary.

## `D23`: finite all-alpha incidence

On `[lambda:1]`, reconstruct

```text
D23(z,e)=(z0,z1,lambda z2+z3,e).                   (5)
```

Normalize `A23=1` and impose all fourteen mixed equations.  Eliminating the
eight extension coordinates gives exactly

```text
<lambda+1, h3, F1, F2, F3>.                        (6)
```

Put `Delta=p^2-q^2` and `E=ell^2-1`.  The three marking equations are

```text
F1 = kappa Delta E h0 h1 - Delta h0 h2 - p E h1 h2
     + kappa ell Delta h0 - q kappa E h1
     + (q-p ell)h2 + kappa(p-q ell),

F2 = (h2-kappa)(h2+kappa)
     (p E h1+p ell+Delta h0-q),

F3 = (h2-kappa)(h2+kappa)
     ((ell-1)h1+1)((ell+1)h1+1).                  (7)
```

The projected all-alpha incidence is real, not a spurious elimination
closure.  However, exact standard-basis reduction in the normalized mixed
ideal gives

```text
NF(B23 | mixed, A23-1)=0.                           (8)
```

Therefore every finite mixed kernel with nonzero all-alpha diagonal has zero
all-beta diagonal.  No finite weight gives a genuine binary `D23` neighbour.
This includes `[0:1]` directly; the only possible all-alpha slope in (6) is
`[-1:1]`.

## `D23` at infinity

At `[1:0]`, direct module reduction over `K[h0,h1,h2,h3]` gives

```text
A23 in rowspan(M23),
NF(B23 | rowspan(M23)) != 0.                        (9)
```

Consequently `M23 z=0` forces `A23 z=0` at every marking.  The infinity
fibre has no genuine binary neighbour either.

## Retained one-diagonal survivor

The finite all-alpha incidence in (6) must not be relabeled empty.  One exact
point is

```text
lambda=-1,
h=(1/(p-q),0,kappa,0),

z=(-q/kappa,-1/kappa,0,0;
   -p/(kappa(p-q)),0,1,0).                          (10)
```

It satisfies all fourteen mixed equations and has

```text
A23=4(p-q)/kappa != 0,
B23=0.                                              (11)
```

Thus the tempting finite row-module claim `A23 in rowspan(M23)` is false.
The correct obstruction is the normalized incidence plus beta-diagonal
identity (8).  The point (10) is an exact one-diagonal survivor, not a binary
or `H22` survivor.

## Consequence and boundary

A weighted `H22` local reduction permits pure neighbours but requires at
least one genuinely binary direction.  Equations (4), (8), and (9) show that
neither direction can be binary at any projective weight.  Hence there is no
`D01`-pure/`D23`-binary shared compatibility branch to analyze further.

- The construction-agent discovery was `CANDIDATE`; a fresh verifier has now
  independently reconstructed and promoted the exact claim to `VERIFIED`.
- It is generic over the component function field.  Special parameter and
  projective component-boundary fibres remain open.
- It makes no component-exhaustiveness, arbitrary-order, prize-graph, or
  global Krenn--Gu claim.

## Replay

```text
uv run --with sympy python claims/p5/h22/coincident-support/derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
uv run --with sympy python claims/p5/h22/coincident-support/audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
```

The standalone replay verifies the pure restriction, all twenty-four `D01`
Hall summands, bidirectional equality of (6), the beta reduction (8), the
infinity row module (9), and the exact survivor (10)--(11).  The independent
verifier repeats these steps without importing the discovery script.
