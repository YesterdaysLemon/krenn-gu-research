# Residual-null polar selectors activate the mixed pair determinant

## Status

**Exact characteristic-zero theorem for the factorized `h=0` branch.**
Consider the five-root, seven-blocker permanent identity obtained after the
two residual vertices have been contracted at a torus zero of their mutual
edge.  The two residual port rows then give corrected pair blocks

```text
D_uv=a_u tensor b_v+b_u tensor a_v,        rank D_uv<=2.             (1)
```

There is a legal polarized contraction of the **full `P_7` tensor equation**
that isolates any selected `D_uv` as one scalar multiple.  It contracts the other
five blocker legs in the common null spaces of `a_w,b_w`.  Every competing
pair term vanishes separately.  Thus the determinant circuit is activated by
aggregated mixed-word equations; the six off-diagonal entries of `D_uv` do
not have to be exposed as six individual deletion faces.

The consequence is structural rather than a complete exclusion.  At most
four of the seven common null spaces may meet the target-coordinate torus.
Equivalently, at least three blockers have a residual two-row span containing
a target coordinate covector.

The later
[`ARBITRARY_PERMANENT_FOUR_MODE_ROW_PAIR_INCIDENCE_THEOREM.md`](ARBITRARY_PERMANENT_FOUR_MODE_ROW_PAIR_INCIDENCE_THEOREM.md)
combines this polar slice with the per-colour kernel Hall quotas and rules out
equality at three.  A factorized `P_7` identity therefore has at least four
such blockers.  The theorem below remains the direct determinant activation
from one selected pair.

This theorem applies only after the residual edge has been made exactly
`h=0`.  It does not treat the coordinate-monomial `h!=0` alternative, does
not exclude every factorized `P_7` restriction, and does not prove the global
Krenn--Gu conjecture.

## 1. The factorized `P_7` identity

Let

```text
R={r_0,...,r_4},                 |R|=5,
B={0,...,6},                     |B|=7,
V_w=C^3                          for w in B.                         (2)
```

For every blocker `w`, let

```text
H_(i,w), a_w, b_w in V_w^*,      i in R.                            (3)
```

The five forms `H_(i,w)` are the contracted root rows, while `a_w,b_w`
are the two residual port rows.  For a five-set `S subset B`, define the
multilinear permanent tensor

```text
P_5(H_S)((x_w)_(w in S))
 =per (H_(i,w)(x_w))_(i in R,w in S).                               (4)
```

In the torus-zero branch the exact surplus-two Laplace identity is

```text
sum_({u,v} subset B)
  D_uv tensor P_5(H_(B minus {u,v}))
 =sum_(c=0)^2 d_c e_c^(tensor 7),

D_uv=a_u tensor b_v+b_u tensor a_v,
d_0 d_1 d_2 !=0.                                                       (5)
```

Tensor factors in each summand are placed in their labelled blocker modes.
Equation (5) is the `P_7 -> Delta_3` identity written by Laplace expansion
along the two residual rows.  No support assumption is made.

For every blocker put

```text
K_w=ker a_w intersection ker b_w subset V_w.                         (6)
```

Because two covectors on a three-space have a nonzero common kernel, every
`K_w` is nonzero.

## 2. The residual-null polar selector

Fix a blocker pair `{u,v}` and put

```text
S=B minus {u,v}.                                                       (7)
```

Choose arbitrary nonzero vectors

```text
kappa_w in K_w,                    w in S.                            (8)
```

Contract equation (5) at the five modes in `S`, leaving the `u,v` modes
open.  Define the complementary scalar

```text
s_uv=per (H_(i,w)(kappa_w))_(i in R,w in S).                          (9)
```

### Theorem 1 (exact polar isolation)

The contraction of (5) is the `3 x 3` bilinear-matrix identity

```text
s_uv D_uv
 =sum_(c=0)^2 d_c
    (product_(w in S) kappa_w[c]) e_c tensor e_c.                    (10)
```

Proof.  The summand indexed by `{u,v}` evaluates its complementary
`P_5` tensor to (9), so it gives the left side of (10).  Every other pair
`e!= {u,v}` meets `S`.  If `w in e intersection S`, then

```text
D_(w,j)(kappa_w,x)
 =a_w(kappa_w)b_j(x)+b_w(kappa_w)a_j(x)=0.                            (11)
```

Hence all twenty competing pair terms vanish **termwise**.  On the target,
contracting the five labelled legs simply multiplies the colour-`c` term by
the five coordinates in (10).  This proves the identity.

The selector is an aggregated mixed-word contraction.  In target coordinate
bases, its matrix entries are

```text
C_cd=sum_(alpha:S->{0,1,2})
       (product_(w in S) kappa_w[alpha(w)])
       T_(c,d,alpha),                                                    (12)
```

where `T` is the full seven-leg coefficient tensor in (5).  Thus one uses
nine polarized linear combinations of top `P_7` word equations.  One does
not first recover the six off-diagonal coordinates of a hidden pair face.

### Corollary 2 (determinant activation)

Taking determinants in (10) gives

```text
0=s_uv^3 det D_uv
 =(d_0 d_1 d_2)
   product_(w in S)(kappa_w[0] kappa_w[1] kappa_w[2]).                (13)
```

Indeed, (1) makes `rank D_uv<=2`.  The right side of (10) is diagonal, so
its determinant is the displayed product.  Notice that no nonvanishing
assumption on `s_uv` is needed: if `s_uv=0` while all five `kappa_w` are
torus points, (10) already says that the zero matrix equals an invertible
diagonal matrix.

Consequently the five spaces `(K_w)_(w in S)` cannot all meet the coordinate
torus

```text
(C^*)^3={x:x[0]x[1]x[2]!=0}.                                         (14)
```

## 3. The exact seven-blocker incidence consequence

Call `K_w` **torus-capable** when it contains a vector in `(C^*)^3`.

### Theorem 3 (at most four torus-capable residual null spaces)

In every identity (5), at most four of the seven spaces `K_w` are
torus-capable.

Proof.  If five were torus-capable, choose them as `S`, choose a torus vector
in each one, and let `{u,v}=B minus S`.  The right side of (13) is nonzero,
a contradiction.

For a nonzero complex linear subspace `K subset C^3`,

```text
K does not meet (C^*)^3
 iff K subset {x[c]=0} for some c.                                   (15)
```

One direction is immediate.  Conversely, if `K` is not contained in any of
the three coordinate hyperplanes, the three proper hyperplane sections
cannot cover the complex vector space `K`; choose a point outside their
union.  Applying this to (6) and taking annihilators gives

```text
K_w is not torus-capable
 iff e_c^* in span{a_w,b_w} for some c.                               (16)
```

Therefore Theorem 3 is equivalently the exact coordinate-incidence bound

```text
at least three blockers w have
e_c^* in span{a_w,b_w} for some target colour c.                      (17)
```

This conclusion couples the three target colours simultaneously.  It is the
rank-two polar refinement of checking one target colour at a time.

## 4. Arbitrary root order

The same proof is independent of the number five.  Let `r>=2`, let `B` have
order `r+2`, and suppose the factorized identity

```text
sum_({u,v} subset B)
  D_uv tensor P_r(H_(B minus {u,v}))
 =sum_(c=0)^2 d_c e_c^(tensor (r+2))                                  (18)
```

holds with `D_uv` as in (1) and every `d_c!=0`.  Contract any `r` blocker
modes in their spaces `K_w`.  Only the complementary pair term survives,
and the analogue of (10)--(13) follows.

### Theorem 4 (arbitrary-order three-boundary law)

At most `r-1` of the `r+2` spaces `K_w` are torus-capable.  Equivalently,
at least three blocker modes satisfy (16), at every order.

The constant three comes from leaving two modes open: a two-row permanent
slice has matrix rank at most two, whereas a concise three-colour diagonal
slice has rank three.

## Scope wall

Proved here:

- exact termwise isolation of `D_uv` as the scalar multiple `s_uv D_uv` from the full
  factorized `P_7` word tensor;
- determinant activation by one residual-null polar contraction;
- at most four torus-capable residual common-null spaces in the seven-mode
  branch;
- the equivalent three-blocker coordinate-incidence boundary;
- the arbitrary-`r` version with at least three boundary modes.

Not proved here:

- the coordinate-monomial residual-edge branch `h!=0`;
- exclusion of all factorized `P_7 -> Delta_3` restrictions;
- legal production of `h=0` in the coordinate-monomial alternative;
- the arbitrary-order local-to-global reduction;
- the Krenn--Gu conjecture.

When `h!=0`, the two-port block is

```text
h B_uv+D_uv,                                                        (19)
```

which can have rank three.  Equation (13) therefore cannot be transferred
to that branch without a new argument.

## Replay

```powershell
uv run --with sympy python verify_p7_residual_null_polar_selector_h0_theorem.py
python audit_p7_residual_null_polar_selector_h0_theorem.py
uv run --with sympy --with ruff python -m ruff check verify_p7_residual_null_polar_selector_h0_theorem.py audit_p7_residual_null_polar_selector_h0_theorem.py
python -m py_compile verify_p7_residual_null_polar_selector_h0_theorem.py audit_p7_residual_null_polar_selector_h0_theorem.py
```

The verifier constructs generic symbolic rank-two pair blocks, checks their
determinant identically, checks the twenty-one-term `P_7` contraction ledger
with symbolic residual-null covectors, reconstructs the target determinant
product, and audits the arbitrary-order count.  It performs no support search
or graph enumeration.  The independent no-import audit uses exact integer
arithmetic and a separate contraction/rank calculation.
