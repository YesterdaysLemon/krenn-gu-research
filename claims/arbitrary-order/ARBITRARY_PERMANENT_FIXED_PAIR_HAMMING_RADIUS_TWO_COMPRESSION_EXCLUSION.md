# Arbitrary permanent fixed-pair Hamming-radius-two compression exclusion

## Status

This note proves an exact characteristic-zero exclusion of a four-dimensional
compression family inside the low-projection residual of
`ARBITRARY_PERMANENT_FIXED_PAIR_DIMENSION_FIVE_FULL_PROJECTION_BOUNDARY.md`.
The fixed modes `0,1` are the same five-dimensional pair.  Modes `2,3,4`
may be arbitrary rank-three planes inside one explicit four-space `W`, and
mode `5` lies in one explicit three-space `V`.

On this family, both mixed-radical quartic tensors vanish automatically.
Nevertheless, the three nonzero pure coefficients and just the 54 equations
obtained by changing one or two of modes `2,3,4` are inconsistent.  The
proof factors the three diagonal sensors through an `R`-valued trilinear
map, makes that map colour-diagonal, and excludes every possible rank of the
three projections to a two-space `A`.

This is a successor to
`ARBITRARY_PERMANENT_FIXED_PAIR_HAMMING_TWO_SPLIT_COMPONENT_EXCLUSION.md`.
It neither modifies nor imports a stronger conclusion into that theorem.
The present family is larger in a different direction: the three local
planes need not coincide and need not be of the affine `h(s)` form.

The proof does **not** classify all cancellation-based simultaneous zeros
of the two mixed quartics.  The general fixed-pair Hamming-radius-two
residual remains open.  Unrestricted `P_6 -> Delta_3` and arbitrary-order
permanent nonrestriction remain unknown, and the global Krenn--Gu
conjecture remains **UNRESOLVED**.

## 1. Fixed pair and compression spaces

Let `K` be a field of characteristic zero and

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).                       (1)
```

At modes `0,1`, fix

```text
u_0=x_0-x_3,      u_1=x_1-x_3,      u_2=x_2-x_3,
v_0=x_1+x_2,      v_1=x_0+x_2,      v_2=x_2-x_3.            (2)
```

Write `d_e=u_ev_e`.  In edge order `(01,02,03,12,13,23)`,

```text
d_0=(1,1,0,0,-1,-1),
d_1=(1,0,-1,1,0,-1),
d_2=(0,0,0,0,0,-2).                                      (3)
```

The two nonzero mixed products are

```text
m_1=(0,1,-1,0,0,-1),       m_2=(0,0,0,1,-1,-1).           (4)
```

Put

```text
ell_1=x_3-x_2-x_0,                 ell_2=x_3-x_2-x_1.     (5)
```

Define

```text
W=ker(x_0) intersect ker(ell_2)
 =span{x_1+x_3, x_2+x_3, x_4, x_5},                       (6)

V={z:x_4(z)=x_5(z)=0 and ell_1(z)=-x_1(z)}
 =span{x_0+x_3, x_1-x_3, x_2+x_3}.                        (7)
```

For each `t=2,3,4`, choose any independent ordered triple

```text
(y_(t,0),y_(t,1),y_(t,2)) subset W.                       (8)
```

Thus each triple spans an arbitrary three-plane inside the four-space `W`.
At mode `5`, choose an ordered basis `(z_0,z_1,z_2)` of `V`.

The rank contradiction below only needs the three `z_e` appearing in their
matching pure and shell equations; their independence is part of the
intended rank-three local-map locus but is not otherwise used.

The earlier Hamming-one sharp fixture is a point of this family.  Its
common plane is

```text
span{x_4,x_5,x_1-2x_2-x_3} subset W,                         (8a)
```

and its mode-five basis

```text
(2x_1+2x_2, 2x_1-2x_3, x_0+x_1)                            (8b)
```

is a basis of `V`.

## 2. Exact statement and shell scope

### Theorem 1 (the `W/V` compression is excluded at radius two)

There are no triples (8) and vectors `z_e in V` satisfying both

```text
[x_0...x_5] d_e y_(2,e)y_(3,e)y_(4,e)z_e != 0
for e=0,1,2,                                                  (9)
```

and

```text
[x_0...x_5] d_e y_(2,i)y_(3,j)y_(4,k)z_e = 0                (10)
```

whenever

```text
1 <= distance((i,j,k),(e,e,e)) <= 2.                         (11)
```

There are exactly

```text
3 * (3 choose 1)*2 + 3 * (3 choose 2)*2^2 = 54              (12)
```

equations in (10)--(11).  They are the Hamming-one and Hamming-two equations
obtained by changing only modes `2,3,4`, while the pair colours and the
mode-five colour stay equal to `e`.  No shell equation changing modes
`0,1,5` is needed.

The full accumulated Hamming-radius-two target equations imply (10), so
Theorem 1 excludes the whole `W/V` family in the intended application.

## 3. Coordinates and the three diagonal sensor factors

Since `x_0=0` and `x_3=x_1+x_2` on `W`, every `y in W` has a unique
expression

```text
y=alpha(x_1+x_3)+beta(x_2+x_3)+a x_4+b x_5.              (13)
```

Write

```text
r(y)=(alpha,beta) in R=K^2,       a(y)=(a,b) in A=K^2.   (14)
```

On `A`, define the nondegenerate symmetric form

```text
J((a,b),(a',b'))=ab'+ba',          matrix [0 1; 1 0].    (15)
```

It extracts the `x_4x_5` coefficient from the product of two `A`-parts.

Every `z in V` is uniquely

```text
z=(gamma,delta,epsilon,gamma-delta+epsilon,0,0).          (16)
```

Define covectors

```text
p_0(alpha,beta)=alpha+beta,       q_0(z)=epsilon,
p_1(alpha,beta)=beta,             q_1(z)=gamma-delta+epsilon,
p_2(alpha,beta)=alpha,            q_2(z)=gamma.           (17)
```

Thus

```text
p_0=p_1+p_2,                                             (18)
```

every two distinct `p_e` span `R^*`, and the three `q_e` form a basis of
`V^*`.

Define the `R`-valued trilinear map

```text
C(y_2,y_3,y_4)
 =r(y_2)J(a(y_3),a(y_4))
 +r(y_3)J(a(y_2),a(y_4))
 +r(y_4)J(a(y_2),a(y_3)).                               (19)
```

The fixed diagonal quadratics are

```text
d_0=x_0x_1+x_0x_2-x_1x_3-x_2x_3,
d_1=x_0x_1-x_0x_3+x_1x_2-x_2x_3,
d_2=-2x_2x_3.                                            (20)
```

For


```text
r=alpha(x_1+x_3)+beta(x_2+x_3)
```

and `z` from (16), direct complement pairing in four variables gives

```text
[x_0x_1x_2x_3]d_0rz =  2(alpha+beta)epsilon,
[x_0x_1x_2x_3]d_1rz =  2beta(gamma-delta+epsilon),
[x_0x_1x_2x_3]d_2rz = -2alpha gamma.                     (21)
```

Because `z` has no `x_4,x_5`, exactly two of `y_2,y_3,y_4` must supply
those variables.  The remaining one supplies its `R`-part.  Equations
(15), (19), and (21) therefore give the exact four-linear sensor
factorization

```text
Q_e(y_2,y_3,y_4,z)
 :=[x_0...x_5]d_e y_2y_3y_4z
  =sigma_e q_e(z)p_e(C(y_2,y_3,y_4)),                    (22)

(sigma_0,sigma_1,sigma_2)=(2,2,-2).                     (23)
```

No genericity or basis normalization is used in (22).

### Optional full-shell consequence at mode five

Under all Hamming-one target equations, not merely the 54 equations in
Theorem 1, changing mode `5` from `e` to `f!=e` while keeping the other
colours equal to `e` gives

```text
0=Q_e(y_(2,e),y_(3,e),y_(4,e),z_f)
 =sigma_e q_e(z_f)p_e(C_(eee)).                          (24)
```

Pure nonvanishing makes the last `p_e` factor nonzero, so

```text
q_e(z_f)=0 for e!=f,              q_e(z_e)!=0.           (25)
```

Thus the mode-five basis is, up to three nonzero scalars, the basis dual to
`q_0,q_1,q_2`.  This useful normalization is forced by the full Hamming-one
shell, but the contradiction below only needs the matching `z_e` and (9).

## 4. Both mixed-radical tensors vanish automatically

The two mixed-radical complementary quartics are

```text
F_1=x_1x_4x_5ell_1,             F_2=x_0x_4x_5ell_2.     (26)
```

On `W`,

```text
x_0=ell_2=0,                    ell_1=x_1.               (27)
```

On `V`,

```text
x_4=x_5=0,                     ell_1=-x_1.               (28)
```

For `F_2`, each of the three `W` columns can occupy only the two nonzero
factor rows `x_4,x_5`; the `V` column occupies `x_0` or `ell_2`.  No
four-factor matching exists, so the pulled-back permanent is identically
zero.

For `F_1`, two `W` columns supply `x_4,x_5`.  If the remaining `W` column
has `(x_1,ell_1)=(alpha,alpha)` and the `V` column has
`(x_1,ell_1)=(delta,-delta)`, their two assignments contribute

```text
alpha(-delta)+alpha delta=0.                              (29)
```

Thus `F_1` also vanishes identically.  The mixed equations are consequences
of the compression geometry, not extra hypotheses in Theorem 1.

## 5. The radius-two shell makes `C` colour-diagonal

Put

```text
C_(ijk)=C(y_(2,i),y_(3,j),y_(4,k)).                      (30)
```

Equations (9) and (22) imply

```text
q_e(z_e)!=0,                p_e(C_(eee))!=0,             (31)
```

so every `C_(eee)` is nonzero.

If `(i,j,k)` is at distance one or two from `(e,e,e)`, equations (10),
(22), and (31) give

```text
p_e(C_(ijk))=0.                                          (32)
```

Take any nonconstant triple.

- If it uses exactly two colours `c,e`, its distances from `c^3` and
  `e^3` are one and two in some order.  Hence both `p_c` and `p_e` vanish
  on `C_(ijk)`.  Any two distinct `p`'s span `R^*`, so `C_(ijk)=0`.
- If it uses all three colours, its distance from every constant triple is
  two, and again `C_(ijk)=0`.

Consequently

```text
C_(ijk)=0 unless i=j=k,             C_(eee)!=0.          (33)
```

## 6. Off-diagonal `J`-orthogonality

Fix distinct modes `s,t in {2,3,4}`, distinct labels `i!=j`, and let `u` be
the remaining mode.  Write

```text
y_(s,i)=(r,a),                    y_(t,j)=(r',a').       (34)
```

The linear map

```text
K_(y,z):W -> R,                   w |-> C(y,z,w)          (35)
```

kills the independent triple `(y_(u,0),y_(u,1),y_(u,2))`, because every
corresponding colour triple contains the distinct labels `i,j` and is
nonconstant.  Hence

```text
dim ker K_(y,z)>=3,               rank K_(y,z)<=1.       (36)
```

On the `R`-summand of `W=R direct-sum A`, equation (19) gives

```text
K_(y,z)(r'',0)=J(a,a')r''.                                (37)
```

If `J(a,a')` were nonzero, this restriction would have rank two.
Therefore

```text
J(a_(s,i),a_(t,j))=0
for every s!=t and i!=j.                                  (38)
```

## 7. The complete projection-rank split

For `t=2,3,4`, put

```text
rho_t=dim span{a_(t,0),a_(t,1),a_(t,2)} subset A.         (39)
```

The three `y_(t,e)` are independent while `dim R=2`, so `rho_t=0` is
impossible.  Hence `rho_t` is one or two.

### Lemma 2 (rank one is impossible)

No `rho_t` equals one.

### Proof

By symmetry, suppose `rho_2=1`.  Let `Ka` be its nonzero image line and

```text
S={e:a_(2,e)!=0}.                                        (40)
```

First suppose `|S|>=2`.  For every label `j`, choose `i in S` with `i!=j`.
Equation (38) puts every `a_(3,j)` and every `a_(4,j)` in the common line
`a^perp`.  In each diagonal value from (19), the two terms pairing
`a_(2,e)` with the other modes vanish, so

```text
C_(eee)=r(y_(2,e))J(a_(3,e),a_(4,e)).                   (41)
```

Nonvanishing of all three diagonal values forces every `a_(3,e)` and
`a_(4,e)` to be nonzero and forces `J` to be nonzero on the square of the
one-dimensional line `a^perp`.  Any two nonzero vectors on that line then
pair nontrivially.  In particular,

```text
J(a_(3,i),a_(4,j))!=0 for i!=j,                          (42)
```

contradicting (38).

Now suppose `|S|=1`, with unique label `h`, and let `i,j` be the other two
labels.  Equation (38) puts

```text
a_(3,i),a_(3,j),a_(4,i),a_(4,j) in a^perp.              (43)
```

For `e=i,j`, equation (41) still holds because `a_(2,e)=0`.  The two
nonzero diagonal values make all four vectors in (43) nonzero and make the
self-pairing of `a^perp` nonzero.  Hence

```text
J(a_(3,i),a_(4,j))!=0,                                  (44)
```

again contradicting (38).  Since `S` is nonempty, these cases exhaust
`rho_2=1`.  Symmetry proves the lemma.

It follows that

```text
rho_2=rho_3=rho_4=2.                                    (45)
```

### Lemma 3 (rank-two common-zero label)

Let `(a_0,a_1,a_2)` and `(b_0,b_1,b_2)` each span the two-space `A`, and
suppose

```text
J(a_i,b_j)=0 for i!=j.                                  (46)
```

Then the two arrays have a common zero-labelled column, and each array has
exactly one zero column.

### Proof

Choose independent columns `b_j,b_k` and let `h` be the remaining label.
Since `b_j!=0`, both `a_k,a_h` lie in the one-dimensional line
`b_j^perp`; similarly, `a_j,a_h` lie in `b_k^perp`.  If `a_h!=0`, all three
`a` columns are proportional, contrary to their rank two.  Thus `a_h=0`.

The remaining `a_j,a_k` are independent.  Equation (46) makes `b_h`
orthogonal to both, so nondegeneracy of `J` gives `b_h=0`.  A rank-two
three-column array cannot have two zero columns, proving uniqueness.

Apply Lemma 3 to mode pairs `(2,3)` and `(2,4)`.  Mode `2` has a unique zero
column, so both common-zero labels coincide, say `h`.  Therefore

```text
a_(2,h)=a_(3,h)=a_(4,h)=0.                              (47)
```

Every term in (19) vanishes at label `h`, giving

```text
C_(hhh)=0,                                               (48)
```

contrary to (33).  This completes the proof of Theorem 1.

## 8. Exact scope and replay

The proof is pointwise and nongeneric.  It uses no algebraic closure and no
division by a variable parameter.  The factors `2,-2` in (21)--(23) explain
the stated characteristic-zero scope; the argument extends verbatim to
every field of characteristic different from two.

The exact boundary is

```text
W/V compression under three pure + 54 middle H1/H2:       EXCLUDED;
arbitrary bases of arbitrary 3-planes L_2,L_3,L_4 in W:   INCLUDED;
arbitrary basis of the fixed 3-space V at mode 5:         INCLUDED;
mixed-radical equations on this family:                   AUTOMATIC;
other simultaneous mixed-quartic zero loci:               NOT CLASSIFIED;
general fixed-pair radius-two residual:                    OPEN;
unrestricted P_6 -> Delta_3:                               UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.  (49)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_hamming_radius_two_compression_exclusion.py
```

The primary verifier checks the coordinate descriptions of `W,V`, all five
pairing identities, the four-linear factorization (22), automatic radical
vanishing, the 54 shell-to-diagonal implications, and symbolic rank-case
witnesses.  The independent no-import audit uses separate exact arithmetic,
exhaustive finite-field tests of the sensor factorization, and a complete
`F_3` enumeration of the abstract `A`-projection obstruction.  These finite
checks replay identities and conventions.  The written rank argument proves
the characteristic-zero theorem.
