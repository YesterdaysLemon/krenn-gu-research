# Classification of the five mixed determinantal primes

## Status

This is an exact characteristic-zero classification of the five
minimal primes in the mixed zero-product normal form of
[`P4_MIXED_ORIENTATION_PURE_COMPONENT.md`](../components/mixed-orientation/P4_MIXED_ORIENTATION_PURE_COMPONENT.md).

On the dense overlapping-support chart used there, the five primes
produce no component orbit beyond the seven certified at that
checkpoint:

1. two primes give the sixth five-dimensional component;
2. one prime is a subfamily of the six-dimensional component;
3. the remaining two primes are source/mode symmetry charts of the
   split-cubic components `L_2` and `L_1`.

This closes the dense five-prime determinantal chart, not the complete
pure-compression locus.  A disjoint-support mixed star outside this
chart has since produced an eighth component in
[`P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md`](../components/disjoint-mixed-star/P4_DISJOINT_MIXED_STAR_PURE_COMPONENT.md).
Degenerate normalizations, other exceptional graphs, and lower-rank
boundary charts remain.

## The determinantal chart

Use

```text
U_1=span((0,0,1,1),(a,1,c,d)),
U_2=span((p,1,0,q),(-1,0,1,0)),
U_3=span((1,0,1,0),(0,0,-1,1)).
```

The rank-at-most-two ideal for the three nonzero contractions to
`U_0` has the five minimal primes

```text
P1=(c+p+q,a+d),
P2=(d+q,a+c+p),
P3=(c,a+d+p+q),
P4=(c-d+p-q,a),
P5=(c-d,a+p-q).                                  (1)
```

The first and third primes are one component orbit by the explicit
mode swap already proved in the mixed-orientation component theorem.

## The lower-rank prime

On `P2`, write `p=-a-c,q=-d`.  A row basis for the four planes is

```text
U_0=span((1,0,1,0),(-1,0,0,1)),
U_1=span((0,0,1,1),(a,1,c,d)),
U_2=span((-a-c,1,0,-d),(-1,0,1,0)),
U_3=span((1,0,1,0),(0,0,-1,1)).                  (2)
```

Row reduction proves that (2) is exactly the subfamily

```text
b=1/a,             e=0
```

of the six-dimensional component in
[`P4_SIX_DIMENSIONAL_PURE_COMPONENT.md`](../components/six-dimensional/P4_SIX_DIMENSIONAL_PURE_COMPONENT.md).
Thus `P2` is not another component orbit.

## The two split-cubic primes

For `P4`, put `a=0,c=d-p+q`.  A polynomial row basis for `U_0` is

```text
U_0=span(
 (-dp,d+q,q(-d+p-q),0),
 (-1,0,0,1)).                                     (3)
```

For `P5`, put `c=d,a=q-p` and use

```text
U_0=span(
 (q(d-p+q),-d-q,dp,0),
 (-1,0,0,1)).                                     (4)
```

Swap source coordinates zero and one.  If
`B_0,B_1,B_2,B_3` denote the planes in the split-cubic normal form of
[`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md),
then reorder them as

```text
(B_2,B_0,B_1,B_3).                                (5)
```

For `P4`, take the `L_2` parameters

```text
S=p,
D=q,
G=q(p-q-d)/(d+q).                                 (6)
```

The `L_2` relation gives

```text
T=D+G-S=-dp/(d+q).
```

The four planes obtained from (5)--(6) have exactly the same Pluecker
coordinates as (3), `U_1,U_2,U_3`.

For `P5`, take the `L_1` parameters

```text
S=p,
D=q,
G=-dp/(d+q).                                      (7)
```

Now

```text
T=-D+G+S=-q(d-p+q)/(d+q),
```

and the same source swap and mode reorder reproduce (4),
`U_1,U_2,U_3`.

Therefore `P4` is a dense chart of `L_2` and `P5` is a dense chart of
`L_1`, up to the allowed symmetries.

## Consequence

The five-prime list (1) contributes exactly four already known
component closures:

```text
P1,P3 -> sixth mixed-orientation component,
P2    -> six-dimensional component,
P4    -> L_2,
P5    -> L_1.                                     (8)
```

No further component arises on this dense mixed determinantal chart.
The disjoint-support eighth component lies outside the normalization
used here, and the eight-component lower bound remains non-exhaustive
globally.

## Verification

Run

```text
python claims/p4/classifications/verify_p4_mixed_determinantal_prime_classification.py
python claims/p4/classifications/audit_p4_mixed_determinantal_prime_classification.py
```

The primary verifier reconstructs the five prime specializations,
checks every permanent, proves the `P2` embedding, and verifies all
four symbolic Pluecker identities in (6)--(7).  The independent audit
replays the plane identifications with a separate modular permanent
and Pluecker implementation over two finite fields.
