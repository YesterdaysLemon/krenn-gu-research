# The formal 2+2+1 scalar charts admit one common terminal block

## Status

**Exact common-terminal-block realization over
`Q(rho)`, with `rho^2=21`.**  The three scalar colour charts of the formal
2+2+1 cofactor ledger are principal-hafnian realizable using one and the same
terminal--terminal matrix.  All 186 prescribed scalar coordinates are
verified exactly.

This removes the terminal-block synchronization gap left by
`P7_221_FORMAL_LEDGER_SCALAR_HAFNIAN_REALIZABILITY_AND_SYNCHRONIZATION_GAP.md`.
The later diagonal-gluing theorem places those different core--core and
core--terminal data into one tensor-valued physical block graph and recovers
all pure charts.  It also exhibits a nonzero mixed word in that canonical
lift.  Cancellation by more general off-diagonal block entries remains
unproved.  The `P_7` restriction and the global Krenn--Gu conjecture therefore
remain unresolved.

## 1. One terminal block for all three charts

Let

```text
P={1,2,3,4,5,a,b},        Q={a,b},
K=Q(rho),                  rho^2=21,
kappa=1+22/rho.                                            (1)
```

The common symmetric terminal block `M` has the following nonzero entries:

```text
M_12=M_14=M_23=M_34=-kappa,
M_13=M_24=M_1a=M_3a=M_2b=M_4b=7,
M_1b=M_2a=M_3b=M_4a=-rho,
M_ab=1-rho.                                                 (2)
```

Every entry involving terminal `5` is zero.  For each colour `c`, construct
a graph with seven core vertices `Z_c` and terminal block (2), and define

```text
C_D^(c)=haf W_c[Z_c union (P\D)].                           (3)
```

The lower-root ledger prescribes 62 values in each chart: all even nonempty
deletions except `D=Q`.  The empty deletion is also free.  The certificate
below realizes every prescribed value and selects

```text
c=0: C_Q=0,       C_empty=155+110 rho/7,
c=1: C_Q=0,       C_empty=155+110 rho/7,
c=2: C_Q=103/147, C_empty=103/147+36 rho.                  (4)
```

## 2. Squarefree Wick deconvolution

The colour-0 construction is obtained symbolically rather than by searching
over graphs.  Work in the squarefree commutative algebra

```text
S=K[x_1,x_2,x_3,x_4,x_5,x_a,x_b]/(x_i^2).                 (5)
```

If a seven-core graph has core block `A`, core--terminal block `R`, and
terminal block `M`, write its odd terminal signature as

```text
F_(A,R,M)(x)=sum_(T odd) haf W[Z union T] x_T.              (6)
```

Let `Phi_(A,R)=F_(A,R,0)` and put

```text
E_M=sum_(S even) haf M[S] x_S
   =exp_S(sum_(i<j) M_ij x_i x_j).                         (7)
```

Splitting a matching according to its terminal--terminal edges gives the
squarefree Wick convolution

```text
F_(A,R,M)=E_M Phi_(A,R),       E_M^(-1)=E_(-M).             (8)
```

Thus the core response required behind a fixed `M` is obtained exactly by
multiplying the target signature by `E_(-M)`.

## 3. Deconvolving the colour-0 ledger

Choose the free colour-0 value `C_Q=0` and temporarily write
`u=C_empty`.  Reindexing the colour-0 cofactor ledger by surviving terminal
sets gives a signature divisible by `x_1x_2`:

```text
F_0=x_1 x_2 H,                                               (9)

H=(x_3+x_5+x_a)
  +(x_45b+x_35a+x_34b-x_5ab+x_4ab+x_3ab)
  +u x_345ab.                                               (10)
```

Because `x_1x_2` is already present, every term of (2) incident to terminal
1 or 2 vanishes in the squarefree product.  Only the restriction of `M` to

```text
V={3,4,5,a,b}                                               (11)
```

contributes.  Put

```text
psi=E_(-M[V]) H.                                            (12)
```

Its linear part is

```text
L=x_3+x_5+x_a.                                              (13)
```

Its cubic coefficients are

```text
psi_345=1+22/rho,        psi_34a=1+43/rho,
psi_34b=-6,              psi_35a=-6,
psi_35b=rho,             psi_3ab=2 rho,
psi_45a=rho,             psi_45b=-6,
psi_4ab=-6,              psi_5ab=-2+rho.                   (14)
```

The quintic coefficient is

```text
psi_345ab=u+76-23/rho.                                     (15)
```

Equations (12)--(15) are a direct squarefree multiplication using (2); no
unknown system remains at this stage.

## 4. A determinant-one four-core factorization

We now realize (12) in the factorized form

```text
psi=L E,                                                    (16)
```

where `E` is the even response of four core vertices indexed by
`3,4,5,a`.  Its constant coefficient is one.  Its quadratic coefficients
are

```text
E_34=kappa,       E_35=1/rho,       E_3a=-6-1/rho,
E_3b=1+rho,       E_45=0,           E_4a=rho,
E_4b=-6,          E_5a=0,           E_5b=-1,
E_ab=-1+rho.                                               (17)
```

Multiplication by (13) gives every cubic value in (14).  For example,

```text
[x_34a](L E)=E_4a+E_34=rho+kappa=1+43/rho,
[x_35a](L E)=E_5a+E_3a+E_35=-6.                           (18)
```

Here is an exact graph producing `E`.  Join each of four core vertices
`h_3,h_4,h_5,h_a` to its namesake terminal with weight one.  Its only
core--core edges are

```text
A[h_3,h_5]=rho,
A[h_4,h_5]=-6-1/rho,
A[h_4,h_a]=1/rho,
A[h_5,h_a]=kappa.                                         (19)
```

The complementary two-core matrix controlling the anchored quadratic
response, in the order `(3,4,5,a)`, is

```text
B=
[ 0          kappa       1/rho      -6-1/rho ]
[ kappa      0           0           rho      ]
[ 1/rho      0           0           0        ]
[ -6-1/rho  rho          0           0        ].          (20)
```

It satisfies

```text
det B=1.                                                   (21)
```

Join terminal `b` to these four cores with column

```text
v=
(-rho,
 -5-2 rho/21,
 230+104 rho/7,
 1+16 rho/21)^T.                                          (22)
```

Then

```text
Bv=(1+rho,-6,-1,-1+rho)^T,                                (23)
```

which supplies exactly `E_3b,E_4b,E_5b,E_ab` in (17).  The
four-terminal response on the four anchors is one; replacing anchor `i` by
`b` gives `v_i`.  Therefore

```text
[x_345ab](L E)=v_3+v_5+v_a
              =231+307 rho/21.                            (24)
```

Comparing (15) and (24) fixes

```text
u=155+110 rho/7,                                          (25)
```

the free colour-0 value in (4).

## 5. The colour-0 and colour-1 graphs

Add three more core vertices to the four-core graph above.

- Join `f_1` only to terminal `1`, with weight one.
- Join `f_2` only to terminal `2`, with weight one.
- Join `ell` to terminals `3,5,a`, each with weight one, and give `ell` no
  core edge.

Together with (19), (22), and the terminal block (2), these are all edges of
the colour-0 graph.  The first two private core vertices force the factor
`x_1x_2`; `ell` forces the factor `L`; and the remaining four cores produce
`E`.  Its no-terminal-edge response is therefore

```text
Phi_0=x_1x_2 L E=x_1x_2 psi.                              (26)
```

Equations (8), (12), and (26) give exactly the target signature (9)--(10),
so every prescribed colour-0 cofactor is realized.

The colour-1 graph requires no new calculation.  The involution

```text
sigma=(1 4)(2 3)(a b),             sigma(5)=5             (27)
```

preserves every entry of the common terminal matrix (2).  It also sends the
entire colour-0 ledger to the colour-1 ledger.  Relabelling only the terminal
ends of the colour-0 core--terminal edges by `sigma` therefore produces the
colour-1 realization, with the same free values as in (25).

## 6. The colour-2 graph already uses the same block

For completeness, the colour-2 certificate using (2) has core vertices

```text
z_*,z_1,z_2,z_3,z_4,z_5,z_6.                              (28)
```

Terminal `5` is joined only to `z_*`, with weight `1/7`.  The nonzero
core--core edges are

```text
A[z_1,z_2]=1,        A[z_3,z_4]=1/rho,
A[z_5,z_6]=rho.                                            (29)
```

The six remaining core--terminal rows are

```text
r_1=X_1+X_3,                 r_2=X_2+X_4,
r_3=X_a+X_1+X_3,             r_4=X_b+X_2+X_4,
r_5=X_1+X_3,                 r_6=X_2+X_4.                 (30)
```

This is exactly the earlier colour-2 graph, whose direct terminal block was
(2).  It realizes all 62 prescribed colour-2 values and the free values in
(4).

### Theorem 1 (common-terminal-block scalar realizability)

Over `Q(sqrt(21))`, the three scalar colour charts of the formal 2+2+1
cofactor ledger admit seven-core principal-hafnian realizations with the
single common terminal matrix (2).  The constructions in Sections 5 and 6
realize all 186 prescribed coordinates and the six free values displayed in
(4).

## 7. Exact boundary after synchronization

The earlier scalar boundary

```text
M_0=M_1=0 but M_2 nonzero
```

was a feature of the first coordinate-copy certificates, not an invariant of
the ledgers.  Equations (2) and (19)--(30) remove it constructively.  Thus a
common terminal matrix cannot be used as a scalar no-go obstruction.

The present theorem is still chartwise.  The three graphs assign different
pure-colour values to core--core and core--terminal edges.  Those values can
be placed into colour components of common tensor edge blocks, but a hafnian
matching may then select different colours on different edges.  The resulting
mixed-colour words are not tested by any of the three scalar specializations.
No cancellation theorem for those words is proved here.

The sharp status wall is therefore

```text
formal scalar ledgers:                         REALIZED;
one common terminal--terminal block:           REALIZED;
common tensor-valued graph with pure charts:   REALIZED LATER;
mixed cancellation for these fixed charts:     EXCLUDED LATER;
mixed cancellation for another scalar lift:    UNKNOWN;
full P7 restriction and global Krenn--Gu:       UNRESOLVED. (31)
```

See `P7_221_DIAGONAL_BLOCK_GLUING_AND_MIXED_WORD_BOUNDARY.md` for the later
pure-chart gluing theorem and its exact mixed coefficient `1/7`.  See
`P7_221_ARBITRARY_ALIGNMENT_DEGREE5_RECTANGLE_OBSTRUCTION.md` for the later
exclusion of every core alignment of these particular charts.

## Replay

```powershell
uv run --with sympy python verify_p7_221_common_terminal_block_scalar_hafnian_realizability.py
python audit_p7_221_common_terminal_block_scalar_hafnian_realizability.py
python -m py_compile verify_p7_221_common_terminal_block_scalar_hafnian_realizability.py audit_p7_221_common_terminal_block_scalar_hafnian_realizability.py
uv run --with ruff ruff check verify_p7_221_common_terminal_block_scalar_hafnian_realizability.py audit_p7_221_common_terminal_block_scalar_hafnian_realizability.py
```

The primary verifier checks the Wick/anchor identities, invariance under
`sigma`, equality of the three terminal blocks, all 186 prescribed
cofactors, and all six free values using exact SymPy arithmetic.  The
independent audit imports neither SymPy nor the primary verifier and repeats
the graph calculation in the exact quotient field
`Q[rho]/(rho^2-21)`.  Neither program searches supports, sweeps parameters,
or enumerates graph candidates.
