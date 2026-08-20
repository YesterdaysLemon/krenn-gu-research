"""Standalone matching-topology audit of the GLD58 out-fork transfer."""

from __future__ import annotations
from collections import Counter
from functools import lru_cache
import sympy as sp

ROOTS=tuple(range(4)); Q0,Q1=4,5; PORTS=tuple(range(6,10)); VERTICES=ROOTS+(Q0,Q1)+PORTS; T=sp.symbols("t")
def swap(c):return 1-c if c in (0,1) else c
def mapped(index):
 if index<24:
  block,offset=divmod(index,12); root,c=divmod(offset,3); return 12*block+3*root+swap(c)
 if index<78:
  offset=index-24; edge,colours=divmod(offset,9); left,right=divmod(colours,3); return 24+9*edge+3*swap(left)+swap(right)
 return 78+swap(index-78)
def sign(index):return -1 if index<12 or 24<=index<78 else 1
@lru_cache(maxsize=None)
def matchings(vertices):
 if not vertices:return ((),)
 first,answer=vertices[0],[]
 for i in range(1,len(vertices)):
  second=vertices[i]; rest=vertices[1:i]+vertices[i+1:]
  for tail in matchings(rest):answer.append(((first,second),)+tail)
 return tuple(answer)
def topology(matching):
 variables=[]; y_edges=0
 for ra,rb in matching:
  a,b=sorted((ra,rb))
  if a in PORTS and b in PORTS:return "zero_port_port"
  if a in ROOTS and b in ROOTS:variables.append("w")
  elif a in ROOTS and b==Q0:variables.append("p0")
  elif a in ROOTS and b==Q1:variables.append("p1")
  elif a==Q1 and b in PORTS:y_edges+=1
 if len(variables)>1:return "discard_multi_variable"
 variable=variables[0] if variables else "constant"; return f"{variable}_y{y_edges}"
def main():
 exchanged=T/(T-1); assert sp.cancel(exchanged/(exchanged-1)-T)==0
 x,y=(1,1,0),(1,-1,0)
 for c in range(3):assert x[swap(c)]==x[c] and y[swap(c)]==-y[c]
 assert len({mapped(i) for i in range(81)})==81
 for i in range(81):assert mapped(mapped(i))==i and sign(mapped(i))==sign(i)
 all_matchings=matchings(VERTICES); assert len(all_matchings)==945
 counts=Counter(topology(m) for m in all_matchings); assert counts=={"zero_port_port":585,"constant_y0":24,"p0_y1":96,"p1_y0":96,"w_y1":144}
 expected={"constant":1,"p0":-1,"p1":1,"w":-1}
 for kind in counts:
  if kind.startswith("zero_") or kind.startswith("discard_"):continue
  variable,y_count=kind.split("_y"); assert expected[variable]==(-1)**int(y_count)
 source={(0,1),(1,2),(3,1)}; reverse={(b,a) for a,b in source}; permutation={0:1,1:0,2:3,3:2}
 assert {(permutation[a],permutation[b]) for a,b in reverse}=={(0,1),(0,2),(3,0)}
 print("PASS: 945 matching topologies independently prove the GLD58 transfer")
if __name__=="__main__":main()
