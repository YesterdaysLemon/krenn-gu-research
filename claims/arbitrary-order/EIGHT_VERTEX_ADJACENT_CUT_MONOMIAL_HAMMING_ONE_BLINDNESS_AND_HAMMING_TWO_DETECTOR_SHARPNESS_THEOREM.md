# Eight-vertex adjacent-cut monomial Hamming-one blindness and Hamming-two detector sharpness theorem

## Status

**Exact characteristic-zero proof-route sharpness theorem.**  In the
invertible monomial part of the vertex-gauge common-quadratic orbit, every
nonzero pure coefficient automatically makes the whole Hamming-one mixed
shell vanish.  For every vertex pair and every base colour, however, at
least one of the four words changing exactly that pair away from the base
colour has nonzero coefficient.  Thus four pair-local Hamming-two equations
exclude the entire monomial synchronized control class.

An exact normalized eight-vertex graph in this class lies in every balanced
rank-drop locus and satisfies all `48` Hamming-one equations, while the six
same-vector root quadrics on each of two adjacent shores span all ternary
quadrics and have empty projective base locus.  One exchanged-pair
Hamming-two coefficient is `-1`.

This does not classify nonmonomial common-form gauges, nonsynchronized
members of `B_all`, or witnesses.  The entire common-quadratic orbit is
already excluded from the witness locus by the existing two-flattening rank
theorem.  The result here identifies the minimum useful mixed shell and
refutes a prescribed-gauge adjacent-cut extraction route.  The global
conjecture remains **UNRESOLVED**.

## 1. The monomial common-form coefficient formula

Let `n` be even and, in fixed target coordinate bases, let

```text
G_i e_c=a_(i,c) e_(pi_i(c)),
a_(i,c)!=0,             pi_i in S_3.                  (1)
```

Put

```text
W_ij=G_i^T G_j.                                        (2)
```

For a coordinate word `alpha` define its latent-label counts

```text
n_l(alpha)=#{i:pi_i(alpha_i)=l}.                       (3)
```

### Lemma 1 (latent parity formula)

The matching coefficient is

```text
[alpha]T_W
 =product_i a_(i,alpha_i)
  product_(l=0)^2 (n_l(alpha)-1)!!                    (4)
```

when all three latent counts are even, and is zero otherwise.  As usual,
`(-1)!!=1`.

### Proof

An edge entry in (2) is nonzero exactly when its endpoint target colours map
to the same latent label.  A contributing perfect matching is therefore the
disjoint union of a perfect matching inside each latent-label class.  Such a
matching exists exactly when every class size is even, and then the number
of choices is the product of the three double factorials.  Every vertex
contributes its nonzero monomial scalar once, proving (4).  QED.

## 2. Hamming one is blind and four Hamming-two cells detect

Fix a base target colour `c` whose pure coefficient `[c^n]T_W` is nonzero.
Then the three counts

```text
#{i:pi_i(c)=l}                                         (5)
```

are all even.

### Theorem 2 (mixed-shell dichotomy)

1. Every word obtained from `c^n` by changing one vertex to either other
   target colour has coefficient zero.
2. Fix any vertex pair `{i,j}`.  Among the four words obtained from `c^n` by
   changing both positions `i,j` to colours different from `c`, at least one
   coefficient is nonzero.  More precisely, exactly two are nonzero when
   `pi_i(c)=pi_j(c)`, and exactly one is nonzero otherwise.

### Proof

A one-vertex change replaces one latent label by a distinct label, making
exactly two previously even counts odd.  Formula (4) gives zero.

For two vertices put

```text
r=pi_i(c),       s=pi_j(c).                            (6)
```

If `r=s`, choose either latent label `t!=r` and use the unique non-`c`
target colours at `i,j` that both map to `t`.  The change removes two `r`
labels and adds two `t` labels, preserving every parity.  These are the
exactly two successful cells.

If `r!=s`, use the unique non-`c` colours that swap the two latent labels:
`i` moves from `r` to `s`, while `j` moves from `s` to `r`.  All counts are
unchanged.  Each of the other three cells flips two latent parities, so this
swap is the unique successful cell.  Formula (4) and the nonzero scalars make
every successful coefficient nonzero.  QED.

Thus the four pair-local Hamming-two target equations are a uniform detector
for this suborbit, whereas the complete Hamming-one shell supplies no
detector at all.

## 3. An exact adjacent-cut control

Take eight vertices and set `W_ij=G_i^T G_j`, with

```text
G_1=I,
G_2=[-1  0  0; 0  0 -1; 0 -1  0],
G_3=diag(-1,-1,1),
G_4=[ 0  1  0; 0  0 -1; 1  0  0],
G_5=[ 0 -1  0;-1  0  0; 0  0 -1],
G_6=-I,
G_7=[ 0  0 -1;-1  0  0; 0 -1  0],
G_8=[ 0  0 -1/3; 0 -1/3 0;-1/3 0 0].                 (7)
```

Every `G_i` and every edge block is invertible, and

```text
G_i^(-T) W_ij G_j^(-1)=I                              (8)
```

on all `28` edges.  The existing common-quadratic orbit theorem therefore
puts every balanced eight-column sensor at rank at most seven.

Direct enumeration of the `105` perfect matchings gives

```text
([0^8]T_W,[1^8]T_W,[2^8]T_W)=(1,1,1),
all 48 Hamming-one coefficients=0,
[00022000]T_W=-1.                                     (9)
```

The last word changes the exchanged vertices `4,5` of the adjacent shores

```text
R={1,2,3,4},       R'={1,2,3,5}.                      (10)
```

For a shore, put the same target-gauge vector `x` into every root and write
the six quadrics `x^T W_ij x` as columns in the monomial row basis

```text
(x_0^2,x_1^2,x_2^2,x_0x_1,x_0x_2,x_1x_2),            (11)
```

with edge columns in lexicographic order.  The two coefficient matrices are

```text
C_R=
[-1 -1  0  1  0  0;
  0 -1  0  0  0  0;
  0  1  0  0  1  0;
  0  0  1  0 -2 -1;
  0  0  1  0  0  1;
 -2  0 -1  0  0  1],          det C_R=4,             (12)

C_R'=
[-1 -1  0  1  0  0;
  0 -1  0  0  0  0;
  0  1 -1  0  0 -1;
  0  0 -2  0  1  2;
  0  0  0  0  1  0;
 -2  0  0  0  1  0],          det C_R'=-8.            (13)
```

Hence each six-quadric ideal has full degree-two part and empty projective
base locus in the prescribed same-vector gauge.  The graph is nevertheless
latently synchronized by (8).  It refutes only the implication

```text
two adjacent balanced rank drops
+ nonzero pure coefficients
+ all Hamming-one mixed equations
  => compatible prescribed-gauge basepoints.          (14)
```

The Hamming-two failure in (9) keeps it outside the witness locus.

## 4. Scope and next use

The exact boundary is

```text
monomial common-form + nonzero pure => H1 vanishes:   PROVED;
four pair-local H2 equations detect the suborbit:     PROVED;
adjacent fixed-gauge basepoint from rankdrop+pures+H1: FALSE;
nonmonomial synchronized H2 detector:                 NOT CLAIMED;
nonsynchronized B_all H2 detector:                    OPEN;
global Krenn--Gu conjecture:                           UNRESOLVED.          (15)
```

For the universal adjacent-cut consequence, use the
[`five-root three-colour boundary-incidence theorem`](EIGHT_VERTEX_FIVE_ROOT_THREE_COLOUR_BOUNDARY_INCIDENCE_CODIMENSION_THREE_THEOREM.md).
Once its three colour products vanish on a five-root zero, varying only the
three complement vectors supplies no additional equation on the internal
ten-block system.  A stronger Hamming-two elimination must couple outside
blocks or several overlapping five-sets; no such independence is inferred
here.

## Focused replay

Run the shared exact replay:

```text
uv run --with sympy python claims/arbitrary-order/verify_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
python -I claims/arbitrary-order/audit_eight_vertex_five_root_three_colour_boundary_envelope_and_adjacent_cut_sharpness.py
```

The primary checks every local permutation case, counts all `105216`
eight-vertex permutation tables with nonzero pure parity, evaluates the
displayed coefficients from all `105` matchings, and verifies (8), (12), and
(13) exactly.  The independent audit uses standard-library `Fraction`, a
different matching recursion, direct determinants, and the nine possible
latent-label pair cases.  Neither script samples parameters.

## Dependencies and lineage

- [`BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md`](BALANCED_COMMON_QUADRATIC_ORBIT_RANK_DROP_AND_FLATTENING_EXCLUSION_THEOREM.md)
- [`BALANCED_ROOT_QUADRIC_BASEPOINT_PERMANENT_RESTRICTION_AND_GAUGE_SHARPNESS_THEOREM.md`](BALANCED_ROOT_QUADRIC_BASEPOINT_PERMANENT_RESTRICTION_AND_GAUGE_SHARPNESS_THEOREM.md)
