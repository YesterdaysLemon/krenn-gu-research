# Hostile self-review: rank-five support-two `(2,2)` complete exclusion

## Verdict

**PASS at the stated local scope.**  The package excludes the complete
transverse joint-rank-five support-two `(2,2)` profile.  The beta-zero atlas
is exhaustive, and its apparent Type-II family automatically becomes Type I
under the involved rank-two target-kernel equation.  The other block is then
unrestricted.  The proof does not exclude another involved-row profile,
support one, a Hilbert--Burch boundary, joint rank at most four, another
physical component, or any higher order.  Global Krenn--Gu remains
**UNRESOLVED**.

Reviewed artifacts:

- the owning theorem;
- its SymPy verifier;
- its independent standard-library `Fraction` audit;
- the S2AG, S2AH, and beta-zero localization dependencies.

## Adversarial claim inventory

1. The exhaustive beta-zero Type-II normal form `B=e_i tensor z` collapses
   to the coordinate monomial `e_i tensor e_i` under the target-kernel row.
2. A monomial block can be moved to `B_23` by the permitted root exchange and
   then is forced to `e_0 tensor e_0`.
3. The opposite involved-row kernel colour is exactly `c=1` or `c=2`.
4. Rank-two projections and the two contracted diagonal targets leave the
   two planes displayed in equation (13), with no assumption on the other
   rows of `C`.
5. The `c=2` plane is inconsistent in two individual root coefficients.
6. The `c=1` plane retains every entry of `C`; its only nonzero corrections
   lie on `T_1`, while the repeated square maps onto `T_2`.
7. The fully-transverse correction-line lemma turns the apparent `T_1`
   mixed corrections into the zero equations needed by the prior
   common-zero atlas.
8. Full singleton rank makes the alternating separated tensor nonzero, so
   the lemma gives the final contradiction.
9. The shared-factor sharpness fixture shows that three-factor
   transversality is load-bearing.

## Hostile questions

### Was the old tangent-only overstatement reintroduced?

No.  The theorem repeatedly treats `C` as arbitrary and explicitly says
that it is not assumed tangent, separable, rank one, or generic.  The full
target table contains the symbolic coefficients `C_(0,j)` and `C_(2,j)`.
The apparent no-monomial Type-II family is not assumed tangent-away; it is
eliminated first by showing that its coordinate-factor block is forced to be
a coordinate monomial.

### Does Type II really collapse without an illegal colour permutation?

Yes.  In the original target-coordinate bases, Type II says
`B=e_i tensor z` for some coordinate line `e_i` at the noncommon endpoint.
No renaming is required.  The target-kernel equation says the nonzero row
`d` of the same block is `kappa e_d`.  Since row `i` is the only nonzero row,
`d=i`, and the common-end form is `z=kappa e_i` in the original third-root
basis.  Hence `B` is a coordinate monomial.  The primary verifier solves all
nine `(i,d)` row systems symbolically; the independent audit enumerates the
same row alternatives with `Fraction` values.

### Does a monomial `B` really have to be diagonal colour zero?

Yes.  Its contraction by the support-two `eta` is the nonzero line `e_0`,
so its noncommon endpoint is colour zero and its common-end colour belongs
to `support eta`.  The target-kernel row of `B` is both nonzero and a
multiple of its own coordinate `e_d`; this forces `d=0` and the common-end
colour zero.  This is the same scalar-safe argument used in S2AH.

### Could the opposite kernel colour be zero after cancellation inside `C`?

No.  The entire kernel row of `C` is fixed by target consistency to
`kappa' e_c`, with no other entry in that row.  Since `eta(e_0)` is nonzero,
`c=0` would contribute a nonzero `e_0` component to `C(eta)`, contradicting
the required line `e_1`.  Hence `c=1` or `2` exhausts the possibilities.

### Are the two planes in equation (13) exhaustive?

Yes.  The row kernels put `pr_1 P` and `pr_2 P` in fixed coordinate
two-planes.  Contracted target consistency puts `(e_0,0)` and `(0,e_1)` in
`P`.  A third vector, modulo those two, has one remaining coordinate in
each projection; both coefficients are nonzero because both projections
have rank two.  This gives exactly the two displayed charts.

### Does the `c=2` contradiction accidentally compare different singleton coefficients?

No.  Both root positions use the coefficient tensor `S_2` of the same basis
vector

```text
u_2=tau E_100+C tensor e_2.
```

At `(1,0,0)`, `p_0=0`, the target is zero, and the coefficient `tau` forces
`S_2=0`.  At `(2,2,2)`, `r_2=0`, the target is `T_2`, and diagonal row two
of `C` forces `-T_2=kappa' S_2`.  No quotient, genericity, or selected-row
replacement is involved.

### Was any entry of the nonmonomial block discarded in the `c=1` chart?

No.  The three zero rows determine only `S_0=-T_0`,
`S_1=-(kappa')^(-1)T_1`, and `S_2=0`.  Coefficient comparison then gives

```text
M_(v_0,v_1)(q_j)=-(kappa')^(-1) C_(0,j) T_1,
M_(v_2,v_1)(q_j)=-(kappa')^(-1) C_(2,j) T_1.
```

The `eta` relation among `q_0,q_1` is mirrored by the contracted relation
among the corresponding `C` entries.  The primary verifier checks this
symbolically; the independent audit checks it in a separate sparse table.

### Why must a `T_1` correction involving `v_2` vanish?

If `v_2` has two source components, every tensor
`per(v_2,u,q)` contains one of the two factor lines of its nonzero square
image.  If `v_2` has three source components, decomposability of the square
image makes it share at least two base factor lines; quotienting the square
identity forces every `q in Q` to use those same two lines.  The mixed
tensor again lies in the sum of the two corresponding factor subspaces.
The colour-one target line differs from colour two in both factors, so its
intersection with that sum is zero.

### Does the common-zero atlas still work when the mutual mixed product is only constrained to a line?

Yes.  The nonconjugate two-source chart makes the two zero divisors
dependent.  The nonzero-tangent chart makes two independent zero divisors
span a plane containing `Q`, contradicting `V intersect Q=0`.  In the fully
conjugate chart, the two mutual products already carry the square-image
factors (one is on the square line itself); a fully transverse correction
line therefore forces both products to zero and the displayed alternating
formula vanishes.  The three-source scaling chart directly makes the three
scalar rows dependent, while the zero-coefficient chart is one-dimensional
or pure in one source.  These are exactly the prior exhaustive cases.

### Is full factor transversality merely cosmetic?

No.  The exact fixture

```text
v=x+y,  Q=span(x-y,t),  u_0=x-y+z_0,  u_1=z_1
```

has row rank five, both common mixed products with `v` zero, a nonzero
mutual correction on `x tensor y tensor z_1`, and a nonzero alternating
tensor.  Its correction and square lines share `x,y`; the physical
`T_1,T_2` lines share no factors.  The verifier and audit both replay this
fixture exactly.

### Is the independent audit genuinely independent?

Yes.  The primary verifier uses SymPy matrices, Kronecker products, symbolic
parameters, and nullspaces.  The audit imports no repository module and no
third-party package.  It rebuilds root and nonroot tensors as flat tuples of
standard-library `Fraction` values, uses hand-written Gaussian elimination,
and checks the transverse-line claim by basis exhaustion.

### Did review expose any implementation error?

Yes, and it was corrected before packaging.  The first primary replay put
`C tensor e_j` in the order `A_1 tensor A_3 tensor A_2` rather than the
physical order `A_1 tensor A_2 tensor A_3`.  The canonical-plane assertion
failed immediately.  The verifier now uses an explicit `place_13_2`
permutation, and the independent audit constructs every coefficient by the
physical index formula `9a+3b+c`.  Both routes now agree.

## Stop boundary

The proved conjunction is

```text
normalized target-consistent physical m=3 common-three-space point
+ transverse two-root derivative of rank six
+ total joint row rank five
+ third-row rank two with support-two kernel
+ both involved row ranks two
+ the exhaustive beta-zero Type-I/Type-II atlas
+ full singleton independence.
```

Removing either involved rank-two assumption breaks the target-kernel step
that collapses Type II and returns to the other S2AG profiles.  Support one,
the `(3,3)` and `(3,2)` support-two profiles, the Hilbert--Burch atlases, and
the lower-rank/global branches are not decided here.  Global status must
remain **UNRESOLVED**.
