# Arbitrary permanent equality five-edge shore Kempe exclusion

## Status

This is an exact arbitrary-order exclusion of the `(1,1,3)` Hall shore in
the two-switch no-completion branch.  It uses a defect-one boundary-balance
invariant and alternating-path exchange.  It performs no support, word, or
matching enumeration.

The shore has five boundary semiedges.  For either switch colour, its pure
matching and the third-colour matching induce two alternating paths inside
the shore.  Defect-one balance forces one bit recording which third-colour
outgoing port is paired with the switch-colour port.  The pure switch toggles
the corresponding exterior pairing without changing the shore bit.  One of
the two pure backbones must therefore align the pairings, split the global
symmetric difference into at least two cycles, and permit a one-cycle flip.
The resulting mixed perfect matching has no cancellation partner by
exceptional-source localization.

Together with the three-edge shore flattening exclusion, this proves that
the residual graph in every hypothetical two-switch equality survivor has a
perfect matching.  Hence the direct port-completion rectangle is forced.
This note alone does not exclude the completed two-switch branch.  A
subsequent opposite-source Hamilton-chord theorem excludes it completely.
The global Krenn--Gu conjecture remains unresolved.

## Five-port shore

Use the notation of the port-completion shore theorem.  Let `S` be a minimal
Hall-deficient residual mode set, `T=N_R(S)`, and

```text
|S|-|T|=1.                                           (1)
```

In shore type `(1,1,3)`, both residual third-colour port modes lie in `S`.
Name the five physical cut semiedges

```text
C, D, E_1, E_2, I.                                  (2)
```

Here `C,D` are the outgoing `c,d` cells from `S` to the same deleted source
`q`; `E_s` is the outgoing `e` cell from a residual mode `u_(e,s)` to
exceptional source `p_s`; and `I` is the unique `e` cell entering a source
of `T` from a mode outside `S` (possibly `b_c` or `b_d`).

These are the complete physical cut cells.  Every residual mode is
coordinate-only, and the preceding port theorem identifies all cells of its
degree-three support with the three backbone cells.  For `c,d`, the
restrictions from `S` minus their single port modes are bijections onto `T`.
For `e`, two matching cells leave `S` and one enters `T`.  Every source in
`T` is nonexceptional, so its only physical cells are its three mandatory
coordinate cells, namely its `M_c,M_d,M_e` preimages.  Hence there are no
additional incoming or outgoing cut cells.

## Defect-one boundary balance

Let `K` be the restriction to `W=S union T` of any perfect matching.  Write
`o(K)` for its number of cells leaving a mode in `S` and `i(K)` for its
number of cells entering a source in `T`.  If `n(K)` internal cells join
`S` to `T`, counting saturated modes and sources gives

```text
|S|=n(K)+o(K),
|T|=n(K)+i(K),
o(K)-i(K)=1.                                         (3)
```

Fix one switch colour `h in {c,d}` and call its port `H`.  Inside `W`, the
boundary patterns of the restrictions of the selected pure matchings are

```text
partial M_h: {H},
partial M_e: {E_1,E_2,I}.                            (4)
```

Their symmetric difference is a disjoint union of alternating cycles and
exactly two alternating paths pairing the four boundary semiedges in (4).
The port `H` cannot pair with `I`: flipping that path in `M_h|W` would leave
boundary `{I}`, whose balance is `-1`, contradicting (3).  Equivalently, the
remaining path cannot pair `E_1` with `E_2`, since flipping it into
`M_h|W` would leave three outgoing ports and balance `3`.

Consequently there is a unique bit

```text
iota_h in {1,2}                                      (5)
```

such that the internal path pairing is

```text
H <--> E_(iota_h),
E_(3-iota_h) <--> I.                                 (6)
```

This is the **five-port Kempe bit**.  It is forced by the shore defect, not
by a Pfaffian or matchgate identity.

## The pure switch toggles the exterior bit

Outside `W`, the `M_h`--`M_e` path beginning with `H` is forced.  If the
selected pure `h`-matching sends the common excess mode `a` to `p_s`, then
the path is

```text
u_h --H-- q --e-- a --h-- p_s --E_s-- u_(e,s).      (7)
```

Indeed, the pure third-colour matching uses the unique cell `a--e--q`, and
at `p_s` it uses the residual port `E_s`.  Hence the exterior pairing is

```text
H <--> E_s.                                          (8)
```

The pure `h`-switch transposes `p_1,p_2` at `a,b_h`, so it toggles `s`.
It changes no cell of the residual graph or of `W`, and therefore does not
change `iota_h`.  Exactly one of the two pure `h`-backbones satisfies

```text
s=iota_h.                                            (9)
```

Choose that aligned backbone.  The internal and exterior paths from `H` to
`E_s` close to one alternating cycle `Z`.  The remaining internal and
exterior paths from `E_(3-s)` to `I` close to a second alternating cycle.
Thus `M_h symmetric-difference M_e` has at least two nonempty cycle
components.  These are cycles of distinct physical cells; all coloured
backbone copies are collapsed before the exchange.

## One-cycle flip and the unique forbidden monomial

Flip only `Z` in `M_h`.  The result is a perfect matching

```text
F subset M_h union M_e                               (10)
```

which is nonmonochromatic.  At the exceptional sources it uses

```text
u_(e,s) --e--> p_s,
b_h       --h--> p_(3-s).                            (11)
```

The first cell belongs to the flipped cycle.  The second belongs to the
other, unflipped cycle and is retained from `M_h`.

Apply the exceptional-source localization and rectangle theorem to `F`.
Because `F` lies in the selected backbone union, any other permanent term
for the same input word would have to be the unique exceptional-source
transposition of (11).  Its required first cross cell is

```text
u_(e,s) --e--> p_(3-s).                              (12)
```

But `u_(e,s)` is a residual coordinate-only mode.  Its unique physical cell
with nonzero `e` coordinate is the named port to `p_s`; therefore (12) is
absent.  No longer alternative cycle is possible by the localization
theorem.  The mixed coefficient containing `F` consequently consists of one
nonzero monomial, contradicting its zero coefficient in `Delta_3`.

Hence

```text
connected no-completion shore (1,1,3): IMPOSSIBLE.   (13)
```

The argument works with either switch colour separately.

## Port-completion corollary

The residual Hall theorem says that failure of a perfect matching in `R`
produces a connected shore of type `(1,1,1)` or `(1,1,3)`.  The first is
excluded by the tight-cut flattening theorem, and (13) excludes the second.
Therefore every hypothetical two-switch equality survivor has

```text
R has a perfect matching.                            (14)
```

The port-completion equivalence then supplies a direct mixed backbone and
forces the third switch-mode rectangle

```text
r_(b_c,p_1)[c] r_(b_d,p_2)[d]
+r_(b_c,p_2)[c] r_(b_d,p_1)[d]=0,                   (15)
```

or, in gain coordinates,

```text
g_(b_c,c)=-g_(b_d,d).                                (16)
```

This is a new forced cross-colour relation.  It does not yet contradict the
two switch pure factors or the excess-plane inequality.

## Literature translation

The internal path decomposition is ordinary matching symmetric difference,
while (3) is the defect-one conservation law of a tight Hall shore.  The
new ingredient is to retain the pairing of boundary semiedges as a single
binary invariant and compare it with the exterior pairing changed by a pure
switch.  This may be viewed as a finite boundary-state or Kempe-exchange
theory for defect-one matching shores.

It resembles matchgate boundary calculus, but no deletion-closed signature
or Pfaffian identity is assumed.  The proof uses only saturation balance,
alternating paths, and the already-proved localization of cancellation to
the two exceptional sources.  The Dulmage--Mendelsohn origin of the shore is
classical; see
[*Coverings of Bipartite Graphs*](https://doi.org/10.4153/CJM-1958-052-0).

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_five_edge_shore_kempe_exclusion.py
python audit_arbitrary_permanent_equality_five_edge_shore_kempe_exclusion.py
```

The primary verifier checks the defect-one boundary balances, invariance and
toggle of the two pairing bits, and the nonzero one-term mixed coefficient
after the missing cross cell is imposed.  The independent no-import audit
checks the same logical spine with integer boundary counts and a separate
bit representation.  These are fixed symbolic checks; the arbitrary-order
content is the full alternating-path and localization proof above.

## Boundary

```text
five physical shore cells:               EXACT;
defect-one balance:                       o-i=1;
internal five-port Kempe bit:             FORCED;
pure switch toggles exterior bit:         FORCED;
aligned backbone:                         EXISTS;
one-cycle flip:                           MIXED PERFECT MATCHING;
exceptional-source cross partner:         ABSENT;
(1,1,3) no-completion shore:              EXCLUDED;
residual R in two-switch equality:        HAS A PERFECT MATCHING;
third switch-mode rectangle:              FORCED;
two-switch equality stratum:              EXCLUDED SUBSEQUENTLY;
global Krenn--Gu conjecture:              UNRESOLVED.
```
