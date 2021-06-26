# *Under Construction*
Mostly hard coded to work with my cluster set up, planing to add a config file, amd some more inlist options to make it a more generically applicable tool.

# MESA-dispatcher
A set of bash and python scripts for painlessly submitting and analyzing many MESA runs at once.
As of now these scripts are really only hard coded to work with MESA runs using my `run_star_extras.f90` file for Dark Matter capture.
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

### `tuya.py`
Move `tuya.py` into your directory with `MESA` log directories in it. For example:
```
    |- tuya.py
    |- name
        |- history_name.data
        |- profiles.index
        |- profile1.index
        ...
        |- profile31.index
```
`./tuya.py -h` will print out the following help statement:
```
usage: tuya.py [-h] [-D str [str ...]] [--DMevo] [--DMheat] [--DMprof] [--cpu] [--HR]
               [--dMdt] [--dRdt] [--dLdt] [--dEddMaxdt] [--rho] [--P] [--T] [--L]
               [--Edd] [--beta] [--XYZ] [-n int] [--Arho] [--AP] [--AT] [--AL]
               [--AEdd] [--Abeta] [--AXYZ] [--poly float] [--Rnorm] [--dM] [--Mnorm]
               [--dMstar] [--no-annotate] [-f str] [-d] [-p] [-x float float]
               [-y float float] [--xlog] [--ylog] [--xlin] [--ylin] [--PDF]

optional arguments:
  -h, --help            show this help message and exit
  -D str [str ...], --dir str [str ...]
                        directory or directories containing data files
  --DMevo               plot DM params over time
  --DMheat              plot radial DM heating profile
  --DMprof              plot radial DM profile
  --cpu                 plot star time versus wall time
  --HR                  plot an HR diagram
  --dMdt                plot total mass over time
  --dRdt                plot total radius over time
  --dLdt                plot total luminosity over time, by source
  --dEddMaxdt           plot maximum Eddington factor over time
  --rho                 plot radial density profile
  --P                   plot radial pressure profile
  --T                   plot radial temperature profile
  --L                   plot radial luminosity profile, by source
  --Edd                 plot radial Eddington factor profile
  --beta                plot radial beta (P_gas/P) profile
  --XYZ                 plot radial composition profile
  -n int, --number int  how many profiles to plot, equispaced by interest
  --Arho                animate radial density profile
  --AP                  animate radial pressure profile
  --AT                  animate radial temperature profile
  --AL                  animate radial luminosity profile, by source
  --AEdd                animate radial Eddington factor profile
  --Abeta               animate radial beta (P_gas/P) profile
  --AXYZ                animate radial composition profile
  --poly float          add a polytrope with specified index to plots
  --Rnorm               normalize all radial profiles to R_star
  --dM                  use enclosed mass instead of radius for all profiles
  --Mnorm               use with --dM, normalize all profiles to M_star
  --dMstar              use M_star instead of time for evolution plots
  --no-annotate         turn all anotations off
  -f str, --filename str
                        filename for the plots to be produced
  -d, --dark            use dark theme for plots
  -p, --plain           use plain theme for plots
  -x float float, --xaxis float float
                        manually set x axis, min and max
  -y float float, --yaxis float float
                        manually set y axis, min and max
  --xlog                force log scale on x axis
  --ylog                force log scale on y axis
  --xlin                force lin scale on x axis
  --ylin                force lin scale on y axis
  --PDF                 produce PDFs of the plots
```
To create a simple HR plot, one would simply run `./tuya.py -D name --HR`, and more complicated options can be added as needed.


