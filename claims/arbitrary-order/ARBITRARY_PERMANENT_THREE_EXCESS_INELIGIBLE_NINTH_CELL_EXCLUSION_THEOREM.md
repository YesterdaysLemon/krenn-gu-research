# The ineligible ninth cell still leaves a Segre obstruction

## Status

**Exact characteristic-zero arbitrary-order conditional theorem.**  In the
aligned one-chord `2+1+0` setup at support `3m+3`, suppose the second chord is
physically present as a mandatory coordinate cell but is ineligible at the
chosen aligned word.  Then this physical nine-cell subbranch is impossible
for every `m>=4`.

The extra cell is retained in the full port tensor.  A coordinate slice in
the aligned `alpha_2` direction kills exactly its `gamma`-coloured terms.
The resulting two-port tensor either has a nonzero `2 x 2` flattening minor,
or is nonzero while cut-colour transport forces the corresponding diagonal
target slice to vanish.  No support family, coefficient-word family, or
matching tuple family is enumerated.

Together with
`ARBITRARY_PERMANENT_THREE_EXCESS_ONE_CHORD_210_ALIGNMENT_DESATURATION_THEOREM.md`,
this excludes both physical realizations of the aligned one-chord `2+1+0`
port: an absent second chord and a present but aligned-word-ineligible one.
It does not exclude the bare aligned theta and does not resolve the global
Krenn--Gu conjecture.

## Hypotheses and the full physical port

Assume a characteristic-zero restriction

```text
P_m -> Delta_3,       support size 3m+3,       m>=4. (1)
```

Choose the mandatory tricolour coordinate cover, the three excess cells,
and aligned pure backbones as in
`ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md`.  Assume the
same labelled alignment and `2+1+0` incidence as in the physical-eight-cell
desaturation theorem, except that the formerly absent cell `a_2p_1` is now
the nonzero mandatory coordinate cell `g y_2`, where

```text
y_2=e_gamma,              gamma!=alpha_2.          (2)
```

After absorbing the other nonzero cell scalars, the full physical port is

```text
X = [ z_0   L_1    L_2  ]
    [ M     a z_1  b z_1]
    [ c z_2 g y_2  d z_2],                         (3)
```

where `z_i=e_(alpha_i)` and `a,b,c,d,g` are nonzero.  The three excess
cells are `L_1,L_2,M`; all six other displayed cells belong to the mandatory
cover.  The cell `g y_2` is ineligible at the aligned core word because of
(2), but it is not deleted from (3).

Mandatory-cover uniqueness at `p_0,p_1,p_2` gives respectively

```text
alpha_0!=alpha_2,
alpha_1!=gamma,
alpha_1!=alpha_2.                                  (4)
```

Together with (2), this says

```text
{alpha_1,alpha_2,gamma}=C={0,1,2},
alpha_0 in {alpha_1,gamma}.                         (5)
```

## The four-placement degree ledger

Let `s_i` count cells from `a_i` to exterior sources and let

```text
tau=sum_(exterior modes r)(deg(r)-3).               (6)
```

The physical core degrees in (3) are `3,3,3`, so the exact surplus equation
is

```text
s_0+s_1+s_2+tau=3.                                 (7)
```

The core at `a_1` spans at most `span(M,z_1)`, hence `s_1>=1`.  At `a_2`
the physical core span is `span(z_2,y_2)`.  Every outgoing cell there is a
mandatory coordinate at a nonexceptional source and is forced into its
colour backbone.  Alignment already uses a core edge of `M_(alpha_2)` at
`a_2`; therefore outgoing colours are distinct and different from
`alpha_2`.  Local rank three forces the missing direction `alpha_1`.
Consequently

```text
s_2=1: B_2=span(e_(alpha_1));
s_2=2: B_2=span(e_(alpha_1),e_gamma).               (8)
```

Equations (7)--(8) and `s_1>=1` leave exactly

```text
(s_0,s_1,s_2;tau)=
  (0,1,1;1),
  (1,1,1;0),
  (0,2,1;0),
  (0,1,2;0).                                       (9)
```

This is the distribution of one surplus unit beyond the forced cells at
`a_1,a_2`, not a search through supports or words.

## The `alpha_2` Segre slice

Put

```text
B_i=span{forms on cells a_i-q:q exterior},
pi_i:V_i -> V_i/B_i.                               (10)
```

The permanent tensor of (3) is

```text
T_K = a d z_0 z_1 z_2 + b g z_0 z_1 y_2
    + d L_1 M z_2     + b c L_1 z_1 z_2
    + g L_2 M y_2     + a c L_2 z_1 z_2.           (11)
```

Equation (8) implies `pi_2(z_2)!=0`.  Choose a functional on `V_2/B_2`
that sends `pi_2(z_2)` to one and kills `pi_2(y_2)` whenever the latter
survives.  Applying it to the product quotient of (11) kills every term
using the ninth cell and leaves

```text
S = d pi_0(L_1) tensor pi_1(M)
  + pi_0(a d z_0+b c L_1+a c L_2) tensor pi_1(z_1). (12)
```

Every nonempty balanced boundary sector contains an `A-Q` cell and dies
termwise under the product quotient.  Freeze the aligned exterior-complement
word.  Its empty-sector exterior matching is uniquely selected: every
eligible `R-Q` cell at a nonexceptional source is forced into its colour
backbone, and a perfect matching uses only one such cell at each mode.  More
directly, the localization lemma puts the source of any same-word cell that
differs from the designated backbone cell in the exceptional set `P`; an
`R-Q` alternative has source in `Q` and is therefore impossible.  This also
covers the possible degree-four exterior mode when `tau=1`.  The empty-sector
coefficient is consequently a nonzero scalar.  Thus the permanent side is
that scalar times `S`.  The ledger analysis below proves `S!=0` in every
case.

On `Delta_3`, the same operation leaves at most

```text
pi_0(e_(alpha_2)) tensor pi_1(e_(alpha_2)),         (13)
```

and may leave zero.  Hence the target belongs to the two-factor Segre cone:
every `2 x 2` flattening minor vanishes.

The following exact facts about (12) will be used.

1. If `s_0=0,s_1=1`, local rank gives
   `z_0,L_1,L_2` independent and makes the boundary line `B_1` transverse
   to `span(M,z_1)`.  In the corresponding quotient bases, (12) has matrix

   ```text
   [a d  0]
   [b c  d]
   [a c  0],                                       (14)
   ```

   whose first two rows have determinant `a d^2!=0`.  Thus `S` has rank
   exactly two.

2. If `s_0=s_1=1`, the same transversality at `a_1` shows that `S=0` would
   put both `L_1` and `a d z_0+b c L_1+a c L_2` in the single line `B_0`.
   Then all forms incident to `a_0` would span at most two dimensions,
   contradicting local rank three.  Thus `S!=0`.

3. If `s_0=0,s_1=2`, alignment gives
   `B_1=span(e_c:c!=alpha_1)`.  Write
   `pi_1(M)=mu pi_1(z_1)`.  Then (12) is the nonzero vector

   ```text
   a d z_0+(b c+d mu)L_1+a c L_2,                  (15)
   ```

   because `z_0,L_1,L_2` are independent and `a,c,d` are nonzero.

## Exclusion of all four placements

The placement `(0,1,1;1)` satisfies the first line above.  Its port slice
has rank two by (14), whereas (13) has rank at most one.  It is impossible.

It remains to use cut transport for the three `tau=0` placements.  Every
exterior mode is then cubic with one mandatory cell of each colour.  If
`rho_0` is the third colour outside `{alpha_0,alpha_2}`, the mandatory cells
missing from the three core sources have colours

```text
colours(R-P)={rho_0,alpha_2,gamma}.                 (16)
```

Exterior cubicity and the one-cell-per-source-and-colour cover give, for
each colour separately,

```text
#_c(A-Q)=#_c(R-P).                                 (17)
```

If `alpha_0=alpha_1`, then `rho_0=gamma`, so (16) contains no
`alpha_1`.  But (8) forces an outgoing `alpha_1` cell at `a_2` in every
placement.  This contradicts (17).

Suppose instead that `alpha_0=gamma`.  Then `rho_0=alpha_1`, so (16)
contains all three colours once.

- In `(1,1,1;0)`, the `a_2` colour is `alpha_1`.  Alignment at `a_0`
  forbids `gamma`, so (17) forces the `a_0` boundary line to have colour
  `alpha_2`.  Therefore `pi_0(e_(alpha_2))=0`: the target slice (13)
  vanishes, whereas the second fact above gives `S!=0`.

- In `(0,2,1;0)`, the two outgoing colours at `a_1` are exactly
  `alpha_2,gamma`.  Thus `pi_1(e_(alpha_2))=0`: again (13) vanishes while
  the third fact gives `S!=0`.

- In `(0,1,2;0)`, equation (8) uses `alpha_1,gamma` at `a_2`, so (17)
  forces the single `a_1` outgoing colour to be `alpha_2`.  The target
  slice vanishes, while (14) gives the stronger `rank(S)=2` contradiction.

All four lines of (9) are impossible.  Therefore

```text
aligned physical nine-cell one-chord 2+1+0
with an aligned-word-ineligible second chord
  => impossible for every m>=4.                    (18)
```

## Why this translation is useful

The operative invented object is the **colour-sliced aligned response
locus**: first impose physical cover incidence and cut transport, then take
a coordinate slice of the boundary response.  The ambient response jet is
dominant, so it has no universal polynomial equations of this kind.  On the
aligned incidence locus, however, the target slice lies on the Segre
rank-one cone and its ordinary flattening minors vanish.

This is the elementary edge of tensor invariant theory rather than a
Pfaffian or matchgate identity.  Flattenings and their determinantal
equations are standard tools for Segre and secant varieties; compare
Landsberg--Manivel, [*On the ideals of secant varieties of Segre
varieties*](https://arxiv.org/abs/math/0311388).  The interpretation as a
boundary tensor obtained by contracting a network is compatible with the
geometric tensor-network viewpoint of Landsberg--Qi--Ye,
[*On the geometry of tensor network states*](https://arxiv.org/abs/1105.4449).
No planarity, Pfaffian orientation, Gaussianity, or matchgate membership is
assumed here.

## Scope wall

```text
scope:      aligned physical 9-cell A-P support in the 2+1+0 profile;
proved:     exact four-placement physical degree ledger;
proved:     the ninth-cell terms die in the alpha_2 coordinate slice;
proved:     every placement has a Segre-rank or cut-colour contradiction;
excluded:   physically present but aligned-word-ineligible second chord;
combined:   both aligned one-chord 2+1+0 physical subbranches excluded;
open:       bare aligned theta;
not proved: exclusion of every three-excess port profile;
not used:   support enumeration, word enumeration, finite fields, numerics;
global Krenn--Gu conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_three_excess_ineligible_ninth_cell_exclusion_theorem.py
python claims/arbitrary-order/audit_arbitrary_permanent_three_excess_ineligible_ninth_cell_exclusion_theorem.py
```

The primary verifier reconstructs the six-term physical permanent, the
`alpha_2` slice, its exact nonzero minor, the four-placement ledger, and the cut
tables.  The independent no-import audit rechecks the fixed symbolic
identities from scratch.  The arbitrary-order boundary-sector selector and
incidence implications are proved above.
