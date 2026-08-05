# Two-residual strict-support staircase and coordinate-boundary forcing

## Status

**Exact arbitrary-order characteristic-zero transport theorem.**  Work over
an algebraically closed characteristic-zero field.  Let `r>=2`
fully supported pairwise-zero roots have `m=r+2` blockers, and suppose a
legal contraction leaves exactly two residual nonblockers.  The existing
two-residual theorem says that either the residual edge restricts to a
nonzero coordinate monomial on the two simultaneous-kernel spaces, or one
may choose torus kernel vectors on which its value is zero.  In the latter
case the general two-port cofactor decomposition becomes one synchronized
`P_m` restriction.

Transporting the strict permanent support theorem through that exact
factorization gives

```text
I+p_0+p_1 >= 3m+3 = 3r+9.                             (1)
```

Here `I` counts active contracted root--blocker forms, and `p_0,p_1` count
the two active contracted blocker--residual port-row families at the chosen
torus zero.  In particular, every exactly-two-residual cell satisfies the
sharp alternative

```text
nonzero coordinate-monomial residual restriction,
or
strict active support at least 3r+9.                   (2)
```

There is also a graph-only consequence.  If the original root--blocker and
blocker--residual cut has at most `3r+8` nonzero edge blocks, then the
residual restriction is forced into the coordinate-monomial branch.  For
the second-surplus `P_5,P_6,P_7` cells, the strict lower bounds are
respectively `18,21,24`, and cuts of size at most `17,20,23` force the
coordinate boundary.

For five roots, this completes the exact support staircase

```text
tight P_5:              support at least 18,
one-port P_6:           support at least 21,
two-residual P_7,
  non-coordinate:       support at least 24.           (3)
```

This does not exclude the coordinate-monomial branch.  The existing
coordinate-slice universality theorem realizes every blocker-admissible
surplus-two cofactor datum inside that branch, so (2) is a sharp proof-route
boundary rather than a global Krenn--Gu proof.  No support, graph, word,
matching family, or parameter space is enumerated.

## 1. Exact second-surplus cell

Let

```text
R={r_1,...,r_r},             |B|=m=r+2,
Q={q_0,q_1}.                                           (4)
```

The statement also applies after any legal prior contraction in a larger
ambient graph that leaves precisely this cell.  For each root and blocker,
put

```text
H_u[i,-]=B_(r_i,u)(x_i,-),

I=#{(i,u):H_u[i,-] is not the zero covector}.          (5)
```

At the two residual vertices define the simultaneous-kernel spaces

```text
K_j=intersection_i ker B_(r_i,q_j)(x_i,-),             (6)
```

which are not contained in coordinate hyperplanes because `q_0,q_1` are
residual nonblockers.  Let

```text
beta=B_(q_0,q_1) restricted to K_0 x K_1.              (7)
```

For torus vectors `z_j in K_j`, define

```text
h=beta(z_0,z_1),
a_u=B_(u,q_0)(-,z_0),        b_u=B_(u,q_1)(-,z_1),

p_0=#{u:a_u!=0},             p_1=#{u:b_u!=0}.          (8)
```

The exact matching recursion on `{u,v,q_0,q_1}` is

```text
W_uv=h B_uv+a_u tensor b_v+b_u tensor a_v.             (9)
```

No factorization hypothesis has been imposed: (9) is the specialization of
the general residual-hafnian formula

```text
H_uv=hB_uv+R_u^T C(A)R_v                              (10)
```

to two residual vertices, for which

```text
C(A)=[[0,1],[1,0]].                                   (11)
```

## 2. Torus-zero transport is one honest permanent

The two-residual torus dichotomy is exact:

```text
beta has a zero on K_0^times x K_1^times,
or
beta(z_0,z_1)=lambda z_0[c_0]z_1[c_1]                (12)
```

on `K_0 x K_1`, for some `lambda!=0`.  One-dimensional kernel spaces are
included.  Here `K_j^times` is the complement of its three coordinate
hyperplane sections.

Assume the first alternative and choose a torus zero.  Then `h=0`, so (9)
becomes

```text
W_uv=a_u tensor b_v+b_u tensor a_v.                   (13)
```

The surplus-two cofactor aggregate is

```text
Lambda
 =sum_(u<v) W_uv tensor P_r(H_w:w in B minus {u,v}).  (14)
```

Appending the two common rows `a,b` and expanding the permanent along them
gives the termwise identity

```text
Lambda=P_m(H;a;b),               m=r+2.               (15)
```

Indeed, a full permanent assignment uniquely records the unordered pair of
columns used by `a,b`, their two possible assignments to that pair, and the
root-row bijection onto the remaining columns.  There are no determinant
signs or hidden multiplicities.

The full graph identity makes (14), hence (15), a concise restriction

```text
P_m -> Delta_3                                      (16)
```

with all three diagonal coefficients nonzero: the roots and the chosen
torus residual vectors have all three coordinates nonzero.  The strict
arbitrary permanent theorem now gives at least `3m+3` nonzero row cells.
The rows of (15) are exactly the `r` root families and the two port families,
so its support is

```text
I+p_0+p_1.                                             (17)
```

Equations (16)--(17) prove (1).  The arbitrary-surplus first-polar theorem
also applies to (16) and gives the additional necessary conditions

```text
span{H_u[i,-]:u in B}=(C^3)^*          for every i,
span{a_u:u in B}=span{b_u:u in B}=(C^3)^*.             (18)
```

Thus the two port families are not merely present; each independently has
full target-dual span.

## 3. The coordinate-forcing theorem

### Theorem 1

In every cell satisfying (4)--(8), exactly one of the following conclusions
holds:

1. `beta` is a nonzero coordinate monomial on `K_0 x K_1`;
2. `beta` is not a nonzero coordinate monomial, a torus zero exists, and for
   every chosen torus zero used in the extraction,

   ```text
   I+p_0+p_1>=3r+9,                                   (19)
   ```

   and all row spans in (18) equal the full target dual.

### Proof

The alternatives in (12) are exhaustive.  In the torus-zero alternative,
the proof of Section 2 applies to the chosen zero and gives (19) and (18).
The other alternative is exactly conclusion 1.

The theorem is deliberately stated as a conclusion dichotomy.  A nonzero
coordinate-monomial restriction has no torus zero.  Thus the two cases are
disjoint as well as exhaustive.

### Corollary 2 (graph-cut forcing)

Let

```text
E_cut=e_G(R,B)+e_G(B,{q_0,q_1})                       (20)
```

count nonzero original edge blocks on the displayed cut.  Every active
contracted form requires its underlying edge block, so

```text
I+p_0+p_1<=E_cut.                                     (21)
```

Consequently

```text
E_cut<=3r+8
   implies beta is a nonzero coordinate monomial.      (22)
```

Equivalently, a non-coordinate residual restriction forces

```text
E_cut>=3r+9.                                           (23)
```

This is a cut bound, not a total-edge bound for the ambient graph.  Blocks
outside the extracted root--blocker--residual cut do not occur in (15).

## 4. `P_5/P_6/P_7` transport tables

For the second-surplus ladder `m=r+2`, Theorem 1 gives

| roots `r` | blockers/order `m` | non-coordinate active support | graph cut forcing the coordinate branch |
|---:|---:|---:|---:|
| 3 | `P_5` | at least `18` | at most `17` |
| 4 | `P_6` | at least `21` | at most `20` |
| 5 | `P_7` | at least `24` | at most `23` |

For the fixed five-root blocker-surplus staircase, combine the established
tight and one-port transports with the new second-surplus conclusion:

| five-root cell | extracted permanent | exact necessary support |
|---|---:|---:|
| five tight blockers | `P_5` | `I>=18` |
| six blockers, one port | `P_6` | `I+p>=21` |
| seven blockers, two residual ports, `beta` non-coordinate | `P_7` | `I+p_0+p_1>=24` |

The last row removes the word “conditional” from the synchronized two-port
support transfer precisely on the torus-zero/non-coordinate branch.  It does
not remove it for an arbitrary two-port cofactor whose residual system has
four or more vertices.

## 5. Sharpness and the higher-surplus boundary

Three exact counterboundaries prevent a broader claim.

1. **Coordinate-monomial slice universality.**  For every blocker-admissible
   surplus-two cofactor datum satisfying the diagonal equation, the existing
   torus-line construction gives a legal local edge realization with a
   nonzero coordinate-monomial residual edge.  It preserves arbitrary
   blocker-pair cofactors, and its factorized sector contains every
   all-full-span `P_(r+2)` datum.  Hence the cofactor equation, blocker
   incidence, root-row span, and matching recursion cannot exclude conclusion
   1 of Theorem 1.
2. **Four or more residual vertices.**  On every even residual order `q>=4`,
   there are exact torus-zero matrices with `haf(A)=0` and full-rank
   cofactor matrix `C(A)`.  The corrected pair response can require multiple
   synchronized channels.  A torus zero therefore does not generally turn
   the aggregate into one `P_(r+2)` restriction.
3. **Surplus at least three.**  General joint port forms do not automatically
   factor through common permanent row families.  Full root-row span remains
   necessary, but the strict support theorem cannot be transferred until a
   synchronized factorization, separator collapse, or another target equation
   is proved.

The exact surviving problem is therefore off-slice or cross-depth:

```text
low second-surplus cut
  -> coordinate-monomial residual restriction
  -> require a different root choice, residual direction,
     mixed-colour equation, or deletion-depth compatibility.             (24)
```

## 6. Scope wall

Proved:

- unconditional strict support `I+p_0+p_1>=3r+9` on the exactly-two-residual
  torus-zero branch;
- equivalently, the same strict support on every non-coordinate residual
  restriction;
- full target-dual span of both port-row families there;
- graph-cut coordinate forcing at `E_cut<=3r+8`;
- the `18/21/24` second-surplus `P_5/P_6/P_7` table;
- the five-root `P_5/P_6/P_7` support staircase (3).

Not proved:

- exclusion of the coordinate-monomial residual branch;
- a full global witness from its slice-universal local construction;
- one-channel factorization for four or more residual vertices;
- synchronized factorization for arbitrary surplus at least three;
- a forced qualifying extraction in every hypothetical graph witness;
- unrestricted `P_5`, `P_6`, or `P_7` nonrestriction;
- the global Krenn--Gu conjecture.

```text
two residuals + non-coordinate beta:        STRICT SUPPORT PROVED;
two residuals + cut <=3r+8:                 COORDINATE MONOMIAL FORCED;
coordinate-monomial slice branch:           LOCALLY UNIVERSAL, OPEN GLOBALLY;
four-or-more residual torus-zero branch:     MULTICHANNEL, NO TRANSFER;
higher unfactored blocker surplus:           UNKNOWN;
global Krenn--Gu:                            UNRESOLVED.                 (25)
```

## Replay

```powershell
uv run --with sympy python verify_arbitrary_order_two_residual_strict_support_staircase_and_coordinate_forcing.py
python audit_arbitrary_order_two_residual_strict_support_staircase_and_coordinate_forcing.py
python -m py_compile verify_arbitrary_order_two_residual_strict_support_staircase_and_coordinate_forcing.py audit_arbitrary_order_two_residual_strict_support_staircase_and_coordinate_forcing.py
uv run --with ruff ruff check verify_arbitrary_order_two_residual_strict_support_staircase_and_coordinate_forcing.py audit_arbitrary_order_two_residual_strict_support_staircase_and_coordinate_forcing.py
```

The primary replay checks the exact two-residual recursion, a symbolic
two-row permanent Laplace identity, both sides of the torus dichotomy, the
support transport, and both tables.  The independent audit imports no
project code or computer algebra and separately checks the matching-count
bijection and integer support arithmetic.  The written dichotomy, matching,
and strict-support theorems establish arbitrary order; neither replay
searches supports, graphs, colour words, or parameter families.
