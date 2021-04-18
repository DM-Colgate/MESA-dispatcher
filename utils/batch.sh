#!/bin/bash
# example of a script to launch a batch of MESA runs on the cluster at once


echo "Dispatching feral hogs... please prepare for deallocation."

# AA: m_chi = 1d3 and rho_chi = 1d6
deploy AA 1d0 1d3 1d6 16
deploy AA 3d0 1d3 1d6 16
deploy AA 3d0 1d3 1d6 16
deploy AA 5d0 1d3 1d6 16
deploy AA 1d1 1d3 1d6 16
deploy AA 3d1 1d3 1d6 16
deploy AA 5d1 1d3 1d6 16
deploy AA 1d2 1d3 1d6 16
deploy AA 3d2 1d3 1d6 16
deploy AA 5d2 1d3 1d6 16
deploy AA 1d3 1d3 1d6 16

# AB: m_chi = 1d3 and rho_chi = 1d7
deploy AB 1d0 1d3 1d7 16
deploy AB 3d0 1d3 1d7 16
deploy AB 3d0 1d3 1d7 16
deploy AB 5d0 1d3 1d7 16
deploy AB 1d1 1d3 1d7 16
deploy AB 3d1 1d3 1d7 16
deploy AB 5d1 1d3 1d7 16
deploy AB 1d2 1d3 1d7 16
deploy AB 3d2 1d3 1d7 16
deploy AB 5d2 1d3 1d7 16
deploy AB 1d3 1d3 1d7 16

echo $(qstat)
