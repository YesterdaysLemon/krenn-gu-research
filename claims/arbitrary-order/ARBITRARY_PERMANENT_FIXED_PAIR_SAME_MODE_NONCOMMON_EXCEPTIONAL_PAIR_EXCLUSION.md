# Arbitrary permanent fixed-pair same-mode noncommon exceptional-pair exclusion

## Status

This note proves an exact characteristic-zero exclusion inside the
simultaneous-low residual for the fixed equality-five pair.  Suppose one
remaining local plane has rank two under both projection families.  If the
two kernel lines in that plane are both different from the common line

```text
N=K(x_2+x_3),
```

then the exact `Delta_3` target equations are inconsistent.  Thus a
same-mode cross-family low can occur only if at least one of its two kernel
lines is `N`.

The proof never inserts two vectors from one local plane into two tensor
slots.  Instead it contracts once in the shared mode, studies the kernel of
the resulting three-mode residual-covector map, and uses the rank-one
diagonal target slices.  Two line pairs die by a dimension count.  The other
two first collapse to exact codimension-two local normal forms and then die
because a two-active-colour argument leaves only one possible supplier of
the common factor `x_4x_5`.

The cases `N` plus a non-`N` line and `N` paired with itself remain open in
this note.  The theorem does not exclude all simultaneous-low incidences and
does not prove unrestricted permanent nonrestriction.  The global
Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Fixed pair, exceptional lines, and target slices

Let `K` be a field of characteristic zero and split

```text
K^6=R direct-sum A,
R=span{x_0,x_1,x_2,x_3},       A=span{x_4,x_5}.          (1)
```

For the fixed equality-five pair, write the five complementary quartics as

```text
star(j)=x_4x_5 g_j,                  j=m_1,m_2,d_0,d_1,d_2,

g_(m_1)=x_1(x_3-x_2-x_0),
g_(m_2)=x_0(x_3-x_2-x_1),
g_(d_0)=(x_1+x_2)(x_3-x_0),
g_(d_1)=(x_0+x_2)(x_3-x_1),
g_(d_2)=-2x_0x_1.                                      (2)
```

Let ordered independent triples

```text
(y_(r,0),y_(r,1),y_(r,2)),                  r=2,3,4,5,
```

span the local planes `L_r`.  Assume the exact target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

The two projection kernels have exceptional lines

```text
Phi_1: N=x_2+x_3,  A_0=x_0+x_3,  C_0=x_0-x_2,
Phi_2: N=x_2+x_3,  A_1=x_1+x_3,  C_1=x_1-x_2.          (4)
```

The predecessor kernel-support theorem gives the forced missing local
colours

```text
A_0 misses 0,       C_0 misses 1,
A_1 misses 1,       C_1 misses 0.                       (5)
```

This note treats a single mode `t` containing a line from each of the two
noncommon sets in (4).

## 2. The legal single-contraction kernel

For a square-free quadratic `g_j` on `R`, let

```text
B_j:R -> R^*
```

be its polarized contraction map.  Put

```text
h_2 =( 1,-1,-1, 1),       h_2'=(-1, 1,-1, 1),
w_0 =( 1,-1,-1,-1),       w_1 =( 1,-1, 1, 1).          (6)
```

Direct contraction of (2) gives

```text
line   B_(m_1)       B_(m_2)       B_(d_0) B_(d_1) B_(d_2)

A_0       0             h_2             0      w_1    -2x_1
C_0       0             h_2            w_0      0     -2x_1
A_1      h_2'            0            -w_0      0     -2x_0
C_1      h_2'            0              0     -w_1    -2x_0. (7)
```

Fix `p in {A_0,C_0}` and `q in {A_1,C_1}` inside the same `L_t`, using the
displayed generators.  They are independent.  Write their local coordinate
columns as

```text
p=sum_c alpha_c y_(t,c),       q=sum_c beta_c y_(t,c),
r_c=(alpha_c,beta_c),          S=span{p,q}.             (8)
```

Let the other three modes be `s,u,v`.  For `ell in R^*`, define the
three-mode tensor

```text
Theta(ell)(z_s,z_u,z_v)
 =[x_0x_1x_2x_3x_4x_5]
   (x_4x_5 ell) z_s z_u z_v,
Q=ker Theta.                                                (9)
```

This is a single contraction in mode `t`; no vector from `L_t` is ever used
in a second slot.  Contracting (3) once gives, for every `z in S`,

```text
Theta(B_(m_1)z)=Theta(B_(m_2)z)=0,
Theta(B_(d_c)z)=lambda_c f_c(z) tau_c,                  (10)
```

where `f_c` is the `c`-th local coordinate covector on `L_t` and
`tau_c=e_c^* tensor e_c^* tensor e_c^*` on the other three modes.

Let

```text
I={c:r_c!=0}.
```

The coordinate map is injective on the two-space `S`, so the three rows
`r_c` span `S^*` and `|I|>=2`.  The tensors `tau_c`, `c in I`, are
independent and occur nontrivially in (10).  Therefore

```text
rank Theta>=|I|,                  dim Q<=4-|I|.          (11)
```

On the other hand, (7) and the mixed equations give

```text
U:=span{h_2,h_2'} subset Q,              dim U=2.       (12)
```

Equations (11)--(12) exclude `|I|=3`.  Hence exactly one row `r_e` is zero
and

```text
|I|=2,                 Q=U.                              (13)
```

For later use, if `r_c!=0`, the vector

```text
z_c=beta_c p-alpha_c q
```

lies in `ker(f_c|S)`, so (10) implies

```text
B_(d_c)z_c in U.                                        (14)
```

If `r_c=0`, the whole space `B_(d_c)S` lies in `U`.

The elementary coordinate facts used below are

```text
w_0,w_1,x_0,x_1 notin U,
U intersect span{x_0,x_1}=K(x_0-x_1).                  (15)
```

## 3. Two immediate exclusions

### Proposition 1

The same-mode pairs `(A_0,A_1)` and `(C_0,C_1)` are impossible.

### Proof

For `(A_0,A_1)`, (5) gives `alpha_0=beta_1=0`.  Let `e` be the unique zero
row from (13).

```text
e=0:  B_(d_0)q=-w_0 notin U;
e=1:  B_(d_1)p= w_1 notin U;
e=2:  B_(d_2)p=-2x_1 notin U.
```

Each line contradicts the zero-row consequence following (14).

For `(C_0,C_1)`, one has `alpha_1=beta_0=0`, and the three cases give

```text
e=0:  B_(d_0)p= w_0 notin U;
e=1:  B_(d_1)q=-w_1 notin U;
e=2:  B_(d_2)p=-2x_1 notin U.
```

This proves both exclusions.

## 4. The two apparent normal forms

The remaining line pairs share their forced missing colour.  They are not
excluded by the first dimension count alone.

### Lemma 2 (same-missing normal forms)

For `(p,q)=(A_0,C_1)`, equations (5), (13), and (14) force

```text
alpha=(0,a,b),       beta=(0,-a,b),       ab!=0.        (16)
```

For `(p,q)=(C_0,A_1)`, they force

```text
alpha=(a,0,b),       beta=(-a,0,b),       ab!=0.        (17)
```

### Proof

In the first case, `r_0=0` is forced by (5), so it is the unique zero row.
Write

```text
alpha=(0,a,b),                 beta=(0,c,d).
```

The two columns have rank two, so `ad-bc!=0`.  From (7) and (14),

```text
B_(d_1)(c p-a q)=(a+c)w_1 in U,
B_(d_2)(d p-b q)=2b x_0-2d x_1 in U.                   (18)
```

Equations (15) and (18) give `c=-a` and `d=b`.  Then
`ad-bc=2ab`, which is nonzero in characteristic zero.  This is (16).

The second case is direct rather than an appeal to an unstated symmetry.
Now `r_1=0`, write `alpha=(a,0,b)`, `beta=(c,0,d)`, and use

```text
B_(d_0)(c p-a q)=(a+c)w_0 in U,
B_(d_2)(d p-b q)=2b x_0-2d x_1 in U.                   (19)
```

Again (15) gives `c=-a`, `d=b`, and the determinant is `2ab!=0`.  This is
(17).

In (16), solving (8) gives

```text
y_(t,1)=(p-q)/(2a) in R,       y_(t,2)=(p+q)/(2b) in R. (20)
```

Thus the `A`-projection of `L_t` is supported only at local colour zero and
has rank at most one.  In (17), the analogous statement is

```text
y_(t,0)=(p-q)/(2a) in R,       y_(t,2)=(p+q)/(2b) in R, (21)
```

so the `A`-projection is supported only at local colour one.

## 5. Two active colours force the final contradiction

On `A`, put

```text
J((r_4,r_5),(s_4,s_5))=r_4s_5+r_5s_4.                 (22)
```

For three vectors in `R direct-sum A`, define the `R`-valued symmetric
tensor

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).             (23)
```

By construction,

```text
Theta(ell)(y,z,w)=ell(C(y,z,w)).                        (24)
```

### Lemma 3 (two-active-colour vanishing)

Suppose three independent local triples in `R direct-sum A` satisfy

```text
C(y_(s,i),y_(u,j),y_(v,l))=0
```

unless `i=j=l` is one of two colours `c,d`, and both corresponding diagonal
values are nonzero.  Then every `A`-projection at the third colour `e`
vanishes.

### Proof

For two distinct modes and two distinct colours `i!=j`, the map

```text
w |-> C(y_(s,i),y_(u,j),w):R direct-sum A -> R
```

kills the three-dimensional third local plane, so its rank is at most
three.  On the four-dimensional `R`-summand it is scalar multiplication by

```text
J(a(y_(s,i)),a(y_(u,j))).
```

The scalar must therefore be zero.  Permuting the modes proves
cross-colour orthogonality between every two distinct modes.

A nonzero diagonal `C`-value contains a nonzero same-colour `J`-pairing, so
both `c` and `d` are active.  The following two-dimensional observation
finishes the proof.  If one mode has two independent `A`-columns, every
third-colour column at either other mode is orthogonal to both and hence
zero.  The two active colours then give two distinct orthogonal-complement
lines for columns at the first mode, forcing its third-colour column to be
zero as well.  If every mode has `A`-rank at most one, an active pairing at
one colour forces both endpoint modes to support only that colour; any
second active pairing shares a mode and would force a different support
there, a contradiction.  Thus that rank-at-most-one alternative cannot
have two active colours.  All third-colour `A`-columns vanish.

### Theorem 4 (same-mode noncommon exceptional-pair exclusion)

No exact target (3) has, in one local plane, one line from
`{A_0,C_0}` and one line from `{A_1,C_1}`.

### Proof

Proposition 1 excludes `(A_0,A_1)` and `(C_0,C_1)`.  Consider
`(A_0,C_1)`.  Equations (11)--(13) say that the image of `Theta` is exactly

```text
span{tau_1,tau_2}.                                      (25)
```

The normal form (16) and (10) show that both diagonal tensors in (25)
occur nontrivially.  By (24), the full `R`-valued tensor `C` on the other
three local triples is therefore zero off the `111` and `222` cells and is
nonzero on both of those cells.  Lemma 3 forces

```text
a(y_(s,0))=a(y_(u,0))=a(y_(v,0))=0.                    (26)
```

Equation (20) says that, in mode `t`, only the colour-zero vector can have
a nonzero `A`-part.  Hence among the four colour-zero vectors at most one
has a nonzero `A`-part.  The quartic

```text
star(d_0)=x_4x_5 g_(d_0)
```

requires two distinct input vectors to supply `x_4` and `x_5`; one linear
factor cannot supply both.  Its all-colour-zero coefficient is therefore
zero, contradicting `lambda_0!=0` in (3).

For `(C_0,A_1)`, equations (17), (21), and the same legal argument give
`im Theta=span{tau_0,tau_2}` with both diagonal cells nonzero.  Lemma 3
forces all three other colour-one `A`-projections to vanish.  Only the
shared mode could supply `x_4` or `x_5` in the pure `d_1` coefficient, so
that coefficient is zero, contradicting `lambda_1!=0`.  All four pairs are
excluded.

## 6. A corrected projective-scaling pitfall

The local columns in (8) and the ambient line generators must be scaled
together.  Replacing `p` by `s p` replaces both `alpha` and every
contraction `B_jp` by the same factor `s`.  Normalizing `alpha` while
holding the displayed ambient generator `p` fixed is not a legal
projectivization.  That incorrect normalization spuriously removes the
two normal forms (16)--(17).  The proof above keeps the generators fixed,
allows all coefficients `a,b,c,d`, derives the normal forms, and only then
excludes them by Lemma 3.

## 7. Exact scope and replay

```text
same mode, A_0 x A_1:                                  EXCLUDED;
same mode, C_0 x C_1:                                  EXCLUDED;
same mode, A_0 x C_1:             NORMALIZED THEN EXCLUDED;
same mode, C_0 x A_1:             NORMALIZED THEN EXCLUDED;
same mode, N plus a non-N line:                         OPEN HERE;
same mode, N paired with itself:                        OPEN HERE;
distinct-mode exceptional incidences:              NOT RECLASSIFIED;
unrestricted P_6 -> Delta_3:                            UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.       (27)
```

Replay the exact coordinate checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_same_mode_noncommon_exceptional_pair_exclusion.py
```

The primary verifier derives the contraction table from the factorized
quartics with exact symbolic arithmetic, checks every dimension-count case,
derives both normal forms, and replays the two-active-colour rank gate.  The
no-import audit imports neither the primary verifier nor SymPy: it rebuilds
the square-free quadratics as edge dictionaries, uses exact rational row
reduction, independently checks the four line pairs and scaling covariance,
and exhausts the two-dimensional orthogonality lemma over two odd finite
fields.  The scripts replay identities and finite algebra.  The written
characteristic-zero argument proves the theorem.
