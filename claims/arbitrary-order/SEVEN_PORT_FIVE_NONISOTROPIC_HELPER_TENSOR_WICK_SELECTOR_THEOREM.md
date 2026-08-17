# Seven-port five-nonisotropic-helper tensor Wick selector

## Status

**Exact characteristic-zero coefficientwise tensor-supply theorem on a
seven-port physical response branch.**  Fix one same-`Q`, `h=0` physical
two-residual response on seven ports.  For any requested coefficient of one
direct pair block, suppose that each of the other five ports has a chosen
coefficient whose residual two-vector is nonisotropic.  Then the requested
coefficient is a constant graph-dependent linear combination of attached
four-port response coefficients:

- at most twenty-one rows when both requested endpoint vectors are nonzero;
- at most six rows when exactly one endpoint vector is zero;
- one row when both endpoint vectors are zero.

Consequently, if every port has at least one nonisotropic coefficient, all
nine coefficients of all twenty-one direct pair blocks are recovered from
the thirty-five four-port tensors on that seven-set.  This is a finite tensor
word cover, not merely one scalar nonzero minor.

Legal constant same-`Q` attachment of every used four-port tensor is an
input.  The coefficientwise inverse is downstream of that attachment and
cannot manufacture it.  The theorem does not attach a six-port response,
force a hypothetical witness onto this branch, display a mixed target
coefficient, or restrict a permanent.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

The scalar support classification used below is
[`GLD8`](GLOBAL_SQUARE_FREE_PHYSICAL_WICK_SUPPORT_UNION_CLASSIFICATION_AND_COMMON_ROW_SELECTOR_THEOREM.md).

## 1. Physical coefficient words

Let `K` have characteristic zero.  At a port `i` and ternary coefficient
`c`, write the two residual incidences as

```text
v_(i,c)=(a_(i,c),b_(i,c)) in K^2.                       (1)
```

Use the hyperbolic form

```text
J((a,b),(a',b'))=ab'+ba'.                              (2)
```

Thus, for a coefficient word `alpha`,

```text
K_ij[alpha_i,alpha_j]
 =J(v_(i,alpha_i),v_(j,alpha_j))
 =a_i b_j+b_i a_j.                                     (3)
```

A coefficient vector is **bi-supported in the fixed residual factorization**,
or equivalently nonisotropic for the fixed physical form `J`, exactly when

```text
J(v_(i,c),v_(i,c))=2a_(i,c)b_(i,c)!=0.                 (4)
```

The scalar support proof uses one fixed factorization.  The equivalent
nonisotropy condition is preserved by residual-frame changes in `O(J)`; it
is not a license to change factorization between coefficient words.

On the `h=0` branch, the scalar coefficient of a four-port response is

```text
z_X[alpha_X]
 =sum_(P subset X, |P|=2) K_(X-P)[alpha_(X-P)]
                              B_P[alpha_P].             (5)
```

For a fixed seven-word this is the square-free Wick map

```text
mu_(K,alpha):A(W)_2 -> A(W)_4.                          (6)
```

All coefficients below may depend on the fixed graph, `Q`, residual frame,
and word.  They are fixed before the attached target values are inspected.

## 2. Five-helper coordinate theorem

Let

```text
W={u,v} disjoint-union H,             |H|=5.           (7)
```

Fix arbitrary requested endpoint colours `c_u,c_v`.  For every helper
`i in H`, choose one colour `h_i` satisfying

```text
a_(i,h_i)b_(i,h_i)!=0.                                  (8)
```

Let `alpha` use `c_u,c_v` at the endpoints and `h_i` at the helpers.

### Theorem 1 (bounded requested-coordinate selector)

The coordinate

```text
B_uv[c_u,c_v]                                           (9)
```

is determined by the thirty-five rows (5) on `W`.  More precisely:

1. if both endpoint vectors are nonzero, it has a selector supported on at
   most twenty-one four-port rows;
2. if exactly one endpoint vector is zero, it has a selector supported on at
   most six four-port rows, all containing the zero endpoint;
3. if both endpoint vectors are zero, it has a one-row selector.

### Proof

For the chosen word, put

```text
S_a={i:a_i!=0},       S_b={i:b_i!=0},
V=S_a union S_b.                                           (10)
```

Every helper belongs to both `S_a` and `S_b`.

If both endpoint vectors are nonzero, then

```text
|S_a|>=5,       |S_b|>=5,       |V|=7.                   (11)
```

The exhaustive `GLD8` support-union criterion makes the full
`35 x 21` map (6) injective.  Select twenty-one independent rows and invert
that square minor.  One inverse row recovers (9), with support at most
twenty-one.

Suppose exactly one endpoint, say `u`, has zero residual vector.  Let
`V=W-{u}`.  The six pair columns containing `u` form the outside-degree-one
block

```text
A(V)_1 -> A(V)_3,
m |-> ell_a ell_b m.                                    (12)
```

Both linear forms have support at least five on `V`.  Multiplication by one
is injective from degree one to degree two once its support has size three;
multiplication by the other is injective from degree two to degree three at
support five.  Hence (12) is an injective `20 x 6` matrix.  Six independent
rows, all corresponding to four-sets containing `u`, recover every star
coordinate and in particular (9).

Finally suppose both endpoint vectors vanish.  Some helper edge `pq` has
`K_pq!=0`.  Indeed, if every helper edge vanished, divide by the nonzero
`b_i b_j` and put `t_i=a_i/b_i`.  Then `t_i+t_j=0` for every distinct
`i,j`.  Three helpers give `2t_i=0`, contradicting (8) in characteristic
zero.  In the row `X={u,v,p,q}`, every term in (5) except the requested one
has a `K`-edge incident to `u` or `v`.  Therefore

```text
z_(uvpq)[c_u,c_v,h_p,h_q]
  =K_pq[h_p,h_q] B_uv[c_u,c_v],                          (13)
```

which is the promised one-row selector. `square`

The last case is also a sharp warning: full scalar-map injectivity is
sufficient but not necessary for one coordinate to have a selector.

## 3. Full tensor cover on seven ports

### Corollary 1.1 (all direct pair tensors)

Assume that every port `i in W` has at least one colour `h_i` with

```text
J(v_(i,h_i),v_(i,h_i))!=0.                              (14)
```

For a requested pair `{u,v}`, use the fixed helper colours at the other five
ports and let the endpoint colours range independently over `0,1,2`.
Theorem 1 recovers all nine coefficients of `B_uv`.  Repeating this for the
twenty-one pairs recovers

```text
{B_uv: {u,v} subset W}                                 (15)
```

as complete ternary tensors.

At most `21*9=189` coefficient words are used, one for each requested tensor
coordinate.  Each uses only four-port rows inside the same seven-set.  Once
the thirty-five `z_4` tensors are legally attached, their coefficient rows
are already available; the word cover does not require separate upstream
attachment for each word.

The recovered physical pair blocks determine the complete residual-absent
matching deck on `W` by the perfect-matching recurrence.  This does not imply
that independently observed higher response rows agree with the recurrence
unless their legal same-graph attachment is also established.

### Corollary 1.2 (pair-diagonal entry criterion)

For each port, assemble its three residual coefficient vectors into

```text
V_i=(v_(i,0),v_(i,1),v_(i,2)):K^3 -> K^2.             (16)
```

Suppose every pair channel

```text
D_ij=V_i^T J V_j                                       (17)
```

is diagonal in the same ternary basis.  If two ports have `rank V_i=2` and
no port has rank zero, then all seven ports satisfy the helper hypothesis
(14).  Hence, after legal attachment of the thirty-five `z_4` tensors,
Corollary 1.1 recovers every direct pair tensor.

### Proof

Let `p,q` be two rank-two ports.  The map
`V_p^T J V_q` has rank two, and by hypothesis it is a rank-two diagonal
matrix.  Its left and right kernels are the kernels of `V_p` and `V_q`;
therefore both are the same coordinate axis.  Thus `p,q` have one common
missing colour and two active colours, say `0,1`.

Choose any third nonzero port `r`, and call the active colours `c,d`.  If it
has rank two, `D_pr,D_qr` are rank-two diagonal matrices with the same
missing index.  The vector `r_c` is orthogonal to both `p_d,q_d`, so those
two lines coincide; `r_d` similarly aligns `p_c,q_c`.  The cross entries of
`D_pq` make the two common lines orthogonal.

If `r` has rank one, then `D_pr` has rank one because `V_p^T J` is injective.
A rank-one diagonal matrix has exactly one nonzero diagonal position, say
`c`.  Hence `r_j=0` for `j!=c`, and `c` is one of the two active colours.
The vector `r_c` is orthogonal to both `p_d,q_d`, so their lines coincide.
The equations `D_pq(c,d)=D_qp(c,d)=0` then put both `p_c,q_c` in the
perpendicular of that common `d`-line, aligning the other active line.

For every later port `s`, rank two gives the same missing colour by the
kernel argument, and `D_ps` puts its active columns on the two common lines.
If `s` has rank one, `D_ps` is a rank-one diagonal matrix; thus `s` has
exactly one nonzero active colour and its vector lies on the corresponding
common line.  The two common lines are orthogonal and distinct.
Neither can be isotropic, because an isotropic line in a nondegenerate
two-plane equals its own perpendicular.  Every port therefore has a
nonisotropic coefficient. `square`

The rank and nonzero-port hypotheses are structural inputs.  Pair
diagonality by itself does not force them.

### Corollary 1.3 (observable diagonal-pair entry route)

Assume the `h=0` pair channels `D_ij=K_ij` are diagonal.  If

1. one displayed diagonal pair tensor `D_pq` has matrix rank two; and
2. every port is incident to at least one nonzero `D_ij`,

then the helper hypothesis (14) holds on all seven ports.  Consequently,
after legal attachment of the thirty-five four-port tensors, the full
189-coordinate direct pair deck is supplied.

Indeed, `rank D_pq=2` forces both `V_p,V_q` to have rank two.  A nonzero
incident `D_ij=V_i^T J V_j` forces `V_i!=0`, so condition 2 excludes every
rank-zero port.  Corollary 1.2 applies.

Thus failure of this observable entry route is contained in the union of

```text
some port is isolated in the nonzero pair-response support graph;
every diagonal pair response has rank at most one.        (17a)
```

This containment is not an if-and-only-if obstruction: either residual
branch may still admit different coordinate selectors.

## 4. Sharp support boundaries

Five helpers cannot be uniformly replaced by four.  On six ports split

```text
A={1,2,3},          B={4,5,6}.                         (18)
```

Give every port one active nonisotropic coefficient, with the `A` vectors on
one nonisotropic line and the `B` vectors on its perpendicular line.  The
six-port scalar Wick map has rank ten and nullity five.  In particular the
cross rectangle

```text
m_14-m_15-m_24+m_25                                  (19)
```

lies in its kernel, so no coordinate occurring in that rectangle has a
selector on that word.

Target diagonality alone also does not force the seven-port helper branch.
Give ports `1,...,5` one common active nonisotropic colour and make the
residual coefficient vectors at ports `6,7` zero.  The resulting `z_2=K` is
diagonal.  On the first five ports,

```text
m_12+m_34-m_13-m_24                                  (20)
```

is a nonzero union-five Wick kernel, so it gives `z_4=0`.  This is a physical
response control, not a hypothetical witness.  It proves that a continuation
must force the helper/rank hypotheses, use coordinate-specific singular-word
selectors, or attach a deeper detector.

Finally, a one-active full seven-port response satisfies the helper theorem
but need not produce any mixed depth-six coefficient.  Take
`v_(i,0)=(1,1)` at every port, set every other colour vector to zero, put
`B_ij(0,0)=c K_ij(0,0)`, and set every other `B` coefficient to zero.  For
`c!=0` the pure four-port response is nonzero, while every matching and
response layer is supported only on the all-zero word.  Tensor supply is not
itself a mixed deeper-response detector.

## 5. Response and target interface

Assume one fixed graph, one residual pair `Q`, one residual frame, and legal
constant graph-equation selectors for every `z_4` tensor used above.  Apply
those selectors first.  Coefficient extraction followed by the fixed
linear combinations from Theorem 1 is then another constant `K`-linear
operation.  No coefficient is selected because its observed value happened
to be diagonal.

The helper colours may vary from port to port and from one requested pair to
another.  The graph, `Q`, contractions, and normalization may not vary.  The
result covers all thirty-five `K_4` subwindows of one named seven-port union;
it is not an arbitrary all-subwindow atlas.

A factorization or support test can be performed using the fixed graph
channel `K`.  The theorem does not use a rational function of open port
coordinates.  Its graph-dependent constants are downstream of legal target
attachment, exactly as in `GLD6` and `GLD8`.

## 6. Frontier and UNKNOWN remainder

```text
five nonisotropic helpers select one tensor coordinate:  PROVED;
both-nonzero endpoint bound:                              <=21 rows;
one-zero endpoint bound:                                  <=6 rows;
two-zero endpoint bound:                                  1 row;
one nonisotropic coefficient at every port gives cover:  PROVED;
two full frames + no zero port + pair diagonality:        IMPLIES COVER;
one rank-two D edge + no isolated response port:          IMPLIES COVER;
all 21 direct pair tensors on the named seven-set:        PROVED CONDITIONAL;
four helpers suffice uniformly on six ports:              FALSE;
target diagonality forces the helper branch:               FALSE;
legal attachment of the 35 four-port tensors:             UNKNOWN;
helper nonisotropy forced on hypothetical witnesses:      UNKNOWN;
seven-port coefficient-pure mixed detector:               UNKNOWN;
legal six-port/deeper-response attachment:                 UNKNOWN;
weighted permanent attachment:                            UNKNOWN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

The breadth is every four-subwindow of one seven-port union.  The depth is
the residual-present four-port response layer, with the fixed residual pair
channel `K` as structural input.  The reconstructed object is the complete
residual-absent direct pair tensor deck and hence its matching recurrence.
There is no transition gauge because all rows belong to one graph and one
`Q`.  The ambiguity object is the kernel projection to the requested
coordinate, which Theorem 1 proves zero.  The target implication is
conditional tensor supply after legal attachment; the permanent implication
is none.

## Verification boundary

Run from repository root:

```powershell
python claims/arbitrary-order/verify_seven_port_five_nonisotropic_helper_tensor_wick_selector.py
python -I claims/arbitrary-order/audit_seven_port_five_nonisotropic_helper_tensor_wick_selector.py
```

The primary verifier checks exact `35 x 21`, `20 x 6`, and one-row controls,
including all nine endpoint types.  The independent no-import audit rebuilds
the coefficient maps with `fractions.Fraction` and separate elimination.
These programs audit the bounded matrices; the support proof is load-bearing.
