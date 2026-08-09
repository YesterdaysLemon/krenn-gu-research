# Bosonic boundary-entanglement rank for a completed theta

## Status

**Exact characteristic-zero tensor-flattening theorem.**  The Hamming-face
pinch excludes a coefficient-induced completed `K_3,3` when its three excess
cells form a port matching.  A second invariant covers the other possible
mode-incidence type.

For a tight completed theta with one excess cell at each of its three source
ports, the unspecialized `3 x 3` permanent port tensor has one-versus-two
flattening rank at least two.  This holds for both possible excess-mode
profiles:

```text
1+1+1,                  2+1+0.                      (1)
```

Therefore the port tensor cannot equal a zero or rank-one slice of
`Delta_3`.  At arbitrary order `m>=4`, a full restriction must either exclude
the two-chord completion or retain nonempty exterior boundary sectors that
cancel its rank-two contribution.  This is a conditional chord-elimination
theorem and an exact description of what any surviving boundary convolution
must carry.

The input boundary convolution is in
[`ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_CORE_ALIGNMENT_BOUNDARY.md`](ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_CORE_ALIGNMENT_BOUNDARY.md),
and the bosonic factor is exposed in
[`ARBITRARY_PERMANENT_THREE_EXCESS_BOSONIC_PLUCKER_DEFECT_THEOREM.md`](ARBITRARY_PERMANENT_THREE_EXCESS_BOSONIC_PLUCKER_DEFECT_THEOREM.md).

## Definition: boundary-entanglement rank

Let `V_i` be the three-dimensional input-colour space at port mode `a_i`.
Write the nine physical port covectors as `ell_ij in V_i`.  Their
unspecialized permanent tensor is

```text
T_K=sum_(sigma in S_3)
       ell_(0,sigma(0)) tensor ell_(1,sigma(1))
                         tensor ell_(2,sigma(2))
    in V_0 tensor V_1 tensor V_2.                  (2)
```

Define the **bosonic boundary-entanglement rank**

```text
BER(T_K)=max_i rank Flat_(i|{0,1,2} minus {i})(T_K). (3)
```

This is ordinary tensor flattening rank used as a boundary invariant.  The
name emphasizes its role here: it measures how much non-product information
the bosonic permanent core must export through the boundary.

## Tight completed-theta hypotheses

Assume:

1. both completing chords of an aligned minimal theta are present, giving a
   full port `K_3,3` on modes `a_0,a_1,a_2` and exceptional sources
   `p_0,p_1,p_2`;
2. there is exactly one excess cell at each `p_j`, and all three excess cells
   lie in the port block;
3. every non-excess port cell is mandatory and has the coordinate colour of
   the selected row word at its mode;
4. local mode rank is three and the global mode-degree excess is three.

Let `h_i` be the number of excess port cells at `a_i`, and let `s_i` be the
number of cells at `a_i` outside the port `K_3,3`.  Inside row `i`, all
`3-h_i` mandatory port covectors are collinear.  Hence local rank three
requires

```text
h_i+s_i>=2.                                         (4)
```

Also

```text
sum_i h_i=3,                 sum_i s_i<=3,          (5)
```

because the three port modes already have degree three and the total mode
surplus is three.  Summing (4) forces equality everywhere:

```text
sum_i s_i=3,                 h_i+s_i=2.             (6)
```

Thus, up to permuting rows, exactly two profiles survive:

```text
(h;s)=(1,1,1;1,1,1),
(h;s)=(2,1,0;0,1,2).                                (7)
```

In particular, `3+0+0` excess-mode incidence is impossible in a completed
theta.  No support census is involved in (4)--(7).

## Rank theorem: profile `1+1+1`

Relabel the unique excess cells as the diagonal.  At row `i`, write its
excess form as `L_i` and the common mandatory port coordinate as `z_i`.
Local rank and `s_i=1` force `L_i,z_i` to be independent.  After absorbing
nonzero cell scalars, the port matrix has the form

```text
[ L_0, a z_0, b z_0 ]
[ c z_1, L_1, d z_1 ]                               (8)
[ e z_2, f z_2, L_2 ]
```

with `a,b,c,d,e,f!=0`.

Flatten along row zero.  In the ordered basis

```text
(z_1z_2, z_1L_2, L_1z_2, L_1L_2),
```

the `z_0` and `L_0` coefficient rows include

```text
z_0:  (ade+bcf, ac, be, 0),
L_0:  (df,       0,  0, 1).                        (9)
```

The minor on the `z_1L_2,L_1L_2` columns is `ac!=0`.  Therefore

```text
BER(T_K)>=2.                                        (10)
```

The `L_0L_1L_2` term is the private all-excess matching tensor; no mandatory
row-zero term can reproduce it.

## Rank theorem: profile `2+1+0`

Relabel rows and sources so the port matrix is

```text
[ L_0, L_1, a z_0 ]
[ b z_1, c z_1, M ]                                (11)
[ d z_2, e z_2, f z_2 ]
```

where all displayed scalars are nonzero,
`{L_0,L_1,z_0}` is independent, and `M,z_1` are independent.  These
independences follow from local rank together with `(s_0,s_1,s_2)=(0,1,2)`.

After factoring `z_2`, the row-zero flattening coefficient vectors in the
basis `(z_1,M)` are

```text
v_0=(cf,e)       for L_0,
v_1=(bf,d)       for L_1,
v_z=(a(be+cd),0) for z_0.                           (12)
```

If `v_0,v_1` are independent, the flattening rank is already at least two.
If they are dependent, then

```text
cd=be.                                              (13)
```

In that case

```text
v_z=(2abe,0)!=0                                    (14)
```

in characteristic zero.  Since `v_0` has the nonzero `M` component `e`, it
is independent of `v_z`.  Thus (10) holds in the second profile as well.
The factor `2` in (14) is the tensor-level return of the bosonic Plucker
defect.

## Conditional exterior-decoupling theorem

Let `m>=4` and freeze the `m-3` exterior modes at a word `beta`.  Suppose the
boundary convolution has no nonempty sectors and its empty sector is a
nonzero scalar `W_beta`.  The surviving restriction slice is then

```text
W_beta T_K.                                         (15)
```

The corresponding slice of

```text
Delta_3=sum_c lambda_c e_c^(tensor m)
```

is zero if `beta` is mixed, and is

```text
lambda_c e_c tensor e_c tensor e_c                 (16)
```

if `beta` is monochromatic of colour `c`.  Its BER is respectively zero or
one.  Equations (10) and (15) give BER at least two, a contradiction.

Therefore:

```text
exterior-decoupled tight completed theta
    => impossible in a full P_m -> Delta_3 restriction, m>=4.  (17)
```

Equivalently, a completed theta necessarily exports boundary entanglement:
for the fixed exterior word `beta`, whenever its empty-sector aggregate is
nonzero, the aggregate contribution of at least one nonempty boundary sector
must be nonzero and participate in cancellation.  This does not select an
individual support matching or a particular `Omega_S`.  The remaining global
target is to eliminate all such aggregates, or prove that their tensor images
cannot cancel (9) or (12).

The later apolar boundary quotient kills every nonempty sector termwise and
uses the tight exterior degree ledger to prove the empty sector nonzero.
Consequently simultaneous eligibility of both theta-completing chords is
excluded outright.  See
`ARBITRARY_PERMANENT_THREE_EXCESS_APOLAR_BOUNDARY_QUOTIENT_THEOREM.md`.

For `m=3` there is no exterior word: the target slice is `Delta_3` itself,
whose flattening rank is three.  The rank-two lower bound alone does not
exclude that separate case.

## Exact check on the six-token model

The `21`-cell `m=6` model has profile `(h;s)=(1,1,1;1,1,1)`.  Fix

```text
w(b_i)=i+2.
```

Then `b_iq_i` is the only eligible cell at `b_i`, so the exterior matching is
forced and every nonempty boundary sector is absent.  At each `a_i`, choose
the private third colour `i+2`.  The only eligible port cell is `E_i=a_ip_i`.
The global coefficient therefore has the unique matching

```text
{E_0,E_1,E_2,b_0q_0,b_1q_1,b_2q_2},               (18)
```

with nonzero weight.  Its word is mixed, so it is forbidden by `Delta_3`.
This recovers the top Hamming-face pinch as the simplest BER witness.

## Verification

Run:

```text
uv run --with sympy python claims/arbitrary-order/verify_arbitrary_permanent_three_excess_boundary_entanglement_rank_theorem.py
python claims/arbitrary-order/audit_arbitrary_permanent_three_excess_boundary_entanglement_rank_theorem.py
```

The primary verifier expands the two canonical port tensors, reconstructs
their flattenings, checks the decisive minors and characteristic-zero case
split, and replays the two valid degree profiles.  The no-import audit checks
the displayed table consequences and an exact factor-two degeneracy instance.
The arbitrary-order convolution conclusion is the tensor-rank proof above.

## Boundary

```text
completed-theta excess-mode profiles:       ONLY 1+1+1 OR 2+1+0;
profile 3+0+0:                              EXCLUDED;
BER of every tight completed theta:         AT LEAST TWO;
zero/rank-one exterior-decoupled slice:      IMPOSSIBLE FOR m>=4;
nonempty boundary sectors forced absent:     NOT PROVED;
boundary-sector rank cancellation:           NOT EXCLUDED;
m=3 by BER alone:                            NOT EXCLUDED;
exclusion of all support 3m+3 cases:         NOT PROVED;
global Krenn--Gu conjecture:                 UNRESOLVED.
```
