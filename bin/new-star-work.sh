#!/bin/bash
# creates new work dir at $1
# 

# create the new directory
cp -r $MESA_DIR/star/work $1

# clean out what we don't need
rm $1/inlist*
rm $1/README*

