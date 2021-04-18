#!/bin/bash
# this script:
# 1) creates new MESA work directories
# 2) inports templates for
#   -> inlist
#   -> submit.sh
#   -> history_columns.list
#   -> profile_columns.list
# 3) edits templates
# 4) copies inlist into log directory
# 5) imports run_star_extras and compiles
# 6) submits job

Help()
{
   # Display Help
   echo "This script:"
   echo "1) creates new MESA work directories,"
   echo "2) imports templates for:"
   echo "  -> inlist,"
   echo "  -> submit.sh,"
   echo "  -> history_columns.list,"
   echo "  -> profile_columns.list,"
   echo "3) edits templates to added specified parameters,"
   echo "4) copies inlist into log directory,"
   echo "5) imports run_star_extras and compiles,"
   echo "6) and submits the job."
   echo
   echo "syntax: deploy [NAME] [TEMP DIR] [STAR MASS] [DM MASS] [DM DENSITY] [THREADS]"
   echo
   echo "options:"
   echo "[NAME]         Name of run."
   echo "[TEMP DIR]     Dictory containing all templates."
   echo "[STAR MASS]    Inital mass of the star in solar masses."
   echo "[DM MASS]      Dark Matter mass in GeV."
   echo "[DM DENSITY]   Dark Matter density in GeV/cm^3."
   echo "[DM THREADS]   Number of threads to run on."
   echo
}

# get the options
while getopts ":h" option; do
   case $option in
      h) # display Help
         Help
         exit;;
     \?) # incorrect option
         echo "Error: Invalid option"
         exit;;
   esac
done

# read from commandline args
NAME=$1
DIR=$2
MASS=$3
MDM=$4
RHODM=$5
THREADS=$6

# name od the run
FULLNAME=$"$NAME$MASS"

# make a new MESA work DIR
new-star-work ${FULLNAME}
cp ${2}/inlists/inlist_template ${NAME}/inlist
cp ${2}/inlists/submit_template.sh ${NAME}/submit.sh
cp ${2}/inlists/history_columns.list ${NAME}/.
cp ${2}/inlists/profile_columns.list ${NAME}/.
cd ${NAME}

# fill out the relevant feilds of the inlist
set-inlist inlist ${NAME} ${MASS} ${MDM} ${RHODM}

# move inlist to LOGS directory so we have a copy for later
mkdir LOGS/${FULLNAME}
cp inlist LOGS/${FULLNAME}/.

# fill in the submit script
set-sub submit.sh ${FULLNAME} ${THREADS}

# move run_star_extras.f in and compile
place-cl-mk ${DIR}

# submit the job
qsub submit.sh 

echo "Hog #"$FULLNAME" has been notified of your location."
