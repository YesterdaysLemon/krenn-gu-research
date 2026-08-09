# Every lower mixed root jet forces an exact complementary-cofactor frame

## Status

**Exact arbitrary-order characteristic-zero necessity theorem.**  Work on a
normalized three-colour GHZ root slice with at least two varied roots.  Assume
that the root--blocker rows vary projectively to first order and restrict the
tangent at root `i` to

```text
S_i=ker(a_i),                 a_i(1,1,1) != 0,          (1)
```

so every differentiated root--blocker edge vanishes.  Freeze the other roots
and the nonblocker vertices, but leave the blocker modes free.  For every root
subset `I` with `|I|>=2`, the complementary hafnian tensors carried by the
companion matchings that saturate `I` must span the exact image of the GHZ
`I`-mixed derivative.

In particular, write

```text
F_c = tensor_(i in I) (e_c^* restricted to S_i),
D_c = d_c e_c^(tensor m),             d_0 d_1 d_2 != 0.               (2)
```

The required cofactor-span rank is

```text
rho(I)=dim span{F_0,F_1,F_2}.                            (3)
```

It has the following complete classification for `|I|>=2`.

1. If the coordinate-axis types occurring among the `a_i` have colour set
   `A`, then `rho(I)=3-|A|`.  The cofactor span contains every individual
   `D_c` with `c notin A`.
2. If no axis type occurs and all `a_i` are supported on one common coordinate
   pair `{p,q}`, then `rho(I)=2`.  With `e` the remaining colour and

   ```text
   lambda=product_(i in I) (-a_(i,q)/a_(i,p)),          (4)
   ```

   the cofactor span contains both `D_e` and `D_q+lambda D_p`.
3. If no axis type and no common coordinate pair occurs, then `rho(I)=3` and
   the cofactor span contains the whole diagonal plane
   `span{D_0,D_1,D_2}`.

Thus matching saturation is only the rank-one shadow of a stronger condition:
a generic multi-root lower jet needs three linearly independent, correctly
valued complementary cofactors.  The common-plane and axis loci need the exact
two- or one-dimensional frames displayed above.

The theorem does not assume that individual companion edges are rank one, and
allows arbitrary root--root tangent blocks.  It is necessary, not sufficient.
It does not classify simultaneous principal-hafnian realizability, restore
nonprojective root--blocker variation, or prove the arbitrary-order
local-to-global reduction.  The global Krenn--Gu conjecture remains
**UNRESOLVED**.  No finite field is used.

## Deletion-class expansion

Fix `I` and differentiate once at every root in `I`.  In every surviving
perfect-matching term, each varied root is paired either to another varied
root or to one fixed nonblocker vertex.  It cannot pair to a blocker because
of (1).  Let `A` be the set of fixed partners used by the varied roots.
All varied roots and all vertices of `A` are deleted before the remaining
matching is chosen.  Therefore every partial companion matching with the
same `A` carries the single complementary tensor

```text
C_(I union A).                                          (5)
```

The internal pairings and the root-to-`A` bijections aggregate into one
multilinear scalar form `G_A`.  Hence the complete graph derivative is

```text
T_I^graph = sum_A G_A tensor C_(I union A),
|A| congruent |I| (mod 2).                              (6)
```

This is an identity of tensors, not a support count.  Linearize the
multilinear root variables on `tensor_(i in I) S_i`.  Equality with the GHZ
derivative

```text
T_I^GHZ = sum_(c=0)^2 F_c tensor D_c                  (7)
```

implies

```text
Im(T_I^GHZ) subset span{C_(I union A): G_A != 0}.       (8)
```

Consequently at least `rho(I)` independent deletion cofactors are necessary,
and (8) forces their actual diagonal combinations, not merely their
nonvanishing.  If no admissible matching saturates `I`, the right side is
zero and this recovers the support theorem in
[`ROOT_RESTRICTED_JET_COMPANION_MATCHING_SATURATION_NECESSITY.md`](ROOT_RESTRICTED_JET_COMPANION_MATCHING_SATURATION_NECESSITY.md).

## Rank and value classification

The form `F_c` is zero exactly when some `a_i` is the coordinate-axis
covector `e_c^*`.  Suppose first that an axis colour occurs.  At a root of
axis type `c`, the restrictions of the other two coordinate covectors are
independent.  Thus any surviving pair of the `F_c` is nonproportional.  There
are at most two survivors, proving case 1.  Independent row forms let one
choose dual tensors that isolate their columns, so (8) contains the stated
individual `D_c`, not just their span dimension.

Now suppose that no axis type occurs.  All three `F_c` are nonzero.  Two of
them, say `F_p,F_q`, are proportional exactly when their local factors are
proportional at every root.  This is equivalent to

```text
a_i in span{e_p^*,e_q^*} for every i in I.             (9)
```

Both coefficients in that pair are then nonzero, and the relation on `S_i`
is

```text
e_p^*|S_i = -(a_(i,q)/a_(i,p)) e_q^*|S_i.             (10)
```

Tensoring (10) gives (4) and the two exact target columns in case 2.

If the three nonzero `F_c` are pairwise nonproportional, they are linearly
independent.  Indeed, a dependence with three nonzero coefficients can be
grouped at one root in a basis of its two-dimensional dual tangent plane.
It would force the three complementary pure tensors to be proportional.
Equality of nonzero decomposable tensors would then make all three coordinate
restrictions proportional at every other root.  Because `|I|>=2`, such a
root exists, contradicting `dim S_i^*=2`.  This proves case 3 and completes
the arbitrary-order classification.

The restriction `|I|>=2` is deliberate.  The singleton derivative has rank
two and its quotient-frame rigidity is already proved in
[`ROOT_TANGENT_COMPANION_NECESSITY_FOR_COORDINATE_SLICE.md`](claims/arbitrary-order/ROOT_TANGENT_COMPANION_NECESSITY_FOR_COORDINATE_SLICE.md).

## The full-jet sharpness construction fails the first lower two-root value

The legal construction in
[`ROOT_ARBITRARY_ORDER_TWO_ENDPOINT_FULL_JET_FRAME_SHARPNESS_NOGO.md`](ROOT_ARBITRARY_ORDER_TWO_ENDPOINT_FULL_JET_FRAME_SHARPNESS_NOGO.md)
has `a_i=e_2^*` at every root.  Hence every two-root subset requires the two
individual cofactor values `D_0,D_1` by case 1.

For every `r>=3`, take `I={r_0,r_1}`, differentiate both roots in direction
`e_1`, and ask for the all-`1` blocker coefficient.  The GHZ value is one.
The graph value is zero in both parities:

- if `r` is odd, the two varied roots may use their colour-`1` path edge,
  but then endpoint `q_1` has no surviving neighbour; its blocker edge has
  colour `0` and its root edge meets a fixed root, where
  `(e_1^*-e_2^*)(1,1,1)=0`;
- if `r` is even, the edge `r_0r_1` has colour `0`, while the only colour-`1`
  neighbour of `r_1` is the fixed root `r_2`, again giving zero.

Thus the construction passes every support-saturation test and realizes the
sharp full-root frame, but fails an actual lower two-root cofactor value at
all root counts `r>=3`.  This is a lower-jet obstruction to that construction,
not a no-go for all legal companion systems.

## Replay

```powershell
uv run --with sympy python verify_root_arbitrary_lower_mixed_jet_cofactor_frame_necessity.py
python audit_root_arbitrary_lower_mixed_jet_cofactor_frame_necessity.py
uv run --with sympy --with ruff python -m ruff check verify_root_arbitrary_lower_mixed_jet_cofactor_frame_necessity.py audit_root_arbitrary_lower_mixed_jet_cofactor_frame_necessity.py
python -m py_compile verify_root_arbitrary_lower_mixed_jet_cofactor_frame_necessity.py audit_root_arbitrary_lower_mixed_jet_cofactor_frame_necessity.py
```

The primary reconstructs the exact restricted-product ranks and required
diagonal image spaces on a bounded projective covector box, audits the
deletion-set grouping of perfect matchings, and evaluates the displayed
lower-jet coefficient in the legal sharpness graph.  The no-import audit
uses independent rational row reduction, a separate matching recurrence,
and a direct parity construction.  These bounded calculations audit the
formulas; equations (5)--(10) and the parity isolation argument prove the
statements for every order in characteristic zero.
