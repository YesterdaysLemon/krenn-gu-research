# Complete rank-three `(2,2,1)` mixed-star classification

## Status

**Exact characteristic-zero classification theorem.**  Suppose the
exceptional graph of a nonzero pure `P_4` restriction is a star, all three
exceptional pair images have rank three, all three leaf-pair images have rank
four, and the three unique relation matrices have ranks `(2,2,1)`.  Up to the
allowed source/mode symmetries, every such tuple lies in the Cayley-toric
family of
[`P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md`](../two-rank-two-spoke-mixed-star-component/P4_TWO_RANK_TWO_SPOKE_MIXED_STAR_COMPONENT.md).

Thus that family is not merely a component construction: it is the complete
dense rank-three graph stratum.  Special divisors where a pair rank drops,
other exceptional graphs, component exhaustiveness, and the global Krenn--Gu
problem remain open.

## Synchronize the two rank-two spokes

Put the rank-two spokes on edges `01` and `02`.  Borel tree gauge gives

```text
y_0x_1=x_0y_1,
y_0x_2=x_0y_2.                                               (1)
```

Hence the two leaves lie in the marked center's synchronizer space.  The
earlier projective-column classification leaves only two possible sources of
a full-rank leaf pair.

- Every ordinary two-dimensional synchronizer pencil is totally isotropic.
  Any two of its points obey another relation, so their pair image has rank at
  most three, contrary to the star hypothesis.
- A zero source column descends to `P_3`; support one drops a center-leaf pair
  below rank three.  Projective endpoints likewise have center-leaf rank at
  most two.
- The only dimension jumps are the full-support `2+2` presymplectic center and
  the support-two equal-ratio center.

The proof is therefore a comparison of two balanced charts, not a search over
plane coefficients.

## Full-support `2+2`: purity forces the toric family

Use

```text
a=X_0+X_1,       a_bar=X_0-X_1,
b=X_2+X_3,       b_bar=X_2-X_3
```

and the marked center `(y_0,x_0)=(a+b,b)`.  Every rank-three synchronized
finite partner is

```text
y_i=a+b-r_i b_bar-s_i a_bar,
x_i=b-s_i a_bar.                                             (2)
```

The projective coefficient of the center in a partner has a cubic rank-three
pivot, so the finite normalization loses no point of the stated stratum.

The rank-one third spoke cannot factor through `y_0`: that row has full
support and zero degree-one annihilator.  A row of the center with a nonzero
annihilator must be one of the two binary block directions `a,b`.  Source
block symmetry therefore gives

```text
y_3=b_bar,       x_3=(A,B,C,D).                              (3)
```

Put `S=s_1+s_2`, `P=s_1s_2`, `H=A+B`, `Q=C+D`, and `E=B-A`.
The all-kernel coefficient is

```text
T_0000=4(r_1+r_2),                                           (4)
```

so purity gives `r_2=-r_1=-r`.  Four remaining coefficient equations may be
written as `F_0=F_2=F_3=0`, with active coefficient `-2F_4`.  They satisfy the
small syzygies

```text
F_2-F_3=-(H+Q),
F_4-F_3=H,
F_0-F_3=-Hr^2-2H-3Q,
F_3=ES-H+QP.                                                  (5)
```

Nonzero purity means `F_4!=0`; since `F_3=0`, (5) first gives `H!=0`.
Then, successively,

```text
Q=-H,
r^2=1,
E/H=(1+P)/S.                                                  (6)
```

The leaf commutator is

```text
y_1x_2-x_1y_2
  =(r_1s_2-r_2s_1)(0,1,-1,-1,1,0)
  =rS(0,1,-1,-1,1,0).                                       (7)
```

Full leaf-pair rank forces `S!=0`, so every division in (6) is legal.  Swap
the two coordinates in the second binary block to take `r=1`.  Scale `x_3`
by `H` and add a multiple of `y_3` to make `C=D=-H/2`.  Equations (6) then
give exactly

```text
x_3 proportional to
(S-1-P, S+1+P, -S, -S).                                     (8)
```

This is the tenth-component normal form.  Its only nonzero coefficient is
`T_1111=-4S`.

The Cayley transformation `c(z)=(z-1)/(z+1)` turns the last equation in (6)
into the multiplication law

```text
c((1+s_1s_2)/(s_1+s_2))=c(s_1)c(s_2),                       (9)
```

so the classification is a toric group-law statement inside a
presymplectic plane.

## Support-two equal ratio: only a lower-rank boundary

The remaining center is `(y_0,x_0)=(a,b)`, with synchronized leaves

```text
y_i=a+beta_i b_bar,
x_i=b+alpha_i a_bar.                                        (10)
```

There are three Borel-distinct orientations of a legal rank-one spoke.

1. `y_0y_3=a a_bar=0`.  Purity forces
   `alpha_1+alpha_2=A+B=C+D=0`; substituting these identities makes the active
   coefficient zero.  No nonzero pure point remains.
2. `y_0x_3=a a_bar=0`.  A nonzero active coefficient forces the other row of
   `U_3` to be `b_bar` modulo `a_bar`.
3. `x_0y_3=b b_bar=0`.  Symmetrically, purity forces the other row of `U_3`
   to be `a_bar` modulo `b_bar`.

In the last two cases

```text
U_3=span(a_bar,b_bar),
dim(U_0U_3)=2,                                                (11)
```

contrary to the required center-spoke rank three.  Keeping the three
orientations separate is essential: a full row swap would move the
purity-fixed kernel line.

## Consequence

Every rank-three star with relation-rank multiset `{1,2,2}` is generically in
the tenth component.  The support-two chart belongs to the lower pair-rank
boundary instead.  The next unresolved all-rank-three compatibility shape is
a triangle with exactly one rank-two relation; special/projective boundaries
of the tenth component also remain.

## Verification

Run:

```text
uv run --with sympy python claims/p4/classifications/star/two-rank-two-spoke-mixed-star-classification/verify_p4_two_rank_two_spoke_mixed_star_classification.py
uv run --with sympy python claims/p4/classifications/star/two-rank-two-spoke-mixed-star-classification/audit_p4_two_rank_two_spoke_mixed_star_classification.py
```

The primary verifier reconstructs (4)--(11) and all three support-two Borel
orientations.  The audit permutes the source order to `(1,0,3,2)` and uses a
subset-dynamic-programming permanent.  Both are constant-size exact symbolic
replays, not searches.
