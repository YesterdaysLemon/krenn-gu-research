# Vacuum-free dual-Wick projectivization and the empty-scalar escape

## Status

**Exact characteristic-zero observability theorem and sharp physical
boundary.**  For a two-residual response, the missing residual-empty scalar
`h=z_empty` can be eliminated from the dual-Wick equations.  On every
nonzero direct four- or six-point chart it is then recovered uniquely.  In a
`P_7` root-budget window this uses only the already eligible layers, once the
needed direct pair faces have been supplied by four-window tomography.

The exceptional moment-null boundary is real.  There is a one-parameter
family of honest seven-port, two-residual block graphs for which the complete
direct response and every nonempty two-residual-present response are fixed,
but `h` is arbitrary.  Exact synchronized one-residual companion depths recover
`h` whenever they expose both incidence rows and one nonzero direct pair;
the current `P_7` selector theory does not yet supply that synchronization.

The opposite-pair additive locus used by the marked-star selector is not a
physical, mixed-colour, companion-depth, or square-zero cumulant identity.
An honest common block graph realizes its three opposite-pair sums
arbitrarily.  Additivity is therefore a sufficient observation condition,
not a universal consequence of graph response.

These results remove the empty face on a dense observable chart and identify
its exact escape.  They do not force the four clean fan windows, align their
normalizations, or exclude the full coloured `P_7` target.  The `P_7`
restriction problem and the Krenn--Gu conjecture remain
**UNKNOWN/UNRESOLVED**.

## 1. Projectivizing the two-residual insertion equations

Let `U` be a scalar transversal port chart.  Write

```text
m_S=haf B[S],                 z_S=haf G[Q union S],
Q={p,r},                      h=z_empty=A_pr.          (1)
```

The empty direct moment is not an unknown graph parameter:

```text
m_empty=haf(empty matrix)=1.                           (2)
```

Only the residual-empty coefficient `h` is missing.  For an even set
`S`, put `|S|=2d>=4` and define the completely nonempty insertion defect

```text
D_S=sum_({u,v} subset S) z_uv m_(S minus {u,v})-z_S.  (3)
```

The two-residual dual-Wick equation gives

```text
D_S=(d-1) h m_S.                                      (4)
```

### Theorem 1 (vacuum-free dual-Wick projectivization)

For any two even port sets `S,T`, of orders `2d,2e>=4`, every honest
two-residual response satisfies

```text
(e-1)m_T D_S-(d-1)m_S D_T=0.                          (5)
```

If `m_S!=0`, then the missing residual scalar is uniquely recovered by

```text
h=D_S/((d-1)m_S).                                     (6)
```

Equivalently, the two rows indexed by

```text
((d-1)m_S)_S,                  (D_S)_S                (7)
```

have rank at most one.  This rank-one formulation stays meaningful on every
coordinate boundary and does not divide by a chosen moment.

Proof.  For two residual vertices, the uncorrected insertion identity is

```text
z_S=sum_({u,v} subset S) z_uv m_(S minus {u,v})
    -(d-1)h m_S.
```

Rearrangement proves (4).  Eliminating the common scalar `h` between the
copies for `S` and `T` proves (5); division on `m_S!=0` proves (6).

For two four-windows `W,V`, (5) is simply

```text
D_W m_V-D_V m_W=0.                                   (8)
```

For a four-set `W` and six-set `X`, it is

```text
2m_X D_W-m_W D_X=0.                                  (9)
```

Thus the missing empty coefficient has an observable projective shadow even
when no window is selected as a denominator.

## 2. Exact consequence for the P7 root budget

At residual order two, the proved `P_7` root budget makes

```text
z_2,z_4,z_6 and m_4,m_6                              (10)
```

eligible.  The four-window tetrahedral tomography theorem conditionally
recovers the six missing `m_2` faces of a target four-window from compatible
marked-star sensors.  Therefore:

1. once those four fan sensors are legal and normalized compatibly, `D_W`
   is observable for the target four-window;
2. if `m_W!=0`, formula (6) recovers `h` from that one window;
3. two reconstructed four-windows can be tested by the empty-free equation
   (8);
4. `D_X` on a six-set uses only `z_2,m_4,z_6`, hence lies entirely inside
   the root-budget layers even before direct pair tomography;
5. if `m_X!=0`, the six-point equation recovers `h`, and (9) synchronizes it
   with every reconstructed four-window.

Consequently the empty face is not an independent generic obstruction.  The
remaining issues are legal forcing of the fan windows, common selector
normalization, and the simultaneous moment-null boundary.

Theorem 1 is an elimination theorem for physical response equations.  It
does not license using (6) to declare arbitrary GHZ-derived values physical:
all base Wick, tangent-Wick, and bosonic-channel conditions still have to
hold.

## 3. Additivity is not forced by any physical response identity

Take four ports and two residual vertices.  Put `B=0`, `h=0`, and choose
residual incidence rows

```text
a=(1,0,0,0),                 b=(0,P,Q,R).             (11)
```

The corrected and uncorrected pair responses coincide:

```text
z_12=P, z_13=Q, z_14=R,      z_23=z_24=z_34=0.        (12)
```

Their three opposite-pair sums are exactly

```text
z_12+z_34=P,
z_13+z_24=Q,
z_14+z_23=R.                                          (13)
```

Since `P,Q,R` are arbitrary, the physical response map to the three
opposite-pair sums is surjective.  Its additive locus is the proper
codimension-two diagonal `P=Q=R`.

### Theorem 2 (physical non-forcing of the additive selector locus)

Neither two-residual physicality, the complete square-zero dual-Wick
cumulant identities, nor exact one-residual companion data force the
opposite-pair equalities.

The same conclusion holds after imposing common mixed-colour block
realizability.  Choose one covector `ell_i` at each port, install the
incidences in (11) along those covectors, and set every other block entry to
zero.  This is one honest symmetric coloured block graph.  Hence all of its
mixed-colour equations and pair-block rank circuits hold automatically,
while (13) remains arbitrary on the chosen transversal chart.

Proof.  Equations (11)--(12) are the physical factorization
`z_ij=a_i b_j+b_i a_j`.  Its relative response polynomial is the pure
quadratic `Q_K`, so every tangent cumulant outside degree two vanishes.
Retaining only `p` or only `r` exposes the exact rows `a` and `b`; their
existence plainly leaves `P,Q,R` arbitrary.  The rank-one coloured
embedding just described realizes the same scalar specialization inside a
single common block graph.

Thus additive weights are a sharp linear criterion for recovering a hidden
pair insertion from four marked stars.  They are not an equation that a
future mixed-colour or cumulant argument may assume without using additional
GHZ target information.

## 4. A physical empty-scalar escape on the moment-null boundary

Use seven ports `1,...,7`, two residual vertices `p,r`, and a parameter
`lambda`.  The only nonzero direct port edge and residual incidences are

```text
B_12=1,             A_pr=lambda,
R_p1=-lambda,       R_r2=1.                            (14)
```

Every other edge is zero.  In the square-zero port algebra, with
`t=x_1x_2` and `t^2=0`,

```text
M=1+t,
Phi=lambda-lambda t,
Z=M Phi=lambda.                                       (15)
```

Therefore all members of the family have exactly the same data

```text
all direct moments m_S, including m_12=1;
all nonempty residual-present moments z_S=0;
all marked-star observations of the direct pair layer;
all nonempty mixed-colour specializations after a rank-one block lift. (16)
```

But `z_empty=lambda` is arbitrary.  In particular, all root-budget layers
`z_2,z_4,z_6,m_4,m_6` are fixed, all direct pair faces may be granted, and
every direct four- and six-point moment vanishes.  Equations (4)--(5) reduce
to `0=0`.

### Theorem 3 (sharp empty-scalar non-observability)

The complete direct moment family together with the complete nonempty
two-residual response family does not universally determine `h`.  This
failure persists inside honest characteristic-zero coloured block graphs.

Proof.  The two matchings on `{p,r,1,2}` have weights `lambda` and
`-lambda`, so they cancel.  Any other nonempty port set contains an isolated
port.  This proves (15)--(16) directly.  Replacing every displayed scalar
edge by a fixed rank-one colour block embeds the construction in the common
mixed-colour model.

This is stronger than a failure of the current root-budget selector: it
fixes every nonempty coefficient of the entire two-residual response.  It is
not a `P_7 -> Delta_3` realization; its purpose is to prove that no universal
response identity can reconstruct the vacuum coefficient on the
moment-null stratum.

## 5. What synchronized companion depths would add

Suppose the two one-residual singleton responses are legally exposed in the
same scalar chart:

```text
a_u=haf G[{p,u}],                 b_u=haf G[{r,u}].    (17)
```

For every pair `u,v`, physicality gives

```text
z_uv=h B_uv+a_u b_v+b_u a_v.                          (18)
```

### Proposition 4 (paired-companion recovery)

If the synchronized values in (17), `z_uv`, and one nonzero direct pair
`B_uv` are known, then

```text
h=(z_uv-a_u b_v-b_u a_v)/B_uv.                        (19)
```

Hence the empty scalar cannot vary while both singleton incidence rows, the
direct pair layer, and the two-residual pair layer remain fixed on a
nonzero-direct-edge chart.

The escape family (14) is sharp relative to this statement: its singleton
response `a_1=-lambda` changes with `lambda`.  Thus an exact paired companion
selector would close that family, whereas access to the two-residual
nonempty response alone cannot.

Eligibility is not observability.  Although a one-residual singleton lies
within the raw root-deletion budget, no existing `P_7` theorem synchronizes
both labelled singleton depths with the same four-fan/two-residual window
and its normalization.  Proposition 4 is therefore a precise conditional
target, not a completed P7 extraction.

## Scope wall

```text
empty direct moment m_empty=1:                         STRUCTURAL;
vacuum-free dual-Wick cross-window equations:          PROVED;
h recovery when some compatible m_4 or m_6 is nonzero: PROVED;
six-point defect inside q=2 P7 root budget:             PROVED;
physical forcing of opposite-pair additivity:           FALSE;
mixed-colour/cumulant forcing of additivity:             FALSE;
universal h recovery on the moment-null stratum:         FALSE;
h recovery from synchronized paired singleton depths:   PROVED;
legal four-fan window forcing in P7:                     UNKNOWN;
common selector normalization across depths:             UNKNOWN;
legal paired-singleton companion extraction in P7:       UNKNOWN;
GHZ-specific mixed-word forcing of additivity:            UNKNOWN;
partition-closed P7 response window:                     UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

## Replay

```powershell
uv run --with sympy python claims/p7/verify_p7_vacuum_free_dual_wick_projectivization_and_empty_scalar_escape.py
python claims/p7/audit_p7_vacuum_free_dual_wick_projectivization_and_empty_scalar_escape.py
python -m py_compile claims/p7/verify_p7_vacuum_free_dual_wick_projectivization_and_empty_scalar_escape.py claims/p7/audit_p7_vacuum_free_dual_wick_projectivization_and_empty_scalar_escape.py
uv run --with ruff ruff check claims/p7/verify_p7_vacuum_free_dual_wick_projectivization_and_empty_scalar_escape.py claims/p7/audit_p7_vacuum_free_dual_wick_projectivization_and_empty_scalar_escape.py
```

The primary replay checks the four-/six-point projectivization symbolically,
the arbitrary opposite-sum family, the square-zero escape, and paired
companion recovery.  The independent no-import audit uses rational hafnian
recurrences on one fixed six-port response and a separate two-term
square-zero multiplication.  Neither script searches graphs, supports,
colour words, selector systems, or parameter samples.
