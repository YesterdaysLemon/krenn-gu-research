# Arbitrary permanent equality pure-matching cube theorem

## Status

This is an exact arbitrary-order structural theorem for the `3m+2` equality
stratum.  After the two exceptional sources `p_1,p_2` are localized, each
pure colour graph has at most two perfect matchings.  If the second exists,
it differs from the first by the unique four-cycle transposition on
`p_1,p_2`.

Consequently all choices of the three-colour pure backbone form a Boolean
cube of dimension at most three: there are at most `2^3=8` backbones.  This
does not enumerate them and does not prove that their glued gain graph is
nonbipartite.  It reduces the multi-backbone compatibility problem to three
symbolic binary switches at every order `m`.

## Setup

Assume a hypothetical equality restriction

```text
P_m -> Delta_3,               m>=3,                  (1)
```

with exactly `3m+2` nonzero row cells.  Choose the mandatory coordinate
cover and let the two excess cells have the distinct source endpoints

```text
P_*={p_1,p_2}.                                       (2)
```

Fix a colour `c` and one perfect matching `M_c` contributing to the pure
word `c^m`.

## Pure matching exchange theorem

Apply the exceptional-source localization lemma to the backbone matching
`F=M_c`.  Every physical row cell eligible for the same pure word but not
the designated `M_c` cell has source endpoint in `P_*`.

Let `M'_c` be another perfect matching for `c^m`.  The symmetric difference

```text
M_c triangle M'_c                                  (3)
```

is a disjoint union of alternating cycles.  Every cycle uses at least two
new edges with distinct source endpoints.  Localization permits only
`p_1,p_2`, so (3) contains exactly one cycle and that cycle has length four.

If `M_c` matches modes `i,j` to `p_1,p_2`, respectively, then the only
possible alternative is

```text
(i,p_1),(j,p_2)  <->  (i,p_2),(j,p_1).               (4)
```

The two cross cells in (4) are unique physical matrix cells.  Hence there
is at most one matching `M'_c` distinct from `M_c`:

```text
number of pure colour-c perfect matchings <=2.        (5)
```

This conclusion remains valid when one or both cross cells are
noncoordinate: eligibility is coefficient-wise, while the symmetric
difference is taken after collapsing coloured copies to physical cells.

## The pure-backbone cube

For each colour, let `epsilon_c` record whether the optional cross matching
is chosen.  A colour with a unique pure matching has no switch; a colour
with two matchings contributes `epsilon_c in {0,1}`.  Therefore all triples

```text
H=M_0(epsilon_0) union M_1(epsilon_1) union
  M_2(epsilon_2)                                      (6)
```

form a face of the three-cube.  In particular

```text
number of pure backbones <=8.                         (7)
```

The switches are not independent at the level of the full permanent
equations; (6)--(7) classify only the choices of pure matchings.  For the
negative-gain route, they say that the all-backbone graph `Gamma^*` is the
union of at most eight canonically bipartite fibres, glued by at most three
four-cycle source swaps.

## Pure coefficient value

If the second matching exists, the pure coefficient is exactly the sum of
the two monomials:

```text
w(M_c)+w(M'_c)=lambda_c !=0.                          (8)
```

After factoring `w(M_c)`, the cross rectangle ratio `rho_c` satisfies

```text
w(M_c)(1+rho_c)=lambda_c.                             (9)
```

Unlike a mixed coefficient, (9) does not force `rho_c=-1`; in fact
`rho_c=-1` would kill the required pure coefficient.  Thus the pure switch
supplies a nonvanishing transport parameter, not another all-negative gain
edge.  Any future holonomy argument must keep this distinction.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_equality_pure_matching_cube_theorem.py
python audit_arbitrary_permanent_equality_pure_matching_cube_theorem.py
```

The scripts check the unique `2 x 2` transposition, the two-term pure
coefficient identity, and the dimension-at-most-three Boolean product.  They
are fixed symbolic checks.  The arbitrary-order proof is localization plus
the alternating-cycle decomposition above.

## Boundary

```text
pure matchings per colour at equality:     AT MOST TWO;
nontrivial pure exchange:                  UNIQUE P_1/P_2 FOUR-CYCLE;
pure backbone choices:                     BOOLEAN CUBE, DIMENSION <=3;
number of pure backbones:                  AT MOST EIGHT;
mixed matchings inside one backbone:       NOT COUNTED;
odd cycle in glued gain graph:             UNKNOWN;
global Krenn--Gu conjecture:                UNRESOLVED.
```
