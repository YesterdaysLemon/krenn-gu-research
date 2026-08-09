# Five-root two-fan sharing and shared-root Veronese transversality

## Status

**Exact characteristic-zero sharing classification, rank theorem, and common
graph-side controls.**  Put two fully polarized root-pair fans on the same
four-port window in the five-root, seven-blocker, two-residual `P_7` cell.
There are only three root-support patterns.

1. The pairs are equal.  Changing tangent bases or the nonzero shore scalar
   does not change the fan kernel, so there is only one observation plane.
2. The pairs share one root.  Their three-root shores share the other two
   roots.  Contrary to a tempting factorization argument, the common root
   does **not** force a common invisible face.
3. The pairs are disjoint.  Each pair lies in the other pair's shore and the
   fifth root is the unique common shore root.  The common fifth row likewise
   imposes no fan-kernel relation.

For the shared-root pattern, write the two fans as `K(A,B)` and `K(A,C)`.
When the four rows of `B` and `C` together span the port space, their common
kernel is exactly the space of binary quadrics on `ker A` that vanish on the
four restricted coordinate directions.  Thus it is zero precisely when at
least three distinct projective directions occur.  If exactly two directions
occur, the common kernel is one-dimensional.  This is a sharp second-Veronese
dichotomy, not a genericity slogan.

An explicit integer shared-root example has fan ranks `4,4` and stacked rank
six.  A second example has ranks `4,4`, stacked rank five, and exactly the
predicted common line.  A disjoint-pair rank-six example is also embedded in
the same five-root geometry.

These are not merely unrelated fan matrices.  One common bilinear edge-block
system with torus root and blocker vectors realizes either example as two
legally isolated graph-side `P_7` coefficient sectors on the same physical
window.  Every three-root shore permanent is simultaneously `6`, root--root
and root--residual nuisance blocks are zero, and shared roots use literally
the same root--port blocks.  What is not supplied is the target GHZ equality,
mixed blocker-word cancellation, or a theorem forcing such sectors in every
hypothetical witness.  `P_7` and Krenn--Gu remain **UNKNOWN/UNRESOLVED**.

No graph, support, colour-word, matching-family, or parameter enumeration is
used.

## 1. Exact five-root sharing geometry

Let

```text
R={0,1,2,3,4},              |R|=5,
B=D disjoint_union W,       |D|=3, |W|=4.             (1)
```

A root pair `I` supplies a fan on `W`; its shore root set and shore scalar are

```text
J_I=R\I,                    f_I=per H[J_I,D].         (2)
```

For two pairs `I,I'`,

```text
J_I intersect J_I'=R\(I union I'),
|J_I intersect J_I'|=5-|I union I'|.                 (3)
```

Consequently the following list is exhaustive.

| pair pattern | normal form | shore pattern |
|:--|:--|:--|
| equal | `ab,ab` | the same shore `cde` |
| one shared root | `ab,ac` | shores `cde,bde`, sharing `d,e` |
| disjoint | `ab,cd` | shores `cde,abe`, sharing only `e` |

In the disjoint case, each root pair is contained in the opposite shore.
In the shared-root case, the common root `a` belongs to neither shore, each
noncommon fan root belongs to the opposite shore, and the remaining two roots
belong to both shores.

This incidence classification is only set theory, but it identifies exactly
which pure root--blocker rows are shared before any rank claim is made.

### Shore nonvanishing has no pairwise obstruction

Take the `5 x 3` pure root--shore matrix

```text
H[R,D]=all-ones.                                      (4)
```

Then for every one of the ten root pairs,

```text
f_I=per(ones_(3 x 3))=3! = 6 !=0.                    (5)
```

Thus equal, shared-root, and disjoint pair patterns all admit their required
nonzero shores simultaneously.  The shared rows in (3) do not themselves
force a shore to vanish.  Nonzero factors `f_I` multiply fan matrices and
therefore do not change their kernels.

## 2. Fan notation

Order the six port pairs as

```text
01,02,03,12,13,23.                                   (6)
```

For a face vector `x`, let `X(x)` be the hollow symmetric `4 x 4` matrix with
off-diagonal entries `x_uv`.  If `A,B` are `2 x 4` root--port incidence
matrices, the fully polarized fan is

```text
Phi_(A,B)(x)=A X(x) B^T,
K(A,B)x=vec(Phi_(A,B)(x)).                            (7)
```

The second expression is a `4 x 6` matrix.  Its columns are

```text
a_u tensor b_v+a_v tensor b_u.                       (8)
```

This is the mixed second permanental, or zeon, compound.

If the same physical root pair is repolarized by `P,Q in GL_2`, then

```text
K(PA,QB)=(P tensor Q)K(A,B).                         (9)
```

Multiplication by a nonzero shore scalar is also invertible on the output.
Hence two copies of the **same** root pair have the same kernel.  Equal-pair
sharing cannot produce six-face tomography.

## 3. The shared-root Veronese theorem

Consider distinct pairs `ab` and `ac`.  Use one tangent basis at their common
root and write their fans as

```text
K(A,B),                 K(A,C),
D_0=[B;C] in K^(4 x 4).                               (10)
```

Here vertical brackets mean row stacking.

### Theorem 1 (exact shared-root reduction)

Assume `D_0` is invertible.  Then

```text
ker K(A,B) intersect ker K(A,C)
 ={x: A X(x)=0}.                                     (11)
```

If `rank A=2`, let `N` be a `4 x 2` matrix whose columns form a basis of
`ker A`, and let `n_u=(p_u,q_u)` be row `u` of `N`.  Define

```text
V_N=
[p_0^2  2p_0q_0  q_0^2]
[p_1^2  2p_1q_1  q_1^2]
[p_2^2  2p_2q_2  q_2^2]
[p_3^2  2p_3q_3  q_3^2].                             (12)
```

Then

```text
dim(ker K(A,B) intersect ker K(A,C))=3-rank V_N.     (13)
```

Because `N` has rank two, its nonzero rows contain at least two distinct
projective directions.  In characteristic zero this gives the sharp
dichotomy

```text
at least three distinct [n_u] in P^1:  intersection=0;
exactly two distinct [n_u] in P^1:     dimension=1.   (14)
```

Zero rows are simply omitted when counting projective directions.

Proof.  The two fan equations concatenate as

```text
[A X B^T | A X C^T]=A X D_0^T.                       (15)
```

Since `D_0` is invertible, (15) vanishes exactly when `AX=0`, proving
(11).  A symmetric matrix whose image lies in `ker A` has a unique form

```text
X=N S N^T,                  S=S^T in K^(2 x 2).       (16)
```

The hollow condition is

```text
0=X_uu=n_u S n_u^T,          u=0,1,2,3.              (17)
```

Writing the three entries of `S` as coordinates turns (17) into `V_N s=0`,
which proves (13).  The rows of `V_N` are second-Veronese evaluations.  A
nonzero binary quadratic has at most two distinct projective zeros, so these
evaluations span dimension three exactly when at least three directions
occur.  With exactly two distinct directions they have rank two.  This proves
(14).

The theorem shows precisely what common-root factorization retains.  It is a
possible binary quadratic on the common kernel plane, not an unavoidable
face direction.

### Transverse shared-root control

Take

```text
A=[-1 -1  1 0]       B=[1 0 0 0]       C=[0 0 1 0]
  [-1 -2  0 1],        [0 1 0 0],        [0 0 0 1].   (18)
```

Then `[B;C]=I_4`, and

```text
N=[1 0]
  [0 1]
  [1 1]
  [1 2]                                             (19)
```

spans `ker A`.  Its four row directions are distinct.  Directly,

```text
rank K(A,B)=rank K(A,C)=4,
rank [K(A,B);K(A,C)]=6.                              (20)
```

Thus two fans sharing one physical root can have transverse invisible planes.

### Sharp defective control

Take

```text
A_0=[1 -1 0  0]
    [0  0 1 -1],                                     (21)

B_0=[1 0 1 1]       C_0=[1 0 1 2]
    [0 1 1 2],          [0 1 2 1].                   (22)
```

Here `det[B_0;C_0]=-1`, while `ker A_0` has row directions

```text
(1:0),(1:0),(0:1),(0:1).                             (23)
```

Both fans have rank four, but their stack has rank five and common kernel

```text
span(0,1,1,1,1,0)                                   (24)
```

in the pair order (6).  This is the off-diagonal binary quadratic between
the two projective direction classes.  Hence both alternatives in (14) are
attained by rank-four fans.

### Theorem 2 (shore-graph and five-root line-family alternative)

For one fixed window, form the **shore-availability graph** `G_W` on the five
roots by declaring

```text
ij in E(G_W) iff f_ij !=0.                            (25)
```

Let `L_i=rowspace(A_i)`, a projective line in `P^3`, and suppose every
`A_i` has rank two.  If `ij,ik` are two edges of `G_W`, then either

```text
the fans K(A_i,A_j),K(A_i,A_k) are transverse;
the common root i lies on the rank-two Veronese boundary; or
L_j intersects L_k.                                  (26)
```

Indeed, `L_j intersect L_k={0}` in vector-space notation is exactly the
invertibility of `[A_j;A_k]`.  Theorem 1 then gives transversality unless the
Veronese matrix at root `i` has rank at most two.

In particular, assume `G_W=K_5`, so all ten shore factors are nonzero.  Then
the five-root incidence family satisfies the exact trichotomy

```text
some shared-root fan pair is transverse; or
some root lies on the rank-two Veronese boundary; or
the five projective row-lines L_i are all concurrent or all coplanar. (27)
```

Proof of the last alternative.  If the first two alternatives fail, choose a
third root `i` for any two roots `j,k`.  The wedge `ij,ik` exists in `K_5`,
so (26) forces `L_j` and `L_k` to meet.  Thus the five lines are pairwise
intersecting.  Two distinct members meet at a point `p` and span a plane
`Pi`.  If every member contains `p`, the lines are concurrent.  Otherwise a
third line lies in `Pi` and avoids `p`; any line meeting the first two and
this third line must also lie in `Pi`.  Hence the whole family is coplanar.

For a noncomplete shore graph, (26) is the correct shore-aware statement:
only endpoints of an available two-edge wedge are constrained.  A vanished
shore deletes the corresponding fan and no kernel conclusion follows from
it.  Equation (5) shows that the complete shore graph is nevertheless a
legal pure configuration, so (27) is not vacuous.

## 4. Disjoint-pair control

For disjoint pairs `01` and `23`, use

```text
A_1=[1 0 1 0]       B_1=[1 0 0 1]
    [0 1 0 1],          [0 1 1 0],                   (28)

A_2=[1 0 1 1]       B_2=[1 0 1 2]
    [0 1 1 2],          [0 1 2 1].                   (29)
```

Their fan ranks are `4,4` and their stacked rank is six.  Place these four
matrices at roots `0,1,2,3`; root `4` is the fifth root shared by both shores.
Equation (4) makes both shore factors six.  Therefore the fifth shore root
does not force a common invisible face either.

## 5. One common graph-side `P_7` coefficient system

The rank controls above fit inside one actual five-root graph-side sector,
not only an abstract observation space.

At every root and blocker/port take the torus vector

```text
v=w=(1,1,1).
```

At a root let

```text
alpha=e_0^*,             S=ker alpha,
pi(x)=x-alpha(x)v=(0,x_1-x_0,x_2-x_0).               (30)
```

At every blocker or port use `beta=e_0^*`, so `beta(w)=1`.  Define each
root--shore-blocker block by

```text
E_(i,d)=alpha tensor beta,             d in D.        (31)
```

It has frozen value one and vanishes when the root argument is tangent.  For
an assigned incidence column `l_(i,u)=(r,s)^T`, define the root--port block

```text
G_(i,u)=((-r-s)e_0^*+r e_1^*+s e_2^*) tensor beta.   (32)
```

This block vanishes at `v`, while its restrictions to the tangent basis
`e_1,e_2` are exactly `(r,s)`.  Set all root--root and root--residual blocks
to zero.  Leave the common response on the residuals and `W` arbitrary.

For the mixed derivative at a root pair `I`:

- both differentiated roots must use two distinct ports of `W`, because
  (31) is tangent-zero and all root companion blocks are zero;
- the other three roots must use `D`, because (32) is frozen-zero;
- their shore sum is `per(ones_(3 x 3))=6`; and
- the two assignments of the differentiated roots give (8).

Therefore the legally isolated coefficient is exactly

```text
6 K(L_i,L_j) J z,                                    (33)
```

where `J` complements the used port pair and `z` is the **same physical
four-window response vector for every root pair**.

For the shared-root control assign `(L_0,L_1,L_2)=(A,B,C)` from (18).  Both
sectors reuse the literal root-0 blocks (32).  For the disjoint control assign
`(L_0,L_1,L_2,L_3)=(A_1,B_1,A_2,B_2)` from (28)--(29); root `4` is common to
the two shores.  In both cases all root vectors are fully supported and
pairwise zero-coupled.

This construction proves that pure shore sharing plus common physical root
data do not force fan-kernel intersection.  It does **not** say that an
arbitrary hypothetical GHZ witness contains either control.

## 6. Consequence and exact remaining boundary

The hoped-for implication

```text
two fans share a root
    => their rank-four defect planes meet nontrivially              (34)
```

is false, even in one legally isolated five-root graph-side coefficient
system.  Under the natural nondegeneracy `det[B;C]!=0`, the correct invariant
is the second-Veronese rank of the four coordinate restrictions to `ker A`.

Any future obstruction must use data absent from this factorization, for
example:

1. the target-normalized mixed GHZ word equations;
2. common principal-hafnian relations among the response faces;
3. unavoidable root--root or root--residual companion columns in an arbitrary
   witness; or
4. a theorem forcing every available fan pair onto the two-direction
   Veronese boundary.

## Scope wall

```text
five-root pair/shore sharing classification:         PROVED;
same-pair polarization gives the same kernel:        PROVED;
shared-root Veronese intersection theorem:           PROVED;
shared-root transverse rank-six pair:                CONSTRUCTED;
shared-root sharp rank-five boundary pair:           CONSTRUCTED;
disjoint-pair rank-six pair with fifth shore root:   CONSTRUCTED;
complete-shore five-root line-family trichotomy:      PROVED;
one common graph-side P7 coefficient realization:    CONSTRUCTED;
all ten shore factors simultaneously nonzero:        CONSTRUCTED;
target GHZ equality for either control:               NOT CLAIMED;
forced two-fan occurrence in every P7 witness:        UNKNOWN;
forced two-direction shared-root boundary:            UNKNOWN;
principal-hafnian and mixed-word compatibility:       UNKNOWN;
P7 nonrestriction:                                    UNKNOWN;
global Krenn--Gu conjecture:                          UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_five_root_two_fan_sharing_and_shared_root_veronese_transversality.py
python claims/p7/audit_p7_five_root_two_fan_sharing_and_shared_root_veronese_transversality.py
python -m py_compile verify_p7_five_root_two_fan_sharing_and_shared_root_veronese_transversality.py audit_p7_five_root_two_fan_sharing_and_shared_root_veronese_transversality.py
uv run --with ruff ruff check verify_p7_five_root_two_fan_sharing_and_shared_root_veronese_transversality.py audit_p7_five_root_two_fan_sharing_and_shared_root_veronese_transversality.py
```

The primary verifier checks the hollow-sandwich reduction, both sides of the
Veronese dichotomy, the shared-root and disjoint rank controls, all shore
permanents, and the frozen/tangent edge-block evaluations.  The independent
no-import audit reconstructs the same certificates with `Fraction` row
reduction, a subset-recurrence permanent, and direct bilinear evaluation.
Neither replay searches any graph, support, word, matching family, or
parameter set.
