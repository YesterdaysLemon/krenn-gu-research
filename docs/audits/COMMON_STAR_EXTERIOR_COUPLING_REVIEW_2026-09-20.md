# Independent assessment: the exterior-coupling obligation

## Verdict and evidence boundary

I accept the source identities and necessary full-cut equations in
[`full-binary-exterior-coupling-obligation.md`](../strategy/full-binary-exterior-coupling-obligation.md).
The row/column resource bookkeeping, mixed-permanent Laplace expansion,
reverse-orientation PSCL factor, distinct-color S2 substitution, and PSCT
diagnostic are mathematically correct.

I do **not** accept the exterior-coupling lemma as proved.  The note labels it
open, and neither the identities nor the diagnostics establish its asserted
incompatibility.  The lemma is, however, quantified strongly enough that a
proof would exclude the full common-star FB antecedent.  It would not supply
a reduction from arbitrary protected arrays or arbitrary Krenn--Gu witnesses.
The global conjecture remains **UNRESOLVED**.

The reviewed strategy note had this SHA-256 value over LF-normalized UTF-8
text bytes:

```text
ca8c9e09b255f3edbad0c95a184ced34d7ef577e0eb684a4bd639e5ca6cfbe2b
```

## Full cuts and resource bookkeeping

Let `C` be the proper induced shortest cycle localized by PSCL in a binary
resource `R`, and let `y` be a cycle vertex.  S1 and both S2 families give
minimum indegree and outdegree at least two, so `y` has an extra in-neighbor
`x`.  Inducedness puts `x` outside `C`.  With

```text
T=C\{y},        Y=M_R\T={y} union W,        W=M_R\C,
```

the full word whose color-`a` components are exactly `T` selects rows `T` and
columns `Y` in `R`.  Every selected left state belongs to `R`; other resources
contain selected right states only and have exact factor one.  Hence the full
mixed target is exactly `Z(T,Y)=0`.  No resource factor is divided out.

The arc `x->y` puts the left state of `x` in `R`.  Recoloring `x` from `b` to
`a` therefore adds row `x`.  If the right state of `x` is outside `R`, its old
resource still has only right states and contributes one; the new full source
in `R` is `Z(T union {x},Y)`.  Subtracting the two zero targets gives

```text
R_x(T,Y)=0.                                                (1)
```

If the right state of `x` is also in `R`, then `x` belongs to `W` and the
recoloring simultaneously removes column `x`.  The new source is
`Z(T union {x},Y\{x})`.  Comparing it with the original zero target gives

```text
R_x(T,Y\{x})=C_x(T,Y\{x}).                                (2)
```

This is the correct return-column case.  Treating it as row addition alone
would lose an actual selected state.  Both words are mixed because
`|T union {x}|=|C|<k`.

## Mixed-permanent Laplace expansion

The row occupation `R_x(P,Q)` consists exactly of source terms whose common
row subset contains `x`.  Expanding the `A` and `B` permanents along that row
has two cases.

If both permutations assign column `j` to `x`, their product extracts
`q_xj`, and the remaining sum is `Z(P,Q\{j})`.  If `A` assigns `j` and `B`
assigns a distinct `k`, their product extracts `A_xj B_xk`.  The remaining
`A` columns retain `k`, the remaining `B` columns retain `j`, and their common
columns lie in `Q\{j,k}`.  This gives exactly

```text
R_x(P,Q)=sum_(j in Q) q_xj Z(P,Q\{j})
 +sum_(j,k in Q, j!=k)
       A_xj B_xk M_(k,j)(P,Q\{j,k}).                      (3)
```

The off-diagonal sum is over ordered pairs, as required by the two different
permanent assignments.  Every term is counted once.  I independently replayed
the identity for two old rows and three columns with fully generic symbolic
`A,B`; the expansion has three same-column terms and six ordered mixed-column
terms and simplifies identically to the row occupation.  This finite symbolic
replay checks the indexing and multiplicity; it is not a proof of the open
lemma or of FB.

## Reverse PSCL factor and equation (4)

In the case `x` is not on the right shore of `R`, `Y={y} union W`.  After
transposing `A,B`, the same resource has exterior left shore `W`, and the
cycle orientation reverses.  Applying PSCL to the proper cycle subset
`T=C\{y}` gives

```text
Z(T,W)=(-1)^|T| product_(v in T) q_(v,succ(v)).
```

All displayed cycle products are supported and nonzero.  The `j=y` term in
(3) is therefore the claimed nonzero term

```text
q_xy (-1)^|T| product_(v in T) q_(v,succ(v)).
```

Separating it from the other diagonal and mixed assignments produces equation
(4) exactly.  Its nonzero value does not imply a contradiction because every
remaining term is an actual complex polynomial that may cancel it.

Equation (4) applies only when the right state of `x` lies outside `R`.  In the
return-column case, applying (3) to `Y\{x}` would produce
`Z(T,W\{x})`, while PSCL controls `Z(T,W)`.  Equation (2) also retains the
column occupation.  The note correctly refuses to replace either quantity or
to reuse (4) silently.

## Third-color identity and its local freedom

For a third color `c`, the displayed contractions use the actual `(a,c)`
factors from `x` and `(b,c)` factors from `y`.  The proved distinct-color S2
identity from PSCS is precisely

```text
q_xy=2H_xy-X_xy Y_xy.                                     (5)
```

Substitution into (4) is legitimate and uses no division.  It does not
identify `H,X,Y` with the binary mixed cofactors `M_(k,j)`: the corresponding
gadgets have different endpoint labels and no equality of their factor values
follows from support alone.  Shortest-cycle minimality removes chords inside
`C`; it does not remove edges from `C` or `x` to the exterior shore `W`.

The two-neighbor parameter `u` demonstrates only local freedom.  With center
factors one, the two leaf pairs satisfy

```text
(p_1-p_2)(h_1-h_2)=q_xy,
p_1+p_2=h_1+h_2=-1,
```

and the exclusions on `u` make all four leaf factors nonzero.  Thus it realizes
the two named local port sums and the single distinct-color edge equation.
It does not impose the reverse port sums at the fresh neighbors, their other
color ports, same-color S2, distinct-color S2 for other pairs, or any global
full-cut system.  It is an underdetermination diagnostic, not a three-color
control or counterexample.

## PSCT diagnostic

The substitution `C={0,1,2}`, `y=2`, `x=3` into PSCT has
`T={0,1}`, `W={5,6}`, and the right state of `x` outside the cycle resource.
Thus equation (1), and then (4), would be the relevant added full-cut
condition.  The accepted PSCT identities instead give

```text
R_3({0,1},{2,5,6})=(r^2+1)/(12r)!=0.
```

This proves that both localized faces plus all binary singleton and same-color
double targets do not imply equation (4).  PSCT has no third-color supply, so
it neither satisfies nor refutes the hypotheses of the proposed exterior-
coupling lemma.

## Why the open lemma would suffice for FB

Assume a full common-star FB array existed.  Its S1 and both S2 families give
minimum indegree and outdegree at least two for every binary directed support.
Its full cuts make each support strongly connected.  A shortest directed
cycle is induced and must be proper: a Hamiltonian shortest cycle together
with minimum outdegree two would have a chord and hence a shorter cycle.

PSCL then puts both states of that cycle in one resource and supplies its
exterior system.  Applying PSCL after reversing the color orientation supplies
the opposite system.  These are exactly the structural hypotheses of the open
lemma.  For every extra in-neighbor and out-neighbor, the two full mixed cuts
described above supply equation (1) or (2), or its transpose, according to the
resource containing the neighbor's other color state.

The lemma would assert that at least one such neighbor must violate its
equation, contradicting those full-cut targets.  Therefore a proof of the
lemma would exclude every array in FB's common-star scope.  The quantifiers are
sufficient; necessity or equivalence is not claimed.

What remains unproved is the lemma's central implication: no identity is yet
known that combines both families of binary mixed cofactors with the complete
third-color S1/S2 system and forces a violation.  Reversing orientation adds
another cofactor family rather than eliminating the first, and the return-
column case removes the PSCL-controlled column.  No full three-color control
or contradiction resolves these terms.  The note accurately records this as
an open parent obligation and ends the bounded synthesis without changing the
status of FB, CSQ4, or Krenn--Gu.

No external theorem, numerical premise, modular computation, Lean
formalization, or kernel check was used in this assessment.
