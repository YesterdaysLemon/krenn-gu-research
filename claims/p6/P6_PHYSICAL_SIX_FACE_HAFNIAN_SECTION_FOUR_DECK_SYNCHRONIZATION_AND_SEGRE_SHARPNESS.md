# P6 physical six-face hafnian section, four-deck synchronization, and Segre sharpness

## Status

**Exact characteristic-zero common-graph reconstruction and sharp scalar
no-go theorem.**  Let an eight-vertex nonroot graph be split into a
four-vertex core `C` and a four-window `W`.  Its six principal two-deletion
faces which delete two vertices of `W` are equivalently the six hafnians

```text
y_pq=haf A[C union {p,q}],                 {p,q} subset W.       (1)
```

These six values are not constrained by scalar principal-hafnian
integrability.  The face morphism from one common eight-vertex graph to
`K^6` is split surjective.  An exact affine section is obtained by setting

```text
a_uv=1                         u,v in C,
a_up=tau                       u in C, p in W,
a_pq=(y_pq-12 tau^2)/3         p,q in W.              (2)
```

The core four-hafnian is the nonzero four-deletion companion `3`, and direct
matching expansion gives every face in (1).  More strongly, all seventy
principal four-hafnian companions of the same graph have closed formulas
below, and all thirty-six partner-expansion stresses coupling the six faces
to that four-deck hold identically.  Thus the construction synchronizes the
faces and complete four-deletion deck on one physical graph; it is not six
unrelated face assignments.

If the desired face vector lies in `(K^*)^6`, `tau` can be chosen nonzero so
that every one of the twenty-eight graph edges in (2) is nonzero.  Combining
this section with the preceding pulled-back Segre theorem proves:

```text
for every invertible clean 2 x 3 fan O,
the full-edge-torus scalar hafnian face locus meets
O^(-1) Seg(P^1 x P^2).                                (3)
```

Consequently no scalar integrability polynomial involving only the six
faces can obstruct the GHZ/Segre equations.  Nor does requiring the
four-deletion companions to come from the same graph obstruct existence when
those companions are allowed to take their induced values.

This is a sharp boundary, not a P6 construction.  A target-clean P6 witness
requires six **tensor-valued** faces to be diagonal simultaneously.  Three
scalar sections can be placed on the diagonal entries of one family of
bilinear edge blocks, but mixed-colour matching coefficients generally
survive.  An explicit mixed word below is nonzero.  Furthermore, if the GHZ
equations independently prescribe the depth-four companion tensor rather
than allowing the induced deck below, its incidence with this section is not
decided.

Thus scalar common-graph integrability and coordinate-torus conditions are
eliminated as possible P6 no-go mechanisms.  Mixed-colour cancellation,
target-clean nuisance separation, and independently fixed depth-four target
incidence remain **UNKNOWN**.  No physical `P_6 -> Delta_3` restriction,
Krenn--Gu counterexample, or global proof is claimed.  Global Krenn--Gu
remains **UNRESOLVED**.

No graph, support, colour word, matching family, parameter grid, numerical
point, or finite field is searched.  The proof is a symbolic section of the
face morphism; the replays expand only its fixed eight-vertex identities.

## 1. The general two-port face formula

Let `K` be a characteristic-zero field.  More generally, let `C` be any
even core, let

```text
h=haf A[C],
D_C[u,v]=haf A[C minus {u,v}]       for u!=v,
D_C[u,u]=0,                                           (4)
```

and attach two new ports `p,q`.  Let `x_p,x_q` be their incidence columns to
`C`, and let `a_pq` be their mutual edge.

### Proposition 1 (bordered-hafnian two-port formula)

```text
haf A[C union {p,q}]
 =h a_pq+x_p^T D_C x_q.                              (5)
```

### Proof

Partition perfect matchings according to the partner of `p`.  If `p` is
matched to `q`, the remaining core contributes `h`.  Otherwise `p` and `q`
match two distinct core vertices `u,v`, in either assignment, and the
remaining core contributes `haf A[C minus {u,v}]`.  Summing these terms is
exactly (5).

For four ports `W`, equation (5) holds simultaneously for all six pairs with
the same `h,D_C`, and the same four incidence columns.  If `h!=0`, it gives
the reconstruction

```text
a_pq=(y_pq-x_p^T D_C x_q)/h.                         (6)
```

Thus, relative to any fixed nonzero-hafnian core and any fixed port
incidences, the six face values independently reconstruct the six window
edges.  This is an actual graph reconstruction, not a formal response
ledger.

## 2. A split section on eight vertices

Now take

```text
C={0,1,2,3},                 W={4,5,6,7}.              (7)
```

Put weight one on every core edge and weight `tau` on every core--window
edge.  The core has three perfect matchings, so

```text
h=3.                                                   (8)
```

Its cofactor matrix `D_C` is the hollow all-one matrix.  Hence for any two
window vertices

```text
x_p^T D_C x_q=12 tau^2.                               (9)
```

Define the six window edges by (2).

### Theorem 2 (split-surjective six-face morphism)

For every `y=(y_pq) in K^6` and every `tau in K`, the graph (2) satisfies

```text
haf A[C union {p,q}]=y_pq             for all p<q in W. (10)
```

Consequently the morphism from hollow symmetric eight-by-eight matrices to
these six principal six-hafnians has the affine section (2).  In particular,
its image is all of `K^6`, not merely a dense open subset.

### Proof

Equations (5), (8), and (9) give

```text
haf A[C union {p,q}]
 =3 (y_pq-12 tau^2)/3+12 tau^2
 =y_pq.
```

This proves both the identity and the section claim.

### Corollary 3 (full-edge-torus section)

If every `y_pq` is nonzero, there exists `tau in K^*` for which every edge
in (2) is nonzero.

### Proof

The core edges are one and the cross edges are `tau`.  A window edge
vanishes only when

```text
y_pq=12 tau^2.                                        (11)
```

The six equations (11), together with `tau=0`, exclude only finitely many
field elements.  A characteristic-zero field is infinite, so another
`tau` exists.

## 3. The complete synchronized four-deletion deck

For each four-set `R subset C union W`, let

```text
g_R=haf A[R].                                         (12)
```

These are exactly the seventy four-deletion companions, labelled by their
remaining four-set.  Put

```text
b_pq=(y_pq-12 tau^2)/3.                               (13)
```

### Theorem 4 (closed complete four-deck)

The induced four-deck of the section (2) is

```text
|R intersect W|=0:
  g_R=3;

|R intersect W|=1:
  g_R=3 tau;

|R intersect W|=2,  R intersect W={p,q}:
  g_R=b_pq+2 tau^2=(y_pq-6 tau^2)/3;

|R intersect W|=3,  R intersect W={p,q,r}:
  g_R=tau(b_pq+b_pr+b_qr)
     =tau(y_pq+y_pr+y_qr-36 tau^2)/3;

|R intersect W|=4:
  g_R=b_45 b_67+b_46 b_57+b_47 b_56.                 (14)
```

### Proof

There are three matching types on four vertices.  With zero window vertices
all three products are one.  With one window vertex, its partner is one of
three core vertices, giving `3 tau`.  With two window vertices, one matching
uses their window edge and the other two use two cross edges.  With three
window vertices, the unique core vertex chooses one of them and the other
two use their window edge.  With four window vertices, the three window
matchings give the last line.  These cases prove all seventy labels at once.

The six faces and these companions obey the exact nested stresses.  If
`T=W minus {p,q}` is the deleted window pair and `v in C union {p,q}`, then

```text
y_pq
 =sum_(s in (C union {p,q}) minus {v})
    a_vs g_((C union {p,q}) minus {v,s}).             (15)
```

Equation (15) is partner expansion of the same six-vertex hafnian along
`v`.  There are six choices of `v` for each of six faces, giving thirty-six
simultaneous face/four-deck equations.  They are not additional assumptions:
the section and (14) satisfy all of them identically.

For an arbitrary proposed synchronized deck, (15) is a necessary physical
integrability test.  The section proves that it has solutions for every face
vector when the four-deck is allowed to be the induced deck (14).  A
separately fixed target four-deck can still fail these stresses.

## 4. Exact intersection with every Segre fan chart

Let `O in GL_6(K)` be any clean `2 x 3` permanental fan observation matrix,
with the deletion/surviving-pair complement permutation absorbed into `O`.
The preceding selector theorem identifies one target-colour slice with

```text
y=O^(-1) vec(r s^T).                                  (16)
```

### Theorem 5 (physical Segre-intersection sharpness)

For every invertible `O`:

1. the scalar physical six-face locus contains the whole pulled-back Segre
   cone in (16);
2. it contains a point of that cone with all six face coordinates nonzero;
3. that point is realized by a common eight-vertex graph with all
   twenty-eight edge weights nonzero and with the complete synchronized
   four-deck (14).

### Proof

Theorem 2 realizes every vector in `K^6`, hence every vector (16).  The
no-coordinate-boundary theorem for an invertible fan supplies factors `r,s`
for which all six entries of (16) are nonzero.  Corollary 3 then chooses
`tau` so that the realizing graph is on the full edge torus.  Theorem 4
supplies its complete physical four-deck.

Therefore the three pulled-back Segre quadrics are genuine target equations,
but they are transverse to no scalar hafnian face obstruction: the physical
face morphism has a section through them.

## 5. Three pure colours synchronize, but mixed words survive

Use the three all-nonzero face columns from the preceding clean-selector
certificate, in pair order `45,46,47,56,57,67`:

```text
y^(0)=(14,-24,20,15,-29,9),
y^(1)=(10,-33,36,30,-58,18),
y^(2)=(2,38,-45,-30,73,-23).                         (17)
```

At `tau=1`, formula (2) gives the window-edge table

```text
             colour 0   colour 1   colour 2
45               2/3        -2/3       -10/3
46               -12         -15        26/3
47               8/3           8         -19
56                 1           6         -14
57             -41/3       -70/3        61/3
67                -1           2       -35/3.         (18)
```

Every entry is nonzero.  For each graph edge `uv`, put the three scalar
weights into one diagonal bilinear block

```text
B_uv=diag(a_uv^(0),a_uv^(1),a_uv^(2)).                (19)
```

Core and cross blocks are the identity.  Every block in (19) is invertible,
and its three pure-colour evaluations reproduce all eighteen face values
(17) on one block graph.

This still is not target-clean.  On the face with remaining vertices
`C union {4,5}`, assign colours

```text
0,1 -> colour 0;       2,3 -> colour 1;
4,5 -> colour 2.                                        (20)
```

Because the blocks are diagonal, the unique surviving matching pairs these
three same-colour pairs.  Its coefficient is

```text
B_01[0,0] B_23[1,1] B_45[2,2]
 =1*1*(-10/3)=-10/3 !=0.                              (21)
```

Thus a forbidden mixed target word survives exactly.  The construction
proves that pure-colour scalar synchronization and full block-edge rank are
not enough; mixed-colour cancellation is the remaining tensorial content.

## 6. Translation and next exact intersection

Equation (5) is the bordered-hafnian version of a Schur/Gram completion:
the core cofactor matrix is the middle form, the cross incidences are port
vectors, and the direct port edge is the freely reconstructible scalar when
`h!=0`.  Algebraically, Theorem 2 exhibits a section of the six-face moment
morphism.  A morphism with a section has no nonzero universal polynomial
relation on its target coordinates.

The complete deck is a finite bosonic moment tower, and (15) is its Wick
partner recursion.  For the surrounding language see Hamilton et al.,
[*Gaussian Boson Sampling*](https://arxiv.org/abs/1612.01199), and Amendola,
Faugere, and Sturmfels,
[*Moment Varieties of Gaussian Mixtures*](https://arxiv.org/abs/1510.04654).
The section (2), the closed deck (14), and its Segre composition are the
problem-specific results here.

The surviving P6 problem is therefore not scalar hafnian integrability.  It
is the tensor incidence

```text
target-clean mixed-colour cancellation
  intersect synchronized nuisance separation
  intersect independently prescribed depth-four GHZ sensor values
  intersect the physical block-valued version of (15).                (22)
```

The scalar section proves that forgetting any of those tensor/sensor
conditions destroys the hoped-for obstruction.

## Scope wall

```text
bordered-hafnian two-port formula:                    PROVED;
six physical H6 faces from one eight-vertex graph:    ARBITRARY;
face morphism to K^6:                                 SPLIT SURJECTIVE;
one nonzero H4 anchor companion:                      THREE;
complete seventy-label H4 deck:                      CLOSED FORM;
thirty-six face/H4 partner stresses:                  IDENTICALLY SATISFIED;
full-edge-torus realization of every torus face:      PROVED;
physical face locus meets every pulled-back Segre:    PROVED;
three pure-colour scalar sections in one block graph: CONSTRUCTED;
every displayed block edge invertible:                PROVED;
displayed block graph is target-clean GHZ:            FALSE;
mixed-colour word (20):                               -10/3, NONZERO;
independently fixed target H4 deck meets section:      UNKNOWN;
mixed-colour cancellation with clean fan:             UNKNOWN;
nuisance-column separation on the same graph:         UNKNOWN;
unrestricted P6 obstruction or construction:          UNKNOWN;
global Krenn--Gu conjecture:                           UNRESOLVED.      (23)
```

## Replay

```powershell
uv run --with sympy python verify_p6_physical_six_face_hafnian_section_four_deck_synchronization_and_segre_sharpness.py
python audit_p6_physical_six_face_hafnian_section_four_deck_synchronization_and_segre_sharpness.py
python -m py_compile verify_p6_physical_six_face_hafnian_section_four_deck_synchronization_and_segre_sharpness.py audit_p6_physical_six_face_hafnian_section_four_deck_synchronization_and_segre_sharpness.py
uv run --with ruff ruff check verify_p6_physical_six_face_hafnian_section_four_deck_synchronization_and_segre_sharpness.py audit_p6_physical_six_face_hafnian_section_four_deck_synchronization_and_segre_sharpness.py
```

The primary replay constructs the symbolic seven-parameter section, checks
all six faces, all seventy four-deletion labels, and all thirty-six nested
partner stresses, then verifies the three-colour block certificate and its
nonzero mixed word.  The independent no-import audit rebuilds the same
identities with a separate sparse rational polynomial algebra and matching
recurrence.  Neither replay searches a graph, support, word, parameter
family, or finite field.

## Dependencies

- [`P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md`](P6_CLEAN_TWO_BY_THREE_SELECTOR_SEGRE_PULLBACK_AND_TORUS_PERMISSION_THEOREM.md)
- [`RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md`](RESPONSE_JETS_AS_PRINCIPAL_DELETION_DECKS_AND_ROOT_PARITY_LEGALITY_THEOREM.md)
- [`HIGHER_RESIDUAL_PERMANENTAL_TOMOGRAPHY_NESTED_COFACTOR_STRESS_AND_CUMULANT_INTERFACE.md`](HIGHER_RESIDUAL_PERMANENTAL_TOMOGRAPHY_NESTED_COFACTOR_STRESS_AND_CUMULANT_INTERFACE.md)
- [`RESIDUAL_DEPTH_LOOP_HAFNIAN_CUMULANT_AND_TWO_PORT_DISCRIMINANT_THEOREM.md`](RESIDUAL_DEPTH_LOOP_HAFNIAN_CUMULANT_AND_TWO_PORT_DISCRIMINANT_THEOREM.md)
