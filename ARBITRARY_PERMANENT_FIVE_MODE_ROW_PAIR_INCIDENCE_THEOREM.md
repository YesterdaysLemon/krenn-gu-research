# Every permanent row pair needs five coordinate-incidence modes

## Status

**Exact arbitrary-order characteristic-zero incidence theorem.**  In every
hypothetical multilinear restriction

```text
P_m -> Delta_3,                    m >= 3,             (1)
```

fix any two source rows.  Their two local covectors span a target coordinate
covector in at least **five** modes.

The committed four-mode theorem proves the lower bound four.  This note
classifies the equality-at-four incidence multihypergraphs symbolically and
excludes all six types using polarized matrix rank.  The argument does not
enumerate mode assignments, supports, mixed words, or graphs.

For `P_7 -> Delta_3`, every selected source-row pair therefore has at most two
modes whose common null space meets the coordinate torus.  This is a necessary
condition, not a proof of `P_7` nonexistence or of the Krenn--Gu conjecture.

## 1. Setup and the polar matrix identity

Let

```text
phi_w:C^3 -> C^m,                 w=0,...,m-1,
r_(w,p)=e_p^* composed with phi_w,
```

and suppose

```text
P_m(phi_0(x_0),...,phi_(m-1)(x_(m-1)))
 =sum_(c=0)^2 lambda_c product_w x_w[c],
lambda_0 lambda_1 lambda_2 !=0.                        (2)
```

Fix distinct source rows `p,q` and put

```text
A_w=span{r_(w,p),r_(w,q)},
K_w=ker r_(w,p) intersection ker r_(w,q),
Z_w={c:e_c^* belongs to A_w},
N_c={w:c belongs to Z_w}.                              (3)
```

The kernel-deletion hierarchy gives

```text
|N_c| >= 2                                             (4)
```

for every colour `c`.  Also `|Z_w|<=2`, because `dim A_w<=2`.

Leave two modes `u,v` free and choose `t_w in K_w` in every other mode.
Expansion of the permanent along rows `p,q` gives the exact polar identity

```text
s_uv D_uv
 =sum_c lambda_c product_(w notin {u,v}) t_w[c]
       e_c^* tensor e_c^*,                             (5)

D_uv=r_(u,p) tensor r_(v,q)+r_(u,q) tensor r_(v,p),   (6)
```

where `s_uv` is the complementary `(m-2)`-by-`(m-2)` permanent.  Indeed,
every contracted mode vanishes on rows `p,q`, so the two free modes must
occupy those rows in either order.

If both `A_u,A_v` have dimension two, write

```text
R_w(x)=(r_(w,p)(x),r_(w,q)(x))^T,
J=[[0,1],[1,0]].
```

Then

```text
D_uv=R_u^T J R_v                                      (7)
```

has rank exactly two: `R_v` is surjective, `J` is invertible, and `R_u^T`
is injective.

## 2. Symbolic classification of equality at four

Assume exactly four modes have nonempty `Z_w`.  A boundary mode is labelled
by either a singleton `{c}` or a doubleton.  Put

```text
x_c = number of singleton modes {c},
y_c = number of doubleton modes missing c,
Y   = y_0+y_1+y_2.                                    (8)
```

Thus `y_0` counts `{1,2}`, and cyclically.  There are four boundary modes,
so the total number of colour incidences is `4+Y`.  Condition (4) gives at
least six incidences, hence

```text
Y in {2,3,4}.                                         (9)
```

The three cases give six and only six multihypergraphs, up to colour
permutation.

### `Y=2`

The degree sum is six, so every colour has degree exactly two.  Since

```text
deg(c)=x_c+2-y_c,
```

we have `x_c=y_c`.  The two partitions of two give

```text
I.   2{12}+2{0},
II.  {12}+{02}+{0}+{1}.                               (10)
```

### `Y=3`

There is one singleton; call it `{0}`.  The quota inequalities are

```text
y_0<=2,                  y_1<=1,                  y_2<=1.
```

Together with `y_0+y_1+y_2=3`, they give either `(1,1,1)` or, up to swapping
colours `1,2`, `(2,1,0)`.  Hence

```text
III. {12}+{02}+{01}+{0},
IV.  2{12}+{02}+{0}.                                  (11)
```

Type IV is essential: its colour degrees are `(2,2,3)`.

### `Y=4`

There are no singletons and

```text
deg(c)=4-y_c>=2,
```

so every `y_c<=2`.  The two partitions of four with largest part at most
two are

```text
V.   2{12}+2{02},
VI.  2{12}+{02}+{01}.                                 (12)
```

This derives the six types from the three possible values of `Y`; it is not
an enumeration of assignments to the four modes.

## 3. The unique size-two neighbourhood obstruction

### Lemma 1

Suppose

```text
N_c={u,v}
```

and no other colour has the same neighbourhood.  If both `A_u,A_v` have
dimension two, then (2) is impossible.

Proof.  For every `w` outside `{u,v}`, the restriction of `e_c^*` to `K_w`
is nonzero.  Choose `t_w in K_w` with `t_w[c]!=0`.  Each other colour `d`
has at least two incidences and `N_d` is not `{u,v}`, so some mode outside
`{u,v}` lies in `N_d`; its `K_w` kills coordinate `d`.  The right side of
(5) is therefore a nonzero rank-one multiple of

```text
e_c^* tensor e_c^*.
```

Equality forces `s_uv!=0`, whereas (7) says `D_uv` has rank two.  This is a
contradiction.

In Types II--VI the lemma applies with endpoints that are doubleton modes,
so their `A` spaces are automatically rank-two coordinate planes:

```text
II:  N_2 is the {12},{02} pair;
III: N_1 is the {12},{01} pair;
IV:  N_1 is the repeated {12} pair;
V:   N_0 is the repeated {02} pair;
VI:  N_0 is the {02},{01} pair.                       (13)
```

Thus Types II--VI are impossible.

## 4. The repeated-pair type also fails

It remains to exclude Type I.  Write

```text
S = the two singleton-{0} modes,
T = the two doubleton-{1,2} modes.
```

Then

```text
N_0=S,                     N_1=N_2=T.                 (14)
```

Leave `S` free and contract its complement with vectors having nonzero
colour-zero coordinate.  Equation (5) has a nonzero rank-one colour-zero
right side.  Consequently the two spaces `A_w`, `w in S`, cannot both have
rank two.  At least one has rank one.  Since its only coordinate incidence
is `0`, that space is exactly

```text
A_a=<e_0^*>,                   K_a={x_0=0}.            (15)
```

Now leave `T` free.  Contract mode `a` with `e_1`.  At the other mode of `S`
and at every nonboundary mode, choose a vector in `K_w` with nonzero
colour-one coordinate; this is possible because `e_1^*` does not belong to
their `A_w`.  The target side of (5) now has:

- colour zero killed by `e_1[0]=0`;
- colour two killed by `e_1[2]=0`;
- colour one nonzero in every contracted mode.

It is a nonzero rank-one multiple of `e_1^* tensor e_1^*`.  But both modes
in `T` have

```text
A_w=<e_1^*,e_2^*>,
```

so their corrected block has rank exactly two by (7).  Contradiction.

### Theorem 2 (five-mode row-pair incidence)

For every source-row pair `{p,q}` in every restriction (2), at least five
local modes satisfy

```text
e_c^* in span{r_(w,p),r_(w,q)}
```

for some target colour `c`.

The proof uses the full family of kernel polar contractions.  If every
`A_w` is already known to have rank two, Type I dies at its first rank-one
slice; the second contraction is needed only to close the possible rank-one
local escape.

## 5. P7 consequence and boundary

For a factorized `P_7 -> Delta_3` candidate and any selected residual
source-row pair, at least five of the seven residual row spans contain a
coordinate covector.  Thus at most two common null spaces meet the
coordinate torus.

The conclusion is intrinsic.  In particular, equality at four is impossible
before imposing the canonical root profile or the three missing-colour pure
conditions

```text
D_(U_c)^(cc) != 0.
```

Not proved here:

- whether the five-mode lower bound is sharp for the full identity;
- classification or exclusion of equality at five;
- nonexistence of `P_7 -> Delta_3`;
- the global Krenn--Gu conjecture.

These remain **UNKNOWN/UNRESOLVED**.

## Replay

```powershell
uv run --with sympy python verify_arbitrary_permanent_five_mode_row_pair_incidence_theorem.py
python audit_arbitrary_permanent_five_mode_row_pair_incidence_theorem.py
uv run --with sympy --with ruff python -m ruff check verify_arbitrary_permanent_five_mode_row_pair_incidence_theorem.py audit_arbitrary_permanent_five_mode_row_pair_incidence_theorem.py
python -m py_compile verify_arbitrary_permanent_five_mode_row_pair_incidence_theorem.py audit_arbitrary_permanent_five_mode_row_pair_incidence_theorem.py
```

The primary verifier checks the six derived normal forms, the five direct
size-two-neighbourhood witnesses, the exact-rank-two port factorization, and
the second polar slice for Type I.  The independent no-import audit repeats
the incidence and matrix-rank checks with exact integer arithmetic.  The
displayed proof, rather than either bounded replay, establishes completeness
of the six-type classification and the arbitrary-order theorem.
