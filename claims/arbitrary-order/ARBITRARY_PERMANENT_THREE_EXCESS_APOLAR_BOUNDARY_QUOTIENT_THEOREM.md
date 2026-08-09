# The apolar boundary quotient excludes simultaneous theta completion

## Status

**Exact arbitrary-order two-chord exclusion for the tight aligned conformal
completed-theta setup in characteristic zero.**  The boundary-entanglement
theorem previously required exterior decoupling.  A canonical quotient now
performs that decoupling without assuming it.

For each of the three completed-theta mode ports, quotient its input-colour
space by the span of covectors on cells leaving the core.  Every nonempty
boundary-convolution sector dies in the tensor-product quotient, while the
empty-sector port tensor retains bosonic boundary-entanglement rank at least
two.  Conformality and the exact degree ledger force the empty exterior
tensor to have a nonzero coefficient.  Contracting that coefficient leaves
a rank-at-least-two port tensor on the permanent side and a zero/rank-one
slice on the `Delta_3` side, a contradiction.

Consequently, under the Setup below, a tight aligned conformal minimal theta
containing all three excess cells cannot have both completing chords eligible
in the same coefficient.  No support family, input-word family, or matching
tuple census is used.

The inputs are
[`ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_ENTANGLEMENT_RANK_THEOREM.md`](ARBITRARY_PERMANENT_THREE_EXCESS_BOUNDARY_ENTANGLEMENT_RANK_THEOREM.md)
and the exact boundary convolution in
[`ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_CORE_ALIGNMENT_BOUNDARY.md`](ARBITRARY_PERMANENT_THREE_EXCESS_CONFORMAL_CORE_ALIGNMENT_BOUNDARY.md).

## Setup

Let `K` be the full `K_3,3` obtained from an aligned minimal theta and its two
simultaneously eligible completing chords.  Its mode shore is
`A={a_0,a_1,a_2}` and source shore is `P={p_0,p_1,p_2}`.  Assume the standard
tight completed-theta consequences:

1. `K` contains all three excess cells, one at each `p_j`;
2. every other cell of `K` is a mandatory coordinate cell eligible at the
   selected row word;
3. local mode rank is three and total mode-degree surplus is three;
4. `K` is conformal, so `G-V(K)` has a perfect matching;
5. `m>=4` and the field has characteristic zero.

The boundary-entanglement theorem proves that the only excess-mode/outgoing-
boundary profiles are

```text
(h;s)=(1,1,1;1,1,1),
(h;s)=(2,1,0;0,1,2),                               (1)
```

and that the unspecialized port tensor `T_K` has BER at least two.

## The apolar boundary quotient

Let `B_i` be the span in the input-colour space `V_i` of the covectors on all
cells from `a_i` to sources outside `K`.  Put

```text
pi_i:V_i -> V_i/B_i,            pi=pi_0 tensor pi_1 tensor pi_2. (2)
```

Partition a global matching by the vertices of `K` that it covers using
outside cells.  Let `A_S subset A` and `P_S subset P` be the mode and source
vertices covered externally.  Since the exterior has the same number
`m-3` of modes and sources, every boundary sector satisfies

```text
|A_S|=|P_S|.                                         (3)
```

If the sector is nonempty, (3) gives `A_S!=empty`.  At least one core mode
`a_i` is then covered by a boundary cell whose covector lies in `B_i`; its
image under `pi_i` is zero.  Hence

```text
pi(every nonempty boundary sector)=0.               (4)
```

Let `Omega_empty` be the exterior perfect-matching tensor of `G-V(K)`.  The
full restriction tensor therefore obeys the exact projected factorization

```text
(pi tensor id_ext) T_G
   = pi(T_K) tensor Omega_empty.                    (5)
```

This is a quotient identity for the complete tensor, not a selected
coefficient and not an assumption that the boundary sectors vanish before
projection.

## The port rank survives the quotient

For profile `1+1+1`, `B_i` is one-dimensional.  Local rank says that the
images of the excess form `L_i` and mandatory port coordinate `z_i` are
independent in `V_i/B_i`.  The projected port tensor has exactly the
canonical form (8)--(9) of the boundary-entanglement theorem, so

```text
BER(pi(T_K))>=2.                                    (6)
```

For profile `2+1+0`, the quotient dimensions at the three port modes are
`3,2,1`.  Local rank makes the images of `M,z_1` independent at the middle
row and keeps `z_2` nonzero at the last row.  The projected tensor therefore
has canonical form (11)--(14), including the characteristic-zero factor
`2`, and (6) again holds.

In particular, `pi(T_K)` is nonzero in both profiles.

## The empty exterior tensor cannot vanish

Equation (1) gives

```text
sum_i s_i=3.                                        (7)
```

Thus the three port modes consume all three units of global mode-degree
surplus.  Every exterior mode has degree exactly three.  All excess cells
lie in `K`, so the three cells at an exterior mode are mandatory coordinate
cells.  Local rank three forces their colours to be exactly `0,1,2`, one of
each.

Conformality supplies a perfect matching `F` of `G-V(K)`.  At every exterior
mode, choose the input colour of its cell in `F`.  That mode has exactly one
cell of the chosen colour in the entire support, so its `F`-cell is forced.
Consequently `F` is the unique eligible exterior perfect matching at this
word and

```text
Omega_empty[beta]=product_(e in F) weight(e) !=0.   (8)
```

This proves `Omega_empty!=0` as a tensor.  It uses conformality, exact
support, local rank, and the fact that all excess cells lie in `K`; it does
not infer nonvanishing merely from the existence of a support matching.

## Contradiction with the target tensor

Apply (5) to the restriction identity `T_G=Delta_3` and contract the exterior
modes at the word `beta` from (8).  The permanent side is

```text
Omega_empty[beta] pi(T_K),                          (9)
```

which has BER at least two by (6).

If `beta` is mixed, the corresponding `Delta_3` slice is zero.  If it is
monochromatic of colour `c`, its projected slice is

```text
lambda_c pi_0(e_c) tensor pi_1(e_c) tensor pi_2(e_c), (10)
```

which has BER at most one.  Equations (9)--(10) are impossible.  Therefore:

```text
aligned conformal minimal theta containing all excess cells
+ simultaneous eligibility of both completing chords
    => contradiction for every m>=4.                (11)
```

The result excludes simultaneous **eligibility in the same coefficient**.
It does not say that the two physical chord cells cannot both occur with
different coordinate colours in the uncoloured support.

## Translation and next target

The quotient (2) is apolar: it kills precisely the local directions through
which a core mode can escape into the exterior.  Equation (4) is therefore a
tensorial version of contracting away every nonempty boundary state.  Unlike
a planar/matchgate identity, it is adapted to the actual three-colour row
covectors and survives the bosonic Plucker defect.

This resolves one of the three exact alternatives in the conformal-core
boundary note: simultaneous theta-chord eligibility is now excluded.  The
remaining work is to propagate the resulting nonzero complementary-minor
channel through the three port extensions strongly enough to force a pure
switch or an odd exchange-lattice relation.

## Verification

Run:

```text
uv run --with sympy python verify_arbitrary_permanent_three_excess_apolar_boundary_quotient_theorem.py
python audit_arbitrary_permanent_three_excess_apolar_boundary_quotient_theorem.py
```

The primary verifier replays the projected canonical flattenings, the two
profile quotient dimensions, boundary-shore balance, and the unique exterior
colour selector.  The no-import audit independently checks the balance-kill
logic, profile dimensions, and rank ledgers.  The arbitrary-order tensor
factorization and conformal nonvanishing argument are the proofs above.

## Boundary

```text
nonempty boundary sectors after quotient:       ZERO;
projected port BER:                             AT LEAST TWO;
empty exterior tensor:                          NONZERO;
tight aligned conformal simultaneous completion:
                                                  EXCLUDED FOR m>=4;
physical chords with different word colours:     NOT EXCLUDED;
one nonzero complementary channel propagated:    NOT YET;
exclusion of all support 3m+3 cases:             NOT PROVED;
global Krenn--Gu conjecture:                     UNRESOLVED.
```
