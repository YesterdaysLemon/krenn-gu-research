# Resonant rank-two triangles are affine holonomy and binary cubics

## Status

This is an exact characteristic-zero reduction for the sole
all-rank-two-relation triangle stratum left after
[`P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md`](P4_NONRESONANT_DEGENERATE_CUT_TRIANGLE_OBSTRUCTION.md).
It is symbolic and uses only gauge normalization, three cyclic
identities, and the perfect pairing of the squarefree algebra.

The subsequent cut argument in
[`P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md`](P4_RESONANT_NONZERO_ADDITIVE_HOLONOMY_OBSTRUCTION.md)
excludes the first of the following two intrinsic shapes:

1. nonzero additive holonomy gives a tangent-Segre first jet together
   with a cyclic triangle of cut quadrics;
2. zero additive holonomy gives a synchronized binary-cubic map
   `Sym^3(C^2) -> R_3` whose first three coefficients span at most a
   plane.

Thus only the zero-additive-holonomy shape remains on the triangle
frontier for pure-`P_4` component exhaustiveness.  Other exceptional
graphs and lower pair-rank strata also remain, so the global
Krenn--Gu problem is unresolved.

## Multiplicative resonance

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2).
```

Let

```text
U_i=span(y_i,x_i),                 i=1,2,3,
```

and assume every pair image `U_iU_j` has dimension three and its
unique multiplication relation has coefficient-matrix rank two:

```text
a_ij y_i y_j+b_ij y_i x_j+c_ij x_i y_j=0,
b_ij c_ij != 0.                                                       (1)
```

The multiplicative holonomy is resonant precisely when

```text
Omega=c_12 b_13 c_23+b_12 c_13 b_23=0.                              (2)
```

Rescale the three active rows and the three relations.  Condition (2)
is exactly the consistency condition needed to put all edges into the
common oriented form

```text
A_ij y_i y_j+y_i x_j-x_i y_j=0,             i<j.                    (3)
```

Indeed, the required active-row ratios are

```text
r_j/r_i=-c_ij/b_ij,
```

and their product around the triangle is consistent exactly on (2).

## The additive holonomy

A Borel change

```text
x_i -> x_i+s_i y_i
```

changes the constants in (3) by

```text
A_ij -> A_ij+s_i-s_j.                                                (4)
```

Therefore

```text
delta=A_12+A_23-A_13                                                (5)
```

is gauge invariant.  It is the translational holonomy of the affine
connection left after the projective holonomy becomes trivial.

There are two cases.

## Nonzero additive holonomy: a tangent first jet

Put

```text
Y  =y_1y_2y_3,

K_1=x_1y_2y_3,
K_2=y_1x_2y_3,
K_3=y_1y_2x_3,

J_1=y_1x_2x_3,
J_2=x_1y_2x_3,
J_3=x_1x_2y_3,

X  =x_1x_2x_3.                                                       (6)
```

Multiply (3) by the remaining kernel row.  The three equations are

```text
A_12Y+K_2-K_1=0,
A_13Y+K_3-K_1=0,
A_23Y+K_3-K_2=0.                                                     (7)
```

The first plus the third minus the second is

```text
delta Y=0.                                                           (8)
```

If `delta!=0`, then `Y=0`, and (7) gives

```text
K_1=K_2=K_3=:K.
```

Next multiply the three relations by the remaining active row:

```text
A_12K_3+J_1-J_2=0,
A_13K_2+J_1-J_3=0,
A_23K_1+J_2-J_3=0.                                                   (9)
```

The same cyclic combination, after the three `K_i` agree, gives

```text
delta K=0.
```

Hence

```text
Y=K_1=K_2=K_3=0,
J_1=J_2=J_3=:J.                                                      (10)
```

The `R_3`-valued triple multiplication tensor is therefore

```text
J(yxx+xyx+xxy)+X xxx.                                                (11)
```

This is a tangent vector to the Segre variety at `xxx`, with `J` its
first-order direction.  If `J=0`, it degenerates to the pure point
`X xxx`.

There is an additional cut structure.  Every kernel-pair product

```text
q_ij=y_i y_j
```

is nonzero: otherwise the pair map `U_i tensor U_j -> R_2` would have
a decomposable kernel tensor, contradicting the assumed rank-two
unique relation.  By (10), both rows of the opposite plane annihilate
`q_ij`.  Thus

```text
U_k=Ann_R1(q_ij),                 {i,j,k}={1,2,3}.                   (12)
```

The multiplication catalecticant of a nonzero quadratic is symmetric
with zero diagonal.  It cannot have rank one, while (12) gives a
two-dimensional kernel.  Its rank is therefore exactly two.  Hence
each `q_ij` is one of the weighted `1+3`/`2+2` cuts classified in the
nonresonant theorem, but now the cuts come from the kernel-kernel
products rather than the earlier cross bridges.

Finally, purity of the full `P_4` restriction gives

```text
U_0 J=0,                       U_0 X != 0                            (13)
```

where the second expression means that the resulting covector on
`U_0` is nonzero.  Equations (11)--(13) are the exact remaining
nonzero-additive-holonomy incidence.

## Zero additive holonomy: a compressed binary cubic

If `delta=0`, choose

```text
s_1=0,             s_2=A_12,             s_3=A_13.
```

Equation (4) kills all three constants, so

```text
y_i x_j=x_i y_j                  for every i<j.                     (14)
```

Multiplying (14) by the remaining row shows that triple products
depend only on their Hamming weight:

```text
y_1y_2y_3=Y,

x_1y_2y_3=y_1x_2y_3=y_1y_2x_3=K,

y_1x_2x_3=x_1y_2x_3=x_1x_2y_3=J,

x_1x_2x_3=X.                                                        (15)
```

After identifying the three local bases with one abstract binary
space `E=span(y,x)`, multiplication factors through the symmetric
cube:

```text
mu_3: Sym^3(E) -> R_3,

y^3   -> Y,
y^2x  -> K,
yx^2  -> J,
x^3   -> X.                                                         (16)
```

Purity of the `P_4` restriction says

```text
U_0Y=U_0K=U_0J=0,               U_0X != 0.                          (17)
```

The pairing

```text
R_1 tensor R_3 -> R_4=C
```

is perfect.  Since `U_0` is a plane, its annihilator in `R_3` is a
plane.  Therefore

```text
dim span(Y,K,J)<=2,              X notin span(Y,K,J).               (18)
```

The zero-holonomy problem is thus a binary cubic whose first three
osculating coefficients compress to a two-plane while the last
coefficient escapes it.

## What the translation buys

The resonance has two layers, exactly as for an affine local system on
a circle:

```text
projective holonomy = 1,
translation class   = delta in H^1(S^1,C).
```

The nonzero class produces the dual-number/tangent tensor (11); the
zero class produces the symmetric-cubic map (16).  This is far smaller
than the original plane-incidence equations.

The local-system analogy is close to Cohen--Orlik,
[Arrangements and local systems](https://arxiv.org/abs/math/9907117).
The tangent tensor belongs to the geometry studied by
Ballico--Bernardi,
[Tensor ranks on tangent developables of Segre
varieties](https://arxiv.org/abs/1210.7976), while the general
secant/tangent dictionary is surveyed by Bernardi et al.,
[Hitchhiker guide to: Secant varieties and tensor
decomposition](https://arxiv.org/abs/1812.10267).
Those papers provide the neighboring languages; equations (2)--(18)
are the repository's direct reduction.

## Exact frontier

After the nonzero additive-holonomy obstruction, the next symbolic
targets are:

1. classify binary-cubic multiplication maps (16) satisfying the
   compression flag (18); and
2. identify whether their closures lie in the nine known components
   or force another component.

No claim of emptiness is made here for that flat branch.

## Verification

Run:

```text
python verify_p4_resonant_rank_two_triangle_affine_holonomy.py
python audit_p4_resonant_rank_two_triangle_affine_holonomy.py
```

The primary verifier checks the gauge invariant, the two cyclic
identities, the tangent coefficient tensor, and the binary-cubic
factorization.  The independent audit treats (4) as the cochain
complex of a triangle and verifies the unique additive cohomology
class before replaying both coefficient patterns.  These scripts are
small exact proofs, not searches.
