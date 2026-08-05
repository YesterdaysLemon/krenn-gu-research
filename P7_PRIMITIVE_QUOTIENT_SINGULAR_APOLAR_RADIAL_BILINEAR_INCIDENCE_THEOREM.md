# P7 quotient singularity is a bilinear radial annihilator incidence

## Status

**Exact characteristic-zero apolar and determinantal reduction of the
primitive quotient-singular branch.**  In the Boolean algebra

```text
A(V)=K[z_0,...,z_7]/(z_0^2,...,z_7^2),
ell=z_0+...+z_7,
Q=sum_(i<j)b_ij z_i z_j,
H=Q^2/2,
```

assume the primitive P7 equation `ell H=0`.  The full edge catalecticant is

```text
D_(e,f)=H_(e union f) if e and f are disjoint,
        0             otherwise.                    (1)
```

The preceding quotient-Hessian theorem proved that the eight-dimensional
incidence space `ell A_1` lies in `ker D`.  This note identifies every
additional kernel direction exactly:

```text
D w=0    <=>    wH=0 in A_6(V).                     (2)
```

Thus quotient singularity is not merely an unexplained determinant zero.
It is the existence of a quadratic annihilator of `H` outside the forced
ideal `ell A_1`.

On the seven-leaf radial chart, this annihilator condition collapses to one
scale-free bilinear map.  Let `J` denote leaf-set complementation, let
`N=F^2/2` be the leaf four-form, and let

```text
G_0={G=sum_(j<k)g_jk z_j z_k : sum_(j<k)g_jk=0}.
```

For `G in G_0`, put

```text
partial G=sum_j(sum_(k!=j)g_jk)z_j,
Phi_N(G)=G(JN)-(partial G)N in A_5(L).               (3)
```

Then the primitive quotient Hessian is singular exactly when

```text
Phi_N(G)=0 for some nonzero G in G_0.                (4)
```

After complementing five-sets to leaf edges, `Phi_N` is a square
`20 x 20` linear map.  Its entries are linear in the 14-dimensional leaf
primitive form `N`, so its determinant is a nonzero homogeneous degree-20
polynomial.  At quotient corank one, `[G]` is unique; all deeper coranks are
retained.

For a physical radial graph, full primitive closure is `AF=t JN`, exactly
the earlier `u=t v` condition.  Hence the quotient-singular branch has the
low-degree lifted incidence

```text
N=F^2/2,
ell_L N=0,
AF=t JN,
sum g_jk=0,
G(JN)=(partial G)N.                                 (5)
```

In particular, `ell_L N=0` and `N=F^2/2` force
`ell_L F^2=0`: every full-edge P7 radial point descends to a full-edge
P6-order primitive square on its seven leaves.  Quotient singularity adds
the compatible quadratic annihilator `G N=0`, which follows from the last
equation in (5).

This replaces the opaque interaction between a degree-67 eliminated
condition and a degree-20 determinant by quadratic and bilinear equations
with explicit auxiliary data.  It does **not** prove that (5) is empty on
the edge torus.  The physical quotient-singular branch, P7, and global
Krenn--Gu remain **UNKNOWN/UNRESOLVED**.

## 1. Catalecticant kernel equals the quadratic annihilator

Write `[z_V]` for the coefficient of the top Boolean monomial.  The pairing

```text
A_6(V) x A_2(V) -> K,             (P,W) -> [z_V]PW (6)
```

is perfect: each six-set monomial pairs only with its complementary edge.
Primitivity in middle degree also gives complement symmetry

```text
H_U=H_(V minus U)                       (|U|=4).     (7)
```

For edge quadrics `w,v`, equations (1) and (7) give

```text
w^T D v
 =sum_(e disjoint f)w_e v_f H_(e union f)
 =[z_V]w v H.                                         (8)
```

Because (6) is perfect, (8) proves (2).  Equivalently,

```text
ker D=Ann_2(H)={w in A_2(V):wH=0}.                   (9)
```

The forced kernel now has an ideal-theoretic explanation:

```text
(ell U)H=U(ell H)=0                       (U in A_1). (10)
```

Let

```text
C=ell A_1,                 P=ker(partial:A_2->A_1).
```

Boolean Lefschetz theory gives `A_2=C direct-sum P`, with dimensions 8 and
20.  Therefore

```text
corank(D|_P)=dim(Ann_2(H))-8,                           (11)
rank(D|_P)<=19
 <=> Ann_2(H) contains a nonzero element of P.          (12)
```

This is the square-free Macaulay-apolar meaning of the quotient-singular
branch.

## 2. Seven-leaf primitive normal form

Let `L={1,...,7}` and write `A(L)` for its Boolean algebra.  For a leaf
subset `S`, define

```text
J(z_S)=z_(L minus S).                                 (13)
```

The leaf restrictions of primitive complement-fixed four-forms are exactly

```text
N_4=ker(ell_L:A_4(L)->A_5(L)),        dim N_4=14.    (14)
```

This is the Specht module of shape `(4,3)`.  For every `N in N_4`, the
Boolean complement/Lefschetz identity is

```text
N+ell_L JN=0.                                        (15)
```

Consequently

```text
H_N=z_0 JN+N                                         (16)
```

is primitive and complement-fixed on `V`, and every such global four-form
has this unique presentation.  One way to see (14)--(16) is to restrict the
14-dimensional global `(4,4)` primitive module to the leaves.  Restriction
is injective by complement symmetry, its image lies in the 14-dimensional
kernel in (14), and (15) is the remaining five-set primitive equation.

Now take the physical radial notation

```text
A=sum_j a_j z_j,
F=sum_(j<k)a_j a_k x_jk z_j z_k,
M=AF,
N=F^2/2,
Q=z_0 A+tF.                                          (17)
```

Then

```text
Q^2/2=t z_0 M+t^2 N.                                (18)
```

For a leaf triple `T`, the coefficient `M_T` is the earlier radial vector
`u_T`; the coefficient `N_(L minus T)` is `v_T`.  On the already imposed
star-pencil/anchor locus, full complement closure is exactly

```text
M=t JN,                                              (19)
```

which is the affine form of `u wedge v=0`.  Substituting (19) into (18)
gives

```text
H=t^2 H_N.                                           (20)
```

Thus quotient rank on a physical radial point depends only on the
projective leaf primitive four-form `[N]`; the star weights and the recovered
scale enter only through the requirement that `N` actually has the square
root and radial presentation (17)--(19).

There is also an exact order descent:

```text
ell_L F^2=2 ell_L N=0.                               (20a)
```

When all original edges are nonzero, all coefficients of `F` are nonzero.
Thus any physical P7 point supplies a full-edge seven-vertex primitive
square before the quotient-singular condition is even imposed.  This is a
necessary P6-order shadow, not a proof that every such leaf square extends
back to P7.

## 3. The zero-row quotient is one leaf hyperplane

For a leaf quadratic `G=sum g_jk z_jz_k`, put

```text
partial G=sum_j d_j z_j,
d_j=sum_(k!=j)g_jk,
sigma(G)=sum_(j<k)g_jk.                              (21)
```

Define

```text
iota(G)=G-z_0 partial G.                             (22)
```

The leaf row sums of `iota(G)` vanish automatically, while its row-zero sum
is `-2 sigma(G)`.  Characteristic zero therefore gives an exact linear
isomorphism

```text
iota:G_0 -> P,
G_0=ker sigma subset A_2(L),             dim G_0=20. (23)
```

This is the branching

```text
S^(6,2) restricted to S_7 = S^(6,1) direct-sum S^(5,2)
```

in concrete coordinates: the 21 leaf edges carry one trivial coordinate,
and deleting their total sum leaves the 20-dimensional P7 quotient.

## 4. Radial factorization of the singular catalecticant

For `N in N_4` and `G in G_0`, define `Phi_N(G)` by (3).  Direct Boolean
multiplication gives

```text
iota(G)H_N
 =GN+z_0(G(JN)-(partial G)N).                        (24)
```

Use (15), `ell_L N=0`, and (3):

```text
GN=-ell_L G(JN)
   =-ell_L(Phi_N(G)+(partial G)N)
   =-ell_L Phi_N(G).                                 (25)
```

Therefore the complete six-form factors as

```text
iota(G)H_N=(z_0-ell_L)Phi_N(G).                      (26)
```

The last multiplication map is injective because its `z_0` component is
`z_0 Phi_N(G)`.  Equations (2), (23), and (26) prove (4).

There is also an exact square form.  Complement the five-set coefficients
of `Phi_N(G)` to a leaf quadratic:

```text
widehat(Phi)_N(G)=J Phi_N(G) in A_2(L).               (27)
```

This quadratic has total coefficient sum zero, so it belongs to `G_0`.
Indeed, complementing (26) to edge coordinates gives the identity

```text
D_(H_N) iota(G)=iota(widehat(Phi)_N(G)).             (28)
```

The right side belongs to `P` because the primitive catalecticant preserves
`P`; equivalently its leaf total is zero.  Thus

```text
D_(H_N)|_P is conjugate through iota to
widehat(Phi)_N:G_0->G_0.                             (29)
```

This proves equality of all quotient ranks, not only equality of their
singular loci.

## 5. Determinantal incidence and exact controls

Choose any basis of `G_0`.  The matrix of `widehat(Phi)_N` is `20 x 20`
and every entry is linear in `N`.  Hence

```text
delta(N)=det widehat(Phi)_N                          (30)
```

is homogeneous of degree 20.  Its zero set and rank stratification are
basis-independent, although its displayed scalar normalization is not.
The construction is `S_7`-equivariant, so every rank stratum is label
invariant.

The ambient primitive rank-20 control in
`P7_PRIMITIVE_BOOLEAN_SQUARE_QUOTIENT_HESSIAN_CORANK_AND_TOMOGRAPHY.md`
restricts to a fixed `N_* in N_4` and satisfies

```text
rank widehat(Phi)_(N_*)=20.                          (31)
```

For the ordered leaf-edge basis

```text
e_12-e_67, e_13-e_67, ..., e_57-e_67
```

on both copies of `G_0`, its determinant is

```text
1519811734108372992 = 2^24*3^13*7*8117 !=0.         (32)
```

Therefore `delta` is not the zero polynomial on the 14-dimensional
primitive leaf space.  This control is not asserted to be `F^2/2` or a
physical graph deck.

On `delta=0`:

```text
rank=19  => ker widehat(Phi)_N is one projective point [G];
rank<=18 => the deeper annihilator incidence is retained.   (33)
```

Combining (14), (17), (19), and (4) proves the lifted physical system (5).
Its last equation consists of 21 bilinear coefficient equations; the seven
apparently additional equations `GN=0` follow automatically from (15) and
(25).  This is a determinantal incidence resolution, not an elimination
claim: projecting away `G,N,t` may recreate high-degree equations and extra
components.

## 6. Literature translation and scope

The language in (2), (9), and (30) is the square-free analogue of classical
apolar catalecticants.  Catalecticant minors and their limitations as
defining equations are treated by
[Landsberg--Ottaviani](https://arxiv.org/abs/1111.4567); that paper supplies
the established geometric vocabulary, not the P7 identities proved here.
The raising, lowering, complement, and Specht decompositions behind
(14)--(15) are instances of the Boolean `sl_2` structure developed by
[Feinsilver](https://arxiv.org/abs/1102.0368).

The new content here is the exact P7 conjugacy (28)--(29) and its radial
bilinear formula (3).  No general catalecticant or Boolean-Lefschetz source
implies that a physical `N=F^2/2` avoids `delta=0`.

## 7. Exact wall

```text
full Hessian kernel equals Ann_2(H):                         PROVED;
forced incidence kernel equals ell A_1 ideal piece:          PROVED;
quotient corank equals excess quadratic annihilator dimension: PROVED;
leaf primitive form N lies in 14-dimensional S^(4,3):        PROVED;
physical P7 radial point descends to ell_L F^2=0:             PROVED;
radial closure u=t v gives H=t^2(z_0 JN+N):                  PROVED;
zero-row quotient P is the leaf hyperplane G_0:              PROVED;
quotient catalecticant conjugate to widehat(Phi)_N:          PROVED;
quotient-singular condition Phi_N(G)=0:                      EXACT, BILINEAR;
seven GN equations from the 21 Phi equations:                AUTOMATIC;
determinant delta on primitive leaf space:                    NONZERO, DEGREE 20;
corank-one annihilator direction:                             UNIQUE PROJECTIVELY;
deeper quotient corank at least two:                          RETAINED;
delta=0 meets the physical radial square edge torus:          UNKNOWN;
lifted system (5) has any full-support solution:              UNKNOWN;
primitive-square edge-torus locus:                            UNKNOWN;
P7 pinned matrix full rank on that locus:                     UNKNOWN;
global Krenn--Gu:                                             UNRESOLVED. (34)
```

No graph/support enumeration, parameter sweep, numerical approximation,
finite-field inference, Groebner elimination, or timeout is used.

## Replay

```powershell
uv run --with sympy python verify_p7_primitive_quotient_singular_apolar_radial_bilinear_incidence.py
python audit_p7_primitive_quotient_singular_apolar_radial_bilinear_incidence.py
python -m py_compile verify_p7_primitive_quotient_singular_apolar_radial_bilinear_incidence.py audit_p7_primitive_quotient_singular_apolar_radial_bilinear_incidence.py
uv run --with ruff ruff check verify_p7_primitive_quotient_singular_apolar_radial_bilinear_incidence.py audit_p7_primitive_quotient_singular_apolar_radial_bilinear_incidence.py
```

The primary verifier checks the perfect-pairing normalization, the full
14-dimensional primitive leaf space, the factorization (26), the exact
conjugacy (28), the physical radial coefficient dictionary, and the fixed
rank-20 ambient control.  The independent standard-library audit rebuilds
all Boolean products, inclusion/complement maps, the 20-dimensional leaf
quotient, and the control without importing the primary or project code.
