# The three-excess phase gluing is an `S_3` chart local system

## Status

**Exact characteristic-zero phase theorem and exact no-go.**  On the torus
where the six permutation monomials are nonzero, one exceptional three-port
coefficient forms a projective `B_3` phase point.  Choosing a different
nonzero physical term as the distinguished backbone is only an `S_3` chart
transition; it supplies no new equation.

If a Boolean two-face is additionally aligned so that its two switch
directions act by fixed port permutations, path independence forces those
permutations to commute.  Thus an aligned face with distinct transpositions,
or with one transposition and one three-cycle, is impossible.  However, exact
complex chart-local-system countermodels realize both surviving abelian
transport types: one fixed transposition and the cyclic group of order three.
They do not construct distinct physical pure backbones.

Therefore phase equations, shared physical coefficients, and Boolean gluing
alone do not exclude the `3m+3` layer.  A global proof still needs an
incidence theorem forcing an aligned same-word face with nonabelian transport,
or an isolation theorem not contained in the phase variety.

The inputs are the port-permutation normal form
[`ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md`](ARBITRARY_PERMANENT_THREE_EXCESS_PORT_PERMUTATION_THEOREM.md)
and the conformal--Birkhoff reduction
[`ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_BIRKHOFF_REDUCTION.md`](ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_BIRKHOFF_REDUCTION.md).

## The projective `B_3` phase point

Index the six physical port terms by `sigma in S_3` and write their
homogeneous weights as `w_sigma`.  The forbidden mixed coefficient and the
unique toric circuit are

```text
sum_(sigma in S_3) w_sigma=0,                       (1)
w_e w_(123) w_(132)=w_(12) w_(13) w_(23).           (2)
```

On the full-torus chart `product_sigma w_sigma!=0`, normalize at `w_e`:

```text
(w_e,w_(12),w_(13),w_(23),w_(123),w_(132))
  =(1,a,b,c,u,v).                                   (3)
```

Then (1)--(2) become

```text
1+a+b+c+u+v=0,              uv=abc.                 (4)
```

This is the phase variety already obtained from the `3 x 3` permanent and
the cubic circuit of the Birkhoff polytope `B_3`.

## Exact chart action

Suppose the same physical coefficient is represented with term `tau` as the
distinguished diagonal.  Relabeling the ports gives

```text
(R_tau w)_rho = w_(tau rho)/w_tau.                  (5)
```

Left multiplication permutes the six terms.  If `tau` is even, it preserves
the two parity triples in (2); if `tau` is odd, it exchanges them.  If `T`
denotes the left side minus the right side of (2), then exactly

```text
T(R_tau w)=sgn(tau) T(w)/w_tau^3.                  (5a)
```

Thus the toric polynomial is anti-invariant for odd `tau`, while its zero
locus and equation are invariant.  The zero-sum form scales by `1/w_tau`.

For example,

```text
R_(12)(a,b,c,u,v)
  =(1/a, v/a, u/a, c/a, b/a),                       (6)

R_(123)(a,b,c,u,v)
  =(b/u, c/u, a/u, v/u, 1/u).                       (7)
```

Thus two fibres that merely select different representatives of the same
word/coefficient are two affine charts of one point.  Repeating (4) in both
charts cannot create an independent phase equation.

## Incidence-aligned faces and flat port transport

Consider a square of selected pure backbones with switch directions `c,d`.
Call it **incidence aligned** when all four vertices represent the same word,
use one fixed ordering of the exceptional modes and ports, and traversing a
positively oriented edge in direction `j` sends the distinguished physical
matching term to its translate by one fixed permutation `tau_j`, independently
of the other bit.  Traversing backwards uses `tau_j^(-1)`; a Boolean toggle
does not assert `tau_j^2=e`.

The physical term at the opposite corner must be independent of the path.
Consequently

```text
tau_c tau_d=tau_d tau_c.                            (8)
```

The centralizer of a transposition in `S_3` is the order-two subgroup that it
generates; the centralizer of a three-cycle is `A_3`.  Therefore a flat
constant-transport cube has abelian image of type

```text
1,            one fixed C_2,            or C_3.     (9)
```

In particular, an aligned face excludes:

- two different `C_2` port transpositions; and
- a `C_2` transposition together with a `C_3` rotation.

The existence of such an aligned face is **not** automatic.  The conformal
matching from matching-covered graph theory need not lie in a selected pure
backbone union, and the same-word condition is a separate coloured extension
problem.

## Exact abstract countermodel for `C_2` transport

Let

```text
theta=-2+sqrt(3),             theta+theta^(-1)=-4,

X_theta = [[1, 1, theta^(-1)],
           [1, 1, 1],
           [theta, 1, 1]].                           (10)
```

Its six physical term weights are

```text
(1,a,b,c,u,v)=(1,1,1,1,theta,theta^(-1)).           (11)
```

Thus

```text
per(X_theta)=4+theta+theta^(-1)=0,
uv=abc=1.                                           (12)
```

On a Boolean cube of any dimension at most three, let the distinguished term
at vertex `t` be

```text
tau_t=(12)^(sum_j t_j mod 2).                        (13)
```

Every abstract vertex uses the same phase matrix `X_theta`; only its affine
chart changes.  Equations (1)--(4) hold in every chart.  Every formal
edge-transition term ratio is `w_(12)/w_e=1` or its reciprocal, so phase
transport alone produces no negative gain.  This is an exact countermodel to
the abstract chart local system in dimensions one, two, and three.  It is not
a realization of distinct pure backbones, their shared-cell incidence, their
pure-switch binomials, or a full permanent restriction.

## Exact abstract countermodel for `C_3` transport

Let `r=(123)` and instead put

```text
tau_t=r^(sum_j t_j mod 3).                           (14)
```

The successive physical switch ratios around the three charts are

```text
theta,              theta^(-2),              theta. (15)
```

None equals `-1`, while every abstract chart is again a rebase of the same
matrix and satisfies the permanent and toric equations.  Pure support
geometry already limits simultaneous `C_3` switch colours, but the abstract
phase local system supplies no additional exclusion.

## What physical sharing actually identifies

There is a strict incidence hierarchy.

1. One shared matrix entry identifies no normalized phase coordinate: the
   gains are row/column-scale-invariant ratios.
2. An anchored numerator/denominator pair in one row identifies a directed
   arc ratio `X_rs/X_rr`.
3. Identifying two oppositely anchored row ratios identifies one
   transposition gain.  Sharing the corresponding physical `2 x 2` rectangle
   is one sufficient way to do this.
4. Equality of the three scalar gains `a,b,c` still fixes only the unordered
   pair `{u,v}`, because the two oriented triangle gains are the roots of

```text
T^2+(1+a+b+c)T+abc.                                 (16)
```

5. By contrast, physically sharing all three `2 x 2` rectangles shares all
   nine matrix entries, so it fixes `u` and `v` individually.  Sharing one
   oriented triangle gain together with `a,b,c` also fixes the other.

The first potentially contradictory datum is therefore nontrivial transport
or holonomy of anchored ratios around an incidence-aligned face, not another
copy of a single-fibre equation.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_three_excess_b3_phase_holonomy_nogo.py
python claims/arbitrary-order/audit_arbitrary_permanent_three_excess_b3_phase_holonomy_nogo.py
```

The primary verifier constructs `S_3`, checks all six chart transitions and
both homogeneous equations, derives (6)--(7), and verifies the `C_2` and
`C_3` countermodels over `Q(sqrt(3))`.  The independent no-import audit uses
a separate permutation representation and exact quadratic-field arithmetic.
The six-element group check is an audit of the symbolic formulas, not a
graph, support, matching, or quadruplet enumeration.

## Boundary

```text
S_3 rebase action on one full-torus phase point: PROVED;
phase/toric zero loci under backbone choice:    PROVED;
aligned-face commuting condition:               PROVED, CONDITIONAL ON ALIGNMENT;
distinct C2 or mixed C2/C3 aligned face:         EXCLUDED;
abstract constant C2 and C3 phase gluing:        EXACT COUNTERMODELS;
physical realization of those glued cubes:      NOT CLAIMED;
existence of an aligned same-word face:          NOT PROVED;
forced nonabelian port holonomy:                 NOT PROVED;
exclusion of support 3m+3:                       NOT PROVED;
global Krenn--Gu conjecture:                     UNRESOLVED.
```
