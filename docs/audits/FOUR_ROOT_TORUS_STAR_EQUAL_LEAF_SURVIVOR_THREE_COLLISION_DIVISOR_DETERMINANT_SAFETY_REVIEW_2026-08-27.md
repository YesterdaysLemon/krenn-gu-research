# Hostile review: equal-leaf survivor three-collision-divisor safety

Date: 2026-08-27

## Verdict

Accept `GLD87` as an exact characteristic-zero, set-theoretic theorem on the
displayed complete scale-fixed equal-leaf chart. Its conclusion is that a
rank-at-most-six incidence on any of `H_1`, `H_2`, or `H_3` has singular center
matrix. Therefore those three divisors are excluded only on the retained
determinant-safe open where `det(G)det(C) != 0` (in particular on the
normalized `D(Omega)` of `GLD83`).

Do **not** read this as an H4 result. `H_4` remains the named low-rank
candidate in this chart, and no pulled-back `GLD83` Fitting ideal is computed.
The global Krenn--Gu conjecture remains **UNRESOLVED**.

## H1 algebraic controls

The actual leaf variables are

```text
G=[1 1 1; p q s; a b c],
```

with `b,c` translated by one from the shifted variables in the GLD86 chart.
On `H_1`, `q=p` and `det(G)=(p-s)(b-a)`. Thus the theorem's use of
`p!=s` and `a!=b` is exactly the leaf-invertibility gate, not an unannounced
genericity assumption.

The primary verifier reconstructs the fixed 37-row GLD71 map and selects
rows `(0,1,2,17,19,25,28,31,32,33,34)`. The blockwise matrix `T_0` has
determinant one. It checks the displayed base block and difference block
entry-for-entry. All `37` nonzero base 4-minors are divided by `p-s`; their
lexicographic Groebner basis is

```text
p-2s^3+3s^2-2s,
s(s-1)(s^2-s+1).
```

The three displayed difference 3-minors have gcd one in `Q[p]`, so their
difference block has rank three at every characteristic-zero specialization.
The block-triangular minor argument therefore leaves, off `p=s`, only

```text
p=1-s,  s^2-s+1=0.
```

On that quotient, the exact selected 7-minor is
`-648(a-b)^3(c*s+c-s)`. Rank at most six forces
`c=s/(s+1)=(s+1)/3`; `s+1` is a unit modulo the Eisenstein relation. The
selected 6-minor is `36(a-b)^3(2s-1)`, nonzero in characteristic zero. Each
of the three root blocks annihilates

```text
(3b+s-2, -3(a-b), 3(a-b)),
```

so the selected matrix has rank six and exactly a one-dimensional kernel in
each block. Applying the inverse unimodular block change preserves the fact
that all three center rows are proportional. Thus every compatible center is
singular. The proof uses only a row submatrix; it does not assume the eleven
rows span all 37 syndrome rows.

The no-import audit independently rebuilds these eleven rows with a separate
sparse polynomial implementation over `Q`, recomputes all base minors,
checks the gcd and both exceptional determinants, and rechecks the complete
kernel identities. It does not import GLD71, GLD75, GLD86, or SymPy.

## H2/H3 transport control

The primary verifier checks the exact symbolic covariance for both leaf-column
transpositions:

```text
M(GP)=M(G) P_blk.
```

The same block permutation transports a center kernel to the permuted frame;
its determinant changes only by `det(P)=+-1`, and leaf determinant nonvanishing
is preserved. Swapping columns two/three maps `p=q` to `p=s`; swapping one/
three maps `p=q` to `q=s`. Hence the H1 singular-center conclusion transfers
to H2 and H3 without dividing by a collision factor.

## Incidence, scale, and Omega audit

The package relies on the already exact GLD86 bridge

```text
B=0 iff M(G) C=0,
```

and its differentiated identity

```text
rank A_lin=rank M(G)[:,0:8]
```

on `B`. The scale-fixed coordinate is `C_8=1`, which is needed upstream to
turn a zero syndrome into the column-replacement rank argument. No derivative
of a certificate matrix is silently retained: at an incidence-zero point it
is multiplied by a vanishing equation vector.

`GLD83` defines the normalized frame/gauge factor with
`Omega=delta_gauge det(C)det(G)^3`. Consequently the explicit
determinant-safe theorem applies on `D(Omega)` in the displayed gauge, while
the proof itself states `det(G)det(C)!=0` so the open condition is visible.
This is the precise refinement of GLD86's four-divisor containment; it does
not claim that the raw H1/H2/H3 intersections are empty before the center
determinant gate.

## Rejected stronger readings

- `GLD87` does not analyze, exclude, or compute the H4 branch.
- It does not compute the `GLD83` pulled-back Fitting ideal or prove a unit
  certificate for that ideal.
- It does not claim that the three raw divisor intersections are empty; the
  H1 residual calculation explicitly exhibits a singular-center boundary.
- It does not transfer the result to unequal leaves, another gauge or
  survivor component, another source presentation, triangles, another root,
  another support profile, or the global conjecture.
- The `A_lin` center coefficient matrix is not the actual center frame `C`;
  the proof keeps those symbols distinct.
- Exact characteristic-zero identities are not finite-field evidence or a
  numerical rank claim.

## Verification commands

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_three_collision_divisor_determinant_safety.py
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_three_collision_divisor_determinant_safety.py
```

Both scripts report the global status `UNRESOLVED`, state that H4 is not
analyzed, and leave the Fitting pullback open.

## Proof-tree delta

`GLD86` supplied

```text
B intersect V(I_7(A_lin)) subseteq V(H_1 H_2 H_3 H_4).
```

`GLD87` adds the exact determinant-safe edge

```text
GLD86 -> GLD87 -> (H4 residual / Fitting / remaining global cover).
```

The next load-bearing task is the divisor-specific `GLD83` Fitting pullback
on `H_4 intersect D(Omega)`, retaining raw response incidence at every
`C_F` rank drop. No global status change is justified.
