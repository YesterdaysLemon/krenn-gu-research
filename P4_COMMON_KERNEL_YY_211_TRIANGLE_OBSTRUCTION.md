# The dense common-kernel `YY` triangle is empty

## Status

**Exact symbolic obstruction over `C`.**  Consider a rank-three exceptional
triangle with relation-rank pattern `(2,1,1)` and common-kernel Borel
orientation

```text
y_1y_3=0,
y_2y_3=0,
y_1x_2-x_1y_2=0.                                  (1)
```

Assume the shared zero-divisor pair has genuine two-coordinate support and
that both complementary binary directions lie in the dense torus of their
`P^1`.  Then no nonzero pure `P_4` restriction exists.

This closes the dense kernel--kernel leaf chart of the common-kernel
orientation.  Mixed kernel/active leaves, active/active leaves, support-one
directions, and lower pair-rank boundaries remain outside the theorem.  It is
not component exhaustiveness or a global graph proof.

## Exact-pair synchronization

Work in

```text
R=C[X_0,X_1,X_2,X_3]/(X_0^2,X_1^2,X_2^2,X_3^2)
```

and normalize the shared exact pair to

```text
a=X_0+X_1,             c=X_0-X_1,
a c=0,                 Ann_R1(c)=C a.               (2)
```

Equations (1) force

```text
y_1=y_2=a,             y_3=c.                       (3)
```

After a Borel shift removes the common `a` component of the active leaf
rows, their rank-two relation becomes the synchronization law

```text
x_1=m=beta*c+s,
x_2=m+r c,             s=uX_2+vX_3.                 (4)
```

Write the remaining active row as

```text
x_3=d=gamma*a+delta*c+t,
t=pX_2+qX_3.                                        (5)
```

The dense chart assumption is

```text
u v p q!=0.                                          (6)
```

## The binary polarity factors all four minors

The seven kernel-containing triple products span the same space as

```text
C_0=a^2d,
C_1=amd,
C_2=m(m+r c)c.                                      (7)
```

Put

```text
A=<s,t>=u q+v p,       Q=[s,t]=u q-v p,
E=(2 beta+r)A.                                      (8)
```

In the degree-three basis indexed by the missing source coordinate, the four
maximal minors of `[C_0 C_1 C_2]` are

```text
 8q u v A,
 8p u v A,
 4Q(E-2 gamma u v),
 4Q(E+2 gamma u v),                                 (9)
```

up to the harmless common sign fixed by the displayed basis order.

Purity requires `dim span(C_0,C_1,C_2)<=2`.  By (6), the first two equations
in (9) force

```text
A=0.                                                 (10)
```

Then `Q!=0`, so the last two force

```text
gamma=0.                                             (11)
```

Equation (10) is exactly `s t=0` in the complementary squarefree binary
block: `t` is the split-polar partner of `s`.

## The active cubic falls into the apolar span

With `d=delta*c+t` and `s t=0`, equations (7) simplify to

```text
C_0=a^2t,
C_1=0,
C_2=m(m+r c)c.                                      (12)
```

The all-active cubic is

```text
X=m(m+r c)d
 =delta C_2-beta(beta+r)C_0.                        (13)
```

The opposite plane `U_0` must annihilate every kernel-rich cubic, hence it
annihilates `C_0,C_2`.  Equation (13) then says it also annihilates the
all-active cubic.  The purported nonzero pure coefficient vanishes, a
contradiction.

This is stronger than merely finding no point in a parameter chart.  The
binary polarity condition forced by apolar compression makes the desired
active class equal to a kernel-rich class in the Frobenius quotient.

## Across the mathematical fence

The proof can be read in three neighboring languages:

```text
binary invariant theory:  A=0 is the graph of a quadratic polarity,
exact zero divisors:       st=0 is a two-periodic annihilator pair,
apolar geometry:           the active cubic lies in the mixed cubic span.
```

Quadratic-form-induced involutions on binary forms are studied by
Abdesselam--Chipalkatti
([arXiv:1008.3117](https://arxiv.org/abs/1008.3117)); exact homogeneous
zero-divisor pairs are studied by Kustin--Striuli--Vraciu
([arXiv:1304.0411](https://arxiv.org/abs/1304.0411)).  Neither source states
(9)--(13); their languages become decisive here only after the permanent
triangle is translated into its three-cubic apolar compression.

## Verification

Run:

```text
uv run --with sympy python verify_p4_common_kernel_yy_211_triangle_obstruction.py
python audit_p4_common_kernel_yy_211_triangle_obstruction.py
```

The primary verifier checks (2)--(13) over the rational function field.  The
independent audit uses a different binary-block coordinate order, subset
dynamic programming, and exact rational samples on the polarity sheet.  Both
are fixed-size symbolic replays, not searches.
