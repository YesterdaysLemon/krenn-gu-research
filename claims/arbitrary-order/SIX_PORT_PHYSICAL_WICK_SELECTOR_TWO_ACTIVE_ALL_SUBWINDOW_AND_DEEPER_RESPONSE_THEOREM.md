# Six-port physical Wick selector, two-active all-subwindow closure, and deeper response

## Status

**Exact characteristic-zero conditional supply and detector theorem.**  Fix one
physical residual pair `Q`, one scalar coefficient chart on six port modes,
and the literal residual-relative response of the same graph.  On the `h=0`
branch its degree-two and degree-four layers obey

```text
z_P=K_P,
z_S=sum_(P subset S, |P|=2) K_P m_(S-P).             (1)
```

After complementing every four-set row, (1) is a `15 x 15` scalar Wick map.
Its determinant on the physical rank-two locus is computed below.  A nonzero
minor gives every pair coefficient by at most fifteen four-port rows.

The determinant condition is sufficient but not necessary.  On the fully
two-active diagonal physical locus, coefficientwise polarization supplies
**every coefficient of every direct pair block** from the fifteen `K4`
subwindows of the same six ports, including the singular `5+1` words and the
inactive colour.  If the attached four-port tensors are target-diagonal, the
direct layer is forced into

```text
B^0=c K^0,                   B^1=-c K^1.             (2)
```

Any nonzero pure four-port coefficient then forces an explicit nonzero mixed
`2+4` coefficient at depth six.  Consequently the fully two-active `h=0`
branch is contradictory if the fifteen `z_2` tensors, all fifteen `z_4` tensors,
and that `z_6` tensor have already been attached by legal constant same-`Q`
selectors and one pure `z_4` coefficient is nonzero.

The attachment hypothesis is load-bearing.  The inverse coefficients may
depend on the fixed graph's `K`, but they are constants only after that graph
chart is fixed.  Pointwise or function-field inversion cannot create the
upstream target attachment.  The theorem does not exclude a general
hypothetical witness, does not force the nonzero-pure hypothesis, and gives no
weighted permanent restriction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.

The bare Kneser matrix and its uniform spectrum already belong to the
[`residual-hafnian Hessian theorem`](RESIDUAL_HAFNIAN_HESSIAN_KNESER_ETALE_AND_JET_INTEGRABILITY_THEOREM.md).
The new content here is the physical rank-two discriminant, the singular-word
selectors, the full tensor polarization cover, and the target-attached
depth-six consequence.

## 1. Scalar six-port Wick map

Work over a field `K` of characteristic zero.  Let `U` be a six-set and
`E=binom(U,2)`.  Fix one scalar coefficient at every port.  For a pair array
`m=(m_P)`, define

```text
(mu_K m)_S=sum_(P subset S, |P|=2) K_(S-P)m_P,
                    S in binom(U,4).                 (3)
```

Index a row by the complementary pair `e=U-S` and a column by `f`.  The
resulting symmetric matrix is

```text
D_K(e,f)=K_(U-(e union f))     if e intersect f=empty,
          0                    otherwise.            (4)
```

Thus `D_K` is the `q=6` residual-hafnian Hessian.  The matrix is literally
`15 x 15` only after the scalar coefficient word has been fixed.  The full
ternary map is tensor-valued, and one scalar minor does not recover it.

### Theorem 1 (physical rank-two discriminant)

Suppose

```text
K_ij=a_i b_j+b_i a_j.                                (5)
```

Put

```text
A=product_i a_i,
s_k=sum_(I subset U, |I|=k)
      product_(i in I)b_i product_(j notin I)a_j.    (6)
```

In the ordering (4),

```text
det D_K=-9216(
  12 A^2 s_5^3
  -4 A s_1 s_4 s_5^2
  +s_1^2 s_3 s_5^2
  -4 s_1^2 s_2 s_5 s_6
  +12 s_1^3 s_6^2).                                 (7)
```

The formula is polynomial and remains valid when some `a_i` vanish.  On the
dense chart `a_i!=0`, set `t_i=b_i/a_i` and let `e_k` be the elementary
symmetric functions of the `t_i`.  Removing the vertex scalings turns (7)
into

```text
det D(t)=-9216(
  12 e_5^3-4 e_1 e_4 e_5^2+e_1^2 e_3 e_5^2
  -4 e_1^2 e_2 e_5 e_6+12 e_1^3 e_6^2).             (8)
```

Whenever (7) is nonzero, every `m_P` is a constant linear combination of the
fifteen rows in (3).  Each selector therefore has support at most fifteen.

### Proof

It suffices first to prove (8).  Let `R` be the `6 x 15` unsigned
vertex--edge incidence matrix, let `one` be the edge all-ones vector, and put

```text
T=sum_i t_i,                 delta_ij=T-2(t_i+t_j),
Delta=diag(delta_ij),
P_(ij,i)=t_j,                P_(ij,j)=t_i.            (9)
```

All other entries of `P` are zero.  Define

```text
L=Delta+P R,
J=I-(1/2)R^T R+(1/3)one one^T.                       (10)
```

For a fixed column edge `f`, direct subset counting gives

```text
sum_g D_(g,f)=3(T-t_f),
sum_(g contains u) D_(g,f)=
  0                         if u in f,
  2(T-t_f-t_u)             if u notin f.             (11)
```

Substitution in (10) gives `J D=L`.  On

```text
K^E=one direct-sum Std_5 direct-sum ker R,            (12)
```

the eigenvalues of `R^T R` are `10,4,0`, so those of `J` are `1,-1,1`.
Hence `J^2=I`, `det J=-1`, `D=J L`, and `det D=-det L`.

Away from the `delta` walls, the determinant lemma reduces this to

```text
det D=-(product_e delta_e) det(I_6+R Delta^(-1)P),   (13)
```

where

```text
(I_6+R Delta^(-1)P)_(i,i)
 =1+sum_(j!=i)t_j/delta_ij,
(I_6+R Delta^(-1)P)_(i,j)=t_i/delta_ij.              (14)
```

Expanding the fixed `6 x 6` determinant, clearing its denominators, and
collecting in the elementary-symmetric basis gives (8).  Both sides are
polynomials, so the identity extends across every wall.  For the general
chart put `a_e=product_(i in e)a_i`.  On `a_i!=0`, entrywise

```text
D_K=A diag(a_e^(-1)) D(t) diag(a_e^(-1)),            (14a)
```

because the complementary pair contributes
`a_k a_l(t_k+t_l)=A(a_e a_f)^(-1)D(t)_(e,f)`.  Since
`product_(e in E)a_e=A^5` and `s_k=A e_k(t)`, determinants turn (8) into
(7).  Polynomiality extends it across every `a_i=0` coordinate hyperplane.

For a finite exact certificate of that collection step, write `P(t)=det D(t)`.
It is symmetric and homogeneous of degree fifteen.  Fix a vertex `i`, order
the five incident edges first, and order the ten nonincident edges last.  The
matrix has block form

```text
D=[[0,C],[C^T,B+t_i H]].                            (14b)
```

The first five determinant rows must consume five of the last ten columns,
so at most five remaining bottom-right entries can contribute `t_i`.  Hence
`deg_(t_i) P<=5` for every `i`.  The right side of (8) has the same bounds.
The space of symmetric homogeneous degree-fifteen polynomials in six
variables with every individual degree at most five has the `32` monomial-
symmetric basis elements indexed by partitions of `15` with largest part at
most `5` and length at most `6`.  The primary verifier evaluates this basis
at `32` displayed deterministic integer points.  Its evaluation determinant
is `188237 mod 1000003`, hence is nonzero over the integers, and exact integer
determinants agree with (8) at every point.  Unisolvence proves the polynomial
identity over `Q`, and therefore over every characteristic-zero field.  This
is an identity certificate, not sampling.

If the determinant is nonzero, ordinary adjugate inversion of (3) gives one
row functional per `m_P`.  Once the graph and its `K` values are fixed, these
are field constants and use no observed target shape.  `square`

At `t_i=1`, `D=2 A_(KG(6,2))`, with eigenvalues `12,-6,2` of multiplicities
`1,5,9`.  Thus `det D=-2^16 3^6`, so the open branch is nonempty.

## 2. Exact two-shore scalar boundary

Assume a coefficient word partitions the ports into shores `A,B`, and

```text
K_ij=alpha x_i x_j       within A,
K_ij=beta y_i y_j        within B,
K_ij=0                   across A,B,                 (15)
```

with all displayed scalars nonzero.  Diagonal row and column scaling removes
the vertex factors.  Direct exact elimination gives the exhaustive six-port
table

| shore count | rank | determinant |
|---|---:|---:|
| `6+0` | 15 | `-1458 alpha^15` |
| `5+1` | 10 | `0` |
| `4+2` | 15 | `54 alpha^10 beta^5` |
| `3+3` | 10 | `0` |

The rows may be reordered, changing the displayed determinant sign but not
its magnitude or the conclusions.

### Theorem 2 (`5+1` selectors and `3+3` kernel)

In a `5+1` word let `b` be the singleton and `A` the five-shore.  After
removing the vertex factors, put

```text
y_T=z_({b} union T)/alpha,       T in binom(A,3).     (16)
```

Then every cross-shore coefficient is selected by ten rows:

```text
m_(b,i)=(1/6)(
  sum_(T contains i)y_T-sum_(T not contains i)y_T).  (17)
```

The remaining kernel is the five-dimensional kernel of the `5 x 10`
four-set/pair inclusion map on the five-shore.

For a `3+3` word, write the cross-pair coefficients as a `3 x 3` matrix `X`.
Then

```text
ker mu_K=
 {X: every row sum and column sum is zero}
 direct-sum K*(alpha sum_(e in binom(A,2))e_e
               -beta sum_(e in binom(B,2))e_e).     (18)
```

It has dimension five, and every pair coordinate varies in the kernel.
Thus an isolated `3+3` word has no individual pair selector.

### Proof

For `5+1`, the ten singleton-containing rows are

```text
y_T=sum_(i in T)m_(b,i).                             (19)
```

In the containing-minus-not-containing sum, `m_(b,i)` has net multiplicity
six and every other coordinate has net multiplicity zero, proving (17).
The five rows avoiding `b` form the `W_(4,2)(5)` inclusion map.  A relation
among its rows, indexed by the omitted vertex, obeys
`sum_(r notin {i,j}) alpha_r=0` for every edge `ij`; hence all coefficients
agree and `3 alpha_r=0`.  Its rank is five and its kernel has dimension five.

For `3+3`, rows of type `3A+1B` give the column sums of `X`, and rows of type
`1A+3B` give its row sums.  A `2A+2B` row gives the weighted relation
`beta m_AA+alpha m_BB`.  This is exactly (18).  Rectangle cycles span the
four-dimensional zero-row/column-sum space, and the displayed internal
direction is independent.  `square`

The `5+1` case already shows why vanishing square minors are not an exhaustive
obstruction: in a `6+1` union every six-window containing a fixed cross pair
is singular, but (17) still selects that pair.

### Corollary 2.1 (overlapping common-row closure)

On a two-shore scalar union of at least seven ports satisfying (15), the
aggregate map from all pair coefficients to all four-port rows is injective.
Every pair coordinate has a selector supported on at most fifteen rows from
one six-subset.

For a within-shore pair, use a `6+0` subset if the other shore has size at
most one, a `2+4` subset if the other shore has at least four ports, and a
`4+2` subset in the remaining cases.  For a cross pair, use (17) if either
shore has at least five ports.  Otherwise the shore counts are `4+3`, `3+4`,
or `4+4`, and a `4+2` subset containing the pair exists.  The table and
Theorem 2 give the claimed selector in every case.  Thus the isolated `3+3`
kernel never survives the overlapping common-row collection.

## 3. Full two-active tensor polarization

Return to ternary port spaces.  Assume that in one common physical gauge the
`h=0` pair channel has exactly two active colours and

```text
K_ij(0,0)=alpha x_i x_j,
K_ij(1,1)=beta y_i y_j,                              (20)
```

for all distinct ports, with `alpha,beta,x_i,y_i` nonzero.  Every other
coefficient of every `K_ij` is zero.  Suppose all fifteen tensors `z_S`,
`|S|=4`, are available from the same physical response.

The line form is a natural exact incidence stratum, not an automatic
consequence of pair diagonality alone.  To see one sufficient entry condition,
write the residual incidence row of colour `c` at port `u` as
`v_(u,c)=(a_(u,c),b_(u,c))` in the nondegenerate residual two-space with
bilinear form `J`.  Suppose all cross-colour pair coefficients vanish.  If
one port `p` has independent `v_(p,0),v_(p,1)` and two further ports `q,r`
have both their `0` and `1` rows nonzero, then the cross equations force two
orthogonal nonisotropic lines `L_0,L_1` with

```text
v_(u,0) in L_0,        v_(u,1) in L_1,
v_(u,2)=0                                             (20a)
```

at every port.  Indeed, rows of colour `1` away from `p` lie in
`v_(p,0)^perp`, and rows of colour `0` lie in `v_(p,1)^perp`.  The `q,r`
cross equation makes those two lines orthogonal, hence identifies them with
the spans at `p`; a third-colour row is orthogonal to both independent lines
and vanishes.  Nonzero scalar coordinates at all six ports then give (20).
Whether every relevant witness supplies these anchors and nonvanishing
coordinates remains open.

### Theorem 3 (six-port coefficientwise all-subwindow supply)

Every coefficient of every direct pair block `B_ij=m_ij` is a constant
linear combination of at most fifteen scalar coefficient rows of the
fifteen four-port tensors.

More precisely:

1. for a same-active-colour coefficient, choose the other four port colours
   so the global word has shore count `4+2` and invert (3);
2. for two different active colours, or one active and one inactive colour,
   make the other four ports the first colour and use the `5+1` selector
   (17);
3. for an inactive--inactive coefficient, colour two remaining ports `0` and
   two `1`; the row on the desired inactive pair plus the two colour-`0`
   ports has exactly one nonzero term,

   ```text
   z_(i,j,p,q)(2,2,0,0)=K_pq(0,0) B_ij(2,2).        (21)
   ```

If every `z_4` tensor is GHZ-diagonal, (17) and (21) show that all active
cross-colour and inactive coefficients of `B` vanish.  Thus `B` is diagonal
in the same two active colours.

### Proof

For each desired tensor coefficient, fix the complete six-port coefficient
word indicated above and apply (3).  In case 1 its `4+2` determinant is
nonzero by (15).  In case 2 the desired pair joins the singleton shore to the
five-shore and (17) applies.  In case 3 all terms of (1) vanish except the
one displayed in (21).  All divisions are by fixed nonzero graph
coefficients.  The support bounds are respectively fifteen, ten, and one.

For a target-diagonal `z_4`, every row used in cases 2 and 3 is mixed and
therefore zero.  This kills the claimed off-diagonal coefficients.  `square`

This theorem uses all fifteen `K4` subwindows of one six-port set.  It avoids
the fixed-word `3+3` kernel by choosing a different polarization word for
each desired coefficient; it does not claim that the `3+3` scalar matrix
became invertible.

## 4. The `h=0` depth-six detector

Keep (20), assume the `z_4` tensors are target-diagonal, and write

```text
b_e^c=B_e(c,c),             k_e^c=K_e(c,c).          (22)
```

### Theorem 4 (two-active all-subwindow/deeper-response closure)

There is one scalar `c in K` such that

```text
b_e^0=c k_e^0,              b_e^1=-c k_e^1          (23)
```

for every pair `e`.  For any disjoint two-set `e` and four-set `R` whose
ports are coloured `0^2 1^4`, the mixed depth-six coefficient is

```text
z_U(0_e^2,1_R^4)=-c^2 k_e^0 C(K_R^1),               (24)
C(K_R^1)=sum_(perfect matchings of R)
          product_(f in matching) k_f^1
        =3 beta^2 product_(i in R)y_i.               (25)
```

The pure four-port coefficients are

```text
z_R(0^4)= 2c C(K_R^0),
z_R(1^4)=-2c C(K_R^1).                               (26)
```

Hence a nonzero pure `z_4` coefficient implies `c!=0`, and then every
compatible coefficient (24) is nonzero.  If the `z_6` tensor is also legally
attached to a GHZ-diagonal target, this is a contradiction.

### Proof

By Theorem 3, `B` has only its two active diagonal coefficients.  For two
disjoint pairs `e,f`, the mixed `0^2 1^2` four-port coefficient is

```text
k_e^0 b_f^1+b_e^0 k_f^1=0.                           (27)
```

Divide by the nonzero `k` values.  The ratios
`r_e^0=b_e^0/k_e^0` and `r_f^1=b_f^1/k_f^1` obey
`r_e^0+r_f^1=0` on the bipartite double cover of `KG(6,2)`.  The Kneser graph
is connected and contains a triangle given by three pairs partitioning the
six-set, so its bipartite double cover is connected.  All ratios are
therefore one common `c` with opposite signs, proving (23).

Now use the matching partition (1) at order six.  The term selecting `e` in
`K` contributes `c^2 k_e^0 C(K_R^1)`.  The six terms selecting a pair
`f subset R` contribute

```text
-c^2 k_e^0 sum_(f subset R, |f|=2)
  k_f^1 k_(R-f)^1=-2c^2 k_e^0 C(K_R^1).              (28)
```

Their sum is (24).  The same order-four partition gives (26).  Rank-one
factorization gives (25), which is nonzero in characteristic zero.  `square`

The contradiction is conditional on legal constant attachment of the
six-port row.  Merely computing (24) in the graph response is not a mixed
target certificate.

## 5. Independent deeper-response control away from `h=0`

The exact scalar family

```text
B=x^2/2-xy+y^2,        M=exp(B),
Z=(1+xy)M                                           (29)
```

is a physical `q=2` response with `h=1`, direct weights `1,-1,2`, and
residual rows producing `Q_K=xy`.  Its pair and four-port layers are pure:

```text
Z_2=x^2/2+y^2,
Z_4=x^4/8+y^4/2.                                    (30)
```

At degree `2m`, factorial normalization gives

```text
R_(2,2m-2)=(2-m)(2m-2)!/(m-1)!,                    (31)
```

so `R_(2,4)=-12` and the mixed leak persists for every `m>=3`.  This is a
two-active response control, not a witness and not an `h=0` argument.

Indeed, before labelled normalization the coefficient of
`x^2 y^(2m-2)` in
`B^m/m!+xy B^(m-1)/(m-1)!` is `(2-m)/(2(m-1)!)`, proving (31).

## 6. Target interface, scope, and UNKNOWN remainder

The legal implication is

```text
same-Q constant attachment of K and all fifteen z_4 tensors
 + h=0 fully two-active nonvanishing line form
 -> constant coefficientwise reconstruction of all B pair blocks;

the preceding hypotheses + target-diagonal z_4
 + one nonzero pure z_4 coefficient
 + legal attachment of z_6
 -> displayed mixed depth-six contradiction.         (32)
```

The breadth is all fifteen four-port subwindows of one six-port set.  The
depth is `z_2,z_4` for supply and `z_6` for the detector.  The reconstructed
data are every coefficient of every direct pair block `B_ij`, hence the
same-graph `M` deck by Wick recurrence.  The local ambiguity object is
`ker mu_K`; it is zero on `6+0` and `4+2`, five-dimensional on `5+1` and
`3+3`, and bypassed coefficientwise as stated.  There is no overlap gauge or
transition object because all rows come from one physical graph and one
`Q`.  The target implication is conditional pair-deck supply and, with
depth-six attachment, a mixed coefficient.  The permanent implication is
none.

```text
physical rank-two determinant formula:                         PROVED;
nonzero-minor <=15-row selectors:                              PROVED;
5+1 ten-row singular selector and 3+3 kernel:                  PROVED;
fully two-active six-port tensor pair-deck supply:             PROVED;
h=0 nonzero-pure depth-six detector:                           PROVED;
constant attachment of all required z_2/z_4/z_6 rows:         UNKNOWN;
witness equations force the fully two-active nonvanishing form: UNKNOWN;
witness equations force a nonzero pure z_4 row:                UNKNOWN;
general all-minors-singular witness locus:                     UNKNOWN;
third-colour activity or weighted permanent consequence:       UNKNOWN;
global Krenn--Gu conjecture:                                   UNRESOLVED.
```

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_six_port_physical_wick_selector_two_active_all_subwindow_and_deeper_response.py
python -I claims/arbitrary-order/audit_six_port_physical_wick_selector_two_active_all_subwindow_and_deeper_response.py
```

The primary verifier constructs the physical Wick matrices, checks `J D=L`
symbolically, and proves the affine determinant formula with the `32`-point
unisolvent certificate following (14b).  It checks the homogenized formula on
an exact suite including coordinate walls, replays all shore ranks and
determinants, verifies every singular selector and kernel generator, checks
the coefficientwise polarization cover, and expands the order-four and
order-six response identities.

The independent no-import audit uses integer Bareiss elimination and direct
matching enumeration.  It checks independent specializations of the
homogenized discriminant, the shore table, the `5+1` formula, the `3+3`
kernel, all tensor-word selector cases, the ratio propagation, and both
deeper-response controls without importing the primary implementation.
These bounded computations audit the displayed identities.  The structural
Wick recurrence, finite matrix arguments, graph-connectivity proof, and
matching partitions above establish the theorem.
