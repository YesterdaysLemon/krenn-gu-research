# Decorated q1 exclusion of a two-hidden run

Date: 2026-09-22

Status: exact local implication inside the minimum-density equality normal
form.  It excludes every pair of adjacent hidden transit literals; the two
end literals may be split or transit.  It therefore excludes the proposed
repeating mixed allocation on
`C_(3k)^2`, but it does not exclude arbitrary mixtures or prove WP1/SFULL.

## Proposition

Permute colors so that four consecutive state literals are

```text
(P,1) -- (Q,0) hidden transit -- (P,2) hidden transit -- (Q,1). (1)
```

No allocation hypothesis is made at the two end literals.  Assume the
empty-q1 alignment prohibition at the two transit literals.  Then
there is a mixed physical word with `q_1<=1` whose coefficient is one
nonzero matching monomial.  Hence (1) cannot occur in a WP1 array.

All entries below are entries of the actual common hollow array.  There are
no freely chosen cofactors and no division.

## Resource notation and forced maps

Let the three consecutive gadgets use resource edges

```text
I=R_P^1={s,p},     J=R_P^2={s,r},
K=R_Q^0={u,q},     L=R_Q^1={u,l}.                   (2)
```

Write `t` and `v` for the fourth ports of `P` and `Q`.  Thus
`̅I={r,t}` is the other `M_1(P)` edge, `̅K={l,v}` is the other
`M_0(Q)` edge, and `̅L={q,v}` is the other `M_1(Q)` edge.

Orient all three endpoint bijections from `P` to `Q`:

```text
g:I -> K       for labels [1,0],
f:J -> K       for labels [2,0],
h:J -> L       for labels [2,1].                    (3)
```

At the hidden literal `(Q,0)`, the unshared ports `p,r` of `I,J` must hit
the same port of `K`; the shared port `s` must hit the other.  At `(P,2)`,
the unshared ports `q,l` of `K,L` must have the same preimage in `J`; the
shared port `u` must have the other.  Therefore

```text
g(s)=f(s),       g(p)=f(r),
h=phi o f,       phi(u)=u, phi(q)=l.                 (4)
```

There are exactly two cases according to the middle bijection `f`.

## Case 1: the middle map preserves intersections

Suppose

```text
f(s)=u, f(r)=q.
```

Equation (4) gives `g(p)=q` and `h(s)=u`.  Color every component outside
`P,Q` uniformly `1`.  On `P,Q` use

```text
P_s=2; every other P port=1,
Q_u=1; every other Q port=0.                         (5)
```

This word has `q_1=1`: neither `M_1(P)` edge is completely non-1, while
exactly the edge `̅L={q,v}` in `Q` is completely non-1.  It has the
matching

```text
P_p -- Q_q     via g, labels [1,0],
P_s -- Q_u     via h, labels [2,1],
̅I in P       protected in color 1,
̅K in Q       protected in color 0,              (6)
```

times the unique protected color-1 matching outside.

This matching is unique.  The other lanes of `g,h` have the wrong source
colors.  The two lanes of `f` are blocked separately: `f(s)=u` has target
color 1 rather than 0, while `f(r)=q` has source color 1 rather than 2.
The only unequal ordered color pairs appearing on `P,Q` are `[1,0]`,
`[2,0]`, and `[2,1]`, so equality supplies no fourth compatible gadget.

The other gadget at `(P,1)` expects target color 2.  Its target component is
either `Q`, which has only colors 0 and 1 in (5), or an outside component,
which is uniformly 1.  The other gadget at `(Q,1)` similarly expects target
color 0, while `P` has only colors 1 and 2 and every outside component is
uniformly 1.  Thus neither end gadget can repair (6), regardless of whether
its resource pair coincides with or complements the displayed one.  The two
hidden literals have no other gadgets.  Hollowness forbids crossings among
the exterior color-1 components.

Thus the coefficient of (5) is the single nonzero actual product
`w_g(P_p,Q_q) w_h(P_s,Q_u)`.

## Case 2: the middle map swaps intersections

Suppose

```text
f(s)=q, f(r)=u.
```

Now (4) gives `g(p)=u` and `h(s)=l`.  Again color every outside component
uniformly `1`, and use

```text
P_s=2; every other P port=1,
Q_u=0; every other Q port=1.                         (7)
```

Here `q_1=0`.  The unique matching is

```text
P_p -- Q_u     via g, labels [1,0],
P_s -- Q_l     via h, labels [2,1],
̅I in P       protected in color 1,
̅L in Q       protected in color 1,              (8)
```

with protected color 1 outside.  The same literal check proves uniqueness:
`f(s)=q` has the wrong target color, `f(r)=u` the wrong source color, all
other local lanes have a wrong endpoint color, and the two end exits are
disabled by the same target-color check as in Case 1.

The coefficient is again one nonzero actual product.  This contradicts the
q0 part of WP1.

## Consequence and residual

Every aligned adjacent-hidden block (1) fails in one of the two cases.  In the
macro-rigid `C_(3k)^2` test, the proposed repeating allocation has color-1
literals split and color-0/color-2 literals transit, so every repeated
block is of form (1).  The family is therefore not a support or weighted
countercontrol to minimum-density WP1.

More generally, every transit literal outside a literal triangle is hidden
by the two-exception macro row.  The proposition therefore proves that the
transit vertices form an independent set on every nontriangle component of
the state graph.  The remaining structures are isolated hidden transit
vertices separated by split vertices and, before macro rigidity is imposed, literal triangles on three
distinct physical components. PSMD separately excludes the latter by a
mixed independent transversal.

## Independent finite replay

`verify_two_hidden_block.py` checks all

```text
2^4 resource-pair choices * 2 aligned middle-map cases = 32
```

literal blocks.  Sixteen have one unique low-q word and sixteen have two;
the displayed construction selects one in every case.  The replay is
corroboration of the two-case proof, not a finite-case premise.

Run:

```text
python -X utf8 claims/arbitrary-order/minimum-density-wp1/verify_two_hidden_block.py
```
