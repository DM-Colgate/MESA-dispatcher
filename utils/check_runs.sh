#!/bin/bash

RUNS=$(qstat | grep "ibania.*\R" | cut -d " " -f7 | cut -d "_" -f2)

for f in $RUNS; do
        echo $f
done
