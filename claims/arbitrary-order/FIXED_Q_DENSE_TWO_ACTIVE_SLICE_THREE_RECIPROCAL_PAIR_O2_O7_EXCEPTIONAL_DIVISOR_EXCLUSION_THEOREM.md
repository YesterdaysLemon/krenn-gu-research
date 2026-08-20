# Three-pair O2/O7 exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbits `O2` and
`O7`.**  Seventeen sparse rational certificates cover the six O2 exceptional
surfaces.  Exact saturated Groebner calculations prove that five
complementary denominator covers have no legal common pole; the sixth leaves
one rational point, which a nine-row core closes.  Active-colour exchange then
reverses O2 to O7.  Thus all `48` labelled masks in the two orbits are empty.

Only GLD50 orbit `O9`, with `8` labelled masks, remains open among exactly
three reciprocal pairs.  Four-or-more-pair supports, proper-secondary cells,
and every permanent bridge also remain open.  The global Krenn--Gu conjecture
remains **UNRESOLVED**.

Dependencies:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md);
- [`GLD55`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_IN_STAR_COLOUR_EXCHANGE_EXCLUSION_THEOREM.md).

## 1. O2 exceptional cover

For canonical support `(0,1),(0,2),(1,0)`, GLD50 leaves

```text
(u+1)(u+v)(v+2)(uw+1)(u+v+1)(uw+vw+v+1)=0.       (1)
```

Every active parameter is different from `0` and `1`.  The six surfaces in
(1) are parametrized respectively by

```text
u=-1;  v=-u;  v=-2;  w=-1/u;  v=-u-1;
w=-(v+1)/(u+v).                                    (2)
```

For compactness define

```text
A=u^3w+2u^2w^2-10u^2w+3u^2+uw^2+16uw-12u-6w^2-5w+6;
B=u^2+2uv+2u-1;          C=u^2+3uv+2u+v^2-1;
D=uv+2u+v;               E=u^2+2uv-2u-4v-1;
F=u^2+2uv+u-v-1.                                  (3)
```

The exact normalized multiplier denominator lcms, with irrelevant nonzero
integer constants suppressed, are:

| Surface | Rows | Denominator lcms |
|---|---:|---|
| `u=-1` | `14,16` | `vw(v-1)(w-1)^3(w+1)`; `w(v-1)(w-1)(3w-2)(vw+v-w+1)` |
| `v=-u` | `11,14,17` | `u^3(uw-1)`; `u^3w^2(u-1)(w-2)(uw+1)`; `(u-1)(uw+1)(uw-w-1)(2uw-u-w+1)` |
| `v=-2`, `uw+1!=0` | `14,14,17` | `uw^2(u-1)^2(w-2)(uw+1)`; `uw(uw-1)(uw+1)A`; `(u-1)(w-1)(uw+1)(uw-2w-1)(2uw-u-w+1)` |
| `uw=-1` | `17,14` | `u^3v^2(u-1)(u+1)(2u+1)`; `uv^2(u^2-2u-1)(u^2+u-1)` |
| `v=-u-1` | `14,16,14` | `u^2w^2(u-1)(u+1)^2(2u+1)(w+1)`; `w(u-1)(u+w)(uw+1)(2uw-u-w+1)`; `uw^2(u-1)^2(u+1)^2(w-2)(uw+1)` |
| `w=-(v+1)/(u+v)` | `14,17,14` | `uv^2(u-1)^2(2u+v)(v+1)^2(2u+3v+1)`; `v(u-1)(v+1)BC`; `uv^2(u-1)(v+1)DEF` |

Each multiplier cancels all `81` nuisance variables and leaves `1`.

## 2. Exact denominator coverage

Introduce a localization variable `z`.  For each row of the table, let
`d_i` be its displayed denominator and let `L` be the product of the active
nonzero factors on that parametrization.  Exact lexicographic Groebner bases
give

```text
<d_i, zL-1> = <1>                                     (4)
```

for `u=-1`, `v=-u`, `v=-2` away from `uw=-1`, `uw=-1`, and the final mixed
surface.  The localizers used are respectively

```text
vw(v-1)(w-1);
uw(u-1)(u+1)(w-1);
uw(u-1)(w-1)(uw+1);
uv(u-1)(u+1)(v-1);
uv(u-1)(v-1)(v+1)(u+v)(u+2v+1).                    (5)
```

The `uw=-1` row covers the part omitted from the `v=-2` localization.
Therefore (4) proves pointwise coverage, not merely generic coverage.

On `v=-u-1`, localization by

```text
L=uw(u-1)(u+1)(u+2)(w-1)
```

gives the reduced basis

```text
(9z-8, 2u+1, w-2).                                  (6)
```

Thus the only legal common pole is

```text
(u,v,w)=(-1/2,-1/2,2).                               (7)
```

A nine-row exact rational core at (7) has denominator lcm `6`, cancels all
`81` nuisance coordinates, and leaves `1`.  Equations (4)--(7) exhaust every
point of (1).

### O2 theorem

The full GLD50 orbit `O2`, all `24` labelled masks, is pointwise empty.

## 3. O7 by active-colour exchange

GLD55 proves covariance of the complete equation system under active-colour
exchange.  It reverses every reciprocal arrow through the involution

```text
f(t)=t/(t-1).
```

The reverse of the O2 representative is exactly

```text
{10,20,01}={01,10,20},
```

the GLD50 `O7` representative.  In O7's ordered coordinates the parameter
map is `(u,v,w) -> (f(w),f(u),f(v))`; it is an automorphism of the active
domain.  Hence the pointwise-empty O2 system is isomorphic to the complete O7
system.

### Theorem

The full GLD50 orbits `O2` and `O7`, all `48` labelled masks, are pointwise
empty.  `square`

## Scope ledger

```text
GLD50 orbit O2 exceptional union:                     EMPTY;
GLD50 orbit O7 exceptional union:                     EMPTY;
three-pair O2 and O7 masks:                         48 EMPTY;
GLD50 orbit O9, all 8 masks:                           OPEN;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o2_o7_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o2_o7_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion.py
```

The primary derives the seventeen sparse cores from the `945` perfect
matchings.  The standalone no-import audit reconstructs recursive permanents,
derives the same multipliers in reverse row and variable order, and repeats
the saturated cover.  The final two replays independently protect the full
active-colour covariance used for O2-to-O7 transfer.
