# Arbitrary permanent star-pair same-mode noncommon and support-two boundary

## Status

This note proves an exact characteristic-zero reduction inside the
simultaneous projection-drop residual for the displayed equality-five
`(4,1)` star pair.  A remaining local plane can have rank two under both
mixed-factor projection families only on their common ambient kernel line

```text
N=K(x_1+x_2),
```

and that occurrence must be singleton-supported at local colour `0` or `1`.
Every common-line occurrence, including the surviving singleton boundary,
propagates to the exact companion line

```text
Q=K(x_2+x_3)
```

as a singleton at colour `2` in another mode.

The proof classifies every same-mode pair from the two three-line exceptional
sets.  Common/noncommon pairs die by ambient-kernel rigidity.  Four
noncommon/noncommon pairs die in the quotient of a legal single-contraction
map.  A support-two common-line occurrence would make the polarization of
`x_0x_4x_5` restrict to a concise weighted `Delta_3`; its rank-one-free slice
space proves that impossible.

The singleton common-line branch remains open.  An exact rational fixture
below satisfies the full slices forced by `N` and `Q`, keeps every local
triple independent and every restricted projection rank at least two, but
fails uncontracted target entries.  It is a sharpness witness for the present
method, not an extension and not a counterexample to the conjecture.

The theorem is pointwise for the displayed based star frame.  It does not
classify the surviving distinct-mode incidences, transport to all based
frames in the unbased `(4,1)` orbit, or treat the `(3,1)` orbit.  Unrestricted
permanent nonrestriction remains unknown, and the global Krenn--Gu conjecture
remains **UNRESOLVED**.

## 1. Fixed star frame and target equations

Let `K` be a field of characteristic zero and split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5},          (1)
```

with

```text
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                  (2)
```

At modes `0,1`, use the displayed star pair

```text
u_0=-x_0+x_2,      u_1=x_0-x_3,       u_2=x_1-x_2,
v_0=x_0+x_1-x_2+x_3,
v_1=x_0+x_1,       v_2=-x_1+x_2.                        (3)
```

Its complementary mixed and diagonal quartics are

```text
star(m_1)=x_4x_5 x_3(x_0+x_1-x_2),
star(m_2)=x_4x_5 (x_0-x_3)(x_1-x_2),

star(d_0)=x_4x_5(
  x_0x_1+x_0x_3-x_1x_2+2x_1x_3-x_2x_3),
star(d_1)=-x_4x_5 x_2(x_0+x_1-x_3),
star(d_2)= 2x_4x_5 x_0x_3.                              (4)
```

Let ordered independent triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                  t=2,3,4,5,
```

span the local three-planes `L_t`.  Assume the full exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (5)
```

The two mixed-factor projections are

```text
Phi_1=(x_3,x_4,x_5,x_0+x_1-x_2),
Phi_2=(x_0-x_3,x_4,x_5,x_1-x_2).                       (6)
```

The kernel-support predecessor proves that every restricted projection has
rank at least two and that every rank-two kernel is one of

```text
Phi_1: N=x_1+x_2,      B_0=x_0+x_2,      C_0=x_0-x_1,
Phi_2: N=x_1+x_2,      B_1=x_0+x_3,      C_1=x_0+x_1+x_2+x_3.  (7)
```

Their forced missing local colours are

```text
N misses 2;       B_0 misses 0;       C_0 misses 1;
                  B_1 misses 1;       C_1 misses 0.      (8)
```

## 2. Common-line rigidity

Solving (6) gives

```text
ker(Phi_1)={p_1(a,b)=(a,b,a+b,0,0,0)},
ker(Phi_2)={p_2(a,b)=(a,b,b,a,0,0)},                    (9)
```

and hence

```text
ker(Phi_1) intersect ker(Phi_2)=K N.                    (10)
```

If `N subset L_t`, then it belongs to both restricted kernels.  The rank-two
floor says each intersection in (9) has dimension at most one, so both equal
`K N`.  Thus the four same-mode pairs

```text
(N,B_1), (N,C_1), (B_0,N), (C_0,N)                     (11)
```

are impossible.  No target contraction beyond the predecessor rank floor is
used here.

## 3. Legal quotient for two noncommon lines

For a square-free quadratic core `g_z` in (4), let

```text
B_z:R -> R^*
```

be its polarized contraction map.  Put

```text
g_1=( 1,1,-1,1),             g_2=(-1,1,-1,1),
U=span{g_1,g_2}.                                         (12)
```

Fix one displayed generator

```text
p in {B_0,C_0},                q in {B_1,C_1}           (13)
```

inside the same `L_t`.  They are independent.  Write their local coefficient
columns as

```text
p=sum_c alpha_c y_(t,c),       q=sum_c beta_c y_(t,c),
r_c=(alpha_c,beta_c).                                     (14)
```

On the other three tensor slots, define

```text
Theta(ell)(z_s,z_u,z_v)
 =[x_0x_1x_2x_3x_4x_5](x_4x_5 ell)z_s z_u z_v,
Q=ker Theta.                                               (15)
```

This is a legal single contraction in the shared mode.  The mixed equations
and the line memberships give

```text
B_(m_1)p=0,       B_(m_2)p=g_2,
B_(m_1)q=g_1,     B_(m_2)q=0,                            (16)
```

so `U subset Q`.  Let

```text
I={c:r_c!=0}.
```

The coordinate map on `span{p,q}` is injective, so `|I|>=2`.  For every
`c in I`, the single-contracted diagonal equations put the nonzero pure
three-tensor

```text
tau_c=e_c^* tensor e_c^* tensor e_c^*
```

in `im Theta`.  The `tau_c` are independent, whence

```text
rank Theta>=|I|,                dim Q<=4-|I|.             (17)
```

Since the two-space `U` lies in `Q`, (17) forces

```text
|I|=2,                         Q=U.                       (18)
```

For a nonzero row `r_c`, the vector

```text
z_c=beta_c p-alpha_c q
```

has zero local `c`-coordinate, so

```text
B_(d_c)z_c in U.                                          (19)
```

For the unique zero row, both `B_(d_c)p` and `B_(d_c)q` lie in `U`.

Use the quotient coordinates

```text
pi:R^* -> K^2,             pi(w)=(w_1+w_2,-w_1+w_3).    (20)
```

They have kernel exactly `U`.  With

```text
a=(-2,2),                     b=(0,2),                   (21)
```

direct contraction of (4) gives the complete diagonal quotient table

```text
line       pi B_(d_0)       pi B_(d_1)       pi B_(d_2)

B_0             0                 a                 b
C_0            -a                 0                 b
B_1            -a                 0                 b
C_1             0                 a                 b.    (22)
```

Both `a` and `b` are nonzero in characteristic zero.

## 4. Excluding all four noncommon pairs

### Same missing colour

For `(p,q)=(B_0,C_1)`, equation (8) gives

```text
alpha=(0,alpha_1,alpha_2),
beta =(0,beta_1,beta_2).                                (23)
```

The zero row is `r_0`.  Applying (19) and (22) for colours `1,2` gives

```text
(beta_1-alpha_1)a=0,          (beta_2-alpha_2)b=0.       (24)
```

Thus `alpha=beta`, contradicting the independence of `p,q` in the local
colour basis.  The pair `(C_0,B_1)` is identical with colours `0,1`
interchanged: its zero row is `r_1`, and the equal `d_0,d_2` quotient
columns again force `alpha=beta`.

### Different missing colours

For `(p,q)=(B_0,B_1)`, one has `alpha_0=beta_1=0`.  By (18), exactly one
row is zero.

```text
zero row r_0:  beta_0=0, but pi B_(d_0)q=-a!=0;
zero row r_1:  alpha_1=0, but pi B_(d_1)p= a!=0;
zero row r_2:  alpha_2=beta_2=0, but pi B_(d_2)p=b!=0.   (25)
```

Each line contradicts the zero-row consequence after (19).  For
`(p,q)=(C_0,C_1)`, the same three cases use respectively the nonzero entries
`pi B_(d_0)p=-a`, `pi B_(d_1)q=a`, and `pi B_(d_2)p=b`.

Therefore every noncommon/noncommon same-mode pair is impossible.  Together
with Section 2, only the proportional pair `(N,N)` remains.

## 5. Propagation from the common line

Contracting (4) once with

```text
N=x_1+x_2
```

gives, after suppressing `x_4x_5`,

```text
m_1=m_2=d_2=0,
d_0=h_0=( 1,-1,-1,1),
d_1=h_1=(-1,-1,-1,1).                                  (26)
```

Their common annihilator is

```text
H=ann_R(h_0,h_1)
 ={(0,u,v,u+v):u,v in K}.                               (27)
```

Write the local expansion of `N` in its mode as

```text
N=alpha_0y_0+alpha_1y_1,                                (28)
```

where either one or both coefficients are nonzero by (8).

### Lemma 1 (a companion meets `H`)

One of the other three local planes meets `H` nontrivially.

### Proof

Suppose all three intersections were zero.  Quotienting the ambient space by
`H` would preserve each remaining local dimension, giving three independent
triples in

```text
W=(R/H) direct-sum A,                  dim(R/H)=2.       (29)
```

The contracted target (26) is zero away from the pure diagonal colours in
the support of (28), and is nonzero on each such diagonal.

For two different colours in two modes, the usual map from `W` to `R/H`
obtained from the polarization of `x_4x_5(R/H)^*` kills the third local
three-space.  Its rank is at most one.  On the two-dimensional `R/H`
summand it is scalar multiplication by the `J`-pairing of the two selected
`A`-columns, so every cross-colour pairing vanishes.

If (28) has singleton support, the one-surviving-diagonal argument now makes
the two off-colour vectors in one local triple lie on one line in `A`,
contradicting independence.  If (28) has support `{0,1}`, both colours are
active.  Two-dimensional cross-orthogonality forces every colour-2
`A`-column in the three remaining modes to vanish.  In the original pure
colour-2 coefficient, only the removed mode could then supply an `A` factor.
It cannot supply both distinct factors `x_4,x_5`, contradicting the nonzero
`d_2` target.  Thus a nonzero companion in (27) exists.

Let `0!=q in L_b intersect H`, where `b` is different from the `N` mode.
For every `q=(0,u,v,u+v)`, direct contraction gives the covector identity

```text
2B_(m_1)q-B_(d_0)q+B_(d_1)q=0.                         (30)
```

Write `q=sum beta_c y_(b,c)`.  Apply the legal single-contraction map on the
other three modes.  The mixed targets vanish, while the `d_0,d_1` targets
are nonzero multiples of the independent tensors `tau_0,tau_1`.  Equation
(30) therefore forces

```text
beta_0=beta_1=0.                                        (31)
```

Thus `q` is singleton-supported at colour `2`.

The full contraction rows for `q=(0,u,v,u+v)` also satisfy

```text
u B_(d_2)q=(u+v)(B_(m_1)q+B_(m_2)q).                   (32)
```

The right side maps to zero under the target, while the left side maps to
`u lambda_2 beta_2 tau_2`.  Since every displayed scalar except possibly
`u` is nonzero, (32) gives `u=0`.  Consequently

```text
q in KQ,                  Q=x_2+x_3,                    (33)
```

and the colour-2 local vector in mode `b` is a nonzero multiple of `Q`.
This conclusion includes both singleton- and support-two occurrences of
`N`; no projective scaling of a local coefficient was separated from its
ambient line generator.

## 6. Excluding support-two `(N,N)` by cubic tensor rank

Assume one mode `a` has `N` as the kernel line of both projection families.
Section 5 supplies a distinct mode `b` whose colour-2 vector is a nonzero
multiple of `Q`.  Let `c,d` be the remaining two modes and define the scalar
trilinear form

```text
P_x(y,z,w)=pol(x_0x_4x_5)(y,z,w).                       (34)
```

Since `B_(d_2)Q=2x_0`, the contraction of the `d_2` target in mode `b`
gives

```text
P_x|_(L_a,L_c,L_d)=mu_2 e_2^* tensor e_2^* tensor e_2^*,
mu_2!=0.                                                (35)
```

On the other hand,

```text
x_0=(h_0-h_1)/2.                                       (36)
```

If `N` has support `{0,1}`, equations (26), (28), and the two nonzero
diagonal targets give

```text
P_x|_(L_b,L_c,L_d)
 =mu_0 e_0^* tensor e_0^* tensor e_0^*
  +mu_1 e_1^* tensor e_1^* tensor e_1^*,
mu_0mu_1!=0.                                           (37)
```

The first-mode slice map of `P_x` therefore sends

```text
y_(a,2), y_(b,0), y_(b,1)
```

to nonzero multiples of `E_22,E_00,E_11`, respectively.  Those matrices are
independent, so the three displayed ambient vectors are independent.  On
their span `Y`, (35)--(37) say that

```text
P_x|_(Y,L_c,L_d)
```

is a weighted `Delta_3` tensor.

Let `E` be the three-space with coordinates `(x_0,x_4,x_5)`.  The weighted
`Delta_3` tensor is concise in all three modes.  Hence the evaluation maps

```text
Y -> E,                   L_c -> E,                   L_d -> E             (38)
```

all have rank three and are isomorphisms.  Thus (38) would make the weighted
`Delta_3` tensor `GL_3^3`-equivalent to

```text
P=pol(XUV) in (E^*) tensor 3.                           (39)
```

But `P` has tensor rank greater than three.  Its first-mode slice space is

```text
S=span{sym(UV),sym(XV),sym(XU)}.                        (40)
```

It contains no nonzero rank-one matrix.  Indeed a nonzero rank-one symmetric
matrix is a scalar multiple of a square

```text
(aX+bU+cV)^2,
```

while membership in `S` makes the coefficients of `X^2,U^2,V^2` vanish and
hence forces `a=b=c=0`.  If the concise tensor `P` had rank at most three,
the three first-mode factors in a three-term decomposition would be
independent; isolating them would put three nonzero rank-one matrices in
`S`, a contradiction.  Therefore `rank(P)>3`, whereas weighted `Delta_3`
has rank three.  This excludes support-two `(N,N)`.

## 7. Exact singleton sharpness fixture

The preceding rank argument needs all three diagonal slices in
(35)--(37).  With singleton `N`, only two remain.  The following exact
rational fixture shows that the propagated full slices and all projection
rank floors are then jointly consistent.

Use mode order `(a,b,c,d)` and columns in local colour order:

```text
L_a:
  (0, 1, 1, 0, 0,0),
  (0, 1,-1/2, 3/2, 0,0),
  (0,-1, 1/2,-1/2, 1,0);

L_b:
  (1, 0,-1/2, 1/2, 0,0),
  (0, 1, 1/2, 3/2, 0,0),
  (0, 0, 1,   1,   0,0);

L_c:
  (0,-2, 0,   0,   0,1),
  (0, 0,-1,   1,   0,0),
  (1,-1, 1/2,-1/2, 0,0);

L_d:
  (0, 1, 1/2,-1/2, 1,0),
  (0, 1, 1/2, 1/2, 0,0),
  (0, 1,-2,   1,   0,1).                               (41)
```

Every triple is independent.  The two projection-rank profiles are

```text
Phi_1: (2,2,2,3),                Phi_2: (2,2,2,3).     (42)
```

Moreover `y_(a,0)=N` and `y_(b,2)=Q`.  Put

```text
r=x_0+x_1-x_2-x_3,              h_1=-x_0-x_1-x_2+x_3. (43)
```

Writing `B_y^ell` for the full bilinear contraction of
`pol(ell x_4x_5)` in the first slot, the fixture satisfies exactly

```text
B_(y_(a,i))^r=0,                 i=0,1,2,
B_(y_(a,i))^(x_0)=delta_(i,2) E_22,

B_(y_(b,i))^(h_1)=0,             i=0,1,2,
B_(y_(b,i))^(x_0)=delta_(i,0) E_00.                    (44)
```

Since `h_0=2x_0+h_1`, these are precisely all three-mode slices forced by a
singleton colour-0 `N` and its colour-2 companion `Q`, up to harmless nonzero
target scalars.

The fixture is not a full extension.  Direct exact evaluation gives, for
example,

```text
T_(d_1)(1,1,1,1)=0,                 required nonzero,
T_(m_1)(1,0,0,0)=3,                 required zero.     (45)
```

Thus (41) is a sharpness witness for any proof using only (44).  A successor
must use uncontracted entries such as (45), or another genuinely stronger
consequence of the full target.

## 8. Theorem and exact boundary

### Theorem 2 (same-mode boundary)

In an exact extension of the displayed star pair, a mode can be low for both
projection families only if their common kernel line `N` is singleton-
supported at colour `0` or `1`.  Such an occurrence forces a distinct mode
to contain `Q` singleton-supported at colour `2`.

Sections 2 and 4 exclude all common/noncommon and noncommon/noncommon pairs.
Section 6 excludes the support-two common/common case.  The kernel-support
predecessor proves that there are no other lines or support sizes.

```text
same-mode common/noncommon line pairs:                  EXCLUDED;
same-mode four noncommon/noncommon pairs:               EXCLUDED;
same-mode proportional N/N, support two:                EXCLUDED;
same-mode proportional N/N, singleton support:          OPEN;
singleton N/N forces Q singleton 2 in another mode:     PROVED;
all same-mode cross-family lows:                         NOT EXCLUDED;

distinct-mode exceptional incidences:                   NOT CLASSIFIED HERE;
all based frames in the unbased (4,1) orbit:             NOT TREATED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                            UNRESOLVED.    (46)
```

Replay the exact checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
python claims/arbitrary-order/audit_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py claims/arbitrary-order/audit_arbitrary_permanent_star_pair_same_mode_noncommon_and_support_two_boundary.py
```

The primary verifier reconstructs all six exceptional lines and their
single contractions, the legal quotient table, every noncommon case, the
common-line companion identities, the cubic rank obstruction, and every
entry claimed for the exact sharpness fixture.  The independent audit imports
neither the primary verifier nor SymPy: it rebuilds the star frame and
complementary cores from square-free edge dictionaries, uses standalone
rational row reduction and quotient coordinates, and directly evaluates the
cubic slices and full-target failures of (41).  The scripts replay displayed
algebra; the written characteristic-zero arguments prove the theorem.
