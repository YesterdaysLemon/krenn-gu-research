# Integer signed-lattice transport theorem

## Statement

Let `x_1,...,x_N` be nonzero complex variables.  Suppose exact
two-monomial amplitudes give relations

```text
x^r_i = -1,                    i=1,...,m,
```

where every `r_i` is in `Z^N`.  Write `R` for the matrix with rows
`r_i`, and let

```text
L = {z^T R : z in Z^m}
```

be their integer row lattice.

1. The relations are inconsistent whenever there is a `z in Z^m` with
   `z^T R=0` and odd `sum_i z_i`.
2. If every integer kernel vector has even coefficient sum, then for
   every `v in L` the parity

   ```text
   epsilon(v) = sum_i z_i mod 2,   where v=z^T R,
   ```

   is independent of the chosen representation.
3. Consequently, whenever `u-v in L`,

   ```text
   x^u = (-1)^epsilon(u-v) x^v.
   ```

4. In any amplitude `sum_j x^u_j`, group exponent vectors by cosets of
   `L` and transport every member to one representative with the sign in
   item 3.  Distinct cosets are distinct Laurent monomials in the quotient
   group algebra.  Hence:

   - a forbidden zero-target amplitude is impossible if exactly one
     grouped coefficient is nonzero;
   - a required nonzero amplitude is impossible if every grouped
     coefficient is zero.

No unimodular pivot minor is required.

More generally, for signed relations `x^r_i=(-1)^b_i` with
`b_i in {0,1}`, replace every coefficient sum above by the signed parity

```text
sum_i z_i b_i mod 2.
```

The proof is identical.  This mixed-sign form is what allows exact
binomial-closure steps to adjoin both `+1` and `-1` relations.

## Proof

Raising the `i`th relation to the integer power `z_i` and multiplying
gives

```text
x^(z^T R) = (-1)^(sum_i z_i).                         (1)
```

If `z^T R=0` and the coefficient sum is odd, (1) says `1=-1`, proving
item 1.

Suppose all kernel vectors have even coefficient sum.  If
`z^T R=z'^T R`, then `(z-z')^T R=0`, so `sum(z-z')` is even.  Thus
`sum z` and `sum z'` have the same parity.  This proves item 2, and (1)
then proves item 3.

After imposing the binomial relations, Laurent monomials whose exponent
vectors differ by `L` become signed copies of one another.  Monomials in
different cosets remain distinct basis elements of the corresponding
twisted group algebra.  A sum is therefore zero exactly when every
coset coefficient is zero.  This proves item 4.

## Exact Smith-form algorithm

Apply Smith decomposition to the transposed relation matrix:

```text
D = S R^T T,
```

where `S` and `T` are unimodular integer matrices and `D` is diagonal.
To decide whether an exponent difference `v` belongs to `L`, solve

```text
D y = S v.
```

The diagonal entries give exact divisibility tests; zero rows give exact
vanishing tests.  If they pass, `z=T y` is an integer relation
representation and its coefficient-sum parity is the transported sign.
Columns of `T` beyond the Smith rank form an integer kernel basis, so an
inconsistent kernel parity is detected exactly.

This handles saturated and nonsaturated row lattices alike.  In
particular, it repairs the earlier computational shortcut that required
one selected maximal minor to have determinant `+1` or `-1`.  A lattice
can have all Smith invariant factors equal to one even when that
particular pivot choice has a larger determinant.

## Order-14 consequence

For the first audited hard `C4+C4+C6` orbit-8 residual, the 22 candidate
cycle relations span a rank-22 lattice on 76 active relation variables.
All 22 Smith invariant factors are one and the integer kernel is zero.
Thus the prior `sign_consistent_relation_selection` stop did not describe
an algebraic survivor: the amplitude layer had simply not been run
because the old pivot-minor routine returned no unimodular basis.

The Smith-form reducer now tests amplitudes modulo this exact row lattice.
Any support exclusion produced by that continuation still requires an
independent replay of the relation clauses, Smith decomposition,
transport coordinates, amplitude activity, and signed coset
coefficients.

## Independent audit

Run:

```text
python claims/arbitrary-order/verify_integer_signed_lattice_transport.py
```

The verifier checks curated saturated, nonsaturated, dependent, and odd
kernel examples; replays deterministic constructed lattice points and
their transported parities; and reconstructs the 22-relation
`C4+C4+C6` instance.  It must write
`tmp/integer_signed_lattice_transport_verified.json` with
`"verified": true`.

## Boundary

This theorem makes signed transport exact for arbitrary integer relation
lattices.  It does not prove that the partial-circuit relation
disjunctions always select an inconsistent lattice, nor that every
forbidden amplitude reduces to a single nonzero coset.  The global
Krenn--Gu conjecture remains unresolved.
