# Maximum-root surplus-two zero-anchor probe exchange, overlap, and unique-nonrigid descent

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS59`.  Work in the complete promoted two-probe chart
of `GLS8`, with probe labels

```text
A={a_0,a_1}
```

and auxiliary labels

```text
Bhat=Q disjoint-union Uhat,       |Bhat|=2r,       r>=3.
```

Write

```text
J_n:V_n -> V_(a_0)^* direct-sum V_(a_1)^*,
J_n(k)=(W_(a_0,n)(-,k),W_(a_1,n)(-,k)),
K_n=ker J_n.                                             (1)
```

Assume the zero-anchor equation

```text
W_(a_0,a_1)=0.                                          (2)
```

The first result is arbitrary-root and pointwise.  If `0!=k in K_n`, then
for either old probe `a_sigma`, every probe vector `z`, and every colour

```text
c in supp(k) intersect supp(z),                         (3)
```

there is a label `t!=n` such that

```text
0!=W_(a_sigma,t)(z,-) in K e_(t,c)^*.                  (4)
```

For every `c in supp(K_n)`, finite irreducibility promotes (4) to a fixed
whole-domain pure probe block

```text
0!=W_(a_sigma,t_(sigma,c))(V_(a_sigma),-)
                         subset K e_(t_(sigma,c),c)^*.  (5)
```

The labels in (5) are distinct as `c` varies, and a descending linear-section
flag of length at most three retains every exceptional root-vector divisor.
No response, edge, rank minor, or coordinate is divided out.

At zero-anchor root order three, `GLS55`--`GLS56` give the exhaustive
source-structure branch in which there is a unique nonrigid label `n` and a
fully supported `k in K_n`.  The other five labels are rigid.  Equation (5)
then gives a three-colour pure star from each old probe into those five
labels.  The two three-label stars overlap.  At an overlap label `t`, either:

1. both probes use the same colour `c`, so `rank J_t=1` and
   `K_t=ker e_(t,c)^*`; or
2. the probes use distinct colours `c,d`, so `rank J_t=2` and
   `K_t=K e_(t,e)`, where `{c,d,e}={0,1,2}`.

Contracting `n` at `k` and this second deficient label `t` at a chosen
nonzero `ell in K_t` reconstructs one honest six-vertex graph.  In the first
case choose `ell` with both coordinates outside `c` nonzero; the descended
target is exactly binary.  In the second choose `ell=e_e`; the descended
target is exactly monocolour.  The accepted complete six-vertex theorem
requires at least three nonzero target colours and therefore excludes neither
endpoint.

Finally, the natural `GLD3` re-anchoring from `GLS56` is more rigidly blocked
than previously known.  At every fully supported old-probe contraction its
three pure-star pair responses cannot all be target-diagonal.  If they were,
`GLS56` would force the three old-probe shores to vanish, while (4) would
require three distinct nonzero pure neighbours among the two remaining
labels.  Thus this receiver fails its target-diagonal gate before activity or
nuisance survival can be invoked.

This is a support-free physical matching consequence and a complete
root-order-three unique-nonrigid structural reduction.  It is **not** a
promoted response, selector, complete-nuisance survivor, synchronized
receiver, branch contradiction, arbitrary-root source cover, strategic-node
closure, or global resolution.

## Dependencies and provenance

- `GLS8` owns the complete promoted two-probe matching identity and its exact
  physical companion/deck interpretation.
- `GLS55` supplies the zero-anchor `r=3` fact that at least five of the six
  auxiliary labels are torus-rigid.
- `GLS56` supplies the exhaustive all-rigid versus unique-nonrigid split and,
  in the latter branch, the simultaneous three-colour pure star from `n`.
  Its covector alternative is reproved below in the form needed here.
- `GLS58`, Theorem 6, records the same two-joint-kernel matching
  reconstruction on its all-rigid branch.  The matching proof below is
  repeated because its algebra does not require both contracted labels to be
  rigid; the new use has one nonrigid and one rigid deficient label.
- `GLD3` owns the conditional four-port diagonal-interference receiver.  Only
  its declared target-diagonal response gate is audited here; no downstream
  entry is claimed.
- The accepted complete six-vertex theorem in `claims/finite/n06` is used only
  to identify the exact three-colour threshold.  No mono/binary consequence
  is inferred from it.

No logical dependence is inferred from filenames.  The new content is the
old-probe exchange theorem, its fixed-block and exceptional-section
consequences, the two-star overlap classification, the unique-nonrigid
mono/binary descent, and the pointwise target-diagonal receiver no-go.

## 1. Covector alternative

Let `V=K^3` with its declared target basis.

### Lemma 1 (coordinate covector or surviving kernel coordinate)

For `ell in V^*` and a colour `c`, exactly one of the following holds:

```text
ell in K^* e_c^*;
there is v in ker ell with v_c!=0.                    (6)
```

### Proof

If `ell` is a nonzero multiple of `e_c^*`, every vector in its kernel has
zero `c`-coordinate.  Conversely, if no vector of `ker ell` has nonzero
`c`-coordinate, then

```text
ker ell subset ker e_c^*.
```

The zero covector cannot satisfy this containment.  Otherwise both kernels
are hyperplanes, hence equal, and `ell in K^*e_c^*`.  `square`

## 2. Pointwise probe exchange

The zero-anchor complete `GLS8` identity is

```text
T_W(-_A,-_Bhat)
 =sum_(D in binom(Bhat,2)) G_D^A tensor H_(Bhat-D),   (7)
```

and on a hypothetical witness its target is

```text
sum_(c=0)^2 e_(a_0,c)^* tensor e_(a_1,c)^*
                  tensor tensor_(u in Bhat)e_(u,c)^*. (8)
```

### Theorem 2 (pointwise old-probe pure-neighbour escape)

Fix `n in Bhat`, `0!=k in K_n`, one old probe `a_sigma`, a vector
`z in V_(a_sigma)`, and a colour satisfying (3).  Then some `t!=n` satisfies
(4).  For fixed `sigma,z`, neighbours supplied for distinct colours are
distinct.

### Proof

Suppose that no `t!=n` satisfies (4).  Put

```text
b_t=W_(a_sigma,t)(z,-).                              (9)
```

For each `t in Bhat-{n}`, Lemma 1 supplies `v_t in V_t` with

```text
b_t(v_t)=0,                 (v_t)_c!=0.              (10)
```

Contract (7) at `z` in probe slot `a_sigma`, at `k` in slot `n`, and at
`v_t` in every auxiliary slot `t!=n`, leaving the other probe open.

Every perfect matching pairs `a_sigma` with exactly one vertex.  If it is the
other old probe, (2) kills the matching.  If it is `n`, `k in K_n` kills the
edge.  If it is another auxiliary label `t`, (10) kills the edge.  Hence the
entire evaluated source is zero.

The coefficient of `e_(a_(1-sigma),c)^*` on (8) is

```text
z_c k_c product_(t in Bhat-{n})(v_t)_c,              (11)
```

which is nonzero.  This contradiction proves (4).  One nonzero covector
cannot lie on two coordinate axes, proving distinctness.  `square`

The proof partitions all complete physical matchings by the partner of the
chosen old probe.  It does not inspect supports of individual decks or
discard any labelled nuisance term.

## 3. Fixed blocks and exceptional sections

For `t!=n`, a probe `a_sigma`, and colour `c`, put

```text
P_(sigma,t,c)={z in V_(a_sigma):
 W_(a_sigma,t)(z,-) belongs to K e_(t,c)^*}.          (12)
```

Let

```text
S_n={c:e_(n,c)^*|_(K_n) is not zero}.                (13)
```

### Theorem 3 (fixed whole-domain pure probe blocks)

For every probe `a_sigma` and `c in S_n`, some fixed label `t_(sigma,c)!=n`
satisfies (5).  For a fixed probe these labels are distinct.  There is one
fully supported probe vector `z` that activates all three blocks whenever
`S_n={0,1,2}`.

### Proof

Choose `k in K_n` with `k_c!=0`; such vectors form a nonempty open in the
linear space `K_n`.  Theorem 2 gives the pointwise cover

```text
V_(a_sigma) cap D(z_c)
 subset union_(t!=n)
 {z in P_(sigma,t,c):W_(a_sigma,t)(z,-)!=0}.          (14)
```

Discard every empty set on the right.  Each remaining set is contained in
the displayed linear subspace `P_(sigma,t,c)`.  A nonempty open subset of an
irreducible vector space cannot be covered by finitely many proper linear
subspaces.  Hence one `P_(sigma,t,c)` is the whole probe space.  Because its
original set was not discarded, the corresponding restricted map is
nonzero.  This proves (5).

Distinctness again follows from the zero intersection of two coordinate
lines.  When all three colours occur, write the fixed maps as

```text
W_(a_sigma,t_(sigma,c))(z,-)=mu_c(z)e_(t_(sigma,c),c)^*.
```

The three nonzero linear forms `mu_c` and the three coordinate forms have
proper kernels.  Their finite union cannot cover the probe space over the
infinite field `K`, giving one fully supported simultaneous activation.
`square`

The empty-set deletion in this proof is load-bearing: no closure of an empty
locally closed pure-nonzero set is treated as a whole linear subspace.

### Theorem 3.1 (complete root-vector exceptional-section flag)

Fix `sigma,c` with `c in S_n`.  There are subspaces and labels

```text
V_(a_sigma)=L_0 strictly contains L_1 strictly contains ... strictly contains L_s,
t_0,...,t_(s-1),                    s<=3,             (15)
```

such that `L_s cap D(z_c)` is empty and, on every stratum

```text
(L_i cap D(z_c))-L_(i+1),                            (16)
```

the fixed block to `t_i` is nonzero and pure in colour `c`.

### Proof

Apply the proof of Theorem 3 on `L_i` whenever `L_i cap D(z_c)` is nonempty.
It supplies a nonzero pure restricted block

```text
W_(a_sigma,t_i)(z,-)=mu_i(z)e_(t_i,c)^* on L_i.
```

Set `L_(i+1)=L_i cap ker mu_i`.  Dimension drops strictly, so the process
stops after at most three steps.  The resulting strata give (16).  `square`

This flag includes zero coordinates, zero selected blocks, rank drops, and
all other divisor fibres without selecting a denominator.

## 4. The root-order-three overlap

Assume now `r=3` and take the unique-nonrigid branch of `GLS56`.  Thus
`|Bhat|=6`, one label `n` has a fully supported `k in K_n`, and all five
labels of `Bhat-{n}` are rigid.

For each probe, Theorem 3 gives an injection

```text
tau_sigma:{0,1,2} -> Bhat-{n}                        (17)
```

such that the entire probe block to `tau_sigma(c)` has nonzero image in the
`c`-axis.

### Theorem 4 (five-label overlap and second deficient label)

The images of `tau_0` and `tau_1` intersect.  For any overlap label

```text
t=tau_0(c)=tau_1(d),                                 (18)
```

exactly one of the following holds:

1. `c=d`, `row J_t=K e_(t,c)^*`, `rank J_t=1`, and
   `K_t=ker e_(t,c)^*`;
2. `c!=d`, `row J_t=K e_(t,c)^*+K e_(t,d)^*`,
   `rank J_t=2`, and `K_t=K e_(t,e)`, where
   `{c,d,e}={0,1,2}`.

### Proof

Two three-element subsets of a five-element set intersect.  At an overlap,
the `a_0` block has nonzero row space exactly `K e_c^*`, while the `a_1`
block has nonzero row space exactly `K e_d^*`.  Their sum is the joint row
space.  Equal axes give case 1; distinct axes give case 2.  `square`

The label `t` is rigid in both cases, but deficient.  Thus the
unique-nonrigid source branch always contains at least two labels with
nonzero joint kernel: the fully supported kernel at `n` and a coordinate
boundary kernel at `t`.

## 5. Honest mono/binary six-vertex descent

Let

```text
P=Bhat-{n,t},                 |P|=4.                 (19)
```

Choose

```text
ell in K_t-{0}                                       (20)
```

with both non-`c` coordinates nonzero in Theorem 4 case 1, and choose
`ell=e_e` in case 2.  For `u in P`, put

```text
h=W_(n,t)(k,ell),
a_u=W_(n,u)(k,-),
b_u=W_(t,u)(ell,-),                                 (21)
```

and for distinct `u,v in P` put

```text
D_uv=hW_uv+a_u tensor b_v+b_u tensor a_v.            (22)
```

### Theorem 5 (unique-nonrigid mono/binary reconstruction)

Let `B'` be the graph on the six open vertices `A disjoint-union P` with

```text
B'_(a_0,a_1)=0,
B'_(a_0,u)=W_(a_0,u),
B'_(a_1,u)=W_(a_1,u),
B'_(u,v)=D_uv.                                       (23)
```

Then

```text
T_W(k at n,ell at t,-_(A disjoint-union P))=T_(B').  (24)
```

On a hypothetical witness its target is

```text
sum_(j=0)^2 k_j ell_j
       tensor_(v in A disjoint-union P)e_(v,j)^*.    (25)
```

In Theorem 4 case 1, (25) has exactly two nonzero colours.  In case 2 it has
exactly one nonzero colour.

### Proof

Insert `k,ell` in the original eight-vertex matching tensor.  Matchings using
`n--t` give the `hW_uv` branch of the unique `P--P` edge in (23).  Otherwise
`n,t` meet two distinct vertices `u,v in P`; the two orientations give
`a_u tensor b_v` and `b_u tensor a_v`.  Matchings sending either `n` or `t`
to an old probe vanish because both vectors lie in their joint kernels.
The zero root edge removes matchings using `a_0--a_1`.

Conversely, expanding the unique `P--P` edge of every nonzero matching of
`B'` through (22) reconstructs exactly these original matchings.  This proves
(24), including the divisor `h=0`.  Contracting the target gives (25).

The vector `k` is fully supported.  In case 1, `ell_c=0` and its other two
coordinates were chosen nonzero, so (25) is binary.  In case 2, only
`ell_e` is nonzero, so (25) is monocolour.  `square`

The complete six-vertex theorem used elsewhere in the repository excludes
targets with at least three nonzero colours.  It has no binary or monocolour
conclusion, so Theorem 5 is a legal reduction but not a contradiction.

## 6. Natural old-probe receiver is never target-diagonal

Use the simultaneous pure-star point supplied by `GLS56` and write its three
neighbours as `s_0,s_1,s_2`, with

```text
W_(n,s_i)(k,-)=lambda_i e_(s_i,i)^*,       lambda_i!=0. (26)
```

For either old probe and a fully supported vector `z`, put

```text
b_i=W_(a_sigma,s_i)(z,-),
D_ij=lambda_i e_i^* tensor b_j
              +b_i tensor lambda_j e_j^*.            (27)
```

### Theorem 6 (target-diagonal pure-star triangle exclusion)

The three tensors `D_01,D_02,D_12` cannot all be target-diagonal.

### Proof

`GLS56`, Theorem 5, proves that simultaneous target diagonality in (27)
forces

```text
b_0=b_1=b_2=0.                                      (28)
```

Apply Theorem 2 to the same fully supported `z`.  It requires three distinct
labels in `Bhat-{n}` carrying nonzero pure probe shores in the three colours.
None of `s_0,s_1,s_2` can serve because of (28).  Only two of the five labels
remain, which cannot carry three distinct shores.  Contradiction.  `square`

Thus the natural `GLD3` re-anchor does not land on a diagonal-but-inactive
cell: at every root-torus point it already violates the simultaneous
target-diagonal response gate.  This does not manufacture another receiver.

## 7. Exact endpoint controls

The following rational full eight-vertex controls verify the local
incidence, overlap, and contraction boundaries.  They are not complete
eight-vertex witnesses.

Use vertices `a_0,a_1,n,t,p_0,p_1,p_2,p_3` in that order, put
`E_ij=e_i^* tensor e_j^*` in the displayed edge orientation, and set every
undeclared block to zero.

### 7.1 Same-colour overlap and binary descent

Take

```text
k=(1,1,1),             ell=(0,1,1),

W_(a_0,t)=E_00,         W_(a_1,t)=E_00,
W_(a_0,p_0)=E_11,       W_(a_1,p_1)=E_11,
W_(a_1,p_2)=E_22,       W_(a_0,p_3)=E_22,

W_(n,t)=E_00,           W_(n,p_0)=E_02,
W_(n,p_2)=E_01,
W_(t,p_1)=E_12,         W_(t,p_3)=E_11.              (29)
```

Then `J_n=0`; `J_t` has rank one with kernel `e_0^perp`; every other label
has a rank-one coordinate row and is rigid.  Both old probes have complete
three-colour pure stars overlapping at `t` in colour zero, and `n` has the
pure star `t,p_2,p_0` in colours `0,1,2`.  Double contraction at `k,ell`
gives exactly the two constant six-vertex words of colours one and two, both
with coefficient one.

### 7.2 Cross-colour overlap and monocolour descent

Take

```text
k=(1,1,1),             ell=e_2,

W_(a_0,t)=E_00,         W_(a_1,t)=E_11,
W_(a_0,p_0)=E_11,       W_(a_0,p_1)=E_22,
W_(a_1,p_2)=E_00,       W_(a_1,p_3)=E_22,

W_(n,t)=E_00,           W_(n,p_0)=E_02,
W_(n,p_2)=E_01,
W_(t,p_2)=E_22.                                      (30)
```

Now `J_t` has rank two with kernel `Ke_2`; all other auxiliary labels except
`n` are again coordinate-rigid.  The two probe stars overlap at `t` in
different colours, while `n` has a three-colour pure star.  Double
contraction gives exactly the constant colour-two word, with coefficient
one.

The focused verifier checks all `3^6=729` open coefficients of each full
eight-to-six contraction.  These controls show that the exact local
interfaces and the binary/mono endpoints are algebraically compatible.  As
off-target full graphs, they do not prove that either endpoint occurs on the
complete original witness locus.

## 8. Exact frontier and non-closure boundary

```text
arbitrary-r old-probe pointwise pure-neighbour escape:    PROVED;
fixed whole-domain pure probe blocks:                     PROVED;
complete root-vector exceptional-section flags:           PROVED;
r=3 unique-nonrigid two-probe star overlap:                PROVED;
second rigid deficient label, rank one or two:             PROVED;
honest binary/mono six-vertex descent:                     PROVED;
binary/mono exclusion by accepted n=6 theorem:             FALSE;
natural old-probe GLD3 target-diagonal triangle:           IMPOSSIBLE;
promoted physical response:                               OPEN;
constant selector and complete nuisance survival:         OPEN;
synchronization, activity, and target-pure anchor:         OPEN;
all-rigid GLS57/GLS58 successor:                           OPEN;
arbitrary-r rigidity of the forced probe neighbours:       OPEN;
nonzero-anchor source branch:                              OPEN;
maximum-root strategic-node closure:                      OPEN;
global Krenn--Gu conjecture:                               UNRESOLVED.
```

The smallest unique-nonrigid successor is to couple the binary/mono
six-vertex descents across **all** overlap labels and kernel choices using the
remaining complete mixed coefficients, or to transport one forced pure
probe block into a named promoted target quotient with response and complete
nuisance survival.  Reapplying the three-colour finite theorem, using one
overlap only, or treating a pure incidence block as a selector cannot close
the branch.

## Verification

Run from repository root:

```text
python claims/arbitrary-order/verify_maximal_root_surplus_two_zero_anchor_probe_exchange_overlap_and_unique_nonrigid_descent.py
python -I claims/arbitrary-order/audit_maximal_root_surplus_two_zero_anchor_probe_exchange_overlap_and_unique_nonrigid_descent.py
```

The primary verifier uses exact rational matrix tensors, a direct
`105=15+15+75` matching partition, all `60^2=3600` ordered probe-star pairs,
and dense coefficient checks of both full controls.  The independent audit
imports neither the primary nor project code; it uses an `F_5` covector
census, bit-mask matchings, finite injection tables, custom modular row
reduction, and a separately written sparse-cell reconstruction.  The written
proof, not either finite replay, carries the characteristic-zero theorem and
its irreducibility arguments.
