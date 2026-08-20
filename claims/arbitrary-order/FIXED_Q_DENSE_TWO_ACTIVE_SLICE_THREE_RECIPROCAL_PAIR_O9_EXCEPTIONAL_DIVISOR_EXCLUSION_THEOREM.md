# Three-pair O9 exceptional-divisor exclusion

## Status

**Exact characteristic-zero pointwise closure of GLD50 orbit `O9`.**  Fourteen
sparse rational certificates cover all six exceptional surfaces.  Five exact
saturated denominator covers have no legal common pole.  On the final surface,
one exact substitution reduces simultaneous poles to two coprime univariate
factors.  Thus all `8` labelled O9 masks are empty.

Together with GLD51--GLD61, this proves **every one of the `220`
exactly-three-reciprocal-pair masks pointwise empty** in the GLD43 fixed-Q
dense two-active-slice cell.  Four-or-more-pair supports, proper-secondary
cells, and every permanent bridge remain open.  The global Krenn--Gu
conjecture remains **UNRESOLVED**.

Dependency:

- [`GLD50`](FIXED_Q_DENSE_TWO_ACTIVE_SLICE_THREE_RECIPROCAL_PAIR_GENERIC_EXCLUSION_THEOREM.md).

## 1. Exact surface cover

For canonical directed-cycle support `(0,1),(1,2),(2,0)`, GLD50 leaves

```text
(uvw-1)(uvw+1)(uv+v+1)(vw+w+1)
  (uw-u-2w+1)P9=0,                                  (1)

P9=uv^2w-uvw+2v^2w-4vw+v+2w+1.                     (2)
```

Every active parameter is different from `0` and `1`.  The six surfaces are
rationally parametrized by

```text
w= 1/(uv);                  w=-1/(uv);
u=-(v+1)/v;                 v=-(w+1)/w;
u=(2w-1)/(w-1);             u=-T/(vw(v-1)),          (3)

T=2v^2w-4vw+v+2w+1.
```

Define

```text
G =v^2w-2vw+w+1;            H =2vw^2-vw+w-1;
HL=v^2w-3vw+v+2w+1;
Q =3v^2w^4-2v^2w^3+2vw^4-3vw^3-2vw^2+5vw-2v
    -w^4-w^3+2w^2+w-1;
R =2vw^2-v+w^2+2w-2;
I =2v^3w^2-v^3w-5v^2w^2+3v^2w+3vw^2-2vw+v+2w+1;
J =3v^2w-6vw+v+3w+1.                                (4)
```

The normalized exact multiplier denominator lcms, with irrelevant nonzero
integer constants suppressed, are:

| Surface | Rows | Denominator lcms |
|---|---:|---|
| `uvw=1` | `13,14` | `uv^2(uv+v-1)`; `uv(u+1)(uv-v+1)` |
| `uvw=-1` | `13,12,18` | `uv^2(2uv+v-1)`; `uv(2u-1)(uv-v+1)`; `(u+1)(v-1)(uv-v-1)(u^2v+uv^2-1)` |
| `uv+v+1=0` | `15,13` | `vw(v+1)(3v^2w-2v^2+v-w+1)`; `v^2w^2(v+1)^2(vw-w+1)(vw+w-1)` |
| `vw+w+1=0` | `13` | `u^2w^2(w+1)^2(uw+u-1)` |
| `uw-u-2w+1=0` | `17,18,13` | `w(3vw-2v-w+1)Q`; `(v-1)(3w-2)(vw+w+1)HR`; `v^2w^2(2w-1)^2(vw-w+1)H` |
| `P9=0` | `18,13,14` | `(v-1)(vw+w+1)GHL I`; `v^2w^2(vw-w+1)GT^2`; `vw^2GHLT^2J` |

Each multiplier cancels all `81` nuisance variables and leaves `1`.

## 2. Exact complementary-denominator proof

Introduce a localization variable `z`.  For the first five table rows, let
`d_i` be the displayed denominators and let `L` be the product of the active
factors and any already-covered product-surface intersection.  Exact
lexicographic Groebner bases give

```text
<d_i,zL-1>=<1>.                                       (5)
```

The localizers are

```text
uv(u-1)(v-1)(uv-1);
uv(u-1)(v-1)(uv+1);
vw(v-1)(v+1)(2v+1)(w-1)(vw+w-1);
uw(u-1)(w-1)(w+1)(2w+1)(uw+u-1);
vw(v-1)(w-1)(2w-1)H.                                 (6)
```

The extra factors in the last three expressions are precisely intersections
with the already closed `uvw=-1` surface.  Thus (5) is a pointwise cover, not
a generic inference.

On `P9=0`, localize by the active factors, by

```text
S=T+vw(v-1),
```

which is the numerator of `u-1`, and by `G`, the `uvw=-1` intersection.  If
the middle denominator in the final table row vanishes after localization,
then

```text
vw-w+1=0,              w=-1/(v-1).                   (7)
```

Under (7), the remaining factors in the first and third denominators become

```text
vw+w+1 = -2/(v-1);     HL=3;
I=(v^3-v-3)/(v-1);     J=-2(v-2).                   (8)
```

Exact Euclidean division gives

```text
gcd(v^3-v-3,v-2)=1.                                  (9)
```

Hence the first and third denominators cannot vanish together on (7).  If
(7) does not hold, the middle certificate is already regular.  This closes
the full `P9` surface.

### Theorem

The GLD50 orbit `O9`, all `8` labelled masks, is pointwise empty.  Therefore
all `220` exactly-three-reciprocal-pair masks in the GLD43 cell are pointwise
empty.  `square`

## Scope ledger

```text
GLD50 orbit O9 exceptional union:                     EMPTY;
three-pair O9 masks:                                 8 EMPTY;
all exactly-three-pair masks:                      220 EMPTY;
four-or-more reciprocal pairs:                        OPEN;
proper-secondary cells:                               OPEN;
every permanent bridge:                               OPEN;
global Krenn--Gu conjecture:                     UNRESOLVED.
```

## Verification boundary

```powershell
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_o9_exceptional_divisor_exclusion.py
uv run --with sympy python -I claims/arbitrary-order/audit_fixed_q_dense_two_active_slice_three_reciprocal_pair_o9_exceptional_divisor_exclusion.py
python claims/arbitrary-order/verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_generic_exclusion.py
```

The primary derives all fourteen cores from the `945` perfect matchings.  The
standalone no-import audit reconstructs recursive permanents, derives the same
multipliers in reverse row and variable order, and independently repeats the
saturated and Euclidean coverage arguments.
