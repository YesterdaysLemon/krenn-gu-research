# Balanced `m=3` joint-rank-five Hilbert--Burch all-coordinate-distinct exclusion

## Status

**Exact characteristic-zero exclusion of the all-coordinate-distinct
`(1,1,1)` Hilbert--Burch boundary of the normalized, target-consistent
physical `m=3` common-three-space full-sensor stratum.**  Let `U` be the
total singleton span, put `K=image H`, and assume

```text
dim U=3,                         rank H=5.             (1)
```

Use the S2AG Hilbert--Burch normal form

```text
ker D_B=span{(x,0,z),(0,y,z)},

B_23=-y tensor z,       B_13=-x tensor z,
B_12= x tensor y.                                      (2)
```

Suppose all three triangle factors are target-coordinate vectors on three
different coordinates.  After permuting colours and retaining the nonzero
scalars, write

```text
x=lambda e_0,       y=mu e_1,       z=nu e_2,
lambda mu nu!=0.                                      (3)
```

Then no target-consistent point satisfying (1)--(3) exists.

The proof uses the same exact torus self-recovery that closed the repeated
chart in S2AP.  It forces a coloop among seven annihilator rows.  Here the
complete binary product `R x P x Q` is zero and the three diagonal targets
sit on its three exterior faces.  If the combined row is the coloop, all
three row planes coincide; a totally cubic-zero two-plane cannot carry two
fully transverse quadratic target images.  If an ordinary row is the
coloop, root/colour symmetry makes it `q_0`; the other two row planes
coincide, while `q_0` and the remaining `q_1` are two quadratic
annihilators.  The missing row `q_2` would give fully transverse nonzero
mixed images with both, which an exact two-source lemma forbids.

Together with S2AN--S2AP, this excludes every `(1,1,1)` chart in which all
three factors are coordinate vectors, and every chart with a repeated
coordinate factor.  It leaves the case of two distinct coordinate factors
and a genuinely noncoordinate third factor, the `(1,1,2)` and `(1,2,2)`
profiles, joint rank at most four, other physical components and pole
strata, higher orders, and the global conjecture open.  Global Krenn--Gu
remains **UNRESOLVED**.

## 1. The coordinate-triangle target faces

The derivative is

```text
D_B(a,b,c)
 =-mu nu a tensor e_1 tensor e_2
  -lambda nu e_0 tensor b tensor e_2
  +lambda mu e_0 tensor e_1 tensor c.                (4)
```

Write the transposed root rows and pure targets as

```text
r_i=rho(e_i^*),       p_j=pi(e_j^*),
q_k=theta(e_k^*),     T_k=X_k tensor Y_k tensor Z_k. (5)
```

The support of (4) is exactly

```text
{(i,1,2):0<=i<=2}
 union {(0,j,2):0<=j<=2}
 union {(0,1,k):0<=k<=2}.                            (6)
```

Every other root coefficient is untouched, so its all-cross permanent is
the corresponding coefficient of the diagonal target.  Put

```text
R=span(r_1,r_2),
P=span(p_0,p_2),
Q=span(q_0,q_1).                                     (7)
```

Each space in (7) is a two-plane.  For example, `r_1` is separated from
`r_2` by the untouched coefficients `(1,1,1)` and `(2,1,1)`, while `r_2`
is nonzero at `(2,2,2)`; the other two families are identical after cyclic
permutation.

No diagonal colour belongs to all three index sets in (7), and none of
their eight cells belongs to (6).  Hence

```text
per(R,P,Q)=0.                                         (8)
```

The three exterior faces retain one diagonal target each.

## 2. The seven-row three-space and its coloop

The derivative-kernel annihilator is

```text
L=(ker D_B)^perp
 ={(alpha,beta,gamma):
     lambda alpha_0+nu gamma_2=0,
     mu beta_1+nu gamma_2=0},        dim L=7.        (9)
```

As in S2AP,

```text
N=K^perp subset L,       dim N=4,
V=H^T(L),                dim V=3.                    (10)
```

Define the two quotient directions and the combined row

```text
A=(nu/lambda) r_0,       B=(nu/mu) p_1,
h=A+B-q_2.                                             (11)
```

The seven rows

```text
r_1,r_2,p_0,p_2,q_0,q_1,h                            (12)
```

lie in `V` and are the images of a basis of `L`.  The exact untouched faces
are

```text
per(A,p_j,q_k)=(nu/lambda) delta_(j,0)delta_(k,0) T_0,
                    j in {0,2}, k in {0,1},

per(r_i,B,q_k)=(nu/mu) delta_(i,1)delta_(k,1) T_1,
                    i in {1,2}, k in {0,1},

per(r_i,p_j,q_2)=delta_(i,2)delta_(j,2) T_2,
                    i in {1,2}, j in {0,2}.          (13)
```

For a product root functional, transpose of (4) gives

```text
D_B^T(alpha tensor beta tensor gamma)
 =(-mu nu beta_1 gamma_2 alpha,
   -lambda nu alpha_0 gamma_2 beta,
    lambda mu alpha_0 beta_1 gamma).                 (14)
```

If all seven coordinates of `ell=(alpha,beta,gamma) in L` in the basis
underlying (12) are nonzero, then all nine target-coordinate evaluations of
`alpha,beta,gamma` are nonzero and

```text
D_B^T(alpha tensor beta tensor gamma)
   =nu^2 gamma_2^2 ell.                              (15)
```

Thus `ell` cannot belong to `N`, by the S2R fully supported product-
annihilator obstruction.  The four-plane `N` is contained in the union of
the seven coordinate hyperplanes of `L`.  Over an infinite
characteristic-zero field it is contained in one of them.  Equivalently,

> One row in (12) is a coloop and the other six span a two-plane. (16)

If `h` is the coloop, (7) gives `R=P=Q`.  If an ordinary row is the coloop,
the other two row planes agree.  Simultaneous root and target-colour
permutations act transitively on the six ordinary rows: label such a row by
the ordered pair `(factor colour omitted by its family, row colour)`, whose
entries are distinct.  The symmetric group on three colours is transitive
on these six ordered pairs.  Hence it is enough to treat `q_0`.

## 3. Two exact two-plane lemmas

Let `W=X direct-sum Y direct-sum Z` and let `S subset W` be a two-plane.

### Lemma 1 (totally cubic-zero plane)

Suppose

```text
per(S,S,S)=0.                                         (17)
```

If `a,b in W` make `per(a,S,S)` and `per(b,S,S)`
nonzero maps with one-dimensional decomposable images, those image tensors
share at least two source factor lines.

### Proof

Restrict every source-coordinate form to `S`.  If all three source
projections of `S` were nonzero, choose one nonzero restricted coordinate
form from each source.  Their product is a nonzero binary cubic, whereas
(17) says that cubic is zero.  Hence one source projection vanishes; after
permuting sources take

```text
S subset X direct-sum Y.                              (18)
```

If a second source projection vanished, `per(a,S,S)` would be zero for
every `a`.  Thus both projections in (18) are nonzero.  Write them as
`x:S->X` and `y:S->Y`.  Then

```text
per(a,s,t)
 =a_Z tensor (x(s) tensor y(t)+x(t) tensor y(s)).    (19)
```

The parenthesized bilinear map is independent of `a`.  A nonzero
one-dimensional decomposable image in (19) therefore fixes one `X` factor
line and one `Y` factor line.  Every other nonzero one-dimensional
decomposable image has those same two lines.  QED.

### Lemma 2 (quadratic-annihilator fork)

Let `0!=v in S` and `w,a in W` satisfy

```text
per(v,S,S)=per(w,S,S)=0.                             (20)
```

If `per(a,v,-)|S` and `per(a,w,-)|S` are nonzero rank-one maps with
decomposable images, their image tensors share at least one source factor
line.

### Proof

Let `m in S^*` span the annihilator of `v`.  The kernel on binary cubics of
directional differentiation along `v` is

```text
ker(partial_v:S^3 S^*->S^2 S^*)=span(m^3).           (21)
```

Suppose all three source projections of `S` were nonzero.  Choose nonzero
restricted coordinate forms `xi,eta,zeta` from the three sources.  Equation
(20) puts the nonzero split cubic `xi eta zeta` in (21), so unique
factorization makes all three forms proportional to `m`.  Multiplying any
other nonzero restricted coordinate form by the two fixed forms in the
other sources gives the same conclusion.  Thus every source-coordinate
form on `S` lies on `span(m)`, contradicting that all coordinate forms
together span the two-space `S^*`.

One source projection therefore vanishes.  A nonzero map
`per(a,v,-)|S` rules out two vanishing source projections.  After permuting
sources, (18) holds with both projections nonzero.  The symmetric bilinear
map in parentheses in (19) is nonzero: otherwise setting `s=t` and using
characteristic zero would make one of the two projection maps vanish.
Projecting `per(w,S,S)=0` to `X tensor Y tensor Z` now gives

```text
w_Z tensor (x(s) tensor y(t)+x(t) tensor y(s))=0,
```

so `w_Z=0`.  Also `v_Z=0` because `v in S`.  Consequently every value of
both mixed maps in the lemma uses the same fixed third-source factor
`a_Z`.  Nonzero decomposable images therefore share that factor line.  QED.

## 4. Exclusion of both coloop types

### 4.1 The combined row is the coloop

If `h` is the coloop, the six rows in (7) span one two-plane

```text
R=P=Q=S.                                              (22)
```

Equation (8) is `per(S,S,S)=0`.  The first two faces in (13) say that

```text
per(A,S,S) and per(B,S,S)                            (23)
```

are nonzero rank-one maps onto `T_0` and `T_1`, respectively.  Those pure
targets are fully transverse, contrary to Lemma 1.

### 4.2 An ordinary row is the coloop

By the symmetry in Section 2, suppose `q_0` is the coloop.  Then

```text
R=P=S,                q_1,h in S,                    (24)
```

and (8) gives

```text
per(q_0,S,S)=per(q_1,S,S)=0.                         (25)
```

Use `q_2=A+B-h`.  For `j in {0,2}`, the first face in (13), the zero
`q_0` row of the second face, and (25) give

```text
per(q_2,q_0,p_j)
 =(nu/lambda) delta_(j,0) T_0.                       (26)
```

For `i in {1,2}`, the zero `q_1` row of the first face, the second face,
and (25) similarly give

```text
per(q_2,q_1,r_i)
 =(nu/mu) delta_(i,1) T_1.                           (27)
```

Because both `(p_0,p_2)` and `(r_1,r_2)` are bases of `S`, equations
(26)--(27) say that

```text
per(q_2,q_0,-)|S and per(q_2,q_1,-)|S               (28)
```

are nonzero rank-one maps onto the fully transverse target lines
`T_0,T_1`.  Lemma 2, with `(a,v,w)=(q_2,q_1,q_0)`, forbids (28).

Both coloop types are impossible, contradicting (16).  Hence the
all-coordinate-distinct pattern (3) does not occur.

## 5. Proof-topology consequence

Together with S2AN--S2AP, the `(1,1,1)` frontier is now

```text
two or three coordinate factors with a repeated line: IMPOSSIBLE;
three pairwise-distinct coordinate factors:           IMPOSSIBLE;
two distinct coordinate factors and a genuinely
  noncoordinate third factor:                         OPEN;

Hilbert--Burch (1,1,2), (1,2,2):                     OPEN;
joint rank at most four / other physical branches:    OPEN;
global Krenn--Gu conjecture:                          UNRESOLVED.      (29)
```

No numerical search, finite-field promotion, or generic-point assumption is
used.

## Focused replay

Run from repository root:

```text
uv run --with sympy python claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_all_coordinate_distinct_exclusion.py
python -I claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_all_coordinate_distinct_exclusion.py
python -m py_compile claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_all_coordinate_distinct_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_all_coordinate_distinct_exclusion.py
uv run --with ruff==0.16.2 ruff check --no-cache claims/arbitrary-order/verify_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_all_coordinate_distinct_exclusion.py claims/arbitrary-order/audit_balanced_m3_common_three_space_joint_rank_five_hilbert_burch_all_coordinate_distinct_exclusion.py
```

The primary replay checks the scalar-general derivative and annihilator,
the seven untouched support cells, zero binary cube, three target faces,
torus self-recovery, coloop orbit, binary directional-derivative kernel, and
two-source factor-sharing identities.  The independent audit imports no
repository or third-party module and reconstructs those identities with
`Fraction` arithmetic, a different tensor ordering, and separate
elimination.  The finite-union and unique-factorization steps are the
written proof above.

## Dependencies

- [Repeated-coordinate Hilbert--Burch exclusion](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_HILBERT_BURCH_REPEATED_COORDINATE_EXCLUSION_THEOREM.md)
- [Joint-rank-five derivative and torus localization](BALANCED_M3_COMMON_THREE_SPACE_JOINT_RANK_FIVE_DERIVATIVE_TORUS_LOCALIZATION_THEOREM.md)
- [Singleton-span torus-annihilator obstruction](BALANCED_M3_SINGLETON_SPAN_TORUS_ANNIHILATOR_PERMANENT_RANK_OBSTRUCTION.md)
