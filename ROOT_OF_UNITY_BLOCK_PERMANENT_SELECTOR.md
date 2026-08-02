# Root-of-unity block selector for permanents

## Status

**Verified characteristic-zero transfer lemma.**  The identity below is a
specialization of the block selector used in Chapter 5 of OpenAI's
[Ten Advances in Mathematics and Theoretical Computer Science](https://cdn.openai.com/pdf/ten-proofs-oai.pdf).
This note translates the construction into the square-zero language already
used in this repository and records exactly what it can and cannot do for the
Krenn--Gu programme.

The theorem concerns bipartite permanents.  It does **not** by itself produce
a legal symmetric graph gadget, a restriction `P_5 -> Delta_3`, a
counterexample, or a proof of the global conjecture.

## The selector theorem

Let `b,t,s>=1`, put `r=bt`, and assume `1<=d<=min(t,s)`.  Partition the
`r` row indices into blocks

```text
R_1 disjoint union ... disjoint union R_b,   |R_h|=t.
```

Choose a primitive `d`th root of unity `zeta` and put

```text
theta=(-1)^(d+1) 2^d.
```

Form an `r x (r-d)` constant matrix `U` from the following columns:

1. for each `h`, take `t-d` copies of the indicator `1_(R_h)`;
2. for each `h=2,...,b` and `j=0,...,d-1`, take

```text
1_(R_1 union ... union R_(h-1)) + 2 zeta^j 1_(R_h).
```

For an `r x s` variable matrix `X`, append `s-d` all-one rows below `X`
and a zero lower-right block:

```text
B(X) = [ X  U ]
       [ 1  0 ].
```

Then every permanent term using variable rows from more than one block
cancels.  More precisely,

```text
per(B(X))
  = (s-d)! (t-d)! (t!)^(b-1)
      sum_(h=1)^b lambda_h M_(t,s,d)(X_(R_h,[s])),       (1)
```

where `M_(t,s,d)` is the sum of the `d x d` permanental minors in the
displayed `t x s` block and

```text
lambda_1 = theta^(b-1),
lambda_h = theta^(b-h) (1+theta)^(h-2)   for h>=2.       (2)
```

Every `lambda_h` is nonzero over `C`.

## Square-zero proof

Work in the commuting square-zero algebra

```text
C[z_1,...,z_r]/(z_1^2,...,z_r^2)
```

and set `y_h=sum_(i in R_h) z_i`.  The coefficient of a squarefree
monomial in the product of the column forms of `U` is the corresponding
complementary permanent of `U`.

The root-of-unity columns give the exact identity

```text
product_(j=0)^(d-1) (Y+2 zeta^j y_h)
  = Y^d + theta y_h^d.                                  (3)
```

Consequently the product of all column forms is

```text
product_h y_h^(t-d)
  product_(h=2)^b ((y_1+...+y_(h-1))^d+theta y_h^d).
```

Square-zero capacity kills every term leaving two blocks unsaturated.
Induction on `h` leaves exactly

```text
sum_(h=1)^b lambda_h y_h^(t-d) product_(g!=h) y_g^t.    (4)
```

The coefficient of any squarefree monomial in the `h`th term of (4) is
`lambda_h (t-d)! (t!)^(b-1)`.  Expanding the permanent of `B(X)` along
its variable columns adds the factor `(s-d)!` and proves (1).

## The four-row seed

The smallest nontrivial case is `b=t=d=s=2`.  It is the exact identity

```text
per [ u  v   1   1 ]
    [ w  z   1   1 ]
    [ p  q   2  -2 ]
    [ r  s   2  -2 ]

  = -8(uz+vw) + 2(ps+qr).                              (5)
```

Thus all matchings mixing the two variable row blocks cancel, while the two
within-block order-two permanents survive with nonzero weights.

## Effect on the Krenn--Gu strategy

This changes the status of Routes E and F in
[`P5_ALTERNATIVE_STRATEGY_MAP.md`](P5_ALTERNATIVE_STRATEGY_MAP.md):

- It is an identity entirely inside the selected squarefree matching degree.
  It therefore supplies the kind of postselection-safe cancellation that
  the Gaussian version of Route E lacked.
- It is a concrete answer to Route F's cross-matching hazard.  A union of
  modules need not leave every cross matching alive; fixed root-of-unity
  columns can cancel whole mixed families at once.
- The tight-root theorem in
  [`FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md`](FIVE_ROOT_TIGHT_BLOCKER_P5_EXTRACTION.md)
  already produces an honest bipartite permanent between roots and blockers.
  That is the safest first setting in which to transport (1).

There are three nontrivial legality questions before this becomes a Krenn--Gu
construction:

1. The constant columns of `U` must arise from legal contractions or herald
   modes of the graph tensor, not from an arbitrary affine operation.
2. The bipartite selector must coexist with the residual hafnian factor and
   with the symmetric edge-block convention of the original graph.
3. The surviving block weights must assemble the required three diagonal
   colour channels without creating forbidden off-diagonal coefficients in
   the uncontracted modes.

## Next bounded experiment

Do not begin with a graph-support census.  Start with the verified heralded
Question-2 module from Route F and perform these tests in order:

1. express two colour-permuted copies as variable row blocks `R_1,R_2`;
2. realize the `d=2` seed (5) using fixed contractions and check every full
   graph matching coefficient;
3. if legal, lift to a `d=3` filter and then to the four-channel selector;
4. if illegal, extract the precise obstruction: affine constants, graph
   symmetry, residual matchings, or colour-channel rank.

A useful result is either a legal selector or a short impossibility theorem
for one of those four steps.  A numerical near-cancellation is not evidence.

## Exact replay

From the repository root:

```text
uv run --with sympy python verify_root_of_unity_block_permanent_selector.py
python audit_root_of_unity_block_permanent_selector.py
```

The primary verifier expands (5), checks (3) modulo cyclotomic polynomials
for `1<=d<=7`, and checks the complete square-zero coefficient support for
eight parameter triples.  The independent audit enumerates complementary
permanents over `Q` for `d=2` and over the exact Eisenstein field
`Q(omega)` for `d=3`.
