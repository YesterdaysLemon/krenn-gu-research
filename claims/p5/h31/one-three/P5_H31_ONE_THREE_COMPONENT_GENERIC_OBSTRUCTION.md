# Generic marked `H31` obstruction on the three `1+3` components

## Status

This is an exact characteristic-zero theorem on dense open subsets of
the three pure-`P_4` components proved in
[`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](../../../p4/classifications/P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md).

At the generic point of each component, no marked binary pure
restriction can lift to an `H31` restriction:

- on `L_3`, no neighbouring binary `Delta_2` slice exists;
- on `L_1` and `L_2`, every neighbouring binary `Delta_2` extension
  has an injective one-marked map, while the corresponding transverse
  pure coefficient is nonzero.

The proof classifies the complete marked-basis fibre over the three
function-field generic points.  It does **not** yet close special
parameter divisors or projective boundary points of the components.
It also does not classify all pure-`P_4` components, exclude all of
`H31`, settle `H22`, or resolve the global prize problem.

## Canonical marked bases

Use the normal form and parameters `S,D,G,T` from
[`P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md`](../../../p4/classifications/P4_DIAGONAL_QUADRIC_ONE_THREE_COMPONENTS.md):

```text
P=G-T,  Q=D-S,

u_0=(2,P+Q,Q-P,0),    u_1=(0,0,1,1),
y_1=(0,1,-1,0),       x_1=(1,0,S,D),
x_2=(1,0,G,T),        y_2=(0,1,0,-1),
z_1=(0,1,1,0),        z_2=(0,1,0,1).               (1)
```

For `L_1` and `L_2`, take

```text
beta=(u_0,x_1,x_2,z_1),

alpha_1=y_1,  alpha_2=y_2,  alpha_3=z_1-z_2,        (2)
```

and

```text
L_1:
 alpha_0=(G+S)u_0-2DG u_1;

L_2:
 alpha_0=(D+G)u_0-2D(D+G-S)u_1.                    (3)
```

For `L_3`, take

```text
alpha=(u_1,y_1,y_2,G(D+G+S)z_1+DS z_2),
beta =(u_0,x_1,x_2,z_1).                           (4)
```

In each case the pure restriction has only coefficient `BBBB`.
Every other marked basis with the same `alpha` directions is uniquely
of the form

```text
beta_i(t)=beta_i+t_i alpha_i,       i=0,1,2,3.      (5)
```

The omitted row scalings do not affect any rank or nonvanishing
argument below.

## Neighbouring binary slices

Let `q` be the source coordinate removed from the pure hyperplane and
replaced by the fifth source coordinate.  The eight new row entries
form an extension vector

```text
e=(x_0,x_1,x_2,x_3,y_0,y_1,y_2,y_3).               (6)
```

The fourteen mixed coefficients of the neighbouring binary
restriction are linear in `e`.  Write their matrix as `M_q(t)`, and
write the two diagonal linear forms as

```text
A_q(e), B_q(e).                                     (7)
```

A genuine binary `Delta_2` extension exists exactly when

```text
M_q(t)e=0,       A_q(e)B_q(e) != 0.                 (8)
```

Eliminate `e` over the function field `C(S,D,G)`, normalizing
`A_q(e)=1` and inverting `B_q(e)`.  The resulting marked projections
are as follows.

### Branch `L_1`

For `q=0,1`, the projection ideal is the unit ideal.  For `q=2`,

```text
t_3=0,
S t_2+(D-S)(S+G)=0,
t_1+D-S=0,
(S+G)t_0+1=0.                                      (9)
```

For `q=3`,

```text
t_3+1=0,
t_2+D-S=0,
(S-D+G)t_1+(D-S)(S+G)=0,
(S+G)t_0+1=0.                                      (10)
```

Thus each surviving source coordinate has one generic marking.

### Branch `L_2`

Again `q=0,1` give the unit ideal.  For `q=2`,

```text
t_3=0,       t_1=0,       (D+G)t_0+1=0,            (11)
```

with `t_2` free.  For `q=3`,

```text
t_3+1=0,     t_2=0,       (D+G)t_0+1=0,            (12)
```

with `t_1` free.  The surviving markings are therefore two rational
pencils.

### Branch `L_3`

For all four values of `q`, the projection ideal is the unit ideal:

```text
no generic marked basis has a neighbouring binary Delta_2 slice.   (13)
```

This already excludes the generic marked `H31` fibre of `L_3`.

## The all-extension one-marked identity

It remains to rule out the binary extensions in (9)--(12).  At every
surviving marking, `M_q` has rank six and a two-dimensional kernel.
Let `N_q(e)` be the `8 x 4` one-marked map at mode zero on the
neighbouring hyperplane.

For `L_1`, take rows

```text
q=2: (0,4,5,7),
q=3: (0,2,3,7).                                    (14)
```

On `ker M_q`, the corresponding determinants satisfy the exact
identity

```text
det N_q(e)[rows,:]
  = A_q(e)^2 B_q(e) / [8 D G(G+S)].                 (15)
```

For `L_2`, use the same row sets.  Uniformly along each marking pencil,

```text
det N_q(e)[rows,:]
  = A_q(e)^2 B_q(e)
    / [8 D(D+G)(D+G-S)].                            (16)
```

A rational kernel basis for (16) changes at

```text
q=2: t_2=G(D+G-S)/(D+G),
q=3: t_1=S.                                        (17)
```

Direct kernel bases at both values in (17) satisfy the same identity
(16).  Thus (16) covers the complete generic marking pencils, not
only their complements.

On the stated dense open sets, the denominators in (15)--(16) are
nonzero.  Condition (8) then makes the right-hand side nonzero, so the
neighbouring one-marked map is injective for every binary extension.

## The `H31` contradiction

In a ternary `H31` lift, the third target row at mode zero must have all
one-marked coefficients equal to zero on both hyperplanes.  Injectivity
of the neighbouring one-marked map forces that row to vanish on the
neighbouring hyperplane, so the five-dimensional row can be supported
only on the removed source coordinate `q`.

For every survivor in (9)--(12), entry `(2,q)` of the pure-hyperplane
one-marked map is the constant

```text
-1 for q=2,
 1 for q=3.                                         (18)
```

Hence a nonzero row supported on `q` cannot vanish in the pure
one-marked map.  The third target row is zero globally, contradicting
the rank-three local-map requirement forced by conciseness of
`Delta_3`.

Consequently:

```text
the complete marked H31 fibre over the generic point of
each of L_1,L_2,L_3 is empty.                        (19)
```

## Exact frontier

The three newly discovered components are now generically excluded,
just as the earlier two components are completely excluded.  The
remaining `H31` work is:

1. close the parameter divisors and projective boundary of
   `L_1,L_2,L_3`; and
2. determine whether still further pure-`P_4` components exist.

The separate `H22` case remains open.

## Verification

Run:

```text
python claims/p5/h31/one-three/verify_p5_h31_one_three_component_generic_obstruction.py
python claims/p5/h31/one-three/audit_p5_h31_one_three_component_generic_obstruction.py
```

The primary verifier reconstructs the canonical bases (2)--(4),
performs the twelve function-field eliminations giving (9)--(13),
computes exact kernel bases, verifies (15)--(17), and checks the
transverse constants (18).  The independent audit uses a separate
dynamic-programming permanent and modular row reduction.  At two
finite-field points it exhausts every marked basis and every
projective extension direction, confirming that every genuine binary
extension has the asserted injective marked map and transverse pure
entry.  The finite-field census is independent QA; the
function-field identities prove the generic theorem over `C`.
