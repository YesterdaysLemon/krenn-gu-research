# Minimal tangent cycles fail the GHZ mixed second jet

## Status

**Exact characteristic-zero second-jet obstruction.**  The symmetric-cycle
construction in
[`ROOT_TANGENT_CYCLE_FRAME_SYMMETRY_REALIZATION.md`](ROOT_TANGENT_CYCLE_FRAME_SYMMETRY_REALIZATION.md)
realizes every required first-jet quotient frame by the minimal edge block

```text
M_i=a_i^+ ell_(i+1)^T+ell_i (a_(i+1)^-)^T.
```

For every cycle length `r>=3`, an explicit fully supported GHZ datum and
pairwise-distinct shared quotient classes make this minimal construction fail
one mixed second derivative on every cycle edge.  The graph-side derivative
is zero, while the GHZ-side derivative is the nonzero diagonal vector

```text
(0,1,t_i^2).
```

Thus the first-jet cycle realization is not itself a second-order formal
graph witness.  Any repair must add a tangent--tangent part to an edge block,
add effective companions outside the minimal cycle, or change the
projectively constant root--blocker layer.

This is a sharp obstruction to one formal realization, not to all companion
systems.  Tangent--tangent edge freedom and additional complementary
hafnian cofactors remain available.  The arbitrary-order local-to-global
reduction remains **UNKNOWN**, and the global Krenn--Gu conjecture remains
**UNRESOLVED**.  No finite field is used.

## Normalized GHZ first jets

Take every root vector to be

```text
x=(1,1,1)
```

and normalize the three surviving GHZ diagonal coefficients to one.  Put

```text
ell=e_0^*,                 ell(x)=1,
S=ker(ell),
F(y)=(y_1-y_0,y_2-y_0).
```

The map `F` is the logarithmic GHZ derivative modulo the scalar diagonal:

```text
V/<x>  ->  Diag/<Lambda> ~= K^2.
```

Choose pairwise-distinct scalars `t_i`, indexed cyclically, and put

```text
q_i=(1,t_i).
```

At root `i`, decompose the quotient derivative in the incident frame:

```text
F(y)=a_i^-(y) q_(i-1)+a_i^+(y) q_i.              (1)
```

Writing `L=t_(i-1)` and `T=t_i`, the two coefficient covectors are

```text
a_i^+(y)=((y_2-y_0)-L(y_1-y_0))/(T-L),
a_i^-(y)=(T(y_1-y_0)-(y_2-y_0))/(T-L).           (2)
```

Both annihilate `x`, and they form a basis of `x^perp`.

## The selected tangent directions

On the edge `e_i={i,i+1}`, choose at both endpoints

```text
y_i=z_(i+1)=(0,1,t_i).                            (3)
```

Then `ell(y_i)=ell(z_(i+1))=0` and `F(y_i)=F(z_(i+1))=q_i`.  Equation (1)
therefore gives

```text
a_i^+(y_i)=1,       a_i^-(y_i)=0,
a_(i+1)^-(z_(i+1))=1,  a_(i+1)^+(z_(i+1))=0.     (4)
```

The directions isolate the shared edge class at both endpoints: every other
minimal-cycle companion evaluation vanishes.

## Vanishing of the graph second derivative

Use exactly the minimal symmetric edge block from the first-jet theorem,
with the normalized scalar covectors `ell_i=ell_(i+1)=ell`:

```text
M_i=a_i^+ ell^T+ell (a_(i+1)^-)^T.               (5)
```

It still has the required endpoint contractions

```text
M_i x=a_i^+,       M_i^T x=a_(i+1)^-,
x^T M_i x=0.                                         (6)
```

But (3)--(5) give

```text
y_i^T M_i z_(i+1)
 =a_i^+(y_i) ell(z_(i+1))
  +ell(y_i) a_(i+1)^-(z_(i+1))
 =0.                                                (7)
```

In the projectively constant root--blocker layer, differentiating a
root--blocker edge contributes `ell(y_i)` or `ell(z_(i+1))`, hence also
vanishes.  By (4), the other cycle edge at either root vanishes.  Therefore
every matching class in the mixed derivative is zero: matchings pairing the
two roots separately acquire a zero endpoint factor, and the matching using
their common edge acquires (7).

This argument is independent of the value of the complementary cofactor
attached to the common edge.

## The GHZ mixed Hessian

For two distinct root slots, the GHZ mixed derivative in directions `y,z`
has diagonal coefficient vector

```text
(y_0 z_0, y_1 z_1, y_2 z_2).
```

Substitution of (3) gives

```text
(0,1,t_i^2),                                        (8)
```

which is nonzero in every characteristic.  Equations (7)--(8) contradict
the second-order GHZ identity on every cycle edge.

## Exact boundary

The general edge block with the same first-order endpoint contractions is

```text
M_i+N_i,       N_i x=0,       N_i^T x=0.           (9)
```

The space of such `N_i` is four-dimensional and is an arbitrary bilinear
form on the two tangent quotients.  It can make (7) nonzero without changing
any first jet.  Additional effective companion edges can also contribute to
the mixed derivative.  Consequently the theorem proves exactly:

```text
minimal symmetric cycle first jets: NOT second-jet compatible;
tangent--tangent repair: AVAILABLE but unclassified;
additional companion-cofactor repair: AVAILABLE but unclassified;
complementary-hafnian realization: UNKNOWN;
global conjecture: UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python verify_root_tangent_minimal_cycle_second_jet_obstruction.py
python audit_root_tangent_minimal_cycle_second_jet_obstruction.py
```

The primary proves the symbolic three-parameter identities and checks exact
cycles of lengths three through twelve.  The no-import audit uses rational
arithmetic and checks lengths three through sixteen independently.
