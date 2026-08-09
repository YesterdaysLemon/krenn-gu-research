# `H31` obstruction on the `r=0` boundary of the ninth component

## Status

This is an exact characteristic-zero theorem on the divisor

```text
A B !=0,             r=0
```

of the embedded-`P_3` ninth pure-`P_4` component.

The complete marked `H31` fibre is empty on this divisor.  Together
with the normalized-chart theorem and the support-two `A=0` theorem,
this closes the whole six-parameter affine component family with
`B!=0` for `H31`.  The projective compactification outside that
family chart has since been closed by homogeneous normal support:
[`P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_PROJECTIVE_CLOSURE_OBSTRUCTION.md).

The proof is symbolic.  The open part `t!=0` is the old normalized
chart in a signed source-coordinate permutation.  At the genuine
corner `r=t=0`, the binary problem becomes the intersection of an
apolar insertion image with a two-secant line of the
`P^1 x P^1 x P^1` Segre variety.  Its mixed determinant has four
factors.  One residual tangent--Segre sheet is excluded by three
neighboring minors; the other three sheets have nine second-rank-drop
families, and five singular base points leave only nine further
families.  Tiny factored one-marked determinants close all of them.

This theorem does not classify the pure-`P_4` component
compactification, prove that the nine known components are exhaustive,
produce a prize graph, or resolve the global Krenn--Gu conjecture.

## The coordinate-swap part

In the component coordinates,

```text
U_0=span((1,0,r,t),(0,1,s,u)).
```

If `r=0,t!=0`, apply the signed source permutation

```text
X_2'=-X_3,             X_3'=-X_2.                 (1)
```

It sends the first row of `U_0` to `(1,0,-t,0)`, so the new parameter
`r'=-t` is nonzero.  On the last three planes it interchanges the two
nonzero sign-rectangle parameters:

```text
(A',B')=(B,A),
```

after interchanging the first two of those three modes.  The permanent
changes only by an overall nonzero scalar.  Source and mode
permutations preserve the `H31` signature.  Hence `t!=0` is already
excluded by
[`P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md`](P5_H31_EMBEDDED_P3_COMPONENT_NORMALIZED_BOUNDARY_OBSTRUCTION.md).

It remains to take

```text
r=t=0.                                             (2)
```

## The genuine mode-zero-plane corner

Normalize `A,B` and use pure-factor bases

```text
alpha_0=(0,1,S,U),          beta_0=(1,0,0,0),

alpha_1=(0,-1,1,0),         beta_1=(0,-1,0,1),
alpha_2=(0, 1,0,1),         beta_2=(0, 1,1,0),
alpha_3=(0, 0,1,1),         beta_3=(0,-1,0,1).     (3)
```

Mark the last three beta rows by

```text
beta_1+a alpha_1,
beta_2+b alpha_2,
beta_3+c alpha_3.                                  (4)
```

As before, deletions `1,2,3` have a zero all-alpha diagonal.  Only
deletion zero can be binary.

The projected mode-zero beta row is `t_0(1,S,U)`.  If the alpha slice
has nonzero `AAA` diagonal `D`, the beta slice contains `t_0 D` in
the same word.  Its mode-zero extension can change only the `BBB`
coefficient, because the last three planes restrict `P_3` to
`-2 BBB`.  Binary diagonality therefore forces

```text
t_0=0.                                             (5)
```

Let

```text
(x_1,x_2,x_3,y_1,y_2,y_3)
```

be extension values on the marked bases (4).  The alpha slice is the
apolar first variation

```text
D_(1,S,U)=sum_i ell_i tensor
             P_3((1,S,U),-,-).                    (6)
```

Its `BBB` coefficient is cancelled by the free alpha extension in
mode zero.  Thus the six mixed words must vanish, while `AAA` must be
nonzero.

## The tangent--Segre divisor

The determinant of the six mixed equations in the six extension
values factors as

```text
-4 d_1 d_2 d_3 Phi,                               (7)
```

where

```text
d_1=S-U-1,       d_2=S+U-1,       d_3=S+U+1,
```

and the residual multiaffine factor is

```text
Phi =
 S { U[(S-U)(a+1)(b+1)-a(b+1)+1] + b(S+1) }
 + c { S b(S+U+1) + U a(1-S-U) }.                 (8)
```

Geometrically, (7) is the pullback of the incidence between the
six-dimensional insertion image and the diagonal secant line through
`AAA,BBB`.  The three linear factors are signed Segre boundary
planes; `Phi` is the residual tangent--secant sheet.

On a generic point of `d_1=0,d_2=0,d_3=0`, the respective kernel is

```text
<y_3>,           <y_2>,           <y_1>.           (9)
```

All three kill `AAA`, so they are not genuine binary directions.

## The residual sheet

First assume

```text
Phi=0,       S U d_1 d_2 d_3 !=0.                 (10)
```

A cofactor kernel has alpha diagonal

```text
D=2 S U d_1 d_2 d_3.                              (11)
```

Let `Y!=0` be the beta diagonal parameter.  Modulo `Phi`, three
neighboring one-marked determinants are

| mode; rows | determinant |
| --- | --- |
| `1; 0247` | `4 S U Y^2 (b+1)d_1 d_2 d_3^2` |
| `2; 0247` | `4 S U Y^2 (a+1)d_1 d_2^2 d_3` |
| `3; 0247` | `-4 S U Y^2 a d_1^2 d_2 d_3` |       (12)

Their transverse pure entries are respectively `d_3,-d_2,-d_1`.
If the first two determinants vanish, then `a=b=-1`, and the third
is nonzero.  Hence the generic residual sheet has no `H31` lift.

The parts of `Phi=0` with one zero projected coordinate but away from
the five singular base points split as follows:

| base divisor | residual branches | one nonzero determinant |
| --- | --- | --- |
| `S=0` | `a=0` | mode `2`, rows `0247`: `4U Y^2(U-1)^2(U+1)` |
| `S=0` | `c=0` | mode `1`, rows `0347`: `-4U Y^2(U-1)^2(U+1)` |
| `U=0` | `b=0` | mode `1`, rows `0247`: `4S Y^2(S-1)(S+1)^2` |
| `U=0` | `c=-1` | mode `1`, rows `0157`: `4S Y^2(S-1)(S+1)^2` | (13)

The omitted factors in (13) are units on the stated strata, and each
selected mode has a nonzero transverse pure entry.

## Second rank drops on the signed sheets

On `d_i=0`, a genuine direction can occur only when the associated
`6 x 5` presentation drops rank.  Its maximal-minor ideals split into
three branches per sheet.  Put

```text
A_*=Sa+S-a,
B_-=Sb+S-1,
B_+=Sb+S+1.
```

Away from the sheet endpoints, the complete branch table is:

| sheet | branch | one nonzero neighboring determinant |
| --- | --- | --- |
| `d_1=0` | `A_*=B_-=0` | mode `2`, rows `0267`: `8S Y^2` |
| `d_1=0` | `B_-=c=0` | mode `1`, rows `0267`: `8Y^2(S-1)` |
| `d_1=0` | `A_*=0,c=-1` | mode `2`, rows `0267`: `8S Y^2` |
| `d_2=0` | `A_*=0,b=0` | mode `2`, rows `0367`: `-8S Y^2` |
| `d_2=0` | `A_*=0,c=-S` | mode `2`, rows `0367`: `-8S Y^2` |
| `d_2=0` | `b=-1,c=-S` | mode `2`, rows `0347`: `-8S Y^2(S-1)` |
| `d_3=0` | `B_+=0,a=0` | mode `2`, rows `0247`: `-8S Y^2` |
| `d_3=0` | `B_+=0,c=S` | mode `1`, rows `0367`: `8Y^2(S+1)` |
| `d_3=0` | `a=-1,c=S` | mode `3`, rows `0247`: `8S^2Y^2` | (14)

For `d_1,d_2`, the endpoint factors are `S(S-1)`; for `d_3` they are
`S(S+1)`.  Thus every determinant in (14) is nonzero on its stated
open sheet.  The free old kernel direction `y_i` does not occur in
any displayed determinant.

## The five singular base points

The only remaining projected mode-zero rows are

```text
(S,U)=(0,0),(0,1),(0,-1),(1,0),(-1,0).            (15)
```

At `(0,-1)` and `(1,0)`, the sparse mixed equations force `AAA=0`.
The other three points each have exactly three genuine marking
families.  Their complete one-marked cover is:

| point | marking family | determinant cover |
| --- | --- | --- |
| `(0,1)` | `a=c=0` | `-8Y^2b`, `-8Y^2(b+1)` |
| `(0,1)` | `a=b=0` | `8Y^2` |
| `(0,1)` | `b=-1,c=0` | `8Y^2` |
| `(-1,0)` | `b=0,c=-1` | `8Y^2a`, `-8Y^2(a+1)` |
| `(-1,0)` | `a=b=0` | `-8Y^2` |
| `(-1,0)` | `a=-1,c=-1` | `8Y^2` |
| `(0,0)` | `a=b=0` | `4Y^2` |
| `(0,0)` | `b=c=0` | `4Y^2` |
| `(0,0)` | `a=0,c=-1` | `4Y^2` |                 (16)

In the two paired rows, the factors `b,b+1` and `a,a+1` cannot vanish
simultaneously.  All other rows have a constant nonzero determinant.
The selected neighboring mode always has a nonzero pure transverse
entry.

## Why a neighboring determinant is enough

A nonzero `4 x 4` determinant in (12)--(16) makes the neighboring
one-marked map injective.  The candidate third local row must
therefore vanish on the four-dimensional deletion-zero source
hyperplane.  Its pure-hyperplane one-marked map has a nonzero entry
on the remaining transverse coordinate, so the row vanishes globally.
This contradicts local rank three, which is forced by conciseness of
`Delta_3`.

Equations (7)--(16) exhaust every binary family at (2), and (1)
transports the rest of `r=0` to the already closed chart.  This proves
the theorem.

## Cross-specialty interpretation

The insertion tensor (6) is a tangent vector to a Segre restriction,
while binary diagonality asks it to lie on a secant line.  This is why
the correct object is the tangent--secant incidence divisor (7), not a
large permanent ideal.  The viewpoint matches the rank stratification
of tangential Segre varieties in
[Ballico--Bernardi](https://arxiv.org/abs/1210.7976) and the general
secant/tensor dictionary surveyed in
[Bernardi et al.](https://arxiv.org/abs/1812.10267).  Those results are
not used as black boxes here; they predict the successful order:

```text
first variation -> Segre incidence -> Fitting strata -> kernel cover.
```

## Verification

Run

```text
python verify_p5_h31_embedded_p3_component_r_zero_boundary.py
python audit_p5_h31_embedded_p3_component_r_zero_boundary.py
```

The primary verifier reconstructs the insertion tensor, factorization
(7), residual cofactor kernel, signed-sheet maximal-minor ideals,
eighteen boundary kernel families, and every displayed one-marked
minor symbolically.  The independent modular audit rebuilds
permanents by subset multiplication and checks representative points
of every stratum over two finite fields.  The modular audit is
corroboration only; the theorem is the characteristic-zero proof
above.
