# A five-equation Laurent core on the exact-two-partial P5 boundary

## Status

This is an exact algebraic obstruction for one labelled support stratum in
the `C4+C6` exact-two-partial boundary.  It is not yet a proof for every
support in that boundary and does not resolve the global Krenn--Gu
conjecture.

The support is

```text
66411
77142
21774
42277
14727
```

where each digit is a three-bit support mask.  Its full support-only
coefficient ideal has 205 distinct mixed equations.  Deletion
minimization found that the five mixed target words

```text
22001, 22002, 22200, 22201, 22202
```

already contradict the required nonzero entries.

## Abstract core

Work over a field of characteristic different from two.  Let

```text
A = a+b
B = 1+A k
C = 1+A h
R = r+q p
```

and define

```text
F1 = B(y+p t) + p C
F2 = B v + p(k+h+l C)
F3 = A(x+s R) + a R + b p
F4 = A(y+p t+R)
F5 = p+R+A(v+l R).
```

There is no common zero of `F1,...,F5` with `a`, `b`, and `p` all
nonzero.

Indeed, put

```text
D = p C - B R
H = A p(k+h) - B(p+R).
```

Direct expansion gives

```text
A F1 - B F4 = A D,
A F2 - B F5 = H + l A D,
D - H = 2p,
a F5 - F3 = 2ap + A(a(v+lR)-x-sR-p).
```

At a common zero, the first two identities give `A D=0` and `H=0`.
If `A` is nonzero, then `D=0`, so the third identity gives `2p=0`.
If `A=0`, the fourth identity gives `2ap=0`.  Both cases contradict
the nonzero hypotheses.

## Connection to the P5 coefficient system

Under the deterministic spanning-tree gauge used by the certificate
generator, set

```text
a=u3,  b=u0,  p=u15, h=u8,  k=u6,  l=u19,
q=u10, r=u11, s=u18, t=u20, v=u23, x=u21, y=u22.
```

The five displayed `F` polynomials expand exactly to mixed equations
180, 181, 197, 198, and 199 of the independently regenerated
205-equation system.  The required exact support makes `u0`, `u3`, and
`u15` nonzero.

Run:

```text
python claims/p5/frontier/verify_p5_five_equation_laurent_core.py
```

The verifier regenerates the full support system, checks the five
coefficient words and polynomial expansions, and checks all four
certificate identities by exact sparse-polynomial arithmetic.
