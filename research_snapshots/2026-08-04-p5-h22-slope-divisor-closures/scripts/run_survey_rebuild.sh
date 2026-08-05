#!/bin/sh
cd "$(dirname "$0")" || exit 1
python3 explore_p5_h22_disjoint_mixed_star_slope_divisors_modular.py \
  p11_23_r2 p11_23_r1 p11_23_r10 p11_23_r0 \
  p11_01_r1 p11_01_r10 p11_01_r0 \
  p13_23_r1 p13_23_r2 p13_23_r12
python3 explore_coupled_divisor_modular.py
