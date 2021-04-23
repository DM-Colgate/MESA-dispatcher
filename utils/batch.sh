#!/bin/bash
# example of a script to launch a batch of MESA runs on the cluster at once


echo "Dispatching feral hogs... please prepare for deallocation."

#######################################
### N
#######################################
# Nq: M_* = 1d1 -> 1d3, m_chi = 1d7, rho_chi = 1d16, and 16 threads
deploy Nq MESA-DM 1d1 1d7 1d16 16
deploy Nq MESA-DM 1d2 1d7 1d16 16
deploy Nq MESA-DM 3d2 1d7 1d16 16
deploy Nq MESA-DM 5d2 1d7 1d16 16
deploy Nq MESA-DM 1d3 1d7 1d16 16

# Nr: M_* = 1d1 -> 1d3, m_chi = 1d7, rho_chi = 1d15, and 16 threads
deploy Nr MESA-DM 1d1 1d7 1d15 16
deploy Nr MESA-DM 1d2 1d7 1d15 16
deploy Nr MESA-DM 3d2 1d7 1d15 16
deploy Nr MESA-DM 5d2 1d7 1d15 16
deploy Nr MESA-DM 1d3 1d7 1d15 16

# Ns: M_* = 1d1 -> 1d3, m_chi = 1d7, rho_chi = 1d14, and 16 threads
deploy Ns MESA-DM 1d1 1d7 1d14 16
deploy Ns MESA-DM 1d2 1d7 1d14 16
deploy Ns MESA-DM 3d2 1d7 1d14 16
deploy Ns MESA-DM 5d2 1d7 1d14 16
deploy Ns MESA-DM 1d3 1d7 1d14 16

# Nt: M_* = 1d1 -> 1d3, m_chi = 1d7, rho_chi = 1d14, and 16 threads
deploy Nt MESA-DM 1d1 1d7 1d13 16
deploy Nt MESA-DM 1d2 1d7 1d13 16
deploy Nt MESA-DM 3d2 1d7 1d13 16
deploy Nt MESA-DM 5d2 1d7 1d13 16
deploy Nt MESA-DM 1d3 1d7 1d13 16

#######################################
### Q
#######################################
# Qn: M_* = 1d1 -> 1d3, m_chi = 1d10, rho_chi = 1d14, and 16 threads
deploy Qn MESA-DM 1d1 1d10 1d14 16
deploy Qn MESA-DM 1d2 1d10 1d14 16
deploy Qn MESA-DM 3d2 1d10 1d14 16
deploy Qn MESA-DM 5d2 1d10 1d14 16
deploy Qn MESA-DM 1d3 1d10 1d14 16

# Qo: M_* = 1d1 -> 1d3, m_chi = 1d10, rho_chi = 1d13, and 16 threads
deploy Qo MESA-DM 1d1 1d10 1d13 16
deploy Qo MESA-DM 1d2 1d10 1d13 16
deploy Qo MESA-DM 3d2 1d10 1d13 16
deploy Qo MESA-DM 5d2 1d10 1d13 16
deploy Qo MESA-DM 1d3 1d10 1d13 16

# Qp: M_* = 1d1 -> 1d3, m_chi = 1d10, rho_chi = 1d12, and 16 threads
deploy Qp MESA-DM 1d1 1d10 1d12 16
deploy Qp MESA-DM 1d2 1d10 1d12 16
deploy Qp MESA-DM 3d2 1d10 1d12 16
deploy Qp MESA-DM 5d2 1d10 1d12 16
deploy Qp MESA-DM 1d3 1d10 1d12 16

# Qq: M_* = 1d1 -> 1d3, m_chi = 1d10, rho_chi = 1d11, and 16 threads
deploy Qq MESA-DM 1d1 1d10 1d11 16
deploy Qq MESA-DM 1d2 1d10 1d11 16
deploy Qq MESA-DM 3d2 1d10 1d11 16
deploy Qq MESA-DM 5d2 1d10 1d11 16
deploy Qq MESA-DM 1d3 1d10 1d11 16


#######################################
### T
#######################################
# Tk: M_* = 1d1 -> 1d3, m_chi = 1d13, rho_chi = 1d16, and 16 threads
deploy Tk MESA-DM 1d1 1d13 1d16 16
deploy Tk MESA-DM 1d2 1d13 1d16 16
deploy Tk MESA-DM 3d2 1d13 1d16 16
deploy Tk MESA-DM 5d2 1d13 1d16 16
deploy Tk MESA-DM 1d3 1d13 1d16 16

# Tl: M_* = 1d1 -> 1d3, m_chi = 1d13, rho_chi = 1d15, and 16 threads
deploy Tl MESA-DM 1d1 1d13 1d15 16
deploy Tl MESA-DM 1d2 1d13 1d15 16
deploy Tl MESA-DM 3d2 1d13 1d15 16
deploy Tl MESA-DM 5d2 1d13 1d15 16
deploy Tl MESA-DM 1d3 1d13 1d15 16

# Tm: M_* = 1d1 -> 1d3, m_chi = 1d13, rho_chi = 1d14, and 16 threads
deploy Tm MESA-DM 1d1 1d13 1d14 16
deploy Tm MESA-DM 1d2 1d13 1d14 16
deploy Tm MESA-DM 3d2 1d13 1d14 16
deploy Tm MESA-DM 5d2 1d13 1d14 16
deploy Tm MESA-DM 1d3 1d13 1d14 16

# Tn: M_* = 1d1 -> 1d3, m_chi = 1d13, rho_chi = 1d14, and 16 threads
deploy Tn MESA-DM 1d1 1d13 1d13 16
deploy Tn MESA-DM 1d2 1d13 1d13 16
deploy Tn MESA-DM 3d2 1d13 1d13 16
deploy Tn MESA-DM 5d2 1d13 1d13 16
deploy Tn MESA-DM 1d3 1d13 1d13 16

echo $(qstat)
