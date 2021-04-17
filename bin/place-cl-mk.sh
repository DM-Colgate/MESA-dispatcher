#!/bin/bash

cp ../${1}/run_star_extras_src/capture.f src/run_star_extras.f
./clean
./mk
