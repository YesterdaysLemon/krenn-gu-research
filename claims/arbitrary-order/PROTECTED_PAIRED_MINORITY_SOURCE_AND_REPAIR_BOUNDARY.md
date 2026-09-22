# Protected paired-minority source and repair boundary

Date: 2026-09-22.

Status: exact identities and scoped route obstructions over C, with a passed
[independent review](../../docs/audits/PROTECTED_FULL_SOURCE_PARENT_REVIEW_2026-09-22.md).
The written matching-count arguments prove the stated arbitrary-order identities;
exact scripts replay finite instances and literal controls. The later
[low-minority countermodel theorem](PROTECTED_LOW_MINORITY_SUPPORT_COUNTERMODELS.md)
refutes P1 exclusion and every fixed paired-minority support cutoff. UPM,
SFULL, and global Krenn--Gu remain **UNRESOLVED**. No timeout or exploratory solver
outcome is evidence for an exclusion, and no Lean formalization is supplied.

The upstream definitions and resource semantics are those of
[PSMR](PROTECTED_SCAFFOLD_MINORITY_CYCLE_AND_RESOURCE_BOUNDARY.md).
This is a parent-theorem attempt extending the
[full-source extension boundary](PROTECTED_SCAFFOLD_FULL_SOURCE_EXTENSION_BARRIERS.md),
not an unrestricted-witness normal form.

## 1. Parent propositions and proof topology

Fix `k>=2` protected unit K4 components with arbitrary hollow oriented
intercomponent color blocks, the reverse orientation being the transpose.
For a background color `c` and a physical color word `a`, let

```text
q_c(a)=#{e in M_c: both endpoints of e have colors different from c}.
```

The background label need not occur at a numerical majority of vertices.

The support parents used here are:

* **macro supply, or UPM(1):** every mixed component-constant word has a
  supported crossing perfect matching in addition to its protected matching;
* **UPM(2):** no mixed physical word has exactly one supported perfect
  matching; and
* **P1:** macro supply together with the restriction of UPM(2) to every mixed
  word satisfying `q_c(a)<=1` for at least one color `c`.

The P1 parent asked whether that conjunction is impossible for every `k>=2`.
That universal exclusion is now refuted by an exact 18-component support;
the definitions and conditional source implication below remain valid.

A hypothetical full complex protected-scaffold source supplies macro support,
because each mixed component-constant protected term of weight one must be
canceled. It also supplies UPM(2), and hence P1, because a zero mixed source
coefficient cannot consist of exactly one nonzero matching monomial.
Therefore an all-order exclusion of P1 would exclude full sources in the
protected scaffold and prove SFULL.  No reduction from arbitrary global
witnesses to this scaffold is claimed.

At `q_c=0`, PSMR makes the no-singleton condition stronger.  A supported
permanent term gives a directed cycle cover on an `M_c`-independent minority
set.  A shortest supported directed cycle has no chord producing another
term, so it yields a mixed singleton word.  Consequently every P1 or UPM
support must satisfy

```text
no nonempty M_c-independent minority word supports a perfect matching,
for each c.                                             (PSMR0)
```

The deltas below show that macro supply plus (PSMR0) alone is still too weak,
and then identify exactly what the `q=1` equations add.

## 2. Cross-word splice and the refuted SES mechanism

For supported scalar perfect matchings `M,N`, possibly on different color
words, decompose the physical multigraph `M union N` into alternating even
cycles.  Choosing the `M` edges on any subset of cycles and the `N` edges on
the complement produces another supported scalar perfect-matching term; its
endpoint colors form one consistent spliced word.

For two singleton component-constant macro words, exceptional at components
`I` and `J`, fix a background `c`.  Give each alternating cycle a Boolean
variable.  Requiring the splice minority set to be `M_c`-independent produces
only four live 2-SAT clauses: two negative clauses from the two `M_c` edges
of `I` and two positive clauses from those of `J`.  This led to the proposed

> **Singleton exchange-splitting lemma (SES).**  Macro supply with `k>=3`
> forces some pair of supplied singleton macro matchings whose four-clause
> gate has a nonpure satisfying splice.

SES would combine with (PSMR0) to exclude the support immediately.  Its
downstream implication is correct.  Its proposed supply from macro support
and PSMR is false.

The [literal support fixture](../../tests/fixtures/protected_twelve_vertex_macro_cycle_control.json)
has 22 crossing
scalar entries on three protected K4 components.  An independent audit reads
only those literals, adds the 18 protected entries, and recursively enumerates
physical scalar matchings.  Its exact receipt is:

```text
canonical literal-support SHA-256
  c32c8a480ab62d9467859f802f3b08ac5d99450c447008c37edb1824686e7651
40 total scalar entries
605 supported scalar perfect-matching terms
401 supported physical words
one term in each pure fibre
all 24 mixed macro fibres have at least two terms
  histogram: 16x2, 5x3, 2x4, 1x8
zero supported nonempty M_c-independent minority terms
260 mixed singleton fibres outside the PSMR subsystem.
```

The unique-word histogram by minimum paired-minority depth is
`{1:56, 2:160, 3:44}`. Each entire directed graph `D_c` is acyclic, which is
stronger than PSMR's independent-cycle condition. Literal topological orders
are checked by the audit. Deleting any one of the 22 crossing entries loses
macro coverage, so the support is also inclusion-minimal for macro supply.

Every cyclewise splice of actual terms is itself among the enumerated terms.
The zero localized count therefore proves that no supplied singleton macro
pair has the nonpure satisfying splice demanded by SES.  This is an exact
`k=3` counterexample to SES under its macro-plus-PSMR premise.

It is not a P1 or UPM support: the 260 non-PSMR singleton fibres violate the
required no-singleton condition.  One concrete word is

```text
0020|0000|1100,        (q_0,q_1,q_2)=(1,4,5),
```

with its sole matching
`{01[00], 2-9[21], 3-8[01], 45[00], 67[00], 10-11[00]}`
replayed by the audit. Thus the countercontrol does
not refute P1, UPM, SFULL, or any weighted source statement.  It proves that a
successful exchange argument must use the `q=1` repair obligations beyond
PSMR, rather than deriving SES from macro supply and `q=0` vanishing alone.

## 3. Exact all-order `q=1` same-source formula

Fix `c` and a word with `q_c(a)=1`.  Let `P={x,y}` be the unique complete
minority `M_c` pair.  Let `I` contain the singleton minorities and set

```text
R=I union {x,y},       J=p_c(I).
```

Let `E` be the intact background `M_c` edges.  Define the actual matrix

```text
A_(r,i)=W_(r,p_c(i))[a_r,c],              r in R, i in I,
Delta_rs=per(A with rows r,s deleted),
g_rs=W_rs[a_r,a_s],
K^e_rs=W_ru[a_r,c]W_sv[a_s,c]
       +W_rv[a_r,c]W_su[a_s,c],           e={u,v} in E,
L_rs=g_rs+sum_(e in E)K^e_rs.                         (1)
```

Then the full physical coefficient is exactly

```text
T_W(a)=sum_({r,s} subset R) Delta_rs L_rs.             (Q1)
```

All factors and all permanental minors come from the same physical `W`.
There is no independently chosen cofactor or exterior resource.

For the counting proof, let `h` be the number of direct minority-minority
matching edges and `t` the number of intact background resources opened toward
two minorities.  Minority/background balance and hollowness give

```text
h+t=1.
```

The case `h=1` supplies `g_rs Delta_rs`; the case `t=1` supplies
`K^e_rs Delta_rs`.  These cases are disjoint and exhaust all physical
matchings, proving (Q1) for every order.

Under (PSMR0), a supported monomial of `Delta_rs` is a cycle-free spanning
path cover from the two roots `x,y` to the deleted rows.  This gives three
different behaviours:

* `Delta_xy=0` when `I` is nonempty;
* deleting one root and one vertex of `I` gives at most one spanning directed
  path from the other root; and
* deleting two vertices of `I` gives an unsigned sum of two vertex-disjoint
  spanning paths, which need not be unique even in a DAG.

Hence PSMR turns the one-root minors into possible unique path terms but does
not collapse the two-path minors.  The exact P1 gap is a **one-root exposure
lemma**: macro supply plus the full `q<=1` no-singleton premises must force a
word where a one-root minor and its actual closure coordinate `L_rs` together
support exactly one literal matching.  Moving to another resource, another
endpoint pair, or another two-path cover are all legal companion mechanisms
that such a proof must eliminate.

## Rooted circuits and the same-word descent obstruction

Let `P_c` be the physical protected matching `M_c`, and let `M` be any
supported scalar matching for a word `a`. Assume (PSMR0). Every nontrivial
alternating component of the multigraph `M union P_c` contains a complete
minority `M_c` pair. Consequently there are at most `q_c(a)` such components.
For `q_c(a)=1` there is exactly one, and it contains every minority vertex.

To prove this, doubled `P_c` edges carry only `(c,c)`, so a minority vertex
cannot lie on one. Conversely a nontrivial component must contain a minority:
hollowness and the protected internal blocks allow a color-`c` vertex to
match another color-`c` vertex only through its `P_c` edge. If a nontrivial
component `Z` contained no complete minority pair, keep its scalar `M` edges
and use `P_c` outside `Z`. This is a supported nonempty `q_c=0` word,
contradicting (PSMR0). Distinct components use disjoint protected pairs,
proving the bound and the q=1 conclusion.

Now let `M,N` be two terms for the same q=1 word, and let `Z` be a component
of their symmetric difference. Such a component is closed under `M`. If
`Z` is also a union of protected pairs (`p_c(Z)=Z`), it is closed under
`M union P_c`. If it meets any minority, it therefore contains the unique
nontrivial component and **all** minorities.

This is an exact obstruction to reducing the minority set by same-word
alternating exchange. An unsaturated component cannot be completed with
protected edges outside it; a saturated component that meets a minority
retains the entire minority word. Taking a minimum-minority word does not
change this conclusion. It is not a refutation of every possible induction
or exchange argument: cross-word/color operations and correctly joined
unsaturated boundaries remain possible, but require a new supply theorem.

There is an additional actual-weight obstruction to shortening the paths
in (Q1). In the accepted
[v3 Laurent control](../../tests/fixtures/eight_vertex_scaffold_subsystem_controls.json),
the word `0012|2212` at `c=2` has two terms with common path `2 -> 6 -> 0`.
One closes with protected edges `01` and `47`; the other closes with
crossings `0-7` and `1-4`. Both use path crossings `2-5` and `3-6`.
Their Laurent weights are respectively
`+r_12^(-1) r_21^(-1)` and `-r_12^(-1) r_21^(-1)`.
Thus the source equation holds while the path is unchanged. Both this v3
support and the 22-entry control are inclusion-minimal macro covers, so
macro minimality does not make each closure unique. The literal stationary
audit verifies these claims; neither control satisfies all P1 premises.

The remaining parent must couple the actual closures across words and
colors. Ordinary multiplication is insufficient because it must still
respect the resource correction below.

## 4. Exact all-order `q=2` correction

For a word with exactly two complete minority `M_c` pairs, let `T` be their
four endpoints, let `S` be the remaining independent minorities, and put
`R=T union S`.  For each four-set `X subset R`, define

```text
Delta_X=per A_(R minus X,S).
```

Retain the same actual seam matrix `L` from (1).  Then

```text
T_W(a)=sum_(X subset R, |X|=4) Delta_X C_X,            (Q2)
C_X=haf(L[X])-sum_(e in E)haf(K^e[X]).                 (2)
```

Expanding `haf(L[X])` correctly includes two direct edges, one direct edge
plus one resource, and two distinct resources.  Its only nonphysical terms
reuse one resource `e`; their total is exactly `haf(K^e[X])`, so the
subtraction in (2) enforces physical resource injectivity.

Writing `K^e_ij=alpha_i beta_j+beta_i alpha_j`, the repeated-resource term is

```text
haf(K^e[X])
 =2 sum_(Y subset X, |Y|=2)
     product_(i in Y)alpha_i
     product_(j in X minus Y)beta_j.                   (3)
```

It is generally nonzero.  Therefore ordinary Wick completion or multiplication
of the `q=1` equations does not give the `q=2` source: it creates precisely the
terms that the physical source subtracts.  This is an exact obstruction to
free `q=1`-to-`q=2` induction, not a refutation of P1 or UPM.

## 5. Protected-seam factor identity

The full `q=1` family nevertheless supplies a useful same-source factorization.
Fix a component `A`, colors `d!=c`, and a protected edge `D={r,s}` of
`M_d(A)`.  In another component choose a protected `M_c` resource
`T={x,y}`.  Color `r,s` by `d`, `x,y` by arbitrary `a,b!=c`, and all other
vertices by `c`.

The protected internal zeros kill every maximal minor in (Q1) except the one
deleting `r,s`, giving

```text
T_W(a)=Delta_T^{a,b}(D) L_D^{-T},                     (4)

Delta_T^{a,b}(D)
 =W_(x,p_c(r))[a,c]W_(y,p_c(s))[b,c]
  +W_(x,p_c(s))[a,c]W_(y,p_c(r))[b,c],                (5)

L_D^{-T}=1+sum_(e in M_c outside A, e!=T)K^e_rs[d,d;c]. (6)
```

The `1` is the protected `M_d` seam `rs`.  For a full complex source, (4) is
a zero-target equation, so

```text
Delta_T^{a,b}(D)!=0  ==>  L_D^{-T}=0.                 (7)
```

If

```text
L_D^macro=1+sum_(e in M_c outside A)K^e_rs[d,d;c],
```

then (7) gives the exact shared-entry identity

```text
L_D^macro=K^T_rs.                                     (8)
```

Here a nonzero supplier means a resource and root-color choice for which
`Delta_T^{a,b}(D)!=0`; a supported monomial or nonzero `K^T_rs` alone is not
that hypothesis. Two distinct nonzero resource suppliers `T,U` for the same
seam force

```text
K^T_rs=K^U_rs=L_D^macro.                              (9)
```

At support level, (4) says the matching count factors into the support count
of the two-path supplier and that of the direct/resource seam; P1 forbids both
counts being one simultaneously.

This factorization also locates the upstream supply gap.  In a degree-two
component-constant macro matching, the two crossing ports of a component
form an edge of the protected matching for that component's own color.  The
supplier in (5) instead needs an `M_c` pair at its root and an `M_d` pair at
its target.  Both endpoint components must therefore have quotient degree
four before the supplier can occur inside that macro matching.  Ordinary
degree-two macro cycles do not supply the nonzero premise of (7).  Even if
several seams are supplied, using the same resource repeatedly lands in the
correction subtracted in (Q2).  A proof needs a cross-word
**distinct-resource supplier** or an identity killing the repeated-resource
correction.

## 6. The q=1 PSFD base control

The explicit 62-component, 248-vertex
[PSFD base support](PROTECTED_SCAFFOLD_FIXED_MINORITY_DEPTH_NO_GO.md) is not a countermodel
to P1.  For each background color, the union of both minority arc systems has
no `M_c`-independent directed cycle, so its entire `q=0` subsystem passes.
Nevertheless an independently replayed word for `c=0` has

```text
q_0=1,
12 minority vertices (one paired-minority edge and ten singleton minorities),
exactly one supported perfect matching on the 248-vertex scalar graph.
```

The literal replay reconstructs 744 scalar support entries and the unique
124-edge perfect matching by forced-endpoint recursion.  Thus the `q=1`
part of P1 detects a defect invisible to PSMR's `q=0` cycle condition.

This finite base also fails component-constant macro supply at its displayed
label-avoiding macro coloring, so it does not satisfy the other P1 premise.
The check does not assert that the same short unique word survives every
high-girth PSFD lift; lifting may postpone closure.  No such extrapolation is
needed for its scoped role as a q=0-versus-q=1 control.

## 7. Exact implications and remaining parent

The accepted deltas give the following proof topology:

1. A full protected source supplies P1 and UPM.
2. PSMR turns their `q=0` part into the exact vanishing condition (PSMR0).
3. SES would have contradicted (PSMR0), but the audited 22-entry `k=3`
   support refutes SES from macro supply plus PSMR alone.
4. Formula (Q1) displays the missing P1 information as actual one- and
   two-path minors contracted with actual closure seams.
5. Formula (Q2) proves that the first macro sector contains a generally nonzero
   repeated-resource correction absent from ordinary Wick closure.
6. The protected-seam factorization extracts one genuine same-source product
   equation, but macro supply does not yet furnish its nonzero supplier or
   distinct resources.

P1 exclusion is now **refuted**, and so is exclusion of its restriction to
whole-port DAGs. The
[subsequent parent synthesis](PROTECTED_LOW_MINORITY_SUPPORT_COUNTERMODELS.md)
constructs an explicit 18-component support and proves finite countermodels
exist for every fixed paired-minority cutoff. Thus no fixed-cutoff support
argument can force the proposed one-root exposure. The identities in this
owner remain valid. UPM remains open: these controls do not supply its
unrestricted all-word condition. SFULL remains open; the weighted WP1 parent
retaining all macro and one-pair coefficient equations is not refuted by the
support constructions.
No global arbitrary-witness-to-protected-scaffold supply is claimed.

The maintained [frontier](../../docs/current-frontier.md) records these
identities, the refuted SES and same-word descent mechanisms, and the later
fixed-cutoff parent refutation. No protected
full-source exclusion or global coverage edge has been closed.

## 8. Minimal literal replay bundle

Run from the worktree root:

```text
python -X utf8 claims/arbitrary-order/audit_protected_macro_cycle_control.py
python -X utf8 claims/arbitrary-order/verify_protected_one_pair_formula.py
python -X utf8 claims/arbitrary-order/verify_protected_two_pair_resource_correction.py
python -X utf8 claims/arbitrary-order/verify_protected_seam_factor.py
python -X utf8 claims/arbitrary-order/audit_protected_stationary_closure.py
python -X utf8 claims/arbitrary-order/audit_protected_psfd_one_pair.py
python -X utf8 claims/arbitrary-order/verify_protected_scaffold_fixed_depth_control.py
```

The first command is the independent literal audit of the 22-entry SES
countercontrol.  The next three check the `q=1`, `q=2`, and protected-seam
identities with exact arithmetic; their arbitrary-order status rests on the
written matching-count proofs, while the scripts give exhaustive finite and
sampled controls. The stationary-closure audit checks the actual Laurent
cancellation and macro minimality. The PSFD audit checks the finite base's
q=0 cycle boundary and its literal q=1 singleton word; the existing
fixed-depth verifier replays its original macro-failure control. No timeout
result or search failure is part of the evidence bundle.
