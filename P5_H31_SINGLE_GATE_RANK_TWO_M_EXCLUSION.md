# Exclusion of the rank-two common-plane single-gate `H31` branch

## Status

This is an exact characteristic-zero obstruction for the single-gate
part of `H31` in which the other three binary row pairs have rank two
on the common source three-space.

More precisely, use

```text
M=span(e_0,e_1,e_2),
H_s=M+Ce_s,
H_p=M+Ce_p.
```

Suppose four binary local row pairs send the embedded `P_4` on `H_s`
to a nonzero pure tensor and the embedded `P_4` on `H_p` to
`Delta_2`.  Suppose one row pair is a rank-one gate on `H_s` and the
other three pairs have rank two on `M`.  Then these binary rows cannot
be enlarged to rank-three local maps whose two four-dimensional
restrictions have the ternary diagonal support required by `H31`.

This closes the entire rank-two-`M` single-gate component, including
all projective line intersections in the binary extension locus.  It
does **not** cover a further rank drop among the other three pairs on
`M`, exclude the all-rank-two pure-`P_4` components not contained in the
known family, exclude all of `H31` or `H22`, prove
`P_5 -> Delta_3` impossible, or settle the global conjecture.

The proof uses determinantal strata and transverse kernel lines.  It
does not enumerate ambient local maps or Grassmannians.

## Binary normal form

The exact reduction in
[`P5_H31_SINGLE_GATE_P3_REDUCTION.md`](P5_H31_SINGLE_GATE_P3_REDUCTION.md)
puts the gate at mode zero and gives

```text
alpha_0|H_s=0,      alpha_0|H_p=e_p^*,
beta_0|M=(v_0,v_1,v_2),

alpha_1=(-B,0,1),   beta_1=(-A,1,0),
alpha_2=( A,1,0),   beta_2=( B,0,1),
alpha_3=( A,1,0),   beta_3=( 0,B,A),                 (1)
```

with `A!=0`.  For one exceptional coordinate, write

```text
z=(t,x_1,x_2,x_3,y_1,y_2,y_3)
```

for the seven new entries.  The seven unwanted contractions form
`N(A,B,v)z=0`, and the wanted `beta^3` coefficient is `d(A,B,v)z`.
The cited theorem classifies every solution with `dz!=0`.

Put

```text
S=v_0+A v_1,   D=v_0-A v_1,
P=v_0-B v_2,   Q=v_0+B v_2.                         (2)
```

## The transverse-kernel principle

Let `F_r^s` and `F_r^p` be the one-marked maps at mode `r`: they send a
candidate third target row to its eight coefficients against all
binary choices at the other three modes on `H_s` and `H_p`.

If `F_r^p` is injective, then the third row `gamma_r` vanishes on
`H_p`.  Globally it is therefore supported on `e_s^*`.  If

```text
F_r^s(e_s^*) != 0,                                  (3)
```

then `gamma_r=0`, contradicting rank three at mode `r`.  The same
argument works with `s,p` interchanged.

The eight rows of a one-marked map are ordered

```text
000,001,010,011,100,101,110,111.                    (4)
```

The exact binary classification gives the following disjoint case
split.  In the table, `h=y_3`; the displayed `4 x 4` minor belongs to
`F_r^p`, and the last column is one nonzero entry of (3).

| binary stratum | mode `r` | rows | determinant | transverse entry |
| --- | ---: | --- | --- | --- |
| `B=0, S!=0` | 3 | `0,3,4,7` | `4hDS` | `S` |
| `B=0, S=0, v_2!=0` | 1 | `0,1,4,7` | `8A^4 v_1v_2(Ay_2+y_3)` | `2Av_2` |
| `B=0, S=0, v_2=0, y_1!=0` | 0 | `0,4,5,7` | `8A^4y_1^2(Ay_2+y_3)` | `2A` |
| `B!=0, v_1=0, v_2P!=0` | 3 | `0,3,4,7` | `4hv_0P` | `P` |
| `B!=0, v_1=0, v_2!=0, P=0` | 1 | `0,1,4,7` | `-8A^3Bhv_2^2` | `2Av_2` |
| `B!=0, v_1=0, v_2=0` | 3 | `0,3,4,7` | `4hv_0^2` | `v_0` |
| `Bv_1!=0, v_2=0, S!=0` | 3 | `0,3,4,7` | `4hv_0S` | `S` |
| `Bv_1!=0, v_2=0, S=0` | 2 | `0,3,5,7` | `8A^4Bhv_1^2` | `-2ABv_1` |
| `Bv_1v_2!=0`, component IV | 2 | `0,3,5,7` | `8A^3Bhv_1(Av_1-Bv_2)` | `-2ABv_1` |

Every factor displayed in its row is nonzero.  This follows directly
from the open conditions in the exact viable-locus classification:
in particular, `h!=0` in all rows containing `h`, while the two
`B=0,S=0` rows have

```text
Ay_2+y_3 != 0.                                      (5)
```

Thus the transverse-kernel principle excludes every row of the table.

## The deepest intersection

Only one case is absent from the table:

```text
B=0,  S=0,  v_2=0,  y_1=0.                         (6)
```

Since `v` is nonzero, rescale it to

```text
beta_0|M=(-A,1,0).
```

On each exceptional coordinate the complete binary solution is

```text
z=(0,x_1,0,0,0,y_2,y_3),   Ay_2+y_3!=0.             (7)
```

Use capitals `X,U,W` for `x_1,y_2,y_3` on `H_s` and lowercase
`x,u,w` on `H_p`.  The two nonzero binary diagonals require

```text
AU+W != 0,   Au+w != 0.                             (8)
```

Stack the `H_s` and `H_p` one-marked equations as maps from the full
five-dimensional third row.  At modes two and three their kernels are
exactly

```text
ker(F_2^s,F_2^p)=C(0,0,-A,W,w),
ker(F_3^s,F_3^p)=C(0,0,-1,U,u).                     (9)
```

Indeed, the `4 x 4` minors using stacked rows `7,8,11,15` and columns
`0,1,3,4` are respectively

```text
-8A^6,   -8A^3,                                     (10)
```

after the normalization above.  The vectors in (9) lie in the
kernels, so (10) proves equality.

Rank three forces the two third rows to be nonzero multiples
`c_2,c_3` of the vectors in (9).  But on `H_s` the mixed target
coefficient is

```text
per(beta_0,beta_1,gamma_2,gamma_3)
 =2A(AU+W)c_2c_3 != 0.                              (11)
```

It has target word `1122`, whereas a diagonal tensor permits only
constant target words.  This final contradiction excludes (6), and
therefore the whole stated branch.

## Verification

Run:

```text
python verify_p5_h31_single_gate_rank_two_m_exclusion.py
python audit_p5_h31_single_gate_rank_two_m_exclusion.py
```

The primary verifier reconstructs the binary extension system, all
normal forms in the table, every displayed one-marked determinant and
transverse entry, both deepest-intersection kernels, and mixed
coefficient (11) symbolically.

The independent audit uses separate modular permanent and
row-reduction code over `F_5` and `F_7`.  It enumerates only the
projective line-arrangement parameters and their kernel extensions,
not ambient maps.  It checks every viable extension against the table
and every ordered pair of deepest-intersection extensions against
(9)-(11).  The finite-field calculation audits boundaries; the proof
above is over characteristic zero.
