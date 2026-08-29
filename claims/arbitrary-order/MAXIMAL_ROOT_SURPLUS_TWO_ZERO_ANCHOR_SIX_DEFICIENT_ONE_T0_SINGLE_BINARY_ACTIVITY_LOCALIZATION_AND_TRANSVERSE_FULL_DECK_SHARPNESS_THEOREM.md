# Maximum-root surplus-two zero-anchor six-deficient one-`T_0` single-binary activity localization and transverse full-deck sharpness

## Status

This is theorem package **GLS72**.  It continues the strict-parent descent of
`GLS71` and localizes every possible Family-A `r=1` source in the key

```text
S_0 R_2 R_1 R_0^2 T_0.
```

The proof is over the same characteristic-zero function field as
`GLS61`--`GLS71`.  It excludes the all-active cell, every cell with a silent
`R_0` port, and all but one scalar branch when the unique `T_0` port is
silent.  The remaining branch is

```text
alpha=[e_(1,1)e_(2,2)]W_12=0,
[e_(1,1)]W_15|_(K_5)=[e_(2,2)]W_25|_(K_5)=0.        (S)
```

An exact common physical-edge array realizes every selector, attachment,
and full-deck equation used here on (S).  Its required pure full coefficient
is supplied by the transverse value of `W_25` at `e_(5,0)`, invisible on the
`T_0` kernel.  Therefore this package is a sharp localization and
source-integrability boundary, **not** an exclusion of the key.

The six-deficient residual remains `98,355 / 81` profiles/keys.  Family A at
`r=1,2,3`, Family B at `r=3`, every other five-/six-deficient branch, every
earlier residual branch, and the global Krenn--Gu conjecture remain
**OPEN / UNRESOLVED**.

## 0. Parent obligation and notation

Use the Family-A normalization from `GLS71`.  Its binary triangle is

```text
T={0,1,2},                    O={3,4,5},              (1)
D_0=O,                        D_1={0,2},
D_2={0,1}.
```

The two pure pair faces force, up to the recorded symmetries and nonzero
scalings,

```text
p_0=P_1 e_1,       q_0=Q_2 e_2,
p_1=P_2 e_2,       q_1=0,
p_2=0,             q_2=Q_1 e_1.                    (2)
```

Exactly one outside port has type `T_0`; the other two have type `R_0`.
On an `R_0` port `i`, write

```text
K_i=K x_i direct-sum K y_i,
```

whereas on the `T_0` port write

```text
K_i=K z_i,                    x_i=y_i=z_i             (3)
```

after absorbing the two nonzero evaluations into the global target
scalars.  Equality in (3) means equality of chosen generators of the one
line; it does not identify the two target colours on either `R_0` port.

The `GLS71` scalar notation must be enlarged at the `T_0` port.  Define the
whole row covectors

```text
P_u=[P_0]p_u,                 Q_u=[Q_0]q_u,
A_P={u:P_u!=0},               A_Q={u:Q_u!=0}.        (4)
```

At an `R_0` port these are scalar multiples of `e_(u,0)`.  At the `T_0`
port they may have a second component in `Ann(K_u)`; no purity of that row
covector is assumed.

### Lemma 0.1 (rank-two activity and one-silent bridge)

The pure outside equation gives

```text
|A_P union A_Q|>=2.                                  (4a)
```

Every active port exposes the same direction-appropriate strict-parent
selectors as in the `GLS71` table, even when its nonzero row covector is not
pure.  If exactly one port `s` is silent and `{v,w}=O-{s}`, then

```text
C_vw=P_v tensor Q_w+Q_v tensor P_w!=0,
C_vw tensor H_(012s)=mu_0 tensor_(i=0)^5 e_(i,0),   (4b)
```

so `C_vw` is proportional to `e_(v,0)e_(w,0)` and the unrestricted deck
`H_(012s)` is nonzero and pure.  At least one crossed summand in `C_vw` is
nonzero and supplies the two mixed selectors used below.

### Proof

If fewer than two outside ports are active, every distinct-endpoint term in
the full `P_0Q_0` coefficient vanishes, contradicting its nonzero target.
For `u in A_P`, the `P_0Q_2` coefficient of the strict four-open equation
on `T union {u}` has the unique source pair `{0,u}`; the `P_0Q_1`
coefficient has the unique source pair `{2,u}`.  In each case the nonzero
row covector `P_u` tensors the relevant physical deck and the target
coefficient is zero, so the deck itself is zero.  The `P_1Q_0` and
`P_2Q_0` coefficients for `u in A_Q` are identical, using pairs `{0,u}`
and `{1,u}`.  This proves selector legality without choosing a line inside
the `T_0` row plane.

If `s` is silent, `P_s=Q_s=0`, not merely zero in one row coordinate.  The
only surviving distinct-endpoint term in the full `P_0Q_0` coefficient is
the pair `{v,w}`, which gives (4b).  A nonzero tensor product equal to the
displayed pure tensor makes both factors pure across that cut.  Since
`C_vw!=0`, one of its two crossed summands is nonzero; its `P` endpoint and
`Q` endpoint expose the two `E` selectors and the corresponding `F/G`
pair. `square`

On the outside kernels put

```text
A=W_12,
Y_i=W_(1i)|_(K_i),       Z_i=W_(2i)|_(K_i),
B_jk=W_jk|_(K_j tensor K_k).                         (5)
```

If all three outside ports are active, the three selector equations and
the two pure attachments are

```text
A B_jk+Y_j Z_k+Y_k Z_j=0,                            (6)
sum_i Y_i B_(O-{i})=lambda e_1 x_3x_4x_5,
sum_i Z_i B_(O-{i})=mu e_2 y_3y_4y_5,
lambda mu!=0.                                        (7)
```

This is the serious parent-theorem continuation required by the repository
policy: it combines the crossed pair mechanism, all activity selectors,
both attachments, and the unrestricted missing-colour deck.  It is not a
third disconnected sibling refinement.

## 1. Three active ports remain impossible

### Theorem 1.1 (one proportional outside port does not rescue three selectors)

Equations (6)--(7) have no solution when two outside kernel pairs
`x_i,y_i` are independent and the third pair spans one common line.

### Proof

The alternating argument of `GLS71` Theorem 5.1 is unchanged and gives

```text
A=alpha e_1 tensor e_2.                              (8)
```

Project as there, writing `k_i` for the `e_1` coordinate of `Y_i` and
`l_i` for the `e_2` coordinate of `Z_i`.  Suppose first `alpha!=0`.
Eliminating the three `B` tensors gives

```text
k_3k_4l_5+k_3l_4k_5+l_3k_4k_5 proportional x_3x_4z_5,
l_3l_4k_5+l_3k_4l_5+k_3l_4l_5 proportional y_3y_4z_5. (9)
```

At each `R_0` port the pair `k_i,l_i` is independent: otherwise the two
nonzero tensors in (9) would have one common local factor line, while their
target factors `x_i,y_i` are independent.  Write

```text
k_5=a z_5,                    l_5=b z_5.
```

In the bases `(k_3,l_3)` and `(k_4,l_4)`, the two coefficient matrices in
(9) are

```text
M_x=[[b,a],[a,0]],            M_y=[[0,b],[b,a]].     (10)
```

Both targets have rank one.  Hence `det M_x=-a^2=0` and
`det M_y=-b^2=0`.  Then `a=b=0`, making both tensors zero, a
contradiction.

Now let `alpha=0`.  The three pair equations are

```text
k_i l_j+l_i k_j=0.                                  (11)
```

If `k_i,l_i` are independent at one `R_0` port, (11) kills both coordinates
at the other two ports.  The two attachments then use the same
complementary `B` tensor, which would have to be proportional to both
complementary target products; those products differ on the other `R_0`
port.  Otherwise every doubly active port has `k_i=r_i l_i`.  Two doubly
active ports require opposite ratios and three would require `2r_i=0`.
If exactly two, say `i,j`, are doubly active, no third one-sided activity is
compatible with (11).  Choose `i` to be an `R_0` port.  Adding the
`l` attachment to `r_i^(-1)` times the `k` attachment cancels the `j` term
and gives

```text
2l_i B_(O-{i})=mu y_3y_4z_5+lambda r_i^(-1)x_3x_4z_5. (11a)
```

The left flattening at `i` has rank at most one and the right flattening has
rank two.  With one doubly active port, all other ports are inactive and
the two complete attachments are proportional, whereas their target
tensors differ on both `R_0` ports.  With no doubly active port, (11)
forbids a `k`-only port from coexisting with an `l`-only port, so one
attachment vanishes.  These cases exhaust (11).
`square`

### Corollary 1.2 (the `r=1` activity fork)

Every hypothetical Family-A `r=1` source has exactly one selector-silent
outside port.

## 2. A silent `R_0` port is impossible

### Theorem 2.1 (transfer of the `GLS71` one-silent proof)

The silent port in Corollary 1.2 cannot have type `R_0`.

### Proof

Relabel the silent port as `5`.  Then `x_5,y_5` are independent, while the
active pair `{3,4}` contains one `R_0` and one `T_0` port.  Thus
`x_3x_4` and `y_3y_4` are independent.  Lemma 0.1 makes the active-pair
tensor pure and supplies at least one nonzero crossed summand.  Its two
whole row covectors expose the same four legal decks

```text
E_45=E_35=F_45=G_35=0                               (12)
```

as in `GLS71` Theorem 6.3, after possibly exchanging `3,4` and the two
probe shores.  The pure outside coefficient again isolates

```text
H_(0125)=nu e_(0,0)e_(1,0)e_(2,0)e_(5,0),
nu!=0.                                               (13)
```

The projection proof in `GLS71` equations (53)--(64a) needs independence
only in the following places:

1. `x_5,y_5` separate the two attachments and make the two nonzero members
   in (54) independent;
2. `x_3x_4,y_3y_4` separate the first line of (54a);
3. after substituting `x_T=y_T=z_T`, equation (58) still has a
   `y_R z_T y_5` word occurring only with coefficient `q`, so `q=0`, and
   its `x_R z_T x_5` word then gives `s=0`; equation (59) symmetrically gives
   `tau=r=0`;
4. the `alpha=0` flattening may be taken at port `5`, and every common-factor
   contradiction in (63) again uses the independent lines `x_5,y_5`.

All four conditions hold here.  The displayed formulas otherwise remain
identical after `x_T=y_T=z_T`.  In particular, after the restricted
`beta_4=beta_5=0` conclusion and `B_45!=0`, the `F_45` projection is
`U_00 B_45=0` and kills the unrestricted scalar
`U_00=[e_(0,0)e_(1,0)]W_01`.  Likewise `G_35`, the restricted
`delta_3=delta_5=0` conclusion, and `B_35!=0` kill the unrestricted scalar
`V_00=[e_(0,0)e_(2,0)]W_02`.  Thus arbitrary off-kernel values of
`W_15,W_25` are multiplied by zero in the full coefficient (64a); no
transport from `K_5` to `e_(5,0)` is used.  Consequently the full central
scalars

```text
[e_(0,0)e_(1,0)]W_01,
[e_(0,0)e_(2,0)]W_02,
[e_(1,0)e_(2,0)]W_12                                (14)
```

all vanish.  Every term in the pure coefficient of (13) is therefore zero,
contradicting `nu!=0`. `square`

The theorem uses independence at the silent port, not an invalid
independence assertion at the `T_0` port.

## 3. The silent-`T_0` equations

It remains to put the unique `T_0` port at `5`, so ports `3,4` are `R_0`.
Assume, after the usual exchange, that the nonzero activity product is
`a_3b_4`.  It supplies `E_45,E_35,F_45,G_35` exactly as in the `GLS71`
selector table.

Write

```text
B_45=L_4 tensor z,              B_35=L_3 tensor z,
u_5=a z,                        v_5=b z,
X=x_3x_4,                       Y=y_3y_4,             (15)
```

where `u_i=[e_(1,1)]Y_i`, `v_i=[e_(2,2)]Z_i`, and identify tensors carrying
the common final factor `z`.  Put

```text
alpha=[e_(1,1)e_(2,2)]A,       B=B_34.
```

The two `E` equations and attachments become

```text
alpha L_i+b u_i+a v_i=0,                    i=3,4,   (16)
u_3L_4+L_3u_4+aB=lambda X,
v_3L_4+L_3v_4+bB=mu Y,             lambda mu!=0.    (17)
```

The one-silent full-deck lemma still gives the unrestricted equality

```text
H_(0125)=nu e_(0,0)e_(1,0)e_(2,0)e_(5,0),
nu!=0.                                                (18)
```

In particular, restriction of (18) to `K_5=Kz` is zero.

### Theorem 3.1 (generic silent-`T_0` branches are impossible)

Equations (16)--(18) and the two legal selectors `F_45=G_35=0` have no
common physical-edge solution when `alpha!=0` or on the branch
`alpha=0, ab!=0`.  When `alpha=0`, the case in which exactly one of `a,b`
is nonzero is impossible.
Thus every possible survivor satisfies `alpha=a=b=0`.

### Proof: `alpha!=0` and `ab!=0`

Define

```text
C=alpha B-(u_3v_4+v_3u_4).
```

Eliminating `L_3,L_4` gives

```text
aC-2b u_3u_4=alpha lambda X,
bC-2a v_3v_4=alpha mu Y.                             (19)
```

At least one of `a,b` is nonzero.  First suppose both are nonzero and put

```text
p_i=b u_i,                      q_i=a v_i.
```

Subtracting the two multiples of (19) gives

```text
q_3q_4-p_3p_4
 =(b alpha lambda/2)X-(a alpha mu/2)Y.               (20)
```

The right side has matrix rank two.  Hence `p_i,q_i` are bases of `K_i^*`
for `i=3,4`, and

```text
L_i=-(p_i+q_i)/alpha!=0.                             (21)
```

Use the remaining central coordinates

```text
r=[e_(1,1)e_(2,0)]A,       s=[e_(1,0)e_(2,2)]A,
t=[e_(1,0)e_(2,0)]A,
delta_5=d z,               beta_5=c z.               (22)
```

Solving the `e_(1,1)e_(2,0)` components of the two `E` equations for
`delta_i` and substituting into the zero `delta` attachment gives

```text
M_delta+d alpha lambda X=0,                          (23)
M_delta=(-2r/alpha+4d/b)p_3p_4
       +(-2r/alpha+2d/b)(p_3q_4+q_3p_4)
       -(2r/alpha)q_3q_4.
```

The coefficient matrix of `M_delta` in the two bases `p_i,q_i` has
determinant

```text
-4(d/b)^2.                                           (24)
```

If `d!=0`, (23) says that this rank-two tensor equals the rank-one tensor
`-d alpha lambda X`, impossible.  Thus `d=0`, after which (23) is a
nonzero multiple of `(p_3+q_3)(p_4+q_4)` unless `r=0`.  Hence `r=0` and all
`delta_i` vanish.

The symmetric `e_(1,0)e_(2,2)` calculation gives

```text
M_beta+c alpha mu Y=0,                               (25)
M_beta=-(2s/alpha)p_3p_4
       +(-2s/alpha+2c/a)(p_3q_4+q_3p_4)
       +(-2s/alpha+4c/a)q_3q_4,
det M_beta=-4(c/a)^2.
```

Therefore `c=s=0` and all `beta_i` vanish.  The `e_(1,0)e_(2,0)` parts of
(16) now give `t=0`.  Since `L_4,L_3` are nonzero, the `e_(0,0)e_(1,0)`
projection of `F_45` kills the full scalar
`U_00=[e_(0,0)e_(1,0)]W_01`, and the corresponding projection of `G_35`
kills `V_00=[e_(0,0)e_(2,0)]W_02`.  With `U_00=V_00=t=0`, the pure
coefficient in (18) vanishes, a contradiction.

### Proof: `alpha!=0` and an endpoint

Suppose `a!=0,b=0`; the other endpoint is obtained by exchanging the two
central labels and target colours.  Equations (16)--(17) give

```text
L_i=-(a/alpha)v_i,
-(2a/alpha)v_3v_4=mu Y.                              (26)
```

Thus `v_i` and `L_i` are nonzero multiples of `y_i`.  Put
`D=u_3L_4+L_3u_4`.  The delta equations and its zero attachment reduce to

```text
-2rL_3L_4-2dD+d lambda X=0.                          (27)
```

The first two terms lie in the tangent space to the rank-one tensor `Y`
and have zero `x_3x_4` coefficient.  Hence `d=0`, and then `r=0`.  All
delta coordinates vanish.

The beta `E` equations first give `c=sa/alpha`.  Its zero attachment has
`(c lambda/a)X` plus a tensor in the same tangent space, so `c=s=0`.  The
remaining separated syzygy is

```text
beta_3=kL_3,                     beta_4=-kL_4         (28)
```

for some scalar `k`.  The `e_(1,0)e_(2,0)` coordinates of the underlying
`E` equations give `t=0`, while the
`e_(0,0)e_(2,0)` projection of `G_35` gives `V_00=0`.

Let

```text
C_5|_(e_(0,0),K_5)=c_0 z,
V_02=[e_(0,0)e_(2,2)]W_02.
```

The `e_(0,0)e_(1,0)` projection of `F_45` is

```text
(U_00-kc_0)L_4=0.                                   (29)
```

If `U_00=0`, then `U_00=V_00=t=0` already makes the pure coefficient of
(18) zero.  Otherwise (29) gives `c_0!=0`.  The
`e_(0,0)e_(2,2)` projection of `G_35` is

```text
V_02 L_3+c_0v_3=0,
```

and (26) therefore gives

```text
V_02=alpha c_0/a.                                   (30)
```

Finally restrict (18) to `K_5` and take its
`e_(0,0)e_(1,1)e_(2,2)z` coefficient.  The `W_01W_25` term is zero because
`v_5=bz=0`; the other two matching terms give

```text
aV_02+alpha c_0=2alpha c_0!=0,                       (31)
```

although the restricted right side of (18) is zero.  This is the required
characteristic-zero contradiction.  For the other endpoint `a=0,b!=0`,
the symmetric calculation gives `U_00=t=0`.  If `V_00=0`, the full pure
coefficient already vanishes; otherwise the `G_35` zero-central projection
forces `c_0!=0`, the `e_(0,0)e_(1,1)` projection of `F_45` gives
`U_01=alpha c_0/b`, and the same restricted full-deck coordinate is

```text
bU_01+alpha c_0=2alpha c_0!=0.
```

Thus the stated symmetry preserves the legally available selector pair.

### Proof: `alpha=0` and `ab!=0`

If exactly one of `a,b` is nonzero, (16) kills the corresponding active
coordinates and one attachment in (17) vanishes.  Suppose now `ab!=0`.
Equation (16) gives

```text
v_i=-(b/a)u_i.
```

Put

```text
D=u_3L_4+L_3u_4,
E=aB.
```

The attachments are exactly

```text
D=(lambda X-(a/b)mu Y)/2,
E=(lambda X+(a/b)mu Y)/2.                            (32)
```

Thus `D` has rank two and `L_3,L_4` are nonzero.  The delta equations and
zero attachment give

```text
2rb L_3L_4=ad mu Y.                                  (33)
```

If exactly one of `r,d` is zero, so is the other.  If both are nonzero,
then `L_3L_4` is proportional to `Y`; but `D=u_3L_4+L_3u_4` lies in the
tangent space at `Y` and cannot have the nonzero `X` coefficient displayed
in (32).  Hence `r=d=0` and all delta coordinates vanish.  Symmetrically,

```text
2sa L_3L_4=bc lambda X                              (34)
```

forces `s=c=0` and all beta coordinates to vanish, since the nonzero `Y`
coefficient of `D` is not tangent at `X`.  The underlying `E` equations now
give `t=0`,
and the two selectors kill `U_00,V_00` because `L_4,L_3` are nonzero.
Again the pure coefficient in (18) vanishes.  If `a=b=0`, neither
attachment vanishes: the two attachment equations retain the same
`L_3,L_4` factors.  That branch is treated next. `square`

The proof never evaluates an off-kernel coefficient of `W_15` or `W_25`.
In the two generic branches it kills their full central multipliers.  In
the endpoint branch it instead uses a coefficient of the already-forced
full physical deck restricted to the one-dimensional `T_0` kernel.  The
remaining `alpha=a=b=0` branch is different: its transverse coefficient is
not multiplied by a forced-zero central scalar.

### Theorem 3.2 (exact transverse full-deck control)

The branch `alpha=a=b=0` is compatible with every deck equation used on the
one-silent-`T_0` branch in Section 3.  In particular it is compatible with
the actual pure full deck (18), not merely with its kernel restriction.

### Proof

Choose full covectors extending `x_3,y_3,x_4,y_4,z`, with
`e_(5,0)|_(K_5)=0`, and set the following physical edges:

```text
W_01=e_(0,0)e_(1,0),          W_02=0,
W_03=W_04=0,                  W_05=e_(0,0)z,
W_12=0,
W_13=e_(1,1)x_3+e_(1,0)y_3,
W_14=-e_(1,0)x_4,             W_15=0,
W_23=0,                       W_24=e_(2,2)y_4,
W_25=e_(2,0)e_(5,0),
W_34=0,                       W_35=y_3z,
W_45=x_4z.                                             (35)
```

All omitted edges in (35) are explicitly zero.  The transverse edge
`W_25` restricts to zero on `K_5`.  Hence, in the notation of (15)--(17),

```text
A=B=Y_5=Z_5=0,
L_3=y_3,                  L_4=x_4,
u_3=x_3,                 u_4=0,
v_3=0,                   v_4=y_4,
alpha=a=b=0.                                          (36)
```

Take `P_3=e_(3,0)`, `Q_4=e_(4,0)` and
`Q_3=P_4=P_5=Q_5=0` for the outside `P_0,Q_0` row coefficients.  Thus the
whole `T_0` row is silent, not merely its `e_(5,0)` coordinate.  Direct
hafnian expansion gives

```text
E_45=H_(1245)|_(K_4 tensor K_5)=0,
E_35=H_(1235)|_(K_3 tensor K_5)=0,

F_45=H_(0145)|_(K_4 tensor K_5)
    =W_01W_45+W_05W_14=0,
G_35=H_(0235)|_(K_3 tensor K_5)=0.                  (37)
```

The pair attachments and the remaining triangle deck are

```text
H_(1345)|_(K_3 tensor K_4 tensor K_5)
 =e_(1,1)x_3x_4z,
H_(2345)|_(K_3 tensor K_4 tensor K_5)
 =e_(2,2)y_3y_4z,
H_(0345)|_(K_3 tensor K_4 tensor K_5)=0.             (38)
```

In the first line, the two `e_(1,0)y_3x_4z` terms from
`W_13W_45` and `W_14W_35` cancel.  Finally the unrestricted deck is

```text
H_(0125)=W_01W_25+W_02W_15+W_05W_12
 =e_(0,0)e_(1,0)e_(2,0)e_(5,0).                    (39)
```

Thus one common physical edge array realizes the two `E` selectors, both
mixed `F/G` selectors, both pure attachments, the zero triangle deck, and
the required nonzero pure full deck.  It is not a complete six-label GHZ
source: the endpoint maps and every remaining open-set coefficient have
not been supplied.  It proves only that the equations used here do not
exclude (S). `square`

### Corollary 3.3 (exact Family-A `r=1` localization)

Every hypothetical Family-A `r=1` source has the unique `T_0` port
selector-silent and satisfies `alpha=a=b=0` after relabelling.  This locus
is nonempty at the common-physical-deck interface by Theorem 3.2.  A further
exclusion must either expose a legal coefficient evaluated at the
transverse vector `e_(5,0)` or prove a source-integrability identity that
transports the kernel restrictions of `W_25` to that transverse value.

## 4. Exact residual and new boundary

No typed profile is removed:

```text
98,355 / 81  ->  98,355 / 81.                       (40)
```

The surviving single-binary keys remain

```text
Family A, r=1:                         1,080 / 1 key,
Family A, r=2:                         1,080 / 1 key,
Family A, r=3:                           360 / 1 key,
Family B, r=3:                            60 / 1 key,
total:                                 2,580 / 4 keys. (41)
```

The exact current boundary is

```text
Family A r=0:                                      EMPTY;
Family A r=1 all-active / silent-R / generic
  silent-T cells:                                  EMPTY;
Family A r=1 alpha=a=b=0 transverse cell:            OPEN;
Family A r=2,3:                                      OPEN;
Family B r=0,1,2:                                  EMPTY;
Family B r=3 all-T_0 parent:                         OPEN;
all other five-/six-deficient branches:              OPEN;
global Krenn--Gu conjecture:                   UNRESOLVED. (42)
```

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_single_binary_activity_localization_and_transverse_full_deck_sharpness.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_six_deficient_one_t0_single_binary_activity_localization_and_transverse_full_deck_sharpness.py
```

The primary verifier independently rebuilds the `GLS70` taxonomy and the
unchanged `GLS71` residual, checks the Family-A `r=1` key size, evaluates the
two all-active determinant matrices, replays the silent-`T_0` projection
matrices and their determinants, and checks exact representative identities
in the excluded `alpha` branches.  It also constructs (35) as full edge
tensors and evaluates every deck in (37)--(39).

The independent audit uses integer support masks, modular tensor algebra,
and a separate determinant/rank implementation.  It does not import the
primary verifier.  The same-source derivation of the selectors, the
alternating argument, the activity fork, the tangent-space exclusions, and
the transfer of the silent-`R_0` written proof remain written mathematics.
The programs certify that the surviving transverse control is one common
edge array, but do not promote it to a complete source or a graph witness.
Neither script proves a global source theorem or the Krenn--Gu conjecture.
