# Independent review of degree-two transport and the local boundary

Date: 2026-09-22. Verdict: **PASS for the stated identities and controls**.
The general degree-two exclusion and global conjecture remain unresolved.

The owning claim is
`claims/arbitrary-order/DEGREE_TWO_SOURCE_TRANSPORT_AND_LOCAL_BOUNDARY.md`.
The independent review separates the general singleton identity from the
stronger color-regular hypothesis used for C8 transport. It does not infer
color regularity from a degree bound.

## 1. Singleton and transport sectors

A singleton word with A colored a and all exterior vertices c has zero,
two or four cut crossings. Exterior c-c crossings vanish. Two deleted
exterior vertices must be one protected M_c edge; four must be two distinct
such edges. The four-crossing sum is over unordered resource pairs, so
every physical matching is counted once. No exterior cofactor is free.

In a color-regular C8 row, the pullback of the two target M_c resources
cannot be M_a by the C8 assumption. If it were M_c, two a-minority vertices
on an M_c(A) edge would force a unique nonzero matching. Thus it is the
third matching M_b.

For complementary M_b edges R,R', the word a on R, b on R', c outside A
forces both a-c lanes. The remaining b pair either uses its protected
edge or its two b-c lanes. The latter completion exists precisely when
their image is one M_c resource distinct from the consumed a-c resource.
Equal-resource collisions, one-endpoint overlap and malformed two-resource
images cannot complete; the uniform exterior has no repair crossing.
Thus the actual coefficient is x or x(1+y), with x nonzero. Source
vanishing forces y=-1 and the resource condition, for both R.

This argument applies when the C8 target resources lie in one component
or in two. `audit_c8_to_split_transport.py` independently enumerates
6,720 target-collision cases and four empty-q1 cases with distinct actual
integer lane weights. It does not import the primary construction.

## 2. The complete local tensor

Use the owner's E_i, P_i, Q_i notation. The transport gives
Q_0!=P_1, Q_1!=P_0, y_0=y_1=-1 and x_0x_1=-1. When Q_i=P_i, aligned
endpoint maps give a unique 3a/1b four-crossing term. A possible protected
a-edge leaves incompatible exterior resources, so it cannot cancel that
term. Hence the maps must be swapped.

Every c port in A must use its protected edge. If precisely one M_c edge
is c, the two remaining foreground ports hit distinct exterior resources,
so there is no matching. Other nonempty c sets are incompatible except
cccc, whose protected matching has weight one. Among a/b words, a mixed
E_i cannot complete an exterior resource and its b port cannot protect.
The remaining four assignments have coefficients

```text
1+x_0x_1,  (1+y_0)(1+y_1),  x_0(1+y_1),  x_1(1+y_0),
```

all zero. This proves the entire 81-word tensor in the same actual array.
The independent symbolic checker verifies the Laurent identity after
x_0=t, x_1=-t^-1, y_0=y_1=-1; it does not substitute a numerical t.

The owner's k=2 whole-array extension has 24 crossings and one crossing to
each foreign color at all states. Exact physical enumeration confirms the
81-word slice and 600 failures elsewhere, including 0000|0011 with
coefficient one. A separately implemented k=3 extension puts P and Q
resources in different exterior components and recovers the same tensor
by matching recursion. These are genuine whole arrays but are not full
sources. They refute contradiction from further words in that same slice.

## 3. Macro controls and scope

The separate four-crossing macro control passes all nine macro targets
using 1-1 cancellation, with no two-crossing terms. Its mixed unique word
0000|0011 has coefficient -1. The 13-entry control passes all macros while
its added entry changes a nonmacro coefficient to 2. Cut parity and the
explicit incompatible complements prove macro invisibility; physical
enumeration checks the unique nonmacro matching. Neither control proves
that the full source is feasible at degree two.

The next supplier must use two nonuniform components, change the exterior
background, or impose global consistency. The theorem does not cover a
(2,0) crossing-color distribution. The earlier draft's shared-target
special case required both foreground layers to be C8; that weaker
argument is not used in this owning proof. In particular, the valid
C8-plus-split control is not excluded by that omitted special case.

## 4. Provenance and verification limits

The independent transport report was frozen at SHA-256
`E0F34B92E629D54B8AFDCF942CDC327FEF2D3898F1DB08161BEC7133DDECBCB3`;
the independent local-tensor report at
`C2A974A460A96AA4480ED3D1DE0883AAFD828A81DF9E02801C1BC79EB5B07883`.
The complete mathematical derivations and portable checks are present in
the tracked package; scratch files are not proof dependencies.

The separate agents worked in the same research session. This is not
independent human refereeing or Lean verification. The finite scripts
corroborate the displayed identities and exact countercontrols; they do
not establish an exhaustive cover of arbitrary degree-two sources.


## 5. Reciprocal all-background control

An independent reconstruction uses a symmetric colored-state edge table
and recursive coefficient evaluation, rather than the primary physical
matching list. It verifies the common permutation P=(0,2,3,1), all six
ordered layer maps, transpose consistency, 12 protected and 24 crossing
entries, and crossing degree two with one neighbor of each foreign color
at every state. The C8 and split layer types hold in both directions.

All 486 one-component/uniform-background specifications hold; these are
477 distinct words because some constant words are counted more than once.
All nine macro targets hold. Full enumeration nevertheless gives 195
incorrect source coefficients, including 171 with min-q at most one.
The first is 0001|0022, coefficient -1, with its unique matching
(01)(27)(36)(45) and factors (1,1,-1,1). This is a local-row insufficiency
control, not a full source or a counterexample to degree-two exclusion.

The separate-agent report was frozen at SHA-256
E59BA94B710E210A4746F208A944CFEE8BDB40A8E1B4AA483FE77FB4815CBC21.
The independent implementation is audit_reciprocal_c8_boundary.py.


## 6. All-order q1 escape

The one-component C8 repair theorem was independently checked at scratch
owner hash 74F5D448A1BD6CBE71411623B9B983741B00AE942D806F83C736E89B1DF65B48.
Its mixed physical word has u-x forced. The remaining b state v either
uses its direct c target y or its unique b-a lane. In the second case y
must return to w=v+b in A, stranding w+a. Hollowness places the b-a
endpoint outside A, so arbitrary additional all-a components cannot repair
the stranded port. Therefore the direct nonzero term is unique at every k.

The independent physical matcher exhausts 384 supports (four affine lifts,
four oriented M_a edges, 24 arbitrary b-a maps). Every case has exactly
one matching; the alternative lane is locally compatible in 192 cases and
never completes. This corroborates the all-order sector proof. The exact
conclusion is escape of at least one split resource from B, not exclusion
of spanning C8s, separated target resources, or automatic iteration.

The audit report was frozen at SHA-256
F1443ACF510238F1F484759C7870378A13D5632D801F57C502142F394CDD53E5.
The portable independent implementation is audit_c8_q1_escape.py.


## 7. Partial-resource local normalization barrier

An independently reconstructed three-component array has 18 protected and
36 crossing entries, with one crossing to each foreign color at every
state and all crossings hollow. Each foreground layer on A has one
product -1 protected-resource pair and two targets which do not form a
resource. All 81 words on A with B,C uniformly2 have the exact delta
tensor: only0000 and1111 have cancelling terms(+1,-1), and2222 has its
protected term1. Port3 always targets C0 while C3 never appears, excluding
every four-crossing sector. The global macro0000|1111|2222 has exactly
three unit terms and coefficient3. The control is not a macro or full source.

The independent word-specific recursion confirms that complete local rows
do not force the exhaustive alternative 'complete split or C8.' The
general color-regular parent still needs a global argument for partial
resources. The frozen author report hash was
6C6D2963A5621F9AA3DC5CCB10BF0AA53CA1F0737A6BB44C81EA967575F62252;
the independent report hash was
F35A42E0A65D15709A08BD02F3657127A6021C3879BB12C8E72C96993DE3F0DF.
The independent implementation is audit_partial_resource_boundary.py.


## 8. Reciprocal fixed-component partial-resource control

I independently reconstructed the four-component array from the three
displayed physical permutations rather than importing the primary builder.
Each permutation is hollow and bijective. The resulting array has 24
protected entries and 48 crossing entries; every physical vertex/color state
has exactly one crossing neighbor in each foreign color. The reverse
incidences at `A` are the actual inverse shores of the same three layers.

For each background `c`, the linear port conjugation sends the two foreground
incidences to

```text
(B0,B3,B1,C0),       (B1,B0,B2,C0).
```

In each of the six ordered incidences, exactly one source protected edge maps
to a background resource with product `-1`, while the complementary source
edge maps to targets in two different components. These are genuine partial
resources with orphan targets, not incomplete data later filled differently
for another word.

The independent word-specific recursion checks all 243 words arbitrary on
`A` and uniform outside. For each background, the background-uniform word has
one protected term, the other two uniform words have weights `(-1,1)`, and
all 78 mixed words have no terms. The outside word
`0000|1200|0000|0000` has exactly one matching of weight one. Thus the array
is an exact local-tensor control and explicitly not a full source. The
displayed failure is nonmacro, so it does not verify macro failure; no
macro-source status is asserted.

The frozen author report hash was
`76047E8ED290F8CC384F0F2D4492275D3B8CE8CA8DC7D6FFBF0FCEFFBE952982`;
the separate-agent review report hash was
`700AD2AC6089306B10229B657CF1227059873F563E650A88F4215D46387DA134`.
The portable implementations are
`verify_partial_orphan_reciprocal_boundary.py` and
`audit_partial_orphan_reciprocal_boundary.py`. Their promoted file hashes are
respectively
`8CD9270BB22BD258F1ED563E5C8088EA5955293AF31E69891AE2C4FEE64331CE`
and
`3EE260163600F518DD273FA7D23F67B2391D466189E64E3E31CE3CD5314B3EE7`.


## 9. Same-component orphan transport

I separately audited the all-order coupled implication. The color-pair layer
is bijective, so two orphan targets in one component are distinct ports. The
orphan premise excludes their background matching. If they instead form the
source-color matching, coloring only those two vertices by the background
forces their two return lanes and every protected complement. This gives one
nonzero matching and a forbidden q1 word. The targets must therefore form the
third-color protected edge.

For the coupled word, the two background-colored orphan targets force their
return lanes to the source resource, with nonzero product `h`. The
complementary third-color pair either protects or uses both of its exits to
the source color. A one-exit sector cannot complete. After both exits, every
remaining vertex has the source color, so a completion exists exactly when
the two distinct targets form one protected source-color resource different
from the already consumed source resource. Targeting that consumed resource
or overlapping it gives a physical collision. The additional sector is
unique, so the literal coefficient is `h` or `h(1+g)`. Source vanishing and
`h!=0` force the distinct target resource and `g=-1`.

Extra all-source-color components use their unique protected matching. This
proves the implication for arbitrary `k>=2` and arbitrary nonzero complex
crossing weights. The proof does not apply when the two orphan targets lie in
different components; that propagation branch remains open.

My symbolic physical matcher exhausts every ordered exit placement for
`k=2,3,4`. It records only monomial `h0*h1` in the direct sector and adds
`h0*h1*g0*g1` exactly for a distinct protected target resource. The primary
three-component replay independently checks all 56 normalized ordered
placements.

The frozen theorem report hash was
`50DDB7F483D1F50CAD15BA4CCBF840C9465D63526D8467C4E9A1202C0ADB5B69`;
the separate-agent review report hash was
`F52330E58DF3A053A5755BEB612E236E2338A625C1C5416792608067E1FC9C93`.
The portable implementations are
`verify_partial_orphan_coupled_transport.py` and
`audit_partial_orphan_coupled_transport.py`, with promoted hashes
`568E499ABF3571725D58BBFAE9FCA8289F5759A5BE60F01ADB9AF2DA3933EA56`
and
`78838F42CAF6A4B63C2A343D518FD8E7D940582B4B1A642C1B492E6625242471`.

These additions sharpen the source-transport map but do not exclude the
repaired same-component branch, establish an exhaustive color-regular cover,
prove a general degree-two exclusion, or resolve the global conjecture.
