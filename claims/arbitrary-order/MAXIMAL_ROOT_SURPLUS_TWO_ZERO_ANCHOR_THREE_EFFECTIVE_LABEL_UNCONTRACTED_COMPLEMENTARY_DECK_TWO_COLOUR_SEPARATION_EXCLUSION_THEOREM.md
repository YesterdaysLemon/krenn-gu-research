# Maximum-root surplus-two zero-anchor three-effective-label uncontracted complementary-deck two-colour separation exclusion

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS52`.  In characteristic zero, at every root order
`r>=3`, no zero-anchor fully swallowed fixed-residual target point has exactly
three effective `GLS39` auxiliary labels.  Together with `GLS48`, every such
point has

```text
|Act|>=4.                                             (1)
```

The proof closes the sole conditional rank-seven normal form left by
`GLS51`.  Before contracting inactive promoted ports, the same physical
port-pair complementary deck is shared by the two off-common-coordinate
diagonal target rows.  The `GLS51` common-coordinate residual lock removes
both residual--port terms from those rows.  One row forces the shared deck to
be the pure word in one colour; the other forces the same nonzero deck to be
the pure word in a different colour.  The inactive-port set is nonempty, so
the two tensors are independent.  This is a contradiction.

The argument is pointwise on every deck-zero, cancellation, incidence-rank,
nuisance-rank, response, divisor, and residual-shore fibre.  It does not
divide by an open-port value, chosen minor, response, or selector.  The only
scalar inversions are the nonzero target coefficient and port-pair deck
scalar already forced pointwise by the complete target.

This theorem raises the activity floor inside the zero-anchor full-swallow
target locus.  It does not force a silent source point into full swallow,
treat four-or-more effective labels, attach raw escape, produce a legal
response/selector/receiver package, handle nonzero anchor, or close the
strategic node.

## Dependencies and provenance

- `GLS21` owns the complete raw pair-labelled promoted decomposition.
- `GLS36` gives the fixed-residual uncontracted target equation and
  `B_Q^anc=im sigma_Q`.
- `GLS39` identifies auxiliary pair labels and effectiveness.
- `GLS48` proves the unconditional three-effective-label floor.
- `GLS49` excludes two residual labels plus one port.
- `GLS51` excludes three promoted ports and proves the common-coordinate
  residual lock in the one-residual/two-port support.

The new step is the two-colour separation of one uncontracted physical
complementary deck.  The focused verifier uses exact symbolic tensor
coefficients.  The independent no-import audit uses a separate sparse word
dictionary and direct coefficient evaluation.

## 1. Exact pre-contraction equation

Fix one `GLS8` chart, one fully supported residual contraction, and suppose
for contradiction that

```text
omega=0,                 |Act|=3.                    (2)
```

The support contains zero, one, or two residual labels.  `GLS49` excludes
two residuals and `GLS51` excludes zero residuals.  It remains only

```text
Act={q_s,u,v},                                      (3)
```

with one residual label and two promoted ports.

Put

```text
I=Uhat-{u,v},              |I|=2r-4>=2.             (4)
```

Every promoted label in `I` is ineffective, so both of its whole-domain
root-incidence maps vanish.  The other residual label is ineffective at the
fixed residual point, so both of its shore vectors vanish and `q=0`.
Consequently the complete `GLS21` equation, after evaluating only the two
residual slots and leaving every promoted port open, has exactly the three
nonzero raw pair coefficients

```text
G_u(z)L_v(w,x_I)+G_v(w)L_u(z,x_I)+M_uv(z,w)H(x_I)
 =sum_(d=0)^2 alpha_d z_d w_d t_d(x_I)r_d.          (5)
```

Here

```text
t_d=(e_d^*)^(tensor I),
```

every `alpha_d` is nonzero, and:

- `L_v` is the residual-evaluated physical deck complementary to
  `{q_s,u}`;
- `L_u` is the residual-evaluated physical deck complementary to
  `{q_s,v}`; and
- `H` is the residual-evaluated physical deck complementary to `{u,v}`.

These are tensors on the indicated open ports, not independent formal deck
variables.  All other raw labels vanish because their root companion is
zero; the top label vanishes because `omega=0`.

Let `1_I` denote evaluation of every port in `I` at
`1=e_0+e_1+e_2`.  Then

```text
lambda_v(w)=L_v(w,1_I),
lambda_u(z)=L_u(z,1_I),
gamma=H(1_I),                                      (6)
```

and (5) becomes exactly the contracted equation used by `GLS51`.

## 2. Off-coordinate diagonal isolation

Apply `GLS51` to (6).  It gives a unique common coordinate `c` such that

```text
lambda_u in K e_c^*,       lambda_v in K e_c^*,
a,b in K e_c,              gamma!=0.                (7)
```

Let `{i,j}={0,1,2}-{c}`.  Since

```text
G_t(x)=a tensor Y_t(x)+X_t(x) tensor b,
```

every value of `G_u,G_v` lies in the coordinate-`c` star

```text
S_c=e_c tensor K^3+K^3 tensor e_c.                  (8)
```

For `d=i,j`, let `rho_d:E->K` select the `(d,d)` matrix coordinate.  Then

```text
rho_d(G_u)=rho_d(G_v)=0.                             (9)
```

Applying `rho_d` to the contracted equation gives the exact whole-domain
identity

```text
gamma rho_d(M_uv(z,w))=alpha_d z_d w_d.             (10)
```

No port coordinate has been selected or inverted in (10).

### Theorem 1 (one deck cannot carry two pure inactive words)

The support (3) is impossible.

#### Proof

Apply `rho_d` to the uncontracted equation (5).  By (9), the two
residual--port terms vanish, leaving

```text
rho_d(M_uv(z,w))H(x_I)
 =alpha_d z_d w_d t_d(x_I).                         (11)
```

Multiply (11) by `gamma` and substitute (10).  Since `alpha_d` is nonzero
and the simple form `z_d w_d` is nonzero, equality in the tensor product
gives

```text
H=gamma t_d.                                        (12)
```

This is denominator-free: equivalently, compare the coefficient of
`z_d w_d` on the two sides after using (10).

For `d=i` and `d=j`, equation (12) gives simultaneously

```text
H=gamma t_i=gamma t_j.                              (13)
```

The inactive set `I` is nonempty by (4), so the two distinct pure word
covectors `t_i,t_j` are linearly independent.  Since `gamma!=0`, (13) is
impossible. `square`

The contradiction uses the same named physical deck `H` in both coefficient
rows.  Replacing it by two unrelated rowwise deck variables would change the
physical source equation and invalidate the argument.

## 3. Exhaustive three-label exclusion

### Corollary 2 (universal four-effective-label floor)

Every characteristic-zero zero-anchor fully swallowed fixed-residual target
point at arbitrary root order satisfies

```text
|Act|>=4.                                            (14)
```

#### Proof

`GLS48` gives `|Act|>=3`.  Under equality, the number of residual labels in
the support is two, one, or zero.  `GLS49` excludes two, Theorem 1 excludes
one, and `GLS51` excludes zero. `square`

The exact frontier is now

```text
zero-anchor full swallow with <=3 effective labels:       EMPTY;
zero-anchor full swallow with >=4 effective labels:       OPEN;
zero-anchor nuisance ranks below five:                    EMPTY (GLS39/47);
rank-five through rank-nine four-label target cells:      OPEN;
silent source necessarily enters full swallow:           UNKNOWN;
raw escape supplies an original legal target package:    NOT SUPPLIED;
nonzero-anchor marginal/double-transverse branches:       OPEN;
response/activity/synchronization/nuisance/anchor gates:  OPEN;
arbitrary-root strategic-node closure:                    UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

The `GLS51` exact rank-seven shared-interface control remains a valid warning:
after evaluating all inactive ports at `1`, it satisfies the contracted
equation.  The present theorem proves precisely why it cannot lift to the
uncontracted target: its one scalar `gamma` would have to come from a deck
tensor equal to two different pure inactive-port words.

The smallest zero-anchor full-swallow continuation is therefore a
support-free, target-coupled treatment of four-or-more effective labels, not
another kernel profile or a rank-seven principal-deck search at one
contraction.

## Verification boundary

The focused verifier replays the three surviving raw labels, contraction of
the full deck tensors, both off-coordinate projections, and exact
two-colour tensor separation for every nonempty inactive set.  It is a
symbolic identity replay, not the prose proof.

The independent audit imports no project code or algebra package.  It uses
sparse word dictionaries and evaluates the two forced deck identities on
opposite pure inactive words.  The written proof carries the arbitrary-root
theorem.

Neither checker proves a four-label exclusion, source-to-swallow coverage,
raw-escape attachment, a response/selector gate, node closure, or the global
conjecture.
