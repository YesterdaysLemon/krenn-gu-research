# Two-slice shared-hafnian transfer obstruction

## Status and scope

**Proved conditional source obstruction over every field, for every even
order n>=4.** The proof uses two full colour slices sharing an actual induced
hafnian. At n=8, independent physical polynomial reconstruction verifies four
colour types, including a 20-literal pattern excluding the Boolean survivor
of all the newly checked two-edge shore patterns.

This is a reusable implication under explicit zero/nonzero premises. There is
no theorem that every hypothetical witness supplies these premises, and no
all-order reduction to eight vertices. Global Krenn–Gu is **UNRESOLVED**.
No Lean formalization or separate-human refereeing is claimed.

## Arbitrary-order statement

Name four distinct boundary vertices `x,p,q,y`; let `F` contain the remaining
`n-4` vertices. Choose a base colour c and colours `alpha,beta,s` different
from c; the latter three need not be distinct. Fix F and p to colour c,
and vary x in `{alpha,c}`, q in `{s,c}`, and y in `{beta,c}`.

For every `i in F`, require the oriented physical entries

```text
W_ip[c,c]=W_iq[c,s]=W_iy[c,beta]=W_iy[c,c]=0.
```

Also require `W_pq[c,s]=W_pq[c,c]=0`. These are `4(n-4)+2` zeros.
Define

```text
A_a=W_xp[a,c], B_a=W_xq[a,s],
C_d=W_py[c,d], D_d=W_qy[c,d], E_d=W_qy[s,d].
```

If `B_alpha*C_beta != 0`, the source cannot realize a diagonal target with
nonzero pure c amplitude. All other entries are arbitrary. No cofactor,
determinant, or unlisted entry is assumed nonzero.

## Proof by transfer between two exact source slices

Let `T_s(a,d)` and `T_c(a,d)` denote the two complete matching coefficients.
Set `H=haf(W[F]; all c)`, and let `R_a` be the actual induced hafnian on
`F union {x,q}`, with x in colour a and every other vertex c.

In the q=s slice, p and q each can pair only with x or y. The two boundary
pairings are therefore `xp+qy` and `xq+py`. In the q=c slice, pairing p
with x forces y to pair with q; pairing p with y leaves R_a. Consequently

```text
T_s(a,d) = H*(A_a*E_d + B_a*C_d),
T_c(a,d) = H*A_a*D_d + R_a*C_d.                        (1)
```

These are full matching expansions, not independently chosen local tensors.
The same physical H appears in both lines, including when H=0.

On the x colours `(alpha,c)`, put `u_Z=Z_alpha*e_c*-Z_c*e_alpha*`.
On the y colours `(beta,c)`, use the analogous covectors `v_Z`.
They satisfy `u_Z(Z)=0`, `u_Z(Q)=-u_Q(Z)`, and the analogous y identities.
Apply `u_A tensor v_D` to the first line, and `u_B tensor v_C` to the second:

```text
(u_A tensor v_D)(T_s) = H*u_A(B)*v_D(C),
(u_B tensor v_C)(T_c) = H*u_B(A)*v_C(D).
```

Both alternating factors change sign, so the right sides are equal. Thus

```text
(u_A tensor v_D)(T_s) - (u_B tensor v_C)(T_c) = 0.      (2)
```

For the target, the fixed p=c slot selects the pure c term even when F is
empty. Since s differs from c, its first slice is zero. The second is
`lambda_c*e_c tensor e_c`, making (2) equal
`-lambda_c*B_alpha*C_beta`, a contradiction. Every step is polynomial and
division-free, so the proof includes all fields and n=4 with `haf(empty)=1`.

This differs from annihilating both slices separately: their potentially
nonzero contracted contributions cancel because H is shared. Replacing that
common source coefficient by two unrelated values loses the implication.

## Eight-vertex certificate

Take `(x,p,q,y)=(0,5,6,7)`, `F={1,2,3,4}`, base c=2, and
`(alpha,beta,s)=(0,0,1)`. The zeros are

```text
99,107,115,117,144,152,160,162,180,188,196,198,
207,215,223,225,233,234.
```

Require only `g47=W06[0,1]` and `g241=W57[2,0]` nonzero.
For `P_w=T_W(w)-delta_w`, equation (2) gives

```text
g47*g241 =
   g39*g250 P_22222212 - g39*g252 P_22222210
 - g45*g250 P_02222212 + g45*g252 P_02222210
 - g47*g241 P_22222222 + g47*g243 P_22222220
 + g53*g241 P_02222222 - g53*g243 P_02222220.           (3)
```

With only those eighteen zeros, the source term counts are
`6,6,6,6,18,18,18,18`. The 96 signed degree-six contributions cancel in
48 pairs of identical physical monomials. The pure-minus-one row leaves
exactly the displayed nonzero monomial. The earlier boundary relation rho
is not used.

The [fixture](../../tests/fixtures/eight_vertex_two_slice_transfer.json) and
[primary pattern generator](../../src/krenn_gu/two_slice_transfer.py) also cover
all four ternary equality types: after a common colour permutation set
`alpha=0,c=2`, and let `(beta,s)` range over `{0,1}^2`. This is a complete
colour classification of this specific template, not of all sources.

The [independent audit](../finite/n08/audit_eight_vertex_two_slice_transfer.py)
reconstructs all physical entries and all 105 perfect matchings, using the
separate bitmask/permutation-quotient route. Each type passes exact reconstruction
and mathematical mutations: every deleted zero, wrong sign, omitted source,
missing pure target, and removed target-nonzero premise. Each zero is necessary
for this displayed identity with every other entry arbitrary, not necessarily
for every possible support exclusion.

```text
python claims/finite/n08/audit_eight_vertex_two_slice_transfer.py
python claims/finite/n08/verify_eight_vertex_two_slice_transfer.py
```

## Relation to the parent

The [source-module attempt](../../docs/strategy/source-module-resolution-attempt-2026-09-14.md)
records the exact parent and bounded computations. The new identity was found
on the checked Boolean survivor of all four previous physical-cut orbits and
all four [two-edge shore pattern types](../finite/n08/EIGHT_VERTEX_TWO_EDGE_SURPLUS_SHORE_EXCLUSION.md).
It is source-coupled progress beyond those cuts; occurrence and unrestricted
parent exclusion remain separate obligations. It also supplies the concrete
degree-six interaction absent from the full declared
[degree-five module](../finite/n08/EIGHT_VERTEX_DEGREE_FIVE_SOURCE_MODULE_LIMITATION.md).

The combined parent test adds all four transfer colour types (10,080 unique
vertex/common-colour images each) to the prior eight pattern orbits. It remains
SAT with 600,063 variables and 4,748,964 clauses. The new 129-entry physical
projection and every auxiliary Boolean value are preserved in the
[packed assignment](../../tests/fixtures/eight_vertex_two_slice_parent_survivor.json).
The generator checks every clause, and the replay regenerates the exact CNF
and verifies its SHA-256 before checking the frozen bits without solving.
Thus the tested Boolean occurrence implication fails; no complex weights are
supplied by this assignment. Its complete degree-six pure-attached calculation
has 142,328 rows and leading rank 142,328: no lower pure-target relation can
couple between grades, and no augmented block contains a monomial. This is a
bounded limitation; mixed-only unattached grades and the full ideal are outside
that computation. See the resolution attempt for the precise scope and replay.
