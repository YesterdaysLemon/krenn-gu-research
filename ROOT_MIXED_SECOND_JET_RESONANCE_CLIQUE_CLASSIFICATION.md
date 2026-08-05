# Pairwise rank-one resonance cliques for the GHZ mixed second jet

## Status

**Exact characteristic-zero structural theorem.**  Let `r>=3`, and let

```text
a_i in P((K^3)^*),             a_i(1,1,1) != 0
```

be the scalar tangent covectors at `r` roots.  Suppose the mixed-Hessian
quotient map

```text
ker(a_i) tensor ker(a_j) -> K^3/<(1,1,1)>
```

has rank one for every distinct pair `i,j`.  Then exactly one of the
following occurs.

1. There is a coordinate `c` such that every `a_i` is the same projective
   covector `e_p^*+e_q^*`, where `{p,q}` is the complementary pair.
2. `r=3`, and the three projective covectors are
   `e_0^*,e_1^*,e_2^*` in some order.

Conversely, both displayed patterns have pairwise rank one.  In particular,
for `r>=4` only the first pattern is possible.

The theorem combines with
[`ROOT_MIXED_SECOND_JET_QUOTIENT_RANK_CLASSIFICATION.md`](ROOT_MIXED_SECOND_JET_QUOTIENT_RANK_CLASSIFICATION.md): unless the root tangent covectors have one of these exceptional global
patterns, at least one root pair needs two independent accessible
double-deletion cofactor quotient classes.

This does not prove that either exceptional pattern is graph/hafnian
realizable, nor that two cofactor classes can or cannot be supplied on a
nonresonant pair.  The arbitrary-order local-to-global reduction and the
global Krenn--Gu conjecture remain **UNRESOLVED**.  No finite field is used.

## Pairwise criterion

The preceding quotient-rank theorem says that a pair `a,b` has rank one if
and only if some coordinate `c` satisfies

```text
a_c=b_c=0,             a_p b_p=a_q b_q,          (1)
```

where `{p,q}` is the complementary pair.  We classify cliques in this
relation under the standing condition that the coordinate sum of every
covector is nonzero.

## Support classification

A fully supported covector cannot occur, because (1) requires a common zero
with every partner.

Suppose `a` has support two and zero coordinate `c`.  Any partner in (1)
must also have support two with the same zero coordinate: a singleton
partner makes exactly one of the two products in (1) nonzero.  Write on the
remaining coordinates

```text
a=(x,y),        b=(u,v),        xu=yv.            (2)
```

All four entries are nonzero.  Projectively, (2) says that the ratio of `b`
is reciprocal to the ratio of `a`.  If a third support-two covector `d`
resonates with both, its two coordinates `(z,w)` satisfy

```text
xz=yw,          yz=xw.                            (3)
```

The determinant of this system in `(z,w)` is `y^2-x^2`.  Since `d` is
nonzero, `x^2=y^2`.  The alternative `x=-y` is forbidden by
`a(1,1,1)!=0`; hence `x=y`.  Equation (2) then gives `u=v`, and every further
pairwise partner is the same projective covector.  This is pattern 1.

It remains to consider singleton supports.  Two coordinate covectors
`e_i^*,e_j^*` satisfy (1) exactly when `i!=j`: their common zero is the third
coordinate and both products in (1) vanish.  A coordinate covector does not
resonate with itself, and there are only three coordinate axes.  Thus a
clique of size at least three is exactly the three distinct axes, and it has
no fourth member.  This is pattern 2.

Support-one and support-two covectors cannot mix in a resonant pair, and the
zero covector is excluded.  The cases above are exhaustive and prove the
classification and its converse.

## Consequence for the higher-jet frontier

For four or more roots, avoiding every generic rank-two mixed quotient
forces a single zero coordinate shared by all tangent covectors and equal
weights on the other two coordinates.  Thus the open second-jet problem
splits sharply:

1. exclude or realize this uniform balanced exceptional splitting; or
2. on some nonresonant pair, analyze whether two independent accessible
   double-deletion cofactor quotient classes can satisfy all mixed-colour
   hafnian recursions.

The three-axis exception is available only for exactly three roots.  These
are reductions of the remaining problem, not closures of either branch.

## Replay

Replay the quotient-rank dependency first:

```powershell
uv run --with sympy python verify_root_mixed_second_jet_quotient_rank_classification.py
python audit_root_mixed_second_jet_quotient_rank_classification.py
```

Then run:

```powershell
uv run --with sympy python verify_root_mixed_second_jet_resonance_clique_classification.py
python audit_root_mixed_second_jet_resonance_clique_classification.py
uv run --with sympy --with ruff python -m ruff check verify_root_mixed_second_jet_resonance_clique_classification.py audit_root_mixed_second_jet_resonance_clique_classification.py
python -m py_compile verify_root_mixed_second_jet_resonance_clique_classification.py audit_root_mixed_second_jet_resonance_clique_classification.py
```

The primary checks the determinant argument symbolically and exhausts a
small exact projective box.  The no-import audit uses independent integer
normalization and a larger box, including coordinate permutations and the
absence of a fourth partner for the three-axis clique.  The finite boxes are
audits of the proved support argument, not theorem evidence by themselves.
