# Generic exclusion theorem for normalized `q4_211`

## Status

This note exactly excludes normalized `q4_211` over `C` on the open
parameter stratum

```text
a b c != 0.                                         (1)
```

It is the logical closure of the parallel, adjacent, and disjoint
singleton-normal analyses in the linked constituent theorems.  The
proof is analytic and uses only small permanent tensors, projective
pencils, conic polarity, binary polarization, and flattening ranks.
It does not enumerate ambient maps or Grassmannians.

The theorem does **not** exclude the boundary `abc=0`, all normalized
`q4_211`, the other unresolved local strata of `P_5 -> Delta_3`, or
the global Krenn--Gu conjecture.

## Exhaustive incidence trichotomy

The two embedded singleton-colour `P_4` contractions have independent
normals

```text
h_1=(b,0,0,-1,0),
h_2=(c,0,0,0,-1).
```

The decomposable-`P_4` rank-drop theorem puts each normal in at least
two of the four remaining row spaces.  Let their containment sets be

```text
S_1={i:h_1 in R_i},
S_2={i:h_2 in R_i}.
```

There are only three possibilities:

1. `S_1 intersect S_2` is empty.  Then both sets have size two and
   partition the four modes: this is exact disjoint incidence.
2. Their intersection has one element after selecting two incidences
   from each set: this is adjacent incidence.
3. Their intersection has at least two elements: select a parallel
   common pair.

The parallel-incidence theorem applies on `bc != 0` and forces a third
common mode.  In particular the parallel case can be reselected as
adjacent.  Thus it remains only to exclude exact disjoint and adjacent
incidence.

## Exact disjoint incidence

On (1), the mixed contraction

```text
(u_0,h_1,h_2) contract P_5
```

is a nondegenerate ternary conic.  Its four cross-pair images have
rank at most one.  Conic polarity forces one normal pair to share the
restricted kernel `C(e_1+e_2)`.  Repeated-normal contractions propagate
that kernel and leave only

```text
(s,s,s,s)
or
(s,s,d,s),
s=e_1+e_2,
d=e_1-e_2.
```

The first architecture kills the required doubled-colour-zero
coefficient.  The second gives incompatible target colours to the
rows `h_2,n`.  Hence exact disjoint incidence is empty.

See:

- [`P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md`](P5_Q4_211_DISJOINT_CONIC_POLARITY_REDUCTION.md)
- [`P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md`](P5_Q4_211_DISJOINT_EXCLUSION_THEOREM.md)

## Adjacent incidence

At a common `h_1,h_2` mode, injectivity of pullback says that the two
cross residuals are not both zero.

If both are nonzero, they produce a marked sharp restriction

```text
P_4 -> Delta_2.
```

The all-rank-two marked family violates a complement-pairing
flattening.  Every rank-one slice boundary belongs to one of two
alternating determinant strata; triple-`n` and double-`n`
contractions exclude the two strata.  Thus the two-cross branch is
empty.

See:

- [`P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md`](claims/p4/classifications/P4_MARKED_DELTA2_SLICE_CLASSIFICATION.md)
- [`P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md`](P5_Q4_211_MARKED_DELTA2_PAIR_IMAGE_OBSTRUCTION.md)
- [`P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md`](claims/p4/classifications/P4_MARKED_DELTA2_ALTERNATING_GATE_CLASSIFICATION.md)
- [`P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md`](P5_Q4_211_ALTERNATING_GATE_OBSTRUCTION.md)

If exactly one cross residual is nonzero, a fourth normal

```text
n=(0,0,0,c,b)
```

occurs at another mode and always pulls back from target colour zero.
A projective normal pencil and a nondegenerate direction conic reduce
the branch to only two gates:

```text
span(u_1,u_2) subset R_Z,                            (2)
```

or

```text
L_A(e_1+e_2)=0
or
L_Y(e_1+e_2)=0.                                     (3)
```

For (2), the conic image fixes the target rows of `u_1,u_2` to colours
one and two.  The common mode and opposite-pencil mode send
`span(e_1,e_2)` to the wrong singleton colour, so a repeated
`u_2` or `u_1` contraction has a required pure coefficient equal to
zero.

For (3), binary polarity propagates the kernels to

```text
A:s,  Y:d,  D:s.
```

The doubled-colour coefficient then gives `L_C(s)` a nonzero
target-colour-zero component.  The nonzero `P_3(w_-)` chart forces
`L_D(w_-)=0`, while the simultaneous zero `P_3(w_+)` chart forces
`L_C(s)` onto target colour two.  This contradiction excludes the
last gate.

See:

- [`P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md`](P5_Q4_211_ONE_CROSS_PENCIL_SATURATION_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_CONIC_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md`](P5_Q4_211_ONE_CROSS_TWO_GATE_REDUCTION.md)
- [`P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_DIRECTION_PLANE_OBSTRUCTION.md)
- [`P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md`](P5_Q4_211_ONE_CROSS_COMMON_KERNEL_OBSTRUCTION.md)

Thus adjacent incidence is empty on (1).

## Conclusion

The incidence trichotomy is exhaustive.  Parallel incidence reselects
as adjacent, and both exact disjoint and adjacent incidence are empty.
Therefore no normalized `q4_211` restriction exists on `abc != 0`.

The only remaining normalized `q4_211` parameter strata are

```text
a=0, b c != 0;
b=0, a c != 0;
c=0, a b != 0,                                      (4)
```

where the last two are colour symmetric.

## Verification

Run:

```text
python verify_p5_q4_211_generic_exclusion.py
python audit_p5_q4_211_generic_exclusion.py
```

These package the constituent certificate hashes and independently
check the complete two-subset incidence trichotomy.  They do not
replace the primary and audit scripts attached to each constituent
theorem.
