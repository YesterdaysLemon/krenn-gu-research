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
