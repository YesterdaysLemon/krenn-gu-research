# Alignment desaturates the one-chord `2+1+0` port

## Status

**Exact characteristic-zero arbitrary-order conditional theorem for the
physical eight-cell one-chord subbranch.**  In that subbranch at support
`3m+3`, coefficient alignment forces the zero-excess port to have exactly
two outgoing cells, in the two colours different from its core word colour.
Therefore

```text
q_2=dim(V_2/B_2)=1,                                 (1)
```

and the apolar saturation `B_2=V_2` is impossible.

The degree ledger then leaves exactly three symbolic placements of the final
surplus.  The branch in which that surplus lies at an exterior mode is
excluded by an exact rank-two apolar slice.  Two concentrated branches--the
extra outgoing cell at `a_0` or at `a_1`--remain open.

This advances the genuine aligned physical-eight-cell subbranch and explains
precisely why the 21-cell saturation model in
`ARBITRARY_PERMANENT_THREE_EXCESS_ONE_CHORD_APOLAR_SATURATION_BOUNDARY.md`
must have backbone-alignment defect at least one.

## Hypotheses and canonical core

Assume a characteristic-zero restriction

```text
P_m -> Delta_3,       support size 3m+3,       m>=4. (2)
```

Choose the mandatory tricolour coordinate cover `B`, the three excess cells
`E`, pure backbones `M_0,M_1,M_2`, and

```text
H=M_0 union M_1 union M_2                           (3)
```

as in `ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md`.
Suppose:

1. all three excess cells lie in an aligned one-chord theta core on modes
   `a_0,a_1,a_2` and exceptional sources `p_0,p_1,p_2`;
2. their mode-incidence profile is `2+1+0`, with no excess cell at `a_2`;
3. a bare-theta matching together with a common exterior complement belongs
   to `H` with chosen alignment labels--every edge labelled `c` belongs to
   `M_c`--and the relevant core competitors are eligible for its word; and
4. the physical `A-P` support consists of exactly the eight cells displayed
   in (4): the missing chord `a_2p_1` is physically absent, not merely
   ineligible at this word.

Write that core word as `(alpha_0,alpha_1,alpha_2)` and put
`z_i=e_(alpha_i)`.  After absorbing nonzero cell scalars, the eligible
one-chord core has the form

```text
X = [ z_0   L_1   L_2 ]
    [ M     a z_1 b z_1]                           (4)
    [ c z_2 0     d z_2],
```

where `a,b,c,d` are nonzero.  The physically absent chord is `a_2p_1`; the
displayed `a_1p_2` cell is the one added chord.  The two forms `L_1,L_2` and
the form `M` are the three excess cells.

If `a_2p_1` exists physically with another coordinate colour but is
ineligible at the aligned word, it contributes to the physical degree and
can supply a missing local-rank direction.  That differently coloured
second-chord branch is outside this theorem and remains open.

Let `Q` be the exterior sources and define

```text
B_i=span{forms on cells a_i-q : q in Q},
s_i=number of such cells.                           (5)
```

Let

```text
tau=sum_(exterior modes r) (deg(r)-3).              (6)
```

Local rank makes every term in (6) nonnegative.

## Theorem 1: alignment forces exact desaturation

Every cell from `a_2` to an exterior source is one of the mandatory
coordinate cells: all three excess cells are already in the core.  If such
a cell has colour `c`, then it must belong to `M_c`.

Indeed, its exterior source is not exceptional.  The localization lemma says
that omitting its mandatory colour-`c` cell from `M_c` would require a
colour-`c` excess replacement at that same source.  No excess cell has an
exterior source, so omission is impossible.

The aligned theta matching uses one of the two core cells incident to `a_2`
in `M_(alpha_2)`.  A perfect matching has only one edge at `a_2`.  Hence no
outgoing cell at `a_2` has colour `alpha_2`.  Moreover there is at most one
outgoing cell in each other colour, because every such cell is forced into
its corresponding `M_c`.

The two core forms at `a_2` are both collinear with `z_2`.  Local rank three
therefore requires outgoing forms in both other coordinate directions.  We
obtain exactly

```text
s_2=2,
B_2=span{e_c : c != alpha_2},
V_2/B_2=span(pi_2(z_2)).                            (7)
```

In particular `pi_2(z_2)` is nonzero and (1) holds.  This proof uses the
coloured alignment incidence absent from the saturation countermodel; it is
not a consequence of the uncoloured degree ledger.

## Theorem 2: the three remaining surplus placements

The core degrees in (4) are `3,3,2`.  Since the total mode-degree surplus is
three,

```text
s_0+s_1+(s_2-1)+tau=3.                             (8)
```

Equation (7) reduces this to

```text
s_0+s_1+tau=2.                                     (9)
```

At `a_1`, its three core cells span at most
`span(M,z_1)`, so local rank three requires `s_1>=1`.  Thus the only
nonnegative solutions of (9) are

```text
(s_0,s_1,s_2;tau) =
  (0,1,2;1),       exterior-surplus branch,
  (1,1,2;0),       a_0-concentrated branch,
  (0,2,2;0).       a_1-concentrated branch          (10)
```

No support, word, or matching family is enumerated in this classification.

## Theorem 3: exclusion of the exterior-surplus branch

Assume the first line of (10).  Then `B_0=0`.  Local rank at `a_0` forces

```text
z_0,L_1,L_2 independent.                           (11)
```

At `a_1`, the single outgoing line `B_1` must be independent from the
two-dimensional core span, so

```text
M,z_1 remain independent in V_1/B_1.               (12)
```

Apply the product quotient

```text
pi=pi_0 tensor pi_1 tensor pi_2,
pi_i:V_i -> V_i/B_i.                               (13)
```

Every nonempty boundary sector contains an `A-Q` cell, whose factor lies in
some `B_i`, so (13) kills it termwise.  The projected core tensor from (4)
factors through the surviving line `pi_2(z_2)` and has two-way part

```text
d L_1 tensor pi_1(M)
 + (a d z_0+b c L_1+a c L_2) tensor pi_1(z_1).     (14)
```

The two row-zero vectors in (14) are independent by (11), and the two
row-one vectors are independent by (12).  Hence its `a_0|a_1` flattening
rank is exactly two.  In the ordered bases `(z_0,L_1,L_2)` and
`(pi_1(z_1),pi_1(M))`, a nonzero minor is

```text
det [a d  0]
    [b c  d] = a d^2 !=0.                          (15)
```

It remains to justify that the empty boundary sector is nonzero.  Let `N`
be the aligned exterior complement and freeze its exterior word.  Every
`R-Q` cell eligible at that word is a mandatory cell at a nonexceptional
source and is therefore forced into its colour backbone.  At a fixed mode a
perfect matching contains only one such cell.  Thus `N` is the unique
empty-sector exterior matching for its word, and its monomial weight is
nonzero.  Cells from `R` to exceptional core sources cannot occur in the
empty sector.

After freezing that word and applying (13), the hypothetical restriction
therefore has a nonzero scalar multiple of the rank-two tensor (14).  On the
target side, (7) kills `e_c` for every `c!=alpha_2`, so the projected
`Delta_3` slice has `a_0|a_1` flattening rank at most one (and may be zero).
This contradicts (15).  Hence

```text
(s_0,s_1,s_2;tau)=(0,1,2;1) is impossible.         (16)
```

## Remaining constrained image

Only the two concentrated lines of (10) survive:

```text
(1,1,2;0):  one outgoing line at a_0 may collapse the two row-zero
             directions in (14);

(0,2,2;0):  two outgoing lines at a_1 may collapse the two row-one
             directions in (14).                  (17)
```

These are genuine method boundaries.  The ambient zeon-jet dominance no-go
does not apply after (7), but ordinary flattening alone need not distinguish
the projected core from the target in (17).  A next theorem must use the
colour forced by the aligned theta edge at the concentrated port, or couple
the degree-one and degree-two permanental compounds.

## Theorem 4: monochromatic-exterior confinement

Although the two charts in (17) are not yet excluded, their projected core
tensors are always nonzero.

In the `a_0`-concentrated chart, `B_1` is one line outside
`span(M,z_1)`, so their quotient classes remain independent.  If the tensor
(14) vanished, both `L_1` and

```text
V=a d z_0+b c L_1+a c L_2                         (18)
```

would lie in the single boundary line `B_0`.  Then `L_1` lies in `B_0`, and
the relation `V in B_0` puts `z_0,L_2,B_0` in a space of dimension at most
two.  All incident forms at `a_0` would have rank at most two, contrary to
local rank three.

In the `a_1`-concentrated chart, the same colour-forcing proof as Theorem 1
gives

```text
B_1=span{e_c:c!=alpha_1}.                           (19)
```

Thus `pi_1(M)=mu pi_1(z_1)` for some scalar `mu`.  Since `B_0=0`, local rank
makes `z_0,L_1,L_2` independent, and the surviving row-zero vector is

```text
a d z_0+(b c+d mu)L_1+a c L_2.                     (20)
```

It is nonzero because its `z_0` and `L_2` coefficients are nonzero.

The frozen target slice is nonzero after (13) only if all exterior modes in
the aligned complement word have colour `alpha_2` and neither of the other
port quotients kills `e_(alpha_2)`.  Therefore every surviving concentrated
chart must satisfy

```text
exterior complement word = alpha_2^(m-3),
pi_0(e_(alpha_2)) != 0,
pi_1(e_(alpha_2)) != 0.                            (21)
```

For `(1,1,2;0)`, if the outgoing colours at `a_0,a_1` are respectively
`beta_0,beta_1`, (21) says

```text
beta_0!=alpha_2,              beta_1!=alpha_2.     (22)
```

For `(0,2,2;0)`, equation (19) turns (21) into

```text
alpha_1=alpha_2.                                    (23)
```

If the aligned full word is mixed, (21) and (23) further force
`alpha_0!=alpha_2` in this second chart.  Put `c=alpha_2`.  The aligned
physical matching then uses its colour-`c` backbone edge at every mode except
possibly `a_0`.  Those `m-1` edges leave exactly the mode `a_0` and the source
`M_c(a_0)` unmatched, so perfectness forces the last physical edge to be
`M_c(a_0)` as well.  The aligned edge at `a_0` consequently lies in both
`M_(alpha_0)` and `M_c` and has nonzero components in both colours.  It
cannot be the mandatory coordinate cell `z_0`; it must be one of the excess
cells `L_1,L_2`.

Thus the diagonal bare-theta matching using `z_0` is impossible in the mixed
`a_1`-concentrated survivor.  Only the other two theta matchings remain, and
their selected `a_0` excess edge must be shared by two pure backbones.
Equations (21)--(23) and this shared-edge condition are necessary, not
constructions and not a proof that either chart survives.

## Scope wall

```text
scope:      physical eight-cell A-P one-chord support;
proved:     alignment forces s_2=2 and q_2=1 in that scope;
proved:     the saturated B_2=V_2 branch is nonaligned and impossible here;
proved:     exactly the three surplus placements (10) remain a priori;
excluded:   the exterior-surplus placement (0,1,2;1);
open:       the concentrated placements (1,1,2;0) and (0,2,2;0);
proved:     every concentrated survivor obeys (21)--(23);
proved:     the mixed a_1-concentrated survivor needs a shared excess edge;
open:       physically present but word-ineligible second chord;
not proved: full exclusion of aligned one-chord 2+1+0;
not proved: exclusion of the bare aligned theta;
not used:   support enumeration, coefficient-word census, finite fields;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_arbitrary_permanent_three_excess_one_chord_210_alignment_desaturation_theorem.py
python audit_arbitrary_permanent_three_excess_one_chord_210_alignment_desaturation_theorem.py
```

The primary verifier checks the exact core flattening and surplus ledger.
The independent no-import audit reconstructs the coefficient matrix,
colour-forcing consequence, and rank minor.  These scripts guard the fixed
symbolic formulas; the arbitrary-order statements are proved above.
