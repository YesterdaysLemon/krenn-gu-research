# Rank classification for the GHZ mixed second-jet quotient

## Status

**Exact characteristic-zero second-jet theorem.**  Let

```text
Q=K^3/<(1,1,1)>,
S_a=ker(a),  S_b=ker(b),
a(1,1,1) != 0,  b(1,1,1) != 0,
```

and define the coordinatewise-product map

```text
mu_(a,b): S_a tensor S_b -> Q,
mu_(a,b)(u,v)=[u_0 v_0,u_1 v_1,u_2 v_2].         (1)
```

Its rank is always one or two.  It has rank one exactly when some coordinate
`c` satisfies

```text
a_c=b_c=0,
a_p b_p=a_q b_q,                                  (2)
```

where `{p,q}` is the complementary coordinate pair.  Outside these three
explicit resonant loci, `mu_(a,b)` is onto the two-dimensional quotient.

For a hypothetical GHZ graph witness with projectively constant root--blocker
first derivatives, `S_a,S_b` are the scalar tangent complements at two roots
and (1) is exactly the diagonal quotient of their mixed GHZ Hessian.  The
hafnian mixed-derivative recursion therefore forces the accessible
double-deletion companion-cofactor classes to span `im(mu_(a,b))`.  In
particular, outside (2) at least two independent second-cofactor quotient
classes are necessary.

This is a necessary higher-jet condition, not a proof that the required
cofactors cannot occur.  Cofactor realizability, the arbitrary-order
local-to-global reduction, and the global Krenn--Gu conjecture remain
**UNKNOWN** or **UNRESOLVED**.  No finite field is used.

## GHZ origin of the map

Fix two fully supported roots and pass to logarithmic tangent coordinates

```text
u_c=y_c/x_i[c],       v_c=z_c/x_j[c].             (3)
```

Normalize the surviving GHZ diagonal vector to `(1,1,1)`.  A projectively
constant root--blocker derivative supplies scalar covectors whose kernels in
the logarithmic coordinates are two-dimensional complements to the constant
line.  After normalization they are `S_a` and `S_b`, with
`a(1,1,1)=b(1,1,1)=1`.

The mixed derivative of the GHZ tensor has diagonal coefficient vector

```text
(u_0 v_0,u_1 v_1,u_2 v_2).                       (4)
```

Modulo the original scalar diagonal, (4) is precisely (1).

On the graph side, differentiating the hafnian at the two roots partitions
the surviving matchings into two types:

1. the roots pair to each other, giving their tangent--tangent edge value
   times the complementary two-deletion cofactor;
2. the roots pair through two disjoint effective companion edges, giving the
   product of their endpoint covectors times the complementary four-deletion
   cofactor.

Root--blocker terms vanish on `S_a,S_b`.  Hence the image of (1) must lie in
the span of the quotient classes of exactly those accessible cofactors.  This
is the asserted second-cofactor span necessity.

## Exact rank calculation

First assume that some coordinatewise product `a_k b_k` is nonzero.  Permute
coordinates so `k=0`.  Bases of the two kernels are

```text
u_1=(-a_1,a_0,0),   u_2=(-a_2,0,a_0),
v_1=(-b_1,b_0,0),   v_2=(-b_2,0,b_0).             (5)
```

Use quotient coordinates

```text
pi(w)=(w_1-w_0,w_2-w_0).
```

The four columns `pi(u_i coordinatewise-product v_j)` form

```text
[ a0*b0-a1*b1   -a1*b2   -a2*b1        -a2*b2      ]
[    -a1*b1     -a1*b2   -a2*b1   a0*b0-a2*b2 ].  (6)
```

Its six `2 x 2` minors are, up to repetition,

```text
-a0*a1*b0*b2,
-a0*a2*b0*b1,
 a0*b0*(a0*b0-a1*b1-a2*b2),
0.                                                   (7)
```

Because `a0*b0 != 0`, rank at most one is equivalent to

```text
a1*b2=0,       a2*b1=0,
a0*b0=a1*b1+a2*b2.                                (8)
```

The two choices putting both `a1,a2` or both `b1,b2` equal to zero contradict
the last equation.  The remaining choices are exactly

```text
a1=b1=0,  a0*b0=a2*b2,
or
a2=b2=0,  a0*b0=a1*b1,                            (9)
```

which are (2) for `c=1` or `c=2`.  The matrix is nonzero, so the rank is
exactly one there and two otherwise.

If `a_k b_k=0` for every `k`, the supports of `a` and `b` are disjoint.  If
their union omits a coordinate `c`, then `a_c=b_c=0` and both products in
(2) are zero; direct kernel bases give rank one.  If their disjoint supports
cover all three coordinates, one support has size one and the other size two;
the two coordinate axes in the product image remain independent modulo the
constant line, so the rank is two.  This completes the classification.

## Consequences and boundary

For the uniform scalar splitting used in the symmetric tangent-cycle
construction, `a=b=e_0^*`.  None of (2) holds, so the mixed GHZ quotient has
rank two.  The single common-edge cofactor line is therefore insufficient,
recovering and strengthening the selected-direction obstruction in
[`ROOT_TANGENT_MINIMAL_CYCLE_SECOND_JET_OBSTRUCTION.md`](ROOT_TANGENT_MINIMAL_CYCLE_SECOND_JET_OBSTRUCTION.md).

On a resonant locus (2), one second-cofactor quotient line is necessary but
the theorem does not assert it is sufficient.  Away from resonance, two
independent accessible classes are necessary but may still fail the complete
mixed-colour or higher-order identities.

## Replay

```powershell
uv run --with sympy python verify_root_mixed_second_jet_quotient_rank_classification.py
python audit_root_mixed_second_jet_quotient_rank_classification.py
```

The primary factors the symbolic minors in (7) and checks all normalized
integer covector pairs in the box `[-2,2]^6`.  The no-import audit uses exact
rational kernel bases, coordinate permutations, and a separate box
`[-3,3]^6` after primitive projective reduction.
