# Component twenty-three `r=0` to `t=0` weighted-`H22` symmetry transfer

## Status

**Exact characteristic-zero symmetry-transfer theorem.**  The normalized
component-twenty-three family has a legal source-mode involution carrying

```text
(r,t) -> (-t,-r).
```

It exchanges the two homogeneous weight coordinates in both `D01` and `D23`.
Consequently the verified `r=0` constant-profile affine obstruction over

```text
Q[t,1/(t*(t-1)*(t+1))]
```

transfers exactly to a complete weighted-`H22` obstruction on the matching
constant-profile open of `t=0` over

```text
Q[r,1/(r*(r-1)*(r+1))].
```

Thus every weight is obstructed whenever `t=0` and
`r*(r-1)*(r+1)!=0`.  The separately verified source fibres
`r=0,t=+/-1` transfer to the two remaining target values `r=-/+1,t=0`.
Consequently the complete normalized target divisor `t=0,r!=0` is empty.
The sole exclusion is `r=0`, the normal-form chart boundary.  In the
standard edge order `01,02,03,12,13,23`, the special target profile is
`(3,3,3,3,4,4)`; the source profile `(3,3,3,4,3,4)` is relabelled by the row
permutation in the involution.

This is a symmetry corollary of the separately replayable `r=0` theorem, not
an arbitrary source-basis result.  Arbitrary ambient or source changes,
omitted component charts, the common chart boundary, other component fibres,
and the global Krenn--Gu conjecture remain **UNRESOLVED**.

## Normalized-family involutions

Use

```text
A=(1,1,0,0),  C=(1,-1,0,0),
B=(0,0,1,1),  D=(0,0,1,-1),

k=(1-r*t)/(t-r),
alpha=(A, A+k*D, A-C+B+r*D, -A-C+B+t*D),
beta =(B, B+C, C, C).
```

The evident mode-pair stabilizer of this normal form is a Klein four group.
Its two generators are

```text
U(v0,v1,v2,v3)=(-v1,-v0,v2,v3),
V(v0,v1,v2,v3)=( v0, v1,v3,v2).
```

The first is accompanied by row permutation `(2 3)` and sends
`(r,t)->(t,r)`; the second fixes the row order and sends
`(r,t)->(-r,-t)`.  On the two contractions, `U` exchanges the homogeneous
weight coordinates only for `D01`, while `V` does so only for `D23`.
Therefore neither preserves the common-weight incidence away from the
self-reciprocal weights.

Their product is the legal common-weight involution

```text
J(v0,v1,v2,v3)=(-v1,-v0,v3,v2).                  (1)
```

It permutes source modes by `(0 1)(2 3)` and changes the signs of modes zero
and one.  Since the permanent is invariant under column permutation and the
product of these two signs is `+1`, `J` preserves the permanent exactly.

Put

```text
(r',t')=(-t,-r),  rho=(0,1,3,2),
c=(-1,-1,1,1).
```

Then direct substitution gives, for every row `i`,

```text
J(alpha[rho[i]](r,t)) = c[i]*alpha[i](r',t'),
J(beta [rho[i]](r,t)) =      beta [i](r',t').      (2)
```

For the affine marking `beta_i+h_i*alpha_i`, equations (2) induce

```text
h' = (-h0,-h1,h3,h2).                             (3)
```

The extension coordinates transform invertibly as

```text
x' = (-x0,-x1,x3,x2,x4,x5,x7,x6).                (4)
```

All four transformations (1)--(4) are involutions.

## Homogeneous projected-tensor covariance

Write the common homogeneous weight as `[mu:nu]` and define

```text
D01(v,e;[mu:nu])=(mu*v0+nu*v1,v2,v3,e),
D23(v,e;[mu:nu])=(v0,v1,mu*v2+nu*v3,e).
```

For `q01=mu*v0+nu*v1` and `q23=mu*v2+nu*v3`, one has

```text
D01(J(v),e;[nu:mu])=(-q01,v3,v2,e),
D23(J(v),e;[nu:mu])=(-v1,-v0,q23,e).              (5)
```

The first projected permanent is multiplied by `-1`; the second is
unchanged.  Let `C^d_epsilon` be the coefficient of the binary row word
`epsilon`, with `0` selecting `alpha` and `1` selecting the marked beta row,
and put

```text
epsilon^rho=(epsilon0,epsilon1,epsilon3,epsilon2).
```

Equations (2)--(5) give the exact identities

```text
C^D01_epsilon(r',t',h';[nu:mu],x')
  = -(-1)^(epsilon0+epsilon1)
      C^D01_(epsilon^rho)(r,t,h;[mu:nu],x),

C^D23_epsilon(r',t',h';[nu:mu],x')
  =  (+1)(-1)^(epsilon0+epsilon1)
      C^D23_(epsilon^rho)(r,t,h;[mu:nu],x).        (6)
```

The primary and no-import audit check (6) for all sixteen row words in both
directions.  Hence all fourteen mixed equations, both pure diagonals, mixed
kernel existence, and pure-diagonal nonvanishing are preserved exactly.

On the finite chart `[lambda:1]`, the weight map is

```text
lambda -> 1/lambda
```

when `lambda!=0`.  Homogeneously, `lambda=0` and the projective weight are
exchanged, while `lambda=1,-1` are fixed.  Thus (6) covers the complete
projective weight line without losing an endpoint.

## Transfer to `t=0`

On the source divisor set `r=0` and write its parameter as `s=t`.  Under
`J`,

```text
(0,s) -> (-s,0).
```

If `r'=-s`, then

```text
r'*(r'-1)*(r'+1) = -s*(s-1)*(s+1).                (7)
```

Thus (7) gives an exact isomorphism

```text
Q[r',1/(r'*(r'-1)*(r'+1))]
  ~= Q[s,1/(s*(s-1)*(s+1))].
```

The marking, extension, and projective-weight maps are all bijective.
Applying (6) to the verified `r=0` constant-profile affine theorem therefore
proves
that the complete weighted-`H22` incidence on

```text
t=0,  r*(r-1)*(r+1)!=0
```

is empty.  The two source boundary fibres `r=0,t=+/-1` are closed separately
by exact nine-minor and endpoint-module certificates.  Applying (6) to those
two point theorems closes the special target fibres `t=0,r=-/+1`, whose
profile is `(3,3,3,3,4,4)`.  Hence the combined exact transfer closes

```text
t=0,  r!=0.
```

Only `r=0` remains outside this normalized target chart.  A discarded direct
target calculation using twenty-one selected minors is not a proof: after a
missing `r*D` row term was restored independently, both implementations gave
the non-unit result `RESULT:0:7:21`.  The present conclusion uses only the
replayed source theorems and the exact covariance (6).

## Replay

```powershell
uv run --with sympy python verify_p5_h22_common_center_kernel_star_component_r_zero_affine_constant_profile_open_obstruction.py
uv run --with sympy python audit_p5_h22_common_center_kernel_star_component_r_zero_affine_constant_profile_open_obstruction.py
uv run --with sympy python verify_p5_h22_common_center_kernel_star_component_r_zero_t_plus_minus_one_special_all_pair_obstruction.py
uv run --with sympy python audit_p5_h22_common_center_kernel_star_component_r_zero_t_plus_minus_one_special_all_pair_obstruction.py
uv run --with sympy python verify_p5_h22_common_center_kernel_star_component_r_t_divisor_symmetry_transfer.py
uv run --with sympy python audit_p5_h22_common_center_kernel_star_component_r_t_divisor_symmetry_transfer.py
```

The first four commands replay the source open and special-point
obstructions.  The last two verify the exact symmetry and transfer; the
audit rebuilds the rows and permanent tensor without repository imports.  No
finite-field computation is used.
