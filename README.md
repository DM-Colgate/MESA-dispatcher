# *Under Construction*
Mostly hard coded to work with my cluster set up, planing to add a config file, amd some more inlist options to make it a more universally applicable tool.

# MESA-dispatcher
A set of bash and python scripts for painlessly submitting and analyzing many MESA runs at once.
As of now these scripts are really only hard coded to work with MESA runs using my `run_star_extras.f` for Dark Matter capture.
But by making a few changes to the sed commands in `set-inlist.sh` one could pretty easily alter this to be able to edit any inlist parameters. 

## Installation
1) Clone the repository on the cluster:
```
git clone https://github.com/deionizedoatmeal/MESA-dispatcher.git
```
2) Execute the install script to move utilities to your bin:
```
./MESA-dispatcher/install.sh
```

## Usage
### `deploy.sh`
```
This script:
1) creates new MESA work directories,
2) imports templates for:
  -> inlist,
  -> submit.sh,
  -> history_columns.list,
  -> profile_columns.list,
3) edits templates to added specified parameters,
4) copies inlist into log directory,
5) imports run_star_extras and compiles,
6) and submits the job.

syntax: deploy [NAME] [TEMP DIR] [STAR MASS] [DM MASS] [DM DENSITY] [THREADS]

options:
[NAME]         Name of run.
[TEMP DIR]     Dictory containing all templates.
[STAR MASS]    Inital mass of the star in solar masses.
[DM MASS]      Dark Matter mass in GeV.
[DM DENSITY]   Dark Matter density in GeV/cm^3.
[DM THREADS]   Number of threads to run on.
```
This can be printed out with `deploy -h`.
Example usage as follows:
```
deploy DK MESA_inlists 1d1 1d11 1d14 32
```
This is intended to be used in a larger script, such as the example in `batch.sh`.

