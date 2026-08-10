# Component twenty-one `q=+/-p` shared-branch ternary obstruction

## Status

**Exact characteristic-zero generic-divisor theorem.**  On either divisor
`q=epsilon*p`, where `epsilon=+1` or `-1`, assume

```text
p*(ell^2-1) != 0.                                  (1)
```

Over `Q(p,kappa,ell)`, for every homogeneous weight, the complete genuine
shared `D01`-pure/`D23`-binary incidence is either empty or has the unique marking

```text
h0=-epsilon*ell/(p*(ell+epsilon)),
h1=-1/(ell+epsilon),
h2=epsilon*kappa,
h3=0.                                               (2)
```

Every extension on (2) has a rank-four one-marked `D23` map, so none lifts
to a ternary weighted-`H22` local map.  Thus the generic weighted-`H22`
fibre is empty on both sign divisors.

The intersections `ell=+/-1` are not covered.  At an admissible one of
these intersections the shared kernel can jump when `kappa=0`, so they
remain **UNKNOWN** rather than being removed by a denominator convention.
The simultaneous `p=q=0` intersection is outside this normalized pure-`P4`
chart and remains separate.  No arbitrary ambient/source/projective-order or
global claim is made.  The global Krenn--Gu conjecture remains **UNRESOLVED**.

## Exact shared-incidence projection

Use the component-twenty-one bases

```text
A=(1,1,0,0), C=(1,-1,0,0), B=(0,0,1,1), D=(0,0,1,-1),
r00=A+pB, r01=C+qB,

alpha=(q*r00-p*r01, ell*A+C, C, D),
beta =(r00, A, B+kappa*A, A+ell*C).                 (3)
```

Only the pure coefficient `T_1111=4p` is nonzero.  The homogeneous all-alpha
`D01` diagonal is identically zero by Hall deficiency, so `D01` cannot be
the binary member of a weighted-`H22` pair.  It remains to classify the
orientation in which `D01` is nonzero pure and `D23` is genuinely binary.

Over the function field `Q(p,kappa,ell)`, for finite weight `[lambda:1]`,
impose the fifteen unwanted `D01`
coefficients, normalize its all-beta diagonal, impose the fourteen mixed
`D23` coefficients, and invert both `D23` diagonals.  Exact saturated
elimination of the shared extension gives, for either sign,

```text
< h3,
  h2-epsilon*kappa,
  (ell+epsilon)h1+1,
  p(ell+epsilon)h0+epsilon*ell >.                  (4)
```

The projective endpoint `[1:0]` gives the same ideal.  Bidirectional
standard-basis reduction against (4) certifies equality, rather than only
containment or a sampled solution.

## Complete common extension kernel

On (2), stack the fifteen unwanted `D01` rows and fourteen mixed `D23` rows
in a `29 x 8` matrix `M`.  Rows `0,...,14` are the lexicographically ordered
`D01` words other than `1111`; rows `15,...,28` are the lexicographically
ordered mixed `D23` words.  Columns are the eight extension entries in
alpha/beta order.  Put

```text
v_epsilon=(-epsilon*p*(ell+epsilon),0,epsilon*ell,0;
            0,epsilon,kappa*(ell-epsilon),0).       (5)
```

Direct expansion gives `M*v_epsilon=0` in both weight charts.  The following
fixed `7 x 7` minors prove that this is the complete kernel on (1).  Every
listed minor uses columns `0123467`.

For `epsilon=+1`, finite weight, rows `11,14,16,17,18,22,26` give

```text
512 p^4 (lambda-1)^4 (lambda+1) (ell-1)/(ell+1).   (6)
```

For `epsilon=-1`, finite weight, the same rows give

```text
-512 lambda^2 p^4 (lambda-1)^4 (lambda+1)
      (ell+1)/(ell-1),                              (7)
```

while rows `10,11,16,18,22,23,26` give

```text
128 p^4 (lambda-1)^4 (lambda+1)^2 (ell+1) H,
H=lambda*ell+lambda+ell-1.                         (8)
```

If (7) and (8) both vanished away from the displayed open factors, then
`lambda=0` and `H=ell-1=0`, contradicting (1).  At weight infinity the rows
`10,11,16,18,22,23,26` for sign plus and
`10,11,16,17,18,22,26` for sign minus give respectively

```text
128 p^4 (ell-1)(ell+1),
-256 p^4 (ell+1)^2.                                (9)
```

Consequently `rank(M)=7` and `ker(M)=C v_epsilon`.  Notice that these
certificates do not invert `kappa`; the same complete kernel and obstruction
therefore hold after specializing the displayed branch to `kappa=0`.

## Binary genuineness and ternary obstruction

Write a common extension as `z=C0*v_epsilon` and put

```text
F=lambda*ell+lambda-ell+1.                         (10)
```

On the finite chart, the required diagonals are

```text
B01 = 2 epsilon C0 p F,
A23 = 2 C0 p (ell+epsilon)^2 (lambda-1),
B23 = -2 C0 (ell-epsilon)(lambda+1).               (11)
```

Thus a genuine point has

```text
C0*p*(ell^2-1)*(lambda^2-1)*F != 0.                (12)
```

At weight infinity the same diagonals are

```text
B01 = 2 epsilon C0 p (ell+1),
A23 = 2 C0 p (ell+epsilon)^2,
B23 = -2 C0 (ell-epsilon),                         (13)
```

and are all nonzero exactly on the corresponding open in (1) with `C0!=0`.

For the `D23` one-marked map in mode three, the fixed rows `0,1,4,7` have
determinant

```text
8 C0^3 p^3 (ell+epsilon)^3 (ell-epsilon)^2
  * (lambda+1)^3                                  (finite),
8 C0^3 p^3 (ell+epsilon)^3 (ell-epsilon)^2         (infinity). (14)
```

This is nonzero at every genuine shared point.  Hence the one-marked map has
rank four, whereas a ternary local factorization requires rank at most three.
The apparent binary branches on `q=+p` and `q=-p` are therefore exact
structured false positives, not counterexample fibres.

## Replay and boundaries

```text
uv run --with sympy python verify_p5_component21_q_plus_minus_p_shared_branch_ternary_obstruction.py
uv run --with sympy python audit_p5_component21_q_plus_minus_p_shared_branch_ternary_obstruction.py
```

The primary performs all four characteristic-zero saturated eliminations,
checks the complete symbolic kernels, fixed rank minors, diagonals, and
one-marked determinants.  The audit imports no repository mathematics and
independently reconstructs the permanents and certificates before replaying
the primary.  No finite-field computation is used.

Still **UNKNOWN** here: both `ell=+/-1` intersections, any additional
specialization-only branches at `kappa=0`, other component-twenty-one
parameter divisors not already covered by separate theorems, arbitrary
source order, and the global conjecture.
