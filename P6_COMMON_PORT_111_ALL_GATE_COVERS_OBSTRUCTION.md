# All 52 larger gate covers are impossible

## Status

**Exact characteristic-zero obstruction for the displayed rank-five model.**
For the specific rank-five exceptional configuration fixed in
[`P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md`](P6_COMMON_PORT_111_RANK_FIVE_CATALYTICANT_CHECKPOINT.md),
none of the 52 minimal bilinear-gate covers of size at least five admits a
zero rectangle `B x C` with

```text
dim B=dim C=3.                                      (1)
```

Each cover has a certified linear combination of its gate matrices that is a
perfect pairing on the five-dimensional ambient space.  Such a pairing
cannot vanish on a product of two three-planes.  Forty-nine certificates use
the unweighted sum of the gates; the other three change one sign.

Together with
[`P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md`](P6_COMMON_PORT_111_UNIQUE_FOUR_GATE_OBSTRUCTION.md),
this excludes every one of the 53 gate-cover alternatives.  Consequently no
three-planes `B,C` satisfy the necessary pointwise rank-two catalecticant
condition for this displayed rank-five configuration, and in particular it
cannot extend to shared full-mode planes `A,B,C`.

This is not a classification of all exceptional configurations with
`dim K=5`.  It therefore does not exclude the whole common-port `1+1+1`
profile, decide `P_6 -> Delta_3`, or settle the global Krenn--Gu conjecture.

## The perfect-pairing lemma

Write each canonical gate as

```text
g_i(b,c)=b^T M_i c.                                 (2)
```

Suppose every gate indexed by a set `S` vanishes identically on `B x C`.  Any
linear combination

```text
M_S=sum_(i in S) alpha_i M_i                         (3)
```

then also satisfies `B^T M_S C=0`.  If `det M_S` is nonzero, `M_S C` is a
three-plane.  Its annihilator in a five-dimensional space has dimension two,
whereas `B` has dimension three.  Thus

```text
det M_S != 0  implies  no such B x C exists.         (4)
```

This argument uses only exact linear algebra.  It does not search either
Grassmannian.

## Why a minimal cover must occur

The twenty-two selected `3 x 3` catalecticant minors factor as nonzero
constants times products of three gates.  If the catalecticant has rank at
most two identically on `B x C`, all twenty-two products vanish in the
coordinate ring of the affine space `B x C`.  That ring is a domain, so one
factor in each product vanishes identically.  The set of all such gates is a
hitting set and hence contains one of the 53 inclusion-minimal covers.

The unique size-four cover is `{0,3,5,9}`.  It does not span a perfect pairing,
but the earlier cycle theorem shows that its only zero rectangles violate a
remaining catalecticant minor.  It remains to exclude the other 52 covers,
which is exactly what (4) and the certificates below do.

## Exact certificates

The matrices use the canonical gate normalization exported by the rank-five
verifier.  In the table, the first column is `S` and the second is
`det M_S`.  All coefficients in (3) are `+1` except on the three rows marked
`flip g_i`, where the coefficient of that one gate is `-1`.

| Cover `S` | `det M_S` |
|---|---:|
| `0,1,4,5,9` | 3 |
| `0,3,5,7,10` | 13 |
| `0,1,4,5,7,10` | -54 |
| `2,3,5,7,12` | 3 |
| `1,2,4,5,7,12` | -102 |
| `1,2,5,7,8,12` | -30 |
| `1,5,8,9,12` | 1 |
| `2,3,5,8,9,12` | 16 |
| `1,5,7,8,10,12` | -102 |
| `2,3,5,8,9,13` | 8 |
| `1,2,4,5,8,9,13` | 2 |
| `2,3,5,7,8,10,13` | 30 |
| `1,2,4,5,7,8,10,13` | 32 |
| `0,3,6,9,11,14` | 4 |
| `0,1,4,6,9,11,14` | 9 |
| `0,3,6,7,10,11,14` | 79 |
| `0,1,4,6,7,10,11,14` | -8 |
| `2,3,6,7,11,12,14` | -45 |
| `1,2,4,6,7,11,12,14` | -80 |
| `1,2,6,7,8,11,12,14` | 40 |
| `1,6,8,9,11,12,14` | 115 |
| `2,3,6,8,9,11,12,14` | -68 |
| `1,6,7,8,10,11,12,14` | 48 |
| `2,3,6,8,9,11,13,14` | -32 |
| `1,2,4,6,8,9,11,13,14` | 60 |
| `2,3,6,7,8,10,11,13,14` | 156 |
| `1,2,4,6,7,8,10,11,13,14` | 108 |
| `0,3,6,10,15` | 1 |
| `0,1,4,6,10,15` | -5 |
| `0,4,9,11,15` | 3 |
| `0,3,6,9,11,15` | 16 |
| `0,4,6,10,11,15` | 36 |
| `0,4,7,10,11,15` | 9 |
| `2,3,6,7,10,12,15` | 72; flip `g_6` |
| `1,2,4,6,7,10,12,15` | -95 |
| `1,6,8,10,12,15` | 1 |
| `2,3,6,8,10,12,15` | -25 |
| `2,4,7,11,12,15` | -3 |
| `2,3,6,7,11,12,15` | -107 |
| `1,2,6,7,8,11,12,15` | -72 |
| `1,4,8,9,11,12,15` | -8; flip `g_1` |
| `2,4,8,9,11,12,15` | 33 |
| `1,6,8,9,11,12,15` | -25 |
| `2,3,6,8,9,11,12,15` | -192 |
| `2,4,6,8,10,11,12,15` | 84 |
| `1,4,7,8,10,11,12,15` | -77 |
| `2,3,6,8,10,13,15` | -1 |
| `1,2,4,6,8,10,13,15` | 16; flip `g_2` |
| `2,4,8,9,11,13,15` | 5 |
| `2,3,6,8,9,11,13,15` | -24 |
| `2,4,6,8,10,11,13,15` | 24 |
| `2,4,7,8,10,11,13,15` | 96 |

Every displayed determinant is nonzero.  The six size-five branches, which
are the first frontier beyond the four-cycle, already have determinants

```text
3, 13, 3, 1, 1, 3.                                  (5)
```

Thus no finer classification of their bilinear zero rectangles is needed.

## Consequence for the displayed rank-five model

Assume its pointwise catalecticant rank were at most two on some `B x C`.
The domain argument would supply a minimal cover `S`.  If `|S|>=5`, its
perfect-pairing certificate contradicts (4).  If `|S|=4`, the unique
four-cycle obstruction supplies an explicit rank-three catalecticant value.
Both alternatives are impossible.  Therefore

```text
rank C_K(b,c) <= 2 identically on B x C              (6)
```

has no pair of three-plane solutions for this `K`.

## Exact replay

```text
uv run --with sympy python verify_p6_common_port_111_all_gate_covers_obstruction.py
python audit_p6_common_port_111_all_gate_covers_obstruction.py
```

The primary verifier reconstructs the catalecticant, factors, gate matrices,
hypergraph, all 53 minimal covers, and all 52 rational determinants.  The
independent audit uses hardcoded linear-factor endpoints to rebuild twice the
gate matrices, then checks the fixed witnesses with exact Bareiss elimination
and modular elimination at `101` and `103`.  The replay performs no
coefficient discovery and no Grassmannian search.
