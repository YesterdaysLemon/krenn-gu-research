"""All-row recursive-permanent replay of the GLD58 out-fork transfer."""

from __future__ import annotations
from itertools import product
import sympy as sp
from verify_fixed_q_dense_two_active_slice_three_reciprocal_pair_in_star_colour_exchange_exclusion import (
    PARAMETER_EXCHANGE,U,V,W,coordinate_sign,equation,mapped_index,swap_word,
)

IN_FORK=((0,1),(1,2),(3,1)); REVERSE_OUT_FORK=((1,0),(2,1),(1,3))
O5={(0,1),(0,2),(3,0)}; POSITION={0:1,1:0,2:3,3:2}
def main():
 assert {(POSITION[a],POSITION[b]) for a,b in REVERSE_OUT_FORK}==O5
 for value in (U,V,W):
  exchanged=value/(value-1); assert sp.cancel(exchanged/(exchanged-1)-value)==0
 words=tuple(product(range(3),repeat=4))
 for pw,rw in product(words,repeat=2):
  source_row,source_rhs=equation(pw,rw,IN_FORK)
  target_row,target_rhs=equation(swap_word(pw),swap_word(rw),REVERSE_OUT_FORK)
  target_row={i:sp.cancel(v.xreplace(PARAMETER_EXCHANGE)) for i,v in target_row.items()}; target_rhs=sp.cancel(target_rhs.xreplace(PARAMETER_EXCHANGE))
  assert sp.cancel(target_rhs-source_rhs)==0,(pw,rw,"rhs")
  for index in range(81):
   assert sp.cancel(target_row.get(mapped_index(index),0)-coordinate_sign(index)*source_row.get(index,0))==0,(pw,rw,index)
 print("PASS: all 6561 complete rows transfer GLD57 O11 to GLD58 O5")
if __name__=="__main__":main()
