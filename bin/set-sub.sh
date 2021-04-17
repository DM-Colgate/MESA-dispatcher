#!/bin/bash
# $2 name
# $3 number of nodes

# find what line ppn is on
LINE=$(cat $1 | grep -hnr "ppn" | tail -1 | cut -d ":" -f1)

# pop
sed -i '/ppn/d' ./${1}

# compose
WORDS="i#PBS\ -l\ nodes=1:ppn="
NODE="$LINE$WORDS$3"

# add new line
sed -i "${NODE}" ${1}



# find what line threads is on
LINE=$(cat $1 | grep -hnr "OMP_NUM_THREADS" | tail -1 | cut -d ":" -f1)

# pop
sed -i '/OMP_NUM_THREADS/d' ./${1}

# compose
WORDS="iexport\ OMP_NUM_THREADS="
NEW="$LINE$WORDS$3"

# add new line
sed -i "${NEW}" ${1}



# find what line name is on
LINE=$(cat $1 | grep -hnr "\-N" | tail -1 | cut -d ":" -f1)

# pop
sed -i '/-N/d' ./${1}

# compose
WORDS="i#PBS\ -N\ MESA_"
NEW="$LINE$WORDS$2"

# add new line
sed -i "${NEW}" ${1}

