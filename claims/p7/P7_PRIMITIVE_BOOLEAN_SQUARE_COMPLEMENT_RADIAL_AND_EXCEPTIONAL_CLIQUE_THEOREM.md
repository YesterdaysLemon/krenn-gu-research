# P7 primitive squares have radial complement closure and small exceptional cliques

## Status

**Exact characteristic-zero reduction of the remaining primitive P7
incidence.**  Continue with the star chart of
`P7_PRIMITIVE_BOOLEAN_SQUARE_STAR_CLOSURE_DISCRIMINANT_AND_ZERO_ROW_BOUNDARY_THEOREM.md`.
Thus the leaf set is `L={1,...,7}`, every `a_j` and every `x_jk` is nonzero,
and

```text
R=sum_j a_j,
Delta_jk=R-2(a_j+a_k),
y_j=sum_(k!=j) a_k x_jk,
y_j+y_k+Delta_jk x_jk=0.                            (1)
```

The preceding note left 35 leaf-triangle quadrics on the discriminant
`P(a)=0`.  This note proves three sharper facts.

1. Modulo (1), those 35 quadrics are equivalent to the 35 complementary
   four-hafnian equalities.  They split into one linear and one quadratic
   vector in a homogeneous star-pencil direction.  Full closure is exactly
   their projective collinearity, and the missing affine scale is unique.
2. On the corank-one part of the `21 x 21` Schur pencil, one adjugate column
   gives the unique candidate.  The remaining condition is a fixed family
   of determinant-cleared homogeneous degree-67 equations in the seven star
   weights.  The corank-at-least-two locus is separated exactly.
3. The exceptional value class `a_j=R/4` has size at most four.  If it has
   size four, the other three star weights lie on one explicit cubic.

None of these statements proves that the final incidence is empty.  The
degree-67 corank-one locus and the deeper pencil-singular locus remain
**UNKNOWN**.  P7 and global Krenn--Gu remain **UNRESOLVED**.

The separate sibling package
`P7_PRIMITIVE_BOOLEAN_SQUARE_QUOTIENT_HESSIAN_CORANK_AND_TOMOGRAPHY.md`
proves the quotient-Hessian corank consequence.  It is cited here but not
duplicated.

## 1. Complement symmetry replaces the leaf equations

Let `V={0} union L` and let `A_4(V)` have its square-free four-set basis.
For a symmetric zero-diagonal matrix `B`, put

```text
H_U=haf B[U]                         (|U|=4).         (2)
```

Let `D_4:A_4(V)->A_3(V)` be Boolean lowering,

```text
(D_4 H)_T=sum_(v notin T) H_(T union {v}).           (3)
```

The primitive-square condition is `D_4 H=0`.  Four-set complementation
`C:H_U -> H_(V minus U)` acts as `+1` on the 14-dimensional primitive
middle Specht module.

There is a useful converse after the anchor triangles have been imposed.

### Theorem 1 (anchor-complement closure)

Assume

```text
(D_4 H)_{0ij}=0                    (i<j in L).        (4)
```

Then

```text
D_4 H=0    <=>    C H=H.                              (5)
```

### Proof

The `+1` complement eigenspace is parametrized by 35 coordinates `h_T`,
one for every leaf triple:

```text
H_{0 union T}=H_{L minus T}=h_T.                     (6)
```

On this space, (4) is

```text
sum_(k in L minus {i,j}) h_{ijk}=0.                  (7)
```

Its matrix is the transpose of the unsigned two-subset/three-subset
inclusion map `W_(2,3)(7)`.  That inclusion map has rank 21 in
characteristic zero, so (7) has rank 21 and its kernel has dimension
`35-21=14`.  The primitive middle space is contained in this kernel, is
complement-fixed, and also has dimension 14.  The two spaces are equal.
This proves (5).

Thus the 35 leaf equations have not disappeared; they have been translated
from a row-sum form to complementary four-hafnians.  The latter exposes a
radial structure that the original display concealed.

## 2. The radial complement criterion

For a full-support direction `x=(x_jk)` in the star-pencil kernel define,
for every leaf triple `T`,

```text
A_T=product_(j in T) a_j,
tau_T(x)=sum_({j,k} subset T) x_jk,
eta_W(x)=haf X[W]
        =x_pq x_rs+x_pr x_qs+x_ps x_qr   (W={p,q,r,s}),

u_T=A_T tau_T(x),
v_T=A_(L minus T) eta_(L minus T)(x).                 (8)
```

For `t!=0`, reconstruct a graph by

```text
b_0j=a_j,
b_jk=t a_j a_k x_jk.                                 (9)
```

The row deviations are `t y_j`.  Since (1) is homogeneous in `(y,x)`,
every graph (9) satisfies row closure and all 21 anchor triangles.  Its two
complementary four-hafnians are

```text
H_{0 union T}=t u_T,
H_{L minus T}=t^2 v_T.                               (10)
```

Theorem 1 therefore gives the exact replacement

```text
all 35 leaf triangles hold
    <=> u=t v.                                        (11)
```

Both vectors in (11) are automatically nonzero on the edge torus.

- If `u=0`, then every triangle sum of `x` vanishes.  The injectivity of
  `W_(2,3)(7)` forces `x=0`.
- If `v=0`, every principal four-hafnian of the seven-vertex matrix `X`
  vanishes.  The exact zero-four-deck theorem on at least six vertices says
  that some edge of `X` must vanish.  For completeness, fix two vertices.
  The equations on their four-sets reconstruct every other edge; substituting
  into a four-set with only one fixed vertex makes every triple sum of the
  nonzero ratios vanish.  With at least four ratios, characteristic zero
  forces every ratio to be zero, a contradiction.

Consequently (11) has a solution `t in K^*` exactly when

```text
u wedge v=0,                                          (12)
```

and then `t` is unique.  Equivalently, all `2 x 2` minors

```text
u_T v_T' - u_T' v_T=0                                (13)
```

vanish.  No pivot has been inverted in (12); any coordinate with `v_T!=0`
then recovers `t=u_T/v_T`.

This is a projective-versus-affine separation.  The star pencil chooses a
projective direction, the complement equations test one collinearity, and
one nonzero ratio restores the unique physical scale.

## 3. Corank-one adjugate reduction

Use the fixed matrices from the preceding note:

```text
U_(j,e)=1 if j in e,
V_(j,{j,k})=a_k,
D=diag_(e={j,k})(Delta_jk),
S(a)=D+U^T V.                                        (14)
```

The `28 x 28` pencil equation is equivalent to

```text
S(a)x=0,       y=Vx,       P(a)=det S(a).             (15)
```

Every entry of `S` is homogeneous linear in `a`.  On the stratum

```text
rank S(a)=20,                                         (16)
```

choose any nonzero column

```text
X=adj(S(a)) e_p.                                      (17)
```

Then `X` spans the kernel.  If its 21 edge coordinates are nonzero, form
`u(X),v(X)` by (8).  The full primitive edge-torus point over this star is
present if and only if

```text
u(X) wedge v(X)=0.                                   (18)
```

If present, it is unique for the fixed normalized star:

```text
t=u_T(X)/v_T(X),
b_0j=a_j,
b_jk=t a_j a_k X_jk.                                (19)
```

Changing the nonzero adjugate column rescales `X`; formula (19) is
unchanged because `u` is linear and `v` is quadratic in `X`.

There is also a clean degree ledger.  An adjugate column has degree 20,
so

```text
deg u(X)=3+20=23,
deg v(X)=4+40=44,
deg(u_T v_T'-u_T' v_T)=67.                           (20)
```

Thus (18) gives 595 displayed homogeneous degree-67 necessary and
sufficient equations on each corank-one adjugate chart.  They are highly
dependent; no codimension is inferred from their raw number.  The deeper
stratum

```text
rank S(a)<=19    <=>    adj S(a)=0                    (21)
```

is retained, not saturated away.

## 4. Exceptional cliques have size at most four

Let

```text
C={j in L:a_j=R/4},       s=R/4,       c=|C|.         (22)
```

Every pair in `C` is exceptional.  If `c>=3`, the equations
`y_i+y_j=0` on its clique give

```text
y_i=0                         (i in C).               (23)
```

Write `O=L minus C` and `p_u=a_u` for `u in O`.  By maximality of the
value class, `p_u!=s`.  The edge equation between `i in C` and `u in O`
then gives

```text
x_iu=-y_u/[2(s-p_u)],                                (24)
```

independent of `i`.  Row closure at the outside vertices and their mutual
edge equations reduce, after clearing denominators, to

```text
((c+2)s-2p_u)y_u
 -2(s-p_u) sum_(v in O minus {u}) p_v x_uv=0,

y_u+y_v+[4s-2(p_u+p_v)]x_uv=0.                       (25)
```

Also

```text
sum_(u in O) p_u=(4-c)s.                             (26)
```

For `c=7`, (26) gives `3s=0`, impossible because `s=a_j!=0`.  For
`c=6`, the cleared system (25) has determinant `12s`.  For `c=5`, with
outside weights `p,q` and `p+q=-s`, its determinant is

```text
360s^3.                                               (27)
```

Both are nonzero.  Equations (25) therefore force every outside `y` and
`x` to vanish, and then (24) forces cross edges to vanish.  This contradicts
the edge torus.  Consequently

```text
|{j:a_j=R/4}|<=4.                                    (28)
```

The first surviving odd-cycle boundary has `c=4`.  Write the other three
weights as `p,q,r`; equation (26) says `p+q+r=0`.  The determinant of the
cleared six-by-six system (25) is

```text
1152s^3 G_s(p,q,r),                                  (29)

G_s(p,q,r)=3pqr+2s(pq+pr+qr)+12s^3.                  (30)
```

Since a full-support pencil kernel cannot make all outside variables zero,
the four-clique boundary necessarily satisfies

```text
G_s(p,q,r)=0.                                        (31)
```

This does not exclude that cubic.  It replaces a large exceptional divisor
by one explicit symmetric curve after projective scaling.

## 5. Exact wall

```text
anchor closure plus complement symmetry <=> full primitive closure: PROVED;
35 leaf quadrics <=> radial collinearity u wedge v=0:          PROVED;
radial affine scale on a full-support pencil direction:        UNIQUE;
corank-one adjugate obstruction degree:                        67;
corank-one adjugate reconstruction when the obstruction holds: UNIQUE;
corank-at-least-two star-pencil stratum:                        RETAINED;
primitive quotient-Hessian corank theorem:                      PROVED IN SIBLING NOTE;
exceptional value class a=R/4:                                 SIZE AT MOST 4;
four-vertex exceptional class:                                 ON CUBIC (30);
degree-67 corank-one torus incidence nonempty:                  UNKNOWN;
corank-at-least-two torus incidence nonempty:                   UNKNOWN;
primitive Boolean-square locus meets the edge torus:            UNKNOWN;
P7 pinned matrix full rank on the edge torus:                    UNKNOWN;
global Krenn--Gu:                                                UNRESOLVED. (32)
```

No graph, support, parameter, finite-field, or numerical search enters this
proof.  The only finite matrices are fixed Boolean incidence operators and
the displayed symbolic systems.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_primitive_complement_radial_and_exceptional_clique.py
python claims/p7/audit_p7_primitive_complement_radial_and_exceptional_clique.py
python -m py_compile verify_p7_primitive_complement_radial_and_exceptional_clique.py audit_p7_primitive_complement_radial_and_exceptional_clique.py
uv run --with ruff ruff check verify_p7_primitive_complement_radial_and_exceptional_clique.py audit_p7_primitive_complement_radial_and_exceptional_clique.py
```

The primary verifier checks the Boolean complement theorem, both nonvanishing
lemmas, the radial hafnian formulas, the degree ledger, and all three
exceptional-clique determinants.
The independent standard-library audit rebuilds the fixed matrices, uses
exact fraction-free ranks, sparse-polynomial arithmetic, and a separate
matching recursion.  Neither imports the other or project code.
