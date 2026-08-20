"""Standalone recursive-permanent audit of the GLD54 reverse-disjoint closure."""

from __future__ import annotations
from itertools import combinations
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOTS=tuple(range(4)); EDGES=tuple(combinations(ROOTS,2)); EDGE_INDEX={e:i for i,e in enumerate(EDGES)}
U,V,W=sp.symbols("u v w")
CASES={
 "u_minus":((("1000","0100"),("0100","0100"),("0010","0001"),("0002","0002"),("0001","0001"),("0011","0011"),("0010","0010"),("0011","0000"),("0000","0011"),("0200","0200"),("0110","0101"),("0101","0101"),("0100","1101"),("0000","1001")),2*V**2*W*(V-1)*(W-1)*(W+1)*(2*W-1)),
 "w_minus":((("1000","0100"),("0010","0001"),("0001","0001"),("0002","0002"),("0100","0100"),("0011","0000"),("0200","0200"),("0110","0000"),("0101","0000"),("0110","0101"),("0010","0111"),("0000","0110")),4*U*V*(U-1)*(U+1)*(U*V+1)),
 "w_half":((("1000","0100"),("0010","0001"),("0002","0002"),("0001","0001"),("0100","0100"),("0012","0012"),("0010","0010"),("0011","0000"),("0200","0200"),("0110","0000"),("0101","0000"),("0110","0101"),("0101","0101"),("0000","0101")),4*U*V*(U-1)*(U+1)*(U*V+1)),
 "product":((("1000","0100"),("0010","0001"),("0001","0001"),("0100","0100"),("0010","0010"),("0101","0000"),("0102","0102"),("0200","0200"),("0110","0101"),("0101","0101"),("0110","0000")),2*U*W*(U-1)*(W-1)),
 "both_minus":((("1000","0100"),("0100","0100"),("0010","0001"),("0001","0001"),("0002","0002"),("0011","0000"),("0200","0200"),("0110","0101"),("0101","0101")),4*V*(V-1)),
 "minus_half":((("1000","0100"),("0100","0100"),("0010","0001"),("0002","0002"),("0001","0001"),("0012","0012"),("0010","0010"),("0011","0000"),("0200","0200"),("0110","0101"),("0101","0101"),("0100","1101"),("0000","1001")),4*V**2*(V-1)),
}
def word(v): return tuple(map(int,v))
def p_index(q,r,c): return (0 if q==0 else 12)+3*r+c
def w_index(a,b,ca,cb):
 if a>b: a,b,ca,cb=b,a,cb,ca
 return 24+9*EDGE_INDEX[(a,b)]+3*ca+cb
def amplitudes(case):
 first=(-1,sp.Rational(1,2)) if case in ("u_minus","both_minus","minus_half") else (U,U/(U-1))
 second=(-1/U,1/(U+1)) if case=="product" else (V,V/(V-1))
 if case in ("w_minus","both_minus"): third=(-1,sp.Rational(1,2))
 elif case in ("w_half","minus_half"): third=(sp.Rational(1,2),-1)
 else: third=(W,W/(W-1))
 return {(0,0,1):first[0],(1,1,0):first[1],(0,1,0):second[0],(1,0,1):second[1],(0,2,3):third[0],(1,3,2):third[1]}
def cross(c,r,p,case):
 if r==p: return sp.Integer(1)
 return amplitudes(case).get((c,r,p),sp.Integer(0))
def permanent(rows,ports,rw,pw,case):
 if not rows: return sp.Integer(1)
 first,total=rows[0],0
 for i,p in enumerate(ports):
  if rw[first]!=pw[p]: continue
  e=cross(pw[p],first,p,case)
  if e: total += e*permanent(rows[1:],ports[:i]+ports[i+1:],rw,pw,case)
 return sp.expand(total)
def add(row,index,value):
 value=sp.expand(row.get(index,0)+value)
 if value: row[index]=value
 else: row.pop(index,None)
def equation(pw,rw,case):
 x,y=(1,1,0),(1,-1,0); row={}; rhs=-permanent(ROOTS,ROOTS,rw,pw,case)
 for op in ROOTS:
  ports=tuple(p for p in ROOTS if p!=op)
  for mr in ROOTS:
   roots=tuple(r for r in ROOTS if r!=mr); minor=permanent(roots,ports,rw,pw,case); c=pw[op]
   add(row,p_index(0,mr,rw[mr]),y[c]*minor); add(row,p_index(1,mr,rw[mr]),x[c]*minor)
 for lp,rp in EDGES:
  lc,rc=pw[lp],pw[rp]; corrected=x[lc]*y[rc]+y[lc]*x[rc]; ports=tuple(p for p in ROOTS if p not in (lp,rp))
  for lr,rr in EDGES:
   roots=tuple(r for r in ROOTS if r not in (lr,rr)); minor=permanent(roots,ports,rw,pw,case)
   add(row,w_index(lr,rr,rw[lr],rw[rr]),corrected*minor)
 if len(set(pw))==1 and rw==pw: add(row,78+pw[0],-1)
 return row,sp.expand(rhs)
def main():
 for case,(keys,expected) in CASES.items():
  matrix=[]; rhs=[]
  for pw,rw in keys:
   row,value=equation(word(pw),word(rw),case); matrix.append([sp.factor(row.get(i,0)) for i in range(81)]); rhs.append(sp.factor(value))
  ns=DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix(); assert ns.rows==1,case
  vector=[sp.factor(ns[0,i]) for i in range(ns.cols)]; detector=sp.factor(sum(a*b for a,b in zip(vector,rhs,strict=True))); assert detector!=0
  weights=[sp.factor(a/detector) for a in vector]; assert sp.factor(sum(a*b for a,b in zip(weights,rhs,strict=True)))==1
  denominator=sp.factor(sp.lcm([sp.denom(sp.cancel(a)) for a in weights])); assert denominator==sp.factor(expected),(case,denominator)
 print("PASS: standalone recursive-permanent audit derives all six GLD54 contradictions")
if __name__=="__main__": main()
