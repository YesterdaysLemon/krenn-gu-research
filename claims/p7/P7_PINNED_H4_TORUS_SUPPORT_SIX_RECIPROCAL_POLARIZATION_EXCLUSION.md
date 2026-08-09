# P7 pinned-star torus circuits cannot have support six

## Status

**Exact characteristic-zero support-six exclusion.**  Let `B` be a weighted
graph on eight named vertices and form the pinned `h_4` star matrix

```text
N_B[T,i]=haf B[T minus {i}]  if i in T,
         =0                  otherwise,     |T|=5.    (1)
```

On the full edge torus,

```text
B_ij!=0 for every i<j,  N_B x=0,  x!=0
                  => |supp(x)|>=7.                    (2)
```

The prior circuit-girth and binary-quadratic arguments excluded supports one
through five.  This note excludes support six without enumerating supports,
graphs, or parameter values.  A hypothetical six-supported dependency has a
two-vertex complement.  Its three-support rows recover every internal
support edge from the two cross-stars.  Its four-support rows are then
exactly the four-subset sums of a 15-coordinate **reciprocal polarization
edge form**.  The two-subset versus four-subset inclusion operator on six
points is invertible in characteristic zero, so the edge form vanishes.
Three of its pair equations already contradict the full edge torus.

Thus this note leaves only a seven- or eight-supported dependency.  The later
`P7_PINNED_H4_TORUS_SUPPORT_SEVEN_BOOLEAN_LEFSCHETZ_EXCLUSION.md` excludes
support seven, leaving only full support eight **UNKNOWN**.
This is not a P7 obstruction, and global Krenn--Gu remains **UNRESOLVED**.

## 1. Gauge-normalized six-support equations

Work over a characteristic-zero field `K`.  Suppose `N_Bx=0`, put

```text
S=supp(x),       |S|=6,
C=V minus S={1,2}.                                   (3)
```

Under diagonal vertex scaling,

```text
B_ij -> d_i d_j B_ij,       x_i -> d_i x_i,           (4)
```

each five-set equation is multiplied by the product of its five vertex
scales.  Choose the six scales on `S` and the product of the two scales on
`C` so that

```text
x_a=1  for a in S,             B_12=1.                (5)
```

No edge becomes zero.  Write

```text
u_a=B_a1,       v_a=B_a2,       D_ab=B_ab.            (6)
```

Every `u_a`, `v_a`, and `D_ab` is nonzero.

## 2. Three-support rows recover the internal graph

For distinct `a,b,c in S`, use the row on `{a,b,c,1,2}`.  Only the three
supported columns contribute.  Direct four-hafnian expansion gives

```text
0=(D_ab+u_a v_b+v_a u_b)
 +(D_ac+u_a v_c+v_a u_c)
 +(D_bc+u_b v_c+v_b u_c).                            (7)
```

Put

```text
F_ab=D_ab+u_a v_b+v_a u_b.                           (8)
```

The two-subset versus three-subset inclusion map on six points is injective,
so (7), for all triples, implies

```text
F_ab=0,
D_ab=-(u_a v_b+v_a u_b)       for every a<b in S.    (9)
```

For completeness, injectivity here has an elementary proof.  If all triangle
sums of edge weights `F_ab` vanish, let `d_a=sum_(b!=a) F_ab` and
`D=sum_a d_a`.  Summing the four triangles through an edge gives

```text
2F_ab+d_a+d_b=0.                                     (10)
```

Summing (10) over `b!=a` gives `6d_a=-D`.  Hence all six `d_a` are equal;
summing them gives `D=-D`, so `D=0`, then every `d_a=0` and every `F_ab=0`.

## 3. Reciprocal polarization edge form

Take a four-set `U subset S` and the row on `U union {1}`.  Summing the four
contributing hafnians gives

```text
sum_({p,q,r} subset U)
  (D_pq u_r+D_pr u_q+D_qr u_p)=0.                    (11)
```

Substitute (9).  For each triple, every monomial with one `v` and two `u`'s
occurs twice, so (11) becomes

```text
sum_({p,q,r} subset U)
 (v_p u_q u_r+u_p v_q u_r+u_p u_q v_r)=0.            (12)
```

The omitted factor `-2` is nonzero in characteristic zero.  Divide (12) by
the nonzero product `prod_(a in U) u_a`.  Pairing the ordered terms indexed
by the `v`-vertex and the omitted vertex produces

```text
sum_({a,b} subset U) Omega_ab=0,                      (13)

Omega_ab=(v_a+v_b)/(u_a u_b).                        (14)
```

We call `Omega=(Omega_ab)` the reciprocal polarization edge form of the two
cross-stars.  The name records its origin: the hyperbolic polarization in
(9), followed by reciprocal normalization by the first cross-star.  The
residual gauge preserving `B_12=1` multiplies every `Omega_ab` by the same
nonzero scalar, so its vanishing and its inclusion sums are intrinsic to
this normalized branch.

## 4. Complement-incidence inversion closes the branch

### Lemma 1 (six-point complement-incidence inversion)

If edge weights `w_ab` on six points satisfy

```text
sum_({a,b} subset U) w_ab=0       for every |U|=4,    (15)
```

then every `w_ab=0`.

### Proof

Let `s=sum_(a<b)w_ab` and `d_a=sum_(b!=a)w_ab`.  Apply (15) to the complement
of `{a,b}`:

```text
w_ab=d_a+d_b-s.                                      (16)
```

Sum (16) over `b!=a` and use `sum_a d_a=2s`:

```text
d_a=4d_a-3s,
```

so `d_a=s`.  Equation (16) now gives `w_ab=s`, while its vertex sum gives
`s=d_a=5s`.  Characteristic zero forces `s=0`, proving the lemma.

Equivalently, the square `15 x 15` inclusion matrix `W_(2,4)(6)` is
invertible; in the fixed lexicographic ordering its determinant is

```text
det W_(2,4)(6)=1458=2*3^6.                            (17)
```

Apply Lemma 1 to (13).  Then `Omega_ab=0` for every pair.  Because every
`u_a` is nonzero,

```text
v_a+v_b=0                 for every a<b in S.         (18)
```

On any three indices, the three equations in (18) have coefficient matrix

```text
[1 1 0]
[1 0 1]        with determinant -2.                  (19)
[0 1 1]
```

Hence all three corresponding `v`'s vanish, contradicting the full-edge
torus.  This proves (2).  Notice that the rows using the second complement
vertex and the rows entirely inside `S` are not needed: the contradiction
occurs one layer earlier.

## 5. Incidence-line consequence

Let a full-rank P7 root sensor meet the diagonal target space in one line,
so its allowable shallow-cofactor vectors form `K_Gamma=K c`.  Every pinned
maximal minor is homogeneous of degree eight in the `h_4` coordinates, and
therefore is either zero on the entire nonzero line or nonzero everywhere on
that line.

If the line lies in the selected pinned determinantal locus and `c` is
realized by a full-edge-torus graph, the prior exclusions together with (2)
force every minimal pinned dependency to have support seven or eight.  The
later Boolean-Lefschetz theorem reduces this further to full support eight.
This is a sharper singular normal form, not an exclusion of the determinantal
branch.  In particular, it does not prove that the target line is graph
realizable or that either surviving support size is impossible.

## 6. Exact wall

```text
P7 full-edge-torus pinned circuits of size 1..4: IMPOSSIBLE (PRIOR);
P7 full-edge-torus pinned circuits of size 5:    IMPOSSIBLE (PRIOR);
P7 full-edge-torus pinned circuits of size 6:    IMPOSSIBLE (THIS NOTE);
P7 full-edge-torus pinned circuits of size 7:    IMPOSSIBLE (LATER NOTE);
P7 full-edge-torus pinned circuits of size 8:    UNKNOWN;
P7 pinned matrix full rank on the edge torus:    UNKNOWN;
target cofactor line graph-torus realizability:  UNKNOWN;
P7 obstruction:                                 UNKNOWN;
global Krenn--Gu:                                UNRESOLVED.           (20)
```

No supports, configurations, graphs, finite fields, words, or parameter
tuples were enumerated.  The replays check only the displayed universal
polynomial identities and fixed characteristic-zero incidence maps.

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_pinned_h4_torus_support_six_reciprocal_polarization_exclusion.py
python claims/p7/audit_p7_pinned_h4_torus_support_six_reciprocal_polarization_exclusion.py
python -m py_compile verify_p7_pinned_h4_torus_support_six_reciprocal_polarization_exclusion.py audit_p7_pinned_h4_torus_support_six_reciprocal_polarization_exclusion.py
uv run --with ruff ruff check verify_p7_pinned_h4_torus_support_six_reciprocal_polarization_exclusion.py audit_p7_pinned_h4_torus_support_six_reciprocal_polarization_exclusion.py
```

The primary verifier checks the two hafnian row reductions, exact ranks and
determinant of the fixed inclusion maps, and the final three-index
contradiction.  The independent standard-library audit repeats the
polynomial identities with a sparse monomial dictionary and the incidence
calculations with fraction-free integer elimination.  Neither imports the
other or any project code.
