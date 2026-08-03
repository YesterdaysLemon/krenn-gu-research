# Cut-colour transport excludes the tight aligned one-chord `1+1+1` branch

## Status

**Exact arbitrary-order symbolic exclusion in characteristic zero.**  Consider
the tight aligned conformal theta setup at support `3m+3`, with one excess
cell at each of the three theta modes and sources.  Suppose exactly one of
the two theta-completing chords is eligible in the aligned coefficient and
the three core modes have four outgoing boundary cells in total.

Then that coefficient is impossible for every `m>=4`.

The proof introduces a colour-by-colour cut conservation law.  It combines
the mandatory source cover with the cubic tricolour exterior forced by the
tight degree ledger.  After quotienting by outgoing boundary covectors, the
cut law either kills every diagonal target direction or confines the tensor
to one repeated-colour chart.  In that chart, two branch positions are
excluded by tensor rank/direction, and the third could imitate the target
only if one theta edge vanished at the aligned word.  Coefficient-induced
theta alignment forbids that vanishing.

This is a symbolic three-port theorem.  It uses no support-family, matching-
tuple, or input-word enumeration.  It extends the two-chord exclusion in
[`ARBITRARY_PERMANENT_THREE_EXCESS_APOLAR_BOUNDARY_QUOTIENT_THEOREM.md`](ARBITRARY_PERMANENT_THREE_EXCESS_APOLAR_BOUNDARY_QUOTIENT_THEOREM.md).

## Setup and canonical one-chord core

Let the core modes be `A={a_0,a_1,a_2}` and exceptional sources be
`P={p_0,p_1,p_2}`.  Relabel the excess matching as the diagonal and the
absent chord as `(a_2,p_1)`.  The unspecialized port matrix is

```text
[ L_0, p z_0, q z_0 ]
[ r z_1, L_1, u z_1 ]                              (1)
[ t z_2,   0, L_2 ]
```

with `p,q,r,u,t!=0`.  Here `z_i=e_(alpha_i)` is the mandatory coordinate
selected by the aligned word at row `i`, while `L_i` is the excess covector.
Because all three internal theta matchings occur nontrivially at that word,

```text
L_i[alpha_i]!=0                 for i=0,1,2.        (2)
```

Let `s_i` count cells from `a_i` to exterior sources.  The internal row
degrees of (1) are `3,3,2`.  Local rank three gives `s_i>=1`, and the global
three-unit mode surplus gives

```text
s_0+s_1+s_2<=4.                                     (3)
```

This note treats the hard equality case

```text
s_0+s_1+s_2=4.                                     (4)
```

Thus `(s_0,s_1,s_2)` is a permutation of `(2,1,1)`, and all three units of
mode surplus occur at the core.  Every exterior mode is consequently cubic.
All excess cells lie in the core, so its three incident exterior cells are
mandatory coordinate cells; local rank makes their colours exactly
`0,1,2`, one of each.

## The cut-colour conservation law

Write `R,Q` for the exterior modes and sources.  For each colour `c`, count
mandatory coordinate cells of colour `c` in the two directed cuts.  Every
exterior mode has exactly one such cell, so

```text
#(R--P cells of colour c)+#(R--Q cells of colour c)=|R|.  (5)
```

The mandatory tricolour cover has exactly one chosen coordinate cell of
colour `c` above every exterior source, so

```text
#(A--Q cells of colour c)+#(R--Q cells of colour c)=|Q|.  (6)
```

Since `|R|=|Q|=m-3`, subtraction gives the **cut-colour transport law**

```text
#(A--Q cells of colour c)=#(R--P cells of colour c) (7)
```

for each `c` separately.  This is stronger than uncoloured shore balance.
It is a consequence of the chosen mandatory cover and exterior cubicity,
not an assumption that physical coordinate cells are unique.

The five mandatory cells in (1) determine the source-side cut.  At `p_0`
the core cover colours are `alpha_1,alpha_2`, at `p_1` only `alpha_0`, and at
`p_2` they are `alpha_0,alpha_1`.  Because the cover contains one chosen cell
per source and colour,

```text
alpha_0!=alpha_1,               alpha_1!=alpha_2.  (8)
```

There are only two symbolic colour patterns.  After renaming colours,

```text
(alpha_0,alpha_1,alpha_2)=(0,1,2):
    colours(R--P)={0,1,2,2};

(alpha_0,alpha_1,alpha_2)=(0,1,0):
    colours(R--P)={1,2,2,2}.                        (9)
```

Equation (7) transfers exactly these multisets to the outgoing core cut.

## Boundary quotient and the all-distinct exclusion

For each row put

```text
B_i=span{coordinate covectors on cells from a_i to Q},
pi_i:V_i -> V_i/B_i,            pi=pi_0 tensor pi_1 tensor pi_2. (10)
```

As in the two-chord apolar theorem, every nonempty balanced boundary sector
contains an `A--Q` cell and dies under `pi`.  The projected full tensor is

```text
(pi tensor id)T_G=pi(T_K) tensor Omega_empty.       (11)
```

Conformality gives an exterior perfect matching.  Its incident colours at
the cubic exterior modes select it uniquely, so `Omega_empty` has a nonzero
coefficient.

If the two outgoing cells at the unique two-cell row have the same colour,
then every `B_i` is one-dimensional.  Local rank makes `L_i,z_i` independent
modulo `B_i`.  Flattening (1) along row zero has coefficient rows

```text
z_0: (put,pr,qt,0),          L_0:(0,0,0,1),        (12)
```

in the basis `(z_1z_2,z_1L_2,L_1z_2,L_1L_2)`.  The
`(z_1L_2,L_1L_2)` minor is `pr!=0`, so the projected core has boundary-
entanglement rank at least two, contradicting the zero/rank-one target
slice.

It remains to take two distinct outgoing colours at the two-cell row `b`.
That quotient leaves one coordinate colour `gamma_b`.  At either other row
`i`, its unique boundary colour `beta_i` differs from `alpha_i`; otherwise
`L_i,z_i` and the boundary line could not have rank three.

For the all-distinct pattern, (7)--(9) give the following complete symbolic
table.  `B_b` lists the two killed colours; the last column exhibits another
row which kills the only survivor.

```text
b   B_b       other boundary colours       survivor killed by
0   {0,2}     beta_1=2, beta_2=1           beta_2
0   {1,2}     beta_1=2, beta_2=0           beta_2
1   {0,2}     beta_0=2, beta_2=1           beta_2
1   {1,2}     beta_0=2, beta_2=0           beta_2
2   {0,1}     beta_0=2, beta_1=2           beta_0,beta_1
2   {0,2}     beta_0=1, beta_1=2           beta_0
2   {1,2}     beta_0=2, beta_1=0           beta_1. (13)
```

Thus `pi_0(e_c) tensor pi_1(e_c) tensor pi_2(e_c)=0` for every colour `c`.
The projected target is zero.  The projected port tensor is nonzero: if
`z_b` dies, local rank makes the private all-excess coefficient survive; if
`z_b` survives, the respective private basis coefficient is `pr`, `pr`, or
`qt` for `b=0,1,2`.  Equation (11) is therefore impossible.

## The repeated-colour chart

Now take `(alpha_0,alpha_1,alpha_2)=(0,1,0)`.  Equations (7)--(9) have one
solution for each possible two-cell row:

```text
B_b=span(e_1,e_2),        B_i=span(e_2) for i!=b.  (14)
```

Only target colour zero survives all three quotients.

If `b=0`, the projected port tensor contains the private basis coefficient

```text
pr z_1 tensor L_2,                                  (15)
```

while the colour-zero target at row two is proportional to `z_2`, not
`L_2`.  Local rank makes `z_2,L_2` independent modulo `B_2`, so (15) excludes
target alignment.

If `b=1`, `z_1=e_1` dies and local rank makes `L_1[0]!=0`.  After factoring
that nonzero scalar, the two remaining rows contain

```text
L_0 tensor L_2 + qt z_0 tensor z_2,                 (16)
```

which has flattening rank two because `L_i,z_i` are independent modulo the
single boundary line.

Finally let `b=2`, the deficient row.  Put `ell=L_2[0]`.  The projected
tensor contains

```text
ell L_0 tensor L_1                                 (17)
```

in the two uncontracted rows.  By (2), `ell!=0`; local rank again makes
`L_0,z_0` independent.  Hence (17) cannot be proportional to the colour-zero
target, whose row-zero direction is `z_0`.

This exhausts (13)--(14), so the aligned one-chord branch with (4) is
excluded.

## Sharpness: the nonalignment absorption divisor

The use of alignment in the last case is essential.  If one sets

```text
L_2[0]=0,                                           (18)
```

then the selected coefficient equation becomes, after normalizing the
coordinate evaluations,

```text
qt L_1[1]+put=0.                                   (19)
```

Modulo `e_2`, write `L_1=k e_0+L_1[1]e_1`, with `k!=0`.  Equations
(18)--(19) turn the projected port tensor into

```text
qt k e_0 tensor e_0 tensor e_0.                    (20)
```

Thus the quotient really can imitate the diagonal target on this divisor.
But (18) deletes the theta edge `(a_2,p_2)` from the aligned word, so one of
the three theta matching monomials vanishes.  It is an exact counterchart to
any proof omitting coefficient-induced alignment, not a surviving aligned
case and not a full restriction.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_one_chord_cut_color_exclusion_theorem.py
python audit_arbitrary_permanent_three_excess_one_chord_cut_color_exclusion_theorem.py
```

The primary verifier checks the port permanent, decisive flattening minors,
the two cut-colour tables, all three repeated-colour branch tensors, and the
exact nonalignment absorption.  The no-import audit independently replays
the colour transport table and integer instances of every rank/direction
test.  The arbitrary-order boundary factorization and unique exterior-word
argument are the proofs above.

## Boundary

```text
cut-colour transport at s=4:                  PROVED;
aligned diagonal-1+1+1 one-chord s=4 branch: EXCLUDED FOR m>=4;
nonalignment divisor L_i[alpha_i]=0:          EXACT TARGET-LIKE COUNTERCHART;
one-chord s=3 branch:                         NOT EXCLUDED;
one-chord 2+1+0 excess-mode profile:          NOT EXCLUDED;
bare aligned theta:                           NOT EXCLUDED;
exclusion of every support-3m+3 case:         NOT PROVED;
global Krenn--Gu conjecture:                  UNRESOLVED.
```
