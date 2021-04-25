#!/bin/bash
# example of a script to launch a batch of MESA runs on the cluster at once


echo "Dispatching feral hogs... please prepare for deallocation."

deploy 4.13. MESA-DM 7d2 1d4 1d13 8 16
deploy 4.14. MESA-DM 7d2 1d4 1d14 8 16
deploy 4.15. MESA-DM 7d2 1d4 1d15 8 16
deploy 4.16. MESA-DM 7d2 1d4 1d16 8 16

deploy 6.13. MESA-DM 7d2 1d6 1d13 8 16
deploy 6.14. MESA-DM 7d2 1d6 1d14 8 16
deploy 6.15. MESA-DM 7d2 1d6 1d15 8 16
deploy 6.16. MESA-DM 7d2 1d6 1d16 8 16

deploy 8.13. MESA-DM 7d2 1d8 1d13 8 16
deploy 8.14. MESA-DM 7d2 1d8 1d14 8 16
deploy 8.15. MESA-DM 7d2 1d8 1d15 8 16
deploy 8.16. MESA-DM 7d2 1d8 1d16 8 16

deploy 10.13. MESA-DM 7d2 1d10 1d13 8 16
deploy 10.14. MESA-DM 7d2 1d10 1d14 8 16
deploy 10.15. MESA-DM 7d2 1d10 1d15 8 16
deploy 10.16. MESA-DM 7d2 1d10 1d16 8 16

deploy 12.13. MESA-DM 7d2 1d12 1d13 8 16
deploy 12.14. MESA-DM 7d2 1d12 1d14 8 16
deploy 12.15. MESA-DM 7d2 1d12 1d15 8 16
deploy 12.16. MESA-DM 7d2 1d12 1d16 8 16

deploy 14.13. MESA-DM 7d2 1d14 1d13 8 16
deploy 14.14. MESA-DM 7d2 1d14 1d14 8 16
deploy 14.15. MESA-DM 7d2 1d14 1d15 8 16
deploy 14.16. MESA-DM 7d2 1d14 1d16 8 16


echo $(qstat)
