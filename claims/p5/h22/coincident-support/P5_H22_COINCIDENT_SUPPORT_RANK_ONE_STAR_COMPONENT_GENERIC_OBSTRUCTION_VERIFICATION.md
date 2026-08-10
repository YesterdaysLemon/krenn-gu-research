# Independent verification of the component-twenty-one generic weighted-`H22` obstruction

```yaml
role: verifier
date_utc: 2026-08-01T13:05:24Z
git_commit: 17d6cdf41bdbdca718068e950babe6ee4e3d8b5f
claim_label: VERIFIED
scope: generic weighted H22 fibre of component twenty-one, the coincident-support rank-one star
inputs:
  P5_H22_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION_CANDIDATE.md: 7c8f235f6c503f9b7e8c69fc0e7a85d998c7a7f2627f81e727cd0d2dd0a3c212
  derive_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py: 41f5a749537db4b2263bff8b9c8bc687389658b3ffa5c2188af2484f20081844
  p5_h22_coincident_support_rank_one_star_component_generic_certificate.json: f616783ac377994ec5bd7a8048dbf3ef4846acfd991320c191368b3088bc18dc
  P4_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT.md: 1b535667beed409fe08d4fa9011f2fbc455d4d4c6a7d0c2aecc089a107cdc447
  verify_p4_coincident_support_rank_one_star_component.py: a170054715c8fc8ec7f1fc1e0dba896c0fdc7d72ed58e41e7f9b8bba23af4adf
  P5_H31_COINCIDENT_SUPPORT_RANK_ONE_STAR_COMPONENT_GENERIC_OBSTRUCTION.md: 8516673bfb7bffd5aa0cba6f92cc54aeb534845d0c43bcd07e1bdfee77e02220
  verify_p5_h31_coincident_support_rank_one_star_component_generic_obstruction.py: ca17f1b69d9083d9c567a228abd08d5395acebb1637378bae430b08302841378
  P5_H22_COMMON_SINGLETON_COMPONENT_GENERIC_OBSTRUCTION.md: da64a3ee55d5dfa361a70cb771196f76f93d13b3d61df358442a22e1e72de1a8
method: fresh subset-DP permanents, homogeneous Hall certificate, exact characteristic-zero finite elimination and beta reduction, direct infinity row-module reduction, and an exact one-diagonal witness
command: uv run --with sympy python claims/p5/h22/coincident-support/audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
outputs:
  audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py: 259dbff442154a84d0ea5cd7438a64dd4de22fa44100e5537cbbf1ebb8e4d68d
limitations: generic function-field theorem only; no special-parameter or projective component-boundary fibres, P4 component exhaustiveness, arbitrary-order local-to-global reduction, prize graph, or global Krenn-Gu conclusion
```

## Verdict

**VERIFIED.**  A fresh no-import verifier reconstructs the component normal
form, pure marking, homogeneous `D01` Hall obstruction, finite and infinite
`D23` incidences, normalized beta-diagonal identity, and retained
one-diagonal survivor over `Q(p,q,kappa,ell)`.  Neither weighted direction can
be genuinely binary, so the generic weighted-`H22` fibre of component
twenty-one is empty.

This is only a generic function-field theorem.  Special parameter divisors
and projective component-boundary fibres remain open.

## Intrinsic basis and pure support

Starting from the independently replayed component theorem, the verifier
rebuilds

```text
alpha0=q(A+pB)-p(C+qB),       beta0=A+pB,
alpha1=ell A+C,               beta1=A,
alpha2=C,                     beta2=B+kappa A,
alpha3=D,                     beta3=A+ell C.
```

The mode-zero basis change has determinant `p`, a unit at the generic point.
A subset-dynamic-program permanent calculation gives

```text
T_w=0 for w!=1111,       T_1111=4p
```

before and after every affine marking `beta_i -> beta_i+h_i alpha_i`.  The
exact `P4` and generic `H31` dependency replays both pass.

## Homogeneous `D01` Hall obstruction

For arbitrary `[rho:sigma]`, the first three projected alpha rows all have
support

```text
{merged channel, extension channel} = {0,3}.
```

Their three-row Hall neighborhood has size two.  The independent verifier
checks all twenty-four permanent summands and the subset-DP permanent itself:

```text
A01=0
```

identically in `rho,sigma` and the four alpha-extension coordinates.  This is
marking-independent and includes `[0:1]` and `[1:0]` without division.  Hence
`D01` is never genuinely binary.

## Finite `D23`: exact normalized incidence

On `[lambda:1]`, normalize `A23=1`, impose all fourteen mixed equations, and
eliminate the eight extension coordinates.  Bidirectional standard-basis
reduction—actual ideal equality, not only radical or set equality—gives

```text
<lambda+1, h3, F1, F2, F3>,
```

with `F1,F2,F3` exactly as stated in the candidate.  The full normalized ideal
has basis size eleven and the projected ideal has basis size five.

The normalization has no hidden saturation gap.  Every contracted coefficient
is homogeneous linear in the common extension vector.  For any actual point
with `A23!=0`, scaling that same vector by `1/A23` reaches `A23=1` without
changing its marking or projective weight.  Conversely, a normalized point has
`A23=1` and is already actual.  No component-parameter denominator is
introduced by this normalization.

The exact reduction in the complete normalized ideal is

```text
NF(B23 | mixed coefficients, A23-1)=0.
```

Thus `B23` lies in the full ideal before projection.  Every actual finite
mixed kernel with `A23!=0` has `B23=0`; this conclusion does not rely on
whether a projected closure point lifts.  The projected equation
`lambda+1=0` also excludes the finite endpoint `[0:1]` directly and leaves
only the possible all-alpha slope `[-1:1]`.

## Direct infinity identity

At `[1:0]`, a separate polynomial-module calculation over

```text
Q(p,q,kappa,ell)[h0,h1,h2,h3]
```

gives

```text
A23 row remainder modulo the fourteen mixed rows = 0,
B23 row remainder modulo the fourteen mixed rows != 0.
```

The first equality is an exact row-module identity with polynomial marking
coefficients; it introduces no marking denominator.  Therefore every
infinity mixed kernel has `A23=0`, independently of the beta row, and cannot
be genuinely binary.

Together, the finite chart and the direct infinity calculation exhaust the
homogeneous weight line.

## The finite incidence is real but one-diagonal

The verifier reconstructs the exact point

```text
lambda=-1,
h=(1/(p-q),0,kappa,0),
z=(-q/kappa,-1/kappa,0,0; -p/(kappa(p-q)),0,1,0).
```

All fourteen mixed coefficients vanish and

```text
A23=4(p-q)/kappa,       B23=0.
```

The only denominators are `kappa` and `p-q`, both nonzero units in the generic
function field.  This point also satisfies `F1=F2=F3=0`.  It proves that the
finite projected all-alpha incidence is not a spurious closure artifact and
refutes the tempting finite claim `A23 in rowspan(M23)`.  It does not threaten
the theorem because a genuine binary tensor needs both diagonals nonzero.

## Evidence boundary and replay

The proof is exact in characteristic zero.  No finite-field sample, parameter
grid, broad brute force, timeout, or solver exit code is used as proof.  It
does not close special or projective component fibres, prove pure-`P4`
component exhaustiveness, establish the arbitrary-order local-to-global
reduction, construct a prize graph, or resolve the global Krenn–Gu conjecture.

```text
uv run --with sympy python claims/p5/h22/coincident-support/audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
uv run --with ruff ruff check claims/p5/h22/coincident-support/audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
python -m py_compile claims/p5/h22/coincident-support/audit_p5_h22_coincident_support_rank_one_star_component_generic_obstruction_candidate.py
python -m json.tool claims/p5/h22/coincident-support/p5_h22_coincident_support_rank_one_star_component_generic_certificate.json
git diff --check
```

The verifier emits current hashes for this report, itself, the candidate
artifacts, and every theorem dependency.
