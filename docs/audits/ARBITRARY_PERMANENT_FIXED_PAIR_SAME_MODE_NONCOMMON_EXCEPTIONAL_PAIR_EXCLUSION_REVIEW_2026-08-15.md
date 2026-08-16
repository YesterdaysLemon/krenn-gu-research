# Hostile review of fixed-pair same-mode noncommon exceptional-pair exclusion

## Verdict and exact scope

**PASS, for the stated fixed-pair, pointwise, characteristic-zero,
same-mode, cross-family, noncommon-exceptional-line scope.**  No tensor-slot,
kernel-dimension, line-pair, scaling, normal-form, active-colour, field,
quantifier, dependency, implementation, or scope blocker survived hostile
review.

If one remaining local plane contains a `Phi_1` low and a `Phi_2` low and
neither ambient kernel line is the common line

```text
N=K(x_2+x_3),
```

the package excludes all four possible noncommon line pairs.  Two pairs are
inconsistent with the unique zero local-colour row.  The other two force
exact codimension-two local normal forms; their two surviving diagonal
colours then make all other-mode `A=span{x_4,x_5}` columns at the missing
colour vanish, leaving only one input slot capable of supplying `x_4` or
`x_5`.

The argument contracts only once in the shared local mode.  It does not use
the distinct-mode double-contraction equation with two vectors from that
mode.  The branches `N` plus a non-`N` line and `N` paired with itself remain
open, as do distinct-mode residual incidences not closed by earlier
packages.  Unrestricted `P_6 -> Delta_3` nonrestriction remains unknown, and
the global Krenn--Gu conjecture remains **UNRESOLVED**.

Reviewed package:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_SAME_MODE_NONCOMMON_EXCEPTIONAL_PAIR_EXCLUSION.md
  verify_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py
  audit_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py
```

Load-bearing frozen predecessors:

```text
claims/arbitrary-order/
  ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md
  ARBITRARY_PERMANENT_FIXED_PAIR_EXCEPTIONAL_KERNEL_NECESSITY_THEOREM.md
```

The adjacent distinct-mode boundary was checked against
`ARBITRARY_PERMANENT_FIXED_PAIR_SUPPORT_TWO_LOW_DOUBLE_CONTRACTION_INCIDENCE_THEOREM.md`.
That theorem is not imported into the same-mode proof, and its explicitly
forbidden same-slot use is not repeated here.

## 1. Legal one-slot contraction and the `Theta` kernel

Split the ambient space as

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5}.
```

For each residual quadratic `g_j` let `B_j:R -> R^*` be its polarized
contraction map.  If the shared mode is `t` and the other three modes are
`s,u,v`, define

```text
Theta(ell)(z_s,z_u,z_v)
 =[x_0x_1x_2x_3x_4x_5](x_4x_5 ell)z_sz_uz_v.
```

This construction removes mode `t` exactly once.  Both vectors `p,q` from
`L_t` are used only to derive separate identities for this one linear map
`Theta`; they are never inserted into two tensor slots simultaneously.

For fixed representatives

```text
p in {A_0,C_0},                 q in {A_1,C_1},
```

direct polarization gives

```text
B_(m_2)p=h_2,             B_(m_1)q=h_2',
```

while the other applicable mixed contractions vanish.  Since both mixed
target tensors vanish,

```text
U:=span{h_2,h_2'} subset ker Theta,            dim U=2.
```

Write the local coordinate columns of `p,q` as `alpha,beta`, put
`r_c=(alpha_c,beta_c)`, and let `I={c:r_c!=0}`.  Because `p,q` are
independent and the local triple is a basis, the three rows `r_c` span the
two-dimensional dual of `span{p,q}`.  Hence `|I|>=2`.

For every `c in I`, the exact diagonal target equation supplies a nonzero
multiple of the independent tensor

```text
tau_c=e_c^* tensor e_c^* tensor e_c^*
```

in `im Theta`.  Thus

```text
rank Theta>=|I|,              dim ker Theta<=4-|I|.
```

The two-dimensional subspace `U` in the kernel excludes `|I|=3`.  Therefore

```text
|I|=2,               ker Theta=U,              rank Theta=2.
```

For

```text
z_c=beta_c p-alpha_c q,
```

the local colour covector `f_c` vanishes, so the diagonal target gives

```text
B_(d_c)z_c in U.
```

If `r_c=0`, the same identity holds for the full two-space
`B_(d_c)span{p,q}`.  This is the only contraction bridge used in the four
line cases.

## 2. Independent contraction-table and quotient check

Re-expanding the five factorized quadratics gives

```text
line   B_(m_1) B_(m_2) B_(d_0) B_(d_1) B_(d_2)

A_0       0       h_2       0      w_1    -2x_1
C_0       0       h_2      w_0      0     -2x_1
A_1      h_2'      0      -w_0      0     -2x_0
C_1      h_2'      0        0     -w_1    -2x_0.
```

In `R^*/U`, the map

```text
(v_0,v_1,v_2,v_3) |-> (v_0+v_1,v_2+v_3)
```

has kernel exactly `U`.  It sends each of `w_0,w_1,x_0,x_1` to a nonzero
class and gives

```text
U intersect span{x_0,x_1}=K(x_0-x_1).
```

These facts independently reproduce every membership and nonmembership used
in the package.

For `(A_0,A_1)`, the forced local zeros are
`alpha_0=beta_1=0`.  If the unique zero row is respectively `0`, `1`, or
`2`, the zero-row consequence would put `-w_0`, `w_1`, or `-2x_1` in `U`.
All three are impossible.  For `(C_0,C_1)`, the zeros
`alpha_1=beta_0=0` similarly produce `w_0`, `-w_1`, or `-2x_1` outside
`U`.  This exhausts the first two line pairs without a genericity
assumption.

## 3. Correct scaling and the two exact normal forms

For `(A_0,C_1)`, both lines miss local colour zero.  It is therefore the
unique zero row.  With the displayed ambient generators fixed, write

```text
alpha=(0,a,b),             beta=(0,c,d),
ad-bc!=0.
```

The colour-one and colour-two kernel combinations give, modulo `U`,

```text
B_(d_1)(c p-a q)=(a+c)w_1,
B_(d_2)(d p-b q)=2b x_0-2d x_1.
```

The quotient calculation forces

```text
c=-a,                 d=b.
```

Consequently `ad-bc=2ab`, so characteristic zero and independence imply
`a,b!=0`.  Solving the local coordinate equations, without rescaling either
ambient generator separately, yields

```text
y_(t,1)=(p-q)/(2a) in R,
y_(t,2)=(p+q)/(2b) in R.
```

Thus only the colour-zero column of mode `t` can have a nonzero
`A`-projection.

For `(C_0,A_1)`, direct calculation rather than an unstated symmetry gives

```text
alpha=(a,0,b),             beta=(c,0,d),
B_(d_0)(c p-a q)=(a+c)w_0,
B_(d_2)(d p-b q)=2b x_0-2d x_1.
```

The same quotient forces `c=-a`, `d=b`, and `2ab!=0`, hence

```text
y_(t,0)=(p-q)/(2a) in R,
y_(t,2)=(p+q)/(2b) in R.
```

Only the colour-one column can have a nonzero `A`-projection in this case.

The scaling covariance was also checked directly.  Replacing the two
ambient representatives by `sp,tq` replaces their local coordinate columns
by `s alpha,t beta`; every kernel combination and every contracted
covector is multiplied by the common nonzero scalar `st`.  The proof does
not normalize the columns while illicitly holding the ambient generators
fixed.

## 4. Two-active-colour lemma

For `y=(r(y),a(y)) in R direct-sum A`, put

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)),
```

where `J` is the nondegenerate hyperbolic form on the two-space `A`.
Because `im Theta` is exactly the span of the two active diagonal tensors,
`C` vanishes at every other colour cell on the remaining three modes and is
nonzero at both active diagonal cells.

For two distinct remaining modes and two distinct colours `i!=j`, the map

```text
w |-> C(y_(s,i),y_(u,j),w): R direct-sum A -> R
```

kills the three-dimensional third local plane.  Its rank is at most three.
On the four-dimensional `R`-summand it is scalar multiplication by

```text
J(a(y_(s,i)),a(y_(u,j))).
```

A nonzero scalar would give rank four, so all cross-colour, cross-mode
pairings vanish.  This is again a one-slot rank argument, not a double
contraction in mode `t`.

The remaining two-dimensional case split is exhaustive:

1. If every remaining mode has `A`-rank at most one, one active colour
   forces both endpoint modes to support only that colour.  A second active
   pair among three modes shares an endpoint and cannot use another colour.
2. Otherwise choose two independent `A`-columns in one mode.  The column at
   the third colour vanishes in each other mode because it is orthogonal to
   both.  Hence the two active colours must be the colours of the independent
   columns.  Activity supplies a nonzero outside column at each of those
   colours.  They lie on the two distinct orthogonal-complement lines of the
   independent columns, so they are independent.  The first mode's
   third-colour column is orthogonal to both and therefore vanishes.

Thus, when exactly two colours are active, all three columns at the missing
colour have zero `A`-projection.  This argument uses only nondegeneracy and
two-dimensional linear algebra; it does not diagonalize `J` or require an
algebraically closed field.

## 5. Final supplier contradiction

In the `(A_0,C_1)` normal form, colours `1` and `2` are active.  The lemma
annihilates the colour-zero `A`-columns in the other three modes, while the
normal form says that only the colour-zero column in the shared mode can
have an `A`-part.  Therefore at most one of the four pure-colour-zero inputs
can supply either `x_4` or `x_5`.

Every polarization term of

```text
star(d_0)=x_4x_5(x_1+x_2)(x_3-x_0)
```

assigns its four linear factors to four distinct input slots.  In particular,
the factors `x_4` and `x_5` must be supplied by two distinct inputs.  With
only one possible `A` supplier, the pure colour-zero coefficient is zero,
contradicting `lambda_0!=0`.

The `(C_0,A_1)` normal form is identical with colours `0` and `2` active:
the three other colour-one `A`-columns vanish, only the shared mode can
supply an `A` factor, and the pure `d_1` coefficient contradicts
`lambda_1!=0`.

## 6. Quantifier, dependency, and boundary audit

Characteristic zero is sufficient.  The proof uses `2!=0`, divides only by
the explicitly nonzero values `2a` and `2b`, and uses finite-dimensional
rank-nullity and a nondegenerate two-dimensional bilinear form.  It uses no
order, positivity, square root, algebraic closure, or unasserted genericity.

The kernel-support predecessor supplies the exact forced missing-colour
zeros on the four noncommon exceptional lines.  The exceptional-kernel
predecessor is needed only to reduce an arbitrary rank-two local kernel to
the finite exceptional list.  The two-sided predecessor supplies the
existence of a low mode in each family but does not force the two modes to
coincide.  None of these facts proves that a same-mode incidence exists.

The ambient intersection of the two projection kernels is exactly `K N`.
Hence the four reviewed noncommon pairs are independent and exhaustive when
both same-mode kernel lines differ from `N`.  The proof says nothing against

```text
(N,A_1), (N,C_1), (A_0,N), (C_0,N), or (N,N)
```

in one local plane.  It also does not reuse this argument for distinct
modes.  The theorem, both executable reports, and this review retain those
open branches explicitly.

## 7. Computational replay and independence

Focused replay passed:

```text
new primary exact verifier:                         PASS;
new independent no-import audit:                    PASS;
kernel-support predecessor primary and audit:       PASS;
exceptional-kernel predecessor primary and audit:   PASS;
two-sided projection-drop primary and audit:        PASS;
distinct-mode incidence primary and audit:          PASS;
py_compile on new and predecessor scripts:          PASS;
Ruff on new and predecessor scripts:                PASS;
tracked and untracked whitespace checks:             PASS.
```

The new primary verifier uses SymPy to derive the contraction table from the
five factorized quadratics, checks the quotient by `U`, exhausts the six
immediate zero-row cases, derives both symbolic normal forms, verifies
projective scaling covariance, and checks the rank-four and one-supplier
gates.

The independent audit imports neither the primary module nor SymPy.  It
reconstructs the quadratics as edge dictionaries, uses exact rational row
reduction and contraction, checks both normal forms at independent rational
samples, verifies scaling covariance separately, and exhausts the
two-active-colour lemma over `F_3` and `F_5`.  The finite-field runs found
respectively `186` and `426` two-active compatible profiles, all with the
third-colour columns zero.  They audit the displayed finite algebra; the
written characteristic-zero argument proves the theorem.

## 8. Accepted boundary

```text
same mode, A_0 x A_1:                                  EXCLUDED;
same mode, C_0 x C_1:                                  EXCLUDED;
same mode, A_0 x C_1:             NORMAL FORM THEN EXCLUDED;
same mode, C_0 x A_1:             NORMAL FORM THEN EXCLUDED;
same mode, N plus a non-N line:                         OPEN;
same mode, N paired with itself:                        OPEN;
distinct-mode exceptional incidences:     NOT RECLASSIFIED HERE;
unrestricted P_6 -> Delta_3:                         UNKNOWN;
global Krenn--Gu conjecture:                         UNRESOLVED.
```

## Final reviewed hashes

```text
new theorem:
BC8851D171C140163259385135B81F9A52567B57D36912C682CD181061966B68

new primary verifier:
3DAA56B1D51CFC9BF5465A4B52D773112CE06FCB1C2AFF57D0F6AE3B3DEF4F2B

new independent audit:
6C6D6955F1C5407DDBF680CDE6D19D1C4DA00C20A539EFFE47EC54A369A18E69

kernel-support predecessor theorem:
7AEC9CD00DEBAC1D5CFA91D44E5D3634BD6D05FF8CA755BA1C2E83D1F8C3C45B

exceptional-kernel predecessor theorem:
2FAB590264EDE5999F55540F2234BE2055637386B978D77469F592F58B004B60

two-sided projection-drop predecessor theorem:
A383731E094E0D0E45482AAB889FB8B202FC7A2CF452D8534D5035E737089F36

distinct-mode support-two incidence theorem:
8C6B0EB9AA3BDD885A0703AB1EE902456045A7DEA89B66E0C097654F1189631F
```
