# Partial-circuit binomial-closure lemma

## Statement

Work in nonzero complex variables and suppose a collection of exact
two-monomial amplitudes has already produced a consistent signed integer
lattice

```text
x^r_i = s_i,                  s_i in {+1,-1}.
```

Reduce another exact amplitude modulo those relations by grouping its
Laurent monomials into exponent-lattice cosets and transporting their
signs with the integer signed-lattice theorem.

1. If a forbidden zero-target amplitude reduces to exactly two nonzero
   coset terms

   ```text
   a x^u + b x^v = 0
   ```

   with `|a|=|b|`, then it forces the new exact signed binomial

   ```text
   x^(u-v) = -b/a in {+1,-1}.                         (1)
   ```

2. If a required monochromatic amplitude, whose exact target is `1`,
   reduces to one nonzero coset term

   ```text
   a x^u = 1
   ```

   with `|a|=1`, then it forces the exact signed anchor

   ```text
   x^u = 1/a in {+1,-1}.                              (2)
   ```

3. Relations (1) and (2) may be adjoined and the reduction repeated.
   Every iteration is an exact logical consequence of the original
   amplitudes.

4. The branch is contradictory if an iteration produces any of:

   - an inconsistent signed integer-kernel dependency;
   - a derived signed relation whose exponent already has the opposite
     transported sign;
   - a forbidden amplitude with exactly one nonzero coset coefficient;
   - a required amplitude with no nonzero coset coefficient.

## Rational-constant extension

The equal-magnitude restriction is optional.  For exact relations

```text
x^r_i = q_i,                  q_i in Q*,
```

an integer dependency `z^T R=0` is consistent exactly when

```text
product_i q_i^z_i = 1.
```

When this kernel condition holds, the transported multiplier for
`v=z^T R` is the well-defined rational number `product_i q_i^z_i`.
Therefore every two-coset forbidden amplitude

```text
a x^u + b x^v = 0
```

with nonzero rational `a,b` yields

```text
x^(u-v) = -b/a,
```

even when `|a| != |b|`.  A one-coset required amplitude similarly yields
an exact rational anchor.  Smith form still decides exponent-lattice
membership; only the transported right-hand side changes from a sign to
a rational product.

## Proof

The integer signed-lattice theorem identifies every monomial in one coset
with a signed copy of the chosen representative.  Thus the displayed
reduced amplitudes are exact identities in the quotient Laurent group
algebra, not numerical approximations.

For item 1, divide the two-term zero identity by the supported nonzero
`a x^v`.  Equal coefficient magnitude makes `-b/a` exactly `+1` or
`-1`, giving (1).  For item 2, divide the exact target identity by
`a`; again `|a|=1` makes the right side a sign.  Adjoining logical
consequences preserves every solution, proving item 3.

The four terminal cases in item 4 respectively assert `1=-1`, assign
opposite signs to the same Laurent monomial, leave a supported nonzero
monomial as the whole value of a forbidden amplitude, or annihilate an
amplitude required to equal one.  Each is impossible.

## Relation disjunctions

The partial minimal-circuit dichotomy can produce disjunctions such as

```text
relation i OR relation j.
```

Binomial closure must therefore distinguish:

- a **relation-selection branch certificate**, conditional on one
  satisfying choice of relations; and
- a **support certificate**, which requires closing every satisfying
  relation selection.

Because adding valid relations cannot repair a contradiction, it is
enough to close every inclusion-minimal satisfying selection.  For the
first audited `C4+C4+C6` orbit-8 support, the 18 clauses consist of four
units and fourteen binary clauses.  They have 128 minimal satisfying
selections: 64 of size 12 and 64 of size 14.

## First audited branch

Selecting all 22 candidate cycle relations gives a rank-22 initial
lattice.  Radius-two binomial closure derives 52 distinct signed
relations from equal-magnitude two-coset forbidden amplitudes.  The final
74-relation lattice has rank 41.  A forbidden colouring with 13 active
perfect matchings then reduces to exactly one nonzero signed coset.

This closes that relation-selection branch, not the support.  The
independent verifier reconstructs all 18 relation clauses, independently
rederives every one of the 52 binomials, replays the final Smith lattice,
and checks the 13-term terminal amplitude:

```text
python verify_fourteen_vertex_partial_circuit_binomial_branch.py \
  tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_closure_all22_r2.json \
  --output tmp/fourteen_vertex_c4_c4_c6_orbit8_partial_binomial_closure_all22_r2_verified.json
```

The required output has `"verified": true`,
`"relation_selection_branch_closed": true`, and
`"support_closed": false`.

## Boundary

The closure lemma is exact, but a finite radius restricts which source
amplitudes are harvested.  A surviving relation selection is therefore
only a null result for that source census.  A support is excluded only
after all its relation-selection branches are independently closed.  The
global Krenn--Gu conjecture remains unresolved.
