# Four-root torus-star equal-leaf survivor rank-eight full intrinsic Fitting nonzero point

## Status

**Exact characteristic-zero point/proper-open theorem (`GLD85`).** Work over
`K=Q(i)` and then extend scalars to `C`.  On one named `GLD84` rank-eight
Schur chart, the full intrinsic `GLD83` quadratic Fitting ideal has a
nonzero pullback: an explicitly pinned point satisfies the two Schur
residual equations, lies in the frame/gauge open, and has a nonzero
`45 x 45` maximal minor of the full intrinsic coefficient map.

Equivalently, the pullback of `I_Pl` to this six-leaf-variable/two-equation
rank-eight chart is **not the zero ideal**, and its vanishing locus is a
proper closed subset because the displayed point lies in `D(I_Pl)`.  This
does not say that the ideal is the unit ideal, and it does not say that the
intrinsic residual is empty.  The residual has not been shown empty or
excluded; `GLD85` exhibits one point outside it.

The old selected `GLD83` quotient determinant can vanish at the same point:
the old thirteen-row pivot has `gamma_old=0` and the exact old selected
`45 x 45` matrix `M_Pl` is zero.  This is a control showing why the full
intrinsic Fitting map is needed, not a contradiction or a new exclusion.

The global Krenn--Gu conjecture remains **UNRESOLVED**.  Other rank-eight
charts, rank-seven and lower-rank strata, other survivor components/gauges,
source branches, and all other graph/root profiles remain open.

Owning dependencies are the [`GLD83` bordered-Pluecker intrinsic Fitting
reduction](FOUR_ROOT_TORUS_STAR_SURVIVOR_BORDERED_PLUCKER_FITTING_OPEN_NONEXTENSION_THEOREM.md)
and the [`GLD84` center-rank Schur chart reduction](FOUR_ROOT_TORUS_STAR_EQUAL_LEAF_SURVIVOR_CENTER_RANK_DETERMINANTAL_CHART_REDUCTION_THEOREM.md).
The exact moving response circuit is the committed
`four_root_torus_star_survivor_moving_response_builder.py` used by the
primary verifier.

## 1. Exact obligation and named chart

Retain the `GLD83` scale-fixed equal-leaf base

```text
B = Spec K[x_0,...,x_14]/(g_0,...,g_9,x_8)
```

and write `c=(x_0,...,x_7)` and `z=(x_9,...,x_14)`.  On the `GLD84` chart
with row set

```text
R_8=(0,1,2,3,4,5,6,7),       mu_R = det A_R,
```

the ten survivor equations have the exact form `g=A(z)c+q(z)`.  The chart
is the localized six-variable/two-equation ring

```text
K[z,1/mu_R]/(rho_(R,8),rho_(R,9)),
rho_(R,k)=mu_R q_k-A_(k,*) adj(A_R)q_R.
```

The point is pinned by the following Gaussian-rational coordinates:

```text
z=(x_9,...,x_14)=(1,0,0,0,-2/3,0),
x_8=0,

c_0 =  4/5 -  8i/5       c_1 =  2/5 -  4i/5
c_2 = -6/5 + 12i/5       c_3 =-12/5 - 36i/5
c_4 =-12/5 -  6i/5       c_5 =  6/5 - 12i/5
c_6 = -6/5 - 18i/5       c_7 = -2   +  4i.
```

The exact Schur and frame values are

```text
mu_R                         = -140/9 - 20i/9 != 0,
rho_(R,8)=rho_(R,9)          = 0,
det(G)                       = -1 - i/3,
det(A_center)                = 1584/25 + 3312i/25,
d(F)=det(A_center)det(G)^3  = 256/3 - 448i/3,
delta_gauge                  = 1.
```

Thus this is a legal point of the named rank-eight Schur chart and of
`D(Omega)`.  The ten original survivor generators are also zero there;
the equality is checked by exact simplification, not floating-point
evaluation.

## 2. Full intrinsic Fitting map at the point

Let `C_F` be the transported `78 x 13` constant block and let
`w_0,w_1,w_2` be the transported response blocks, each linear in the nine
homogeneous coordinates `y=(u_0,...,u_7,s)`.  The primary reconstructs these
blocks from the committed adjugate tensor transport and the fixed nuisance
and invariant-kernel circuits.  Exact rank computation gives

```text
rank_K(C_F)=13.
```

At this point an exact row RREF of `C_F` uses the quotient pivot rows

```text
P=(0,1,2,3,4,5,7,8,12,17,19,26,52).
```

The ordered quotient rows are the complement in `0,...,77`, namely

```text
Q=(6,9,10,11,13,14,15,16,18,20,21,22,23,24,25,27,28,29,30,31,
   32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,
   53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,
   73,74,75,76,77).
```

After quotienting by the thirteen-dimensional constant image, the full
intrinsic coefficient map has `45` quadratic rows and

```text
3*binom(65,2)=6240
```

ordered columns.  The column order is response pairs `(0,1),(0,2),(1,2)`;
within each pair, quotient coordinate pairs `(a,b)` with `0<=a<b<65` in
lexicographic order.  The following forty-five zero-based columns are
pinned:

```text
(252,257,259,260,261,263,264,267,272,275,
 284,285,286,288,289,431,433,434,435,437,438,
 441,446,449,458,459,460,462,703,704,705,707,
 708,711,716,719,728,729,805,806,808,809,812,
 855,2784).
```

They form a `45 x 45` coefficient submatrix.  No numerical rank estimate is
used: the primary converts every exact Gaussian-rational entry to two
finite fields

```text
p_1=1,000,000,007,       p_2=10,000,019,
```

both prime and `3 mod 4`, so `F_p[i]` is a field.  For each prime it checks
all `3*78*9=2106` response Gaussian entries and `78*13=1014` constant
Gaussian entries.  Each of the `6240` real/imaginary rational denominator
slots is explicitly tested not to vanish modulo the prime.  The selected
determinant residues are

```text
det_45 mod p_1 =  9,639,769 + 249,939,722 i,
det_45 mod p_2 =  1,610,829 +   5,232,695 i,
```

and both are nonzero.  The companion certificate stores the two packed
matrices, their hashes, the pivot/quotient rows, and these residues.

### Theorem 2.1 (full intrinsic Fitting nonzero/properness)

The pullback of the `GLD83` full intrinsic ideal

```text
I_Pl = I_45(A_Pl) = Fitt_0(coker A_Pl)
```

to the named `GLD84` rank-eight chart is nonzero.  Its vanishing locus
`V(I_Pl)` is a proper closed subset of that chart: the pinned point belongs
to `D(I_Pl)`.

#### Proof

At a rank-thirteen constant block, quotienting the mixed response space by
`im(C_F)` identifies the intrinsic wedge coordinates
`C_F wedge w_c wedge w_d` with the `6240` quotient columns above, up to the
invertible basis changes and row/column signs allowed by `GLD83`.  Hence the
pinned `45 x 45` submatrix is a maximal minor of the full intrinsic map.

The primary computes this submatrix from exact `Q(i)` entries.  Its input
denominators are units at both displayed primes, so reduction is a defined
ring homomorphism.  If the exact determinant were zero in `Q(i)`, each
reduction would be zero.  The two explicitly nonzero residues therefore
prove that the exact determinant is nonzero.  This determinant is an element
of the pulled-back `I_Pl`, so that ideal is not the zero ideal and its
vanishing locus misses the pinned point. `square`

This is a characteristic-zero conclusion obtained through exact modular
certificates, not an unqualified numerical observation.

## 3. Old selected determinant control

For comparison, retain the old `GLD83` selected pivot rows

```text
I_old=(0,1,2,3,4,5,7,8,9,11,17,27,53),
J_old={0,...,77} \\ I_old.
```

Using the same forty-five descriptors as `GLD82`/`GLD83`, the exact point
has

```text
gamma_old=det(C_F[I_old])=0,
M_Pl(point)=0_(45 x 45).
```

The primary evaluates each descriptor by an exact local Schur complement:
eighteen descriptor row sets already have constant rank below thirteen, and
the remaining twenty-seven exact coefficient vectors also vanish.  Thus the
old selected matrix can vanish even though the full intrinsic Fitting map
has a nonzero maximal minor.  This control uses no floating-point or
modular inference.

The old `M_Pl` is only one coordinate selection from the full exterior
family.  Its vanishing is not a surviving response, a counterexample, or a
claim that `I_Pl` vanishes.

## 4. Verification and independent audit

Run the derivation-side verifier:

```powershell
python claims/arbitrary-order/verify_four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_nonzero.py
```

It loads the committed moving-response builder, reconstructs the exact
survivor point and Schur equations, checks the frame open and
`rank(C_F)=13`, evaluates the old selected matrix, forms the full quotient
map, checks every exact denominator slot at both primes, and matches the
selected determinant against the pinned certificate.

Run the genuinely separate no-import arithmetic audit:

```powershell
python -I claims/arbitrary-order/audit_four_root_torus_star_equal_leaf_survivor_rank_eight_full_intrinsic_fitting_nonzero.py
```

The audit imports no repository Python module, SymPy, primary verifier, or
moving builder.  It independently decodes the packed `45 x 45` matrices,
checks their dimensions, hashes, point/row/column metadata and denominator
records, and recomputes both Gaussian-extension determinants using its own
standard-library elimination.  Its scope is the modular witness arithmetic;
the primary is responsible for deriving that witness from the exact
GLD75--GLD76 circuit.  This division is intentional and is not presented as
two independent derivations of the same transport matrices.

## 5. Scope fences and next obligation

`GLD85` proves only that the intrinsic Fitting-open complement is nonempty
on one named rank-eight chart.  In particular:

- `V(I_Pl)` has not been proved empty, nonempty, or excluded; the point is
  outside it, and no residual point is supplied here.
- The result does not prove that the rank-eight chart, or its two-equation
  model, is empty.  It supplies a further principal-open exclusion available
  to the `GLD83` response theorem.
- The other `44` rank-eight row charts, all `960` rank-seven charts, and the
  rank-at-most-six branch from `GLD84` are untouched.
- Other equal-leaf components/gauges, lower-support or isotropic boundaries,
  triangles, smaller survivor families, off-chart source branches, other
  roots and orders, and the global source-integration/gluing problem remain
  open.
- The nonzero point does not alter the global status: the Krenn--Gu
  conjecture is **UNRESOLVED**.

The next load-bearing obligation is a chart-level ideal calculation: decide
whether the pullback of `I_Pl` is the unit ideal, has additional components,
or leaves an exact residual on this rank-eight chart, then repeat on the
rank-seven and lower-rank branches.  A single further maximal minor would
only enlarge the known principal-open exclusion; it would not close the
intrinsic residual or the global conjecture.
