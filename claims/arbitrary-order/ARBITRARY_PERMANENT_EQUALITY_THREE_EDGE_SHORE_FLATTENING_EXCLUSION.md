# Arbitrary permanent equality three-edge shore flattening exclusion

## Status

This is an exact arbitrary-order exclusion of the `(1,1,1)` Hall shore in
the two-switch no-completion branch.  It uses one full-support tight-cut
Laplace expansion and a rank-three target flattening.  It performs no
support, word, or matching enumeration.

The two switch-colour shore ports end at the same outside source `q`.
Consequently their complement minors are literally identical, so the full
permanent flattening across the shore has rank at most two.  The corresponding
flattening of `Delta_3` has rank exactly three.  This contradiction excludes
the shore over any field where the three target coefficients are nonzero;
in particular it applies in characteristic zero.

## Shore data

Use the no-completion notation from the port-completion shore theorem.  Let
`S` be the minimal deficient residual mode set and `T=N_R(S)`, with

```text
|T|=|S|-1.                                           (1)
```

For cut type `(1,1,1)`, exactly one third-colour port mode lies in `S`.  The
three coloured shore cells are

```text
e_c=(u_c,q),
e_d=(u_d,q),
e_e=(u_e,p_j)                                        (2)
```

for one `j in {1,2}`.  The first two cells have different shore modes but
the same outside source `q`.

## The cut is tight for the full physical support

Every mode in `S` is residual: it lies outside the common excess mode and
both degree-four switch modes.  It is coordinate-only, has degree three, and
its three physical cells are exactly its three backbone cells.  Thus there
are no additional physical cells leaving `S`.

Here the last assertion uses the preceding port theorem, not degree counting
alone.  The exceptional mandatory `c,d` cells lie at `b_c,b_d`, while the
pure third-colour matching uses `a--e--q`; its exceptional mandatory cells are
therefore precisely the two named residual `e`-ports.  All other residual
cells are nonexceptional mandatory coordinate cells.

For each colour `h`, the restriction

```text
M_h:S-{u_h} -> T                                     (3)
```

is a bijection.  Every source in `T` is nonexceptional, so its three
mandatory coordinate cells are exactly its incoming backbone cells.  There
are no additional physical cells entering `T` from outside `S`.

Therefore the full physical cut of `W=S union T` consists exactly of (2),
all directed from shore modes to outside sources.  Every perfect matching
must cover all `|T|=|S|-1` internal sources from `S`, because no outside mode
can enter `T`.  Exactly one shore mode is left, and it must use exactly one
cell in (2).  Hence every full permanent monomial crosses the cut once.

This is a genuine full-support tight cut, not merely a statement about the
three selected pure matchings.

## Exact Laplace factorization

For a cut cell `z=(u,v)`, define the shore polynomial

```text
L_z(X_S)=r_(u,v)(X_u)
         per(A[S-{u},T]),                            (4)
```

where `A` is the full row-cell matrix after applying the local input maps.
Define the complementary minor

```text
O_v(X_(bar S))
  =per(A[bar S, P-(T union {v})]).                   (5)
```

Partition every permanent term by its unique cut cell.  Equations (2),
(4), and (5) give the literal identity

```text
P_m=L_(e_c) O_q+L_(e_d) O_q+L_(e_e) O_(p_j)
   =(L_(e_c)+L_(e_d)) O_q+L_(e_e) O_(p_j).           (6)
```

The equality of the first two complement factors is exact: after either
the colour-`c` or colour-`d` port occupies source `q`, the outside modes see
the same remaining source set.  Their different port weights and input
variables already belong to the shore factors in (4).

Equation (6) is a sum of two decomposable tensors across the mode partition

```text
{modes in S} | {modes outside S}.                    (7)
```

Thus the flattening rank of the restricted permanent across (7) is at most
two.

## Target rank contradiction

The diagonal target has flattening

```text
Delta_3=sum_(r=0)^2 lambda_r
  (product_(i in S) x_i[r]) tensor
  (product_(i notin S) x_i[r]).                      (8)
```

Both mode sets in (7) are nonempty.  The deficient set `S` is nonempty, and
its complement contains the three deleted modes `a,b_c,b_d`.  On each side,
the three pure coordinate monomials in (8) are linearly independent.  Since
all `lambda_r` are nonzero,

```text
flattening rank of Delta_3 across (7)=3.              (9)
```

Equations (6) and (9) contradict the assumed equality restriction.  Hence

```text
connected no-completion shore (1,1,1): IMPOSSIBLE.   (10)
```

Connectedness is supplied canonically by minimal Hall deficiency, but the
rank proof itself applies to any full-support shore with the three-port,
two-outside-source boundary (2).

## Literature translation

This is tensor-network bond-dimension compression arising from a matching
tight cut.  The equality support theorem makes the physical boundary exact;
ordinary Laplace expansion then identifies two boundary states because they
occupy the same outside source.  In tensor language, the shore bond has only
two distinct complement states, while the Schmidt rank of `Delta_3` across
every nontrivial factor partition is three.

The argument is elementary but is the desired local-to-global bridge: it
packages all mixed coefficient equations at the shore simultaneously rather
than inspecting their monomials one at a time.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_equality_three_edge_shore_flattening_exclusion.py
python claims/arbitrary-order/audit_arbitrary_permanent_equality_three_edge_shore_flattening_exclusion.py
```

The primary verifier checks the two-complement factorization and its matrix
rank against the diagonal rank-three target.  The independent no-import
audit repeats the rank calculation by exact minors and checks the tight-cut
cardinality.  These are fixed symbolic checks; the arbitrary-order proof is
the full-support argument above.

## Boundary

```text
full physical shore cut:                 EXACTLY THREE CELLS;
crossing count per perfect matching:     EXACTLY ONE;
distinct complement minors:              TWO;
shore flattening rank:                   AT MOST TWO;
target flattening rank:                  EXACTLY THREE;
(1,1,1) no-completion shore:             EXCLUDED;
(1,1,3) no-completion shore:             NOT ADDRESSED HERE;
residual completion branch:              NOT ADDRESSED HERE;
two-switch equality stratum:             UNRESOLVED;
global Krenn--Gu conjecture:              UNRESOLVED.
```
