# `P_6` simultaneous-kernel and natural-lift obstructions

## Status

This note gives four exact statements over `C` about a possible restriction

```text
P_6 -> Delta_3.
```

1. It gives a necessary-and-sufficient simultaneous-kernel formulation after
   five local maps are fixed.
2. It identifies the sharp common-port row-deletion normal form forced by the
   five-root/six-blocker extraction.
3. It proves that the published support-four `P_5` construction cannot be
   lifted by the natural zero-row embedding, even when the new fifth map is
   arbitrary.
4. It excludes every restriction whose local target columns are scaled source
   coordinate vectors.

These are reductions and restricted no-go theorems.  They do **not** decide
the unrestricted `P_6 -> Delta_3` question, do not imply
`P_5 -> Delta_3`, and do not resolve the Krenn--Gu conjecture.

## The exact simultaneous-kernel criterion

Write

```text
P_6 = sum_(sigma in S_6)
        e_(sigma(0)) tensor ... tensor e_(sigma(5)).       (1)
```

Fix five local maps

```text
L_i:C^6 -> C^3,   i=0,...,4,
```

and define the linear contraction map

```text
Phi(z)=(tensor_(i=0)^4 L_i)(z contract P_6).              (2)
```

Let

```text
D_5=span{e_0^5,e_1^5,e_2^5}
```

be the diagonal three-plane, let `pi_off` delete those three target
coordinates, and put

```text
M_L=pi_off composed with Phi:C^6 -> C^240.                (3)
```

There is a sixth local map completing the chosen five maps to a restriction
of `P_6` onto `Delta_3` if and only if

```text
Phi(ker(M_L)) = D_5.                                      (4)
```

Here the left side is automatically contained in `D_5`.  If a restriction
exists, the three pullback columns `u_c` of its sixth map satisfy

```text
Phi(u_c)=lambda_c e_c^5,   lambda_c != 0,                 (5)
```

so (4) follows.  Conversely, if (4) holds, choose in `ker(M_L)` a preimage
of each `e_c^5`; using those three vectors as the sixth pullback columns gives
the required restriction.  In particular, every solution satisfies

```text
dim ker(M_L) >= 3,
rank(M_L) <= 3,                                           (6)
```

and the diagonal part of `Phi` has rank three on the kernel.  The last
condition is essential: low off-diagonal rank alone is not sufficient.

This is the six-mode analogue of the rank-at-most-two contraction-pencil
condition for `P_5`, with one additional source dimension.

## The five-root/six-blocker common-port normal form

The `r=5`, `|B|=6` case extracted by
[`ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md`](ODD_RESIDUAL_PORT_PERMANENT_EXTRACTION.md)
has more structure than six arbitrary local maps.  Index the source rows by
the five roots and one common port `p`.  At blocker mode `u`, write

```text
M_u = [ five root rows a_(i,u) ; port row g_u ],
A_u = span{a_(i,u):i in R} subset (C^3)*.              (B1)
```

The extracted diagonal is concise, so every `M_u` has rank three.  For each
target colour, the multi-star theorem says

```text
B_c={u:e_c^* belongs to A_u},   |B_c|>=5.              (B2)
```

Define the missing-colour support at mode `u` by

```text
S_u={c:u notin B_c}.                                   (B3)
```

There are six blocker modes.  Therefore each colour occurs in at most one
set `S_u`, the nonempty sets `S_u` are pairwise disjoint, and

```text
sum_u |S_u| <= 3.                                     (B4)
```

Every blocker belongs to the union `B`, so no `S_u` has size three.

If `S_u` is empty, `A_u` contains all three coordinate covectors and hence
has rank three.  The root-row projection of the pullback three-plane is
injective, so that plane does not contain the port coordinate vector `e_p`.

Suppose `S_u` is nonempty.  Because `u` blocks at least one colour, `A_u` is
nonzero.  It cannot have dimension one: adjoining the single port row would
then give `rank(M_u)<=2`.  It cannot have dimension three because a
three-dimensional `A_u` would block every colour.  Consequently

```text
dim(A_u)=2,
K_u=A_u^perp=<k_u>                                     (B5)
```

is a line.  A coordinate covector `e_c^*` belongs to `A_u=K_u^perp` exactly
when `k_u[c]=0`, so

```text
supp(k_u)=S_u.                                        (B6)
```

Rank three of `M_u` also forces `g_u notin A_u`, equivalently
`g_u(k_u)!=0`.  Thus the exceptional kernel maps to the common port:

```text
M_u k_u = g_u(k_u) e_p != 0.                          (B7)
```

For every `c in S_u`, condition (B2) is tight:
`B_c=B minus {u}`.  The exact-blocker factorisation gives the compatible
stronger relation

```text
g_u restricted to K_u
  = gamma_(u,c) e_c^* restricted to K_u,
gamma_(u,c) != 0.                                     (B8)
```

Equivalently, `g_u-gamma_(u,c)e_c^* belongs to A_u`.  When `|S_u|=2`,
the two missing coordinate restrictions are proportional on the line `K_u`,
so the two instances of (B8) are consistent.

Up to blocker and colour permutations, the complete list of missing-support
profiles is

```text
empty,
1,
1+1,
1+1+1,
2,
2+1.                                                  (B9)
```

In particular, at least three of the six root-row submatrices have rank
three, and at most three have rank two with pairwise disjoint target kernels.

This does not yield the desired `P_5` shortcut.  Contracting an exceptional
mode by `k_u` uses (B7) to contract `P_6` at the coordinate `e_p`, so the
source tensor becomes `P_5`.  But the target contraction is

```text
sum_(c in S_u) lambda_c k_u[c] e_c^5,                 (B10)
```

which is only `Delta_1` or `Delta_2`, never `Delta_3`.  At a full mode the
pullback plane does not contain `e_p` at all.  Thus the blocker incidence
blocks the naive coordinate-contraction reduction instead of proving
nonexistence.  A next exact problem is to classify the six common-port
deletion profiles (B9) subject to the simultaneous-kernel criterion (4).
For the `1+1+1` profile, the three overlapping pure `P_5` deletions have now
been reduced to a marked squarefree triple-product incidence.  Its complete
linear Frobenius relaxation is consistent; nonlinear shared factorisation of
the 27 marked cubic products is the remaining condition.  See
[`P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md`](P6_COMMON_PORT_111_FROBENIUS_REDUCTION.md).

## The support-four construction does not zero-row lift

Let `A_0,...,A_3` be the four integer maps in
[`SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md`](SUPPORT_FOUR_P5_CONTRACTION_RESTRICTION.md),
and define

```text
R(z)=(tensor_(i=0)^3 A_i)(z contract P_5),
N=pi_off composed with R:C^5 -> C^78.                    (7)
```

The exact row reduction already used in the simultaneous-pencil analysis is

```text
rank(N)=4,
ker(N)=span(1,1,1,1,0),                                  (8)
```

and the displayed kernel generator has diagonal image `(12,12,12)`.

Extend every `A_i` to `C^6` by adding a zero row at source coordinate `5`.
Let

```text
L:C^6 -> C^3
```

be an otherwise arbitrary fifth map, set `ell=L(e_5)`, and form `Phi` from
these five maps as in (2).  Put

```text
E=span(e_0,...,e_4) subset C^6.
```

For every `z in E`, the four zero-extended maps cannot consume source
coordinate `5`.  Hence the fifth map must consume it, and direct expansion of
the permanent gives

```text
Phi(z)=R(z) tensor ell.                                   (9)
```

If `ell != 0`, project the five-mode off-diagonal target once more onto

```text
(four-mode off-diagonal space) tensor C^3.
```

By (9), the restriction of this projection to `E` is

```text
z |-> N(z) tensor ell,
```

which has rank four by (8).  Therefore `rank(M_L)>=4`, contradicting the
necessary bound (6).

If `ell=0`, equation (9) says `Phi(E)=0`.  Since `C^6/E` is one-dimensional,
the whole image of `Phi` has dimension at most one.  Its diagonal image on
`ker(M_L)` therefore cannot have rank three, contradicting (4).

Thus:

```text
No zero-row extension of the four published support-four maps,
together with any arbitrary fifth map, lifts to P_6 -> Delta_3. (10)
```

The same proof applies to every member of the published two-parameter family:
its four-mode off-diagonal contraction map has rank four everywhere on the
family.  This result does not cover extensions in which one or more of the
four old maps has a nonzero new source row.

## No coordinate-column restriction

Call a local map *coordinate-column* if each of its three target pullback
columns is a scalar multiple of one source basis vector.  Suppose all six
local maps had this form and gave `Delta_3`.

For each target colour `c`, its nonzero pure coefficient forces six nonzero
scalars and a permutation

```text
sigma_c:{0,...,5}->{0,...,5}:                            (11)
```

the source coordinate selected in each mode.  A target word has a nonzero
coefficient precisely when its six selected source coordinates form a
permutation; in this coordinate-column setting there is only one possible
permanent monomial, so cancellation is unavailable.

Fix two colours `c,d`.  The union of their permutation matchings decomposes
into the alternating cycles of the relative permutation

```text
sigma_c^(-1) sigma_d.                                    (12)
```

If (12) has more than one cycle, switch from the `c` matching to the `d`
matching on one proper nonempty cycle.  The result is another perfect
matching and hence a nonzero, nonconstant two-colour target coefficient.  A
fixed-point cycle is allowed in this argument: changing the target colour at
that mode keeps the same source edge but still produces a mixed target word.
Therefore absence of forbidden two-colour coefficients forces every pairwise
relative permutation to be a single 6-cycle.

But a 6-cycle is odd.  After setting

```text
a=sigma_0^(-1) sigma_1,
b=sigma_0^(-1) sigma_2,
```

both `a` and `b` would be odd, so

```text
sigma_1^(-1) sigma_2 = a^(-1)b
```

is even and cannot be a 6-cycle.  This contradiction proves

```text
P_6 has no coordinate-column restriction to Delta_3.     (13)
```

The same parity proof excludes coordinate-column restrictions
`P_n -> Delta_3` for every even `n`.

## What contraction does and does not imply

Suppose an unrestricted `P_6 -> Delta_3` restriction has sixth-mode pullback
plane

```text
U=span(u_0,u_1,u_2) subset C^6.
```

Contracting the sixth target mode by `t=(t_0,t_1,t_2)` contracts `P_6` by

```text
u(t)=t_0 u_0+t_1 u_1+t_2 u_2                            (14)
```

and sends the result to

```text
sum_c lambda_c t_c e_c^5.                               (15)
```

Consequently there is one useful conditional reduction: if `U` contains a
source coordinate vector `e_j` whose preimage `t` in (14) has all three
coordinates nonzero, then `e_j contract P_6` is a coordinate copy of `P_5`
and (15), after rescaling, proves `P_5 -> Delta_3`.

There is no unconditional monotonicity here.  A general three-plane in
`C^6` need not contain a coordinate point, and a coordinate point that is
present can have a preimage on a target coordinate hyperplane.  Contracting
an arbitrary sixth source vector gives a support-up-to-six contraction, not
automatically `P_5`.  Likewise, the known support-four `P_5` example is an
order-four tensor after contraction and does not restore the two missing
modes of a `P_6` restriction.

Ordinary flattening ranks also give no obstruction: all target flattenings
have rank three, while the corresponding `P_6` flattenings have rank at least
three and local maps are allowed to lower rank.

## Replay

Run:

```text
python verify_p6_simultaneous_kernel_and_natural_lift.py
python audit_p6_simultaneous_kernel_and_natural_lift.py
```

The primary verifier reconstructs the `5!` permanent contractions over the
integers, checks (8), exhausts the zero-row basis identities behind (9), and
enumerates the cycle-switch and parity obstruction in `S_6`.  It also
reconstructs all 337 labelled common-port incidence patterns, the six profiles
in (B9), and rank-sharp local models for all seven proper missing-colour masks.
The independent audit uses subset dynamic programming and modular row
reduction over `F_5` and `F_7`, rebuilds the profile census from blocker masks,
and checks the alternating cycles with a separate graph walk.  The finite
computations audit the displayed identities; the proofs above are over `C`.

## Boundary

The surviving `P_6` problem is genuinely simultaneous.  Five rank-three
local maps would have to make the `240 x 6` off-diagonal contraction matrix
have rank at most three while retaining diagonal rank three on its kernel.
The extracted six-blocker maps additionally lie in one of the six common-port
deletion profiles (B9), but those incidences only expose `Delta_1` or
`Delta_2` coordinate contractions.  The coordinate-column locus and the
natural zero-row lift of the only known support-four `P_5` family miss the
simultaneous condition, while general dense maps and nonzero-row extensions
remain open.
Even the `1+1+1` profile survives every linear Frobenius pairing and dimension
condition; its shared triple-product factorisation is an explicit nonlinear
frontier rather than a completed obstruction.
