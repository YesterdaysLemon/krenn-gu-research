# Arbitrary permanent equality two-switch excess-plane separation theorem

## Status

This is an exact characteristic-zero theorem for the sole branch in which a
hypothetical `3m+2` equality restriction has two switchable colours.  It uses
only physical-cell incidence, local concision, the equality degree ledger,
and the exact gain equations.  It performs no support, word, or matching
enumeration.

The two noncoordinate excess rows are co-located at one mode `a`.  Their
minor in the two switch-colour directions is nonzero.  Equivalently, the two
switch-colour gain ratios at `a` are distinct.  This separates several
natural pairs of ratio states into different components of every relevant
cancellation graph.

The result rules out the most local proposed gluing obstruction: the two
switch states at `a` can never form a one-switch straddling pair.  This note
alone does not exclude the two-switch equality branch.  A subsequent
opposite-source Hamilton-chord theorem excludes it using additional
permanent coefficients.

## Sharp two-switch ledger

Let `c,d` be the two switchable colours and `e` the third colour.  By the
pure-matching cube theorem, the two excess physical cells have distinct
exceptional sources `p_1,p_2` but the same mode `a`, are both noncoordinate,
and exhaust the nonmandatory cells.  Write them in the `(c,d,e)` basis as

```text
x_1=r_(a,p_1)=(A,C,E_1),
x_2=r_(a,p_2)=(B,D,E_2).                             (1)
```

Both switches use both excess cells, so

```text
A B C D !=0.                                        (2)
```

The sharp degree ledger is

```text
d_a=3,
d_(b_c)=d_(b_d)=4,                                  (3)
```

where `b_c,b_d` are distinct modes supporting the mandatory cross pairs for
the two pure switches.  Thus mode `a` contains exactly one further physical
cell `z`.  It belongs to the mandatory coordinate cover.  Its source is not
`p_1` or `p_2`, whose cells at `a` are already `x_1,x_2`.

## Third-colour lemma

The mandatory cell `z` has colour `e`.

If `z` had colour `c`, each of the two pure colour-`c` matchings would match
mode `a` through one of `x_1,x_2` and omit `z`.  The exceptional-source
localization lemma says that the source of an omitted mandatory colour-`c`
cell must be an exceptional source, because its replacement is one of the
two excess cells.  This contradicts the source observation above.  The same
argument excludes colour `d`.  Therefore

```text
z=alpha e^*,        alpha!=0.                        (4)
```

## Excess-plane minor

Local concision says that the three rows at mode `a` span the full
three-dimensional colour space.  Equations (1) and (4) give

```text
0 != det [ A  C  E_1 ]
         [ B  D  E_2 ]
         [ 0  0  alpha]
   =alpha(AD-BC).                                    (5)
```

Hence

```text
AD-BC !=0.                                           (6)
```

In the ratio variables of the negative-gain theorem,

```text
g_(a,c)=B/A,        g_(a,d)=D/C,                     (7)
```

so (6) is exactly

```text
g_(a,c) != g_(a,d).                                  (8)
```

This is the nonzero Pluecker coordinate of the excess two-plane in the
switch-colour chart.

## Same-mode component separation

Put

```text
v=(a,c),        w=(a,d).                             (9)
```

In a fixed backbone fibre where the selected pure matchings route `v,w` to
the same exceptional source, they lie on the same canonical side.  If they
belonged to one cancellation component, a path between them would have even
length.  Every cancellation edge satisfies `g_x=-g_y`, so propagation along
that path would give `g_(a,c)=g_(a,d)`, contradicting (8).  Therefore

```text
v and w are in distinct cancellation components
in every fibre where they have the same source side. (10)
```

Along an edge of the two-dimensional backbone cube that switches exactly
one of `c,d`, the states (9) have the same source side at one endpoint and
opposite sides at the other.  Condition (10) means they cannot be connected
in both endpoint fibres.  Thus the local pair `(a,c),(a,d)` can never satisfy
the one-switch straddling condition.

## Pure-switch component separation

Let the mandatory colour-`c` cross entries at mode `b_c` be

```text
y_(c,s)=r_(b_c,p_s)[c],       s=1,2.                 (11)
```

The two pure colour-`c` matchings have one common residual factor and local
coefficient

```text
A y_(c,2)+B y_(c,1) !=0.                             (12)
```

All four entries in (12) are nonzero.  Dividing by `A y_(c,1)` gives

```text
g_(a,c)+g_(b_c,c) !=0.                               (13)
```

The two states `(a,c),(b_c,c)` are on opposite canonical sides in every
colour-`c` backbone.  If they were in one cancellation component, an odd
path would force `g_(a,c)=-g_(b_c,c)`, contradicting (13).  Hence

```text
(a,c) and (b_c,c) lie in distinct components
in every backbone fibre.                             (14)
```

The identical argument gives

```text
(a,d) and (b_d,d) lie in distinct components
in every backbone fibre.                             (15)
```

Equations (10), (14), and (15) are route exclusions: a successful gluing
obstruction must connect a switch state to a ratio state away from the common
excess mode.  Cross-colour pairs at `b_c` or `b_d` remain unanalysed.

## Why the nearby imported theories stop here

The rows `x_1,x_2` define a point of `Gr(2,3)`.  Its three `2 x 2` minors are
unconstrained homogeneous coordinates because `Gr(2,3)` is projective
two-space.  There is no quadratic Pluecker relation at this size.  The first
such relation needs four boundary directions.  Thus Grassmannian geometry
proves the open-chart condition (6), not a contradiction.

Nor do the present backbones form a matchgate signature.  After choosing a
nonzero base signature coordinate, matchgate identities require one
deletion-closed family of boundary values represented in the corresponding
compatible Pfaffian chart.  The four backbones here are alternative
pure-colour choices, not external-vertex deletions;
kernel-deletion inequalities do not supply all deleted permanent values;
and coloured copies of one noncoordinate physical cell cannot be treated as
independent edges.  See Cai and Gorenstein,
[*Matchgates Revisited*](https://arxiv.org/abs/1303.6729), and Bravyi,
[*Contraction of matchgate tensor networks on non-planar graphs*](https://arxiv.org/abs/0801.2989).

There is no orientation obstruction from the two known switch rectangles
alone.  On rows `a,b_c,b_d` and columns `p_1,p_2`, the sign pattern

```text
          p_1  p_2
a          +    +
b_c        +    -
b_d        +    -                                  (16)
```

turns each of the two known permanents, on `(a,b_c)` and `(a,b_d)`, into the
negative of its signed determinant.  Requiring the third row pair
`(b_c,b_d)` as well would be impossible: if `tau_i` is the ratio of the two
edge signs in row `i`, every permanent-to-determinant rectangle requires
`tau_i=-tau_j`, which cannot hold for all three pairs in characteristic not
two.  This is only an obstruction to one coherent three-row Pfaffian chart;
it does not make a third bosonic permanent equation inconsistent.  Using the
orientation failure as a contradiction would be circular unless a
deletion-closed matchgate signature were first derived.

The subsequent port-completion shore theorem classifies the direct physical
route to that third rectangle by one residual Hall condition.  It does not
use the determinant-signing obstruction.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_equality_two_switch_excess_plane_separation_theorem.py
python claims/arbitrary-order/audit_arbitrary_permanent_equality_two_switch_excess_plane_separation_theorem.py
```

The primary verifier checks the determinant, gain inequalities, pure-switch
factor, and two-rectangle sign orientation.  The independent no-import audit
repeats those checks with exact rational values and verifies that three
pairwise sign-ratio negations are inconsistent.  These are fixed symbolic
checks; the arbitrary-order proof is the incidence, localization, and path
parity argument above.

## Boundary

```text
coordinate cell at common excess mode:       THIRD COLOUR;
switch-colour excess-plane minor:            NONZERO;
same-mode same-source switch states:         DISTINCT COMPONENTS;
same-colour switch-mode pair:                DISTINCT COMPONENTS;
local same-mode straddling route:            EXCLUDED;
two known rectangles Pfaffianizable:         YES;
direct third-rectangle route:                RESIDUAL HALL DICHOTOMY;
indirect third-rectangle consequence:        UNKNOWN;
deletion-closed matchgate signature:         NOT ESTABLISHED;
two-switch equality stratum:                 EXCLUDED SUBSEQUENTLY;
global Krenn--Gu conjecture:                  UNRESOLVED.
```

See `ARBITRARY_PERMANENT_EQUALITY_TWO_SWITCH_PORT_COMPLETION_SHORE_THEOREM.md`.
