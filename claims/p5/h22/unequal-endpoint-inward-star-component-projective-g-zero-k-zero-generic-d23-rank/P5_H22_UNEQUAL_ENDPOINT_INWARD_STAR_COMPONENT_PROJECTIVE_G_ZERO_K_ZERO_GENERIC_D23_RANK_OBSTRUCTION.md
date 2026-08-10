# Component twenty-five's `g=0,k=0` projective divisor: generic `D23` closure

## Status

**Exact characteristic-zero special-divisor theorem.**  On both normalized
projective leaf sheets

```text
a=1, g=0, k=0, es=+1 or es=-1, s!=0,
```

the generic finite-`D23` weighted-`H22` fibre is empty.  The complete
normalized binary incidence is a reduced disjoint union of two affine lines
over `Q(s,lambda)`.  The second line is a genuine specialization-only branch
that is absent over `Q(s,k,lambda)`.  Exact paired-`D01` ranks obstruct every
point of both lines, and all four one-marked ranks are classified exactly.

This theorem is not transported from component twenty-three.  In standard
edge order `01,02,03,12,13,23`, the present `P_4` pair-rank profile is

```text
(3,3,4,3,4,4),
```

whereas component twenty-three's closed `t=0` special fibre has profile
`(3,3,3,3,4,4)`.  The profile multisets differ, so no source-mode
permutation and ambient linear equivalence can identify the two loci.

The statement is over the generic ordinary finite-weight field.  It does not
specialize the calculation to any special finite weight, including
`lambda=0,+1,-1`.  Those weights, `D23` weight infinity, `s=0`, other
component/projective charts, arbitrary source or ambient changes, and the
global Krenn--Gu conjecture remain **UNRESOLVED**.

## The `k=0` plane configuration

Put

```text
A=(1,1,0,0), C=(1,-1,0,0),
B=(0,0,1,1), D=(0,0,1,-1).
```

On the `es=1` sheet the four two-planes are

```text
U0=<A,B>,
U1=<A,B+sC>,
U2=<C,A+B/s>,
U3=<D,B-sC>.
```

The exact pure permanent tensor has only

```text
T1111=4/s
```

nonzero, and direct ranks of the six stacked plane pairs give
`(3,3,4,3,4,4)`.  The previously certified sign-sheet map specializes at
`k=0`: swap both ambient coordinate pairs, send `s` to `-s`, invert the
homogeneous weight, and apply alpha-row signs `(1,1,-1,-1)`.  The primary and
audit check the induced identity on all sixteen marked coefficients, so it
suffices to classify `es=1`.

## Complete normalized `D23` incidence

Use finite weight

```text
(x,e) -> (x0,x1,lambda*x2+x3,e)
```

and normalize the empty binary coefficient to one.  The ten fixed-vertex
Segre equations must be recomputed after the specialization `k=0`; merely
substituting into the generic-`k` answer misses a whole component.  Their
ideal is the reduced disjoint union of two affine lines.  Put

```text
X=s+2(1-lambda)t.
```

The inherited line `L0` is

```text
z0=X/[2s(lambda-1)],
z1=X/[2s(lambda-1)],
z2=1/[2(lambda-1)],
z3=X/[2(lambda+1)],
z4=0,
z5=0,
z6=t/s,
z7=t.
```

Its forced marking is

```text
h=(-1,-1,-1,-(lambda+1)/(lambda-1)).
```

All fourteen mixed marked `D23` coefficients vanish.  The two pure
diagonals are one and

```text
-(lambda+1)[s+4(1-lambda)t]/[s(lambda-1)].
```

The new specialization line `L1` is

```text
z0=-t/s,
z1=-t/s,
z2=0,
z3=-[s+2(lambda-1)t]/[2(lambda+1)],
z4=1/[2(lambda-1)],
z5=0,
z6=t/s,
z7=t.
```

Its forced marking is

```text
h=(-1,0,-1,0),
```

and its opposite pure diagonal is

```text
(lambda+1)[s+4(lambda-1)t]/[s(lambda-1)].
```

On both lines all fourteen mixed marked `D23` coefficients vanish and the
first pure diagonal is one.  Each binary incidence is genuinely populated
on a dense open subset.

Algebraically, the union is visible from the square-free factor

```text
z4[2(lambda-1)z4-1]=0.
```

The other six Groebner generators solve `z0,z1,z2,z3,z5,z6` linearly in
`z4,z7`.  This certifies that `L0` and `L1` are all normalized solutions and
that there are no embedded or additional branches on the generic ordinary
weight chart.

## Complete paired-`D01` rank classification on `L0`

Project the same marked rows in the paired `D01` direction.  Write

```text
Y=s+4(1-lambda)t,
Z=s+8(1-lambda)t,
P=s(lambda-2)-3(lambda-1)^2 t.
```

For mode zero, two maximal minors are

```text
X/s^3,
-2(lambda+1)Y/[s^3(lambda-1)].
```

They cannot vanish together because `2X-Y=s`.  Thus mode zero has rank four
for every `t`; this alone obstructs the whole incidence line.

For mode one, two maximal minors are

```text
(lambda+1)X/[s^3(lambda-1)],
-(lambda+1)^2 Z/[s^3(lambda-1)^2].
```

They cannot vanish together because `4X-Z=3s`.  Hence mode one also has rank
four everywhere.

For mode two, the maximal minor

```text
-(lambda+1)X^2/[s^4(lambda-1)]
```

gives rank four on `X!=0`.  At the unique residual point
`t=s/[2(lambda-1)]`, all `3 x 3` minors vanish while the `2 x 2` minor in
rows `(1,3)` and columns `(1,3)` equals `-(lambda+1)/s`.  Its rank is exactly
two there.

For mode three, every maximal minor vanishes identically.  Two `3 x 3`
minors are unit multiples of `P` and `X`; they cannot vanish together because

```text
2P-3(lambda-1)X=-s(lambda+1).
```

Thus mode three has rank exactly three everywhere.  The complete profile is
therefore

```text
X!=0 : (4,4,4,3),
X=0  : (4,4,2,3).
```

Thus every point of `L0` is a false positive.

## Complete paired-`D01` rank classification on `L1`

Put

```text
W=s+2(lambda-1)t.
```

Every maximal minor of modes zero and three vanishes.  For mode zero, two
`3 x 3` minors are

```text
24t^3(lambda-1)^2/s^4,
-(s-4t)W/s^4.
```

They cannot vanish together because at `t=0` the second is `-1/s^2`.
Consequently mode zero has rank exactly three everywhere.

For mode one, two maximal minors are

```text
-12t^2(lambda-1)^2/s^4,
(lambda-1)W^2/[s^4(lambda+1)].
```

At `t=0`, `W=s`; hence mode one has rank four everywhere.  Similarly, mode
two has the two maximal minors

```text
4W^2/[s^4(lambda-1)],
12t^2(lambda+1)^3/[s^4(lambda-1)],
```

so it also has rank four everywhere.

Finally, two mode-three `3 x 3` minors are

```text
6t(lambda+1)/s^6,
-[s+6(lambda-1)t]/s^6.
```

They cannot vanish together, and every maximal minor is zero, so mode three
has rank exactly three everywhere.  The complete `L1` profile is therefore

```text
(3,4,4,3) for every t.
```

A legal weighted-`H22` lift requires all four one-marked ranks to be at most
three.  Modes one and two obstruct every point of `L1`; together with the
mode-zero obstruction on `L0`, this proves the complete normalized generic
finite-`D23` fibre on the `k=0` divisor is empty.

## Independent audit and replay

The primary uses permutation permanents, a direct grevlex ideal comparison,
and the rank certificates above.  The audit imports no project code, rebuilds
the permanent by subset dynamic programming, compares the ideal in reversed
variable grevlex order, and uses alternate maximal and submaximal minors for
all four modes.

```powershell
uv run --with sympy python claims/p5/h22/unequal-endpoint-inward-star-component-projective-g-zero-k-zero-generic-d23-rank/verify_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_k_zero_generic_d23_rank_obstruction.py
uv run --with sympy python claims/p5/h22/unequal-endpoint-inward-star-component-projective-g-zero-k-zero-generic-d23-rank/audit_p5_h22_unequal_endpoint_inward_star_component_projective_g_zero_k_zero_generic_d23_rank_obstruction.py
```

Both calculations are exact over characteristic zero.  No finite-field output
is used as proof.
