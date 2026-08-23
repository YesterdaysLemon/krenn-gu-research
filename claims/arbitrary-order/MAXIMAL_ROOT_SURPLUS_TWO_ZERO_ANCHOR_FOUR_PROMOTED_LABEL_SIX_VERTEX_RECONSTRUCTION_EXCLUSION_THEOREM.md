# Maximum-root surplus-two zero-anchor four-promoted-label six-vertex reconstruction exclusion

## Status and scope

The global Krenn--Gu conjecture is **UNRESOLVED**.

This document proves `GLS53`.  In characteristic zero, at every root order
`r>=3`, no zero-anchor fully swallowed fixed-residual target point has exactly
four effective auxiliary labels when all four labels are promoted ports.  The
proof retains the complete physical complementary decks, contracts only the
inactive promoted ports, and reconstructs an ordinary six-vertex ternary
Krenn--Gu graph.  The accepted complete six-vertex theorem excludes that
graph.

The result is pointwise on every incidence-rank, nuisance-rank, deck-zero,
response, selector, divisor, and residual-shore fibre.  It makes no
genericity assumption and divides by no response, deck, selector, or minor.
It includes `r=3`, where there are no inactive promoted ports.

The theorem excludes only the support type consisting of four promoted
ports and no residual label.  Exactly-four-label supports containing one or
both residual labels, every support of five or more labels, source-to-full-
swallow coverage, raw escape, nonzero anchors, and every legal attachment
gate remain open.  This is not strategic-node closure or global resolution.

## Dependencies and provenance

- `GLS21` gives the complete raw pair-labelled promoted decomposition and
  identifies each coefficient's complementary physical deck.
- `GLS36` gives the fixed-residual uncontracted target equation.
- `GLS39` defines auxiliary-label effectiveness and identifies vanishing
  root companions.  No rank statement from `GLS39` is used.
- `GLS52` is frontier context: it proves the lower bound `|Act|>=4` inside
  the zero-anchor full-swallow target locus.  It is not a proof step in the
  four-promoted-label exclusion.
- The accepted computer-assisted
  [`six-vertex theorem`](../finite/n06/SIX_VERTEX_CERTIFICATE.md) excludes
  every complex six-vertex Krenn--Gu solution in three or more colours.

The new step is the exact graph reconstruction from the six surviving raw
pair labels.  The focused verifier enumerates all six-vertex perfect
matchings and compares them with the raw-label formula.  The independent
no-import audit uses a separate bit-mask hafnian recursion and sparse
polynomial words.  The written proof carries the arbitrary-root and
characteristic-zero transfer.

## 1. Fixed-residual equation and effective support

Retain the established notation

```text
A={a_0,a_1},                  Q={q_0,q_1},
T=Q disjoint-union Uhat,      |Uhat|=2r-2>=4,
X_u:V_u -> V_(a_0)^*,        Y_u:V_u -> V_(a_1)^*.
```

Fix a fully supported residual contraction on `Q`.  Thus the three target
coefficients `alpha_c` in the remaining equation are nonzero.  Assume
pointwise that

```text
omega=0,
Act=P={u_0,u_1,u_2,u_3} subset Uhat.                (1)
```

In particular, both residual auxiliary labels and every promoted label
outside `P` are ineffective.  Put

```text
I=Uhat-P,                 |I|=2r-6>=0.              (2)
```

Evaluate every port in `I` at

```text
1=e_0+e_1+e_2.                                      (3)
```

When `r=3`, `I` is empty and (3) is the empty contraction.  Each target pure
word evaluates to one on every inactive port, so the three target
coefficients remain the nonzero `alpha_c`.

For distinct `u,v in P`, the promoted pair coefficient is

```text
mu_uv(z_u,z_v)
 =X_u(z_u) tensor Y_v(z_v)+X_v(z_v) tensor Y_u(z_u)
 in V_(a_0)^* tensor V_(a_1)^*.                    (4)
```

For a pair `{k,l} subset P`, define the residual- and inactive-evaluated
complementary deck

```text
D_kl
 =H_(Q union I union {k,l})(z_Q,1_I,-_k,-_l)
 in V_k^* tensor V_l^*.                             (5)
```

Equivalently, `D_kl` is the physical deck belonging to the raw root pair
`P-{k,l}`, after exactly the contractions already specified.  It is a
bilinear edge block on the two uncontracted ports `k,l`; it is not a freely
chosen rowwise coefficient.

Every raw pair label outside `binom(P,2)` has zero root companion.  Indeed,
a promoted pair incident with `I` contains an endpoint with `X=Y=0`, and a
pair incident with either residual auxiliary label contains a vanished
evaluated residual shore.  Both residual labels being ineffective also
gives `q=0`.  Finally the top raw label vanishes because `omega=0`.
Therefore the complete contracted source equation is exactly

```text
sum_({u,v} subset P) mu_uv tensor D_(P-{u,v})
 =sum_(c=0)^2 alpha_c e_c^(tensor(A union P)).       (6)
```

No deck in (5) is assumed nonzero, and no exceptional fibre has been
discarded.

## 2. Six-vertex reconstruction

Construct a weighted ternary graph on the literal six vertices `A union P`
with bilinear edge blocks

```text
W_(a_0,a_1)=0,
W_(a_0,u)=X_u,                 u in P,
W_(a_1,u)=Y_u,                 u in P,
W_(k,l)=D_kl,                  {k,l} subset P.       (7)
```

### Lemma 1 (matching bijection)

The hafnian tensor of (7) is the left side of (6).

#### Proof

The zero root--root edge removes every perfect matching pairing `a_0` with
`a_1`.  Every remaining perfect matching chooses an unordered pair
`{u,v} subset P` of ports hit by the two roots.  Its two possible root--port
orientations contribute

```text
X_u tensor Y_v+X_v tensor Y_u=mu_uv,                (8)
```

and the two ports in `P-{u,v}` must be paired by their single edge
`D_(P-{u,v})`.  Conversely every choice of `{u,v}` and either orientation is
one perfect matching.  Grouping the twelve surviving matchings into six
unordered pairs gives exactly the left side of (6). `square`

Thus (6) says that the graph (7) has the weighted GHZ output

```text
sum_(c=0)^2 alpha_c e_c^(tensor 6),       alpha_c!=0.          (9)
```

### Lemma 2 (weighted target normalization)

Over any field containing the coefficients and the inverses of the
`alpha_c`, (9) yields an ordinary normalized ternary Krenn--Gu solution on
the same six vertices.

#### Proof

At the single vertex `a_0`, apply the invertible diagonal local scaling

```text
e_c^* |-> alpha_c^(-1)e_c^*.                        (10)
```

Apply (10) to the `a_0` factor of every incident edge block.  Every perfect
matching contains exactly one edge incident with `a_0`, so the graph tensor
is transformed by the same local map.  Its pure colour-`c` coefficient
becomes one, and every forbidden mixed coefficient remains zero.  The zero
root edge stays zero. `square`

### Theorem 3 (four-promoted-label exclusion)

No point satisfying (1) exists over a characteristic-zero field.

#### Proof

First suppose the ground field is a subfield of `C`.  Lemmas 1 and 2 turn
the complete target equation into a six-vertex ternary Krenn--Gu solution,
contradicting the accepted six-vertex theorem.

For an arbitrary characteristic-zero field, collect the finitely many edge,
contraction, and target coefficients of the alleged point, together with the
three `alpha_c^(-1)`, in a finitely generated extension `K_0` of `Q`.
Every finitely generated characteristic-zero field embeds into `C`.
Applying such an embedding preserves all polynomial source and target
equalities and the nonvanishing of the `alpha_c`.  The resulting complex
point is excluded by the preceding paragraph. `square`

## 3. Exact boundary

Together with `GLS52`, the four-label frontier inside zero-anchor full
swallow is

```text
zero-anchor full swallow with <=3 effective labels:          EMPTY;
exactly 4 labels, 0 residual + 4 promoted:                    EMPTY;
exactly 4 labels, 1 residual + 3 promoted:                    OPEN;
exactly 4 labels, 2 residuals + 2 promoted:                   OPEN;
five-or-more effective labels:                               OPEN;
silent source necessarily enters full swallow:               UNKNOWN;
raw escape supplies an original legal target package:        NOT SUPPLIED;
nonzero-anchor marginal/double-transverse branches:           OPEN;
response/activity/synchronization/nuisance/anchor gates:      OPEN;
arbitrary-root strategic-node closure:                        UNKNOWN;
global Krenn--Gu conjecture:                                  UNRESOLVED.
```

The proof is support-free with respect to edge-entry patterns: it uses only
the auxiliary-label support type and the complete physical target equation.
It does not imply that an arbitrary four-label incidence family has a
private target row, nor does it classify either residual-containing support.

## Verification boundary

The focused verifier enumerates the fifteen perfect matchings of six
vertices, checks that the three root--root matchings vanish and the remaining
twelve group into the six terms in (6), checks the complementary-deck index
typing for several root orders including `r=3`, and replays diagonal target
normalization over exact rationals.

The independent audit imports no project code or algebra package.  It uses
a bit-mask recursive hafnian with sparse monomial dictionaries, derives the
raw-label census independently, and checks equality with the six-term
formula at exact finite-field samples.  The written proof, not either finite
test range, carries the arbitrary-root theorem.

The accepted six-vertex theorem is an upstream computer-assisted premise.
Its authenticated historical certificate bundle is not tracked in a clean
worktree.  The current verifier was replayed read-only against the protected
authority bundle with output redirected outside every repository.  It
returned `verified=true` with CNF SHA-256
`154b1a64a70b10eef5bd7cb3ddb929033d408b65f26ff2704eacc610030154c7`;
the exact command and artifact hashes are retained in the hostile review.
This package does not reprove that finite theorem.

Neither checker proves either residual-containing four-label branch,
five-or-more-label exclusion, source coverage, raw-escape attachment, a
legal downstream receiver package, strategic-node closure, or the global
conjecture.
