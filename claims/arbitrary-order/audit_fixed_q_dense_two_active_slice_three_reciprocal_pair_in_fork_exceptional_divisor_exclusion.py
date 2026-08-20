"""Standalone recursive-permanent audit of the GLD57 in-fork closure."""

from __future__ import annotations
from itertools import combinations
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOTS=tuple(range(4)); EDGES=tuple(combinations(ROOTS,2)); EDGE_INDEX={e:i for i,e in enumerate(EDGES)}
U,V,W=sp.symbols("u v w")
def rows(value): return tuple(tuple(item.split(":")) for item in value.split(","))
CASES={
 "u_minus":(rows("1000:0100,0001:0001,0001:0100,0010:0010,0001:0010,0100:0010,0002:0002,0011:0011,0000:0011,0100:0100,0011:0110,0000:0110,0101:0011,0101:0000,0101:0101,0100:0111"),2*V**3*W**2*(W-1)*(W+2)),
 "difference":(rows("1001:0101,0001:0100,0001:0001,0002:0002,0011:0011,0010:0010,0000:0011,0011:0110,0000:0110,0001:0010,0100:0010,0100:0100,0011:0000,0101:0011,0101:0000,0000:0101,0101:0101"),2*U**2*V**3*(U-2)*(U-1)**3*(U+1)*(U*V+V+1)),
 "sum":(rows("1000:0100,0001:0100,0010:0010,0000:0011,0011:0110,0001:0111,0001:0010,0100:0010,0002:0002,0011:0011,0001:0001,0100:0100,0011:0000,0101:0011,0101:0000,0101:0101,0000:0101"),4*U**2*V**3*(U+1)**2*(U+2)*(U*V+V+1)),
 "product":(rows("1000:0100,0001:0100,0001:0001,0002:0002,0011:0011,0001:0111,0000:0110,0011:0110,0010:0010,0001:0010,0100:0010,0100:0100,0011:0000,0101:0011,0101:0000,0101:0101,0000:0101"),2*U*W**2*(U+1)*(W-1)*(U-W-1)*(U+W+1)),
 "minus_difference":(rows("1001:0101,0001:0001,0001:0100,0010:0010,0001:0010,0002:0002,0100:0100,0100:0010,0011:0011,0000:0011,0011:0110,0000:0110,0101:0011,0101:0000,0100:0111,0101:0101"),8*V**3),
 "difference_product":(rows("1001:0101,0001:0100,0001:0001,0002:0002,0011:0011,0001:0111,0000:0110,0011:0110,0010:0010,0001:0010,0100:0010,0100:0100,0011:0000,0101:0011,0101:0000,0000:0101,0101:0101"),4*U**2*(U-2)*(U-1)**3*(U+1)),
 "sum_product":(rows("1000:0100,0001:0100,0002:0112,0011:0110,0010:0010,0001:0010,0100:0010,0002:0002,0011:0011,0001:0001,0001:0111,0100:0100,0011:0000,0101:0011,0101:0000,0101:0101,0000:0101"),4*U**2*(U+1)**2*(U+2)),
}
def word(v):return tuple(map(int,v))
def p_index(q,r,c):return 12*q+3*r+c
def w_index(a,b,ca,cb):
 if a>b:a,b,ca,cb=b,a,cb,ca
 return 24+9*EDGE_INDEX[(a,b)]+3*ca+cb
def amplitudes(case):
 first=(-1,sp.Rational(1,2)) if case in ("u_minus","minus_difference") else (U,U/(U-1))
 second=(-1/(U+1),1/(U+2)) if case in ("product","difference_product","sum_product") else (V,V/(V-1))
 if case in ("difference","difference_product"):third=(U-1,(U-1)/(U-2))
 elif case in ("sum","sum_product"):third=(-U-1,(U+1)/(U+2))
 elif case=="minus_difference":third=(-2,sp.Rational(2,3))
 else:third=(W,W/(W-1))
 return {(0,0,1):first[0],(1,1,0):first[1],(0,1,2):second[0],(1,2,1):second[1],(0,3,1):third[0],(1,1,3):third[1]}
def cross(c,r,p,case):
 if r==p:return sp.Integer(1)
 return amplitudes(case).get((c,r,p),sp.Integer(0))
def permanent(rs,ps,rw,pw,case):
 if not rs:return sp.Integer(1)
 first,total=rs[0],0
 for i,p in enumerate(ps):
  if rw[first]!=pw[p]:continue
  e=cross(pw[p],first,p,case)
  if e:total+=e*permanent(rs[1:],ps[:i]+ps[i+1:],rw,pw,case)
 return sp.expand(total)
def add(row,index,value):
 value=sp.expand(row.get(index,0)+value)
 if value:row[index]=value
 else:row.pop(index,None)
def equation(pw,rw,case):
 x,y=(1,1,0),(1,-1,0); row={}; rhs=-permanent(ROOTS,ROOTS,rw,pw,case)
 for op in ROOTS:
  ps=tuple(p for p in ROOTS if p!=op)
  for mr in ROOTS:
   rs=tuple(r for r in ROOTS if r!=mr); minor=permanent(rs,ps,rw,pw,case); c=pw[op]
   add(row,p_index(0,mr,rw[mr]),y[c]*minor); add(row,p_index(1,mr,rw[mr]),x[c]*minor)
 for lp,rp in EDGES:
  lc,rc=pw[lp],pw[rp]; corrected=x[lc]*y[rc]+y[lc]*x[rc]; ps=tuple(p for p in ROOTS if p not in (lp,rp))
  for lr,rr in EDGES:
   rs=tuple(r for r in ROOTS if r not in (lr,rr)); minor=permanent(rs,ps,rw,pw,case); add(row,w_index(lr,rr,rw[lr],rw[rr]),corrected*minor)
 if len(set(pw))==1 and rw==pw:add(row,78+pw[0],-1)
 return row,sp.expand(rhs)
def main():
 for case,(keys,expected) in reversed(tuple(CASES.items())):
  matrix=[]; rhs=[]
  for pw,rw in reversed(keys):
   row,value=equation(word(pw),word(rw),case); matrix.append([sp.factor(row.get(i,0)) for i in reversed(range(81))]); rhs.append(sp.factor(value))
  ns=DomainMatrix.from_Matrix(sp.Matrix(matrix).T).nullspace().to_Matrix(); assert ns.rows==1,case
  vector=[sp.factor(ns[0,i]) for i in range(ns.cols)]; detector=sp.factor(sum(a*b for a,b in zip(vector,rhs,strict=True))); assert detector!=0,case
  weights=[sp.factor(a/detector) for a in vector]; denominator=sp.factor(sp.lcm([sp.denom(sp.cancel(a)) for a in weights])); assert denominator==sp.factor(expected),(case,denominator)
 print("PASS: standalone recursive-permanent audit derives all seven GLD57 contradictions")
if __name__=="__main__":main()
