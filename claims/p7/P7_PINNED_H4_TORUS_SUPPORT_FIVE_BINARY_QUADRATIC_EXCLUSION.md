# P7 pinned-star torus circuits cannot have support five

## Status

**Exact characteristic-zero support-five exclusion.**  Let `B` be a weighted
graph on eight named vertices and form the pinned `h_4` star matrix

```text
N_B[T,i]=haf B[T minus {i}]  if i in T,
         =0                  otherwise,     |T|=5.    (1)
```

The preceding torus circuit-girth theorem excluded kernel supports one
through four.  This note proves the next case:

```text
B_ij!=0 for every i<j,  N_B x=0,  x!=0
                  => |supp(x)|>=6.                    (2)
```

The proof uses no support enumeration.  For a hypothetical five-supported
kernel, split the vertices into its five-point support and a complementary
triangle.  Vertex gauge normalizes the five kernel entries and the three
triangle edges.  The equations with two support vertices force all five
cross stars into one two-plane.  The equations with three support vertices
then become binary-quadratic identities.  A fixed nondegenerate quadratic
splits over the algebraic closure, and both resulting scalar coordinate
systems would have support at most one.  Five nonzero cross stars are
therefore impossible.

Consequently, this note leaves only dependencies using six, seven, or eight
star columns.  The later
`P7_PINNED_H4_TORUS_SUPPORT_SIX_RECIPROCAL_POLARIZATION_EXCLUSION.md`
excludes support six as well, leaving seven and eight at that stage.  The
still later
`P7_PINNED_H4_TORUS_SUPPORT_SEVEN_BOOLEAN_LEFSCHETZ_EXCLUSION.md` excludes
support seven, leaving only full support eight.  This is not a P7
obstruction, and global Krenn--Gu remains **UNRESOLVED**.

## 1. Gauge-normalized support-five equations

Work over a characteristic-zero field `K`.  A contradiction after extending
to its algebraic closure is already a contradiction over `K`, so all
nonzero square roots and binary-quadratic factors used below are legitimate.

Suppose `N_Bx=0` and write

```text
S=supp(x),       |S|=5,
C=V minus S={1,2,3}.                                  (3)
```

Under diagonal vertex scaling

```text
B_ij -> d_i d_j B_ij,       x_i -> d_i x_i,           (4)
```

each five-set equation is multiplied by the product of its vertex scales.
Choose the five scales on `S` so that

```text
x_a=1                   for every a in S.             (5)
```

Because the three edges inside `C` are nonzero, choose the remaining scales
so that

```text
B_12=B_13=B_23=1.                                     (6)
```

For example, `d_1^2=B_23/(B_12 B_13)` and the other two scales then follow.
All cross edges remain nonzero.

For `a in S`, put

```text
v_a=(B_a1,B_a2,B_a3) in K^3.                          (7)
```

Every coordinate of every `v_a` is nonzero.

## 2. Two-support rows force a common plane

Take a five-set `{a,b} union C`, with `a,b in S`.  Only the two supported
kernel columns contribute to (1), so

```text
haf B[{a} union C]+haf B[{b} union C]=0.              (8)
```

Using (6),

```text
haf B[{a} union C]=B_a1+B_a2+B_a3.                    (9)
```

Write this scalar as `g_a`.  Equation (8) says `g_a+g_b=0` for every pair in
a five-set.  Three indices already force every `g_a=0`.  Hence

```text
v_a in P={u in K^3:u_1+u_2+u_3=0}       for all a.   (10)
```

The plane `P` has basis

```text
p=(1,0,-1),       q=(0,1,-1).                         (11)
```

## 3. Three-support rows and the binary quadratic

For `u,v in P`, define the symmetric bilinear pair-product map

```text
Beta(u odot v)=
 (u_1 v_2+u_2 v_1,
  u_1 v_3+u_3 v_1,
  u_2 v_3+u_3 v_2).                                  (12)
```

On the symmetric-square basis

```text
p odot p,       p odot q,       q odot q,
```

its matrix is

```text
M_Beta=[
  0  1  0
 -2 -1  0
  0 -1 -2
],                 det M_Beta=-4.                    (13)
```

Thus `Beta:Sym^2(P)->K^3` is an isomorphism.  The inverse image of the unit
triangle-edge vector is

```text
Q_0=Beta^(-1)(1,1,1)
    =-p odot p+p odot q-q odot q.                    (14)
```

This binary quadratic is nondegenerate: in the basis `(p,q)` its determinant
is `3/4` up to the harmless convention for `odot`.

Now take a five-set `{a,b,c,i,j}` with three vertices in `S` and two in `C`.
Put `D_ab=B_ab`.  Expansion of each four-hafnian gives

```text
haf B[{a,b,i,j}]
 =D_ab+v_a,i v_b,j+v_a,j v_b,i.                      (15)
```

The three supported columns in (1) therefore give

```text
Beta(v_a odot v_b+v_a odot v_c+v_b odot v_c)
  =-(D_ab+D_ac+D_bc)(1,1,1).                         (16)
```

Invert (13) and pass to the quotient by the line `K Q_0`:

```text
v_a odot v_b+v_a odot v_c+v_b odot v_c=0
                  in Sym^2(P)/K Q_0                  (17)
```

for every triple `{a,b,c} subset S`.

## 4. A scalar triple lemma closes the branch

Over the algebraic closure, factor the nondegenerate binary quadratic as

```text
Q_0=lambda e odot f                                  (18)
```

for a basis `(e,f)` of `P` and `lambda!=0`.  Write

```text
v_a=r_a e+s_a f.                                     (19)
```

The `e odot e` and `f odot f` coefficients of (17) say, independently,

```text
r_a r_b+r_a r_c+r_b r_c=0,
s_a s_b+s_a s_c+s_b s_c=0                            (20)
```

for every triple in the five-set `S`.

### Lemma 1 (five-scalar triple annihilation)

If five scalars `t_a` satisfy

```text
t_a t_b+t_a t_c+t_b t_c=0                            (21)
```

for every triple, then at most one `t_a` is nonzero.

### Proof

If two entries `t_a,t_b` are nonzero, equation (21) with any third index
shows that third entry cannot be zero.  Thus all five entries are nonzero.
Divide (21) by `t_a t_b t_c`:

```text
1/t_a+1/t_b+1/t_c=0                                  (22)
```

for every triple.  The one-subset versus three-subset inclusion matrix on
five points has full column rank in characteristic zero: comparing two
triple sums that differ in one index makes all reciprocals equal, and one
triple then kills their common value.  This contradicts nonzero `t_a`.

Apply Lemma 1 separately to `(r_a)` and `(s_a)`.  At most one `v_a` can have
a nonzero `e` coordinate and at most one can have a nonzero `f` coordinate.
Hence at most two of the five vectors `v_a` are nonzero.  But every `v_a`
has three nonzero edge coordinates by the full-edge-torus hypothesis.  This
contradiction proves (2).

Notice that the edges `D_ab` inside the five-point support disappear after
quotienting by `Q_0`.  The exclusion therefore occurs before the four- and
five-support row types impose their additional equations.

## 5. Incidence-line consequence

Let a full-rank P7 root sensor meet the diagonal target space in one line,
so its allowable shallow-cofactor vectors form

```text
K_Gamma=K c.                                          (23)
```

A pinned maximal minor is homogeneous of degree eight in the `h_4`
coordinates.  On the vector line,

```text
Delta(t c)=t^8 Delta(c).                              (24)
```

Therefore the nonzero line is either wholly inside this selected pinned
chart or wholly inside its determinant hypersurface.  If every maximal minor
vanishes and `c` is realized by a full-edge-torus graph, equation (2) upgrades
the remaining singular alternative to

```text
kernel circuit size in {6,7,8}.                       (25)
```

The later reciprocal-polarization and Boolean-Lefschetz theorems strengthen
(25) first to `{7,8}` and then to `{8}`.

This is a graph-realizability constraint on the sensor-dependent cofactor
line, not a universal linear relation on arbitrary cofactor vectors.  It
does not prove that the GHZ incidence line meets the graph torus or that one
of the surviving circuit sizes is impossible.

## 6. Exact wall

```text
P7 full-edge-torus pinned circuits of size 1..4: IMPOSSIBLE (PRIOR);
P7 full-edge-torus pinned circuits of size 5:    IMPOSSIBLE (THIS NOTE);
P7 full-edge-torus pinned circuits of size 6:    IMPOSSIBLE (LATER NOTE);
P7 full-edge-torus pinned circuits of size 7:    IMPOSSIBLE (LATER NOTE);
P7 full-edge-torus pinned circuits of size 8:    UNKNOWN;
P7 pinned matrix full rank on the edge torus:    UNKNOWN;
target cofactor line graph-torus realizability:  UNKNOWN;
P7 obstruction:                                 UNKNOWN;
global Krenn--Gu:                                UNRESOLVED.           (26)
```

No supports, configurations, graphs, words, finite fields, or parameter
values were enumerated.  The replays below check only the fixed linear maps
and symbolic identities in the proof.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_pinned_h4_torus_support_five_binary_quadratic_exclusion.py
python claims/p7/audit_p7_pinned_h4_torus_support_five_binary_quadratic_exclusion.py
python -m py_compile claims/p7/verify_p7_pinned_h4_torus_support_five_binary_quadratic_exclusion.py claims/p7/audit_p7_pinned_h4_torus_support_five_binary_quadratic_exclusion.py
uv run --with ruff ruff check claims/p7/verify_p7_pinned_h4_torus_support_five_binary_quadratic_exclusion.py claims/p7/audit_p7_pinned_h4_torus_support_five_binary_quadratic_exclusion.py
```

The primary verifier checks the gauge-normalized hafnian expansion, the
binary pair-product isomorphism and its nondegenerate inverse image, and the
five-point triple-incidence rank.  The independent standard-library audit
repeats the fixed rational matrices and representative polynomial identities
without importing the primary verifier or project code.
