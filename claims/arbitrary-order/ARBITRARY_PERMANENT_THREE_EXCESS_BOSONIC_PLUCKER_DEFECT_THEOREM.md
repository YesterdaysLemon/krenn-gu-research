# The bosonic Plucker defect and the conformal `K_3,3` boundary

## Status

**Exact characteristic-zero identity, exact six-token structural
countermodel, and a conditional Pfaffian exclusion.**  Translating the
minimal theta into matchgate language reveals one missing term rather than a
new automatic identity.  For a `3 x 3` permanent, the Grassmann--Plucker
relation acquires a quartic **bosonic defect**.  The bare theta kills this
defect, while its two completing chords support it.

There is an exact `m=6`, `21`-cell support satisfying the support ledger,
matching-coveredness, local rank three, pure backbones, a conformal theta,
and the exact `3+3` replay budget in which both chords occur and the defect is
nonzero.  It is a structural boundary model, not a full
`P_6 -> Delta_3` restriction.

The later Hamming-face pinch theorem proves exactly why it cannot become one:
the bypass survives the central and all distance-one equations, but any
two-row selector flip isolates a forbidden nonzero diagonal monomial.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_HAMMING_FACE_PINCH_THEOREM.md`.

## The bosonic Plucker identity

Let `X=(x_ij)` be a `3 x 3` matrix and write

```text
P_ij=per X_(row i and column j deleted).
```

Direct polynomial expansion gives

```text
per(X) x_33
  = P_11 P_22 + P_12 P_21
    - 2 x_13 x_23 x_31 x_32.                       (1)
```

The final monomial is the bosonic Plucker defect

```text
D_12;12(X)=2 x_13 x_23 x_31 x_32.                 (2)
```

The factor `2` is essential in characteristic zero: two permanent monomials
coalesce where the alternating Pfaffian expansion would cancel them.  Row
and column relabelling gives the other eight anchor versions of (1), one for
each choice of surviving entry `x_rc`.

For the canonical theta between row vertices `1,2,3` and column vertices
`1,2,3`, the two completing chords are `x_23` and `x_32`.  On the bare theta,
both vanish and (1) becomes the defect-free condensation identity.  When
both chords are eligible, no support argument forces (2) to vanish.

## Exact non-spinorial bypass

Over `Q(sqrt(2))`, take

```text
X = [ 1,        1, 1-sqrt(2) ]
    [ -1,       1,           1 ]
    [ 1+sqrt(2),-1,           1 ].                 (3)
```

Then

```text
per(X)=P_11=P_22=P_33=0,
P_12=P_21=sqrt(2),
D_12;12(X)=2.                                      (4)
```

Thus (1) reads `0=2-2`.  The corresponding defect-free matchgate equation
would read `0=+/-2`, so no sign convention can remove this surviving product.
Equation (3) is an exact non-spinorial certificate, not a numerical sample.

## Exact six-token completion

Use modes `a_i,b_i` and sources `p_i,q_i`, with all indices modulo three.
Take the cells

```text
a_i p_j                  for all i,j,               (9 cells)
a_i q_i, b_i p_i,
b_i q_i, b_i q_(i+1)     for all i.                (12 cells) (5)
```

There are `21=3*6+3` cells.  Their degrees are

```text
deg(a_i)=deg(p_i)=4,
deg(b_i)=deg(q_i)=3.                                (6)
```

Hence the degree excess is exactly three on each shore, located at the
vertices `a_i` and `p_i`.  Declare the excess cells to be

```text
E_i=a_i p_i.                                        (7)
```

Inside the complete `a`-to-`p` block, the seven cells

```text
E_0, a_0p_1, E_1, a_1p_0, a_0p_2, E_2, a_2p_0     (8)
```

form the minimal theta with branch vertices `a_0,p_0`.  Its complement is
the `b`-to-`q` six-cycle and has the perfect matching `{b_iq_i}`.  Both
completing chords

```text
a_1p_2,                  a_2p_1                    (9)
```

are present.  Together, the theta and its chords are a conformal `K_3,3`.

The support is connected and matching-covered.  This has a direct witness
proof, requiring no matching census:

- every `a_i p_j` extends by a `K_3,3` perfect matching together with
  `{b_iq_i}`;
- the two `b`-to-`q` perfect matchings cover every outer-cycle cell;
- `a_iq_i` and `b_ip_i` extend together with
  `{a_jp_j,b_jq_j:j!=i}`.

## Colour and coefficient structure

Give the 18 mandatory cells the colours

```text
a_i p_j, i!=j : i,          a_iq_i       : i+1,
b_i p_i         : i,        b_iq_i       : i+2,
b_i q_(i+1)     : i+1,                              (10)
```

and give each excess cell `E_i` full colour support.  Every source has
exactly one mandatory cell of each colour.  Local rank is three at every
mode.  Explicit pure colour-`c` perfect matchings are

```text
{a_(c-1)q_(c-1), b_(c-2)q_(c-2), b_(c-1)q_c,
 b_c p_c, a_c p_(c-1), E_(c+1)}.                  (11)
```

For the mixed word

```text
w(a_i)=i,                    w(b_i)=i+2,            (12)
```

the eligibility graph is exactly the full `a`-to-`p` `K_3,3` plus the
forced matching `{b_iq_i}`.  Put the matrix (3) on the `a`-to-`p` block and
unit weights on the forced matching.  The mixed coefficient is exactly
`per(X)=0`, and the three diagonal complementary permanents also vanish.
The two chord sectors supply precisely the defect that permits this
cancellation.

## Pfaffian and matchgate translation

Matchgate identities are necessary and sufficient for planar-matchgate
signatures; see Cai and Gorenstein,
[*Matchgates Revisited*](https://arxiv.org/abs/1303.6729).  Kuo's graphical
condensation identities similarly concern perfect matchings in plane
bipartite graphs; see
[*Applications of Graphical Condensation for Enumerating Matchings and
Tilings*](https://arxiv.org/abs/math/0304090).

The present eligibility graph is outside that regime for an exact graph
reason.  Little's bipartite characterization, recalled by Little, Rendl, and
Fischer in
[*Towards a characterisation of Pfaffian graphs*](https://arxiv.org/abs/math/9909026),
says that a bipartite graph is Pfaffian exactly when it has no conformal even
subdivision of `K_3,3`.  Here (8)--(9) form `K_3,3` itself and the complement
has a perfect matching.  Consequently, if the seven theta cells are eligible
and their exterior complement has a word-eligible perfect matching,

```text
coefficient eligibility graph Pfaffian
    => the two completing chords cannot both be eligible.       (13)
```

But the six-token theorem does not imply Pfaffianity: (5) is already a
non-Pfaffian six-token model.

There is also a precise limit on trying to recover an identity by summing
matchgate channels.  Six-terminal even matchgate signatures lie on the
pure-spinor variety `S_6^+` in `P^31`.  Galgano records that its second secant
fills the whole ambient space,

```text
sigma_2(S_6^+)=P^31;
```

see [*Identifiability and singular locus of secant varieties to spinor
varieties*](https://arxiv.org/abs/2302.05295).  Therefore membership in a sum
of two spinorial channels alone cannot imply any nonzero universal
polynomial identity on the six-terminal signature.  This is a Zariski-level
statement; it does not claim a canonical two-channel decomposition for the
present permanent gadget.

Finally, the six replay tokens are endpoint-use multiplicities, not six
canonically distinct Boolean dangling edges.  A Holant or spinor contraction
therefore supplies no identity until a Pfaffian orientation, planar terminal
order, or matchgate-realizable basis is proved independently.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_three_excess_bosonic_plucker_defect_theorem.py
python claims/arbitrary-order/audit_arbitrary_permanent_three_excess_bosonic_plucker_defect_theorem.py
```

The primary verifier expands (1) symbolically, checks (3)--(4) exactly in
`Q(sqrt(2))`, and verifies all support, witness-matching, colour, pure
backbone, theta, replay, and eligibility claims.  The independent no-import
audit reconstructs the quadratic-field arithmetic, pure-matching templates,
theta support, and replay count.  Neither script enumerates a family of
supports or matching quadruplets.

## Boundary

```text
bosonic Plucker identity (1):              PROVED IN CHARACTERISTIC ZERO;
bare-theta defect:                         ZERO;
two-chord defect forced zero:              FALSE;
six-token two-chord structural model:      EXISTS AT m=6;
model coefficient cancellation:            EXACT OVER Q(sqrt(2));
eligibility graph Pfaffian:                 FALSE IN THE MODEL;
Pfaffian plus conformal eligible theta excludes
  simultaneous two-chord completion:          TRUE;
six tokens imply Pfaffian eligibility:      FALSE;
two spinor channels give an identity:       FALSE IN GENERAL;
full mixed-equation counterexample:         NOT CLAIMED;
exclusion of support 3m+3:                  NOT PROVED;
global Krenn--Gu conjecture:                UNRESOLVED.
```
