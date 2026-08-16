# Arbitrary permanent triangle-pair same-mode two-low exclusion

## Status

This note proves an exact characteristic-zero exclusion inside the
simultaneous projection-drop residual for the displayed Delta-admissible
`(3,1)` triangle pair.  No remaining local plane can have rank two under
both mixed-factor projection families.

The predecessor kernel boundary leaves only five ambient kernel lines:

```text
Phi_1: N=x_1+x_2, B=x_0+x_2, C=x_0-x_1,
Phi_2: N=x_1+x_2, S=x_3.                                (1)
```

Rank-nullity removes the common/noncommon same-mode pairs.  A legal
single-slot contraction excludes `B/S` and `C/S`.  The proportional `N/N`
case needs more: every occurrence of `N` propagates to a singleton `x_3`
in another mode; the two-low zero-permanent profiles are impossible; and
the only resulting three-low cycle dies by an exact two-by-two pure-tensor
gate together with the previously unused all-colour-zero diagonal slice.

The proof never inserts two vectors from one local plane into two different
tensor slots.  It does not exclude all distinct-mode low incidences and does
not prove unrestricted permanent nonrestriction.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Exact setup and predecessor boundary

Let `K` be a field of characteristic zero and put

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

For the triangle pair, define

```text
ell_1=x_2-x_1-x_0,                   ell_2=x_2-x_1,
Phi_1=(x_3,x_4,x_5,ell_1),           Phi_2=(x_0,x_4,x_5,ell_2). (2)
```

The two mixed and three diagonal complementary quartics are

```text
F_1=x_4x_5 x_3 ell_1,                F_2=x_4x_5 x_0 ell_2,
D_0=2x_4x_5 x_0x_3,
D_1= x_4x_5 x_2(x_0+x_1),
D_2= x_4x_5 x_1(x_0-x_2).                              (3)
```

Let ordered independent triples span local planes `L_2,...,L_5`, and
assume the exact target equations

```text
T_(F_1)=T_(F_2)=0,
T_(D_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (4)
```

The triangle kernel-boundary predecessor proves that every restricted map
has rank at least two and that every low kernel line is among (1).  Its
forced local supports are

```text
N subset {1,2},        B subset {0,1},        C subset {0,2},
S exactly {0}.                                             (5)
```

Here and below, a line name also denotes its displayed generator.

## 2. The noncommon same-mode pairs

If a local plane contains `N`, then `N` lies in both ambient projection
kernels.  The rank-two floor says that each local kernel intersection has
dimension at most one.  Thus `N` cannot share its mode with `S`, `B`, or
`C` as a second projection-kernel line.  Only `N/N`, `B/S`, and `C/S`
remain.

Suppose one mode contains `p in {B,C}` and `q=S`.  Let `Theta:R^*` map a
residual covector to its `x_4x_5` three-mode tensor on the other local
planes, where

```text
R=span{x_0,x_1,x_2,x_3},                Q=ker Theta.     (6)
```

The legal single contractions of the two mixed channels are

```text
i_p F_2=x_4x_5(x_0-x_1+x_2),
i_q F_1=x_4x_5(-x_0-x_1+x_2).                            (7)
```

Hence the independent covectors in (7) span a two-plane `U subset Q`.
Write the local coordinate rows of `p,q` as `alpha,beta`.  Equation (5)
gives

```text
beta=(beta_0,0,0),             beta_0!=0,

p=B: alpha=(alpha_0,alpha_1,0), alpha_1!=0,
p=C: alpha=(alpha_0,0,alpha_2), alpha_2!=0.              (8)
```

Thus exactly two local coordinate rows on `span{p,q}` are nonzero.  Their
two independent diagonal target tensors lie in `im Theta`, so

```text
rank Theta>=2,                    dim Q<=2.
```

Together with `U subset Q`, this gives `Q=U`.  The vector

```text
z_0=beta_0 p-alpha_0q
```

has zero local colour-zero coordinate.  Therefore the contracted `D_0`
residual must lie in `Q`.  But

```text
i_p D_0=2x_4x_5x_3,                i_qD_0=2x_4x_5x_0,
```

so this would put

```text
beta_0x_3-alpha_0x_0 in
span{x_0-x_1+x_2,-x_0-x_1+x_2}.                         (9)
```

The right side has zero `x_3` coefficient, contradicting `beta_0!=0`.
Both `B/S` and `C/S` are excluded.

## 3. Every `N` propagates to a singleton `S`

It remains to exclude a local common kernel `N/N`.  Contracting (3) once
with `N` leaves

```text
F_1=F_2=D_0=0,
D_1=x_4x_5h_+,                    D_2=x_4x_5h_-,
h_+=x_0+x_1+x_2,                 h_-=x_0-x_1-x_2.       (10)
```

The common residual kernel is

```text
H=ann_R(h_+,h_-)=span{x_1-x_2,x_3}.                    (11)
```

### Lemma 1 (propagation to `H`)

Some other local plane meets `H` nontrivially.

### Proof

If `N` is singleton-supported, suppose all other local planes were disjoint
from `H`.  Their images in

```text
(R/H) direct-sum span{x_4,x_5}
```

would remain three-dimensional.  Equation (10) would give exactly one
nonzero diagonal of the standard `D direct-sum A` contraction tensor.
The one-diagonal lemma applies because `dim(R/H)=2`: an off-diagonal slice
kills a three-plane but a nonzero `J`-scalar has rank two on `R/H`; the two
other local vectors in a suitable mode are then forced onto one
one-dimensional `J`-orthogonal line, contradicting their independence.

If `N` has support `{1,2}`, the same quotient tensor has exactly two active
colours.  Cross-colour orthogonality in the two-space
`A=span{x_4,x_5}` forces every colour-zero `A`-column in the other three
modes to vanish.  The removed kernel vector is pure `R`, so in the original
all-colour-zero `D_0` coefficient only the removed mode could supply an
`A` factor.  It cannot supply both `x_4` and `x_5`; this contradicts
`lambda_0!=0`.  Thus one of the other planes meets `H` in either support
case.  This proves the lemma.

Take a nonzero propagated vector

```text
q=s(x_1-x_2)+t x_3.                                     (12)
```

Suppressing `x_4x_5`, its five residual covectors are

```text
F_1=t ell_1-2s x_3,             F_2=-2s x_0,
D_0=2t x_0,                     D_1=s ell_1,
D_2=-s ell_1.                                           (13)
```

If `s!=0`, the `D_1,D_2` tensors in (13) are negatives of one tensor but
have disjoint target supports.  Both local coefficients of `q` at colours
`1,2` therefore vanish.  Its colour-zero coefficient is nonzero.  The
zero `F_2` tensor then kills the `x_0` residual.  If `t!=0`, this contradicts
the live `D_0` tensor; if `t=0`, `D_0` itself is identically zero and gives
the same contradiction.  Hence `s=0`.

Now `q=tx_3`, with `t!=0`.  The zero `D_1,D_2` residuals force its local
colour-`1,2` coefficients to vanish.  Thus a local `N` always propagates,
in a distinct mode, to

```text
S=x_3                 singleton-supported at colour 0. (14)
```

## 4. Two `Phi_2` lows are not enough

Assume first that the `N` mode and the propagated `S` mode are the only
`Phi_2`-low modes.  In factor coordinates

```text
(z_0,z_1,z_2,z_3)=(x_0,x_4,x_5,ell_2),                 (15)
```

the zero tensor `F_2=z_0z_1z_2z_3` has two plane images and two hyperplane
images.  The exact hyperplane-plane profile theorem has two exhaustive
branches.

In branch I, all four images lie in one coordinate hyperplane.  Missing
`z_1` or `z_2` kills every diagonal target; missing `z_0` kills `D_0`.
If `z_3=ell_2` is missing, then `ell_1=ell_2-x_0=-x_0` on every local
plane, so

```text
F_1=-D_0/2,
```

contradicting their zero and nonzero targets.

In branch II, the two plane images equal a coordinate plane

```text
P=span{z_k,z_l},
```

and the hyperplanes are

```text
H_+=P direct-sum K(z_i+t z_j),
H_-=P direct-sum K(z_i-t z_j),           t!=0,          (16)
```

for the complementary coordinates `{i,j}`.  Contract (4) in the singleton
`S` slot.  On `P x H_+ x H_-`, it requires

```text
pol(z_1z_2(z_3-z_0))=0,
pol(z_1z_2z_0)!=0.                                      (17)
```

There are only six coordinate planes.  Direct polarization gives

```text
P              first tensor in (17)          second tensor

<z_0,z_1>             nonzero                    nonzero
<z_0,z_2>             nonzero                    nonzero
<z_0,z_3>               zero                       zero
<z_1,z_2>       contains t-1 and -t-1             nonzero
<z_1,z_3>         contains t and -t                 zero
<z_2,z_3>         contains t and -t                 zero.             (18)
```

Characteristic zero and `t!=0` make every displayed nonzero claim exact.
Thus (17) is impossible.  Both profile branches are excluded.

## 5. The forced three-low cycle

There must be another `Phi_2`-low mode.  It cannot contain another `S`:
the legal double contraction of two distinct copies of `S` annihilates all
five quartics, while their singleton colour-zero coordinates give a
nonzero `D_0` target.

The new low is therefore another `N`.  Double contraction of two copies
of `N` gives

```text
D_1=2x_4x_5,                  D_2=-2x_4x_5,
F_1=F_2=D_0=0.                                         (19)
```

The two targets in (19) have different colour supports.  Hence the
remaining `A`-pairing matrix is zero and the two actual supports of `N`
are disjoint.  They are nonempty subsets of `{1,2}`, so the two `N`
occurrences are complementary singletons at colours `1` and `2`.  No third
`N` can be disjoint from both, and no second `S` can occur.  After naming
the modes, the only residual profile is

```text
a: N at colour 1,       b: S at colour 0,
c: N at colour 2,       h: high for Phi_2.              (20)
```

The zero matrix in (19) is

```text
G_(bh)=A_b^T J A_h=0,                                  (21)
```

where `A_t` is the `x_4,x_5` projection of mode `t`.  Mode `b` is high for
`Phi_1`: every possible same-mode low line there was excluded in Section 2
or by rank-nullity.  Thus `A_b!=0`.  Highness of `h` for `Phi_2` gives
`A_h!=0`.  In the nondegenerate two-space `A`, equation (21) forces

```text
rank A_b=rank A_h=1.                                   (22)
```

## 6. The two-by-two pure-tensor gate

Factor the two rank-one shores as

```text
A_b=u rho_b,                  A_h=v rho_h,
J(u,v)=0,                    u,v!=0.                    (23)
```

Put

```text
X=h_+|L_b,        Y=h_-|L_b,       U=h_+|L_h,       V=h_-|L_h,
delta_t=J(A_t(-),v),               epsilon_t=J(u,A_t(-)). (24)
```

The two legal single contractions by the `N` vectors in modes `a,c` give,
after harmless reordering of tensor factors,

```text
delta_c tensor (X tensor rho_h)
 +epsilon_c tensor (rho_b tensor U) = lambda e_1 tensor (e_1 tensor e_1),
delta_c tensor (Y tensor rho_h)
 +epsilon_c tensor (rho_b tensor V) =0,

delta_a tensor (X tensor rho_h)
 +epsilon_a tensor (rho_b tensor U) =0,
delta_a tensor (Y tensor rho_h)
 +epsilon_a tensor (rho_b tensor V) =mu e_2 tensor (e_2 tensor e_2),   (25)
```

with `lambda,mu!=0`.  Since the two `N` columns are pure `R`,

```text
delta_c(e_2)=epsilon_c(e_2)=0,
delta_a(e_1)=epsilon_a(e_1)=0.                          (26)
```

The second equation of (25), together with the nonzero fourth equation,
forces `delta_c,epsilon_c` to span at most one line.  The first equation
then identifies that line as `Ke_1`.  Similarly the third and first
equations force `delta_a,epsilon_a` onto `Ke_2`.  Write

```text
delta_c=r_1e_1,       epsilon_c=r_2e_1,
delta_a=s_1e_2,       epsilon_a=s_2e_2.                 (27)
```

Let

```text
A=X tensor rho_h,       B=rho_b tensor U,
C=Y tensor rho_h,       D=rho_b tensor V.               (28)
```

Equations (25) reduce to

```text
r_1A+r_2B=lambda E_11,       r_1C+r_2D=0,
s_1A+s_2B=0,                 s_1C+s_2D=mu E_22.         (29)
```

The coefficient rows `(r_1,r_2)` and `(s_1,s_2)` cannot be proportional,
because a nonzero equation in (29) would then be proportional to a zero
one.  The coefficient matrix is invertible.  Solving (29) makes `A,B`
multiples of `E_11` and `C,D` multiples of `E_22`.

The shared nonzero factors `rho_b,rho_h` leave only two possible zero
patterns.  Otherwise `rho_h` would be proportional to both `e_1,e_2`
through nonzero `A,C`, or `rho_b` would be proportional to both through
nonzero `B,D`.  The two surviving coefficient matrices are, up to nonzero
row scalings,

```text
diagonal:      r_2=s_1=0,
antidiagonal:  r_1=s_2=0.                               (30)
```

In the diagonal case, (28)--(29) give

```text
rho_b proportional e_2,      rho_h proportional e_1,
epsilon_a proportional e_2,  delta_a=0,
delta_c proportional e_1,    epsilon_c=0.              (31)
```

The antidiagonal case gives the colour-swapped incidence

```text
rho_b proportional e_1,      rho_h proportional e_2,
delta_a proportional e_2,    epsilon_a=0,
epsilon_c proportional e_1,  delta_c=0.                (32)
```

If `u,v` were dependent, `J(u,v)=0` would make the rows `delta_t` and
`epsilon_t` proportional for every mode, contradicting (31) or (32).
Thus `u,v` are an orthogonal basis of `A`, and both self-pairings are
nonzero.  Equations (31) say that `A_a,A_b` are supported only at colour
`2` on the `u` line, while `A_c,A_h` are supported only at colour `1` on
the `v` line.  Equations (32) exchange the two shores.  In either case,

```text
A_a e_0=A_b e_0=A_c e_0=A_h e_0=0.                    (33)
```

The all-colour-zero coefficient of every quartic in (3) therefore has no
possible supplier for either `x_4` or `x_5`.  In particular its `D_0`
value is zero, contradicting `lambda_0!=0`.  This excludes the forced
three-low cycle and hence the last same-mode `N/N` case.

## 7. Exact near-survivor and the mistake it exposes

The final `D_0` slice in Section 6 is indispensable.  The following exact
rational local triples realize the diagonal zero pattern in (30), have
projection-rank pairs `(2,2),(3,2),(2,2),(2,3)`, satisfy `G_(bh)=0`, and
replay both `N` single-contraction tensors in (25):

```text
L_a:
 (1,0,0,0,0,0), (0,1,1,0,0,0), (0,0,0,1,1/2,1/2)
L_b:
 (0,0,0,1,0,0), (1/2,1/4,1/4,0,0,0), (0,0,0,0,1,1)
L_c:
 (1,0,0,0,0,0), (0,0,0,1,-1/2,1/2), (0,1,1,0,0,0)
L_h:
 (0,1,-1,0,0,0), (0,0,0,0,1,-1), (1/2,0,-1/2,0,0,0). (34)
```

After contracting `N` in `L_a`, only the `D_1` cell `(1,1,1)` survives,
with value `1`.  After contracting `N` in `L_c`, only the `D_2` cell
`(2,2,2)` survives, again with value `1`.  Nevertheless every colour-zero
`A`-column in (34) vanishes.  Contracting `x_3` in `L_b` produces off-target
`F_1` and `D_0` cells at `(0,1,1)`, so (34) is not a restriction and not a
counterexample to the conjecture.

The fixture records the failed shortcut: the two `N` slices and the
rank-one shore incidence alone do **not** close the cycle.  The full
uncontracted target, specifically (33), does.

## 8. Conclusion and replay

Combining Sections 2--6 proves

```text
same-mode N with a noncommon line:                      EXCLUDED;
same-mode B/S and C/S:                                  EXCLUDED;
same-mode proportional N/N:                            EXCLUDED;
every same-mode cross-family low:                       EXCLUDED;
distinct-mode exceptional incidences:                      OPEN;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.     (35)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_triangle_pair_same_mode_two_low_exclusion.py
```

The primary verifier reconstructs every single and double contraction,
checks the legal `Theta` kernel argument, exhausts the six coordinate-plane
profiles symbolically, replays the two-by-two zero-factor split, and checks
the rational near-survivor by complete polarization.  The independent
no-import audit rebuilds the square-free quartics, uses separate rational
row reduction and polarization, checks the six profile charts as affine
polynomials, exhausts the finite coefficient split over odd fields, and
independently replays the fixture.  Computation audits the displayed
identities and finite cases; the written arguments prove the
characteristic-zero theorem.
