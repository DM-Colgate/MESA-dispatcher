#!/bin/bash
# example of a script to launch a batch of MESA runs on the cluster at once


echo "Dispatching feral hogs... please prepare for deallocation."

# AA: M_* = 1d1 -> 1d3, m_chi = 1d10, rho_chi = 1d16, and 16 threads
deploy AA MESA-DM 1d1 1d10 1d16 16
deploy AA MESA-DM 2d1 1d10 1d16 16
deploy AA MESA-DM 3d1 1d10 1d16 16
deploy AA MESA-DM 5d1 1d10 1d16 16
deploy AA MESA-DM 7d1 1d10 1d16 16
deploy AA MESA-DM 1d2 1d10 1d16 16
deploy AA MESA-DM 2d2 1d10 1d16 16
deploy AA MESA-DM 3d2 1d10 1d16 16
deploy AA MESA-DM 5d2 1d10 1d16 16
deploy AA MESA-DM 5d2 1d10 1d16 16
deploy AA MESA-DM 7d2 1d10 1d16 16
deploy AA MESA-DM 1d3 1d10 1d16 16

echo $(qstat)
