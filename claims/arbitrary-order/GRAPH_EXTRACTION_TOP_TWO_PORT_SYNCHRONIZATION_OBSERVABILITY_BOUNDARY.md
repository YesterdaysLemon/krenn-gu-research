# Top two-port synchronization is not observable without a companion depth

## Status

**Exact arbitrary-order counterboundary and extraction consequence.**  A
physical two-port residual cofactor has the form

```text
W_uv=h B_uv+a_u tensor b_v+b_u tensor a_v.             (1)
```

The last two terms are the synchronized two-row permanent channel.  The
first term is an arbitrary direct port edge.  Whenever `h!=0`, the map from
physical edge data to the top family `(W_uv)` is surjective: set
`B_uv=W_uv/h` and `a_u=b_u=0`.  Thus top two-port data alone satisfy no
universal polynomial equation and do not force synchronized factorization.

The concrete physical block

```text
W_01=I_3,       W_uv=0 otherwise                       (2)
```

cannot itself be the synchronized **two-row channel** given by the last two
terms of (1), because a sum of two rank-one `3 x 3` matrices has rank at most
two.  It is realized by the arbitrary direct term: both in the
two-residual direct sector with `h=1` and, at minimum residual order, by the
ordinary blocker edge itself.

The residual-relative response tower identifies the exact missing datum.
For two residual vertices, if the residual-absent family `M` and the
residual-present family `Z` are observed on the same principal-deletion
window, then, on every legal polarized port chart,

```text
Phi=Z/M=h+Q_K,
K_uv=z_uv-h m_uv=a_u b_v+b_u a_v.                     (3)
```

The corrected channel is therefore observable after one companion depth,
but not from `z_uv` alone.  For data coming from one physical graph it is
factorized by the same residual incidence rows.  Abstract scalar charts must
still be polarized compatibly before common covectors may be claimed.  At
four or more residual vertices the top permanental compound is independent
of the residual matrix `A`; it likewise cannot determine the lower
hafnian-cofactor layers.

Consequently the strict-support transfers to extracted `P_5` and one-port
`P_6` remain unconditional under their established extraction hypotheses.
The `P_7` bound `I+p_0+p_1>=24` remains conditional on a legal factorized
extraction (or on additional synchronized deletion data that actually
produce the required nonzero diagonal target).  It cannot be inferred from
the top surplus-two tensor merely by applying hafnian recursion.

This is a proof-route boundary, not a graph witness for the GHZ identity and
not a nonrestriction theorem.  The full top GHZ equations could impose
additional constraints not present in the abstract physical cofactor map.

## 1. The exact top cofactor map

Let `Q={q_0,q_1}` be two residual vertices contracted against fixed vectors.
For every port `u`, write

```text
a_u(z)=B_(u,q_0)(z,z_0),
b_u(z)=B_(u,q_1)(z,z_1),
h=B_(q_0,q_1)(z_0,z_1).                               (4)
```

The three perfect matchings on `{u,v,q_0,q_1}` give

```text
W_uv(z_u,z_v)
 =h B_uv(z_u,z_v)+a_u(z_u)b_v(z_v)+b_u(z_u)a_v(z_v). (5)
```

No sign, planarity, genericity, or division is involved in (5).

### Theorem 1 (top two-port surjectivity)

Fix nonzero `h`.  For arbitrary finite-dimensional port spaces `V_u`, the
polynomial map

```text
(B,a,b) |-> (hB_uv+a_u tensor b_v+b_u tensor a_v)_(u<v) (6)
```

is surjective onto

```text
product_(u<v) (V_u^* tensor V_v^*).                   (7)
```

Proof.  Given any target family `T_uv`, take `a_u=b_u=0` and
`B_uv=T_uv/h`.  Equation (5) then gives `W_uv=T_uv` for every pair.

### Corollary 2 (no top-only polynomial constraint)

No nonzero polynomial in the entries of `(W_uv)` vanishes on every physical
top two-port family with `h!=0`.

Proof.  By Theorem 1 the image is the whole affine target space.  A
polynomial vanishing there is the zero polynomial.

This is stronger than a dimension count and is unaffected by taking a
Zariski closure.

## 2. An exact nonsynchronized physical block

Take all port spaces to be `K^3` and prescribe (2).  It has an honest
two-residual realization:

```text
z_0=z_1=(1,1,1),
B_(q_0,q_1)(x,y)=x_0 y_0,          so h=1,
B_01=I_3,
B_(u,q_j)=0 for every u,j,
all other B_uv=0.                                      (8)
```

Then (5) is exactly (2).  This can be embedded in a legal root--blocker
slice: take fully supported root vectors, zero root--root edges, arbitrary
blocker-admissible root rows, and zero root--residual edges.  The simultaneous
kernel at each residual vertex is the whole local space, so the chosen
`z_j` are torus vectors and the residual vertices block no colour.

Suppose instead that the top block (2) were itself a synchronized two-row
channel.  At the pair `0,1` its matrix
would be

```text
g_(00) g_(11)^T+g_(10) g_(01)^T,                      (9)
```

a sum of two rank-one matrices.  Its rank is at most two, whereas
`rank I_3=3`.  Hence no synchronized two-row factorization exists.

At empty residual set `Q=empty`, the same boundary is even more immediate:
`haf(A[empty])=1` and the surplus-two cofactor is the direct blocker edge
`W_uv=B_uv`.  Thus the minimum-order five-root/seven-blocker top tensor also
has no automatic rank-two factorization.

The example does not satisfy or refute the full diagonal GHZ aggregate.  It
proves the narrower—and necessary—statement that synchronization is not a
formal consequence of physical matching recursion or top cofactor data.

## 3. One companion depth recovers the two residual rows

Let `U` be a transversal scalar port chart and work in its square-zero
algebra.  Put

```text
M=exp(Q_B),
Q_K=sum_(u<v) (a_u b_v+b_u a_v)x_u x_v.              (10)
```

The exact two-residual dual-Wick identity is

```text
Z=M(h+Q_K).                                           (11)
```

Since `M_empty=1`, the constant response determines `h=Z_empty`.  Division
is finite square-zero convolution, so

```text
Phi=Z/M=h+Q_K.                                        (12)
```

At pair degree this reads

```text
z_uv=h m_uv+K_uv,
K_uv=z_uv-hm_uv=a_u b_v+b_u a_v.                     (13)
```

Thus the corrected channel is not an extra hidden quantity once the paired
families `(M,Z)` are legally exposed on one common deletion window.  In an
actual physical graph it is factorized by the original common rows `a,b`.
For abstract response data, however, one must expose compatible polarized
copies of all local port coordinates (or prove the corresponding common
rank-two block completion); a single scalar transversal does not manufacture
global covectors.  The word "paired" is also essential: knowing only `z_uv`
leaves the decomposition

```text
z_uv=hB_uv+K_uv                                       (14)
```

completely nonidentifiable by Theorem 1.

The four-port companion equation is the tangent-Wick identity

```text
n_ijkl
 =n_ij m_kl+m_ij n_kl
  +n_ik m_jl+m_ik n_jl
  +n_il m_jk+m_il n_jk,                              (15)
```

where `n=Z-hM`.  Equation (15) is a test that the same corrected pair family
persists to the next deletion depth.  It is unavailable from a single top
surplus tensor.

## 4. Higher residual order has the same observability gap

For an even residual set `Q` of size `q`, the relative response is

```text
[x_S]Phi_(A,R)
 =sum_(T subset Q, |T|=|S|)
    haf(A[Q minus T]) per(R_(T,S)).                   (16)
```

At top degree `|S|=q`, this reduces to

```text
[x_S]Phi=per(R_(Q,S)),                                (17)
```

which is independent of `A`.  Therefore top degree cannot determine the
constant hafnian or any lower cofactor layer.

For an explicit `q=4` witness, take four scalar ports and `R=I_4`.  Compare

```text
A^(0)=0,
A^(1)_12=A^(1)_34=1,       all other entries zero.    (18)
```

Both models have top coefficient `per(I_4)=1`.  The first has constant and
quadratic relative response zero.  The second has `haf(A^(1))=1` and
nonzero quadratic cofactors at the complementary pairs `12` and `34`.
Thus even exact top permanental data do not synchronize the residual tower.

## 5. Exact P5/P6/P7 consequence

Combining this boundary with the strict permanent support theorem gives the
following status table.

```text
five roots/five tight blockers:
    extracted P_5 support I >=18;                     UNCONDITIONAL

r roots/(r+1) blockers/one residual port:
    extracted P_(r+1) support I+p >=3r+6;             UNCONDITIONAL
    in particular r=5 gives P_6 support >=21;

r roots/(r+2) blockers/two ports:
    I+p_0+p_1 >=3r+9, hence P_7 support >=24 at r=5;  CONDITIONAL
```

The last line is unconditional only after a legal argument has replaced the
whole surplus-two tensor by two common port rows with a nonzero diagonal
target.  Examples include the exact two-residual torus-zero branch `h=0`.
Equations (12)--(15) show another possible route if a common companion depth
is exposed and its corrected target remains the required diagonal.  Neither
condition follows from top data alone.

In particular, applying a rank-two port count directly to `W_uv` on the
`h!=0` or empty-residual branch is invalid: it silently discards the
arbitrary direct term `hB_uv`.

## Scope wall

Proved:

- surjectivity of the physical top two-port map for `h!=0`;
- an exact legal rank-three top block with no synchronized factorization;
- exact recovery of the corrected channel from paired depths, with physical
  common-row factorization on compatible polarized charts;
- top-degree nonobservability of lower residual layers for every `q>=4`;
- no new unconditional `P_7` support transfer from top data alone.

Not proved:

- that a full GHZ top aggregate can contain the rank-three example (2);
- that the full GHZ equations fail to force synchronization by some other
  argument;
- that an arbitrary hypothetical witness exposes the paired deletion window
  needed in (11)--(15);
- that the corrected paired-depth target has three nonzero diagonal colours;
- an unconditional `P_7 -> Delta_3` extraction or nonrestriction;
- the Krenn--Gu conjecture.

The exact boundary is

```text
top two-port physical image at h!=0:          FULL AFFINE SPACE;
top-only synchronized factorization:         FALSE IN GENERAL;
paired-depth corrected q=2 physical channel: SYNCHRONIZED EXACTLY;
top q>=4 compound determines lower tower:    FALSE;
P5/P6 strict-support transfers:              UNCONDITIONAL AS BEFORE;
P7 strict-support transfer from top data:    CONDITIONAL;
global Krenn--Gu:                            UNRESOLVED.               (19)
```

## Replay

```powershell
uv run --with sympy python claims/arbitrary-order/verify_graph_extraction_top_two_port_synchronization_observability_boundary.py
python claims/arbitrary-order/audit_graph_extraction_top_two_port_synchronization_observability_boundary.py
python -m py_compile claims/arbitrary-order/verify_graph_extraction_top_two_port_synchronization_observability_boundary.py claims/arbitrary-order/audit_graph_extraction_top_two_port_synchronization_observability_boundary.py
uv run --with ruff ruff check claims/arbitrary-order/verify_graph_extraction_top_two_port_synchronization_observability_boundary.py claims/arbitrary-order/audit_graph_extraction_top_two_port_synchronization_observability_boundary.py
```

The primary verifier checks generic top surjectivity, the symbolic
rank-two determinant identity, exact dual-Wick recovery through four ports,
the `q=4` equal-top/different-lower witness, and the `P_5/P_6/P_7` support
table.  The independent audit uses a no-import polynomial dictionary,
square-zero convolution, and fixed hafnian/permanent recurrences.  Neither
replay enumerates supports, colour words, or candidate graphs.
