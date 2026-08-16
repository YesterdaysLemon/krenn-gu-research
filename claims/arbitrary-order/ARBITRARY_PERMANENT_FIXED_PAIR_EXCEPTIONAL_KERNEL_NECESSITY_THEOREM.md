# Arbitrary permanent fixed-pair exceptional-kernel necessity theorem

## Status

This note proves an exact characteristic-zero reduction inside the
simultaneous projection-drop residual for the fixed equality-five pair of
`ARBITRARY_PERMANENT_FIXED_PAIR_TWO_SIDED_PROJECTION_DROP_THEOREM.md`.
Every rank-two local projection has its kernel on one of three explicit
ambient lines.  In particular, the generic kernel directions localized in
`ARBITRARY_PERMANENT_FIXED_PAIR_KERNEL_SUPPORT_BOUNDARY_THEOREM.md` cannot
occur in an exact `P_6 -> Delta_3` extension.

The result is a necessary boundary, not an existence theorem.  It does not
classify the remaining exceptional-line incidences, does not exclude the
fixed pair, and does not prove unrestricted permanent nonrestriction.  The
global Krenn--Gu conjecture remains **UNRESOLVED**.

## 1. Fixed pair and predecessor boundary

Let `K` be a field of characteristic zero and work in

```text
Z_6=K[x_0,...,x_5]/(x_0^2,...,x_5^2).
```

For the fixed equality-five pair, the two projection maps are

```text
Phi_1=(x_1,x_4,x_5,x_3-x_2-x_0),
Phi_2=(x_0,x_4,x_5,x_3-x_2-x_1).                       (1)
```

Their ambient kernels are parametrized by

```text
p_1(a,b)=(a,0,b,a+b,0,0),
p_2(a,b)=(0,a,b,a+b,0,0).                              (2)
```

Let ordered independent triples

```text
(y_(t,0),y_(t,1),y_(t,2)),                 t=2,3,4,5,
```

span the local planes `L_t`.  Assume the exact fixed-pair target equations

```text
T_(m_1)=T_(m_2)=0,
T_(d_c)=lambda_c e_c^* tensor e_c^* tensor e_c^*
                         tensor e_c^*,
lambda_c!=0,                                      c=0,1,2. (3)
```

For a nonzero `p in L_t`, write

```text
p=alpha_0 y_(t,0)+alpha_1 y_(t,1)+alpha_2 y_(t,2).     (4)
```

The kernel-support predecessor proves the following facts.

1. Every restricted projection has rank at least two.
2. If `p_k(a,b)` lies in `L_t` and `a b (a+b)!=0`, then exactly one
   coefficient in (4) is nonzero.
3. The two-sided projection-drop predecessor gives at least one rank-two
   mode in each projection family.

The new step excludes the generic case in item 2.

## 2. A one-diagonal obstruction

Let

```text
W=R direct-sum A,             dim R=4, dim A=2,
```

and let `J` be a nondegenerate symmetric bilinear form on `A`.  Write
`y=(r(y),a(y))` and define

```text
C(y,z,w)=r(y)J(a(z),a(w))+r(z)J(a(y),a(w))
                         +r(w)J(a(y),a(z)).             (5)
```

### Lemma 1 (one surviving diagonal is impossible)

For three modes `s,u,v`, let each ordered triple

```text
(y_(q,0),y_(q,1),y_(q,2)),                 q in {s,u,v},
```

be linearly independent in `W`.  It is impossible that

```text
C(y_(s,i),y_(u,j),y_(v,l))=0 unless i=j=l=0,
C(y_(s,0),y_(u,0),y_(v,0))!=0.                         (6)
```

### Proof

Fix two modes, say `s,u`, and labels `(i,j)!=(0,0)`.  The linear map

```text
K_(i,j):W -> R,
w |-> C(y_(s,i),y_(u,j),w)                             (7)
```

kills the three-dimensional space `L_v`.  Hence its rank is at most three.
On the four-dimensional summand `R`, however,

```text
K_(i,j)(r,0)=J(a(y_(s,i)),a(y_(u,j))) r.                (8)
```

If the scalar in (8) were nonzero, the rank would be at least four.
Therefore

```text
J(a(y_(q,i)),a(y_(q',j)))=0
```

for distinct modes `q,q'` whenever `(i,j)!=(0,0)`.  The argument applies
after any permutation of the three modes.

The nonzero value in (6) is a sum of three `R`-vectors multiplied by
pairings of the three zero-labelled `A`-vectors.  At least one pairing is
nonzero.  After permuting modes, assume

```text
J(a(y_(s,0)),a(y_(u,0)))!=0.                           (9)
```

For `l=1,2`, the two cross pairings involving `a(y_(v,l))` vanish by
(8).  Expanding the zero value `C(y_(s,0),y_(u,0),y_(v,l))` therefore gives

```text
r(y_(v,l)) J(a(y_(s,0)),a(y_(u,0)))=0.
```

By (9), `r(y_(v,1))=r(y_(v,2))=0`.  Thus `y_(v,1)` and `y_(v,2)` lie in
the two-space `A`.  Both are also orthogonal to the nonzero vector
`a(y_(s,0))`, so both lie on its one-dimensional orthogonal-complement
line.  They are dependent, contradicting independence of the local triple.
This proves the lemma.

## 3. Excluding generic kernel directions

Remove a mode `t` containing a generic kernel vector `p_k(a,b)` with

```text
a b (a+b)!=0.                                          (10)
```

As in the kernel-support predecessor, decompose the ambient six-space as

```text
R=K^{\{0,1,2,3\}},             A=K^{\{4,5\}},
J((s_4,s_5),(t_4,t_5))=s_4t_5+s_5t_4.                  (11)
```

The four nonzero-channel residual covectors obtained by contracting the
five complementary quartics with `p_k(a,b)` have determinant

```text
8 a^2 b(a+b).                                          (12)
```

They therefore form a basis of `R^*`.  The two mixed target equations and
the three diagonal target equations determine the tensor (5) on the three
remaining local colour bases:

```text
C(y_(s,i),y_(u,j),y_(v,l))=0               unless i=j=l,
C(y_(s,e),y_(u,e),y_(v,e))!=0
                                      iff alpha_e!=0.   (13)
```

The predecessor proves that under (10), precisely one `alpha_e` is
nonzero.  Relabel that colour as zero.  Equation (13) is then exactly the
configuration excluded by Lemma 1.  Hence no generic kernel direction can
lie in any local plane of an exact extension.

## 4. Exceptional-line conclusion

For every mode `t` and family `k`,

```text
0!=L_t intersect ker(Phi_k)
   => its unique projective kernel direction is one of
      p_k(0,1), p_k(1,0), p_k(1,-1).                   (14)
```

Equivalently, every rank-two restricted projection has its kernel on one
of the three lines

```text
K p_k(0,1),          K p_k(1,0),          K p_k(1,-1). (15)
```

Combining (14) with the two-sided predecessor gives the finite residual
boundary

```text
some L_t contains one of the three exceptional Phi_1-kernel lines,
some L_u contains one of the three exceptional Phi_2-kernel lines.       (16)
```

The modes `t,u` may coincide.  The theorem does not assert that every
exceptional line is realizable, nor that its local support has size two.

## 5. Exact scope and replay

```text
fixed pair, generic local kernel directions:              EXCLUDED;
fixed pair, every low kernel direction exceptional:       PROVED;
exceptional-line incidence classification/exclusion:      OPEN;
unrestricted P_6 -> Delta_3:                              UNKNOWN;
global Krenn--Gu conjecture:                              UNRESOLVED.
```

Replay the exact identity checks with

```powershell
python claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
python claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
python -m py_compile claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
python -m ruff check claims/arbitrary-order/verify_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py claims/arbitrary-order/audit_arbitrary_permanent_fixed_pair_exceptional_kernel_necessity.py
```

The primary verifier symbolically reconstructs the two ambient kernels,
the contraction determinants, the rank-four scalar-identity gate, and the
one-dimensional common-orthogonal-space contradiction.  The independent
audit uses only Python's standard library: it performs square-free
contractions directly, checks the determinant over exact rational
arithmetic, and exhausts the two-dimensional orthogonality core over two
odd finite fields.  The finite-field runs audit displayed algebra only;
the proof above is the characteristic-zero argument.
