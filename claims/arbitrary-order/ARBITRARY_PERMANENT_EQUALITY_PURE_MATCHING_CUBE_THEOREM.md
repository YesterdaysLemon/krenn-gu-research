# Arbitrary permanent equality pure-matching cube theorem

## Status

This is an exact arbitrary-order structural theorem for the `3m+2` equality
stratum.  After the two exceptional sources `p_1,p_2` are localized, each
pure colour graph has at most two perfect matchings.  If the second exists,
it differs from the first by the unique four-cycle transposition on
`p_1,p_2`.

The physical-cell geometry collapses the apparent three-cube further.  Any
pure switch must use both excess cells.  If their mode endpoints are
distinct, at most one colour can switch.  Multiple switches require the two
excess cells to be noncoordinate and co-located at one mode.  Local concision
and the total mode-degree excess then permit at most two switchable colours.
Thus there are at most four pure backbones at every order `m`.

This does not enumerate them.  It reduces the multi-backbone compatibility
problem to at most two symbolic binary switches.  Subsequent zero-, one-,
and two-switch theorems exclude every face and hence all `3m+2` equality;
see `ARBITRARY_PERMANENT_EQUALITY_TWO_SWITCH_EXCLUSION_THEOREM.md` for the
final closure and strict support corollary.

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

## The apparent pure-backbone cube

For each colour, let `eta_c` record whether the optional cross matching
is chosen.  A colour with a unique pure matching has no switch; a colour
with two matchings contributes `eta_c in {0,1}`.  Therefore all triples

```text
H=M_0(eta_0) union M_1(eta_1) union M_2(eta_2)        (6)
```

initially form a face of the three-cube.

## Physical-cell dichotomy and dimension at most two

Let the unique excess cell at source `p_s` be

```text
e_s=r_(a_s,p_s).                                     (7)
```

If colour `c` has two pure matchings, each source must supply two distinct
colour-`c` eligible cells.  The mandatory cover supplies only
`b_(p_s,c)`; every other mandatory cell at that source is a different
coordinate colour.  Hence the second eligible cell is necessarily `e_s`,
and `e_s[c]!=0`.  In particular, no pure switch can avoid either excess
cell.

### Distinct excess modes

If `a_1!=a_2`, the four-cycle uses those two modes and forces

```text
b_(p_1,c)=r_(a_2,p_1),
b_(p_2,c)=r_(a_1,p_2).                               (8)
```

Two switchable colours would require their distinct mandatory coordinate
covectors in the same physical cross cells.  Hence

```text
number of switchable colours <=1 if a_1!=a_2.         (9)
```

The same conclusion holds if either `e_s` is coordinate, regardless of mode
placement: every switchable colour must occur nontrivially in both `e_1` and
`e_2`, so it must equal the singleton colour of that coordinate excess cell.

### Co-located excess modes

Suppose `a_1=a_2=a`.  A four-cycle cannot use the two excess edges in one
matching because they share mode `a`.  Instead there is a second common mode
`b_c!=a` such that

```text
b_(p_1,c)=r_(b_c,p_1),
b_(p_2,c)=r_(b_c,p_2).                               (10)
```

The two matchings pair `a` to one exceptional source and `b_c` to the other,
then transpose them.  Different switchable colours require distinct modes
`b_c`; otherwise two independent coordinate covectors would again occupy
one physical cell.

Both nonmandatory cells are at `a`, so every cell at `b_c` belongs to the
mandatory coordinate cover.  Let

```text
d_i=3+varepsilon_i,       sum_i varepsilon_i=2        (11)
```

be the equality mode-degree ledger.  At mode `b_c` there are two coordinate
rows of colour `c`.  Because the mode is coordinate-only, local rank three
requires at least one row in each of the other two coordinate directions,
so

```text
d_(b_c)>=4,       varepsilon_(b_c)>=1.               (12)
```

If `k` colours are switchable, their `b_c` are distinct, and therefore

```text
k+varepsilon_a<=2.                                  (13)
```

Consequently `k<=2`.  The case `k=2` is possible only in the ledger shape

```text
both e_1,e_2 noncoordinate at the same mode a,
varepsilon_a=0,
two distinct common modes b_c,b_d with
varepsilon_(b_c)=varepsilon_(b_d)=1.                 (14)
```

In particular

```text
number of switchable colours <=2,
number of pure backbones <=4.                        (15)
```

The switches are not independent at the level of the full permanent
equations; (6)--(15) classify only the choices of pure matchings.  For the
negative-gain route, they say that the all-backbone graph `Gamma^*` is the
union of at most four canonically bipartite fibres, glued by at most two
four-cycle source swaps.  Outside the co-located two-noncoordinate branch it
is the union of at most two fibres.

## Pure coefficient value

If the second matching exists, the pure coefficient is exactly the sum of
the two monomials:

```text
w(M_c)+w(M'_c)=lambda_c !=0.                         (16)
```

After factoring `w(M_c)`, the cross rectangle ratio `rho_c` satisfies

```text
w(M_c)(1+rho_c)=lambda_c.                            (17)
```

Unlike a mixed coefficient, (17) does not force `rho_c=-1`; in fact
`rho_c=-1` would kill the required pure coefficient.  Thus the pure switch
supplies a nonvanishing transport parameter, not another all-negative gain
edge.  Any future holonomy argument must keep this distinction.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_equality_pure_matching_cube_theorem.py
python claims/arbitrary-order/audit_arbitrary_permanent_equality_pure_matching_cube_theorem.py
```

The scripts check the unique `2 x 2` transposition, the two-term pure
coefficient identity, the distinct-mode physical-cell collision, and the
co-located mode-degree ledger.  They are fixed symbolic checks.  The
arbitrary-order proof is localization plus the alternating-cycle,
cell-incidence, and local-concision argument above.

## Boundary

```text
pure matchings per colour at equality:     AT MOST TWO;
nontrivial pure exchange:                  UNIQUE P_1/P_2 FOUR-CYCLE;
pure backbone choices:                     BOOLEAN CUBE, DIMENSION <=2;
number of pure backbones:                  AT MOST FOUR;
zero-switch face:                          EXCLUDED SUBSEQUENTLY;
two-switch branch:                         CO-LOCATED NONCOORDINATE EXCESS;
all equality faces:                        EXCLUDED SUBSEQUENTLY;
mixed matchings inside one backbone:       NOT COUNTED;
odd cycle in glued gain graph:             UNKNOWN;
global Krenn--Gu conjecture:                UNRESOLVED.
```

See `ARBITRARY_PERMANENT_EQUALITY_ZERO_SWITCH_EXCLUSION_THEOREM.md` for the
zero-face exclusion.
